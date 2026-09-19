"""Real local-fixture checks for offline teaching detectors; no service calls."""
import contextlib
import copy
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "labs"))
import run_labs as labs


def fixture(case, suffix="a"):
    rows = [json.loads(line) for line in (labs.DATA_DIR / case / "events.jsonl").read_text(encoding="utf-8").splitlines()]
    return [row for row in rows if row["entity"] == case + "-" + suffix]


class FixtureTests(unittest.TestCase):
    def test_all_hand_authored_expected_results_match(self):
        for case in labs.CASES:
            with self.subTest(case=case):
                result = labs.run_case(case)
                self.assertTrue(result["expected_match"])
                self.assertEqual([a["entity"] for a in result["alerts"]], [case + "-a", case + "-d"])
                self.assertEqual({k: result["metrics"][k] for k in ("tp", "fp", "tn", "fn")},
                                 {"tp": 1, "fp": 1, "tn": 2, "fn": 1})
                self.assertTrue(all(a["disposition"] == "human_review_only" for a in result["alerts"]))

    def test_input_order_does_not_change_evidence(self):
        for case in labs.CASES:
            events = fixture(case)
            self.assertEqual(labs.detect(case, events), labs.detect(case, list(reversed(events))))

    def test_known_error_metadata_is_explicit_and_matches_labels(self):
        for case in labs.CASES:
            expected = json.loads((labs.DATA_DIR / case / "expected.json").read_text(encoding="utf-8"))
            labels = {row["entity"]: row["class"] for row in json.loads(
                (labs.DATA_DIR / case / "scenarios.json").read_text(encoding="utf-8"))}
            self.assertEqual(expected["known_false_positives"][0]["entity"], case + "-d")
            self.assertEqual(labels[case + "-d"], "benign")
            self.assertEqual(expected["known_false_negatives"][0]["entity"], case + "-e")
            self.assertEqual(labels[case + "-e"], "simulated_abuse")

    def test_equal_timestamps_do_not_establish_a_causal_sequence(self):
        for case in ("gtg50014", "gtg50020"):
            events = fixture(case)
            for row in events:
                row["timestamp"] = events[0]["timestamp"]
            self.assertEqual(labs.detect(case, events), [])

    def test_failed_signin_does_not_complete_50014_chain(self):
        events = fixture("gtg50014")
        events[1]["attrs"]["success"] = False
        self.assertEqual(labs.detect("gtg50014", events), [])

    def test_50014_must_use_same_session(self):
        events = fixture("gtg50014")
        events[-1]["attrs"]["session"] = "another-session"
        self.assertEqual(labs.detect("gtg50014", events), [])

    def test_50014_window_boundary(self):
        events = fixture("gtg50014")
        events[-1]["timestamp"] = "2026-01-01T00:15:00Z"
        self.assertEqual(len(labs.detect("gtg50014", events)), 1)
        events[-1]["timestamp"] = "2026-01-01T00:15:01Z"
        self.assertEqual(labs.detect("gtg50014", events), [])

    def test_14020_repetition_of_one_person_does_not_meet_distinct_threshold(self):
        events = fixture("gtg14020")
        for row in events:
            row["attrs"]["subject_ref"] = "one-fictional-subject"
        self.assertEqual(labs.detect("gtg14020", events), [])

    def test_14020_different_templates_are_not_combined(self):
        events = fixture("gtg14020")
        events[-1]["attrs"]["template"] = "unrelated-template"
        self.assertEqual(labs.detect("gtg14020", events), [])

    def test_14020_window_boundary(self):
        events = fixture("gtg14020")
        events[-1]["timestamp"] = "2026-01-01T00:30:00Z"
        self.assertEqual(len(labs.detect("gtg14020", events)), 1)
        events[-1]["timestamp"] = "2026-01-01T00:30:01Z"
        self.assertEqual(labs.detect("gtg14020", events), [])

    def test_14020_sensitive_attributes_alone_do_not_trigger(self):
        events = fixture("gtg14020")
        for row in events:
            row["attrs"]["coercion_tag"] = False
        self.assertEqual(labs.detect("gtg14020", events), [])

    def test_50020_requires_evidence_chain_in_order(self):
        events = fixture("gtg50020")
        self.assertEqual(labs.detect("gtg50020", [events[0], events[-1]]), [])
        events[1]["timestamp"] = "2025-12-31T23:59:00Z"
        self.assertEqual(labs.detect("gtg50020", events), [])

    def test_50020_allowlist_is_exact_and_canary_is_required(self):
        events = fixture("gtg50020")
        events[-1]["attrs"]["destination"] = "model-gateway.invalid"
        self.assertEqual(labs.detect("gtg50020", events), [])
        events[-1]["attrs"]["destination"] = "model-gateway.invalid.other.invalid"
        self.assertEqual(len(labs.detect("gtg50020", events)), 1)
        events[-1]["attrs"]["canary_present"] = False
        self.assertEqual(labs.detect("gtg50020", events), [])

    def test_50020_window_boundary(self):
        events = fixture("gtg50020")
        events[-1]["timestamp"] = "2026-01-01T00:10:00Z"
        self.assertEqual(len(labs.detect("gtg50020", events)), 1)
        events[-1]["timestamp"] = "2026-01-01T00:10:01Z"
        self.assertEqual(labs.detect("gtg50020", events), [])

    def test_50020_does_not_correlate_separate_jobs(self):
        events = fixture("gtg50020")
        events[-1]["entity"] = "separate-job"
        self.assertEqual(labs.detect("gtg50020", events), [])

    def test_bad_or_ambiguous_event_data_is_rejected(self):
        original = fixture("gtg50014")
        changes = [("timestamp", "2026-01-01T00:00:00"), ("event", "run-command"), ("attrs", {}), ("entity", "")]
        for key, value in changes:
            events = copy.deepcopy(original)
            events[0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                labs.detect("gtg50014", events)
        with self.assertRaises(ValueError):
            labs.detect("gtg50014", original + [original[0]])
        events = copy.deepcopy(original)
        events[0]["attrs"]["asn"] = True
        with self.assertRaises(ValueError):
            labs.detect("gtg50014", events)

    def test_metrics_do_not_invent_precision_when_no_alerts(self):
        metrics = labs.evaluate([], [{"entity": "normal", "class": "benign"}])
        self.assertIsNone(metrics["precision"])
        self.assertIsNone(metrics["recall"])
        self.assertEqual(metrics["tn"], 1)

    def test_cli_runs_all_and_only_reads_fixtures(self):
        before = {p: p.read_bytes() for p in labs.DATA_DIR.rglob("*") if p.is_file()}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(labs.main(["--all"]), 0)
        self.assertEqual(len(json.loads(output.getvalue())["labs"]), 3)
        after = {p: p.read_bytes() for p in labs.DATA_DIR.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_cli_reports_expected_mismatch_and_invalid_data(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / "gtg50014"
            shutil.copytree(labs.DATA_DIR / "gtg50014", folder)
            expected = json.loads((folder / "expected.json").read_text(encoding="utf-8"))
            expected["alerts"] = []
            (folder / "expected.json").write_text(json.dumps(expected), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(labs.main(["--case", "gtg50014", "--data-dir", directory]), 1)
            (folder / "events.jsonl").write_text("not-json\n", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(labs.main(["--case", "gtg50014", "--data-dir", directory]), 2)


if __name__ == "__main__":
    unittest.main()
