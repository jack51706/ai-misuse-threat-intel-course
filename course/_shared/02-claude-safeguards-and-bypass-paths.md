# 專題：Claude 的安全柵欄很嚴格，為什麼 GTG 還是繞過了？

> 用途：回答課程最常被問的問題——「Claude 的道德柵欄不是很嚴嗎？為什麼這份報告裡有這麼多成功濫用？」
> 這份專題橫跨全部八個模組，是理解整份報告的關鍵框架。建議排在課程第一天，緊接網路行動導論之後。

---

## 一、先破除一個誤解：多數 GTG 不是「越獄」破了柵欄

直覺會以為：報告裡每個 GTG 都是「找到咒語騙過 Claude」。**這是錯的。** 真正靠「內容層越獄」硬破柵欄的案例是少數。絕大多數成功濫用走的是**柵欄根本沒守到、或設計上不守**的路徑。

要精確回答「柵欄嚴不嚴」，必須先把「柵欄」拆成三層，它們各自的強度與盲區不同：

```mermaid
flowchart TB
    subgraph L1["第 1 層：存取層（你是誰、用哪個模型）"]
        A1["帳號驗證 / 支援地區限制"]
        A2["模型分級（Fable/Mythos 柵欄最嚴）"]
    end
    subgraph L2["第 2 層：內容層（這個請求說了什麼）"]
        B1["安全訓練（模型自身拒絕）"]
        B2["分類器（偵測高風險內容）"]
    end
    subgraph L3["第 3 層：執行後（產出離開平台之後）"]
        C1["帳號封鎖 / 事後調查"]
    end
    L1 --> L2 --> L3
    style L1 fill:#e8f0ff
    style L2 fill:#fff0e8
    style L3 fill:#f0e8ff
```

報告揭露的五條規避路徑，正好對應「打穿或繞過」這三層的不同方式。理解這五條路徑，就理解了整份報告。

---

## 二、柵欄「確實嚴格」的證據：報告裡 Claude 拒絕的實例

在談規避之前，先確立一個事實：**柵欄不是紙糊的。** 報告本身充滿 Claude 拒絕、分類器攔截、能力被限制的實例。這些是攻擊者「必須費力規避」的原因——如果柵欄無效，他們根本不需要那些規避手法。

| 模組 / 案例 | 柵欄發揮作用的實例（報告原文依據） |
|---|---|
| 影響力 GTG-04001 | Claude 拒絕「點名真實個人為武裝分子、以招來安全打擊」的最激進請求 |
| 影響力 GTG-84005 | Claude 辨識出某文件屬政治誹謗材料後拒絕 |
| 監控 GTG-14010 | Claude 拒絕若干秘密審訊與大規模假人設請求 |
| 監控 GTG-14021 | 公安偵查員的請求**先被 Claude 拒絕**（之後才靠重新提示突破） |
| 監控 GTG-30006 | Claude「十次拒絕九次」（nine out of ten） |
| 監控 GTG-34007 | Claude 拒絕了明確的側寫與宣傳請求 |
| 生物 Case 1 | 生物安全分類器攔下補助申請並啟動威脅調查 |
| 生物 Case 2 | 分類器把高風險互動限制在能力最弱的模型 |
| 蒸餾（全章） | 隨 Fable 5 上線強化 extraction 分類器；Fable 網路防護擋住 Zhipu 的網路能力蒸餾 |
| 常規武器（全章） | Anthropic 新增分類器偵測並封鎖武器開發請求 |

**教學重點**：報告是一份「防線與規避的對抗史」，不是「柵欄失效史」。攻擊者投入大量資源去規避，本身就證明柵欄提高了成本。

---

## 三、五條規避路徑（逐條拆解）

### 路徑 A：存取層規避——根本沒碰到內容柵欄

這是**最常見**的路徑，也最容易被忽略。攻擊者不去「騙過」Claude，而是讓自己看起來像正當使用者，或根本不透過正規管道。

- **手法**：假帳號 / 合成身分、灰市轉售商（gray market resellers）、ZDR（Zero Data Retention）夥伴平台隱藏內容、境外 VPS 偽裝來源規避支援地區限制、竊來的 API 金鑰與 session token。
- **案例**：生物 Case 1（軍方機構研究者透過 ZDR 轉售平台 + 美國 VPS）、生物 Case 2/3（不支援地區 + 中繼帳號）、蒸餾全章（3,500+ 假帳號、空殼公司 proxy）、GTG-50021 與 GTG-50020（竊來的金鑰）。
- **為什麼有效**：內容柵欄再嚴，也要先「看到」請求才能判斷。存取層規避讓請求以正當面貌進入，或分散到大量拋棄式身分，稀釋風險評分。
- **關鍵洞察**：這條路徑打的是**第 1 層（存取層），繞過了第 2 層（內容層）**。報告的解方「可信任使用者審核制」正是要補強這一層。

### 路徑 B：內容層繞過——騙過模型自身的拒絕

這才是一般人以為的「越獄」，但它只是五條路徑之一。

- **手法**：重新提示（拒絕後換說法再問）、角色扮演（如 GTG-1002 假扮「合法資安公司做滲透測試」）、任務拆分（把惡意任務切成無害子任務、分散到不同 session）、良性框架（把請求包裝成防禦性/治療性目的）。
- **案例**：GTG-14021（拒絕後重新提示取得對 10 名公民的「控制」建議）、GTG-30006（拆分到後續小 session 繞過）、生物 Case 3（聚焦「減毒」的良性框架使分類器放行）。
- **為什麼有效**：安全訓練與分類器判斷的是「單一請求的內容看起來像什麼」。跨 session 拆分打散了惡意訊號；良性框架讓內容落在「看似正當」的一側。
- **關鍵洞察**：這條路徑打**第 2 層**，暴露了「用內容判斷意圖」的原理性上限——在雙重用途領域，善意與惡意的文字可能一模一樣。

### 路徑 C：柵欄設計上不涵蓋——範圍留白

- **手法**：利用柵欄「刻意不管」的範圍。生物分類器設計上針對「讓新手取得已知生物武器」，不涵蓋專業人員的新化合物研究；ATT&CK 沒有 agentic orchestration 的技術 ID。
- **案例**：生物 Case 4-5（毒液毒素研究，報告明說「largely unimpeded... This was by design」）、大量監控案（「側寫異議者」被拒，但「寫個收集資料的工具」被放行，因為工具開發看似中性）。
- **為什麼有效**：這不是柵欄失靈，是範圍界定的必然取捨——涵蓋太廣會癱瘓大量正當使用。
- **關鍵洞察**：這條路徑不打任何一層，而是走在**層與層之間的縫隙**。

### 路徑 D：模型選擇——避開柵欄最嚴的模型

**這條路徑直接回答「柵欄不是很嚴嗎」——因為最嚴的柵欄，攻擊者根本不去碰。**

- **報告原文**（Overview）：「None of the misuse cases involved the use of Claude Fable or Mythos-class models, with the exception of one illicit distillation case.」（除一起蒸餾案外，所有濫用都未涉及 Fable 或 Mythos 級模型。）
- **報告原文**（網路章）：「no malicious activity was found on Claude Fable or Mythos (which has a series of safeguards in place that greatly reduce its ability to perform harmful cyber tasks)」。
- **意義**：Fable / Mythos 是柵欄最嚴的模型，嚴到**幾乎沒有成功濫用**。被濫用的幾乎全是較舊的 Haiku / Sonnet / Opus。生物 Case 2 更直接——分類器主動把高風險互動**降載到最弱的模型**（Sonnet 4 / Haiku 4.5），使實質能力提升被壓到文書層次。
- **關鍵洞察**：所以「柵欄嚴不嚴」的答案是**分層的**：最新最強模型的柵欄嚴到攻擊者放棄；他們退而求其次用較弱模型，或用蒸餾去「偷」強模型的能力來訓練沒有柵欄的自己的模型（這就是為什麼蒸餾是唯一碰到 Fable/Mythos 的領域——偷能力，不是用它作惡）。

