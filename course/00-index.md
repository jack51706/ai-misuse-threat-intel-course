# 課程總索引：偵測與反制 AI 濫用（Anthropic 2026 年 9 月威脅報告深度教材）

> 課程主題：解析 Anthropic 於 2026-09-10 同日發布的兩份文件，作為資安、威脅情報、AI 治理與台灣國安防禦的教學教材。
> 教材初版：2026-09-13；閱讀分層、證據規範與實作更新：2026-09-19。各頁列出實際核對範圍，尚未逐項複核的來源維持待驗證。
> 讀者定位：台灣的資安專業人士、SOC/CTI 團隊、政策與國安分析者、以及開設相關課程的講師。

---

## 一、這套教材是什麼

本教材把兩份一手文件拆解成 **8 個核心模組、48 份獨立教材**，另有持續增補的**模組 09 延伸研究**與跨案例專題。核心教材圍繞以下面向展開：一頁速覽、行為者側寫與歸因、受害者清單、AI 濫用的攻擊生命週期、TTP 與 MITRE ATT&CK 對應、**圖表逐一判讀**、IOC 與技術指標、Anthropic 的偵測與防線缺口、第三方驗證、課程教學設計、關鍵原文引文、研究限制。

三個貫穿全教材的製作原則：

1. **圖表親自判讀**：報告的 51 張圖表有大量關鍵數字**只存在於圖片內、PDF 文字層抓不到**（例如某監控案「30 天 2,475 份成品、16 名分析師縮為 1 人」只在圖說裡；某常規武器案對美國具安全許可工程師建檔只在情報循環圖裡）。每份教材都用渲染圖親自判讀對應圖表。
2. **一手為準、第三方查證**：所有主張以 PDF 原文為準，並標明每個第三方來源是「獨立查證」還是「僅引述 Anthropic」。**這是本教材最重要的情報紀律**——全報告絕大多數案例是**單一來源情報**（只有 Anthropic 的平台側遙測），少數有外部佐證（如某商業間諜軟體案有 Forbidden Stories 的獨立調查、某俄羅斯間諜案的惡意程式雜湊與微軟報告完全一致）。
3. **安全紅線**：所有 IOC（網域、IP、Telegram 帳號、雜湊）一律保留報告原本的 defang 格式抄錄，全程不對任何指標連線或查詢；涉及武器與生物的教材只寫治理、偵測與政策，不記述任何可操作的技術內容。

---

## 二、兩份一手文件

| 項目 | 威脅情報報告 | 常規武器能力研究 |
|---|---|---|
| 標題 | Detecting and countering misuse of AI: September 2026 | Measuring tactical intelligence targeting and conventional weapons capabilities of AI models |
| 發布 | 2026-09-10 | 2026-09-10 |
| 單位 | Threat Intelligence Team | Frontier Red Team |
| 形式 | 154 頁 PDF（本目錄內） | 網頁長文 |
| 涵蓋 | 2025-12 至 2026-08，七大危害領域 | 能力評測（情報鎖定 + 常規武器） |
| 涉及模型 | Claude Haiku / Sonnet / Opus；除一起蒸餾案外未涉 Fable / Mythos | Sonnet 5、Opus 5、Mythos 5、Mythos Preview；對照 Kimi K3、GLM 5.2 |

兩份文件互相呼應：能力研究測「模型可能做什麼」，威脅報告記「有人實際做了什麼」。這兩種證據類型的互補與各自局限，是本課程的方法論核心。

---

## 三、完整模組地圖（核心 48 份教材，另含延伸研究）

### 模組 01：網路行動（Cyber operations）— 7 份
- `01-cyber/00-cyber-trends-and-skills.md` — 章節導論：三大趨勢、uplift 三軸、Appendix A 武器化 skills 清單、四份威脅報告演進
- `01-cyber/GTG-20006-russian-espionage.md` — 俄羅斯國家級間諜（關聯 Midnight Blizzard），AI 自主逃避偵測閉環、CaptiveCrunch
- `01-cyber/GTG-50014-shinyhunters.md` — ShinyHunters 附屬的犯罪產業鏈，六階段流程圖組（全報告最完整）
- `01-cyber/GTG-10007-exploit-foundry.md` — 中國學生級行為者，agent swarm 與自主零日鑄造廠
- `01-cyber/GTG-50021-fake-reseller.md` — 假 Claude 轉售商 + 憑證收割；AI 供應鏈 Loot/Compute/Cover 框架
- `01-cyber/GTG-50020-ai-supply-chain.md` — 財務動機行為者轉向 AI 產業，評測沙箱 prompt injection 竊金鑰
- `01-cyber/GTG-50029-hacktivist.md` — 單一法語 hacktivist 打出國家級規模，WordPress race condition、doxxing 平台

