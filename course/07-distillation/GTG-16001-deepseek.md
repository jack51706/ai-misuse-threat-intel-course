# GTG-16001：DeepSeek 把 Claude 當成自家模型提供並蒐集對話用於訓練

> 課程模組：07 非法蒸餾（Illicit distillation）｜ 一手來源：《Detecting and countering misuse of AI: September 2026》PDF p.149–150（章節整體 p.143–154）｜ 整理日期：2026-09-13
>
> 本案原文標題：**"GTG-16001: DeepSeek serves Claude instead of its own models and collects exchanges for model training"**

---

## 1. 一頁速覽（給學員的 TL;DR）

1. **這是什麼案子**：Anthropic 指控中國 AI 業者 **DeepSeek（深度求索）** 把「以為自己在用 DeepSeek 模型」的使用者請求，**靜默轉送（silently relayed）給 Claude**，把 Claude 的回應當成自家模型的回應顯示給使用者，同時把這些對話存下來拿去訓練自家模型。這是一種「非法蒸餾（illicit distillation）」，但比一般蒸餾更惡劣——它同時**冒用了 Claude 當後端**又**出賣了自己使用者的隱私**。

2. **手法與 GTG-16002 Moonshot 幾乎同源**：DeepSeek 建了一條 **CoT 萃取管線（CoT extraction pipeline）**，用與 Moonshot 完全相同的**跨工作階段重放攻擊（cross-session replay attack）** 來繞過 Anthropic 對「思維軌跡（reasoning traces）」的技術保護，專門針對 **Claude Opus** 的推理軌跡下手。

3. **獨門的目標篩選手法**：DeepSeek 會**檢查進站請求中的字串（checked various strings included in inbound requests）**，把使用 **Claude Code、Claude Agent SDK、OpenCode** 這類第三方／Anthropic 編碼工具框架（coding harnesses）的使用者「打標籤（tagging）」，再把被選中的高價值使用者請求**轉送到 Claude Opus**。這是一種精準的「價值分流」，只挑最能蒸餾出高階能力的流量下手。

4. **規模數字（逐字確認）**：**"Scale of distillation attacks attributable to DeepSeek over 14 days in July 2026: over 12.1 million exchanges observed."**——2026 年 7 月的 **14 天內**，觀察到超過 **1,210 萬次（12.1 million）** 可歸因於 DeepSeek 的互動。

5. **全蒸餾章節最戲劇性的發現——流量暴露了政府系統的即時憑證**：被轉送的流量中，有一名替**俄羅斯國防部相關政府機關**工作的 IT 人員，其請求**暴露了「一個俄羅斯政府資料庫的即時憑證（live credentials for a Russian government database）」**；另有工程師在替**中國某市級公安局（municipal Public Security Bureau）** 建置**案件管理系統（case management system）**，該系統是「用國民身分證號比對民眾移動軌跡與警方記錄」的監控工具。**注意**：報告只在俄羅斯這一案明講「憑證」，公安局案講的是監控工具的功能，並未說暴露了憑證——本教材第 3 節會精準拆解這個差別。

6. **三重外洩的諷刺**：（a）蒸餾流量本身就洩漏了「DeepSeek 的使用者正在做什麼」；（b）這些使用者本身多半在從事**監控／情報／國防**工作；（c）於是 Anthropic 因為別人來偷它的模型，反而**意外看見了俄、中政府系統的即時活動**。偷竊者把被害者（俄中政府使用者）的機敏資料，親手送進了美國公司的伺服器。

7. **歸因信度**：章節層級 Anthropic 用 **"attributed with high confidence"（高信度歸因）** 這個正式的情報估計用語（p.147）；DeepSeek 個案內文則用 **"Our investigation revealed…"（我們的調查揭露）** 這種直述句，對「使用者是否知情」則保守地用 **"likely not made aware"（很可能不知情）**。措辭層次值得課堂細讀。

8. **獨立佐證存在，但要分清楚**：本案的細節（俄中憑證、12.1M 次數）目前是**單一來源（Anthropic）**；但「DeepSeek 對美國前沿模型進行工業級蒸餾」這個更大的指控，有 **2026-09-08 FBI/NSA/CISA 聯合公告（AA26-251A）** 這個**獨立政府來源**點名 DeepSeek 佐證，也與 **2025 年初 OpenAI 指控 DeepSeek 蒸餾 GPT** 的舊案一脈相承。

> **這個案例在課程裡要教什麼**：教學員辨識「AI 供應鏈信任崩壞」的新型態威脅——當你以為在用 A 模型、其實流量被轉送給 B 模型並被第三方蒐集時，你的機敏資料（憑證、國防資料、監控目標）會在你毫不知情下跨境外流；並教「蒸餾流量如何反過來成為情報側通道（side-channel）」這個防禦與情報分析的雙面刃思維。

---

## 2. 行為者側寫與歸因

### 2.1 行為者身分：DeepSeek（深度求索）是誰

DeepSeek（中文：杭州深度求索人工智能基礎技術研究有限公司）並非典型的「駭客組織」或「詐騙集團」，而是一家**有正式品牌、有旗艦模型、在全球有數億使用者**的中國 AI 前沿實驗室。這一點讓本案在整份威脅報告中格外特殊：**行為者不是躲在暗處的個人，而是一家知名科技公司**。

| 項目 | 內容 | 來源 |
|---|---|---|
| 成立時間 | 2023 年 7 月，從量化避險基金 **High-Flyer（幻方量化）** 於 2023 年 4 月設立的內部 AGI Lab 分拆而來 | Built In／Wikipedia 類彙整（第 9 節） |
| 創辦人 | **梁文鋒（Liang Wenfeng）**，同時是幻方量化（管理資產逾 80 億美元）的所有人 | 同上 |
| 旗艦模型 | **DeepSeek-V3**（671B 參數 MoE 架構，宣稱訓練成本約 550 萬美元）、**DeepSeek-R1**（開源推理模型，宣稱效能對標 OpenAI o1、使用成本約便宜 96%） | CNBC／IBM（第 9 節） |
| 全球知名度事件 | 2025 年 1 月 R1 發表，以「極低成本對標 GPT-o1」震撼全球市場，一度導致美股 AI 類股大跌 | 多家（第 9 節） |

**教學重點**：把 DeepSeek 理解為「行為者」時，要記得它有雙重身分——它既是**濫用 Claude 的加害者**（本報告），也是**2025 年初被 OpenAI 指控蒸餾的加害者**，同時還是**被多國政府以資安理由封禁的對象**。這種「同一主體、多重角色」正是情報分析裡「行為者側寫」要能同時容納的複雜性。

### 2.2 歸因（Attribution）：Anthropic 憑什麼指向 DeepSeek

本案的歸因要拆成兩層來讀：

**第一層——章節層級的正式信度用語（p.147）**：

> *"Since February 2026, we have detected and disrupted unauthorized distillation campaigns we have attributed **with high confidence** to specific PRC-based labs targeting Anthropic's Opus-class models."*
>
> 譯：自 2026 年 2 月起，我們已偵測並瓦解多起未經授權的蒸餾行動，並**以高信度**歸因於特定的中國（PRC）實驗室，其目標鎖定 Anthropic 的 Opus 級模型。

**"high confidence"（高信度）** 在情報學（可對照美國情報體系的 ICD 203 估計性用語標準）是最高一級的信度表述，意指「判斷有優質、可靠、多來源的證據支撐，即使仍非百分之百確定」。Anthropic 沒有用 "suspected"（疑似）或 "consistent with"（與……相符）這類較弱的措辭，代表它自認手上有**可直接歸因到組織**的證據。

**第二層——DeepSeek 個案內文的措辭（p.149–150）**：

- 對「做了什麼」——用直述句：**"Our investigation revealed that DeepSeek…"**（我們的調查揭露 DeepSeek……）。這是對**自家可觀測遙測資料（telemetry）** 的陳述，Anthropic 能直接看到自己伺服器上發生了什麼，所以講得很篤定。
- 對「使用者是否知情」——用保守推斷：**"their customers were likely not made aware"**（其客戶**很可能**未被告知）、**"This sensitive data was likely routed to Anthropic without the knowledge or consent of DeepSeek's customers."**（這些機敏資料**很可能**在 DeepSeek 客戶不知情、未同意下被送往 Anthropic）。這裡用 "likely" 是因為 Anthropic **無法看到 DeepSeek 內部有沒有通知它的使用者**——這是對「第三方內部作為」的合理推斷，不是直接觀測，所以誠實地降一級信度。

> **情報學教學點（怎麼想，而不只是發生什麼）**：同一份報告裡，Anthropic 對「我能直接觀測到的事」與「我只能推斷的事」用了**不同強度的動詞**。學員要學會讀出這個層次——這正是負責任的情報產出（intelligence product）該有的紀律：**信度要跟證據的可觀測性對齊**。

### 2.3 為什麼「靜默轉送自家使用者」本身就是強歸因訊號

這是本案在偵測工程上最精妙的地方，值得單獨講：

一般的蒸餾（如 SenseTime 向第三方資料商**購買**對話、如 Alibaba 用假帳號**直接查詢** Claude）中，Anthropic 看到的是「一批可疑帳號在查詢 Claude」。要把這些帳號歸因到某家公司，需要靠代理網路特徵、付款方式、行為模式等旁證。

但 DeepSeek（與 Moonshot）的手法不同：**它把「使用者以為在跟 DeepSeek 對話」的請求，轉手送進 Claude**。這意味著：

- **只有 DeepSeek 自己**能攔截並轉送「打進 DeepSeek 產品」的入站流量。一個隨機的代理商（proxy reseller）沒有能力去攔截打向 DeepSeek App／API 的使用者請求。因此，當 Anthropic 在轉送來的流量裡看到「這些明顯是 DeepSeek 產品的使用者」時，**能執行這種轉送的主體，邏輯上就指向 DeepSeek 本身**。
- 轉送流量裡夾帶的**內容**（例如 DeepSeek 使用者拿去分析的內部文件、公安系統程式碼），本身就是「這是 DeepSeek 的使用者」的內生證據。

**這是一種罕見的「加害者自證」結構**：加害者為了偷模型，反而把「我確實在攔截並轉送我自己使用者」這件事，透過流量本身洩漏給了被偷的對象。教學上這是一個絕佳範例，說明**攻擊手法的選擇會決定歸因的難易度**。

### 2.4 基礎設施交叉：DeepSeek 與 Alibaba 共用代理池

一個容易被忽略但很重要的歸因線索出現在 Alibaba 案（p.148）：

> *"Alibaba accessed Claude through two main pools of fraudulent accounts... Some of these accounts were found to have been **funneling requests from DeepSeek and Xiaomi**, demonstrating that the same proxy service networks are often used by a variety of organizations."*
>
> 譯：Alibaba 透過兩大詐欺帳號池存取 Claude……其中有些帳號被發現**同時在為 DeepSeek 與 Xiaomi 轉送請求**，顯示同一批代理服務網路常被多個組織共用。

**意涵**：DeepSeek 的部分流量與 Alibaba 的第二個帳號池**共用同一套代理網路（proxy service network / "transfer station"）**。這對歸因是雙面刃：

- **有利**：共用基礎設施讓 Anthropic 能把跨組織的活動串在一起分析。
- **困難**：共用基礎設施也讓「某筆流量到底屬於哪一家」變得更難切分——同一個假帳號可能今天替 Alibaba 跑、明天替 DeepSeek 跑。這是 Anthropic 選擇「**歸因到組織、而非逐一封鎖帳號**」策略（見第 8 節）的現實原因。

### 2.5 模組脈絡：七家中國實驗室蒸餾案速查表（把 DeepSeek 放進全局）

DeepSeek 只是本模組（第 07 章「非法蒸餾」）點名的**七家中國實驗室**之一。要正確理解 DeepSeek 案的定位，必須把它放進整章的比較脈絡。下表數字**均逐字錄自 PDF 各案的斜體 "Scale of distillation attacks…" 小結行與內文**（p.143–154），供課堂建立「規模 vs 手法 vs 敏感度」的整體圖像。

| GTG 代號 | 實驗室 | 規模（觀察到的互動） | 時窗 | 假帳號數 | 手法特徵 | 是否「冒名轉送自家使用者」 |
|---|---|---|---|---|---|---|
| **16005** | **Alibaba**（Qwen） | **逾 1.51 億次** | 2026-05～07 | 兩池，第一池近 5,000 | 注入固定提示強迫吐 CoT；規模最大（峰值近 300 萬/日）；另用於 RL 環境與架構 R&D | 否（假帳號直接查詢） |
| **16002** | **Moonshot**（Kimi） | **逾 2,300 萬次** | 2026-05～07 | 5,380（多在新加坡 / 日本） | **首見的 thinking-signature 跨 session 重放**；10 天轉送近 30 萬筆給 Opus | **是**（冒名 Kimi 提供 Claude） |
| **16001** | **DeepSeek** ← 本案 | **逾 1,210 萬次** | 2026-07（14 天） | **原文未給** | **沿用** Moonshot 重放攻擊；**harness 字串標籤**精準分流 Opus；**流量含俄羅斯政府資料庫即時憑證** | **是**（冒名自家模型提供 Claude） |
| **16006** | **Zhipu / Z.ai**（GLM） | 逾 340 萬次 | 2026-06～07（17 天） | 273（CoT 清洗用） | 把擷取的 CoT **回放給 Claude 清洗**；**唯一先鎖定 Fable、被安全機制擋下後改打 Opus 4.6** | 否（清洗管線 + 蒸餾） |
| **16008** | **Xiaomi**（MiMo） | 逾 40 萬次 | 2026-03～04（20 天） | 原文未給 | 把自家 MiMo 對話 / 編碼 session 經 **OpenClaw / OpenCode** 回放給 Claude；存下對話但未拿去服務使用者 | 否（回放自家 session） |
| **16012** | **SenseTime** | 未給明確總量 | — | — | **向第三方資料商購買** Claude 對話逐字稿；用 Claude 寫蒸餾管線、啟動 / 監控訓練 | 否（購買轉售資料） |
| **16003** | **MiniMax** | 未給明確總量 | — | — | 透過**空殼公司**建代理網路，只提供 Anthropic + OpenAI 模型、不含自家模型 | 否（空殼代理收割） |

**從表中可讀出的教學洞察**：

1. **DeepSeek 在「規模」上排第三**（1,210 萬），低於 Alibaba（1.51 億）與 Moonshot（2,300 萬）——**但它在「內容敏感度」上排第一**（唯一出現政府 / 國防資料庫即時憑證）。這再次印證「規模與敏感度是兩個獨立維度」。
2. **只有 DeepSeek 與 Moonshot 採「冒名轉送自家使用者」**（GTG-16001、16002）——這是整章**最惡劣的一類手法**，因為多了「出賣使用者隱私 + 知情同意崩壞」。DeepSeek 案是這類手法中**內容後果最嚴重**的一例。
3. **手法呈光譜分布**：從「買資料」（SenseTime）→「空殼代理收割」（MiniMax）→「假帳號直接查詢」（Alibaba）→「回放自家 session」（Xiaomi/Zhipu）→「冒名轉送真實使用者」（Moonshot/DeepSeek）。惡意程度與知情同意的破壞程度大致遞增。
4. **Zhipu 案的對照價值**：它是**唯一先嘗試打 Fable、被 Anthropic 強化過的安全機制擋下、才改打防護較弱的 Opus 4.6** 的案例——證明**安全防護的強弱會直接改變攻擊者的目標選擇**，是「防禦有效性」最直接的證據。

