# 離線防禦實作包

版本：1.0.0｜編製與指定測試：2026-09-19｜Python 3.10 以上｜僅使用標準函式庫。

## 開始

解壓縮後，在含有本 README.md 與 run_labs.py 的目錄開啟終端機：

```text
python run_labs.py --all
python run_labs.py --case gtg50014
python run_labs.py --case gtg14020
python run_labs.py --case gtg50020
```

在課程原始碼根目錄，可改用 `python course/labs/run_labs.py --all`。不需要任何 API key、網路、雲端帳號或額外套件。工具只讀取資料，輸出 JSON 到螢幕；不會解析目的地、執行事件內容、讀取系統秘密或封鎖帳號。

## 材料

- `data/<case>/events.jsonl`：學員先讀的合成日誌，每行一個 JSON object。
- `data/<case>/scenarios.json`：教學者設定的情境真值；完成第一次判讀後才開啟。
- `data/<case>/expected.json`：獨立預先寫好的告警 ID、證據 ID 與 entity 層級混淆矩陣，含刻意的誤報／漏報。
- `templates/case-*-response.md`：三案專屬回應表；`evidence-ledger.csv` 為共用證據帳本。
- `templates/module-*.csv`：其他模組的專屬紙上作業素材，非真實事件資料。
- `templates/rubric.csv`：100 分共用評分規準。個案細分標準見網站講師頁。

網站教材入口：https://jack51706.github.io/ai-misuse-threat-intel-course/#10-practice/00-practice-guide.html

## Schema 與觀察限制

每筆事件必須有唯一 `id`、帶時區的 ISO 8601 `timestamp`、非空 `entity`、規則支援的 `event` 與 `attrs`。程式先驗證型別，再按時間與 ID 排序。同一 entity 在本資料內代表一個情境；沒有跨平台身分歸因。

50014 使用 signin 的 session/ip/asn/success 及 privileged_export 的 session。50014 的 IP 是文件示例位址；只做字串比較，不解析或定位。

14020 只使用 profile_metadata 的 template/subject_ref/sensitive_attribute/coercion_tag；風險標籤由教學者預先指定，不是模型分析結果，不含真人資料。

50020 使用 tool_result 的 trusted、secret_read 的 marker，以及 egress 的 destination/canary_present。LAB_CANARY 沒有任何權限；目的地以 .invalid 結尾，只是資料，不進行外連。允許清單是完全相等比較，不支援萬用字元。

## 如何解讀輸出

每案含 5 個情境；三案共 45 筆事件。預期每案觸發 a 與 d，a 是 TP，d 是已知 FP，b/c 為 TN，e 是已知 FN。因此每案 precision=0.5、recall=0.5。這是教學者手工設計的資料，不能當正式環境準確率。

`expected_match=true` 表示告警、證據 ID、混淆矩陣與指定結果一致，包含預先設計的誤報及漏報。告警的 `disposition=human_review_only` 只是輸出文字，沒有自動處置。

- 回傳 0：所有指定結果一致。
- 回傳 1：結果與 expected 不一致；修改合成資料後也可能是合理差異，須人工說明。
- 回傳 2：輸入資料、欄位或檔案有問題。

## 變體測試與驗收

先保留原始資料，複製 data 目錄後在副本調整時間、session、template 或核准目的地，再執行 `python run_labs.py --case gtg50014 --data-dir <副本資料夾>`。副本資料夾底下仍須有 gtg50014 子目錄。不用修改真實帳號或模型，也不要為了拿到回傳 0 而抹掉 known_false_positives／known_false_negatives。

課程原始碼另外含 `course/tests/test_labs.py`，檢查時間窗邊界、跨 session/job 隔離、正常對照、資料錯誤與 CLI 行為：`python -m unittest discover -s course/tests -p test_labs.py -v`。下載包的日常驗收用 `--all` 即可。

## 測試聲明

指定測試通過只適用本包規則與合成資料。沒有驗證 Sentinel／Sigma 後端、真實日誌 schema、NER、語意分類器、DLP、正式環境誤報率或實際防禦成效。不得把合成標籤或教學門檻歸為原報告的觀察。