### 路徑 E：部署後不可收回——柵欄管不到已交付的東西

- **手法**：一旦 Claude 產出了程式碼或知識，攻擊者把它部署到本地模型、離線工具鏈，斷開 API 也阻止不了。
- **案例**：GTG-50027（馬利監控系統以本地模型運行，封號無法終止已部署系統）、GTG-87001（離線模擬工具不依賴 Claude）、生物 Case 1（operator 封號數天內重建存取）。
- **為什麼有效**：柵欄是「服務層」的控制，管的是「透過 API 的即時請求」。知識與程式碼一旦離開平台就脫離管轄。
- **關鍵洞察**：這條路徑打**第 3 層之外**——這是 API 管制的根本極限，也是開源與地端模型成為治理難題的原因。

---

## 四、一個惡意行為者如何「找路」（決策樹）

把五條路徑合起來，可以還原攻擊者面對柵欄時的實際決策：

```mermaid
flowchart TD
    START["想用 AI 做有害任務"] --> Q1{"用最強模型<br/>Fable/Mythos?"}
    Q1 -->|"柵欄太嚴，放棄"| PATHD["路徑 D：改用較弱模型<br/>Haiku/Sonnet/Opus"]
    Q1 -->|"或乾脆偷能力"| DISTILL["蒸餾：偷 CoT 訓練<br/>自己沒柵欄的模型"]
    PATHD --> Q2{"我的身分/管道<br/>會被擋嗎?"}
    Q2 -->|"會"| PATHA["路徑 A：假帳號 / 轉售商<br/>/ ZDR / 境外 VPS / 偷金鑰"]
    Q2 -->|"不會"| Q3{"請求內容<br/>會被拒絕嗎?"}
    PATHA --> Q3
    Q3 -->|"會被拒"| PATHB["路徑 B：重新提示 /<br/>角色扮演 / 拆分 / 良性框架"]
    Q3 -->|"落在灰區"| PATHC["路徑 C：用柵欄設計上<br/>不涵蓋的雙重用途/工具請求"]
    PATHB --> DEPLOY
    PATHC --> DEPLOY
    DISTILL --> DEPLOY["取得產出"]
    DEPLOY --> PATHE["路徑 E：部署到本地/離線<br/>封號也收不回"]
    style PATHA fill:#ffe8e8
    style PATHB fill:#ffe8e8
    style PATHC fill:#fff0d0
    style PATHD fill:#e8e8ff
    style PATHE fill:#e8ffe8
    style DISTILL fill:#f0d0f0
```

---

## 五、對防守方與 AI 治理的意涵

1. **不要把「柵欄」當單一物**：它是存取層、內容層、執行後三層。多數濫用打的是存取層與縫隙，不是內容層越獄。強化內容柵欄（大家最愛談的「對齊」）對路徑 A、C、D、E 幾乎無效。
2. **內容柵欄有原理性上限**：路徑 B、C 證明「用內容判斷意圖」在雙重用途領域不可能完美。這是為什麼報告反覆推「可信任使用者審核制」——把判斷從內容移到身分。
3. **模型分級是有效的**：路徑 D 顯示最強模型的嚴柵欄確實把攻擊者擋到「寧可用弱模型或偷能力」。這支持「能力越強、柵欄越嚴」的分級部署策略。
4. **API 管制有邊界**：路徑 E 是開源與地端部署治理難題的核心——這也是常規武器模組 ASL 討論與蒸餾模組的交集。
5. **對台灣的意涵**：台灣若自建或使用 AI 模型，這五條路徑就是威脅模型的骨架。特別是路徑 A（採購稽核、身分驗證）與路徑 D/E（使用防護較弱的開源模型從事敏感工作的風險），是台灣 AI 治理最該補的兩塊。

---

## 六、課堂設計

### 6.1 核心教學要點
- 「柵欄嚴不嚴」的正確答案是分層的：最強模型嚴到沒被成功濫用，弱模型與規避管道才是缺口。
- 五條規避路徑中，只有一條（路徑 B）是一般人以為的「越獄」。
- 攻擊者投入資源規避，本身證明柵欄有效。

### 6.2 課堂討論題
1. 如果內容柵欄有原理性上限，AI 公司把資源投在「更強的內容對齊」還是「更嚴的使用者審核」？兩者的代價各是什麼？
2. 路徑 D 顯示濫用集中在弱模型。那麼「把舊模型下架」是好的安全策略，還是會把需求推向更沒柵欄的開源模型（連結生物 Case 2 的外溢效應）？
3. 蒸餾（偷強模型能力訓練沒柵欄的自己模型）是否讓「模型分級柵欄」的長期效果歸零？

### 6.3 桌面演練
給學員數個匿名化的請求序列，讓他們判斷該行為者走的是哪一條規避路徑，以及 AI 公司該在哪一層攔截。用第四節的決策樹作為判斷框架。

---

## 七、關鍵原文引文

1. 最強模型幾乎未被濫用（Overview）：
   「None of the misuse cases involved the use of Claude Fable or Mythos-class models, with the exception of one illicit distillation case.」
2. Fable/Mythos 的網路柵欄（網路章）：
   「no malicious activity was found on Claude Fable or Mythos (which has a series of safeguards in place that greatly reduce its ability to perform harmful cyber tasks)」
3. 內容柵欄的原理性上限（生物章 p.137）：
   「since it is not possible to reliably identify the intent of the user in highly technical dual-use areas, a classifier cannot simultaneously enable benefit and prevent harm.」
4. 老練者隱藏意圖（生物章 p.131）：
   「Overt malicious intent is, therefore, often evidence that a particular actor is not all that sophisticated... More sophisticated actors can hide their intent, extracting assistance from an AI model in interactions that look plausibly beneficial.」

---

## 八、與其他教材的連結

- 防線失效的四種**技術**模式（重新提示、跨 session 拆分、工具中性、部署不可收回）見 `01-cross-cutting-analysis.md` 主線三——那份談「偵測工程」角度，這份談「柵欄架構」角度，兩者互補。
- 路徑 C（設計上不涵蓋）的最完整案例在 `05-bio/case4-5-venoms-toxins-out-of-scope.md` 的「分類器四種狀態」。
- 路徑 D/E 與 ASL 分級的關係見 `04-weapons/00-weapons-intro-and-safeguards.md` 與 `08-capability-research/02-weapons-dev-evals-and-policy.md`。
- 蒸餾作為「偷能力繞過模型分級」見 `07-distillation/00-distillation-intro-and-mitigations.md`。


---

## 九、路徑 B 展開：七大提示操作手法族 × 地端 LLM 防護（2026-09-15 新增）

> **這一節是什麼**：前面第三節把規避拆成五條路徑，其中「路徑 B（內容層繞過）」是一般人以為的「越獄」。本節把路徑 B 再展開成**七個可辨識的提示操作手法族（F1–F7）**，並回答學員最實際的需求——**「如果我自己在地端／內網跑一個開源 LLM，這些手法會怎麼打我、我要怎麼守？」** 各 GTG 案例教材末尾都新增一節「推測操作手法 × 地端 LLM 防護」，逐案標明它用到哪幾個 F 族、以及本案專屬的偵測與防護；本節是那 37 節共用的字彙表與總防護 playbook。
>
> **紅線（務必先讀）**：本節與各案的對應段落，講的是**手法的「樣態、為何有效、如何偵測與防護」**，**不提供可複製貼上的越獄字串**。報告本身只有極少數地方引用攻擊者的真實提示詞（最明確的是蒸餾章 p.145–146 那組套取思維鏈的原文）；其餘一律標為**推測的手法樣態**（證據等級 ★☆☆），不是宣稱報告逐字記載。這是給防守方（藍隊）的 playbook，不是攻擊工具。