---

## 3. 受害者與目標清單

本案的「受害者」有兩層，這是理解本案戲劇性的關鍵：

- **第一層受害者**：**Anthropic 與 Claude**——模型能力被非法萃取、技術控制被繞過。
- **第二層受害者（更敏感）**：**DeepSeek 自己的使用者**——他們以為在用 DeepSeek，機敏資料卻在不知情下被送往美國公司 Anthropic，並被 DeepSeek 存下來訓練。

報告在 p.150 具體列出三個「第二層受害者」案例（**"These cases include:"**）：

| # | 受害者類型 | 使用者做的事 | 被暴露 / 外流的內容 | 報告用語 |
|---|---|---|---|---|
| 1 | **中國某科技公司**（A PRC technology company） | 員工用「他以為是 DeepSeek」的服務分析**內部文件** | 某**旗艦 AI 專案**的**完整規格、組織架構、戰略目標**（full specifications, organizational structure, and strategic objectives of a flagship AI program） | "almost certainly not made aware"（幾乎確定不知情） |
| 2 | **俄羅斯國防機關**（Russian defense agency） | 一名 IT 操作人員處理**與俄羅斯國防部相關之政府機關**的資料 | **一個俄羅斯政府資料庫的即時憑證**（live credentials for a Russian government database） | 直述："exposed live credentials" |
| 3 | **中國警方監控**（PRC police surveillance） | 工程師替**某市級公安局**建置**案件管理系統** | 一個「**用國民身分證號比對民眾移動軌跡與警方記錄**」的監控工具（其設計與功能被送往 Claude） | 直述：描述工具功能，**未提「憑證」** |

### 3.1 ⚠️ 精準拆解：報告到底說了什麼、沒說什麼（品質紅線）

課程研究必須嚴守「不誇大原文」。本案有一個極易被二手報導與簡報講義**過度概括**的點，務必釐清：

- **只有「俄羅斯」這一案，報告明確使用「即時憑證（live credentials）」一詞**：
  > *"**Russian defense agency.** DeepSeek relayed requests from an IT operator working with data from a Russian government agency associated with its Ministry of Defense. The relayed requests **exposed live credentials for a Russian government database**."*

- **「中國公安局」這一案，報告描述的是監控工具的功能，並未說暴露了憑證**：
  > *"**PRC police surveillance.** Engineers building a case management system for a municipal Public Security Bureau in China used DeepSeek, which relayed those requests to Claude. The engineer built a tool that compares a person's movements against police records using the national ID number of citizens."*

換言之，若有人說「本案暴露了**俄羅斯與中國警方兩套系統的憑證**」，這在**中國公安局那一半是不精確的**——報告沒這樣寫。中國公安局案的敏感性不在「憑證」，而在**它揭露了一套正在被建置的、以全體公民身分證號為基礎的大規模移動軌跡比對監控系統**，這在人權與監控治理上的意義，其實不亞於一組憑證。

> **教學點**：情報教材的價值在於「精確」。「暴露憑證」與「暴露一套監控系統的設計」是**兩種不同性質的洩漏**，各有其威脅意涵。把兩者混為一談（都說成「憑證外洩」）會誤導風險評估。這也是本教材相對於先前「太短、混談」摘要版本的具體改進。

### 3.2 三案的共同威脅意涵

1. **蒸餾流量 = 受害者活動的側通道情報**：Anthropic 原本只是「被偷模型的一方」，卻因為偷竊手法是「轉送真實使用者流量」，而**被動獲得了對俄、中政府 / 國防 / 公安系統即時活動的可見度**。這是一個典型的「非預期情報收穫（unintended intelligence windfall）」。
2. **這些使用者本身多在從事監控 / 情報 / 國防工作**：俄羅斯國防部 IT、公安局案件管理、某旗艦 AI 專案戰略——被外洩的不是一般民眾的家常對話，而是**國家級敏感作業**。當事人在做的事越敏感，「用了會轉送流量的 AI」造成的反噬就越嚴重。
3. **對 DeepSeek 使用者的信任崩壞**：三案的共同句型都是「使用者**以為**在用 DeepSeek（used what they believed was DeepSeek / had no way of knowing）」。這是本案的核心倫理與資安問題——**知情同意（informed consent）的徹底缺失**。

---

## 4. AI 濫用的攻擊生命週期（逐階段拆解）

本案沒有像前面 ShinyHunters 那種完整的攻擊生命週期流程圖（p.149–150 為純文字），但可依報告敘述重建一條**「非法蒸餾 + 使用者流量劫持」的生命週期**。每階段標示自主程度。

### 階段 0：建立詐欺存取基礎設施（Establish fraudulent access）
- **人類做什麼**：DeepSeek（或其委外的代理服務商）建立 / 租用「代理服務網路（proxy services，報告稱 "transfer stations" 轉運站）」，用假身分、假 / 盜刷信用卡、盜用的 API 金鑰大量開設帳號，繞過 Anthropic 的地理限制與存取控制（p.144 章節通則）。
- **與 DeepSeek 交叉**：部分帳號與 Alibaba 第二帳號池共用（p.148）。
- **自主程度**：人類 / 工程建置為主。

### 階段 1：攔截並「打標籤」自家入站流量（Intercept & tag inbound traffic）— DeepSeek 獨門
- **人類 / 系統做什麼**：DeepSeek 在自己的服務入口，**檢查進站請求中的字串**，辨識哪些使用者是透過 **Claude Code、Claude Agent SDK、OpenCode** 等編碼工具框架在呼叫「DeepSeek 模型」，並**對這些使用者打標籤**。
- **為什麼挑這些**：使用這些 harness 的多半是**開發者 / 進階使用者**，其請求（含多輪工具呼叫、複雜推理）正是蒸餾**高階 agentic / coding / reasoning 能力**最有價值的原料。這是**精準的價值分流**，不是無差別全抓。
- **自主程度**：自動化系統依規則篩選。

### 階段 2：靜默轉送到 Claude Opus（Silent relay）
- **系統做什麼**：被選中的標籤使用者，其請求被**轉送到 Claude Opus**（報告明確點名 Opus，因為 Opus 是推理能力最強、最值得蒸餾的等級）。使用者端**看到的是 Claude 的回應，卻以為是 DeepSeek 的回應**。
- **Claude 做什麼**：正常回應請求——**Claude 在此階段是「被冒名利用的後端」，並非攻擊工具**。這與其他案例（Claude 被當攻擊工具）性質不同。
- **自主程度**：全自動轉送。

### 階段 3：跨工作階段重放，萃取完整推理軌跡（Cross-session replay → CoT extraction）
- **系統做什麼**：這是技術核心。Claude 為防蒸餾，**不直接回傳原始思維**，而是回傳一個「**思維簽章（thinking signature / reasoning signature）**」作為指標（見第 4.1 節機制詳解）。DeepSeek 的 CoT 萃取管線把這個簽章**存下來，另開一個新工作階段（new session），誘導 Claude 把簽章「還原」成完整的推理軌跡**。
- **關鍵後果**：藉此 DeepSeek **拿到了本應被「摘要化（summarized）」隱藏的完整 CoT**——報告原文：*"DeepSeek used this technique to exfiltrate reasoning traces that would have otherwise been summarized."*
- **自主程度**：自動化管線（pipeline）+ 精心設計的提示（人類研究者設計技術）。

### 階段 4：蒐集、儲存、訓練（Collect, store, train）
- **系統做什麼**：把轉送來的對話與萃取出的 CoT 存檔，餵入 DeepSeek 自家模型的訓練 / 後訓練管線。
- **附帶損害**：使用者夾帶在請求裡的機敏資料（俄羅斯政府資料庫憑證、公安監控工具、企業旗艦專案規格）**一併被存進 DeepSeek，並經 Claude 過了一手**。
- **自主程度**：批次自動化。

### 階段 5：規模化（Scale）
- **14 天內超過 1,210 萬次互動**。這不是實驗，是**工業化量產**。

> **自主程度總評**：本案不是「AI 自主編排的多代理攻擊」，而是**「人類設計 + 系統自動化執行」的資料收割流水線**。Claude 在其中扮演**被冒名的後端與被萃取的教師模型（teacher model）**，而非攻擊的執行者。這與模組其他「Claude 被當武器」的案例是根本不同的濫用型態，教學時要明確區分。

### 4.1 機制詳解：思維簽章與跨工作階段重放攻擊（本案技術核心）

這是整個模組最值得花時間講清楚的技術機制。它源自 Moonshot 案（p.148–149），DeepSeek **原樣沿用**。

**Anthropic 的防禦設計（thinking signature）**，原文（p.148）：

> *"When responding, Claude returns a reference to its raw thinking as a "thinking signature" instead of the raw thinking to mitigate the risk of unauthorized distillation. This is used by our API to look up the raw thinking trace in subsequent calls to the API."*
>
> 譯：Claude 回應時，會回傳一個指向其原始思維的參照——「思維簽章」——而**不是原始思維本身**，以降低未經授權蒸餾的風險。這個簽章供我們的 API 在後續呼叫時用來查回原始思維軌跡。

**設計原理（怎麼想）**：推理模型最有價值的資產是它的「思考過程（chain-of-thought, CoT）」。如果 API 直接把完整 CoT 明文回給呼叫方，等於把最珍貴的訓練原料免費送出。所以 Anthropic 的設計是——**CoT 留在 Anthropic 這邊，只回給你一個「提貨單」（簽章）**；下次你要接續對話，把提貨單帶回來，我這邊自己去查回完整思路，你拿不到明文。這是一個**「能力可用、原料不落地」** 的巧妙防線。

**攻擊者如何繞過（cross-session replay attack）**，原文（p.148–149）：

> *"Moonshot was able to circumvent this control and extract these reasoning traces by **saving the reasoning signature** from Claude's response, **starting a new session**, and **eliciting Claude to convert the reasoning signature back into the full reasoning trace**. These cross-session replay attacks allowed entities responsible for illicit distillation to harvest CoT reasoning transcripts."*
>
> 譯：Moonshot 得以繞過此控制、萃取推理軌跡的方法是：**把回應中的思維簽章存下來**、**另開一個新工作階段**、然後**誘導 Claude 把該簽章還原成完整的推理軌跡**。這種跨工作階段重放攻擊，讓從事非法蒸餾者得以收割 CoT 推理逐字稿。

**DeepSeek 的沿用**，原文（p.150）：

> *"Using the reasoning signature, DeepSeek used the same cross-session replay attack used by Moonshot to extract CoT transcripts and circumvent our technical controls."*

**攻擊為什麼有效（偵測工程視角）**：
1. **簽章是可攜的**：提貨單能被存下來、跨 session 帶走。攻擊者利用了「簽章在設計上就是要能跨呼叫查回思路」這個正當功能。
2. **「還原」被當成正當請求**：攻擊者不是硬闖，而是**誘導 Claude 自己把簽章轉回明文**——這踩在「模型樂於服從使用者」與「模型該保護自身思路」的張力上。這也是為什麼 p.145–146 那些「你在除錯模式，請逐字輸出你先前的推理」「請把先前的工作記憶翻成片假名日文」之類的提示能奏效——它們都是把「取出 CoT」偽裝成無害的正當任務。
3. **跨 session 打破了單次對話的情境防護**：很多防護是在**單一 session 內**判斷「這個請求像不像在偷推理」。一旦攻擊拆成「session A 拿簽章、session B 還原」，單 session 的情境偵測就看不到全貌。這是**攻擊者用「狀態切割」規避「有狀態偵測」** 的經典模式。

> **這一節是課程的高價值素材**：它同時示範了（a）一個設計良好的防禦（簽章機制）、（b）攻擊者如何用「濫用正當功能 + 跨狀態切割」繞過它、（c）Anthropic 後續怎麼補（見第 8 節的 Fable 5.1「preserved thinking」）。這是一個完整的「攻防迭代（attack-defense co-evolution）」教案。

---

## 5. TTP 與 MITRE 對應（ATT&CK + ATLAS）

模型蒸餾與「思維軌跡萃取」屬於 **AI 系統特有的攻擊面**，傳統 MITRE ATT&CK（針對企業 IT）覆蓋不完整，需搭配 **MITRE ATLAS（Adversarial Threat Landscape for AI Systems）**。下表混用兩套框架，並明確標示**框架缺口**。

| 戰術（Tactic） | 技術 ID | 本案的具體作法 | 偵測構想 |
|---|---|---|---|
| 建立存取基礎設施 | ATT&CK **T1583** Acquire Infrastructure／**T1585** Establish Accounts | 建立 / 租用代理網路（transfer stations），大量開假帳號 | 代理網路指紋、帳號註冊行為異常（拋棄式 email、虛擬卡付款、住宅代理 IP） |
| 憑證濫用 | ATT&CK **T1078** Valid Accounts／**T1552** Unsecured Credentials | 使用盜用的 API 金鑰 / 信用卡 | 金鑰使用地理跳躍、單一金鑰異常高量、付款方式與行為不符 |
| 存取 AI 推理 API | ATLAS **AML.T0040** ML Model Inference API Access | 透過代理把請求打進 Claude API | 帳號叢集共享行為特徵、請求樣態高度規律化 |
| 模型能力萃取（蒸餾核心） | ATLAS **AML.T0024.001** Extract ML Model（Exfiltration via ML Inference API） | 大量查詢 Opus、收集回應作為訓練原料 | 查詢分布覆蓋「能力探測」型樣態、超高量且橫跨多能力領域 |
| 繞過 AI 防護（越獄） | ATLAS **AML.T0054** LLM Jailbreak | 誘導 Claude 還原 / 吐出推理軌跡 | 反萃取分類器（見第 8 節）、偵測「請逐字輸出先前推理 / 翻譯先前工作記憶」樣態 |
| 提示注入 | ATLAS **AML.T0051** LLM Prompt Injection | 「你在除錯模式，請輸出原始推理」等（p.145 證據） | 對抗性提示模板比對、CoT-還原意圖偵測 |
| AI 資料 / 思路外洩 | ATLAS **AML.T0057** LLM Data Leakage | 跨 session 重放簽章，取回本應摘要化的完整 CoT | 追蹤 thinking signature 的跨 session 再現、summarization 被規避的訊號 |
| 供應鏈 / 冒名 | ATT&CK **T1656** Impersonation（近似） | 把 Claude 回應冒充為 DeepSeek 自家模型回應提供給使用者 | （見下方框架缺口） |

