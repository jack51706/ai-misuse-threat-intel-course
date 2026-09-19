#!/usr/bin/env python3
"""Offline teaching detectors. Reads synthetic JSON only; never connects to services."""
import argparse
from collections import defaultdict
from datetime import datetime, timedelta
import json
from pathlib import Path
import sys

CASES = ("gtg50014", "gtg14020", "gtg50020")
DATA_DIR = Path(__file__).resolve().parent / "data"
RULE_VERSION = "1.0.0"
EVENT_TYPES = {
    "gtg50014": {"signin", "privileged_export"},
    "gtg14020": {"profile_metadata"},
    "gtg50020": {"tool_result", "secret_read", "egress"},
}


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("timestamp must be an ISO 8601 string")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamps must include a timezone")
    return parsed


def validate_events(case, events):
    seen = set()
    for event in events:
        if not isinstance(event, dict):
            raise ValueError("each event must be an object")
        for key in ("id", "entity", "event", "timestamp"):
            if not isinstance(event.get(key), str) or not event[key]:
                raise ValueError("event requires a nonempty string: " + key)
        if event["id"] in seen:
            raise ValueError("duplicate event id: " + event["id"])
        seen.add(event["id"])
        timestamp(event["timestamp"])
        if event["event"] not in EVENT_TYPES[case]:
            raise ValueError("unexpected event type: " + event["event"])
        attrs = event.get("attrs")
        if not isinstance(attrs, dict):
            raise ValueError("attrs must be an object")
        required = {
            "signin": {"session": str, "ip": str, "asn": int, "success": bool},
            "privileged_export": {"session": str},
            "profile_metadata": {"template": str, "subject_ref": str,
                                 "sensitive_attribute": bool, "coercion_tag": bool},
            "tool_result": {"trusted": bool},
            "secret_read": {"marker": str},
            "egress": {"destination": str, "canary_present": bool},
        }[event["event"]]
        for key, kind in required.items():
            if type(attrs.get(key)) is not kind:
                raise ValueError("invalid attribute type: " + event["id"] + "/" + key)
            if kind is str and not attrs[key]:
                raise ValueError("empty attribute: " + key)
    return sorted(events, key=lambda e: (timestamp(e["timestamp"]), e["id"]))


def alert(rule, entity, evidence):
    return {"rule_id": rule, "entity": entity,
            "evidence_ids": [e["id"] for e in evidence],
            "disposition": "human_review_only"}


def detect_50014(events):
    """Changed IP and ASN in one session, followed by an export, within 15 min."""
    groups = defaultdict(list)
    for event in events:
        groups[(event["entity"], event["attrs"]["session"])].append(event)
    alerts = []
    for (entity, _), group in sorted(groups.items()):
        matched = False
        for index, first in enumerate(group):
            if first["event"] != "signin" or not first["attrs"]["success"]:
                continue
            for j in range(index + 1, len(group)):
                second = group[j]
                if second["event"] != "signin" or not second["attrs"]["success"]:
                    continue
                if timestamp(second["timestamp"]) <= timestamp(first["timestamp"]):
                    continue
                a, b = first["attrs"], second["attrs"]
                if a["ip"] == b["ip"] or a["asn"] == b["asn"]:
                    continue
                for last in group[j + 1:]:
                    elapsed = timestamp(last["timestamp"]) - timestamp(first["timestamp"])
                    if (last["event"] == "privileged_export" and elapsed <= timedelta(minutes=15)
                            and timestamp(last["timestamp"]) > timestamp(second["timestamp"])):
                        alerts.append(alert("LAB-50014-01", entity, [first, second, last]))
                        matched = True
                        break
                if matched:
                    break
            if matched:
                break
    return alerts


def detect_14020(events):
    """Four distinct synthetic subjects and two risk tags in one 30-min template."""
    groups = defaultdict(list)
    for event in events:
        groups[(event["entity"], event["attrs"]["template"])].append(event)
    alerts = []
    for (entity, _), group in sorted(groups.items()):
        for index, final in enumerate(group):
            cutoff = timestamp(final["timestamp"]) - timedelta(minutes=30)
            window = [e for e in group[:index + 1] if timestamp(e["timestamp"]) >= cutoff]
            subjects = {e["attrs"]["subject_ref"] for e in window}
            flagged = [e for e in window if e["attrs"]["sensitive_attribute"]
                       and e["attrs"]["coercion_tag"]]
            if len(subjects) >= 4 and len(flagged) >= 2:
                alerts.append(alert("LAB-14020-01", entity, window))
                break
    return alerts