### 模組 02：影響力行動（Influence operations）— 10 份
- `02-influence/00-influence-intro-and-breakout-scale.md` — 章節導論：定義、上游偵測、Breakout Scale 六級量表、九案評級
- `02-influence/GTG-04001-russia-car-fimi.md` — 俄羅斯在中非共和國的 FIMI（全報告唯一 Category Four）
- `02-influence/GTG-54002-influence-as-a-service.md` — 商業「影響力即服務」，六大洲、法國 LKM Company
- `02-influence/GTG-84005-malaysia-election-platform.md` — 商業選舉操縱平台，馬來西亞 222 選區、伊斯坦堡 BBS
- `02-influence/GTG-24015-russian-state-media.md` — 俄羅斯國家媒體編輯管線（唯一能逐字對上實際發布內容的案例）
- `02-influence/GTG-34001-iran-icco.md` — 伊朗國家對齊，soft war 與 Jihad al-Tabyin 教義框架
- `02-influence/GTG-54006-bangladesh-awami-league.md` — 孟加拉單一操作者，`fake_news_3.py`、鎖定低識字受眾
- `02-influence/GTG-84006-mek-ncri-viktor.md` — MEK/NCRI 對齊，共享 AI 代理平台「Viktor」、冒充真人（對個人風險最高）
- `02-influence/GTG-54004-kenya-cib.md` — 肯亞為 2027 大選預備的協同不實行為
- `02-influence/GTG-84002-uae-muslim-brotherhood.md` — 阿聯指揮，滲透聯合國人權機制、側寫歐洲議會議員

### 模組 03：監控行動（Surveillance operations）— 9 份
- `03-surveillance/00-surveillance-intro.md` — 章節導論：三類行為者、AI 取代工程人力、四種防線失效模式
- `03-surveillance/GTG-54009-s2t-commercial-spyware.md` — 商業監控平台（關聯 S2T），六類編碼群體、監控+敘事一體化
- `03-surveillance/GTG-14010-uyghurs-syria.md` — 中國對敘利亞維吾爾人的監控與招募，AI 作為社交工程品管員
- `03-surveillance/GTG-14020-religious-affairs-taiwan-church.md` — **中國宗教事務情報，點名台灣基督長老教會領導層、場所偵察**
- `03-surveillance/GTG-14021-weiwen-transnational-repression.md` — 中國維穩與跨境鎮壓，三子行動、重新提示突破防線的最清楚證據
- `03-surveillance/GTG-14022-public-opinion-monitoring-taiwan.md` — **中國輿情監控，點名台灣政治人物、三戰框架**
- `03-surveillance/GTG-34007-iran-surveillance.md` — 伊朗兩單位，Arman 案件管理系統、偽裝禱告工具的惡意擴充
- `03-surveillance/GTG-50027-mali-mass-interception.md` — 馬利國家情報機關的全民攔截平台，AI 參與拆除法院令狀要求
- `03-surveillance/GTG-30004-30005-30006-osint-recon.md` — 三個伊朗關聯案（OSINT/海軍偵察/國內監控工具），含工控網通 CVE 清單

### 模組 04：常規武器（Conventional weapons）— 7 份
- `04-weapons/00-weapons-intro-and-safeguards.md` — 章節導論：常規武器 vs CBRN、ASL-3 防線錯位、V 模型與 TRL
- `04-weapons/GTG-87001-yemen-gnc.md` — 葉門武器工程小組（治理框架），AI 取代工程人力、實彈試射失敗
- `04-weapons/GTG-17001-fire-control-spec.md` — 中國反魚雷火控規格書，用假美國廠商身分投標解放軍海軍
- `04-weapons/GTG-27005-autonomous-fpv-drone.md` — 俄羅斯自主 FPV 自殺無人機，可自行辨識人員目標並引爆（倫理爭議最大）
- `04-weapons/GTG-17002-ew-sead-taiwan.md` — **中國電子戰/防空壓制套件，模擬情境改為台灣 12 個目標（對台最敏感）**
- `04-weapons/GTG-27006-procurement-diversion.md` — 俄羅斯軍民兩用物項採購與出口管制規避
- `04-weapons/GTG-17003-directed-energy-intel.md` — 中國對美國定向能武器的科技情報蒐集，對具安全許可工程師建檔

### 模組 05：生物濫用（Biological misuse）— 5 份（治理與偵測框架，不含技術內容）
> 注意：報告的生物章節**不使用 GTG 編號**，改用「Case study 1–5」。其他六個危害領域使用 GTG 代號；生物章節的行為者國家、機構全部去識別。所以本模組檔名用 case1–5，不是遺漏。