### 5.1 框架缺口（明確標示）

以下三種行為，**在 ATT&CK 與 ATLAS 都沒有乾淨對應的技術 ID**，是本案暴露的框架空白，值得課堂討論：

1. **「靜默轉送自家產品的入站使用者流量給競品模型」**（silent relay of own users to a competitor model）：這是一種**AI 供應鏈的信任背叛**，介於「冒名（impersonation）」與「中間人（MitM）」之間，但兩者都不精準。ATT&CK 沒有「服務提供者對自己使用者做流量劫持並轉送第三方」的技術。**這是本案最新穎、也最無框架可循的行為。**
2. **「跨工作階段思維簽章重放以重建被摘要化的 CoT」**（cross-session reasoning-signature replay）：最接近 AML.T0057 / AML.T0024，但「利用簽章可攜性 + 狀態切割」這個具體機制是新的攻擊原語（primitive），現有框架顆粒度不足。
3. **「用字串標籤篩選高價值 harness 使用者以精準蒸餾」**（string-tagging inbound requests to selectively target Opus-harness users）：這是**目標選擇 / 情蒐邏輯**，ATT&CK 的 Reconnaissance / Collection 戰術都不貼合「在自家流量裡篩選最值錢的受害者來轉送」這種行為。

> **教學點**：框架缺口不是框架的失敗，而是**威脅演化快過框架**的正常現象。教學員遇到「框架對不上」時，正確反應是「明確標註為缺口並描述行為本質」，而不是硬塞一個不貼切的 ID。這對日後撰寫威脅報告是重要職業素養。

---

## 6. 圖表逐一判讀（p.149–150）

**重要說明**：本案頁段 **p.149 與 p.150 皆為純文字頁**，經以 Read 工具逐頁判讀對應的渲染圖片（`page-149.png`、`page-150.png`）確認——**兩頁均無流程圖、長條圖、架構圖或介面截圖**，因此 `figures.txt` 未登錄任何 Figure，`course/figures/` 也沒有 `page-149.png`／`page-150.png`（該資料夾只存含圖表的頁面）。這與模組前段（如 p.143 的「非法蒸餾生命週期」圖示、Alibaba 章節）不同。以下如實判讀兩頁的**版面與資訊結構**，因為「版面本身如何組織資訊」對教材理解與引用同樣重要。

### 6.1 page-149.png（p.149）：Moonshot 案收尾 + GTG-16001 開篇

- **圖片類型**：純文字排版頁（襯線字體正文 + 大標題 + 項目符號清單 + 斜體小結）。
- **版面實際看到的元素（由上而下）**：
  1. 承接 p.148 的段落，講「跨工作階段重放攻擊讓非法蒸餾者得以收割 CoT」，並預告「We're introducing new methods to strengthen our defenses（我們正引入新方法強化防禦）」。
  2. 一段講 Moonshot 轉送的流量夾帶敏感資訊，並老實承認「**We do not know if Moonshot notified their customers**（我們不知道 Moonshot 是否通知了它的客戶）」——這種「明講自己不知道什麼」的措辭是報告可信度的重要來源。
  3. **項目符號清單（"These include:"）** 列出 Moonshot 兩個受害案例（PLA 相關的成都 CCTV 監控案、某中國大型國企工程師洩漏多家公司內部程式碼與**即時憑證**）。
  4. 斜體小結行：**"Scale of distillation attacks attributable to Moonshot between May and July 2026: over 23 million exchanges observed."**
  5. **大號襯線標題**：**"GTG-16001: DeepSeek serves Claude instead of its own models and collects exchanges for model training"**——本案正式開篇。
  6. DeepSeek 開篇段落：宣告 DeepSeek「也部署了與 Moonshot 類似的手法……建了 CoT 萃取管線……靜默轉送……客戶很可能不知情」。
  7. 頁尾：報告頁眉「Detecting and countering misuse of AI: September 2026」與頁碼 149。
- **這頁傳達的核心訊息**：報告**刻意把 DeepSeek 案緊接在 Moonshot 案之後**，並反覆用 "similar to Moonshot's"、"the same cross-session replay attack" 把兩案綁定。版面上「Moonshot 收尾 → DeepSeek 開篇」的**視覺並置**，本身就是報告的論證策略：**先詳述 Moonshot 的技術機制，再說 DeepSeek「照抄」，達到「機制講一次、套用兩次」的敘事效率**。
- **課堂用法**：用這頁教學員觀察「威脅報告如何用版面順序建立案件之間的關聯」。可讓學員比較「若把 DeepSeek 案獨立抽出、不接在 Moonshot 後面讀，資訊會缺什麼？」——答案是 DeepSeek 案的**技術機制細節其實寫在 Moonshot 段**，這正是為何本教材第 4.1 節必須回頭引用 p.148。

### 6.2 page-150.png（p.150）：DeepSeek 案主體 + 三受害案例 + GTG-16006 開篇

- **圖片類型**：純文字排版頁（正文段落 + 項目符號清單 + 斜體小結 + 下一案大標題）。
- **版面實際看到的元素（由上而下）**：
  1. 第一段：DeepSeek **針對 Opus 的推理軌跡**、用簽章 + 跨 session 重放萃取 CoT、繞過技術控制、取得**本應被摘要化**的推理軌跡。
  2. 第二段：**harness 字串標籤**手法——檢查進站字串、標記使用 Claude Code / Claude Agent SDK / OpenCode 的使用者、把選中者轉送 Claude Opus。
  3. **項目符號清單（"These cases include:"）** 三個粗體起頭的受害案例：**A PRC technology company.**／**Russian defense agency.**／**PRC police surveillance.**（即第 3 節表格三案）。
  4. 斜體小結行（本案關鍵數字）：**"Scale of distillation attacks attributable to DeepSeek over 14 days in July 2026: over 12.1 million exchanges observed."**
  5. **大號襯線標題**：**"GTG-16006: Distillation, AI R&D, and targeting cyber capabilities"**（轉入 Zhipu / Z.ai 案）。
  6. Zhipu 開篇段落起頭，頁尾頁碼 150。
- **資料如何組織**：這頁的資訊密度極高，用**「技術手法 → 具體受害案例 → 規模數字」** 的三段式結構，把一個完整案件濃縮在半頁內。三個粗體案例標籤（PRC tech / Russian defense / PRC police）在視覺上形成**由「商業機密」升級到「國防」再到「國家監控」的敏感度階梯**。
- **這頁傳達的核心訊息**：**DeepSeek 案的殺傷力不在數字（12.1M 其實低於 Moonshot 的 23M、遠低於 Alibaba 的 151M），而在被轉送流量的「內容敏感度」**——俄羅斯國防資料庫即時憑證、中國公安全民監控工具。版面把「相對不驚人的規模數字」與「極驚人的內容案例」並列，形成強烈反差。
- **課堂用法**：這是本模組**最適合拿來討論「規模 vs 敏感度」如何各自構成威脅**的一頁。可設計練習：「若你是 CISO，Alibaba 的 1.51 億次無害查詢，與 DeepSeek 的一筆俄羅斯國防憑證外洩，哪個更該上報董事會？為什麼？」引導學員理解**威脅嚴重性不能只看量級**。

> **判讀總結**：雖然本頁段沒有可供標註的圖表，但**兩頁的文字版面結構本身就是教材**——它示範了 Anthropic 如何用「機制敘述 → 受害案例清單 → 斜體規模小結」的標準化模板，把七家實驗室的蒸餾案並置比較。學員若要自己寫威脅報告，這個模板值得臨摹。

---

## 7. IOC 與技術指標

### 7.1 本案沒有傳統 IOC 表

與模組其他案例（如 ShinyHunters 有 IP、網域、Telegram 帳號的 IOC 表）不同，**GTG-16001 在頁段內未提供任何網域、IP、雜湊值或帳號等傳統入侵指標（IOC）**。原因是本案的行為者是一家**公司**，而非用一組固定基礎設施的攻擊者；其「基礎設施」是**大量拋棄式假帳號 + 共用代理網路**，本質上是**流動、可替換、刻意去識別化**的，抓單一 IOC 意義不大。

> **偵測工程教學點**：這正是 Anthropic 為何走「**歸因到組織、而非封鎖單一 IOC**」路線的原因（見第 8 節）。當對手的基礎設施是「工業化量產的假帳號池」時，**行為指標（behavioral indicators）與帳號叢集分析** 比「IP / 網域黑名單」有效得多。這是課程要傳達的偵測典範轉移：**從 IOC-centric 到 behavior/attribution-centric**。

### 7.2 本案可用的「行為指標」（替代 IOC）

雖無傳統 IOC，仍可整理出本案的**行為 / 遙測指標**，並評估其偵測價值與壽命：

| 指標類型 | 具體樣態 | 偵測價值 | 壽命 |
|---|---|---|---|
| 帳號基礎設施 | 住宅代理、拋棄式 email、虛擬卡付款、盜用 API 金鑰、大量新帳號（p.144 通則） | 中：可辨識代理網路，但假帳號可快速再生 | 短：封一批、生一批 |
| 流量內容特徵 | 轉送來的請求「明顯是 DeepSeek 產品使用者」（夾帶 DeepSeek 情境的內容） | 高：這是把流量歸因到 DeepSeek 的內生證據 | 中：只要 DeepSeek 持續轉送就存在 |
| harness 字串標籤的反向訊號 | 針對 Claude Code / Claude Agent SDK / OpenCode 使用者的選擇性轉送樣態 | 高：揭露對手的「價值分流」邏輯 | 中 |
| 思維簽章跨 session 再現 | 同一 reasoning signature 在不同 session 被帶回、被要求「還原」 | 極高：這是萃取 CoT 的直接技術訊號 | 長：只要簽章機制存在，重放樣態就可監測 |
| CoT-還原型提示樣態 | 「輸出先前推理」「翻譯先前工作記憶」等對抗性提示（p.145–146） | 高：可訓練分類器攔截 | 中：對手會持續變形提示 |
| 帳號池交叉 | 同一代理池同時替 DeepSeek / Alibaba / Xiaomi 轉送（p.148） | 中：協助跨組織關聯 | 中 |

**安全紅線遵守聲明**：本案頁段內無任何網域、IP、Telegram 帳號或雜湊值需抄錄；即使模組他處（如 p.33 Fraud 案）有 IOC 表，本教材亦僅作研究資料引用，**不對任何 IOC 進行連線、DNS 查詢或互動式查詢**，並保留報告原本的 defang 格式。

---

## 8. Anthropic 的偵測、處置與防線缺口

### 8.1 Anthropic 做了什麼（章節層級的分層防禦，p.153–154）

報告在「How we address illicit distillation」明確列出**分層防禦（layered defense）**，其中多項直接對應 DeepSeek 的手法：

1. **從「封帳號」升級到「歸因到組織」**：
   > *"Instead of banning proxy accounts individually, we work to attribute this suspicious activity to a specific organization, allowing us to take comprehensive enforcement actions more effectively."*
   
   用 metadata 與異常訊號辨識代理網路帳號，但**不逐一封鎖**，而是把可疑活動**歸因到特定組織**再全面處置。這正是為什麼報告能點名「DeepSeek」而不只是「一批可疑帳號」。

2. **反萃取分類器（adversarial-extraction classifiers）**：
   > *"We've also built classifiers designed specifically to detect adversarial extraction. When we are confident that a set of requests are associated with an illicit distillation campaign... we block the request and ban the associated accounts. We strengthened these classifiers... alongside the launch of Fable 5."*
   
   專門偵測「對抗性萃取」的分類器；判定為蒸餾即**封請求、封帳號**。隨 **Fable 5** 上線強化。

3. **推理摘要化（summarization）——DeepSeek 正是要繞過這一層**：
   > *"Claude now summarizes its internal reasoning before responding, which makes stolen transcripts less useful for training another model."*
   
   Claude 回應前**先摘要**內部推理，讓被偷的逐字稿對訓練別的模型用處變小。**本案關鍵扣連**：報告說 DeepSeek「exfiltrate reasoning traces that **would have otherwise been summarized**」——DeepSeek 的跨 session 重放，就是為了**繞過這層摘要化、取回完整未摘要的 CoT**。

4. **Fable 5.1 的「preserved thinking」——直接反制跨 session 重放**：
   > *"With Fable 5.1 we introduced preserved thinking, which stops new API accounts from altering the system prompt, tools, or messages that precede Claude's reasoning in multi-turn conversations. That reasoning is encrypted, but editing the context before it is a common technique attackers use to make Claude reveal it."*
   
   **這是針對 DeepSeek / Moonshot 攻擊的精準補丁**：跨 session 重放的關鍵，是攻擊者在「新 session」裡**竄改簽章前的上下文**來誘導 Claude 還原 CoT。preserved thinking **禁止新 API 帳號竄改推理前的 system prompt / 工具 / 訊息**，等於堵住了重放攻擊的施力點。推理內容本身則加密。

5. **身分驗證（identity verification）**：
   > *"When we detect signals of potential abuse, like the unauthorized resale of Claude or accounts operating from unsupported countries like China, Russia, and Iran, our systems can require users to verify their identity to retain access. Accounts that fail to do so are banned."*
   
   偵測到來自不支援國家（明確點名 China, Russia, Iran）或未授權轉售的訊號時，要求身分驗證，驗證失敗即封號。

6. **章節層級的預告**：p.149 承諾「We're introducing new methods to strengthen our defenses against these tactics.（我們正引入新方法強化對這些手法的防禦）」。

### 8.2 防線在哪裡失效 / 自曝的缺口（課程高價值素材）

品質紅線要求「務必挖出報告自曝的失效之處」。本案與章節多處誠實暴露了防禦的極限：

1. **思維簽章機制被完整繞過**：簽章設計原意是「原料不落地」，但攻擊者用**跨 session 重放**成功把完整 CoT 取回。報告直承 DeepSeek「circumvent our technical controls」。**一個設計良好的技術控制，被「濫用其正當功能 + 狀態切割」打穿**——這是防禦者最該記取的一課：**你的防禦功能本身，可能就是攻擊者的施力點**。

2. **摘要化只是「降低有用性」，不是「阻止萃取」**：報告用字是 makes stolen transcripts **less useful**（用處**變小**），而非 useless。DeepSeek 更透過重放**直接取回未摘要版本**，等於部分抵銷了這層防禦。

3. **補丁是「事後追趕」且綁定新版模型**：preserved thinking 要到 **Fable 5.1** 才有、classifiers 隨 **Fable 5** 才強化，且 preserved thinking 明講只擋「**new API accounts**」。這意味著**在這些防禦上線前的視窗期**，以及**舊模型 / 舊帳號**上，攻擊是奏效的——DeepSeek 的 12.1M 次互動正發生在 2026 年 7 月。**防禦與攻擊是持續的軍備競賽，報告本身就是「我們補了，但他們先得手了」的紀錄。**