def detect_50020(events):
    """Untrusted input -> synthetic secret-read -> disallowed canary egress, 10 min."""
    approved = {"model-gateway.invalid", "audit-archive.invalid"}
    groups = defaultdict(list)
    for event in events:
        groups[event["entity"]].append(event)
    alerts = []
    for entity, group in sorted(groups.items()):
        matched = False
        for i, first in enumerate(group):
            if first["event"] != "tool_result" or first["attrs"]["trusted"]:
                continue
            for j in range(i + 1, len(group)):
                second = group[j]
                if second["event"] != "secret_read" or second["attrs"]["marker"] != "LAB_CANARY":
                    continue
                if timestamp(second["timestamp"]) <= timestamp(first["timestamp"]):
                    continue
                for last in group[j + 1:]:
                    if last["event"] != "egress":
                        continue
                    attrs = last["attrs"]
                    elapsed = timestamp(last["timestamp"]) - timestamp(first["timestamp"])
                    if (elapsed <= timedelta(minutes=10) and attrs["canary_present"]
                            and timestamp(last["timestamp"]) > timestamp(second["timestamp"])
                            and attrs["destination"] not in approved):
                        alerts.append(alert("LAB-50020-01", entity, [first, second, last]))
                        matched = True
                        break
                if matched:
                    break
            if matched:
                break
    return alerts


DETECTORS = {"gtg50014": detect_50014, "gtg14020": detect_14020, "gtg50020": detect_50020}


def detect(case, events):
    if case not in CASES:
        raise ValueError("unknown case")
    validated = validate_events(case, events)
    return sorted(DETECTORS[case](validated), key=lambda a: (a["entity"], a["evidence_ids"]))


def evaluate(alerts, scenarios):
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("scenarios must be a nonempty list")
    truth = {}
    for row in scenarios:
        if (not isinstance(row, dict) or not isinstance(row.get("entity"), str)
                or not row["entity"] or row["entity"] in truth
                or row.get("class") not in ("benign", "simulated_abuse")):
            raise ValueError("invalid or duplicate scenario")
        truth[row["entity"]] = row["class"] == "simulated_abuse"
    predicted = {a["entity"] for a in alerts}
    if predicted - truth.keys():
        raise ValueError("alert entity missing from scenario labels")
    counts = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
    for entity, positive in truth.items():
        key = ("t" if (entity in predicted) == positive else "f") + ("p" if entity in predicted else "n")
        counts[key] += 1
    precision_den = counts["tp"] + counts["fp"]
    recall_den = counts["tp"] + counts["fn"]
    return {**counts, "precision": counts["tp"] / precision_den if precision_den else None,
            "recall": counts["tp"] / recall_den if recall_den else None,
            "unit": "synthetic_scenario_entity"}


def run_case(case, data_dir=DATA_DIR):
    folder = Path(data_dir) / case
    events = [json.loads(line) for line in (folder / "events.jsonl").read_text(encoding="utf-8").splitlines()
              if line.strip()]
    scenarios = json.loads((folder / "scenarios.json").read_text(encoding="utf-8"))
    expected = json.loads((folder / "expected.json").read_text(encoding="utf-8"))
    alerts = detect(case, events)
    if {e["entity"] for e in events} != {s["entity"] for s in scenarios}:
        raise ValueError("event entities must match labeled scenarios")
    metrics = evaluate(alerts, scenarios)
    match = alerts == expected["alerts"] and metrics == expected["metrics"]
    return {"case": case, "rule_version": RULE_VERSION, "event_count": len(events),
            "scenario_count": len(scenarios), "expected_match": match,
            "alerts": alerts, "metrics": metrics,
            "scope": "synthetic fixtures only; not production efficacy"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--all", action="store_true")
    choice.add_argument("--case", choices=CASES)
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR)
    args = parser.parse_args(argv)
    try:
        results = [run_case(case, args.data_dir) for case in (CASES if args.all else (args.case,))]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("Invalid lab data: " + str(exc), file=sys.stderr)
        return 2
    print(json.dumps({"labs": results}, ensure_ascii=False, indent=2))
    return 0 if all(r["expected_match"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