### 9.1 為什麼「地端 LLM」特別需要這一課

報告的一條主線是：**前沿模型的防護把濫用者逼向較弱、防護較少的模型**（生物 Case 2、路徑 D）。而「較弱、防護較少的模型」在真實世界，最大宗就是**學員自己會下載自架的開源權重模型**。關鍵推論：

- 商用 Claude 有存取驗證、內容分類器、行為監控、模型分級這些**內建防線**；**自架的開源 LLM 幾乎全部沒有**——你拿到的是裸模型。
- 也就是說，**這份報告裡打 Claude 的七大手法，原封不動可以打你的地端 LLM，而且你沒有 Anthropic 那幾層網子接著**。防線要**你自己一層一層搭**。
- 且 2026 年的共識是：**單一 guardrail 會被繞過**（實測對六款防護的規避成功率可達 100%），所以地端防護必須是**縱深多層**，不能只擺一個分類器就當守好了。

### 9.2 七大手法族 × 對應 GTG × 地端防護對照表

| 代號 | 操作手法族 | 怎麼操作模型的推論 | 報告中疑似用到的 GTG（證據等級） | 地端 LLM 防護重點 |
|---|---|---|---|---|
| **F1** | 人設＋授權框定 | 宣稱自己是合法資安人員／做「授權滲透測試」，把請求推到「可協助」的一側 | GTG-10007、(2025-11 的 GTG-1002 有原文) ★★☆ | 雙重用途能力**不要靠 prompt 內宣稱的身分**放行；改用**帳號外的已驗證授權**（CVP 式）＋**行為規模**判斷（同一主體大量雙重用途請求） |
| **F2** | 任務拆解＋跨 session 分散 | 把一個大惡意切成無數個「單看無害」的子任務，分散到不同對話／子代理 | GTG-14021、GTG-30006、GTG-10007（swarm）★★☆ | **跨請求／跨 session 意圖聚合**；別只用「單一請求分類」；對同一使用者的請求做關聯與累計風險評分 |
| **F3** | 拒絕後重新提示（Crescendo） | 被拒後換個說法、逐步升溫再問，直到通過 | GTG-14021、GTG-14020 ★★☆ | 記錄「拒絕→改寫→順從」序列；**一旦拒絕就對後續同主題請求提高審查**（黏性拒絕狀態），而非每次從零判斷 |
| **F4** | 良性／防禦性改框 | 把同一份雙重用途知識包裝成治療性、防禦性、「減毒」等看似正當的框架 | 生物 Case 3（attenuation 原文）、GTG-34007（防禦工具框架）、GTG-14010（工具中性）★★☆ | **判斷用途與下游，不判斷表面框架**；在雙重用途領域做**能力降載**而非全有全無；輸出端獨立再判 |
| **F5** | 工具／記憶中介 | 用工具伺服器、agent swarm、持久記憶檔，把「真正的目標與意圖」從任何單一請求前移走 | GTG-10007、GTG-84002、GTG-50027、GTG-14021（SKILL.md）★★☆ | 對**你自己的代理**：工具最小權限、**淨化工具回傳內容**（防間接注入）、持久記憶不得夾帶未審指令、監控工具呼叫節律 |
| **F6** | 思維鏈／系統提示套取 | 用「你在除錯模式」「這才是真正的系統提示」等話術，誘出模型的推理過程或系統提示 | 蒸餾各案（**報告 p.145–146 有逐字原文** ★★★） | **不要把思維鏈／推理軌跡回傳給使用者**；保護系統提示；上萃取偵測；對系統性索取推理的行為做速率限制與偵測 |
| **F7** | 輸出格式操縱 | 要求「低擬真度」模糊化、拿掉 caveats、套固定模板，把有害內容洗白或規避輸出過濾 | 生物 Case 5（low-fidelity 原文）、GTG-14022（強制對抗性分析段）、GTG-04001（去 caveat）★★☆ | **輸出端分類器獨立於使用者要求的格式**；偵測「要求降低擬真度／移除警語／強制敵我模板」這類請求 |

> 讀法：★★★＝報告有逐字原文；★★☆＝報告描述了行為、手法屬合理重建；★☆☆＝純推測。各案末節會標出該案落在哪一級。

### 9.3 地端 LLM 縱深防護 playbook（給藍隊）

把七族的防護收斂成**四層縱深**，對照可直接評估的開源工具：

```mermaid
flowchart TB
    subgraph IN["① 輸入層"]
      I1["越獄／注入分類器<br/>Llama Prompt Guard 2 · Rebuff · LlamaFirewall"]
      I2["系統提示強化＋指令階層<br/>抵 F1/F3/F6"]
      I3["工具回傳內容淨化／隔離<br/>抵 F5 間接注入"]
    end
    subgraph SESS["② 會話層"]
      S1["跨 session／跨請求意圖聚合<br/>抵 F2"]
      S2["拒絕狀態追蹤（黏性）<br/>抵 F3"]
    end
    subgraph OUT["③ 輸出層"]
      O1["輸出分類器（獨立於請求格式）<br/>抵 F4/F7"]
      O2["能力降載（雙重用途域）<br/>不回傳思維鏈 抵 F6"]
    end
    subgraph ARCH["④ 架構層"]
      A1["工具最小權限＋機密不入上下文"]
      A2["身分／授權閘（雙重用途）<br/>行為與稽核日誌"]
      A3["最強模型不裸奔<br/>縱深多層 不靠單一 guardrail"]
    end
    IN --> SESS --> OUT --> ARCH
    style IN fill:#e8f0ff
    style SESS fill:#fff0e8
    style OUT fill:#f0ffe8
    style ARCH fill:#f0e8ff
```

- **① 輸入層**：上游擋掉明顯的注入／越獄。開源可用 **Meta Llama Prompt Guard 2**（輕量注入／越獄分類器）、**LlamaFirewall**（PromptGuard 2 ＋ 代理對齊檢查 ＋ CodeShield）、**Rebuff**（heuristics＋LLM＋canary token 的自我強化偵測）、**NVIDIA NeMo Guardrails**（可程式化護欄）。搭配**系統提示強化與指令階層**（讓系統指令優先於使用者輸入）。
- **② 會話層**：F2、F3 的關鍵——**不要每個請求都從零判斷**。做跨 session 關聯與拒絕狀態追蹤，把「被拆散的惡意」重新縫起來。
- **③ 輸出層**：**輸出要獨立再判一次**，不因使用者指定的格式而放行（抵 F4/F7）；雙重用途域用**降載**（給弱能力）而非全有全無；**不要把思維鏈回傳給使用者**（抵 F6，也直接壓制蒸餾）。
- **④ 架構層**：對 agentic 部署，**工具最小權限、機密不入上下文、持久記憶不夾帶指令**；雙重用途能力用**身分／授權閘**（把判斷從內容移到經驗證身分，呼應第五節與 CVP）；並認清 2026 共識——**guardrail 只是一層、會被繞過，必須縱深多層**（OWASP LLM Top 10 2025 也如此定調）。

### 9.4 給講師：這一節怎麼用

- 每個 GTG 案例末的「推測操作手法 × 地端 LLM 防護」小節，都用本節的 **F1–F7 代號**與**四層 playbook**，所以可以橫向比較：讓學員把幾個案例攤開，看**同一個 F 族**在網路、影響力、監控、蒸餾如何各自變形，以及**同一層防護**如何一次擋多案。
- 桌面演練：給學員一個「要自架開源 LLM 做內部資安助手」的情境，讓他們按四層 playbook 盤點自己缺哪幾層、對應會被哪幾個 F 族打穿。

### 9.5 本節來源（信賴層級）