4. **12,000 次提示實驗顯示防禦可被系統性繞過（p.145）**：報告承認某實驗室跑了**逾一萬二千次**、每次用不同技術測試哪種能萃取 CoT，「vast majority... rejected, but **some were successful**」，然後**用成功的技術發動更大規模攻擊**。這自曝了「分類器不是滴水不漏，且對手會系統化探測防線的縫隙」。

5. **偵測的本質是「事後歸因」而非「即時阻擋」**：報告能給出「14 天 1,210 萬次」這種**回溯統計**，恰恰說明這些流量**當下多半是通過的、事後才被歸因與統計**。偵測工程的殘酷現實：**你常常是在損害發生後，才拼出全貌**。

6. **「不支援國家」的地理管制靠代理輕易繞過**：身分驗證與地理限制是防線，但整個蒸餾生態的基礎就是**用代理網路 / 假身分繞過地理限制**（p.144）。這層防線與攻擊手法是「矛與盾」直接對撞，且矛（假帳號量產）成本遠低於盾（逐一驗證）。

> **教學總結**：本案是「**防禦有效但不充分**」的教科書範例。Anthropic 的防線不是沒用——它讓 Anthropic 能歸因、能統計、能發報告、能出補丁；但它**沒能即時阻止 1,210 萬次流量與俄中憑證外洩**。教學員理解「偵測（detection）、歸因（attribution）、阻擋（prevention）是三件不同難度的事，且阻擋最難」。

---

## 9. 第三方驗證與外部來源

本節嚴格區分每條來源是「**獨立查證（independent verification）**」還是「**僅引述 Anthropic（cites Anthropic only）**」，這是判斷情報是否為單一來源的關鍵。

### 9.1 判定：本案的「具體細節」目前是單一來源（Anthropic）

**本案最敏感的具體事實**——12.1M 次數、俄羅斯國防資料庫即時憑證、中國公安全民監控工具、harness 字串標籤手法——**目前只有 Anthropic 一個來源**。所有主流媒體報導這些細節時，**都是引述 Anthropic 的報告，沒有任何一家獨立查證了這些憑證或數字**。學員必須清楚：**這是單一來源情報（single-source intelligence）**，其可信度取決於對 Anthropic 遙測資料與誠信的信任。

### 9.2 外部來源清單

| # | 來源 | URL | 日期 | 性質判定 | 對本案的價值 |
|---|---|---|---|---|---|
| 1 | **Anthropic 原始報告**（一手） | anthropic.com/threat-intelligence-report-september-2026 | 2026-09-10 | 一手來源 | 本案唯一的具體事實來源 |
| 2 | **US FBI/NSA/CISA 聯合公告 AA26-251A** | cisa.gov/news-events/cybersecurity-advisories/aa26-251a | 2026-09-08 | **獨立政府評估**（但 References 有引 Anthropic） | **最強獨立佐證**：見 9.3 |
| 3 | TechCrunch | techcrunch.com/2026/09/10/anthropic-details-distillation-campaigns... | 2026-09-10 | **僅引述 Anthropic**（未獨立查證） | 確認報告存在、提及 OpenAI 曾就類似活動點名 DeepSeek |
| 4 | CNBC | cnbc.com/2026/09/11/chinese-ai-labs-moonshot-deepseek-alibaba-anthropic.html | 2026-09-11 | **僅引述 Anthropic** | 佐證 12.1M / 14 天數字；報導「四家公司未回應置評」 |
| 5 | CNBC（背景） | cnbc.com/2026/09/03/anthropic-distillation-battle-turns-to-dark-web-china-concerns-swell.html | 2026-09-03 | Anthropic 相關背景 | 報告發布前的鋪陳，蒸餾戰場延伸到暗網 |
| 6 | Quartz (Qz) | qz.com/anthropic-chinese-ai-labs-distillation-alibaba-deepseek-moonshot-091126 | 2026-09-11 | **僅引述 Anthropic** | 報導中國商務部 9/9 回應 |
| 7 | Al Jazeera | aljazeera.com/news/2026/9/9/china-slams-us-claims-of-industrial-scale-ai-theft | 2026-09-09 | **獨立報導中國官方回應** | 中國否認、稱蒸餾是「正常」商業行為 |
| 8 | 旺報／中時（台媒） | chinatimes.com/realtimenews/20260912001362-260409 | 2026-09-12 | 引述 Anthropic（繁中） | 「DeepSeek、月之暗面遭指轉送敏感資料」 |
| 9 | iThome（台媒） | ithome.com.tw/news/178864（另 174010） | 2026-09 | 引述 Anthropic（繁中） | 繁中技術媒體報導；標題提及「2.4萬詐欺帳戶」（見 9.5 caveat） |
| 10 | Newtalk 新聞（台媒） | newtalk.tw/news/view/2026-09-12/1059327 | 2026-09-12 | **未經證實傳言** | 「網傳月之暗面楊植麟等 16 人遭帶走」——**謠言，不可採信**（見 9.5） |
| 11 | law.asia / Rest of World / Berkeley Law（2025 舊案） | 見內文 | 2025 | **獨立記錄 2025 OpenAI-DeepSeek 舊案** | 建立 DeepSeek「被指蒸餾」的歷史脈絡 |

### 9.3 最強獨立佐證：FBI/NSA/CISA 聯合公告（AA26-251A，2026-09-08）

這是**獨立於 Anthropic** 的美國三大國安機構（NSA、CISA、FBI）聯合網路安全公告，**比 Anthropic 報告早兩天發布**，內容確認：

- **明確點名六家中國 AI 公司**：**DeepSeek、Moonshot AI、Alibaba、MiniMax、StepFun、Z.AI**（注意：與 Anthropic 報告的七家名單**重疊但不完全相同**——CISA 有 StepFun 但無 Xiaomi/SenseTime；見 9.4）。
- **針對 DeepSeek 的具體指控**：自**至少 2024 年底**起對美國前沿模型進行有組織蒸餾；用萃取資料**訓練其 R1 與 V3 模型**；萃取能力涵蓋「法律專業、API 規則驅動任務、chain-of-thought 推理、agentic 功能」；從**多個 Claude 與 GPT 版本**蒸餾。
- **被鎖定的美國模型**：Claude（Sonnet 3.7/4/4.5、Opus 4.1、Fable 5）、GPT 系列、Gemini、Grok。
- **質疑 DeepSeek 的成本敘事**：公告直指 DeepSeek 宣稱的「**560 萬美元**」訓練成本「misleading（誤導）」，因為**未計入蒸餾的成本**。（這條極重要——它把本案與 2025 年「DeepSeek 如何用極低成本做出 R1」的全球疑問直接連起來。）
- **政策建議與 Anthropic 不同**：CISA 建議「**悄悄劣化（subtly alter / degrade）** 對高信度蒸餾帳號的回應」而**非直接封鎖**，且不要讓對手知道回應被劣化了。**這與 Anthropic「block the request and ban the accounts（封請求、封帳號）」的做法形成有趣對比**——同一威脅，政府與廠商的最佳處置策略未必一致。

**判定**：AA26-251A 是**目前對「DeepSeek 進行工業級蒸餾」最有力的獨立佐證**。但要精確：它在 References 引用了 Anthropic，故並非「完全獨立不受 Anthropic 影響」；不過它是**多機構聯合評估、且涵蓋 Anthropic 報告以外的證據**（如 R1/V3 訓練、成本質疑），可信度高於單純轉述。**它佐證的是「DeepSeek 蒸餾美國模型」這個大命題，並未獨立證實 Anthropic 報告裡「俄羅斯憑證」「12.1M」等具體細節。**

### 9.4 中國官方回應（獨立來源，但是「否認」而非「查證」）

- **中國商務部（2026-09-09）**：稱美方指控「缺乏事實與法律依據」、是把「AI 產業正常的技術與商業行為政治化、武器化」；主張蒸餾是「產業普遍使用、美國公司自己也用」的中性技術方法；警告「若美國以蒸餾為藉口打壓中國 AI 企業，中國將採取堅決反制」。
- **中國外交部（發言人毛寧）**：呼籲美方「停止無端指責與抹黑」，稱「中國 AI 發展是高水準科技自立自強的結果」。

**判定**：這是**獨立於 Anthropic 的官方回應**，但性質是**政治否認**，**未提出反證**，也**未針對 Anthropic 的具體技術指控逐條回應**。且**中國官方回應的對象是「美國政府公告（AA26-251A）」，不是 Anthropic 報告本身**——這個區別學員要抓住：截至報導時點，**中國官方與 DeepSeek 都未直接回應 Anthropic**。

### 9.5 DeepSeek 本身的回應：沉默

多家媒體（CNBC、Qz、TechCrunch）報導：**Alibaba、DeepSeek、Moonshot、MiniMax 均未回應置評請求（did not respond to requests for comment）**。**DeepSeek 迄今對 Anthropic 的指控保持沉默**，未發表任何公開聲明。

**需標註的 caveat（避免以訛傳訛）**：
- **Newtalk「楊植麟等 16 人遭帶走」為未經證實的網路傳言**，且指涉的是 Moonshot（月之暗面）而非 DeepSeek，本教材**不採信、僅記錄其存在**，提醒學員警惕熱門事件周邊的謠言污染。
- iThome 標題出現的「**2.4 萬（24,000）詐欺帳戶**」數字，**未見於 Anthropic 報告的 DeepSeek 頁段**（報告只給了 Moonshot 5,380、Alibaba 近 5,000 + 第二池的帳號數；**DeepSeek 的帳號數在原文中並未給出**）。此「2.4 萬」**很可能是跨多家實驗室的彙總或該報導自行推估**，不應直接當成 DeepSeek 單獨的帳號數。**以 PDF 原文為準**。

### 9.6 歷史脈絡：從「被指蒸餾 OpenAI」到「被指轉送 Claude」（獨立舊案）

本案不能孤立看，必須放進 DeepSeek 的「蒸餾史」：

- **2025 年 1 月**：DeepSeek 發表 R1，以對標 GPT-o1 的效能 + 極低成本震撼全球。
- **OpenAI 的指控（2025 上半）**：OpenAI 指 DeepSeek 用其模型輸出訓練競品、違反使用條款；在**給美國國會的備忘錄**中稱 DeepSeek 用「distillation」與「obfuscated routers（混淆路由）」大規模抓取其模型。微軟資安研究員稱在 2024 年底偵測到疑似與 DeepSeek 相關的、透過 OpenAI API 的資料外流；並發現 DeepSeek 模型會**自稱是 OpenAI 開發的**。
- **DeepSeek 當時的回應**：對「是否蒸餾 OpenAI」未正面回應；僅表示 R1 的蒸餾**是以 Qwen2.5、Llama-3.1 為基礎**。
- **與本案的連續性**：
  1. **手法同源**：2025 用「obfuscated routers」抓 OpenAI；2026 用「transfer stations（轉運站）代理網路」抓 Claude——**都是用代理路由掩護的蒸餾**。
  2. **升級**：2025 是「拿 OpenAI 的輸出訓練」；2026 進一步到「**把自家使用者的流量轉送給 Claude**」——從「偷老師的作業」升級到「**把學生的考卷也一起賣了**」。
  3. **成本敘事的破口**：CISA 直指「560 萬美元」訓練成本說法「未計入蒸餾成本」——本案為「DeepSeek 低成本奇蹟是否建立在非法萃取之上」這個 2025 年就存在的質疑，**再添一筆**。

**判定**：2025 舊案由 OpenAI / 微軟 / 多家媒體獨立記錄，**與 Anthropic 無關**，是**獨立的、可佐證「DeepSeek 有蒸餾前科」的歷史來源**。它不能證明 2026 本案的具體細節，但能大幅提高「DeepSeek 從事蒸餾」這個行為模式的**先驗可信度（prior）**。

> **情報分析教學點**：單一來源情報（本案細節只有 Anthropic）+ 強烈的行為前科（2025 OpenAI 案）+ 獨立政府佐證大命題（CISA）= 一個「**具體細節待查、但整體圖像高度可信**」的情報態勢。學員要學會分層評估：**哪些是被獨立證實的、哪些是單一來源的、哪些是先驗推斷的**，不要一律當成同等確定。

---

## 10. 課程教學設計

### 10.1 核心教學要點

1. **非法蒸餾的定義與惡意升級**：從「用假帳號查詢偷輸出」（Alibaba/SenseTime）→「靜默轉送自家使用者並冒名」（DeepSeek/Moonshot）是質變。後者多了**冒名 + 隱私出賣 + 知情同意崩壞**三重惡化。
2. **AI 供應鏈信任問題**：「你以為在用 A、實際被轉送給 B、還被 C 蒐集」是全新的供應鏈威脅型態。傳統資安的「端點 / 網路 / 憑證」防護，對「你信任的 AI 供應商本身背叛你」無能為力。
3. **技術控制與其繞過的攻防迭代**：thinking signature（防禦）→ cross-session replay（繞過）→ preserved thinking / summarization（再補）。這是完整的協同演化教案。
4. **規模 vs 敏感度是兩種獨立的威脅維度**：DeepSeek 12.1M 次「不是最多」，但「內容最敏感」（俄中政府憑證與監控系統）。威脅評估不能只看量。
5. **蒸餾流量是雙面刃的情報側通道**：偷竊行為反過來讓被偷方（Anthropic）看見了俄中政府系統的活動。防禦者要理解「攻擊者的資料，也會洩漏攻擊者的意圖與其使用者的秘密」。
6. **信度用語的紀律**：high confidence / revealed / likely 的層次差異，對應「可觀測 vs 可推斷」。這是撰寫與閱讀威脅情報的基本功。
7. **單一來源 vs 多來源的判讀**：本案具體細節單一來源、大命題有政府獨立佐證、行為有歷史前科——三層可信度要分開評估。
8. **偵測 ≠ 阻擋**：能事後統計出 1,210 萬次，恰說明當下多半沒擋住。理解 detection / attribution / prevention 的難度階梯。

### 10.2 課堂討論題（有爭議、無標準答案）

1. **CISA 建議「悄悄劣化」蒸餾者的回應、Anthropic 選擇「直接封鎖」——哪種策略更好？** 悄悄劣化能否「反制訓練」（餵對手壞資料）？但這是否等於「主動污染」而有倫理 / 法律風險？如果被劣化的是一個**其實無辜的正當使用者**呢？
2. **DeepSeek 把使用者流量轉送給 Claude，責任該由誰負？** DeepSeek（未告知）？使用者（把國防憑證打進商用 AI）？還是 Anthropic（其模型成了被冒名的後端、且蒐集了不該看的資料）？三方責任如何分配？
3. **Anthropic 因蒸餾而「意外看見」俄中政府系統的即時活動——它該如何處理這些資料？** 通報美國政府？刪除？當成威脅情報？這是否讓 Anthropic 從「AI 廠商」變成了「事實上的情報蒐集者」？其中的法律與倫理界線在哪？
4. **蒸餾到底是「偷竊」還是「正常的技術學習」？** 中國官方稱蒸餾是「產業普遍、美國自己也用」的中性方法；OpenAI 一邊被指蒸餾、一邊被批「自己也未經授權爬全網資料」。**當每一方都在用別人的資料訓練時，「非法」的界線該畫在哪？** 是「違反 ToS」？「規模」？「是否冒名」？「是否出賣使用者」？
5. **「單一來源情報」該給多少權重？** 本案最勁爆的細節（俄羅斯憑證）只有 Anthropic 一個來源、且 Anthropic 是利害關係方（被偷的一方）。作為分析師，你會如何在報告裡標註這種「利害關係方提供的單一來源指控」？
6. **若你是台灣某金融機構 CISO**，員工回報「我們一直在用某第三方 App 裡的『DeepSeek』功能處理客戶資料」——依本案，你的即時處置與長期政策各是什麼？（延伸到 10.4）