- `05-bio/00-bio-intro-and-safeguards.md` — 章節導論：雙重用途困境、分類器四種狀態、可信任使用者審核制
- `05-bio/case1-classifier-caught.md` — 案例 1：分類器攔下 + 啟動調查（Soviet Biopreparat 類比）
- `05-bio/case2-weak-model-limit.md` — 案例 2：分類器降載到最弱模型；「把需求推向防護較弱模型」的外溢效應
- `05-bio/case3-classifier-gap.md` — 案例 3：分類器漏接（框架繞過的結構性盲區）
- `05-bio/case4-5-venoms-toxins-out-of-scope.md` — 案例 4-5：分類器設計上不涵蓋；五案總表收束

### 模組 06：詐騙（Scams and fraud）— 1 份
- `06-scams/GTG-15001-dating-app-network.md` — 中國交友 app 網絡，4,700+ AI 人設、與殺豬盤信任養成的關係

### 模組 07：非法蒸餾（Illicit distillation）— 7 份
- `07-distillation/00-distillation-intro-and-mitigations.md` — 章節導論：定義、思維鏈套取技術、Anthropic 分層反制、地緣政治爭議
- `07-distillation/GTG-16005-alibaba.md` — Alibaba（Qwen/Tongyi），史上最大蒸餾攻擊、1.51 億次
- `07-distillation/GTG-16002-moonshot.md` — Moonshot（Kimi），掛 Kimi 賣 Claude、跨階段重放攻擊
- `07-distillation/GTG-16001-deepseek.md` — DeepSeek，流量暴露俄中政府系統即時憑證
- `07-distillation/GTG-16006-zhipu.md` — Zhipu（GLM），蒸餾 + AI 研發 + 鎖定網路能力
- `07-distillation/GTG-16008-xiaomi.md` — Xiaomi，重放自家使用者工作階段
- `07-distillation/GTG-16012-16003-sensetime-minimax.md` — SenseTime、MiniMax 與轉售商/資料商生態

### 模組 08：能力評測研究（Frontier Red Team）— 2 份
- `08-capability-research/01-targeting-evals.md` — 情報鎖定三評測：身分關聯、照片地理定位（近超人級）、文字地理定位
- `08-capability-research/02-weapons-dev-evals-and-policy.md` — 無人機模擬評測結果解讀、開源治理、如何讀 AI 能力評測報告

### 模組 09：延伸研究（其他機構的同類研究）— 持續增補
> 本模組收錄 Anthropic 先前的威脅報告，以及 OpenAI、Google GTIG 等其他機構的同類 AI 濫用研究。每份研究一份教材、固定十二節，第 4 節一律與 2026-09 報告對照。每週由排程研究代理自動增補，人工事後審核。

- `09-external-research/00-external-research-intro.md` — 模組導論：收錄標準、閱讀路徑、自動維護的收錄清單
- 個別教材依 `<機構>-<年月>-<主題>` 命名（例如 `openai-2026-02-disrupting-malicious-uses.md`），完整清單見導論頁

### 模組 10：實作與評量 — 把閱讀轉成可覆核的成果

- [各模組作業與評分規準](10-practice/00-practice-guide.html)：涵蓋模組 01–09，講師可依角色與時間選題。
- [GTG-50014 工作階段異常](10-practice/01-50014-student.html)、[GTG-14020 風險模板](10-practice/03-14020-student.html)、[GTG-50020 工具內容與外傳](10-practice/05-50020-student.html)：三套學員作業各附講師版。
- [下載離線合成實作](downloads/course-labs.zip)：程式、日誌、正常反例與預期結果；不呼叫真實模型，不連線 IOC。

---

## 四、建議教學路徑

課程可依受眾選擇不同的進入路徑：

第一次來，建議先讀[安全防護專題](_shared/02-claude-safeguards-and-bypass-paths.html)、[證據與方法](_shared/04-evidence-and-methods.html)，再選一個案例。每頁的導讀區會指出快速理解、必讀與進階章節。閱讀前也請留意[查核狀態與公開勘誤](_shared/05-editorial-review-and-changelog.html)。