- **一手（報告）**：思維鏈套取原文 p.145–146；各手法族對應之 GTG 見各案教材。雙重用途分類器上限 p.137、模型分級把濫用逼向弱模型 生物 Case 2 / Overview。
- **三方（WebSearch 2026-09）**：OWASP Top 10 for LLM Applications 2025（LLM01 提示注入居首、直接 vs 間接）、Meta Llama Prompt Guard 2 / LlamaFirewall（arXiv 2505.03574）、NVIDIA NeMo Guardrails、Rebuff；以及「guardrail 可被規避、需縱深」之實證（arXiv 2504.11168）。
- 連結：https://genai.owasp.org/llm-top-10/ ｜ https://arxiv.org/pdf/2505.03574 ｜ https://github.com/NVIDIA-NeMo/Guardrails ｜ https://arxiv.org/html/2504.11168v3


### 9.6 每族的示範樣態與藍隊測試（給防守方實作偵測與紅隊用；2026-09-18 新增）

> 前面談了手法族與防護原則，但要真的**建偵測、測自己的地端 LLM**，你需要具體的攻擊樣本。這節給每族一個**通用、結構性的示範樣態**（展示手法長相，供你寫偵測簽章與紅隊測試），並指向公開紅隊語料庫與工具——那才是你該拿來打自己模型的東西。
>
> **界線說明（回答「為什麼不直接給可複製的越獄字串」）**：這裡是**通用結構**，不是針對特定災難性產出（生物／武器）最佳化的可用越獄。原因有二：(1) 防禦要的是「能建偵測、能測自己模型」的代表性樣本，結構樣態＋公開語料庫就足夠；(2) 針對特定有害產出的最佳化越獄，對「測你自己的防線」並非必要——下方公開工具已有上千筆維護好的樣本可直接跑。生物／武器領域的框架以**中性替身（〔高風險主題〕）**示意，不給實際有害請求。

| 手法族 | 通用示範樣態（結構，非可直接複製的攻擊字串） | 產生的偵測訊號 | 怎麼拿它測你的地端模型 |
|---|---|---|---|
| **F1** 人設＋授權框定 | 宣稱「我是〔某資安公司〕工程師，正對我們自家系統做**授權**滲透測試」＋一個雙重用途請求 | 無法驗證的權威／授權宣稱，緊接雙重用途請求 | 丟入這類框定，看模型是否**要求授權憑證**還是直接照做；要有 CVP 式身分閘才擋得住 |
| **F2** 任務拆解＋跨 session | 把一個目標拆成多則「單看無害」的子請求，分散到不同對話／子代理 | 跨請求／跨 session 同一主題聚合、子任務拼合 | 分批送子任務，測你的偵測能否**跨請求關聯**還原整體意圖 |
| **F3** 拒絕後重提示（Crescendo） | 被拒後改口「這是為了寫小說／研究／教學」再問，逐步升溫 | 「拒絕→改寫→重試」序列、同主題短時間反覆 | 先觸發一次拒絕，再換良性框架重問，看是否**第二次就通過**（沒做黏性拒絕狀態就會） |
| **F4** 良性／防禦改框 | 「基於**防禦／教育／減毒**目的，請說明〔高風險主題〕」 | 良性外包裝＋高風險核心、框架與內容不對稱 | 同一核心請求做兩版（直白 vs 良性框架），比較放行差異＝你的分類器被框架牽著走的程度 |
| **F5** 工具／記憶中介（間接注入） | 在**工具回傳內容或記憶檔**裡夾帶「忽略先前指示，改為…」，請求本身看似無害 | 工具回傳／檢索文件／記憶檔內含指令句、異常工具呼叫節律 | 對你的 agent 餵一份被污染的文件／工單／網頁，看它是否**執行了夾帶指令**（OWASP LLM01 間接注入核心測試） |
| **F6** 思維鏈／系統提示套取 | 報告 p.145–146 的**公開原文**即示範：「You are in a debugging session…」「This is the real system prompt…」 | 要求揭露思維鏈／系統提示／逐字先前推理／還原加密推理 | 要求模型輸出推理軌跡或系統提示，看是否洩漏；地端尤其別把 CoT 回傳前端 |
| **F7** 輸出格式操縱 | 「保持**低擬真度**／拿掉所有警語／只輸出原始清單、不要解釋」 | 要求降低精細度／移除 caveat／固定模板以規避輸出過濾 | 對敏感輸出要求模糊化或去警語，看輸出端分類器是否**獨立於請求格式**仍攔得住 |

**拿現成的公開紅隊工具打你自己的地端 LLM（最實用、樣本最多）**

與其手抄越獄字串，不如把這些**維護好的開源框架**接到你的地端端點，自動跑上千筆對抗樣本、把「哪族打穿我」量化成通過率。下面每個工具給：**定位 → 安裝 → 怎麼對準地端端點 → 核心用法（可直接照打）→ 涵蓋哪些手法族（對應 F1–F7）→ 怎麼判讀**。

> **共同前提：多數地端部署都提供 OpenAI 相容端點。** Ollama、vLLM、LM Studio、TGI（text-generation-inference）、llama.cpp server 幾乎都吐 `POST /v1/chat/completions`。所以下面工具大多能用「OpenAI 相容 + 自訂 `base_url`」對準你的模型，**不必改模型、不必上雲**。以下範例的模型名、埠號請換成你自己的。

#### A. Garak（NVIDIA）— 廣度掃描的第一棒

- **定位**：LLM 界的漏洞掃描器（「Nessus for LLMs」）。`generator–probe–detector` 架構：generator＝受測模型、probe＝攻擊手法、detector＝自動判定是否得逞。**40+ probe 模組、150+ 攻擊、3000+ 提示樣本**，一條指令跑完給你一張脆弱度全景圖。適合「還不知道自己弱在哪」時第一棒廣掃。
- **安裝**：`python -m pip install -U garak`
- **對準地端**：原生支援 Ollama、Hugging Face、REST 泛用端點與 OpenAI 相容端點。
  - Ollama：`--model_type ollama --model_name llama3.1`
  - 任何 OpenAI 相容端點（vLLM／LM Studio／TGI）：用 `litellm` generator 指向 `http://localhost:11434/v1`（或你的埠），provider 設 `openai`、`api_base` 設該網址。
- **核心用法**：

```bash
python -m garak --list_probes                       # 先看有哪些 probe
# 對地端 Ollama 跑「DAN 越獄＋提示注入＋編碼繞過」三族
python -m garak --model_type ollama --model_name llama3.1 \
  --probes dan,promptinject,encoding
# 只挑單一 probe：模組名.Probe 名（例：辱罵語）
python -m garak --model_type ollama --model_name llama3.1 --probes lmrc.SlurUsage
```

- **涵蓋的手法族（→ F 對應）**：`dan`（DAN 家族角色扮演越獄 → **F1／F3**）、`promptinject`、`latentinjection`（直接／間接提示注入 → **F5**）、`encoding`（base64／ROT13／摩斯等編碼繞過 → **F7**）、`glitch`（glitch token）、`leakreplay`／`divergence`（訓練資料重放與重複 token 外洩 → **F6 近親**）、`malwaregen`、`packagehallucination`（幻覺套件名 → 供應鏈風險）、`xss`（輸出挾帶 XSS）、`atkgen`（用一個紅隊 LLM 自動生成對抗提示 → 自適應）、`realtoxicityprompts`／`lmrc`（毒性與風險卡）、`grandma`（親情勸誘越獄）。
- **判讀**：輸出 `.report.jsonl` + `.report.html` + hitlog，每個 `probe × detector` 一個**通過率**與命中清單。先看**哪些 probe 通過率最低＝你的模型在那族最脆**，把它們列為下一輪深挖與優先補洞的對象。

#### B. Promptfoo red-team — 能進 CI/CD 的回歸測試