### 10.3 實作／桌面演練建議（安全、不教攻擊操作）

> 所有演練均為**防禦 / 治理 / 分析導向**，不涉及任何攻擊操作或連線 IOC。

1. **威脅報告精讀與「信度標註」演練**：發給學員 p.149–150 原文，要求逐句標註每個主張的信度用語（revealed / likely / high confidence），並判斷每句是「可觀測事實」還是「推斷」。訓練情報閱讀紀律。
2. **「規模 vs 敏感度」風險排序桌演**：給出七家實驗室的規模數字（見第 2.5 節速查表）與各自最敏感的一筆內容外洩，讓小組排序「最該優先上報 / 處置」，並說明理由。刻意製造「量最大的不一定最該處理」的認知衝突。
3. **AI 供應鏈盡職調查（DD）清單設計**：讓學員為「採用某 AI 服務前」設計一份查核清單——如何確認「我的請求不會被轉送第三方？」「供應商的 ToS 與資料流向？」「是否有獨立稽核？」以本案為反面教材。
4. **偵測構想工作坊**：不寫攻擊、只寫**偵測**——給定「跨 session 簽章重放」「harness 字串標籤選擇性轉送」等行為，讓學員設計偵測邏輯（要看什麼遙測、設什麼閾值、如何降誤報）。對應第 5 / 7 節。
5. **框架缺口研討**：讓學員嘗試把本案三種「無框架可循」的行為（靜默轉送、簽章重放、字串標籤）提案為新的 ATLAS 技術條目，練習「當框架追不上威脅時如何結構化描述」。
6. **政策模擬——多國禁用決策**：分組扮演台灣數位發展部 / 美國 CISA / 企業 CISO，各自根據本案 + 2025 舊案，草擬一份「是否 / 如何限制 DeepSeek」的決策備忘錄，比較不同角色的取捨。

### 10.4 對台灣的意涵（必寫）

本案對台灣有**直接且具體**的政策與資安意涵，分四層：

**（1）為台灣 2025 年的禁用決策提供強力的「事後佐證」**

台灣**數位發展部於 2025 年 1 月底 / 2 月初，已禁止所有公部門、公立學校、國營事業、關鍵基礎設施使用 DeepSeek**，理由是「危害國家資訊安全」——當時的核心疑慮是「DeepSeek 的授權條款載明，蒐集自使用者的一切（含按鍵）都會回傳中國」，即**資料主權與回傳中國的風險**。

本案（GTG-16001）**為這個當年「基於疑慮」的預防性決策，提供了一個更具體、更嚴重的新證據面向**：台灣 2025 年擔心的是「DeepSeek 把使用者資料回傳中國」；本案揭露的是**更進一步的事實**——DeepSeek 不只可能回傳中國，還會**把使用者流量轉送給第三方（美國 Anthropic）、並蒐集下來訓練**，且**流量中曾出現政府 / 國防 / 監控系統的即時憑證與敏感設計**。換言之，**「用 DeepSeek 等於把資料交給不特定第三方」從 2025 年的推測，變成 2026 年有威脅報告佐證的事實**。這是台灣可用來**強化 / 續行 / 擴大**禁用政策的新論據。

**（2）第三方 App 夾帶「DeepSeek」的隱蔽風險——台灣使用者的實際暴露面**

台灣公部門雖已禁用 DeepSeek 官方管道，但**風險並未消除**，因為：
- 大量第三方 App、外掛、「AI 助理」整合了「DeepSeek 模型」作為後端選項，使用者未必意識到自己在用 DeepSeek。
- 本案證明：**你以為在用的「DeepSeek」，其流量可能被再轉送、被蒐集**。對台灣使用者而言，這是**雙層不透明**——第一層不知道 App 後端是 DeepSeek，第二層不知道 DeepSeek 又把它轉送給別人。
- **政策落差**：禁用「DeepSeek 官方 App」相對容易稽核；但禁止「所有內嵌 DeepSeek 的第三方服務」極難落實。台灣的資安治理需要從「禁單一 App」升級到「盤點 AI 供應鏈的實際模型流向」。

**（3）「憑證出現在蒸餾流量中」對台灣使用任何 AI 服務的普遍警示**

本案最該讓台灣記取的，**不只是「別用 DeepSeek」，而是「別把機敏資訊交給任何你無法確認資料流向的 AI」**：
- 俄羅斯國防 IT 人員、中國公安工程師，都是**在做敏感工作時，把即時憑證 / 系統設計打進了 AI**，結果外流。這個教訓**與 AI 是哪國的無關**——**任何** AI 服務（含美系）都可能記錄、可能外流你貼進去的憑證、原始碼、客戶資料。
- 對台灣的關鍵基礎設施、金融、半導體、國防產業：**應假設「貼進商用 AI 的任何內容，都可能被記錄並在你不知情下移動」**，據此建立「哪些資料絕不可貼進外部 AI」的分級禁令與 DLP（資料外洩防護）管控。
- 具體建議：（a）企業內部明訂「憑證 / 金鑰 / 未公開原始碼 / 客戶 PII 禁止貼入任何外部 AI」；（b）優先採用可稽核資料流向、可簽 DPA、可本地部署的 AI 方案處理機敏資料；（c）對「內嵌未知後端模型」的第三方 AI 工具做供應鏈盤點。

**（4）同一份報告另有「直接鎖定台灣」的案例，強化整體威脅圖像**

需向學員說明：**同一份 Anthropic 報告（不同章節）另揭露一起「電子戰模擬」案例**——某中國使用者用 Claude 開發電子戰軟體模組，並**把預設模擬目標改成 12 個台灣設施**（含指揮掩體、預警雷達站、愛國者 / 天弓飛彈陣地、主要空軍基地、戰區指揮部）。**該案屬「常規武器 / 電子戰」章節，不是本 DeepSeek 案**，但兩案並置，說明**中國實驗室 / 使用者對美國前沿 AI 的濫用，既有「偷能力」（蒸餾），也有「直接對台軍事應用」**——對台灣而言，這份報告的整體訊號是：**台灣同時是「AI 濫用的潛在資料受害者」與「AI 賦能軍事模擬的直接目標」**。（此段僅作跨案脈絡補充，細節請見該對應章節教材，勿與本案混淆。）

---

## 11. 關鍵原文引文（英文逐字 + 繁中翻譯，供講義引用）

> 以下引文均逐字錄自 PDF，標註頁碼。翻譯為本教材所加。

**引文 1（p.149，本案開篇 / 手法定調）**
> *"Our investigation revealed that DeepSeek also deployed tactics similar to Moonshot's. DeepSeek built a CoT extraction pipeline, relying on the same cross-session replay attack described above. DeepSeek also silently relayed exchanges to Claude without informing DeepSeek customers. Like GTG-16002, their customers were likely not made aware that their requests were being funneled to Claude."*
>
> 譯：我們的調查揭露，DeepSeek 也部署了與 Moonshot 類似的手法。DeepSeek 建立了一條 CoT 萃取管線，倚賴前述相同的跨工作階段重放攻擊。DeepSeek 也在未告知其客戶的情況下，靜默地把對話轉送給 Claude。與 GTG-16002 一樣，其客戶很可能未被告知他們的請求正被導流至 Claude。

**引文 2（p.150，針對 Opus 推理軌跡 / 繞過摘要化）**
> *"Our investigation revealed that DeepSeek targeted the reasoning traces of Opus, leveraging a similar technique to that of Moonshot. Using the reasoning signature, DeepSeek used the same cross-session replay attack used by Moonshot to extract CoT transcripts and circumvent our technical controls. DeepSeek used this technique to exfiltrate reasoning traces that would have otherwise been summarized."*
>
> 譯：我們的調查揭露，DeepSeek 鎖定了 Opus 的推理軌跡，運用與 Moonshot 類似的技術。利用思維簽章，DeepSeek 使用與 Moonshot 相同的跨工作階段重放攻擊來萃取 CoT 逐字稿並繞過我們的技術控制。DeepSeek 用此技術外洩了那些原本會被摘要化的推理軌跡。

**引文 3（p.150，harness 字串標籤 / 精準分流）**
> *"DeepSeek rerouted requests from users that were attempting to use one of DeepSeek's models through third-party or Anthropic coding harnesses, like Claude Code, the Claude Agent SDK, or OpenCode. DeepSeek checked various strings included in inbound requests, tagging users that were using these third-party harnesses. Selected tagged users then had their requests relayed to Claude Opus. This sensitive data was likely routed to Anthropic without the knowledge or consent of DeepSeek's customers."*
>
> 譯：DeepSeek 把「試圖透過第三方或 Anthropic 編碼工具框架（如 Claude Code、Claude Agent SDK 或 OpenCode）使用 DeepSeek 模型」的使用者請求重新導向。DeepSeek 檢查進站請求中夾帶的各種字串，對使用這些第三方框架的使用者打標籤。被選中打標籤的使用者，其請求隨後被轉送至 Claude Opus。這些敏感資料很可能在 DeepSeek 客戶不知情、未同意的情況下被送往 Anthropic。

**引文 4（p.150，俄羅斯國防機關——本案最敏感，逐字保留）**
> *"Russian defense agency. DeepSeek relayed requests from an IT operator working with data from a Russian government agency associated with its Ministry of Defense. The relayed requests exposed live credentials for a Russian government database."*
>
> 譯：俄羅斯國防機關。DeepSeek 轉送了一名 IT 操作人員的請求，該人員處理的是一個與俄羅斯國防部相關之政府機關的資料。被轉送的請求暴露了一個俄羅斯政府資料庫的即時憑證。

**引文 5（p.150，中國公安監控——注意此案講的是工具功能而非憑證）**
> *"PRC police surveillance. Engineers building a case management system for a municipal Public Security Bureau in China used DeepSeek, which relayed those requests to Claude. The engineer built a tool that compares a person's movements against police records using the national ID number of citizens."*
>
> 譯：中國警方監控。在中國替某市級公安局建置案件管理系統的工程師使用了 DeepSeek，DeepSeek 把這些請求轉送給 Claude。該工程師打造的工具，會用公民的國民身分證號，把一個人的移動軌跡與警方記錄進行比對。

**引文 6（p.150，本案規模數字——逐字）**
> *"Scale of distillation attacks attributable to DeepSeek over 14 days in July 2026: over 12.1 million exchanges observed."*
>
> 譯：2026 年 7 月的 14 天內，可歸因於 DeepSeek 的蒸餾攻擊規模：觀察到超過 1,210 萬次互動。

**引文 7（p.148，思維簽章防禦機制——本案技術背景）**
> *"When responding, Claude returns a reference to its raw thinking as a "thinking signature" instead of the raw thinking to mitigate the risk of unauthorized distillation. This is used by our API to look up the raw thinking trace in subsequent calls to the API."*
>
> 譯：Claude 回應時，會回傳一個指向其原始思維的參照——稱為「思維簽章」——而非原始思維本身，以降低未經授權蒸餾的風險。此簽章供我們的 API 在後續 API 呼叫中查回原始思維軌跡之用。

**引文 8（p.146，章節層級點名 DeepSeek 涉及使用者資料濫用與隱私）**
> *"DeepSeek, Xiaomi, and Moonshot fed conversations between their own models and users into Claude. These labs then used Claude's responses as training data with which to distill Claude's capabilities. Some of these exchanges included sensitive information... These practices are likely inconsistent with privacy laws and the labs' own terms of service."*
>
> 譯：DeepSeek、Xiaomi 與 Moonshot 把它們自家模型與使用者之間的對話餵給了 Claude。這些實驗室接著把 Claude 的回應當作訓練資料，用以蒸餾 Claude 的能力。其中部分對話含有敏感資訊……這些作為很可能與隱私法律以及這些實驗室自己的服務條款相牴觸。

---

## 12. 未能驗證之處與研究限制

1. **本案具體事實為單一來源（Anthropic）**：12.1M 次數、俄羅斯政府資料庫即時憑證、中國公安全民監控工具、harness 字串標籤——**均只有 Anthropic 一個來源，且 Anthropic 是被侵害的利害關係方**。無任何第三方獨立查證這些具體細節。應以「利害關係方提供的高信度單一來源指控」看待。

2. **報告未提供 DeepSeek 的帳號數等技術指標**：不同於 Moonshot（5,380 帳號、多在新加坡 / 日本）與 Alibaba（近 5,000 + 第二池），**DeepSeek 頁段未給出假帳號數量、地理分布、IP 或任何 IOC**。台媒（iThome）標題出現的「2.4 萬詐欺帳戶」**未見於原文對應段落**，很可能是跨實驗室彙總或報導推估，本教材不採為 DeepSeek 單獨數字。

3. **「憑證」一詞只適用俄羅斯案，不適用中國公安案**：務必避免把兩案都概括成「憑證外洩」。中國公安案原文描述的是監控**工具的功能**，未提憑證。本教材第 3.1 節已據原文更正此常見誤述。

4. **DeepSeek 與中國官方均未直接回應 Anthropic**：DeepSeek 對置評請求未回應；中國商 / 外交部的回應對象是**美國政府公告（AA26-251A）**，非 Anthropic 報告，且屬政治否認、未提反證。因此**「DeepSeek 對本案的說法」目前是空白**，無法呈現對造版本。

5. **CISA 公告與 Anthropic 報告的名單不一致**：Anthropic 列七家（含 Xiaomi、SenseTime、Zhipu），CISA 列六家（含 StepFun、無 Xiaomi/SenseTime）。兩者重疊但不相同，顯示不同機構掌握的證據範圍不同；本教材未能取得能完全解釋此差異的一手資料。

6. **報告的時間軸與模型命名屬其自身框架**：報告內出現 Opus 4.6/4.8、Fable 5/5.1、Mythos 5/Preview 等模型與 2026 年的日期，均依報告與整理當日（2026-09-13）的時間框架呈現；部分模型細節無法由本案頁段外的公開資料完全交叉驗證。

7. **未經證實的周邊傳言已排除**：如 Newtalk「月之暗面 16 人遭帶走」屬網路傳言、且指涉 Moonshot 非 DeepSeek，本教材僅記錄其存在以示警，不納入事實。