| 角色 | 先完成的閱讀與練習 | 本次交付 |
|---|---|---|
| SOC／偵測工程 | 安全防護專題 → GTG-50020 → 對應離線實作 | 一條證據鏈、控制驗收條件與 FP／FN 分析 |
| CTI／情報分析 | 證據與方法 → 任兩個案例 → 模組 09 來源比較 | 分開來源陳述、推論與未知的比較表 |
| 治理／採購 | 安全防護專題 → 能力評測 → [台灣公部門指引](09-external-research/moda-2026-01-public-sector-ai-playbook.html) | 附責任人、資料範圍與驗收方式的風險登錄表 |
| 講師 | 作業總覽 → 任一學員包 → 對應講師包 | 選定學習成果、時間安排與評分規準 |

- **完整課程（8 週）**：依模組順序 01 到 08，每模組先讀導論再讀個案。網路行動導論建立「攻擊複雜度不再等於攻擊者能力」的核心翻轉，是全課程的開場。
- **資安/SOC 向（聚焦偵測工程）**：01 網路行動全部 → 03 監控導論與失效模式 → 07 蒸餾（AI 供應鏈）→ 08 能力評測。重點在 IOC 的壽命、行為面偵測、agentic orchestration 的框架缺口。
- **政策/治理向**：08 能力評測（方法論）→ 04 常規武器導論（ASL 防線錯位）→ 05 生物（分類器四狀態、可信任審核制）→ 07 蒸餾（智財與地緣政治）。
- **台灣國安防禦向（最貼近讀者）**：03 監控的 GTG-14020（長老教會）與 GTG-14022（政治人物）→ 04 武器的 GTG-17002（台灣 12 目標）→ 02 影響力導論（認知作戰）→ 06 詐騙（金融防詐）。

---

## 五、貫穿全課程的核心主題

這六個主題橫跨多個模組，適合作為課程的縱向主線（詳見 `_shared/01-cross-cutting-analysis.md`）：

1. **攻擊複雜度與攻擊者能力脫鉤**：AI 抹平人力與工具落差，複雜度不再是歸因訊號。
2. **AI 作為勞動力，而非知識**：多個案例的關鍵不是「AI 提供了知識」，而是「AI 取代了稀缺的工程與分析人力」——這在武器與監控領域的擴散意義最深遠。
3. **防線失效的四種模式**：重新提示突破、跨工作階段拆分、工具請求看似中性、部署後不可收回。這是偵測工程與 AI 安全設計的核心教材。
4. **單一來源情報的紀律**：絕大多數案例只有 Anthropic 一方，如何負責任地教學與引用。
5. **圖表揭露多於正文**：情報視覺化如何隱藏與揭露訊息，以及「必須親自判讀」的方法論。
6. **對台灣的綜合意涵**：兩案直接點名台灣（長老教會、政治人物），一案模擬攻擊台灣（12 目標），加上金融詐騙、供應鏈、認知作戰的間接風險。

---

## 六、使用說明

- **圖檔**：每份教材引用的報告圖表已渲染為 PNG，存於 `figures/page-XXX.png`（三位數頁碼）。教材中以相對路徑 `../figures/page-XXX.png` 引用。
- **IOC 安全**：所有指標保留 defang 格式（如 `example[.]com`）。教學或演練時**絕不可**對這些指標連線、解析或查詢互動式服務。
- **單一來源情報**：每份教材的第 9 節明確標示哪些主張有第三方獨立查證、哪些僅來自 Anthropic。教學時請把後者當「高價值但未經外部驗證」的情報處理。
- **引用原則**：教材全文繁體中文，英文原文引文保留原樣並附頁碼，供講義直接引用。
- **跨案例分析**：`_shared/01-cross-cutting-analysis.md` 串起六大主題，可作為課程回顧與討論材料。
- **安全防護專題**：`_shared/02-claude-safeguards-and-bypass-paths.md` 從五個控制檢查點、案例證據與 F1–F7 分析，連到防護措施、離線實作與驗收規準。建議排課程第一天。
- **網頁閱讀**：點選上方教材名稱即可開啟，各頁提供「本頁目錄」快速跳至章節。流程圖需連線載入；列印時會省略導覽與目錄。

---

## 七、品質與限制聲明

- 本教材是**對兩份公開文件的教學性整理與分析**，不是原始情報。所有事實以 PDF 與研究網頁原文為準。
- 報告本身存在若干內部不一致（例如某案正文說四條工作線、表格列五列；某影響力案的證詞「是否實際送達」在案例層與摘要層說法不同；某案 GTG 編號在不同頁寫法不一）。這些都在對應教材的研究限制中標註，並多半轉化為課堂查核演練。
- 生物與常規武器模組**刻意只寫治理、偵測與政策層次**，不含任何可操作的技術內容。這是製作時的安全設計，不是資訊缺漏。
- 各案例的第三方查證受限於製作時的網路存取（部分來源因付費牆或封鎖無法取得原文），已在各教材第 12 節逐項標明。