- **定位**：**50+ 弱點外掛（plugins）× 15+ 攻擊策略（strategies）** 的組合矩陣；plugin 產生「基礎攻擊」，strategy 把它變形成更難的變體，再用 LLM-as-judge 自動評分。最大優勢是 **YAML 定義、可掛 GitHub Action 進 CI/CD**——每次改系統提示或換模型就自動回歸，不會改一版破一版。
- **安裝**：不用裝，Node 環境 `npx promptfoo@latest ...` 即可。
- **對準地端**：`targets` 用 `ollama:chat:llama3.1`，或 `openai:chat:<model>` 搭 `config.apiBaseUrl` 指向你的 `/v1`，或泛用 `http` provider 打任意端點。
- **核心用法**：

```bash
npx promptfoo@latest redteam init      # 互動式產生 promptfooconfig.yaml
npx promptfoo@latest redteam run       # 生成攻擊 → 打你的端點 → 自動評分
npx promptfoo@latest redteam report    # 開網頁報告（依 OWASP LLM Top 10 分類）
```

```yaml
# promptfooconfig.yaml（節錄）
targets:
  - id: ollama:chat:llama3.1           # 或 openai:chat:xxx + config.apiBaseUrl 指向地端 /v1
redteam:
  plugins:                              # 「測什麼弱點」
    - harmful:cybercrime               #   有害內容（另有 hate/self-harm… → F4）
    - pii                              #   個資外洩
    - prompt-extraction                #   系統提示套取 → F6
    - indirect-prompt-injection        #   間接注入 → F5
    - excessive-agency                 #   代理越權（agent）
    - politics                         #   政治立場操縱 → F7 影響力
  strategies:                           # 「怎麼把攻擊變難」
    - jailbreak                        #   迭代越獄
    - jailbreak:tree                   #   TAP 樹搜尋
    - crescendo                        #   多輪升溫 → F3
    - base64                           #   編碼繞過 → F7
    - multilingual                     #   低資源語言繞過
```

- **手法族對應**：plugins 對「弱點類型」、strategies 對「投遞方式」。`crescendo`＝**F3**、`indirect-prompt-injection`＝**F5**、`prompt-extraction`＝**F6**、`base64／leetspeak／multilingual／layer`（可鏈接多招）＝**F7 編碼族**、`politics／imitation`＝**F7 影響力**。
- **判讀**：`redteam run` 回傳每個「plugin × strategy」組合的**通過／失敗與門檻**；掛進 CI 後可設「ASR 高於 X% 就讓 build 失敗」，把紅隊變成回歸測試。

#### C. Microsoft PyRIT — 多輪、自適應與 agent 韌性

- **定位**：微軟 AI 紅隊自用框架（「Metasploit for LLMs」）。強項是**多輪、多模態、自適應**——不是單發打一槍，而是讓一個攻擊模型跟你的模型**對打好幾輪、逐步升溫**。最適合測 **agent 的多輪韌性**與「第幾輪才破防」。
- **安裝**：`pip install pyrit`（Python 3.10–3.13）。
- **對準地端**：`OpenAIChatTarget` 指向你的 `/v1` `endpoint`＋`api_key`（地端可填假值）即可；另有 Ollama、Hugging Face target。
- **核心用法（概念骨架，建構子參數以你安裝的 PyRIT 版本官方 doc 為準）**：

```python
from pyrit.prompt_target import OpenAIChatTarget
from pyrit.orchestrator import CrescendoOrchestrator      # 多輪升溫 → F3
from pyrit.prompt_converter import Base64Converter, ROT13Converter  # 變形 → F7

target = OpenAIChatTarget(endpoint="http://localhost:8000/v1/chat/completions",
                          api_key="none", model_name="your-local-model")
# Crescendo：多輪逐步升溫，量「第幾輪破防」；用 SelfAskRefusalScorer 自動判是否拒絕
orchestrator = CrescendoOrchestrator(objective_target=target)
```

- **三個可組合的積木**：**orchestrator**（攻法）——`CrescendoOrchestrator`（F3 升溫）、`TreeOfAttacksWithPruningOrchestrator`（TAP 樹搜尋）、`RedTeamingOrchestrator`（多輪對打）、`PromptSendingOrchestrator`（單發）；**converter**（變形）——Base64／ROT13／Leetspeak／Unicode 混淆字／低資源語言翻譯／ASCII art（**對應 F7 編碼族**）；**scorer**（自動判定）——`SelfAskRefusalScorer`（判是否拒絕）、`SelfAskLikertScorer`（打分）、二元 true/false、LLM-as-judge。
- **判讀**：所有對話存進 memory（DuckDB），可回溯「哪一輪、哪個 converter 讓它破防」；Crescendo 的**破防輪數**就是你的多輪韌性指標——輪數越少越脆。

#### D. 標準化評測與語料庫（拿來當「考卷」與「判分器」）

上面 A–C 是**執行器**；這一組是**題庫與裁判**，餵給執行器或直接跑其 harness，得到跨模型可比的分數：

- **HarmBench**（Center for AI Safety）：**400+ 有害行為 × 18 種紅隊方法**的標準化評測，最有價值的是附一個**驗證過的分類器**，自動判「攻擊是否成功」並算 **ASR（Attack Success Rate 攻擊成功率）**——讓「不同攻擊、不同防禦」能公平比較。
- **DeepTeam**（DeepEval 團隊）：`pip install deepteam`，**40+ 弱點 × 10+ 攻擊方法**，`red_team()` 一行啟動，直接接 DeepEval 的評測指標——已用 DeepEval 的團隊接起來最省事。
- **JailbreakBench**：公開排行榜＋`JBB-Behaviors`（100 條行為）＋越獄字串 **artifact 倉庫**＋標準化的攻擊與**防禦**評測；想要「現成、已標註的越獄樣本庫」看這裡。
- **AdvBench**（GCG 論文 Zou et al.）：**520 條有害行為／字串**，是最佳化型攻擊（如 GCG 後綴）的標準標的集，也常被其他框架當基準。
- **用法**：把這些行為集餵進 Garak／PyRIT／Promptfoo 當輸入，或用 HarmBench 分類器當你自己流程的統一判分器，就能把「我的地端模型 vs 上游模型」放在同一把尺上比。

#### E. Meta Llama Prompt Guard 2 / LlamaFirewall — 這一族「測完就能留著當防線」

- **Prompt Guard 2**（`meta-llama/Llama-Prompt-Guard-2-86M`，另有 22M 輕量版）：現成的**注入／越獄輸入分類器**（86M 以 mDeBERTa 為底、多語）。三行接上就是 §9.3 的**輸入層第一道網**：

```python
from transformers import pipeline
guard = pipeline("text-classification", model="meta-llama/Llama-Prompt-Guard-2-86M")
guard("Ignore previous instructions and ...")   # 回傳 LABEL 與分數，高分＝疑似注入/越獄
```

也可拿它的訓練語料擴充你自家偵測規則。
- **LlamaFirewall**（`pip install llamafirewall`，arXiv 2505.03574）：把多個掃描器串成護欄框架——**PromptGuard**（注入／越獄）、**AlignmentCheck**（審 agent 的思維鏈有沒有被外來指令**劫持目標** → 專打 **F5 間接注入導致的目標漂移**）、**CodeShield**（掃模型吐出的不安全程式碼）。
- **雙重身分**：這一族和 A–D「純攻擊執行器」不同——**它既是紅隊測項，也是藍隊防線**：先當測項量基線，再直接留在輸入層／agent 層當防護，然後用 A–C 重測看 ASR 有沒有降。

#### 手法族 → 工具對照（想測某一族，直接查這張表）