8. **CISA「悄悄劣化回應」的建議與 Anthropic「封鎖」做法的優劣**，屬政策判斷、無定論，本教材列為討論題（10.2）而非結論。

---

*（本教材依《00-agent-brief.md》產出規格撰寫；所有具體主張均可追溯至 PDF 頁碼或第 9 節所列 URL。安全紅線：未對任何 IOC 進行連線或查詢；引用保留報告原本格式。）*


---

# 技術附錄（第二階段技術深化增補，2026-09-14）

> **增補說明**：本附錄為「技術深化 pass」新增，**不改動上方第 1–12 節任何既有內容**。目的是把本案補到「技術高手能據以理解與防禦」的深度——靜默轉送與推理軌跡蒸餾的**技術實作機制**、憑證外洩的**側通道意義與企業 DLP 防護**（含可直接部署的偵測規則）、規模／敏感度的**量化模型**、DeepSeek **蒸餾史的技術脈絡**，並以 **Mermaid** 重繪關鍵資料流、跨 session 重放時序、DLP 閘道架構與規模／敏感度二維定位。
>
> **本附錄共 4 張 Mermaid 圖**：① 靜默轉送＋憑證洩漏資料流（A5）、② 規模／敏感度二維定位（A6，任務指定）、③ 跨 session 簽章重放時序（A2）、④ 企業 prompt-DLP 閘道架構（A5）。其中 ①② 為任務明確指定的兩張核心圖。
>
> **安全紅線遵守**：本附錄未新增任何來自報告 IOC 表的網域／IP／雜湊；偵測規則中出現的第三方 AI 端點僅以**子字串比對關鍵字**（如 `deepseek`）與**佔位符**呈現，**不列出可直接連線的完整 FQDN、未做任何連線或 DNS 查詢**；規則中的網段、主機名前綴均為**部署佔位範例**。攻擊者用來套取 CoT 的提示（p.145–146）僅作**類型化描述供偵測**，不逐字轉錄。

---

## A1. 靜默轉送（silent relay）的技術實作剖析

主文第 4 節已從「攻擊生命週期」角度描述靜默轉送。此處補「**技術上這條轉送鏈到底怎麼搭起來**」，讓學員能據以設計偵測與防禦。

### A1.1 轉送鏈的元件與資料落地點

DeepSeek 能做到「使用者以為在用 DeepSeek、實際被送去 Claude」，前提是它**控制了使用者請求的入口**。一條可運作的轉送鏈至少包含四個環節：

1. **Ingress / 反向代理層（DeepSeek 自控）**：使用者的用戶端（App、IDE 外掛、CLI harness）向「DeepSeek 端點」發出請求。此端點終止 TLS（TLS termination），因此 **DeepSeek 在此看到的是完整明文**——包含 system prompt、對話歷史、工具呼叫、以及使用者不小心貼進去的**憑證與機敏資料**。這是第一個明文落地點。
2. **標籤／分流引擎（tagging engine）**：對明文做字串比對（見 A1.2），決定「自家模型回應」或「轉送 Claude」。
3. **transfer stations 代理網路（灰市代理，可能與 Alibaba 共用，見主文 2.4）**：被選中的請求，透過**偽冒的 Claude 帳號**（假身分／盜刷卡／盜用 API 金鑰）打向 Anthropic，藉此繞過地理限制與存取控制。這是第二個明文落地點（代理商也看得到）。
4. **Anthropic Claude Opus API（被冒名的後端）**：Claude 正常回應。這是第三個、也是**本案戲劇性的關鍵**明文落地點——**使用者的俄羅斯政府資料庫即時憑證，就是在這一步進入 Anthropic 的可觀測範圍**（詳見 A5）。

> **偵測工程要點**：一份請求的明文，在使用者不知情下**至少經過三方**（DeepSeek ingress、代理商、Anthropic）。「你貼進 AI 的東西只有 AI 供應商看得到」這個直覺，在轉送架構下**完全失效**。這是 A5「機敏資訊不進 AI 請求」防護的根本理由。

### A1.2 harness 指紋辨識：DeepSeek「檢查進站字串」比對的是什麼

報告原文（p.150）僅說 *"DeepSeek checked various strings included in inbound requests, tagging users that were using these third-party harnesses"*。以下是**依公開技術常識重建**的可比對指紋面向（**非報告逐字內容**，供設計偵測／理解手法）——凡是使用 Claude Code / Claude Agent SDK / OpenCode 的用戶端，其請求都會攜帶下列**高辨識度特徵**：

| 指紋面向 | 可比對的技術特徵（重建） | 為何高辨識度 |
|---|---|---|
| HTTP 標頭 | `User-Agent` / 用戶端識別字串（SDK/CLI 版本標記）、`anthropic-beta` 等自訂標頭 | harness 會帶固定客戶端指紋 |
| API 形狀（shape） | Anthropic Messages API 特有結構：`system` 陣列、`tools` JSON schema、`thinking` 參數、`stop_sequences`——與 OpenAI-相容格式明顯不同 | 請求「長得像 Anthropic 呼叫」本身就是訊號 |
| System prompt 樣板 | 各 harness 注入的**特徵性指示樣板與保留標記**（如工具前言、`<system-reminder>` 類標記） | 這些樣板文字幾乎固定、可字串比對 |
| 工具 schema 名稱 | 編碼 harness 特有的工具名（bash / str_replace / read / edit 類 JSON 工具定義） | 工具名集合是強指紋 |

**這解釋了主文 3 的「精準價值分流」**：使用這些 harness 的多為開發者／進階使用者，其多輪、含工具呼叫與複雜推理的請求，正是蒸餾**高階 agentic / coding / reasoning 能力**最有價值的原料。DeepSeek 不是無差別全抓，而是**用指紋在自家流量裡篩出最值錢的受害者**再轉送。

> **給防禦方的反向啟示**：同一套指紋邏輯，企業可反過來用在**egress（出向）**——偵測「我的哪些主機正在對外發出 Anthropic/OpenAI 形狀的 API 呼叫、且目的地不在核可清單」，見 A5 的 Sigma / KQL 規則。

---

## A2. 推理軌跡蒐集：CoT 蒸餾的技術原理與 thinking signature 攻防

主文 4.1 已詳解 thinking signature 與跨 session 重放的**機制**。此處補「**為什麼推理軌跡是皇冠上的寶石**」「**技術上如何被拿去訓練**」，以及**學術界對此攻擊面的獨立研究**。

### A2.1 為什麼 CoT 是最高價值的蒸餾原料（teacher→student）

知識蒸餾的本質是「**用強模型（teacher）的輸出當弱模型（student）的訓練標的**」。對**推理模型**而言，最有價值的不是最終答案，而是**通往答案的完整思考鏈（chain-of-thought, CoT）**：

- **SFT 冷啟動資料**：DeepSeek-R1 的訓練方法（見 A7）本身就以「一批 CoT 範例（curated chain-of-thought exemplars）」做冷啟動監督微調。**別家模型的高品質 CoT 逐字稿，正是這種冷啟動資料的完美來源**——偷來即用。
- **RL 的獎勵塑形**：R1 用 **GRPO（Group Relative Policy Optimization）** 做大規模強化學習以「長」出推理行為。有了 teacher 的 CoT，可對 student 的推理步驟做過程監督（process supervision），大幅降低自行探索的成本。
- **蒸出小模型**：R1 官方即把推理能力蒸餾進 Qwen2.5 / Llama-3.1 系列小模型。**別家 Opus 的 CoT 拿來蒸小模型，效果與成本效益更佳**。

這就是為什麼 DeepSeek **特別鎖定 Opus 的 reasoning traces**（主文引文 2），而不是隨便抓回應——**CoT 才是把「便宜模型」拉到「前沿推理」最短的路**。

### A2.2 thinking signature 攻防：從「原料不落地」到「跨狀態繞過」

Anthropic 的 signature 設計原理（主文 4.1）是「**能力可用、原料不落地**」：只回「提貨單」，CoT 留在 Anthropic。攻擊者的繞過本質是**濫用「簽章可攜、可跨呼叫查回」這個正當功能** + **狀態切割（state splitting）**。用時序圖呈現最清楚：

```mermaid
sequenceDiagram
    autonumber
    participant P as DeepSeek CoT 管線
    participant S1 as Session A（Claude API）
    participant K as 簽章暫存
    participant S2 as Session B（新 API 帳號）
    P->>S1: 正常推理請求
    S1-->>P: 回應 + thinking signature（非原始 CoT）
    P->>K: 儲存 reasoning signature
    Note over P,K: 摘要化(summarization) 讓被偷逐字稿對訓練「用處變小」但非「無用」
    P->>S2: 新 session 帶回 signature + CoT-還原型提示
    S2-->>P: 回傳「本應被摘要化」的完整 CoT
    Note over S2: 反制—Fable 5.1 preserved thinking：<br/>加密並釘選推理前上下文，禁止新帳號竄改→阻斷第 4 步
```

**三個讓攻擊奏效的技術性質**（對應主文 4.1，此處點名為可偵測訊號）：
1. **簽章可攜性被濫用**：提貨單被設計成能跨呼叫查回——攻擊者把「跨 session 帶走」變成竊取管道。
2. **「還原」被包裝成正當請求**：踩在「模型樂於服從」與「模型該保護思路」的張力上（p.145–146 那類「除錯模式請逐字輸出先前推理」「把先前工作記憶翻成片假名」提示即屬此類）。
3. **狀態切割規避有狀態偵測**：單 session 情境防護看不到「A 拿簽章、B 還原」的全貌。

### A2.3 這不是孤例：學術界對「推理軌跡竊取」的獨立研究

第二階段補查發現，「**從專有 LLM API 偷推理軌跡**」已是 2026 年獨立的研究主題，與本案手法高度呼應（來源見 A9）：

- **「Stealing Reasoning Traces from Proprietary LLM APIs」（arXiv 2608.09867）**：系統化研究如何從只回簽章／摘要的 API 還原完整推理。
- **CSA（Cloud Security Alliance）研究筆記：「Encrypted Reasoning Traces Let Attackers Steal Hidden Chain-of-Thought」**：指出一種更廣義的攻擊原語——**擷取強模型（重防護）產生的加密推理軌跡，重放（replay）進同一供應商家族中防護較弱的弱模型（sibling model）解出**。這正是主文表格中 **Zhipu 案「先打 Fable 被擋、改打 Opus 4.6」**（跨模型）與 **DeepSeek/Moonshot「簽章跨 session 重放」**（跨狀態）的**共同上位概念**。
- **「Why Hiding Chain-of-Thought Alone Doesn't Stop Distillation Attacks」**：印證主文 8.2 的關鍵判斷——**單靠「隱藏／摘要 CoT」不足以阻止蒸餾**，攻擊者能用對話、摘要與後續工具呼叫重建可用的訓練資料。

> **教學收斂**：本案不是 Anthropic 獨有的偶發事件，而是**整個前沿 LLM 產業共同面對的新攻擊面**。thinking signature / preserved thinking 是「防禦性設計」的一種答案，但學術界已證明這條戰線會持續演化——這使主文 4.1、8.2 的「攻防協同演化」框架更具普遍教學價值。

---

## A3. DeepSeek vs Moonshot：同源手法的技術異同（補主文 2.5）

主文 2.5 的速查表偏「案件層級比較」。此處聚焦 **16001（DeepSeek）與 16002（Moonshot）兩個「冒名轉送」案的技術差異**，因為報告反覆用 "similar to Moonshot's" 綁定兩案，學員須能講清**哪裡相同、哪裡是 DeepSeek 的獨門加碼**。

| 技術面向 | Moonshot（GTG-16002） | DeepSeek（GTG-16001） | 差異意義 |
|---|---|---|---|
| CoT 萃取管線 | 首見；建立跨 session 重放 | **原樣沿用** Moonshot 手法 | DeepSeek 是「快速跟隨者」，非原創 |
| 目標分流邏輯 | 報告未強調字串標籤 | **獨門 harness 字串標籤**，精準挑 Claude Code/Agent SDK/OpenCode 使用者 | DeepSeek 的分流「更精準、更工程化」 |
| 鎖定模型 | Claude（含 Fable 5，據 CISA） | **明確鎖定 Opus 推理軌跡** | DeepSeek 直取最強推理等級 |
| 規模／時窗 | 逾 2,300 萬次／2026-05–07 | 逾 1,210 萬次／2026-07 的 14 天 | DeepSeek 規模較小但**日均更密集** |
| 流量敏感度 | PLA 相關成都 CCTV、國企即時憑證 | **俄羅斯國防 DB 即時憑證 + 中國公安全民監控工具** | 兩案皆爆憑證，**DeepSeek 敏感度更高**（跨國國防級） |
| 知情同意 | 報告：不知 Moonshot 是否告知客戶 | 報告：客戶「very likely / almost certainly not made aware」 | 同屬「知情同意崩壞」類 |

> **重點**：**技術機制兩案共用；DeepSeek 的加碼在「分流精準度」與「流量內容的敏感度」**。這解釋了為何本教材把 DeepSeek 定位為「這類手法中內容後果最嚴重的一例」。

---

## A4. CISA AA26-251A 的官方 MITRE ATLAS 對應（補強主文第 5 節）

主文第 5 節自行做了 ATT&CK/ATLAS 對應並誠實標了框架缺口。第二階段補查取得 **FBI/NSA/CISA 聯合公告 AA26-251A 官方列出的 MITRE ATLAS 技術**，可與主文第 5 節互相校準（來源見 A9）：

| AA26-251A 官方對應（ATLAS） | 技術名 | 對應本案階段 |
|---|---|---|
| **AML.T0008** | Acquire Infrastructure | 建代理網路 / transfer stations（主文階段 0） |
| **AML.T0040** | AI Model Inference API Access | 透過代理打進 Claude API（階段 2） |
| **AML.TA0008** | Discovery（戰術） | 探測模型能力邊界 |
| **AML.T0051** | LLM Prompt Injection | CoT-還原型提示（階段 3） |
| **AML.T0054** | LLM Jailbreak | 誘導 Claude 吐推理軌跡（階段 3） |
| **AML.T0042** | Verify Attack | 一萬二千次提示實驗篩「哪種能成功」（主文 8.2 第 4 點） |
| **AML.TA0009** | Collection（戰術） | 蒐集回應 + CoT（階段 4） |
| **AML.T0024.002** | Exfiltration via AI Inference API | 蒸餾核心：大量外洩模型能力 |
| **AML.T0048** | External Harms | 對第三方（模型擁有者、被轉送使用者）造成外部傷害 |

