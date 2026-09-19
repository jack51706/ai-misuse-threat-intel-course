# 編輯紀錄

`catalog.json` 是網站使用的逐頁審核登錄，不是自動產生的批准清單。

- `schema_version` 為 1，`pages` 以 course 相對 Markdown 路徑作 key。
- `content_sha256` 指向紀錄所述範圍的檢查版本；換行正規化，只有模組 09 導論的自動 LEDGER 區段除外。一般教材即使含同名標記仍計入完整雜湊。
- `checked_on` 只記結構／編輯檢查日期。`scope` 明說本次範圍，`pending` 保留待驗證事項，`changes` 記重要修訂。
- `source_checked_on` 可空白；有值時必須有 `source_check_scope`，僅能寫實際取得並核對的項目。不能將指定段落複核寫成全文事實認證。
- `detection_level` 說明偵測成熟度。合成資料通過，不升級為正式部署。

新增或變更教材會自動顯示待審。維護者先核對差異與來源，再用 `python course/check_content.py --fingerprint 相對/教材.md` 取得版本雜湊；不要在 CI、建置腳本或排程研究中自動重填全站雜湊。

其他 JSON 是本次工作的勘誤與指定來源複核證據，用來支持 catalog 的範圍。它們本身不會自動批准教材。網站公開的是每頁的範圍與待驗證資訊及 `_shared/05-editorial-review-and-changelog.md`，不直接上傳整個 editorial 目錄。