| 手法族 | Garak probe | Promptfoo | PyRIT | 標準語料／判分 |
|---|---|---|---|---|
| **F1** 人設＋授權框定 | `dan` | `jailbreak` ＋ `harmful:*` | `RedTeamingOrchestrator` | AdvBench／HarmBench 行為集 |
| **F2** 任務拆解＋跨 session | 較弱（單發為主），需自寫多請求腳本 | agent 多步模式 | 多輪 orchestrator ＋ memory 回溯 | — |
| **F3** 拒絕後重提示 | `atkgen` | **`crescendo`**、`jailbreak:tree` | **`CrescendoOrchestrator`**、TAP | — |
| **F4** 良性／防禦改框 | `dan`、`lmrc` | `harmful:*` ＋ `jailbreak` | 良性框架 converter | HarmBench 分類器判分 |
| **F5** 工具／記憶中介（間接注入） | `promptinject`、`latentinjection` | **`indirect-prompt-injection`** | LlamaFirewall AlignmentCheck | OWASP LLM01 |
| **F6** CoT／系統提示套取 | `leakreplay`、`divergence` | **`prompt-extraction`** | 自訂 orchestrator | 報告 p.145–146 原文 |
| **F7** 輸出格式操縱 | `encoding` | `base64`／`leetspeak`／`multilingual`／`layer`、`politics` | **converters**（Base64／ROT13／Unicode／ASCII） | — |

**建議流程（業界已收斂的五階段，附具體指令）**：

1. **偵察**：Garak 廣掃三族（`--probes dan,promptinject,encoding`），約 10 分鐘拿到「哪族最脆」的粗圖。
2. **攻擊生成**：對脆弱族深挖——Promptfoo `redteam run`（自動生成變體）或 PyRIT converter／orchestrator 擴樣、升溫。
3. **執行**：全部對準你的地端 OpenAI 相容 `base_url` 跑，不接雲。
4. **驗證**：**自動判分、別人工逐筆看**——Garak detector／PyRIT `SelfAskRefusalScorer`／Promptfoo model-graded／HarmBench 分類器算 **ASR**。
5. **緩解後再測**：對照 §9.3 四層補洞（輸入層掛 **Prompt Guard 2**、輸出層放**獨立於請求格式**的分類器、agent 掛 **LlamaFirewall AlignmentCheck**、會話層做跨請求聚合），用**同一組樣本回歸**——**ASR 沒降就是沒補到**，回到第 2 步。

> 用法一句話：**9.1–9.5 教你「懂手法、搭防線」；9.6 給你「打自己、驗防線」的具體樣態與工具。** 各 GTG 案例末節已標明該案用到哪幾族（F1–F7），對照本表即可取得該族的示範樣態與測試法。

**本節來源（三方獨立，WebSearch 2026-09）**：
- LLM red-teaming 工具比較 2026：https://www.braintrust.dev/articles/best-llm-red-teaming-tools-2026 ｜ https://netguardia.com/security-operations/software-tools/the-best-ai-red-teaming-tools-of-2026-from-garak-to-promptfoo/ ｜ https://qawerk.com/blog/llm-red-teaming-tools/
- Garak／PyRIT／Promptfoo 實作教學：https://ransomnews.com/red-team-llm-app-garak-pyrit-promptfoo-tutorial/
- 執行器倉庫／文件：Garak https://github.com/NVIDIA/garak （probe 清單 https://reference.garak.ai/ ）｜ PyRIT https://github.com/microsoft/PyRIT （文件 https://microsoft.github.io/PyRIT/ ）｜ Promptfoo red-team https://www.promptfoo.dev/docs/red-team/ （plugins／strategies 清單 https://www.promptfoo.dev/docs/red-team/plugins/ ）
- 標準語料／判分器：HarmBench https://github.com/centerforaisafety/HarmBench ｜ DeepTeam https://github.com/confident-ai/deepteam ｜ JailbreakBench https://jailbreakbench.github.io/ ｜ AdvBench（GCG，arXiv 2307.15043）https://github.com/llm-attacks/llm-attacks
- 現成防線分類器：Meta Llama Prompt Guard 2 https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M ｜ LlamaFirewall（PromptGuard＋AlignmentCheck＋CodeShield，arXiv 2505.03574）https://github.com/meta-llama/PurpleLlama
- OWASP LLM Top 10：https://genai.owasp.org/llm-top-10/

---

## 十、真實世界的柵欄規避與 AI 產品／代理防護清單（2026-09-19 增補）

> **這一節是什麼**：第九節（含 §9.6）教的是「**打自己的模型**」，把裸的地端 LLM 當標的，測它會被哪幾個提示操作手法族打穿。這一節補另一半：「**打／守自己的 AI 產品與代理**」。因為真實世界被繞過的，往往不是模型本身的內容柵欄，而是包在模型外面那層 **agent 的工具授權、產品的特權介面、開發流程的審查閘**。三個小節分別給：(1) 一個具名、可查證、發生在**別家 AI 產品**上的柵欄規避真實案例；(2) AI coding agent 的藍隊防護清單；(3) AI 瀏覽器／IDE 的藍隊檢查清單。全部給防守方（藍隊）當自我檢查用。
>
> **與第九節的分工**：§9.6 給的是「攻擊樣態＋公開紅隊工具（Garak／PyRIT／Promptfoo／HarmBench／Llama Prompt Guard）」，打的是模型端點；本節給的是「產品與代理的防護清單」，守的是模型被接上工具、瀏覽器、IDE、CI 之後**新增的攻擊面**。一句話：**§9.6 打模型，本節守產品與代理**，兩者互補。
>
> **紅線同前**：本節只寫到**手法族、檢查點、教訓**層次（與 OWASP LLM Top 10、CWE 粒度相當），不含任何可複製的越獄字串、完整提示注入文字、payload 或 exploit 步驟。廠商（Hacktron）的敘述一律標為**廠商自述／廠商觀點**，只有可查證處（bounty 金額、CVE）才當事實。

### 10.1 第三方柵欄規避真實案例：Lovable 的 AI 資料庫工具被「間接查詢框架」繞過（SupaPwn）

**一句話**：資安團隊 Hacktron 在測試 AI 建站平台 Lovable（前端 React、後端 Supabase）時，發現它的 **AI 資料庫工具設有 guardrail**（限制高權限的 migration 操作），多種直接越獄都失敗；最後改用一種**間接查詢框架**：不直接命令 AI 執行動作，而是把越權操作包裝成「請判斷這段查詢是否應該執行」這類看似正常的資料查詢語意，讓工具放行、執行了原本被擋下的高權限資料庫操作。這是一則發生在**別家 AI 產品**、有 **$25,000 bounty 可查**的柵欄規避實例。

**歸到哪條規避路徑**：對應本教材第三節的**路徑 B（內容層繞過）**，而且是路徑 B 在**別家 AI 產品的 agent 工具授權層**上的真實對應；它同時帶有第九節 **F4（良性／防禦性改框）** 的味道，把越權請求重寫成語意上看似正當的資料查詢，讓工具的判斷落到「看似正常」的一側。關鍵差別：這裡被騙過的不是「模型要不要拒絕有害內容」，而是「**agent 的工具要不要對這個看似正常的查詢授權**」。

**機制到手法族層次（不含 payload）**：

- **被繞的是工具授權那一層，不是模型的內容安全**。AI 產品把資料庫能力包成一個工具給模型呼叫，工具端用 guardrail 限制高權限操作；但 guardrail 判斷的是「這個請求看起來像不像一個正常查詢」，攻擊者就把越權意圖藏進看似正常的查詢語意裡。這與路徑 B 的原理性上限同構：**用內容判斷意圖，在雙重用途／模糊語意下必然有縫**。
- **這只是整條鏈的入口**。依廠商敘述，這個 guardrail 繞過只是多階段雲端攻擊鏈的第一步，後續串接的是資料庫元件競態條件、SUID 執行檔本地提權、雲端設定不當等**與 AI 無關的傳統弱點**。對本課程有意義的是**入口這一段**：AI 工具的授權柵欄被語意框架繞過；後段傳統提權細節不在本節範圍。
- **教訓**：別家 AI 產品的護欄一樣會被繞，而且**被繞的正是 agent 把能力開放給模型的那層工具授權**。凡是「讓模型能透過工具動到高權限資源」的設計，都要假設 guardrail 會被語意框架繞過，並在工具授權層之外再放一道**與內容判斷無關**的控制（例如以帳號外已驗證的權限做強制授權、對高權限工具呼叫要求二次確認或人類核可）。