**框架調和說明**：主文 5 使用 `AML.T0024.001` 與 `AML.T0057（LLM Data Leakage）`；CISA 官方採 `AML.T0024.002（Exfiltration via AI Inference API）` 並補上 `AML.T0042 Verify Attack`。兩者指向**同一件事——經推理 API 外洩模型能力**；差異來自 ATLAS 子技術編號的版本演進。教學上應向學員說明：**同一行為在不同框架版本／不同機構文件可能對到不同 ID，重點是描述清楚行為本質，而非拘泥單一 ID**（呼應主文 5.1「框架缺口是常態」的職業素養）。CISA 官方對應**仍未涵蓋主文 5.1 指出的三項最新穎行為**（靜默轉送自家使用者、簽章跨狀態重放、字串標籤精準分流），佐證了主文的框架缺口判斷。

---

## A5. 「流量暴露憑證」的技術意義與企業 DLP 防護（本案最戲劇性，深化）

這是本案在資安上最該被記取的一課。主文第 3 節精準區分了「俄羅斯＝憑證、中國公安＝監控工具功能（非憑證）」；此處補**技術層面的三個問題**與**可落地的企業防護**。

### A5.1 (a) 蒸餾流量本身，就是洩漏使用者活動的側通道

**技術意義**：蒸餾攻擊者為了偷模型，把**真實使用者的完整請求明文**搬運到 Anthropic。這條「為偷 A（模型能力）而搬運的資料」，同時夾帶了 B（使用者在做什麼）。於是：

- **蒸餾流量 = 使用者活動的側通道（side-channel）**：看流量內容，就能反推「DeepSeek 的使用者群在做什麼」——本案揭露出的，是**俄羅斯國防 IT、中國公安工程、某旗艦 AI 專案戰略**這類國家級敏感作業。
- **這是「非預期情報收穫（unintended intelligence windfall）」**：Anthropic 沒有去蒐集，卻因「被偷」而被動獲得對俄／中政府系統的**即時可見度**。偷竊者把被害者（俄中政府使用者）的機敏資料，親手送進了美國公司的伺服器。

### A5.2 (b) 機敏資訊出現在 AI 請求中的資料外洩風險（技術路徑）

**風險的技術本質**：LLM 請求是**純文字 payload**，使用者為了「讓 AI 幫我 debug / 分析 / 寫程式」，會很自然地把**真實憑證、連線字串、原始碼、客戶 PII、系統設計**直接貼進 prompt。一旦貼入：

1. 明文在傳輸鏈上**至少三方可見**（A1.1）。
2. 供應商（或冒名轉送方）可能**儲存**該請求（本案 DeepSeek 明確存下來訓練）。
3. 憑證一旦進入他方訓練語料，理論上可能在**未來模型輸出中被重現（memorization / training-data leakage）**。
4. **即時憑證（live credentials）比歷史資料更危險**——它當下可用，外洩＝可被立即利用（雖可輪替，但輪替前的視窗期即風險）。

**這條路徑與「AI 是哪一國的」無關**：俄羅斯國防 IT 與中國公安工程師，都是**在做敏感工作時把即時憑證／系統設計打進了 AI**。教訓對任何 AI 服務（含美系）皆成立。

### A5.3 (c) 為何這讓 Anthropic「意外看見」第三方系統活動——資料流圖

關鍵在 A1.1 的**明文落地點**：轉送架構使「本該只在 DeepSeek↔使用者之間」的明文，**被搬到 Anthropic 的可觀測範圍**。以下 Mermaid 圖呈現完整資料流與憑證洩漏、以及「非預期可見性」的產生點：

```mermaid
flowchart TB
    subgraph USER["DeepSeek 使用者（誤以為在用 DeepSeek）"]
      U1["俄羅斯國防 IT<br/>政府DB 即時憑證"]
      U2["中國公安工程師<br/>身分證比對監控工具設計"]
      U3["中國科技公司員工<br/>旗艦AI專案完整規格"]
      H["Claude Code / Agent SDK / OpenCode"]
    end
    U1 --> H
    U2 --> H
    U3 --> H
    H -->|"含機敏內容的請求（明文）"| GW
    subgraph DS["DeepSeek 入口（攻擊者控制）"]
      GW["Ingress Reverse-Proxy<br/>TLS 終止＋檢查進站字串"]
      TAG{"字串標籤<br/>是否為 Claude harness"}
      STORE[("蒸餾資料湖<br/>對話＋CoT → 訓練")]
      GW --> TAG
    end
    TAG -->|"否｜自家模型回應"| OWN["DeepSeek V3/R1"]
    subgraph PROXY["transfer stations 代理網路（假帳號／盜用金鑰）"]
      RELAY["偽冒 Claude 帳號轉送"]
    end
    TAG -->|"是｜靜默轉送"| RELAY
    subgraph AN["Anthropic（被冒名的後端）"]
      ANTH["Claude Opus API"]
      SIG["回傳 thinking signature（非原始 CoT）"]
      ANTH --> SIG
    end
    RELAY -->|"使用者明文含憑證，經第三方送出"| ANTH
    SIG -->|"跨 session 重放 → 還原完整 CoT"| RELAY
    RELAY -->|"Claude 回應（冒充成 DeepSeek）"| GW
    GW -->|"使用者以為是 DeepSeek 回的"| H
    RELAY --> STORE
    ANTH -.->|"非預期可見性"| WIN["側通道情報<br/>Anthropic 意外看見俄／中政府系統活動"]
    classDef leak fill:#fde,stroke:#c33,color:#900;
    class U1,U2,U3,WIN leak;
```

**圖的核心訊息**：紅色節點是「洩漏源」與「非預期可見性」。**憑證從使用者端出發，經 DeepSeek→代理→Anthropic，一路都是明文**；`ANTH -.-> WIN` 這條虛線就是「Anthropic 為何會看見俄中政府活動」的技術答案——**因為冒名轉送把明文送進了它的後端**。

### A5.4 企業技術防護：「機敏資訊不進 AI 請求」

本案給企業的第一守則是：**假設「貼進任何外部 AI 的內容都可能被記錄、被移動」，據此在資料離開組織前就攔下機敏值**。核心是一道 **inline egress broker（出向仲介）＝ Prompt-DLP Gateway**：

```mermaid
flowchart LR
    U["員工 / AI Agent"] -->|prompt| S1
    subgraph GW["Prompt-DLP Gateway：inline egress broker"]
      S1["Stage1 正則比對<br/>API金鑰/私鑰/JWT/連線字串/身分證號（亞毫秒）"]
      S2["Stage2 語意 NER<br/>PII/未公開原始碼/國防敏感實體"]
      POL{"政策判定"}
      RED["Smart Redaction<br/>以佔位符替換機敏值"]
      S1 --> S2 --> POL
      POL -->|"可去識別"| RED
    end
    POL -->|"命中禁令"| BLOCK["阻擋＋告警（SIEM/DLP）"]
    POL -->|"乾淨"| ALLOW["放行"]
    RED --> ALLOW
    ALLOW --> LLM["核可 AI 端點<br/>可簽 DPA／可稽核／可本地部署"]
    LLM -->|"回應"| REPOP["本地還原佔位符"] --> U
    POL -->|"deny-by-default：未核可端點"| NONAPP["DeepSeek 等未知後端（封鎖）"]
    classDef deny fill:#fdd,stroke:#c00,color:#900;
    class NONAPP deny;
```

**兩階段偵測（hybrid detection）**——第一階段用**正則**抓結構化機敏（亞毫秒延遲），第二階段用**語意 NER** 抓非結構化敏感實體：

```text
# Prompt-DLP Stage-1 結構化機敏樣式（gitleaks/trufflehog 風格；部署於 egress broker）
# AWS Access Key ID
AKIA[0-9A-Z]{16}
# AWS Secret Access Key（帶語境）
(?i)aws.{0,20}(secret|private).{0,20}['"]?[A-Za-z0-9/+=]{40}['"]?
# 私鑰 PEM 區塊
-----BEGIN (RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----
# JWT
eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}
# 通用 API 金鑰 / 權杖
(?i)(api[_-]?key|access[_-]?token|secret|bearer)['"]?\s*[:=]\s*['"]?[A-Za-z0-9._\-]{20,}
# 資料庫連線字串（含密碼）— 對應本案「俄羅斯政府資料庫即時憑證」情境
(?i)(postgres(ql)?|mysql|mongodb(\+srv)?|redis|mssql)://[^\s:'"]+:[^\s@'"]+@[^\s/'"]+
# GitHub PAT / Slack / Google API key
ghp_[0-9A-Za-z]{36}
xox[baprs]-[0-9A-Za-z-]{10,48}
AIza[0-9A-Za-z_\-]{35}
# 中國公民身分證號（18 碼）— 對應本案公安監控工具情境
[1-9]\d{5}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[0-9Xx]
# 台灣身分證字號（本地情境）
[A-Z][12]\d{8}
```

**Smart Redaction（可用性與安全兼顧）**：命中後不必一律阻擋——可**以佔位符替換機敏值**送給 AI（AI 仍能推理任務），回應回來後在**使用者本地端還原**，機敏值全程不出組織（見圖中 `RED → REPOP` 路徑）。這比「一律封鎖」更能兼顧生產力，是本案「使用者為了 debug 而貼憑證」情境的正解。

**網路層 egress 控制（預設拒絕）**——偵測「敏感主機連往未核可 LLM 端點」，防止流量流入會轉送／記錄的第三方（如 DeepSeek 情境）：

```yaml
title: Sensitive-Segment Egress to Unsanctioned GenAI/LLM Endpoint
id: 3a9b7e42-0c14-4d7a-9e21-deepseek16001
status: experimental
description: >
  以「預設拒絕＋核可清單」邏輯偵測敏感網段主機連往未核可 LLM 推理端點，
  防止提示中的機敏資料流入會轉送/記錄的第三方 AI。端點清單請以貴組織核可清單為準。
logsource:
  category: proxy
detection:
  llm_endpoints:
    c-uri-path|contains:
      - '/v1/messages'
      - '/v1/chat/completions'
      - '/api/generate'
  known_unsanctioned:
    c-uri|contains:
      - 'deepseek'          # 子字串比對；不列出可直連 FQDN
  sanctioned:
    c-uri-host:
      - 'api.anthropic.com'
      - 'REPLACE-with-your-approved-endpoints'
  sensitive_src:
    src_ip|cidr:
      - '10.20.0.0/16'      # 部署佔位：R&D／財務／OT 跳板網段
  condition: sensitive_src and ( known_unsanctioned or (llm_endpoints and not sanctioned) )
falsepositives:
  - 已核可之 AI 試點（維護 allowlist）
level: high
tags:
  - attack.exfiltration
  - atlas.AML.T0024.002
```

```kql
// Microsoft Sentinel / Defender：敏感主機連往未核可 GenAI 端點
let Sanctioned = dynamic(["api.anthropic.com"]);        // 貴組織核可清單（佔位）
let SensitiveHosts = dynamic(["FIN-","RND-","OT-"]);    // 敏感主機名前綴（佔位）
DeviceNetworkEvents
| where Timestamp > ago(24h)
| where RemoteUrl has_any ("deepseek","/v1/messages","/v1/chat/completions","/api/generate")
| where not (RemoteUrl has_any (Sanctioned))
| where DeviceName has_any (SensitiveHosts)
| summarize Hits=count(), Endpoints=make_set(RemoteUrl, 20)
    by DeviceName, InitiatingProcessFileName, InitiatingProcessAccountUpn, bin(Timestamp, 1h)
| order by Hits desc
```

**供應商側（Anthropic 類）反制邏輯**（概念示意，僅供理解，非可直接部署——只有供應商握有此遙測）：

```text
# 跨 session 簽章重放偵測（概念邏輯）
score = 0
if request.carries(reasoning_signature):
    sig = request.reasoning_signature
    if sig.origin_session_id != request.session_id:            # 跨 session
        score += 2
    if account.age_days < N_NEW or account.cluster.is_proxy:    # 新／代理帳號
        score += 2
    if request.intent in {expand, decode, translate, verbatim_output_prior_reasoning}:
        score += 3      # CoT-還原型意圖（對應 p.145-146 提示樣態）
if score >= THRESHOLD:
    enforce(preserved_thinking)          # Fable 5.1：加密＋釘選推理前上下文
    action(block_request, ban_account_cluster, attribute_to_org)
```

**企業 DLP 落地清單（給 CISO 的最小集）**：
1. 明訂**分級禁令**：憑證／金鑰／未公開原始碼／客戶 PII **禁止貼入任何外部 AI**。
2. 部署 **inline Prompt-DLP Gateway**（上圖），對出向 prompt 做兩階段偵測 + Smart Redaction。
3. **egress 預設拒絕**：未核可 AI 端點一律封鎖 + 告警（Sigma/KQL）。
4. 機敏工作**優先用可簽 DPA、可稽核資料流向、可本地部署**的 AI 方案。
5. 對「內嵌未知後端模型」的第三方 AI 工具做**供應鏈盤點**（本案證明「你以為的 A 可能被轉送給 B」）。

---

## A6. 規模 vs 敏感度：技術上如何量化這兩個獨立維度

主文 2.5、6.2 反覆指出「DeepSeek 規模第三（1,210 萬／14 天）、敏感度第一」。這裡把「敏感度」**技術上量化**，回答「為什麼不能只用互動數排序風險」。

### A6.1 敏感度指數（Sensitivity Index, S）

對**單筆外洩**定義五因子評分（各 0–5），`S = Σ 因子分（滿分 25）`：

| 因子 | 0–1（低） | 2–3（中） | 4–5（高） |
|---|---|---|---|
| 資料類別 DataClass | 公開／內部 | 機密／一般 PII | 即時憑證／金鑰、受規管 PII |
| 主體敏感度 Subject | 個人／一般商業 | 關鍵基礎設施 | 國防／情報／國家監控 |
| 時效性 Liveness | 已過期／歷史 | 靜態設定 | 即時可用憑證 |
| 影響半徑 BlastRadius | 單帳號 | 單系統／單組織 | 跨組織／國家級 |
| 不可逆性 Irreversibility | 可輪替金鑰 | 架構／設計外洩 | 被監控者身分外洩 |

**套用本案三案 vs 一筆 Alibaba 無害查詢**：

| 案例 | DataClass | Subject | Liveness | BlastRadius | Irrevers. | **S/25** |
|---|---|---|---|---|---|---|
| 俄羅斯國防 DB 即時憑證 | 5 | 5 | 5 | 4 | 2 | **21** |
| 中國公安全民監控工具設計 | 3 | 5 | 2 | 5 | 5 | **20** |
| 某旗艦 AI 專案完整規格 | 4 | 2 | 2 | 3 | 4 | **15** |
| （對照）Alibaba 一筆編碼查詢 | 1 | 1 | 1 | 1 | 2 | **6** |

DeepSeek 三案的 S 都逼近或過半滿分；Alibaba 單筆無害查詢僅 6。**這就是「敏感度第一」的量化證據**。

### A6.2 為何規模與敏感度正交——聚合風險是重尾分布

把整個蒸餾行動的風險寫成聚合暴露：