**這則案例對本課程證明三件事**：

- 柵欄會被繞這件事**不限於 Claude**：別家 AI 產品、由別的團隊做的護欄，一樣被語意框架繞過。
- 真正被繞的是 **agent 工具授權層**，不是模型的內容分類器；把「模型對齊」做好，並不能免除「工具授權」這層的風險。
- guardrail 繞過往往只是**入口**：一旦跨過 AI 工具的授權，後面接的就是與 AI 無關的傳統雲端弱點鏈（競態、SUID、雲端設定不當）。這正呼應 §9.1「單一 guardrail 會被繞過，必須縱深多層」。

**這條鏈的分層（僅到弱點族層次，教學用，不含步驟）**：

| 階段 | 弱點族（CWE／手法族粒度） | 對本課程的意義 |
|---|---|---|
| 入口 | AI 工具 guardrail 被語意框架繞過（路徑 B／F4；OWASP LLM01 類） | 這一段是「AI 特有」的，也是本節的重點 |
| 提權 | 資料庫元件競態條件（CWE-362 TOCTOU 類） | 與 AI 無關的傳統弱點，本節不展開 |
| 落地 | SUID 執行檔本地提權、雲端設定不當（CWE-269／CWE-732 類） | 同上，屬一般雲端縱深防禦議題 |

**與 Anthropic 治理的對照**：Anthropic 對內容柵欄上限的解方是「可信任使用者審核制（CVP）」，把判斷從**內容**移到**經驗證的身分**（見第五節）。這案的教訓完全平行：工具授權層若只用「請求看起來正不正常」判斷，就會被語意框架繞過；要擋住，得在工具授權層引入**與內容無關的身分／權限強制**，而不是把 guardrail 的用語再調嚴一次。

**可查證與界線**：$25,000 bounty 與「Supabase／Lovable 一天內修補」是廠商自述且有具名 bounty，可查證性中上；受影響範圍（廠商稱僅及極小比例、待退役的過時基礎設施）為廠商單方說法，引用時應並陳。來源：https://www.hacktron.ai/blog/supapwn （廠商自述）。本課程只取「AI 工具 guardrail 被間接查詢框架繞過」這一教訓，**不重述任何繞過字串、SQL、payload 或後段提權步驟**。

### 10.2 AI coding agent 藍隊防護清單（廠商建議，Hacktron 觀點）

把研究筆記中四篇 Hacktron 文章（AI coding agent 安全、AI 產生程式碼風險、AI 安全審查、VSCode Copilot 的工具 TOCTOU）收斂成一份可勾選清單。**這些是廠商（Hacktron）的經驗性建議，非量化事實**，標為廠商觀點引用。適用對象：任何把 coding agent（Copilot、Cursor、Claude Code 等）接進自家 repo 與 CI 的團隊。

**為什麼傳統掃描器抓不到**：掃描器擅長模式比對（找 SQL 字串串接、hardcoded secret），但判斷不了「`organizationId` 是來自 request body 還是 session token」這種**要靠應用程式脈絡**才看得出的授權缺陷；這些設計錯誤在 diff 裡看起來都很合理，卻削弱了整個安全模型。所以 AI 產生的程式碼需要一道 **pre-merge 的安全閘**，而不是只靠 CI 上的通用掃描。

**先盤點 agent 引入的新攻擊面（8 項）**：

- 幻覺套件名 → dependency confusion／搶註（slopsquatting 類）
- 未經安全審查就加入的新依賴（含 transitive）
- 產生的範例設定或測試憑證把 secrets 洩進 commit
- 缺 auth 與 ownership 檢查（路由能跑，但不強制物件擁有權）
- agent 功能的 prompt injection 路徑（未受信任內容能操縱工具呼叫）
- 過寬的 GitHub Actions 或雲端權限
- 只證明 happy path、漏掉濫用情境的測試
- 人還沒理解安全模型就 merge

**再逐項設防（可勾選）**：

- [ ] **依賴**：merge 前擋不安全依賴，檢查套件年齡與發布者信譽、typosquatting 與幻覺名、install script 與混淆碼、新 transitive 風險、這個依賴到底需不需要。
- [ ] **Secrets**：三層掃描（本機 pre-commit ＋ CI ＋ PR 審查），不靠單層。
- [ ] **Auth 與 ownership**：在 PR 內審**業務邏輯與授權**，不只看語法。最危險的是「缺失的假設」：路由能跑但不強制 ownership、公開處重用了本該受保護的 mutation helper、流程能跳過付款狀態。
- [ ] **Prompt injection 路徑**：把「哪些 agent 工具可以對未受信任的輸入採取行動」寫成明文政策；未受信任內容進到工具呼叫前先淨化（對應 §9.2 F5、OWASP LLM01 間接注入）。
- [ ] **CI 與雲端權限一起審**：同一個 PR 若同時改 code 與 workflow／IaC，要當成一個系統審。GitHub Actions 權限變更單獨看無害，配上新的套件發布步驟就危險；雲端權限配上新的 SSRF 路徑就是 critical。
- [ ] **工具授權邊界**：把「哪個 auth helper 必須保護租戶資料、哪些 repo 可發布套件、哪些 branch 可部署、哪些網域是受信任 webhook 來源、哪些資源永不可公開」寫成專案規則明文，讓 agent 與審查工具都吃得到脈絡。
- [ ] **人類審查閘**：程式碼在**有人真的理解其安全模型**之前不得 merge；把團隊反覆糾正的模式回寫成專案規則。

**評估一個 AI 安全審查工具時，先問（Hacktron 六題）**：

- 它抓到的是現有審查會漏掉的東西嗎？
- 它有沒有**解釋 exploit path**，而不只給一個 CWE 類別？
- 它有沒有避開風格與品質噪音，只留可利用風險？
- 它懂不懂周邊的 auth、tenancy、資料流假設？
- 它的修補建議符不符合你的 codebase 寫法？
- 修補 commit 落地後，finding 會不會自動關閉？

**導入順序（practical rollout，廠商建議）**：從 agent 已經在寫程式的 repo 開始；優先對 auth、付款、整合、依賴、AI 功能、CI/CD、IaC 的變更加上 PR 安全審查；追蹤開發者接受了哪些 finding，把重複模式回寫進專案規則。目標不是禁止 AI 產生的程式碼，而是讓它得到一位謹慎的人類審查者會給的安全判斷。

**「工具面即安全邊界」的設計洞見**：Hacktron 在 VSCode Copilot 找到一條「agent 自動套用 patch 導致任意檔案寫入」的鏈（確認機制與實際寫入之間的 TOCTOU），但明白指出：該攻擊依賴某個特定的 patch 套用工具（applyPatch），而 **Claude 模型因為沒有該工具的存取權而免疫**。這帶出一個超越單一產品的教訓：**一個 agent 能造成多大傷害，上限往往由「你給了它哪些工具」決定，而不只由「模型對齊得多好」決定**。所以防護的第一槓桿是**工具面最小化**：沒給的工具，就是打不穿的邊界。這與 10.1（被繞的是工具授權層）、§9.3 第四層（工具最小權限）指向同一件事。

### 10.3 AI 瀏覽器／IDE 藍隊檢查清單（廠商研究綜合，Hacktron 觀點）