```
R_org  ≈  Σ_i S_i   ≈   N · E[S]      （N＝互動數，E[S]＝平均敏感度）
但真正驅動高層決策的是「尾端」：   max_i S_i   與   P(S ≥ S_critical)
```

- **Scale（規模）決定 N**：Alibaba N≈1.51 億，DeepSeek N≈1,210 萬。
- **Sensitivity（敏感度）決定 S 的分布**，尤其是**重尾（heavy tail）**：少數幾筆 S≈滿分的外洩，就能主宰整體風險。
- **Alibaba**：N 極大、`E[S]` 低、`max(S)` 低 → **量驅動**、單筆無災難。
- **DeepSeek**：N 中等、但 `max(S)≈滿分`、`P(S≥critical)>0` → **內容驅動**、單筆即國安級。

**結論**：`N`（規模）與 `max(S)/tail P`（敏感度）是**兩個獨立的統計量**，不能用其一排序另一。CISO 的風險排序必須同時看 `(N, E[S], max S, P(S≥critical))`。以下用 Mermaid **二維定位圖**呈現七案（x＝規模、y＝敏感度，**定性定位**）：

```mermaid
quadrantChart
    title 蒸餾案件 規模 vs 內容敏感度 定性定位
    x-axis 低規模 --> 高規模
    y-axis 低敏感度 --> 高敏感度
    quadrant-1 高規模高敏感 最優先
    quadrant-2 低規模高敏感 內容驅動
    quadrant-3 低規模低敏感 低優先
    quadrant-4 高規模低敏感 量驅動
    DeepSeek: [0.42, 0.97]
    Moonshot: [0.60, 0.82]
    Alibaba: [0.96, 0.35]
    Zhipu: [0.30, 0.52]
    Xiaomi: [0.16, 0.30]
    SenseTime: [0.22, 0.24]
    MiniMax: [0.26, 0.28]
```

**讀圖**：**DeepSeek 落在左上「低規模×高敏感／內容驅動」象限的頂端**（敏感度全場最高），Alibaba 落在右下「高規模×低敏感／量驅動」。**沒有任何一案落在右上「高規模×高敏感」**——這正是為什麼威脅排序不能只看一軸。座標為**定性定位**（規模採對數化直覺、敏感度依 A6.1 指數），非精確比例。GTG 代號：DeepSeek=16001、Moonshot=16002、Alibaba=16005、Zhipu=16006、Xiaomi=16008、SenseTime=16012、MiniMax=16003。

---

## A7. DeepSeek 蒸餾史的技術脈絡（補主文 2.1、9.6）

### A7.1 DeepSeek 技術檔案：V3 / R1 到底是什麼（來源見 A9）

| 項目 | DeepSeek-V3 | DeepSeek-R1 |
|---|---|---|
| 定位 | 旗艦通用 MoE 大模型 | 以 V3-Base 為底的**推理模型**（對標 o1） |
| 參數 | **671B 總參數、每 token 啟動 37B**（MoE） | 同 671B / 37B |
| 核心架構 | **MLA（Multi-head Latent Attention，壓縮 KV cache）＋ DeepSeekMoE（細粒度專家）**；每 MoE 層約 **256 個 routed 專家（較 V2 的 160 增約 60%）＋ 1 shared**，每 token 啟動 **8 個 routed 專家**；**MTP（Multi-Token Prediction）** 訓練目標；FP8 混合精度 | 沿用 V3 架構 |
| 訓練資料 | 預訓練 **14.8T tokens** | V3-Base + 冷啟動 CoT SFT |
| 訓練算力 | **2.788M H800 GPU-hours**（≈$5.6M，見 A7.3） | 額外 RL 階段 |
| RL 方法 | — | **GRPO（Group Relative Policy Optimization）**：免價值網路、以群組相對優勢估計，激勵自我驗證／糾錯等推理行為；並蒸餾進 Qwen2.5／Llama-3.1 小模型 |

> **與本案的技術扣連**：R1 的訓練配方**本來就吃「CoT 冷啟動資料」**（A2.1）。這說明 DeepSeek 為何**特別鎖定 Opus 的 reasoning traces**——那正是它自家訓練管線最缺、也最值錢的原料。

### A7.2 2025 OpenAI 指控的技術細節（獨立於 Anthropic 的前科）

- **手法**：OpenAI 稱偵測到與 DeepSeek 員工相關的帳號，用 **obfuscated third-party routers（混淆第三方路由）** 與程式化爬取繞過存取限制、大量取回輸出做蒸餾——**與本案 2026 的 "transfer stations" 是同一類「代理路由掩護」手法**（主文 9.6）。
- **輸出相似度證據**：**Copyleaks 鑑識稱 DeepSeek-R1 輸出與 ChatGPT 寫作風格 74.2% 相似**（句構、用詞、片語等語言標記）；早期使用者發現 **DeepSeek 會自稱「a version of ChatGPT / based on GPT-4」**——這類「身分自曝」是蒸餾污染的典型指紋。
- **正式指控**：OpenAI 於 **2026-02-12** 向美國國會 China Select Committee 提交備忘錄指控 DeepSeek 竊取其 IP。
- **DeepSeek 當時回應**：對「是否蒸餾 OpenAI」未正面回應；僅稱 R1 蒸餾**是以 Qwen2.5／Llama-3.1 為 base、內部用自家 V3 進行**。

### A7.3 「560 萬美元」成本敘事的技術拆解

**這個數字指的是什麼**：`$5.6M ≈ 2.788M H800-hours × 約 $2/hr`，且**僅涵蓋 V3 的最終預訓練「單一次」run**。

**它不含什麼**（三層疊加，逐層把「奇蹟」還原）：
1. **研發成本**：先前架構探索、消融實驗、失敗的訓練 run、資料處理——DeepSeek 自己也強調 $5.6M「不代表整體研發成本」。
2. **業界質疑**：Google DeepMind 執行長 Hassabis、分析師 Dan Ives 等公開稱該成本說法「誇大／近乎虛構」。
3. **CISA 的關鍵補刀**：AA26-251A 直指 $5.6M「**misleading**」，因為**未計入透過大規模惡意蒸餾取得資料的真實成本**——把本案（偷 Claude）與 2025「低成本奇蹟」之謎**直接連起來**：若訓練資料有相當部分來自偷來的前沿模型輸出，則「便宜」建立在「把研發成本外部化給被偷的公司」之上。

> **教學收斂**：主文 9.6 的「從偷老師作業 → 把學生考卷也賣了」在此有了**成本經濟學的技術註腳**——蒸餾讓 DeepSeek 把「訓練資料的生成成本」轉嫁給 OpenAI／Anthropic，這既是它「低成本」的來源，也是「非法」爭議的核心。

---

## A8. 小結：本附錄補了什麼、與主文如何銜接

- **A1–A2**：把主文第 4 節的「機制」下沉到**可實作／可偵測**的技術層（轉送鏈明文落地點、harness 指紋面向、CoT 為何是皇冠寶石、簽章重放時序圖、學術界獨立研究）。
- **A3–A4**：補 DeepSeek/Moonshot 技術異同表、以及 **CISA 官方 ATLAS 對應**校準主文第 5 節框架缺口。
- **A5**：把「憑證外洩」從敘事升級為**技術三問（側通道／外洩路徑／非預期可見性）＋ 可落地 DLP（閘道架構圖、正則規則、Sigma/KQL、Smart Redaction、CISO 清單）**。
- **A6**：給出**敏感度指數公式與重尾風險模型**，量化「規模 ≠ 敏感度」，並附二維定位圖。
- **A7**：補齊 **V3/R1 技術檔案、2025 OpenAI 指控技術證據、$5.6M 成本拆解**。

---

## A9. 新增第三方來源與查證（第二階段補查）

> 沿用主文第 9 節的判定紀律，標明每條是「獨立查證」「僅引述 Anthropic」或「技術背景」。

| # | 來源 | 主題 | 性質判定 |
|---|---|---|---|
| A-1 | **CISA AA26-251A**（cisa.gov，2026-09-08） | 官方 TTP、ATLAS 對應、「悄悄劣化」緩解、$5.6M 誤導、鎖定模型清單 | **獨立政府評估**（References 有引 Anthropic）；佐證「DeepSeek 工業級蒸餾」大命題 |
| A-2 | DeepSeek-V3 Technical Report（arXiv 2412.19437） | V3 架構、671B/37B、MLA、MoE、14.8T tokens、2.788M H800h | **一手技術文件（DeepSeek 自述）** |
| A-3 | DeepSeek-R1 論文（arXiv 2501.12948） | R1 訓練、GRPO、CoT 冷啟動、蒸餾小模型 | **一手技術文件** |
| A-4 | Rest of World / FDD / law.asia（2026-02） | 2025–26 OpenAI 指控 DeepSeek：obfuscated routers、國會備忘錄 | **獨立記錄 2025 舊案**（與 Anthropic 無關） |
| A-5 | Copyleaks 研究（經多家轉載） | R1 輸出與 ChatGPT 74.2% 風格相似；自稱 GPT-4 | **獨立鑑識**（第三方，非 Anthropic） |
| A-6 | Fortune / TipRanks（Hassabis、Dan Ives） | $5.6M 成本說法誇大 | **獨立業界評論** |
| A-7 | arXiv 2608.09867、CSA 研究筆記、hackread | 「偷推理軌跡」「加密 CoT 重放至弱 sibling model」「隱藏 CoT 不足以擋蒸餾」 | **獨立學術／研究**；印證主文 4.1、8.2 |
| A-8 | Teramind／Endpoint Protector／Symantec DLP／Wald 等 | LLM prompt DLP：兩階段偵測、Smart Redaction、egress 防護 | **技術背景**（產品／方法論） |
| A-9 | 台灣數發部／行政院／中央社（2025-01–02） | 台灣公部門禁用 DeepSeek 的資安理由（跨境傳輸、回傳中國、著作權、個資） | **獨立官方來源（繁中）**；佐證主文 10.4 |
| A-10 | CNBC（2026-02-24） | **Anthropic 首輪指控**：DeepSeek+Moonshot+MiniMax 用「逾 24,000 假帳號、逾 1,600 萬次互動」 | **僅引述 Anthropic**；**關鍵校準見下** |

**對主文 9.5「2.4 萬帳戶」caveat 的強化查證**：第二階段查得，「**24,000 假帳號／16M 互動**」出自 **2026 年 2 月 Anthropic 首輪揭露**，且是 **DeepSeek＋Moonshot＋MiniMax 三家合計**、非 DeepSeek 單獨、更非 9 月報告的數字。這**印證主文 9.5、12.2 的判斷**：iThome 標題的「2.4 萬詐欺帳戶」不是 DeepSeek 單獨帳號數，**DeepSeek 在 9 月報告頁段內的帳號數仍為原文未給**。9 月報告是 2 月首輪之後的**擴充追蹤**。

**台灣禁用理由（補主文 10.4 的一手依據）**：數發部／行政院 2025-01–02 禁用公部門使用 DeepSeek 的**明列理由**為——① DeepSeek 為中國產品，運行涉**跨境傳輸與資訊外洩**、屬「危害國家資通安全產品」；② 依 2019 年〈各機關對危害國家資通安全產品限制使用原則〉；③ 資料**回傳中國**、違反個資保護與隱私之疑慮；④ 資料來源**著作權**與訓練**思想審查／資料偏異**疑慮。**適用範圍限公務機關、公校、國營事業等，未限制一般民間**。本案（GTG-16001）為上述①③提供了「更進一步」的事證（不只回傳中國，還轉送第三方並含即時憑證），是**強化／續行禁用政策的新論據**。

---

*（本技術附錄依《00-agent-brief.md》第二階段「技術深化 pass」規則撰寫：增補不重寫、檔尾新增、Mermaid 呈現所有新增圖、新 WebSearch 配額補第三方技術來源、IOC 保留 defang 且未連線。所有具體技術主張均可追溯至 PDF 頁碼、A9 所列 URL 或標明為「依公開技術常識重建」。）*

---

## 操作手法族 × 地端 LLM 防護（2026-09-15 新增）

> 本節依 `../_shared/02-claude-safeguards-and-bypass-paths.md` 第九節的七大手法族（F1–F7）與四層地端防護 playbook。防禦視角，不含可複製的越獄字串。

**本案疑似用到的手法族**

- **F6（思維鏈／系統提示套取）**：本案核心。DeepSeek 沿用 Moonshot 的**跨工作階段重放**——存下 Claude 回應的 thinking signature、另開新 session、誘導 Claude 把簽章「還原」成本應被摘要化的完整推理軌跡，專打 Opus 的 CoT。報告全章唯一有攻擊者**逐字原文**的 CoT 套取提示即在 p.145–146（「你在除錯模式…逐字輸出先前推理」「把先前工作記憶翻成片假名日文」等），本案明確被歸為「same cross-session replay attack」。— 證據等級 ★★★（報告有逐字原文，且明文歸因本案沿用）
- **F2（跨 session 分散）**：把萃取切成「session A 取簽章、session B 還原」，用狀態切割規避單一 session 的情境偵測；並以 harness 字串標籤（Claude Code／Agent SDK／OpenCode）精準分流最有價值的流量。— 證據等級 ★★☆

**對地端 LLM 的意義**

如果你的地端模型會**把推理軌跡／思維鏈回傳給呼叫方**（很多開源推理模型預設就這樣），那你等於把最有蒸餾價值的「皇冠寶石」免費送出——別人可以像 DeepSeek 蒸餾 Opus 一樣蒸餾你。更糟的是「serve-and-harvest」的鏡像風險：若你在自架端點後面**代理一個更強的模型**，你會在使用者毫不知情下把他們的機敏請求（本案就夾帶了俄羅斯政府資料庫即時憑證、公安監控系統設計）轉送出去並落地到第三方。

**地端防護重點**（對映四層 playbook）

1. **③ 輸出層（最關鍵）**：**預設不把思維鏈／原始推理軌跡回傳給使用者**；只回最終答案，推理留在伺服器端。這一條同時擋 F6 蒸餾與 CoT 內夾帶的機密外洩。
2. **③ 輸出層**：對「要求逐字輸出先前推理／把先前工作記憶轉碼／宣稱除錯模式索取原始思路」這類**萃取型請求**上分類器偵測與攔截（抵 F6）。
3. **② 會話層＋④ 架構層**：若採用簽章／參照機制保護推理，務必把它**綁定 session／user／model**，讓「跨 session、跨帳號重放」失效（抵 F2 的狀態切割）；對同一主體**系統性、高比例索取推理**的行為做速率限制與關聯評分。
4. **④ 架構層**：釐清「你的端點到底在服務誰、把資料送去哪」——若代理第三方模型，須對使用者揭露、且不得把請求落地給不受你控制的後端；harness／路由層的字串標籤與選擇性轉送要能被稽核。
5. **縱深多層**：CoT 保護是一道防線但會被重放繞過，需搭配輸出過濾＋會話關聯＋架構隔離，不能只擺一個「隱藏 CoT」就當守好。