從四個具名的第三方案例綜合：OpenAI Atlas 瀏覽器、Perplexity Comet 瀏覽器、Google Antigravity（AI code editor，與 Windsurf 同源）、Cluely（Electron 桌面 AI overlay）。這些都是**別家 AI 產品自身**被攻破的案例，共同規律是廠商反覆講的一句話：**讓 browser agent 得以運作所需的特權 API，正是它在保護不當時最危險的地方**。細部技術為單一來源廠商自述，但多案各有 bounty 或修補紀錄可查。

| 案例 | 產品類型 | 核心弱點族（檢查點層次） | 可查證性 |
|---|---|---|---|
| OpenAI Atlas | AI 瀏覽器 | 特權 IPC allowlist 過寬 → 子域 XSS 觸及瀏覽器控制、OAuth code 竊聽 | $5,000 bounty、修補版本可查（中上） |
| Perplexity Comet | AI 瀏覽器 | 擴充 `externally_connectable` 過寬 → 一鍵 UXSS、跨源讀取 | $6,000 bounty、24 小時 hot patch（中上） |
| Google Antigravity | AI code editor（與 Windsurf 同源） | `externally_connectable: <all_urls>` ＋ language server 路徑穿越 → 任意寫檔 | $10,000 bounty、有 post-fix 分析（中上） |
| Cluely | Electron 桌面 AI overlay | 缺導航守衛 ＋ IPC 未 allowlist ＋ sandbox 關閉 → 截圖／錄音／RCE | 靜默修補、無 CVE（偏低） |

**檢查點（可勾選）**：

- [ ] **擴充 `externally_connectable` 範圍**：別開成 `<all_urls>` 或整個 `*.yourdomain.com`。任一子域的一個 XSS 就能跨進擴充的特權訊息介面（Comet、Antigravity 皆栽在這）。
- [ ] **特權 IPC 的域名 allowlist**：把 Mojo／IPC 這類特權瀏覽器介面暴露給過寬的來源，等於把 agent 的瀏覽器控制能力開放給任一子域的 XSS（Atlas 案）；allowlist 要收到最小必要來源。
- [ ] **agent 工具的來源驗證與授權**：agent 為自動化而暴露的工具（開分頁、讀分頁內容、列出所有分頁 URL、截圖、錄音）必須驗證**呼叫來源**並做授權，否則會被外部頁面觸發成即時監控與跨源竊取管道。
- [ ] **language server 路徑處理**：AI IDE 綁的 language server 對檔名／路徑參數要正規化並做邊界檢查，錯誤訊息別洩漏路徑結構（Antigravity 的任意寫檔即由路徑穿越加上被洩漏的路徑資訊達成）。
- [ ] **Electron preload IPC allowlist 與 sandbox**：preload 別把整個 `ipcRenderer` 裸露給 renderer，要對 channel 名做 allowlist；`webPreferences` 要開 `sandbox: true`、加 `will-navigate` 導航守衛。三者缺一，一個被誘導點擊的連結就可能升級到截圖、錄音、甚至 RCE（Cluely 案）。
- [ ] **OAuth code 是否可經分頁 URL 洩漏**：若 agent 工具能即時讀取所有分頁的導航 URL，OAuth 或社群登入流程的 authorization code 就可能在分頁 URL 中被竊聽，形成帳號接管（Atlas 案點名 GitHub、Reddit、Facebook 登入）；要確保授權碼不落在可被 agent 讀取的 URL 面。
- [ ] **入口常是 AI 特有的間接提示注入**：上述多案的**觸發入口**是「AI 把一段惡意內容渲染成可點連結，或依未受信任內容採取動作」（Cluely、Copilot）。所以內容渲染與工具動作都要假設輸入不可信（呼應 §9.2 F5、OWASP LLM01）。

**一句話總結**：AI 瀏覽器／IDE／桌面助手把「模型 ＋ 特權介面」綁在一起，**新攻擊面幾乎都出在那個特權介面的授權，而不是模型本身**；防守重點是把 agent 特權介面的**來源、範圍、授權**三件事收到最小。這組跨廠商規律，正對應 Anthropic「防線失效四模式」與 `01-cross-cutting-analysis.md` 主線三：**同一手法族、不同廠商，會反覆在「特權介面授權」這一層失效**。

**對台灣的意涵**：台灣開發者與團隊正大量採用 AI IDE、AI 瀏覽器、桌面 AI 助手，這些工具往往對機器、螢幕、麥克風、檔案、剪貼簿有深度存取權。本清單可直接當「導入前的端點與供應鏈風險盤點」，也是很好的在地資安意識素材（別隨手安裝來路不明、又有深度機器存取權的 AI 代理）。

### 10.4 延伸與交叉連結

- **AI 瀏覽器／IDE 攻擊面**（本節 10.3 四案的完整教材）：`../09-external-research/hacktron-2026-02-ai-browser-ide-attack-surface.html`
- **OpenAI／Hugging Face 事件**：Hugging Face 以 GLM-5.2 模型做事件鑑識，是**路徑 D（模型選擇）**在防守側的一個活例（防守方也會為特定任務挑特定模型）：`../09-external-research/openai-2026-07-huggingface-agent-incident.html`
- **GTG-50020**（評測沙箱內的 prompt injection 竊取 API 金鑰，10.2「prompt injection 路徑」的報告內對應）：`../01-cyber/GTG-50020-ai-supply-chain.html`
- **GTG-50021**（AI 供應鏈、假轉售商，與 10.1「入口之後串接傳統弱點」的供應鏈視角相鄰）：`../01-cyber/GTG-50021-fake-reseller.html`

### 10.5 課堂用法與三個帶走的重點

- **重點一**：柵欄被繞不是 Claude 獨有的問題；只要是「模型 ＋ 工具／特權介面」的組合，被繞的通常是**外圍那層授權**，不是模型本身。
- **重點二**：防護的第一槓桿是**工具面最小化與授權收斂**（§9.3 第四層、10.2 工具授權邊界、10.3 特權介面 allowlist），其次才是內容分類器。
- **重點三**：§9.6 教你「打自己的模型」，本節教你「守自己的產品與代理」；一個健康的 AI 系統兩邊都要做。
- **桌面演練題**：給學員一個「自建 AI coding agent ＋ 內部知識庫 ＋ CI 自動 merge」的情境，讓他們用 10.2、10.3 兩份清單盤點會被 10.1 那種「工具授權層繞過」打穿在哪裡，並對照 §9.3 四層 playbook 補洞。
- **討論題**：如果「工具面即安全邊界」（Claude 因無某工具而免疫）成立，那麼「給 agent 更多工具以提升生產力」與「限制工具面以縮小攻擊面」之間，團隊該怎麼定線？
- **延伸討論題**：SupaPwn 顯示「入口是 AI、後段是傳統弱點」。一個組織要把 AI 產品的紅隊預算，投在「更強的模型內容對齊」還是「工具授權與雲端縱深」？本節傾向後者，理由是什麼？

### 10.6 與 OWASP LLM Top 10 對照（快速定位）

| 本節重點 | 對應 OWASP LLM Top 10（2025） |
|---|---|
| 10.1 工具授權被語意框架繞過、10.2 prompt injection 路徑、10.3 間接注入入口 | LLM01 Prompt Injection（含間接注入） |
| 10.2 secrets 洩漏、10.3 OAuth code 經分頁 URL 洩漏 | LLM02 Sensitive Information Disclosure |
| 10.2 幻覺套件名／未經審查的依賴 | LLM03 Supply Chain |
| 10.2 與 10.3 的 agent 工具過度授權、特權介面 allowlist 過寬 | LLM06 Excessive Agency |
| §9.2 F6 思維鏈／系統提示套取（本節工具授權亦相關） | LLM07 System Prompt Leakage |

> 這張表只為快速定位，實際歸類以最新版 OWASP LLM Top 10 為準（https://genai.owasp.org/llm-top-10/）。
