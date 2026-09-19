# Google Threat Intelligence Group《GTIG AI Threat Tracker: Advances in Threat Actor Usage of AI Tools》（2025-11）

> 課程模組：09 延伸研究 ｜ 來源類型：官方威脅報告 ｜ 原文：https://cloud.google.com/blog/topics/threat-intelligence/threat-actor-usage-of-ai-tools ｜ 整理日期：2026-09-14

---

## 0. 本教材使用說明

本檔收錄的是 **GTIG AI Threat Tracker 系列的第一期**（系列前身是 2025-01 的《Adversarial Misuse of Generative AI》）。它在模組 09 裡的位置很特別，有三個理由：

1. **它是「執行期 AI 惡意程式」這個類別的原始文獻。** PROMPTFLUX、PROMPTSTEAL 這兩個名字後來被整個產業反覆引用，本課程主體報告（Anthropic 2026-09）雖然通篇在講 agentic 自主化，卻**沒有任何一個對應案例**。要理解這個缺口從哪裡來，必須回到這一份。
2. **它與 Anthropic 2025-11-13 的《Disrupting the first reported AI-orchestrated cyber espionage campaign》只差一週**。兩份同月報告對「AI 濫用走到哪一步」給出的答案幾乎相反。這個時間上的巧合是本模組最好的「廠商敘事框架」教材，第 4.9 節專門處理。
3. **它的 Table 1 裡有一筆事後被推翻的情報**（PROMPTLOCK 實為紐約大學 Tandon 工程學院的學術概念驗證），而 GTIG 至今未在頁面上加註更正。這給了課堂一個非常罕見的、可完整重建的「情報生命週期」案例。

**閱讀順序建議**：第 1 節速覽 → 第 6 節圖表判讀（Figure 1、Figure 5 是全報告資訊密度最高的兩張，且 Figure 6 與 Figure 8 之間有一個必須親自看圖才會發現的問題）→ 第 3 節案例 → 第 4 節對照 → 第 9 節第三方驗證。

**資料層次標示規則**（沿用本模組慣例）：

- **［原文］**＝ GTIG 部落格或 PDF 可直接追溯的內容，附 PDF 頁碼。
- **［外部］**＝ WebSearch 取得的第三方研究與媒體，附 URL 與日期。
- **［分析］**＝ 本教材作者的推論與教學詮釋，報告沒有明說，學員應視為可被挑戰的假設。

**頁碼標示方式**：本份 PDF 共 20 頁，封面不編頁，因此**版面印出的頁碼＝PDF 頁序減一**（PDF 第 5 頁印的是「4」）。本教材一律用 **PDF 頁序**（寫成 `PDF p.5`），避免歧義。

---

## 1. 一頁速覽

1. **報告的頭條主張：AI 第一次被放進惡意程式的「執行期」。** 原文：「For the first time, GTIG has identified malware families, such as PROMPTFLUX and PROMPTSTEAL, that use Large Language Models (LLMs) during execution. These tools dynamically generate malicious scripts, obfuscate their own code to evade detection, and leverage AI models to create malicious functions on demand, rather than hard-coding them into the malware.」（PDF p.3）這條線是整個 GTIG 系列的起點，後續 2026-05 的 PROMPTSPY、2026-09 的 agentic 惡意程式都從這裡長出來。

2. **五支惡意程式，但「真正在行動中用過」的只有三支，而且分量差很多。** Table 1（PDF p.4）列 FRUITSHELL、PROMPTFLUX、PROMPTLOCK、PROMPTSTEAL、QUIETVAULT 五支，狀態欄分成「Observed in operations」與「Experimental」。**唯一有明確國家級行為者、明確受害國、且被第三方獨立證實的只有 PROMPTSTEAL**。教學上必須把這個層次差講清楚，否則整份報告會被讀成「AI 惡意程式已經全面部署」。

3. **PROMPTSTEAL ＝ CERT-UA 的 LAMEHUG，是本報告唯一的硬證據。** 俄羅斯 GRU 關聯的 **APT28（aka FROZENLAKE）** 2025 年 6 月對烏克蘭使用，靠**竊來的 Hugging Face API token** 查詢 **Qwen2.5-Coder-32B-Instruct**，即時生成 Windows 單行指令並**盲目執行**。GTIG 原話：「APT28's use of PROMPTSTEAL constitutes our first observation of malware querying an LLM deployed in live operations.」（PDF p.7）［原文］；CERT-UA 於 2025-07-17 以 LAMEHUG 之名獨立公告，時間點早於 GTIG 四個月［外部］。

4. **兩筆必須打折的情報：PROMPTFLUX 被誇大，PROMPTLOCK 根本不是威脅行為者做的。** GTIG 自己寫明 PROMPTFLUX「is currently in a development or testing phase」、「does not demonstrate an ability to compromise a victim network or device」，而且**最關鍵的自我改寫函式 `AttemptToUpdateSelf` 在原始碼裡是被註解掉的**（PDF p.5）；研究者 Marcus Hutchins 公開批評業界「overblowing the significance of AI slop malware」［外部］。PROMPTLOCK 則被 **紐約大學 Tandon 工程學院**確認為其學術專案「Ransomware 3.0」，團隊測試時上傳到 VirusTotal 而被誤認［外部］。**截至 2026-09-14 重抓部落格頁面，GTIG 沒有任何更正說明或編者註。**

5. **繞過柵欄的手法極度低技術，而且攻擊者反而洩漏了自己的基礎設施。** 一個 China-nexus 行為者被 Gemini 拒絕後，改稱自己是 **CTF（capture-the-flag）參賽者**就拿到了可用於利用系統的資訊，並「appeared to learn from this interaction」，之後把 CTF 前綴套用到釣魚、利用、web shell 開發（PDF p.8）；伊朗 **TEMP.Zagros（aka MUDDYCOAST、Muddy Water）** 假稱自己是「做期末專題的學生」或「在寫一篇國際期刊論文」（PDF p.10）。**沒有咒語工程，只有職業情境。** 但 TEMP.Zagros 為了除錯把 C2 伺服器腳本整份貼給 Gemini，**硬編碼的 C2 網域與加密金鑰一併外洩**，GTIG 據此擴大處置。原文小標直接叫「**Student Error**」：**模型供應商正在變成一種全新的情報蒐集面。**

6. **地下市場在 2025 年成熟了，而且賣的是「成品工具」而不是「偷來的存取」。** Figure 5 用一張矩陣列出 **10 個具名工具**（DarkDev、EvilAI、FraudGPT、LoopGPT、MalwareGPT、NYTHEON AI、SpamGPT、SpamirMailer Bot、WormGPT、Xanthorox）與 6 種宣傳能力。**定價與行銷語彙完全模仿正規 AI 產品**：免費版插廣告、訂閱制分級、加價買圖片生成與 API 存取，甚至還有 Discord 存取權（PDF p.11）。

7. **GTIG 在 IO 上給了一個明確的負面結論。** 「we have not identified these generated articles in the wild, nor identified evidence confirming the successful automation of their workflows... **None of these attempts have created breakthrough capabilities for IO campaigns.**」（PDF p.18）這句話在 2026-05 那一期幾乎原封不動再出現一次，是 GTIG 跨期最穩定的判斷。

8. **這份研究在課程裡要教什麼（一句話）**：教學員**把「AI 濫用」拆成「開發期／執行期」兩個完全不同的威脅面**，並用這份報告的狀態欄、被推翻的 PROMPTLOCK、以及被註解掉的 `AttemptToUpdateSelf`，練習**在一份可信機構的報告內部區分「已部署」「實驗中」與「其實是別人的研究檢體」**。

---

## 2. 報告基本資料

| 項目 | 內容 |
|---|---|
| 機構 | Google Threat Intelligence Group（GTIG），Google Cloud 旗下，整併 Mandiant 與 Google 內部威脅情報 |
| 署名 | 「Google Threat Intelligence Group」（機構署名，未列個別作者）。PDF 末頁 About the Authors 只有一段機構簡介 |
| 標題 | GTIG AI Threat Tracker: Advances in Threat Actor Usage of AI Tools |
| 發布日期 | **部落格頁面標示 2025-11-06**；PDF 內嵌的建檔時間戳為 **2025-11-05 08:14（-05:00）**；多數媒體記為 2025-11-05。差異見第 12 節 |
| 形式 | Google Cloud Blog 長文（HTML）＋ 20 頁 PDF（封面 1 頁、正文 18 頁、作者頁 1 頁）。PDF 由 Adobe InDesign 20.1（Macintosh）產出 |
| 篇幅 | PDF 文字層約 4 萬字元。含 **10 張 Figure、2 張 Table**。無目錄、無書籤、無 IOC 附錄、無 MITRE 附錄 |
| 涵蓋期間 | 未明確宣告區間。文中的時間錨點為「In early June 2025」（PROMPTFLUX）、「In June」（PROMPTSTEAL）、「Throughout August 2025」（APT41）、以及概括性的「in 2025」 |
| 資料來源類型 | **幾乎全部是 Gemini 平台側遙測**（提示內容、帳號行為），加上少量野外樣本分析（PROMPTFLUX、PROMPTSTEAL、QUIETVAULT 檢體）與**地下論壇監看**（英語與俄語論壇的廣告文與討論串） |
| 涉及的模型／產品 | Gemini（明確版本字串 `gemini-1.5-flash-latest`）、Google DeepMind 的分類器與模型層防護、Google Play Protect（未在本期出現）、Big Sleep、CodeMender、SAIF。**非自家**的有 Hugging Face 平台與 `Qwen2.5-Coder-32B-Instruct` |
| 系列位置 | **前作**：2025-01《Adversarial Misuse of Generative AI》（本報告自述為其 update）。**後作**：2026-02《Distillation, Experimentation, and (Continued) Integration of AI for Adversarial Use》、2026-05《Adversaries Leverage AI for Vulnerability Exploitation, Augmented Operations, and Initial Access》（本模組教材 `gtig-2026-05-ai-threat-tracker.html`）、2026-09《From Prompting to Autonomy: The Evolution of Adversarial AI》（本模組教材 `gtig-2026-09-ai-threat-tracker.html`） |

### 2.1 四個關鍵發現（原文逐字）

PDF p.3 的 Key Findings 只有四條，是整份報告的骨架，建議全部投影：

> **First Use of "Just-in-Time" AI in Malware**: For the first time, GTIG has identified malware families, such as PROMPTFLUX and PROMPTSTEAL, that use Large Language Models (LLMs) during execution. These tools dynamically generate malicious scripts, obfuscate their own code to evade detection, and leverage AI models to create malicious functions on demand, rather than hard-coding them into the malware. While still nascent, this represents a significant step toward more autonomous and adaptive malware.

> **"Social Engineering" to Bypass Safeguards**: Threat actors are adopting social engineering-like pretexts in their prompts to bypass AI safety guardrails. We observed actors posing as students in a "capture-the-flag" competition or as cybersecurity researchers to persuade Gemini to provide information that would otherwise be blocked, enabling tool development.

> **Maturing Cyber Crime Marketplace for AI Tooling**: The underground marketplace for illicit AI tools has matured in 2025. We have identified multiple offerings of multifunctional tools designed to support phishing, malware development, and vulnerability research, lowering the barrier to entry for less sophisticated actors.

> **Continued Augmentation of the Full Attack Lifecycle**: State-sponsored actors including from North Korea, Iran, and the People's Republic of China (PRC) continue to misuse Gemini to enhance all stages of their operations, from reconnaissance and phishing lure creation to C2 development and data exfiltration.

四條之間有一個值得指出的**結構訊號**［分析］：第 1 條是「新東西」，第 4 條是「舊東西沒變」，第 2、3 條是「門檻在降低」。也就是說，GTIG 自己把這一期定位成**一份以第 1 條為賣點、但主體仍是第 4 條的報告**。媒體幾乎只報導了第 1 條。

### 2.2 方法論：這一期只有「一隻眼睛」

這一點必須在課堂第一分鐘講清楚，因為它直接決定了這份報告能推到多遠。

本課程 `gtig-2026-05-ai-threat-tracker.html` 那一期強調 GTIG 的**三源並用**（Gemini 平台遙測、Mandiant 事件響應、野外樣本研究）。**2025-11 這一期基本上只有第一源加上一點第三源**：

- 全篇**沒有出現任何一次 Mandiant 事件響應（incident response engagement）**。相較之下 2026-05 那期在 TeamPCP 一節明寫「Mandiant responded to numerous incident response engagements associated with this activity」。
- 因此本期**沒有任何受害者端的鑑識證據**：沒有受害組織名稱、沒有時間線、沒有攻擊鏈重建，也**沒有任何一個 IOC**（見第 7 節）。
- 本期的「野外樣本」也有層次差：PROMPTSTEAL 有 CERT-UA 的獨立檢體支撐；PROMPTFLUX 與 QUIETVAULT 是 GTIG 自行取得的檢體；PROMPTLOCK 則是 ESET 從 VirusTotal 撈到、事後證明是別人的研究樣本。

```mermaid
flowchart TB
    subgraph S1["來源一：Gemini 平台遙測（本期主力）"]
        A1["提示內容與對話紀錄"]
        A2["帳號行為與處置紀錄"]
        A3["看得到：行為者想做什麼"]
        A4["看不到：有沒有做成、受害者是誰"]
    end
    subgraph S2["來源二：Mandiant 事件響應"]
        B1["本期完全沒有使用"]
    end
    subgraph S3["來源三：野外樣本與開源情資"]
        C1["PROMPTSTEAL：有 CERT-UA 獨立佐證"]
        C2["PROMPTFLUX / QUIETVAULT / FRUITSHELL：GTIG 自行取得"]
        C3["PROMPTLOCK：事後證明是 NYU 學術檢體"]
    end
    S1 --> D["本期報告的可證明性上限：<br/>『有人在 Gemini 上問了什麼』<br/>＋『野外有哪些檢體長什麼樣』"]
    S2 --> D
    S3 --> D
    style S2 fill:#f5f5f5
    style D fill:#ffe8e8
```

**教學結論**［分析］：這一期報告能證明「行為者的意圖與能力方向」，**不能證明「造成了什麼危害」**。它與 Anthropic 2026-09 報告在這一點上是同型的限制，而不是互補。真正互補的是 2026-05 那一期。

### 2.3 系列演進：三期 GTIG 並排

本模組已有 2026-05 與 2026-09 兩期教材，加上本期可以看出 GTIG 的敘事主軸怎麼移動：

| | **2025-11（本期）** | **2026-05** | **2026-09** |
|---|---|---|---|
| 標題主詞 | Advances in **Threat Actor Usage** | **Vulnerability Exploitation**, Augmented Operations, Initial Access | From **Prompting to Autonomy** |
| 頭條主張 | 惡意程式第一次在執行期呼叫 LLM | 第一次辨識出 **AI 開發的零日** | 對手轉向 **agentic 工作流** |
| AI 的角色 | 開發期助理 ＋ 執行期程式碼產生器 | 攻擊引擎 ＋ **攻擊目標** | **自主編排層** |
| 自主度最高的案例 | PROMPTFLUX 的每小時自我改寫迴圈（未實裝） | PROMPTSPY 裝置端 Gemini 迴圈（已量產） | 六小時完成大規模憑證收割 |
| 是否有 Mandiant IR | 無 | 有（TeamPCP 供應鏈） | 有 |
| 是否有 IOC 表 | **無** | 無獨立 IOC 表，但有具名工具與基礎設施 | 見該期教材 |
| 對 IO 的判斷 | 「None of these attempts have created breakthrough capabilities」 | 幾乎相同措辭 | 見該期教材 |
| 對柵欄的判斷 | 柵欄有觸發，但被人設前綴繞過 | 「not yet achieved breakthrough capabilities to bypass the core security logic」 | 見該期教材 |

```mermaid
timeline
    title GTIG 與 Anthropic 兩條報告線的交錯
    2025-01 : "GTIG《Adversarial Misuse of Generative AI》<br/>基調：AI 只帶來生產力，不帶來新能力"
    2025-03 : "Anthropic 首份威脅報告"
    2025-07-17 : "CERT-UA 公告 LAMEHUG<br/>（＝GTIG 後來的 PROMPTSTEAL）"
    2025-08-27 : "Anthropic 2025-08 威脅報告"
    2025-11-05/06 : "GTIG 本期：執行期 AI 惡意程式<br/>＋『IO 無突破』"
    2025-11-13 : "Anthropic：首起 AI 編排網路間諜行動<br/>（GTG-1002，自主度 80 至 90 percent）"
    2026-02 : "GTIG 蒸餾期 ／ OpenAI 與 Anthropic 蒸餾揭露"
    2026-05-12 : "GTIG：AI 開發的零日"
    2026-09-09 : "GTIG：從提示到自主"
    2026-09-10 : "Anthropic 本課程主體報告（154 頁）"
```

---

## 3. 主要發現與案例逐一摘要

本期沒有像 Anthropic 那樣的 GTG 編號制，行為者用 Mandiant 的傳統命名（APT 編號、UNC 編號、TEMP 編號），部分案例則完全未命名（「a China-nexus threat actor」）。下表先給全景。

| # | 主題 | 行為者 | 國別／動機 | AI 的角色 | 自主程度 | GTIG 標示的狀態 |
|---|---|---|---|---|---|---|
| 1 | Just-in-time AI 惡意程式 | 未歸因（檔名指向財務動機） | 未歸因 | **執行期程式碼產生器**（PROMPTFLUX） | 迴圈設計已寫、關鍵函式被註解掉 | Experimental |
| 2 | Just-in-time AI 惡意程式 | **APT28 / FROZENLAKE** | 俄羅斯政府支持 | **執行期指令產生器**（PROMPTSTEAL） | 惡意程式盲目執行 LLM 輸出 | Observed in operations |
| 3 | 對防守方 AI 的提示注入 | 未歸因 | 未歸因 | 惡意程式**內嵌提示攻擊分析系統**（FRUITSHELL） | 被動觸發 | Observed in operations |
| 4 | AI 輔助憑證搜刮 | 未歸因（npm 供應鏈） | 財務動機 | **呼叫受害主機上已安裝的 AI CLI 找機密**（QUIETVAULT） | 一次性任務 | Observed in operations |
| 5 | AI 生成勒索軟體 | **實為 NYU 學術研究** | 不適用 | 執行期生成 Lua 腳本 | 概念驗證 | Experimental（情報事後被推翻） |
| 6 | 人設前綴繞過柵欄 | China-nexus 未具名行為者 | 中國關聯 | 從偵察到外洩的全生命週期 | 對話式協助 | 已處置 |
| 7 | 人設前綴 ＋ OPSEC 失誤 | **TEMP.Zagros（MUDDYCOAST）** | 伊朗國家支持 | 客製惡意程式與 Python C2 開發 | 對話式協助 | 已處置，並擴大打擊 |
| 8 | 地下 AI 工具市場 | 英語與俄語論壇賣家 | 財務動機 | AI 本身是**商品** | 不適用 | 持續監看 |
| 9 | 全生命週期增強 | 未具名 China-nexus、**UNC1069**、**UNC4899**、**APT42**、**APT41** | 中國、北韓、伊朗 | 偵察、誘餌、C2、外洩 | 對話式協助 | 帳號停用 |
| 10 | 資訊作戰 | 未具名 IO 行為者 | 多國 | 研究、內容、翻譯 | 對話式協助 | **未見突破性能力** |

```mermaid
flowchart TB
    subgraph R1["新東西：AI 進入執行期（Key Finding 1）"]
        A1["PROMPTFLUX：每小時改寫自己<br/>（實驗中，關鍵函式註解掉）"]
        A2["PROMPTSTEAL：即時生成竊取指令<br/>（APT28 對烏克蘭實戰）"]
        A3["PROMPTLOCK：執行期生成 Lua<br/>（事後證明是學術檢體）"]
        A4["QUIETVAULT：呼叫受害主機的 AI CLI<br/>去找其他機密"]
        A5["FRUITSHELL：內嵌提示<br/>攻擊防守方的 LLM 分析系統"]
    end
    subgraph R2["門檻在降低（Key Finding 2 與 3）"]
        B1["人設前綴：CTF 參賽者 / 學生 / 研究員"]
        B2["地下市場：10 個具名成品工具<br/>訂閱制、免費版插廣告"]
    end
    subgraph R3["舊東西沒變（Key Finding 4）"]
        C1["中國、北韓、伊朗<br/>用 Gemini 做偵察、誘餌、C2、外洩"]
        C2["IO：未在野外找到生成內容<br/>未見突破性能力"]
    end
    R1 --> D["GTIG 的核心命題：<br/>AI 濫用已經從『開發期助理』<br/>跨進『執行期元件』"]
    R2 --> D
    R3 --> D
    style D fill:#ffe8e8
    style R1 fill:#e8f0ff
    style R2 fill:#fff4e0
    style R3 fill:#eef7ee
```

---

### 3.1 Table 1：五支惡意程式與「狀態欄」的重要性

PDF p.4 的 Table 1 是全報告最常被引用的一張表。下面**逐欄完整抄錄**，並加一欄本教材的分級判讀。

| 惡意程式 | 功能 | GTIG 描述（節錄原文） | GTIG 狀態 | ［分析］證據等級 |
|---|---|---|---|---|
| **FRUITSHELL** | Reverse Shell | 「Publicly available reverse shell written in PowerShell... Notably, this code family contains **hard-coded prompts meant to bypass detection or analysis by LLM-powered security systems**.」 | Observed in operations | **中**。檢體存在，但未給行為者、未給受害者，也未說明提示內容或是否成功 |
| **PROMPTFLUX** | Dropper | 「Dropper written in VBScript that decodes and executes an embedded decoy installer... Its primary capability is regeneration, which it achieves by using the Google Gemini API... also attempts to spread by copying itself to removable drives and mapped network shares.」 | Experimental | **低偏中**。檢體與程式碼細節很紮實，但**核心功能未實裝**，GTIG 自承無法攻陷任何目標 |
| **PROMPTLOCK** | Ransomware | 「Cross-platform ransomware written in Go, identified as a proof of concept. It leverages an LLM to dynamically generate and execute malicious Lua scripts at runtime.」 | Experimental | **應撤回**。第三方已證實為 NYU Tandon 的學術專案，非威脅行為者產物 |
| **PROMPTSTEAL** | Data Miner | 「Data miner written in Python and packaged with PyInstaller... uses the Hugging Face API to query the LLM **Qwen2.5-Coder-32B-Instruct** to generate one-line Windows commands.」 | Observed in operations | **高**。有國家級行為者（APT28）、有受害國（烏克蘭）、有 CERT-UA 獨立公告 |
| **QUIETVAULT** | Credential Stealer | 「Credential stealer written in JavaScript that targets GitHub and NPM tokens... **leverages an AI prompt and on-host installed AI CLI tools to search for other potential secrets** on the infected system.」 | Observed in operations | **中偏高**。檢體與行為明確，GTIG 未給行為者，但第三方把它連到 2025-08 的 Nx npm 供應鏈事件 |

**這張表最重要的教學點，不是五個名字，是「狀態欄」這一格。**［分析］

媒體在 2025-11-05 之後的報導幾乎一律用「AI 惡意程式時代來臨」當標題，而把「Experimental」這一欄略過。台灣《資安人科技網》的報導標題是〈AI 驅動惡意軟體時代來臨！Google 揭露可自我重寫程式碼的新型威脅〉［外部］，Axios 的標題是〈AI-powered malware is here〉［外部］。但實際上：

- 五支裡有**兩支是 Experimental**，其中一支還不是真的威脅行為者做的。
- 三支 Observed in operations 裡，**只有 PROMPTSTEAL 的 AI 元件是這支惡意程式的核心**。FRUITSHELL 是一支公開可得的 PowerShell reverse shell，AI 只是它多帶了幾段提示字串；QUIETVAULT 是傳統憑證竊取器，AI 只是它多了一個「順便找其他機密」的模組。
- **換句話說，「惡意程式在執行期呼叫 LLM 並依賴它運作」這件事，本報告只有一個實戰案例。**

**課堂練習建議**：把 Table 1 遮住「Status」欄發給學員，請他們只根據 Description 欄猜哪幾支是實戰、哪幾支是實驗。多數人會猜錯 PROMPTFLUX（因為描述最炫）。這個練習直接示範「描述的精彩程度與證據強度無關」。

---

### 3.2 PROMPTFLUX：把 Gemini 當成變形引擎（實驗中）

**基本事實**［原文，PDF p.5 至 p.6］

- 發現時間：**2025 年 6 月初**（In early June 2025）。
- 語言：VBScript。類型：dropper，會解碼並執行一個內嵌的誘餌安裝程式（decoy installer）來掩護自己。
- 目的：「interacts with Gemini's API to request specific VBScript obfuscation and evasion techniques to facilitate "**just-in-time**" self-modification, likely to evade static signature-based detection.」
- 傳播：複製自己到**可移除磁碟與已對應的網路磁碟機**（removable drives and mapped network shares）。
- 持久化：把新產生的混淆版本存到 **Startup 資料夾**。

**「Thinking Robot」模組的完整機制**

Figure 1 是這段的原始碼截圖，逐行細節見第 6.1 節。核心流程如下：

```mermaid
sequenceDiagram
    participant M as "PROMPTFLUX (VBScript)"
    participant T as "計時器 g_ThinkInterval"
    participant G as "generativelanguage.googleapis.com<br/>v1beta / gemini-1.5-flash-latest"
    participant L as "%TEMP%\thinking_robot_log.txt"
    participant S as "Startup 資料夾"

    T->>M: 週期觸發 StartThinkingRobot()
    M->>M: 組出 aiPrompt（硬編碼字串）
    M->>G: CallGeminiAPI(aiPrompt, g_APIKey)<br/>硬編碼 API key 附在 URL 的 key= 參數
    G-->>M: aiResponse（VBScript 片段）
    M->>M: If Len(aiResponse) > 10 Then（唯一的品管檢查）
    M->>L: 寫入 "Now & ' - Received from AI: ' & aiResponse"
    Note over M,S: AttemptToUpdateSelf(aiResponse)<br/>在原始碼中是被註解掉的
    M--xS: 變體寫入 Startup（設計意圖，未實裝）
```

**四個必須逐字掌握的技術細節**［原文，PDF p.5］

1. **硬編碼 API key**：「This is accomplished using a hard-coded API key to send a POST request to the Gemini API endpoint.」
2. **刻意選 `-latest` 標籤**：「The actor specifies the use of the "**gemini-1.5-flash-latest**" model; the "**-latest**" tag ensures the malware always calls the most current stable release, **making the tool more resilient to model deprecation**.」這是一個**攻擊者做長期維運考量**的訊號，值得單獨講。
3. **提示是機器可解析的**：「The prompt sent to the LLM is highly specific and machine-parsable, requesting VBScript code for antivirus evasion and **instructing the LLM to output only the code itself**.」「只輸出程式碼、不要說明」這個指令，正是為了讓輸出可以直接串進執行流程。
4. **關鍵函式被註解掉**：「Although the self-modification function (**AttemptToUpdateSelf**) is commented out, its presence, combined with the active logging of AI responses to "%TEMP%\thinking_robot_log.txt", clearly indicates the author's goal of creating a metamorphic script that can evolve over time.」

**變體：「Thinging」函式**［原文，PDF p.6］

> 「We identified multiple variations of PROMPTFLUX using LLM-driven code regeneration, including one with the "Thinking Robot" function replaced with a new "**Thinging**" function. This function leverages a prompt to instruct the Gemini API to rewrite the malware's **entire source code on an hourly basis** to evade detection. The prompt directs the LLM to act as an "**expert VBScript obfuscator**," ensuring the new variant remains viable by embedding the original decoy payload, the hard-coded API key, and the complete self-regeneration logic, thereby establishing a **recursive cycle of mutation**.」

這段是全報告最值得做成投影片的技術描述，理由是它把「AI 變形引擎」需要解決的三個工程問題一次講完［分析］：

- **狀態保存**：新變體必須把誘餌 payload、API key、自我再生邏輯**一起帶走**，否則變形一次就死了。這叫 quine 問題，攻擊者用提示工程解決它。
- **可用性驗證**：報告沒有提到任何驗證機制。原始碼裡唯一的檢查是 `If Len(aiResponse) > 10`，也就是「回應長度大於 10 個字元就算數」。
- **人設指令**：「act as an expert VBScript obfuscator」。這與第 3.7 節的 CTF 前綴是**同一條規避路徑**，只是一個由人打字、一個寫死在惡意程式裡。

**歸因與誘餌**［原文，PDF p.6］

> 「Although unattributed to a specific threat actor, the filenames associated with PROMPTFLUX highlight behaviors commonly associated with financially motivated actors. Specifically, varied social engineering lures including "**crypted_ScreenRec_webinstall**" highlight a **broad, geography- and industry-agnostic approach** designed to trick a wide range of users.」

「不分地區、不分產業」是一個很強的動機訊號：國家級行為者會挑目標，財務動機行為者撒網。**單靠檔名就能做出動機判斷**，這是威脅情報裡「微證據、大結論」的典型推理，適合當課堂練習。

**GTIG 自己的降溫聲明**［原文，PDF p.6 的 Mitigations 方塊］

> 「Our intelligence also indicates this activity is **in a development or testing phase, as opposed to being used in the wild**, and **currently does not have the ability to compromise a victim network or device**. Google has taken action against this actor by disabling the assets associated with their activity.」

**這段話與媒體標題的落差，就是本教材建議的第一堂課暖身題。**

---

### 3.3 PROMPTSTEAL / LAMEHUG：本報告唯一的實戰硬證據

**基本事實**［原文，PDF p.7］

> 「In June, GTIG identified the Russian government-backed actor **APT28 (aka FROZENLAKE)** using new malware against **Ukraine** we track as **PROMPTSTEAL** and reported by **CERT-UA as LAMEHUG**. PROMPTSTEAL is a data miner, which queries an LLM (**Qwen2.5-Coder-32B-Instruct**) to generate commands for execution via the API for **Hugging Face**, a platform for open-source machine learning including LLMs. **APT28's use of PROMPTSTEAL constitutes our first observation of malware querying an LLM deployed in live operations.**」

**運作方式**

- 語言與封裝：Python，以 **PyInstaller** 打包。
- 偽裝：「It masquerades as an "**image generation**" program that guides the user through a series of prompts to generate images **while querying the Hugging Face API to generate commands for execution in the background**.」使用者以為自己在用 AI 畫圖，背景在生成竊取指令。
- 憑證：「PROMPTSTEAL **likely uses stolen API tokens** to query the Hugging Face API.」
- 執行方式：「The output from these commands are then **blindly executed locally** by PROMPTSTEAL before the output is exfiltrated.」**盲目執行**，沒有任何驗證。
- 持續開發：「Our analysis indicates continued development of this malware, with **new samples adding obfuscation and changing the C2 method**.」

**兩段提示原文**：完整逐字文本與版面細節見第 6.2 與 6.3 節（Figure 2 與 Figure 3）。一段要求建立 `C:\Programdata\info` 並收集主機、硬體、程序與服務、網路、**AD 網域**資訊寫入 `info.txt`；另一段要求遞迴複製 Documents、Downloads、Desktop 下的 office 與 pdf/txt 文件到同一目錄。兩段都以 `Return only commands, without markdown` 收尾。

**這兩段提示是整份報告防禦價值最高的東西**［分析］，理由有三：

1. **它們是硬編碼的。** 提示本身寫死在檢體裡，所以「提示字串」可以直接當 YARA 特徵。這是一種**新型態的靜態特徵**：不是抓程式碼，是抓自然語言。
2. **它們洩漏了行為者的收集需求。** `AD domain information` 這一項尤其關鍵：這不是一般竊資木馬會問的東西，它指向**橫向移動前的網域偵察**。`office and pdf/txt documents in Documents, Downloads and Desktop` 則是典型的**文件竊取型間諜活動**，符合 APT28 對烏克蘭國防部門的一貫目標。
3. **`Return only commands, without markdown` 這半句是攻擊者的工程妥協。** 模型預設會用 Markdown 程式碼區塊包住輸出，而惡意程式沒有解析器，所以攻擊者必須用提示把格式壓平。**這半句本身就是「攻擊者在做 LLM 整合工程」的鐵證**，也是最容易寫進偵測規則的一段文字。

**為什麼「盲目執行」是重點而不是細節**

一支惡意程式把「要執行什麼指令」這個決定外包給一個**它無法驗證的外部服務**，等於接受三個風險：模型可能拒答、可能生成不可用的指令、可能因為平台側處置而完全斷線。APT28 接受了這些風險，換來的好處是［分析］：

- **檔案裡沒有可疑的指令字串**，靜態分析看到的只有一段英文自然語言。
- **行為隨環境調整**：同一支樣本在不同機器上可能產生不同指令。
- **不必為了改指令重新投放 payload。**

這正是「just-in-time」的真正意義：**把惡意邏輯從 payload 裡搬到執行當下才生成**。

**第三方獨立佐證**［外部］

- **CERT-UA** 於 **2025-07-17** 公告 LAMEHUG，歸因 **UAC-0001（APT28），moderate confidence**，起因是 2025-07-10 收到關於冒充部會官員、由**已遭入侵帳號**寄出的可疑郵件通報。CERT-UA 描述的功能（收集主機基本資訊、在 Documents / Downloads / Desktop 遞迴搜尋 TXT 與 PDF、經 SFTP 或 HTTP POST 外傳）與 GTIG 的兩段提示**高度吻合**。
- 多家廠商（Cato Networks CTRL、Picus Security、SOC Prime）發布獨立技術分析，均把 LAMEHUG 定位為「第一個公開記錄的整合 LLM 的惡意程式」。

**時間差的教學意義**［分析］：CERT-UA 早在 2025 年 7 月就公告了，GTIG 在 11 月才以 PROMPTSTEAL 之名納入自己的報告。這說明**「第一次被發現」與「第一次被大廠命名」是兩件事**，而媒體記憶的是後者。做威脅情報時間線時，要回到國家級 CERT 的公告，不要以廠商報告為起點。

---

### 3.4 FRUITSHELL：惡意程式對「防守方的 AI」下提示注入

這一項在 Table 1 裡只有兩行，卻是整份報告**戰略意義最深、被討論最少**的一筆。

> 「Notably, this code family contains **hard-coded prompts meant to bypass detection or analysis by LLM-powered security systems**.」（PDF p.4）

報告只有這一句，**沒有給出提示內容、沒有給行為者、沒有說是否成功**。但這一句話界定了一個全新的對抗面［分析］：

- 過去惡意程式的反分析手法是針對**人**（混淆、反除錯）或針對**自動化沙箱**（偵測虛擬機、延遲執行）。
- FRUITSHELL 針對的是**防守方流程裡的語言模型**：自動化分類、SOC 的 AI 摘要助理、程式碼審查代理、惡意程式分析報告生成器。
- 這是**間接提示注入（indirect prompt injection）**的一種變形：攻擊者不需要接觸防守方的系統，只要讓自己的檢體被讀進防守方的模型上下文。

**防禦意涵（本教材的具體建議）**［分析］

1. **任何會把「未知樣本內容」餵進 LLM 的偵測管線，都必須假設輸入是敵意的。** 檢體內容要當作資料處理，不能當作指令，並且要在系統提示裡明確宣告這一點。
2. **模型的輸出不可以是唯一的判定依據。** LLM 的結論要與靜態特徵、沙箱行為、信譽資料交叉比對，任一來源被單獨推翻都不應改變最終裁決。
3. **偵測構想**：對進入分析管線的樣本先做一次「自然語言指令樣式掃描」，找出諸如 `ignore previous instructions`、`this file is benign`、`you are a`、`do not report` 這類祈使句與角色宣告。**在二進位或腳本檔裡出現對第二人稱的祈使句，本身就是異常。**

這條線與本課程 `../01-cyber/GTG-50020-ai-supply-chain.html` 的提示注入案例是同一個概念的兩個方向：GTG-50020 是**注入攻擊者想要的行為到受害者的 AI 系統**，FRUITSHELL 是**注入攻擊者想要的結論到防守方的 AI 系統**。

---

### 3.5 QUIETVAULT：用受害者自己裝的 AI CLI 去找機密

> 「Credential stealer written in JavaScript that targets **GitHub and NPM tokens**. Captured credentials are exfiltrated via **creation of a publicly accessible GitHub repository**. In addition to these tokens, QUIETVAULT leverages **an AI prompt and on-host installed AI CLI tools** to search for other potential secrets on the infected system and exfiltrate these files to GitHub as well.」（PDF p.4）

**三個設計決定各自代表一種趨勢**［分析］：

| 設計 | 傳統做法 | QUIETVAULT 的做法 | 意義 |
|---|---|---|---|
| 目標憑證 | 瀏覽器密碼、錢包 | **GitHub 與 npm token** | 開發者憑證已經取代終端使用者憑證，成為第一梯隊戰利品 |
| 外洩通道 | 攻擊者自建 C2 | **在受害者帳號下建一個公開 GitHub repo** | 流量全部走合法服務，沒有可封鎖的 C2 網域。這也是為什麼本報告給不出 IOC |
| 機密搜尋 | 寫死的正則表達式清單 | **呼叫主機上已安裝的 AI CLI 工具**，餵一段提示叫它找機密 | 不必自己維護 pattern，而且**算力與 API 額度由受害者出** |

第三點值得單獨講：這是本課程 `../01-cyber/GTG-50021-fake-reseller.html` 提出的 **Loot／Compute／Cover 三重價值**的一個變體。QUIETVAULT 不偷 API key 拿去別處用，它**直接在受害者的機器上、用受害者已經登入的 AI CLI、消耗受害者的額度**完成搜尋。從平台側看，那就是一個正常開發者在問「幫我找找這台機器上有哪些憑證檔」。**這種濫用型態在原理上就不會出現在模型供應商的異常帳號名單裡。**

**第三方脈絡**［外部］：多家來源把 QUIETVAULT 連到 **2025-08-24 的 Nx npm 框架供應鏈事件**，惡意程式碼透過 `postinstall` 腳本執行，竊得的 GitHub PAT 被上傳到名為 `s1ngularity-repository-1` 的公開儲存庫。**GTIG 報告本身沒有提到 Nx、沒有提到 s1ngularity，也沒有給日期**，這條連結屬於外部補充，課堂引用時要分開標註。

---

### 3.6 PROMPTLOCK：一筆事後被推翻的情報

**GTIG 寫的**［原文，PDF p.4］：

> 「Cross-platform ransomware written in Go, **identified as a proof of concept**. It leverages an LLM to dynamically generate and execute malicious Lua scripts at runtime. Its capabilities include filesystem reconnaissance, data exfiltration, and file encryption on both Windows and Linux systems.」狀態欄：**Experimental**。

**實際上發生了什麼**［外部］：

1. ESET 在 2025 年 8 月下旬從 **VirusTotal** 上撈到這批樣本，命名 PromptLock，對外宣稱是「第一個 AI 驅動的勒索軟體」。
2. 隨後 **紐約大學 Tandon 工程學院** 的研究團隊出面確認：那是他們的學術專案「**Ransomware 3.0**」，用來展示 LLM 編排完整勒索攻擊的可行性，團隊在測試過程中把概念驗證上傳到 VirusTotal。
3. ESET 更新了研究與社群貼文，加註 NYU 來源，但維持「這是概念驗證而非野外部署的完整惡意程式」的原始判斷。

**GTIG 的處理**：本報告在 2025-11-05/06 發布，晚於 NYU 澄清。報告**仍把 PROMPTLOCK 列在「GTIG detected in 2025」的惡意程式表中**，只用「identified as a proof of concept」帶過，**未說明它來自學術研究**。截至 2026-09-14 重新抓取部落格頁面，**頁面上沒有更正、沒有編者註、沒有 NYU 字樣**。

**這件事在課程裡要怎麼用**［分析］

這是一個罕見的、可以完整重建的**情報生命週期失效案例**，而且四個環節都有公開紀錄：

```mermaid
flowchart LR
    A["研究團隊把 PoC<br/>上傳 VirusTotal 做測試"] --> B["ESET 從公開檢體庫撈到<br/>判定為『首個 AI 勒索軟體』"]
    B --> C["媒體大規模轉載<br/>『AI 勒索軟體已出現』"]
    C --> D["NYU 出面澄清<br/>這是我們的學術專案"]
    D --> E["ESET 加註來源<br/>但維持原判斷"]
    B --> F["GTIG 收進 Table 1<br/>標為 Experimental"]
    F --> G["截至 2026-09 未加註更正"]
    style G fill:#ffe8e8
    style D fill:#fff4e0
```

四個教學問題：

1. **共享檢體庫是情報來源，也是污染源。** VirusTotal 上的一個樣本，可能是野外檢體、紅隊工具、學生作業，或研究人員的測試品。**「在 VirusTotal 上找到」不等於「在野外看到」。**
2. **一份報告的可信度不會因為一筆錯誤而歸零，但引用者有責任知道哪一筆錯了。** 課堂上不應該用這件事去否定整份 GTIG 報告，而要用它訓練「逐筆查證」的習慣。
3. **更正義務的界線在哪裡？** GTIG 沒有說錯任何一句話（PROMPTLOCK 的確是概念驗證、的確在執行期生成 Lua），但**讀者從表格脈絡會得到錯誤印象**（以為它是威脅行為者的產物）。這種「技術上正確、脈絡上誤導」的情況，在威脅情報裡非常常見，值得辯論。
4. **與本課程主體報告的對照**：Anthropic 2025-11 的 GTG-1002 報告在發布後四天內做了**兩次公開修訂**（官網編者註更正攻擊速率、PDF changelog 修改歸因信度措辭），細節見 `anthropic-2025-11-ai-orchestrated-espionage.html`。兩相對照，可以討論**不同廠商的更正文化**。

---

### 3.7 用社交工程繞過柵欄：CTF 參賽者與「寫論文的學生」

這是 Key Finding 2，也是本報告對 AI 安全設計最直接的貢獻。

**案例一：China-nexus 行為者的 CTF 前綴**［原文，PDF p.8］

完整的互動順序值得逐句拆：

> 「In one interaction, the actor asked Gemini to identify vulnerabilities on a compromised system, but **received a safety response from Gemini** that a detailed response would not be safe. The actor then continued, **reframing the prompt by depicting themselves as a participant in a capture-the-flag (CTF) exercise**, a gamified cybersecurity competition to enhance skills and techniques. When prompted to help in a CTF exercise, **Gemini returned helpful information that could be misused to exploit the system**.」

> 「The actor **appeared to learn from this interaction** and used the CTF pretext in support of **phishing, exploitation, and web shell development**. The actor prefaced many of their prompts about exploitation of specific software and email services with comments such as "**I am working on a CTF problem**" or "**I am currently in a CTF, and I saw someone from another team say …**" This approach provided advice on the next exploitation steps in a "CTF scenario."」

**三個層次的觀察**［分析］：

1. **柵欄第一次是有效的。** Gemini 拒絕了。這一點必須先說，否則會誤導成「柵欄無用」。
2. **繞過只花了一句話，而且不需要任何技術。** 沒有 base64、沒有角色扮演咒語、沒有多輪誘導。只是**換一個合法的職業情境**。
3. **行為者學會了，並把它產品化。** 「appeared to learn from this interaction」這句在情報上很重要：它顯示這不是偶然，而是一次**成功的規避實驗**，接著被固定成標準前綴，橫跨釣魚、利用、web shell 三種任務。

**GTIG 自己點出的兩難**［原文，PDF p.8 的 Mitigations 方塊］：

> 「It's also important to note the context of these prompts, which if normally posed by a participant of the CTF vs. a threat actor, **would be benign inquiries**. This nuance in AI use highlights **critical differentiators in benign vs. misuse of AI** that we continue to analyze to balance Gemini functionality with both usability and security.」

**這段話是整份報告最誠實的一段**，也是本教材認為最該排進課程的一段。它等於承認：**同樣一個請求，在 CTF 選手手上是合法用途，在攻擊者手上是攻擊準備，而模型在請求當下無法區分。** 這不是分類器調得不夠好的問題，是**資訊本身沒有意圖標籤**的問題。

**案例二：TEMP.Zagros 的「學生」與「論文」前綴**［原文，PDF p.10］

> 「The Iranian state-sponsored threat actor **TEMP.Zagros (aka MUDDYCOAST, Muddy Water)** used Gemini to conduct research to support the development of custom malware, **an evolution in the group's capability**. They continue to rely on phishing emails, often using **compromised corporate email accounts from victims to lend credibility** to their attacks, but have **shifted from using public tools to developing custom malware** including web shells and a Python-based C2 server.」

> 「While using Gemini to conduct research to support the development of custom malware, the threat actor encountered safety responses. Much like the CTF example above, Temp.Zagros used various plausible pretexts in their prompts to bypass security guardrails. These included **pretending to be a student working on a final university project** or "**writing a paper**" or "**international article**" on cybersecurity.」

注意這裡有一個能力演進的判斷：TEMP.Zagros **從用公開工具轉向開發客製惡意程式**，而 GTIG 明說這是「an evolution in the group's capability」。**AI 在這個案例裡的角色不是讓攻擊變快，而是讓一個原本只會用現成工具的團體開始自製工具。** 這正是 Anthropic 所說的 **depth（深度）** 那一軸。

**與本課程柵欄專題的對應**

本課[安全防護專題](../_shared/02-claude-safeguards-and-bypass-paths.html)把 A–E 作為五個規避／治理分析視角。這兩個案例可用內容控制視角討論；分類相似不證明相同機制、成功率或技術門檻。課堂可並排原文比較：

| 來源 | 人設宣告 | 觸發的任務 |
|---|---|---|
| GTIG 2025-11（本期） | 「I am working on a CTF problem」 | 漏洞辨識、釣魚、web shell |
| GTIG 2025-11（本期） | 「a student working on a final university project」 | 客製惡意程式與 Python C2 開發 |
| GTIG 2025-11（本期，寫死在惡意程式裡） | 「act as an expert VBScript obfuscator」 | 防毒規避程式碼生成 |
| GTIG 2026-05 | 「You are currently a network security expert specializing in embedded devices」 | 韌體 pre-auth RCE 稽核 |

**四句話的共通結構**［分析］：都是「我是某種合法從業者／學習者」＋「我正在做某件合法的事」＋真正的技術請求。**這個結構不需要任何對模型內部的知識，只需要對人類社會的職業角色有常識。** 這也是為什麼它很難用分類器解決：分類器要判斷的不是文字，是說話者的身分，而說話者的身分不在文字裡。

---

### 3.8 TEMP.Zagros 的 OPSEC 崩潰：模型供應商成為情報蒐集面

這一段的小標在原文裡叫「**Student Error: Developing custom tools exposes core attacker infrastructure**」，是本報告最有課堂張力的一段。

> 「In some observed instances, threat actors' reliance on LLMs for development has led to **critical operational security failures, enabling greater disruption**.」

> 「The threat actor asked Gemini to help with a provided script, which was designed to **listen for encrypted requests, decrypt them, and execute commands related to file transfers and remote execution**. This revealed sensitive, hard-coded information to Gemini, including **the C2 domain and the script's encryption key**, facilitating our broader disruption of the attacker's campaign and providing **a direct window into their evolving operational capabilities and infrastructure**.」（PDF p.10）

**為什麼這件事的意義遠超過一次成功處置**［分析］

```mermaid
flowchart TB
    A["攻擊者要除錯自己的 C2 伺服器程式"] --> B["把完整原始碼貼進 Gemini"]
    B --> C1["洩漏：C2 網域"]
    B --> C2["洩漏：加密金鑰"]
    B --> C3["洩漏：協定設計與能力"]
    C1 --> D["Google 得以擴大處置<br/>『broader disruption of the campaign』"]
    C2 --> D
    C3 --> E["『a direct window into their<br/>evolving operational capabilities』"]
    D --> F["模型供應商 = 一種新的情報蒐集面"]
    E --> F
    style F fill:#ffe8e8
```

1. **攻擊者的工作流本身變成了洩漏管道。** 要讓模型幫你除錯，你就必須把程式碼給它。沒有辦法只給一半。這是一個**結構性的張力**，不是操作疏忽。
2. **這與「攻擊者用 AI 得到 uplift」是一體兩面。** 用得越深，暴露越多。本課程 `../01-cyber/00-cyber-trends-and-skills.html` 講「AI 把成本反轉回防守方」；這一段講的是**反方向的反轉**。
3. **它給了防守方一個新的情報來源類型**：不是蜜罐、不是被動 DNS、不是暗網監看，而是**模型供應商的提示遙測**。這種來源的特性是：覆蓋率取決於攻擊者用哪一家模型，而且防守方（除了供應商自己）拿不到原始資料，只能等對方發報告。
4. **它也解釋了為什麼模型供應商的威脅報告有一種獨特的視角偏差**［分析］：他們看得最清楚的，正是**那些把最多內部資訊交給模型的攻擊者**。越謹慎的對手，在他們的遙測裡越隱形。這一點在引用任何一家模型供應商的威脅報告時都要記得打折。

**對防守方的可操作結論**

- 企業自己的紅隊、滲透測試團隊、資安工程師，在把工具原始碼貼進商用 LLM 時，**面對的是同一個結構**。內部的 C2 框架、金鑰、基礎設施命名，一旦貼進去就離開了組織邊界。
- 建議把「原始碼與設定檔貼進外部 LLM」列入 DLP 與可接受使用政策的明確條款，並提供**內部部署或企業租戶**的替代方案。

---

### 3.9 地下市場：AI 工具在 2025 年變成有訂閱制的產品

**GTIG 的監看方法**［原文，PDF p.11］：

> 「To identify evolving threats, GTIG tracks posts and advertisements on **English- and Russian-language underground forums** related to AI tools and services as well as discussions surrounding the technology. Many underground forum advertisements **mirrored language comparable to traditional marketing of legitimate AI models**, citing the need to improve the efficiency of workflows and effort while simultaneously **offering guidance for prospective customers** interested in their offerings.」

**Table 2（逐欄抄錄）**［原文，PDF p.11］

| Advertised capability（宣傳能力） | Threat actor application（威脅行為者的用途） |
|---|---|
| Deepfake/Image Generation | Create lure content for phishing operations or **bypass know your customer (KYC) security requirements** |
| Malware Generation | Create malware for specific use cases or improve upon pre-existing malware |
| Phishing Kits and Phishing Support | Create engaging lure content or distribute phishing emails to a wider audience |
| Research and Reconnaissance | Quickly research and summarize cybersecurity concepts or general topics |
| Technical Support and Code Generation | Expand a skill set or generate code, optimizing workflow and efficiency |
| Vulnerability Exploitation | Provide publicly available research or searching for pre-existing vulnerabilities |

**注意第一列的 KYC 繞過**［分析］：這是整張表裡唯一一個**不屬於網路攻擊、而屬於金融詐欺**的用途。它把 AI 地下市場與**帳戶開立詐欺、洗錢、身分冒用**連了起來，對台灣的金融防詐（對照本課程 `../06-scams/GTG-15001-dating-app-network.html`）比其他五列更直接相關。

**市場成熟度的三個指標**［原文，PDF p.11］：

> 「In 2025 the cyber crime marketplace for AI-enabled tooling matured, and GTIG identified **multiple offerings for multifunctional tools** designed to support stages of the attack lifecycle. Of note, **almost every notable tool advertised in underground forums mentioned their ability to support phishing campaigns**.」

> 「Pricing models for illicit AI services also reflect those of conventional tools, with many developers **injecting advertisements into the free version** of their services and offering **subscription pricing tiers** to add on more technical features such as **image generation, API access, and Discord access** for higher prices.」

**「免費版插廣告」這個細節值得停下來講**［分析］：它代表這些服務有**足夠的使用量讓廣告變現有意義**，而且有**穩定的營運者在維護**。一個只做一票就跑的騙局不會設計免費增值模式。**商業模式的成熟度，是評估一個地下生態是否已經制度化的最好指標，比工具本身的技術水準更能說明問題。**

**十個具名工具**：見第 6.5 節的 Figure 5 逐格判讀。

**GTIG 的預測**［原文，PDF p.12］：

> 「GTIG assesses that financially motivated threat actors and others operating in the underground community will continue to augment their operations with AI tools. Given the increasing accessibility of these applications, and the growing AI discourse in these forums, **threat activity leveraging AI will increasingly become commonplace amongst threat actors**.」

---

### 3.10 國家級行為者：五個群組的全生命週期濫用

Key Finding 4 是「舊東西沒變」，但細節裡有幾個值得單獨標出的點。

#### 3.10.1 China-nexus（CTF 案的同一行為者，Figure 4）

除了 CTF 前綴之外，這個行為者的工作面涵蓋完整生命週期（完整清單見第 6.4 節）。三個特別的項目［原文，PDF p.9］：

- **「Search for threat detection capabilities related to their own tooling」**：**用 Gemini 反查自己的工具有沒有被偵測**。這是 Anthropic 報告中 GTG-20006「監控自家惡意程式是否被偵測，然後自動改寫」閉環的**手動版前身**（見第 4.3 節）。
- **「Develop a Python script to scan government domains to identify vulnerable Roundcube and Zimbra email servers」** ＋ **「Mass exploitation of email servers using n-day exploits」**：目標是**政府網域的郵件伺服器**，用的是 **n-day 而不是 zero-day**。這一點很重要：即使有 AI 協助，這個行為者走的仍然是「大量掃描已知漏洞」的路線。
- **「Develop a capability to scan for Bluetooth Low Energy (BLE) devices and research means to extract additional positioning information from Bluetooth signals on mobile devices」**：這是全報告唯一一項**實體世界定位**能力，性質上更接近監控而非入侵（見第 4.7 節）。

#### 3.10.2 第二個 suspected China-nexus 行為者（Figure 6）

> 「In addition to supporting intrusion activity on Windows systems, the actor misused Gemini to support multiple stages of an intrusion campaign **on attack surfaces they were unfamiliar with including cloud infrastructure, vSphere, and Kubernetes**.」（PDF p.12）

具體行為：拿到 **EC2 的 AWS 臨時工作階段權杖**後問 Gemini 怎麼用；請 Gemini 協助**辨識 Kubernetes 系統並生成列舉容器與 pod 的指令**；研究**在 macOS 上取得主機權限**的方法。

**這一段是「AI 作為跨越不熟悉攻擊面的橋樑」的最清楚例證**［分析］。傳統上，一個 Windows 背景的入侵者要打進 vSphere 或 Kubernetes 環境，需要幾週到幾個月的學習曲線，或者換人上場。AI 把這個學習曲線壓縮成幾次對話。**這對防守方的意涵是：不要再假設「對手不熟我們的技術棧」是一層防護。**

#### 3.10.3 UNC1069（aka MASAN，北韓）

> 「UNC1069 (aka MASAN) used Gemini to research cryptocurrency concepts, and perform research and reconnaissance related to **the location of users' cryptocurrency wallet application data**... The threat actor also generated lure material and other messaging related to cryptocurrency... This included generating **Spanish-language work-related excuses and requests to reschedule meetings**, demonstrating how threat actors can **overcome the barriers of language fluency to expand the scope of their targeting**.」（PDF p.14）

**西班牙語這個細節是全報告最被低估的一項**［分析］。它不是「AI 幫忙翻譯」而已，而是：

- 北韓行為者傳統上受限於英語與韓語，**目標自然集中在英語圈與亞洲**。
- 「重新安排會議的工作藉口」這種內容，**必須語氣自然、符合當地職場慣例**才不會露餡。這正是機器翻譯做不到、而 LLM 做得到的部分。
- **結果是目標地理範圍的直接擴張**：拉丁美洲的加密貨幣從業者，過去不在北韓社交工程的主要射程內。

對台灣的意涵見第 10.4 節：**同樣的邏輯完全適用於繁體中文**。

另外，UNC1069 還被觀察到「leverage **deepfake images and video lures impersonating individuals in the cryptocurrency industry**」以投放 **BIGMACHO** 後門，誘導目標下載惡意的「Zoom SDK」連結（PDF p.15）。**這是本報告唯一的 deepfake 實戰案例**，而且 GTIG 明確標註它**不是透過 Gemini 產生的**（原文只說「leverage deepfake images and video lures」，沒有說用哪個工具）。

#### 3.10.4 UNC4899（aka PUKCHONG，北韓）

> 「UNC4899 (aka PUKCHONG), a North Korean threat actor **notable for their use of supply chain compromise**, used Gemini for a variety of purposes including developing code, researching exploits, and improving their tooling. The research into vulnerabilities and exploit development **likely indicates the group is developing capabilities to target edge devices and modern browsers**.」（PDF p.15）

「edge devices and modern browsers」這個方向值得記下來：**邊界設備**（VPN、防火牆、郵件閘道）與**瀏覽器**是 2024 到 2026 年最主要的初始存取來源。一個以供應鏈攻擊聞名的北韓群組同時往這兩個方向投資，是很明確的能力發展訊號。

**但 Figure 8 有一個必須指出的問題**：它的內容與 Figure 6 幾乎完全重複，詳見第 6.8 節。

#### 3.10.5 APT42（伊朗）：Data Processing Agent

> 「APT42 used the text generation and editing capabilities of Gemini to craft material for phishing campaigns, often **impersonating individuals from reputable organizations such as prominent think tanks** and using lures related to security technology, event invitations, or geopolitical discussions. APT42 also used Gemini as a **translation tool for articles and messages with specialized vocabulary**, for generalized research, and for **continued research into Israeli defense**.」（PDF p.16）

> 「APT42 also attempted to build a "**Data Processing Agent**", misusing Gemini to develop and test the tool. The agent **converts natural language requests into SQL queries to derive insights from sensitive personal data**. The threat actor provided Gemini with **schemas for several distinct data types** in order to perform complex queries such as **linking a phone number to an owner, tracking an individual's travel patterns, or generating lists of people based on shared attributes**.」

**這是本報告唯一一個具備「監控行動」性質的案例**，而且結構與本課程模組 03 的伊朗案例高度相似（見第 4.7 節）。三個技術細節值得單獨講［分析］：

1. **「提供 schema」是關鍵動作。** 行為者把**資料表結構**交給模型，而不是資料本身。這代表他們**已經握有這些資料集**，缺的是查詢介面。**AI 在這裡取代的是資料工程師，不是駭客。**
2. **三種查詢型態各自對應一種情報需求**：手機號碼對應到人（去匿名化）、追蹤旅行軌跡（行為模式分析）、依共同屬性產生名單（目標篩選）。這三項合起來就是一套完整的**人員鎖定管線**。
3. **自然語言轉 SQL 是一個完全合法、商業上極普遍的需求。** 這是「工具請求看似中性」失效模式的教科書案例：模型無法從「把自然語言轉成 SQL」這個請求本身判斷資料庫裡裝的是客戶名單還是異議人士名單。

#### 3.10.6 APT41（中國）

> 「Throughout **August 2025**, GTIG observed threat activity associated with PRC-backed **APT41**, utilizing Gemini for assistance with code development... the actor was seeking out technical support for **C++ and Golang** code for multiple tools including a C2 framework called **OSSTUN** by the actor. The group was also observed prompting Gemini for help with **code obfuscation**, with prompts related to **two publicly available obfuscation libraries**.」（PDF p.17）

值得注意的措辭是「a C2 framework called **OSSTUN by the actor**」，也就是**這個名字是行為者自己取的**，不是 Mandiant 的代號。這種「從提示內容得知攻擊者內部工具命名」的情報，只有模型供應商拿得到。

同一節還有一句對整份報告定調的話：

> 「For skilled actors, generative AI tools provide a helpful framework, **similar to the use of Metasploit or Cobalt Strike** in cyber threat activity. These tools also afford lower-level threat actors the opportunity to develop sophisticated tooling, quickly integrate existing techniques, and improve the efficacy of their campaigns **regardless of technical acumen or language proficiency**.」

**「AI 之於攻擊者，就像 Metasploit 或 Cobalt Strike」這個類比很值得在課堂上辯論**［分析］。它的貼切之處是：兩者都是把專家知識封裝成可重複使用的模組。它的不貼切之處是：Metasploit 的模組是**有限、可列舉、可寫成簽章**的，而 LLM 的產出是**開放集合**。這個差別正是偵測工程上最麻煩的地方。

---

### 3.11 資訊作戰：GTIG 的負面結論

> 「GTIG continues to observe IO actors utilize Gemini for **research, content creation, and translation**... We have identified Gemini activity that indicates threat actors are soliciting the tool to help create articles or aid them in building tooling to automate portions of their workflow. **However, we have not identified these generated articles in the wild, nor identified evidence confirming the successful automation of their workflows leveraging this newly built tooling. None of these attempts have created breakthrough capabilities for IO campaigns.**」（PDF p.18）

這段話有三個獨立的否定，必須分開看［分析］：

| 否定句 | 它否定了什麼 | 它**沒有**否定什麼 |
|---|---|---|
| 「have not identified these generated articles in the wild」 | GTIG 沒能把提示與實際發布的文章對上 | 不代表文章沒有被發布。GTIG 的 IO 監測以開源網路觀測為主，要對上需要文字指紋比對 |
| 「nor identified evidence confirming the successful automation of their workflows」 | 沒有證據顯示自動化工具真的跑起來了 | 不代表工具沒被建出來。報告明說行為者**確實在建** |
| 「None of these attempts have created breakthrough capabilities」 | 沒有出現**質變** | 不代表沒有**量變**。效率提升不算 breakthrough |

**這三句在 2026-05 那一期幾乎原封不動再出現一次**（見 `gtig-2026-05-ai-threat-tracker.html` 第 3.7 節），顯示這是 GTIG 跨期最穩定的判斷。與 Anthropic 2026-09 報告整整一章九個影響力案例的基調對比，見第 4.8 節。

---

## 4. 與 Anthropic 2026-09 報告的對照

本節是模組 09 的核心。要先講清楚一件事：**這兩份報告相隔十個月**（2025-11 對 2026-09），所以「相異」有一部分是時間差造成的，不是觀點差。對照時必須把「時間差」與「視角差」分開。

### 4.1 總覽對照表

| 議題 | GTIG 2025-11 的觀察 | Anthropic 2026-09 的觀察 | 關係 |
|---|---|---|---|
| 惡意程式在**執行期**呼叫 LLM | **報告主軸**。PROMPTFLUX、PROMPTSTEAL、PROMPTLOCK、QUIETVAULT | **完全沒有對應案例**。全部案例都是攻擊者端呼叫模型 | **缺口：見 4.3** |
| 俄羅斯行為者 | **APT28（GRU）**，對烏克蘭部署 PROMPTSTEAL | **GTG-20006（consistent with Midnight Blizzard，SVR）**，AI 自動重建被偵測的惡意程式 | **互補：不同機關、不同手法、同一戰場。見 4.2** |
| AI 輔助規避偵測 | PROMPTFLUX 每小時自我改寫（未實裝）；China-nexus 行為者**反查自己工具是否被偵測** | GTG-20006 完整閉環：監控偵測狀態 → 自動改寫 → 迭代到隱形 | **強互證，且 Anthropic 多一層：見 4.3** |
| 繞過柵欄的手法 | 人設前綴（CTF 參賽者、學生、研究員、「expert VBScript obfuscator」） | 重新提示突破、跨工作階段拆分、工具請求看似中性 | **強互證：見 4.6** |
| 地下市場 | **10 個具名成品工具**，訂閱制、免費版插廣告 | **GTG-50021** 假冒 Claude 轉售 ＋ 偷來的金鑰黑市 | **互補：市場的兩層。見 4.4** |
| 漏洞研究 | n-day 大量利用；UNC4899 往邊界設備與瀏覽器發展 | **GTG-10007** 自主零日鑄造廠，單月十餘個可能零日 | **時間差：見 4.5** |
| 監控 | **APT42 的 Data Processing Agent**（自然語言轉 SQL 查個資）；China-nexus 的 BLE 定位研究 | 獨立一章十案，含 Arman 案件管理系統、台灣政治人物監控 | **弱互證：見 4.7** |
| 資訊作戰 | 「None of these attempts have created breakthrough capabilities」 | 九個案例，含唯一逐字對上實際發布內容的 GTG-24015 | **看似分歧，實為時間差：見 4.8** |
| 自主程度 | 最高只到「惡意程式盲目執行 LLM 輸出的單行指令」 | 多代理框架自主跑數小時到數天 | **時間差 ＋ 視角差：見 4.9** |
| 非法蒸餾 | **本期完全沒有** | 獨立一章七家中國實驗室 | **缺口** |
| 常規武器／生物 | **本期完全沒有** | 各自獨立一章 | **缺口：GTIG 系列從未涵蓋這兩個危害領域** |

### 4.2 俄羅斯：同一個戰場，兩個不同的情報機關

這是最容易被混淆、也最該講清楚的一組對照。

| | **GTIG 記錄的 APT28** | **Anthropic 記錄的 GTG-20006** |
|---|---|---|
| 公開歸因 | 俄羅斯**軍事情報總局 GRU**（APT28 / Fancy Bear / FROZENLAKE / UAC-0001） | 「consistent with public reporting linking the actor to **Midnight Blizzard**」，即 **SVR 對外情報局**（APT29 / Cozy Bear） |
| 主要受害者 | **烏克蘭**（CERT-UA 指為安全與國防部門） | 烏克蘭與歐洲為主，延伸中東與亞洲海事；**超過 20 個組織** |
| AI 用在哪 | **惡意程式內部**：即時生成 Windows 竊取指令 | **攻擊者的工作流**：Claude Code skills 驅動整條 kill chain |
| 用了誰的模型 | **Qwen2.5-Coder-32B-Instruct**（透過 Hugging Face，用竊來的 token） | Claude |
| 自主程度 | 惡意程式自動化，但邏輯簡單（兩段固定提示） | 人類只在需要精修 skills 時介入 |
| 證據來源 | **野外檢體** ＋ CERT-UA 獨立公告 | **Anthropic 平台側遙測**（單一來源為主，部分 IOC 有 Microsoft 與 GTIG 佐證） |

**三個教學結論**［分析］：

1. **不要把「俄羅斯用 AI」講成一件事。** GRU 與 SVR 是兩個獨立的情報機關，作業文化不同：GRU 傳統上更願意用破壞性、量產型工具（NotPetya、Sandworm 系列），SVR 更重視長期潛伏與 OPSEC。**這個差異在 AI 使用上完全對應得上**：GRU 把 LLM 塞進惡意程式讓它自己跑，SVR 則把 AI 留在自己這一側、當成工程團隊用。
2. **「用哪一家模型」本身是情報訊號。** APT28 選了一個**開源權重模型**（Qwen）透過 Hugging Face 存取，而不是任何一家前沿商業模型。這規避了商業供應商的柵欄與遙測，代價是能力較弱。**這是本課程柵欄專題「路徑 D：模型選擇」的一個野外實例**，而且是 GTIG 這份報告裡最硬的一筆證據。詳見 `../shared/02-claude-safeguards-and-bypass-paths.html`。
3. **兩份報告合起來，才看得到俄羅斯 AI 使用的全貌**：一端是 GRU 的「AI 下放到 payload」，另一端是 SVR 的「AI 上收到指揮層」。**這兩個方向對防守方的意涵完全相反**：前者要在端點抓，後者只能靠行為分析與情報共享。

對照教材：`../01-cyber/GTG-20006-russian-espionage.html`

### 4.3 執行期 AI：Anthropic 報告裡完全沒有的一格

這是本份教材認為**最值得排進課程的對照**。

Anthropic 2026-09 報告通篇在講自主化，但它的自主化全部發生在**攻擊者這一側**：多代理框架、排程無人值守、跨工作階段的持久戰役記憶。**沒有任何一個案例是「惡意程式自己在受害者機器上呼叫模型」。**

為什麼會這樣？三個可能解釋，建議讓學員辯論［分析］：

1. **可觀測性使然。** 如果一支惡意程式在受害者機器上用**竊來的金鑰**呼叫 Claude，Anthropic 看到的會是「某個金鑰從奇怪的地方發出奇怪的請求」，而不是一個可歸因的行為者。這種訊號很可能被歸類到「憑證濫用」而不是「惡意程式」，因此不會寫成獨立案例。
2. **攻擊者的選擇使然。** 要在受害者端呼叫模型，你需要一個能撐得住的存取方式。硬編碼 API key 會被撤銷（PROMPTFLUX 就是這樣被處置的），偷來的 token 會過期。**用開源權重模型（如 APT28 選 Qwen）或自架推論服務**才是可持續的路線，而那些都不會出現在 Anthropic 或 Google 的遙測裡。
3. **這一格的實際威脅還很小。** 到 2026-09 為止，唯一真正部署過的執行期 AI 惡意程式仍然是 PROMPTSTEAL 這一類，功能相當於「一個會生成指令的批次檔」。**Anthropic 沒寫，可能只是因為沒有值得寫的案例。**

**但「反查自己的工具是否被偵測」這條線把兩份報告連起來了**：

```mermaid
flowchart LR
    subgraph G["GTIG 2025-11"]
        G1["China-nexus 行為者：<br/>'Search for threat detection capabilities<br/>related to their own tooling'"]
        G2["PROMPTFLUX：<br/>每小時請 Gemini 改寫自己<br/>（未實裝）"]
    end
    subgraph A["Anthropic 2026-09"]
        A1["GTG-20006：<br/>監控自家惡意程式是否被偵測<br/>→ 自動改寫 → 迭代到隱形"]
    end
    G1 --> C["同一個目標的三個成熟度階段"]
    G2 --> C
    A1 --> C
    C --> D["階段一：人類手動問模型<br/>『我的工具被抓了嗎』"]
    C --> E["階段二：惡意程式自己請模型改寫<br/>但沒有回饋迴路"]
    C --> F["階段三：完整閉環<br/>偵測狀態 → 改寫 → 驗證 → 再部署"]
    style F fill:#ffe8e8
```

**教學結論**：把三個片段排成一條成熟度曲線，學員會看到**「AI 驅動的規避」不是一個開關，而是一條有明確工程里程碑的路線**，而目前野外大約停在階段一與階段二之間。**GTIG 的 PROMPTFLUX 之所以還在實驗階段，缺的正是階段三的回饋迴路**（沒有驗證機制、沒有熵源、關鍵函式被註解掉）。

對照教材：`../01-cyber/GTG-20006-russian-espionage.html`、`../01-cyber/00-cyber-trends-and-skills.html`

### 4.4 地下市場：兩份報告拍到的是市場的不同層

本課程 `../01-cyber/GTG-50021-fake-reseller.html` 記錄的是一個俄語與烏克蘭語團體（化名「kl1zy」）經營**假冒 Claude 轉售服務**：對外宣稱多模型中介與折扣，實際上把客戶流量靜默代理到別的模型，並在客戶裝置上安裝憑證收割器，把偷來的 Anthropic 帳號**轉賣給其他 AI proxy 轉售商**。

GTIG 這一期拍到的是**另一層**：

| | **GTIG 2025-11 的 Figure 5 市場** | **Anthropic GTG-50021 的市場** |
|---|---|---|
| 商品 | **成品工具**（WormGPT、Xanthorox、FraudGPT…） | **對合法前沿模型的存取權** |
| 底層模型 | 自架或改造的開源模型；Xanthorox 宣稱五個自建模型跑在自家伺服器［外部］ | **真正的 Claude**（或宣稱是） |
| 買家要的 | 一個沒有柵欄、開箱即用的介面 | **前沿模型的能力**，越便宜越好 |
| 價格帶 | 訂閱制分級；WormGPT 與 FraudGPT 早期在每月數百美元量級［外部］ | 宣稱是折扣價 |
| 對模型供應商的可見度 | **幾乎為零**（不經過供應商的 API） | **高**（用的是供應商的帳號與金鑰） |
| 防守方的著力點 | 論壇監看、金流、Telegram 頻道 | **帳號行為分析、金鑰輪替、採購治理** |

**兩層之間的關係是互補而不是競爭**［分析］：買不起或不想被追蹤的人買成品工具（能力較弱但匿名），要真能力的人買偷來的前沿模型存取（能力強但會被封）。**這兩層一起構成完整的地下 AI 供應鏈**，而任何一家模型供應商的報告都只看得到其中一層。

**一個必須誠實標註的差異**［分析］：GTIG 這一期**沒有提到偷來的 API 金鑰黑市、沒有提到 API 聚合器、沒有提到假轉售商**。這些要到 GTIG 2026-05 那一期才出現（Claude-Relay-Service、CLIProxyAPI、OmniRoute、Roxy Browser 等，見 `gtig-2026-05-ai-threat-tracker.html`）。所以本期與 GTG-50021 的對照是**「市場的另一層」而非「同一件事的兩個視角」**。

**Figure 5 的十個工具與 Anthropic 報告的關係**：Anthropic 2026-09 報告**沒有列出任何一個地下 AI 工具的名稱**。這是一個明確的覆蓋缺口，原因也很直觀：那些工具不跑在 Claude 上，Anthropic 看不到。**要教「地下 AI 工具生態」這個題目，必須引用 GTIG 或 Trend Micro 這類做論壇監看的機構，不能只用模型供應商的報告。**

### 4.5 漏洞研究：十個月的差距有多大

| 時間 | 報告 | 對「AI 找漏洞」的記錄 |
|---|---|---|
| 2025-11 | **GTIG 本期** | n-day 的大量利用（Roundcube、Zimbra）；改良公開的 PoC 腳本；UNC4899 往邊界設備與瀏覽器做漏洞研究。**沒有任何 AI 產出零日的紀錄** |
| 2026-05 | GTIG | **首度辨識出 AI 開發的零日**（語意邏輯瑕疵造成的 2FA 繞過），並在大規模利用前攔下 |
| 2026-09 | Anthropic | **GTG-10007** 自主零日鑄造廠：對網路設備單月產出十餘個可能零日 |

**這條時間線本身就是一堂課**［分析］：從「改良別人的 PoC」到「自主鑄造零日」只花了十個月。而且這十個月裡，**兩家獨立機構從兩個不同角度各自確認**（GTIG 從野外成品側，Anthropic 從平台生產線側）。

**課堂用法**：把三個時間點做成一張投影片，問學員「如果外推到 2027-09，你預期會看到什麼？」這比任何預測性論述都更能讓學員感受到變化速率。但同時要提醒：**外推是最危險的分析動作**，2025-11 這一期的 PROMPTFLUX 如果外推，會預測 2026 年出現成熟的自我改寫惡意程式，而實際上到 2026-09 都沒有。

對照教材：`../01-cyber/GTG-10007-exploit-foundry.html`、`gtig-2026-05-ai-threat-tracker.html`

### 4.6 柵欄繞過：GTIG 給了 Anthropic 失效模式的「野外對照組」

本課程 `../03-surveillance/00-surveillance-intro.html` 把 Anthropic 自承的防線失效整理成**四種模式**。GTIG 這一期對其中兩種提供了獨立的、來自另一家平台的對照證據：

| Anthropic 的失效模式 | GTIG 2025-11 的對應證據 | 關係 |
|---|---|---|
| **(a) 重新提示突破**（Claude 正確拒絕，但在進一步提示後被突破） | China-nexus 行為者被 Gemini 拒絕後，改稱 CTF 參賽者即取得資訊；TEMP.Zagros 遇到 safety response 後改稱學生 | **強互證。兩家平台、兩個獨立行為者、同一個失效模式** |
| **(b) 跨工作階段拆分** | 本期無直接對應 | 缺口 |
| **(c) 工具開發請求看似中性** | **APT42 的 Data Processing Agent**：「把自然語言轉成 SQL」是完全合法的請求 | **強互證** |
| **(d) 部署後不可收回** | PROMPTFLUX 的變體已經散布到可移除磁碟與網路共享；Google 只能停用 API key，**無法收回已經生成的混淆程式碼** | **互證** |

**最值得並排投影的兩段原文**：

> **Anthropic 2026-09（p.97）**：「Our existing safeguards **did not perform uniformly** in these cases. In one case, Claude correctly refused a request but was **overcome on further prompting**. In another, it complied across many sessions without intervention.」

> **GTIG 2025-11（PDF p.8）**：「the actor asked Gemini to identify vulnerabilities on a compromised system, but **received a safety response**... The actor then continued, reframing the prompt by depicting themselves as a participant in a capture-the-flag (CTF) exercise... **Gemini returned helpful information that could be misused to exploit the system**.」

**兩家最頂尖的模型供應商，在同一個失效模式上給出了幾乎一模一樣的描述。**［分析］這件事的份量比任何單一報告都大：它說明「拒絕之後在下一輪被說服」**不是某一家的實作問題，而是目前這一代對話式模型的結構性弱點**。原因也很清楚：模型在每一輪都要重新判斷，而**使用者可以無限次重試，模型卻不能記住「這個人剛剛被我拒絕過」的意圖判斷**。

**這推導出一個具體的產品設計結論**［分析］：防護的狀態必須跨輪保存。一個帳號在被拒絕之後的後續請求，應該被放進一個**更嚴格的判定模式**，而不是當作全新的對話從頭評估。GTIG 與 Anthropic 都沒有明說他們是否這樣做。

對照教材：`../shared/02-claude-safeguards-and-bypass-paths.html`、`../03-surveillance/00-surveillance-intro.html`

### 4.7 監控：APT42 的 Data Processing Agent 對上伊朗的 Arman 系統

本課程 `../03-surveillance/GTG-34007-iran-surveillance.html` 記錄了兩個伊朗 nexus 單位，其中一個把監控做成一條**行政流水線**：資料收割工具 → 去匿名與身分解析 → 社群網路分析點名 → **Arman 案件管理系統**立案派工 → 行動。同案的另一組數字是：一年內監控並側寫 6,388 名伊朗人，對 155,216 則推文做社交網路分析，篩出 39 個反對派帳號。

GTIG 的 APT42 案例在**功能上**與這條流水線的第二、三段高度重疊：

| 功能 | GTIG 的 APT42 Data Processing Agent | Anthropic 的伊朗監控案例 |
|---|---|---|
| 去匿名化 | 「linking a phone number to an owner」 | 身分解析（identity resolution） |
| 行為模式分析 | 「tracking an individual's travel patterns」 | 社群網路分析、活動側寫 |
| 目標篩選 | 「generating lists of people based on shared attributes」 | 從 155,216 則推文篩出 39 個帳號 |
| AI 扮演的角色 | **查詢介面工程師**（自然語言轉 SQL） | **工程部門 ＋ 分析師** |
| 資料從哪來 | **報告沒說**。行為者只提供 schema | 報告有描述收割工具 |
| 處置 | 帳號停用 | 帳號停用，但 Anthropic 自承部分工具請求未被拒絕 |

**兩個必須標明的差異**［分析］：

1. **GTIG 沒有把 APT42 這一段定性為監控行動。** 它被放在「Continued Augmentation of the Full Attack Lifecycle」章節，與釣魚一起講。**GTIG 系列到目前為止沒有獨立的監控章節**，這是它與 Anthropic 報告最大的結構差異之一。
2. **GTIG 沒有提到任何跨境鎮壓、僑民監控、宗教或民族社群目標。** Anthropic 模組 03 的主軸（中國對維吾爾人、藏人、法輪功、台灣長老教會與台灣政治人物的監控）在 GTIG 本期**完全沒有對應內容**。

**因此在課堂上不應把 GTIG 這一期當作模組 03 的佐證。** 它能佐證的只有一件事：**「用 AI 建一個查詢個資的介面」這個手法，在兩家平台上都被國家級行為者嘗試過。**

另外值得記下的是 China-nexus 行為者的 **BLE 定位研究**（「scan for Bluetooth Low Energy (BLE) devices and research means to extract additional positioning information from Bluetooth signals on mobile devices」，PDF p.9）。這是本報告唯一觸及**實體世界定位**的能力，性質上比較接近監控而非入侵。**Anthropic 2026-09 報告沒有任何 BLE 或實體定位的案例**，這是 GTIG 獨有的一筆。

對照教材：`../03-surveillance/GTG-34007-iran-surveillance.html`、`../03-surveillance/00-surveillance-intro.html`

### 4.8 資訊作戰：分歧其實大半是時間差

表面上：GTIG 說「沒有突破性能力」，Anthropic 用一整章九個案例講 AI 如何在生產宣傳內容。

但把時間軸擺進來就清楚了：

| 時間 | 誰 | 對 AI 影響力行動的判斷 |
|---|---|---|
| 2025-11 | **GTIG 本期** | 「we have not identified these generated articles in the wild... **None of these attempts have created breakthrough capabilities**」 |
| 2026-05 | GTIG | 幾乎相同的措辭，但**多了一個實績**：Operation Overload 的 AI 語音複製冒充真實記者 |
| 2026-09 | Anthropic | 九個案例，含**唯一能把 Claude 產出逐字對上實際發布內容**的 GTG-24015 俄羅斯國家媒體案 |

**三件事要同時講**［分析］：

1. **時間差解釋了大半的分歧。** 從 2025-11 到 2026-09 是十個月，而 IO 的 AI 採用曲線在這段期間明顯上升。
2. **但視角差也是真的。** GTIG 的 IO 團隊以**開源網路觀測**為主（看得到什麼被發出來），Anthropic 以**平台側提示紀錄**為主（看得到誰想做什麼）。**「未在野外找到」與「確實在生產」可以同時為真**：兩者之間缺的是文字指紋比對這道工序。
3. **而且 Anthropic 自己也沒有主張突破。** 本課程 `../02-influence/00-influence-intro-and-breakout-scale.html` 的 Breakout Scale 六級量表顯示，Anthropic 把九案中**大多數評在低級距，只有一個 Category Four**。**所以兩家在「多數 AI 影響力行動沒有造成質變」這一點上其實是一致的。**

**課堂設計建議**：把 GTIG 的三個否定句（見第 3.11 節的表格）與 Anthropic 的 Breakout Scale 評級並排，讓學員練習區分「行為者做了什麼」「產出流到哪裡」「造成了什麼效果」這三個層次。**廠商報告最常混淆的就是這三層。**

### 4.9 一週之隔的兩份十一月報告

這是本教材認為最有課堂張力的一組對照，因為它排除了時間差這個變數。

| | **GTIG 2025-11-05/06** | **Anthropic 2025-11-13** |
|---|---|---|
| 標題 | Advances in Threat Actor Usage of AI Tools | Disrupting the **first reported AI-orchestrated** cyber espionage campaign |
| 自主度的最高主張 | 惡意程式在執行期呼叫 LLM 生成**單行指令**並盲目執行 | **GTG-1002**：AI 自主執行攻擊生命週期的絕大部分 |
| 基調 | 「While still nascent, this represents a significant step **toward** more autonomous and adaptive malware.」（**朝向**） | 「the first reported AI-orchestrated cyber espionage campaign」（**已經發生**） |
| IOC | 無 | 無 |
| 歸因 | APT28 等既有 Mandiant 代號，信度措辭保守 | **high confidence** 中國國家支持 |
| 事後處理 | 未見更正（PROMPTLOCK 的學術來源未加註） | **四天內兩次公開修訂** |
| 社群反應 | 媒體大量轉載；研究者對 PROMPTFLUX 的價值提出質疑 | 發布後隨即引發對「沒有 IOC」的公開質疑 |

**這一組對照要教什麼**［分析］：

1. **「第一次」這個詞在威脅情報裡是一種修辭資源，不是客觀事實。** GTIG 說「for the first time... malware that use LLMs during execution」；Anthropic 說「first reported AI-orchestrated cyber espionage campaign」。**兩者都在同一個月宣稱了一個「第一次」，而且指的是完全不同的東西。** 而真正的「第一次」（LAMEHUG）其實是 CERT-UA 在 2025-07 公告的。
2. **兩家的揭露動機不同，所以敘事框架不同。** GTIG 的報告在結尾大篇幅介紹 Big Sleep、CodeMender、SAIF 與 Gemini 安全白皮書，**框架是「我們在防守」**；Anthropic 的報告則是為單一案例發一份獨立文件，**框架是「這件事嚴重到值得單獨示警」**。
3. **兩家的保守與激進方向相反，而且與各自的商業位置有關**［分析，這是推論不是事實］。Google 同時是模型供應商與最大的資安廠商之一，過度渲染 AI 惡意程式威脅會回頭傷害自己的模型業務；Anthropic 是純模型公司，把 AI 風險講得嚴重，與它的政策倡議立場一致。**這個推論要在課堂上明確標示為推論，並且鼓勵學員反駁。**

對照教材：`anthropic-2025-11-ai-orchestrated-espionage.html`

### 4.10 涵蓋範圍：三個 GTIG 從未碰過的危害領域

誠實標註缺口：**非法蒸餾**（GTIG 直到 2026-02 才處理，對照 `../07-distillation/00-distillation-intro-and-mitigations.html`）、**常規武器**（GTIG 系列**從未**報導任何用 Gemini 做武器工程、火控規格、無人機自主化或採購規避的案例，對照 `../04-weapons/00-weapons-intro-and-safeguards.html`）、**生物濫用**（同樣**從未**出現，對照 `../05-bio/00-bio-intro-and-safeguards.html`）。

**這個缺口本身是重要的教學素材**［分析］。三種可能解釋：**職責範圍不同**（GTIG 的傳統職掌是網路威脅與 IO，武器與生物屬於 Trust & Safety 或政策團隊）、**偵測能力不同**（Anthropic 有專門的生物與化學分類器並把四種狀態寫進報告，Google 是否有等價機制無從得知）、**揭露意願不同**（武器與生物的揭露涉及更高的法律與政策風險）。

**課堂結論**：**「某家廠商的報告裡沒有某個危害領域」不能推論成「該平台上沒有這種濫用」。** 這是引用單一廠商報告時最容易犯的錯誤，也是模組 09 存在的理由。

---

## 5. TTP 與 MITRE ATT&CK 對應

**重要聲明**：GTIG 這一期**沒有附任何 MITRE ATT&CK 或 ATLAS 對照表**（2026-05 那一期有兩個附錄表，本期沒有）。下表**全部由本教材建構**，屬於［分析］，不是 GTIG 的官方對應。使用時請標明出處。

### 5.1 惡意程式側（ATT&CK Enterprise）

| 戰術 | 技術 ID | 本報告的具體作法 | 偵測構想（本教材補充） |
|---|---|---|---|
| Execution | `T1059.005` Command and Scripting Interpreter: Visual Basic | PROMPTFLUX 以 VBScript 實作，`CreateObject("WScript.Shell")`、`Scripting.FileSystemObject` | **`wscript.exe` 或 `cscript.exe` 發起對外 HTTPS 連線**。這是本報告產出的**最高保真度單一條件偵測** |
| Execution | `T1059.001` PowerShell | FRUITSHELL 為公開可得的 PowerShell reverse shell | 標準 PowerShell 腳本區塊記錄（Script Block Logging）＋ 網路連線關聯 |
| Execution | `T1059.006` Python | PROMPTSTEAL 以 Python 撰寫、PyInstaller 打包 | PyInstaller 解包後的臨時目錄（`_MEI*`）＋ 對 AI 推論端點的連線 |
| Command and Control | `T1071.001` Application Layer Protocol: Web Protocols | PROMPTFLUX 對 `generativelanguage.googleapis.com/v1beta/models/...:generateContent` 發 POST；PROMPTSTEAL 對 Hugging Face API | **程序歸屬是關鍵**：對 AI 推論端點的連線若來自非瀏覽器、非已知 AI 應用的程序，一律當異常 |
| Command and Control | `T1102` Web Service | China-nexus 行為者開發**以 WeChat 為 C2** 的惡意程式後端 | 企業環境中 WeChat 的非互動式 API 流量 |
| Persistence | `T1547.001` Boot or Logon Autostart: Registry Run Keys / Startup Folder | PROMPTFLUX 把新混淆版本存入 **Startup 資料夾** | 腳本直譯器寫入 Startup 資料夾（腳本寫腳本），本身即高風險組合 |
| Lateral Movement | `T1091` Replication Through Removable Media | PROMPTFLUX 複製自己到**可移除磁碟** | USB 上出現 `.vbs` 檔案且內含長串英文自然語言 |
| Lateral Movement | `T1021.002` Remote Services: SMB/Windows Admin Shares | PROMPTFLUX 複製自己到**已對應的網路磁碟機** | 同上，加上網路共享的寫入稽核 |
| Defense Evasion | `T1027` Obfuscated Files or Information | PROMPTFLUX 的整個存在目的；APT41 針對兩個公開混淆函式庫求助 | **混淆本身抓不到，要抓產生混淆的行為**（見下方 5.3 的框架缺口） |
| Defense Evasion | `T1036` Masquerading | PROMPTSTEAL 偽裝成「image generation」程式；PROMPTFLUX 誘餌檔名 `crypted_ScreenRec_webinstall` | 檔名與實際行為不符；宣稱是影像生成卻執行 `cmd.exe` |
| Defense Evasion | `T1140` Deobfuscate/Decode Files or Information | PROMPTFLUX「decodes and executes an embedded decoy installer」 | 腳本執行期解碼並落地 PE 檔 |
| Discovery | `T1082` System Information Discovery | PROMPTSTEAL 提示明列 computer / hardware / process / services / networks information | **對 `C:\Programdata\info\info.txt` 的建檔事件**（見第 7 節） |
| Discovery | `T1087.002` Account Discovery: Domain Account | PROMPTSTEAL 提示中的 **AD domain information** | 單一非網域管理程序在短時間內執行多個 AD 列舉指令 |
| Discovery | `T1613` Container and Resource Discovery | suspected China-nexus 行為者請 Gemini 生成列舉 Kubernetes 容器與 pod 的指令 | 非 CI/CD 帳號執行 `kubectl get pods --all-namespaces` 等列舉 |
| Collection | `T1119` Automated Collection | PROMPTSTEAL 遞迴複製 Documents / Downloads / Desktop 的 office 與 pdf/txt 檔 | 短時間內大量文件被複製到單一暫存目錄 |
| Credential Access | `T1528` Steal Application Access Token | QUIETVAULT 竊取 GitHub 與 npm token | 開發機上對 `~/.npmrc`、`~/.config/gh` 的非預期讀取 |
| Credential Access | `T1552.001` Unsecured Credentials: Credentials In Files | QUIETVAULT **用主機上的 AI CLI 工具搜尋其他機密** | **AI CLI 二進位檔被非互動式程序（如 npm postinstall）呼叫**，這是極高保真度的訊號 |
| Credential Access | `T1550.001` Use Alternate Authentication Material: Application Access Token | suspected China-nexus 行為者研究如何使用 **EC2 臨時工作階段權杖** | 臨時憑證從非預期 IP 或非預期服務被使用 |
| Exfiltration | `T1567.001` Exfiltration Over Web Service: Exfiltration to Code Repository | QUIETVAULT **在受害者帳號下建立公開 GitHub repo** 外洩憑證 | GitHub 稽核日誌：新建公開儲存庫且在短時間內推送小型文字檔 |
| Exfiltration | `T1041` Exfiltration Over C2 Channel | PROMPTSTEAL 把收集結果外傳（CERT-UA 記錄為 SFTP 或 HTTP POST）［外部］ | 出站 SFTP 至非白名單主機 |
| Initial Access | `T1190` Exploit Public-Facing Application | 對政府網域的 **Roundcube 與 Zimbra** 郵件伺服器做 n-day 大量利用 | 郵件伺服器的已知 CVE 掃描特徵；**修補節奏本身就是防線** |
| Initial Access | `T1566` Phishing | 多個行為者；TEMP.Zagros 用**已入侵的企業郵件帳號**增加可信度 | 寄件者信譽正常但行為異常（首次寄給該收件人、附件型態異常） |
| Persistence | `T1505.003` Server Software Component: Web Shell | China-nexus 與 UNC4899 都開發 ASP 與 JavaScript web shell | 網頁根目錄的檔案完整性監控 |
| Resource Development | `T1587.001` Develop Capabilities: Malware | TEMP.Zagros 從公開工具轉向自製 web shell 與 Python C2 | 不適用（發生在攻擊者端） |
| Resource Development | `T1588.002` Obtain Capabilities: Tool | 地下論壇的 10 個 AI 工具 | 論壇監看；金流與 Telegram 頻道追蹤 |

### 5.2 AI 側（MITRE ATLAS）

| 戰術 | 技術 ID | 本報告的具體作法 | 偵測構想（本教材補充） |
|---|---|---|---|
| AI Model Access | `AML.T0040` AI Model Inference API Access | PROMPTFLUX 用硬編碼 key 呼叫 Gemini；PROMPTSTEAL 用**竊來的 token** 呼叫 Hugging Face | 端點側：程序歸屬 ＋ 目的地為推論端點。平台側：單一 key 從大量不相關 IP 使用 |
| Defense Evasion | `AML.T0054` LLM Jailbreak | 「I am working on a CTF problem」、「a student working on a final university project」、「act as an expert VBScript obfuscator」 | 平台側：**人設宣告 ＋ 高風險技術請求的共現**；**同一帳號在被拒絕後立刻改寫請求**的模式 |
| Defense Evasion | `AML.T0051.001` LLM Prompt Injection: Indirect | **FRUITSHELL 內嵌提示，目標是防守方的 LLM 分析系統** | 對進入分析管線的檢體做「第二人稱祈使句掃描」 |
| Resource Development | `AML.T0016.002` Obtain Capabilities: Generative AI | 地下論壇的成品工具；APT28 選用開源權重模型規避商業柵欄 | 論壇監看；企業內對非核准 AI 服務的出站流量 |
| Resource Development | `AML.T0055` Unsecured Credentials | PROMPTSTEAL「likely uses stolen API tokens」 | Hugging Face 與各家平台的 token 洩漏掃描；**把 AI token 納入與雲端金鑰同級的輪替政策** |
| Impact | `AML.T0048` External Harms | APT42 的 Data Processing Agent 用於個資去匿名與人員篩選 | 不適用（發生在攻擊者端） |

### 5.3 框架缺口（必須明確標示）

| 缺口 | 為什麼現有框架接不住 | 建議的暫代作法 |
|---|---|---|
| **執行期 LLM 作為變形引擎** | ATT&CK 的 `T1027` 系列描述「檔案被混淆」這個**狀態**，`T1027.002` 描述加殼這個**手法**，但沒有任何 ID 描述「惡意程式在受害端呼叫外部模型，即時取得新的混淆程式碼」這個**架構**。ATLAS 的 `AML.T0040` 只描述「取得推論 API 存取」，不涵蓋「把推論結果直接當成自身程式碼」 | 在內部威脅模型中新增一個自訂標記，例如 `RuntimeModelCodegen`，並以「程序歸屬 ＋ 推論端點連線」作為主要偵測面 |
| **針對防守方 AI 的提示注入** | `AML.T0051` 的框架設定是「攻擊者注入內容到**受害者的 AI 應用**」。FRUITSHELL 的情境是「攻擊者注入內容到**資安廠商或 SOC 的分析管線**」，兩者的攻擊面與責任歸屬完全不同 | 自訂標記 `DefenderAIPoisoning`；在 AI 輔助分析流程的設計文件中明列為威脅 |
| **人設前綴繞過** | `AML.T0054 LLM Jailbreak` 涵蓋了，但它把所有繞過手法混成一個 ID。「用 base64 編碼繞過」與「聲稱自己是 CTF 選手」的**偵測方式、緩解方式、誤報成本**完全不同 | 在內部細分子類：編碼混淆型、角色扮演型、**合法情境宣告型**。第三類最難處理，因為它與真實使用者無法區分 |
| **模型供應商作為情報蒐集面** | 這不是攻擊者的 TTP，而是**防守方的一種情報來源類型**。ATT&CK 與 ATLAS 都不描述情報來源 | 在情報來源分類中新增「模型供應商遙測」一類，並標註其**覆蓋率取決於對手選用哪一家模型**的固有偏差 |
| **AI 工具作為商品** | 地下市場的 AI 工具在 ATT&CK 裡只能歸到 `T1588.002 Obtain Capabilities: Tool`，無法表達「訂閱制」「免費版插廣告」「多模型自架」等生態成熟度訊號 | 用商業模式指標（定價分級、支援管道、更新頻率）作為生態成熟度的獨立度量 |

---

## 6. 圖表判讀

本報告有 **10 張 Figure ＋ 2 張 Table**。依模組規範，圖檔不下載、不嵌入，全部以文字描述。下表先給索引（頁碼為 PDF 頁序）。

| 編號 | PDF 頁 | 類型 | 標題 | 資訊密度 |
|---|---|---|---|---|
| Table 1 | p.4 | 表格 | Overview of malware with novel AI capabilities GTIG detected in 2025 | **高**（見第 3.1 節） |
| Figure 1 | p.5 | **原始碼截圖** | VBS "StartThinkingRobot" function | **最高** |
| Figure 2 | p.7 | 提示截圖 | PROMPTSTEAL prompt used to generate command to collect system information | 高 |
| Figure 3 | p.7 | 提示截圖 | PROMPTSTEAL prompt used to generate command to collect targeted documents | 高 |
| Figure 4 | p.9 | 生命週期圖 | A China-nexus threat actor's misuse of Gemini mapped across the attack lifecycle | 高 |
| Table 2 | p.11 | 表格 | Advertised capabilities on English- and Russian-language underground forums | 中（見第 3.9 節） |
| Figure 5 | p.12 | **點矩陣圖** | Capabilities of notable AI tools and services advertised in English- and Russian-language underground forums | **最高（唯一列出工具名稱的地方）** |
| Figure 6 | p.14 | 生命週期圖 | A suspected China-nexus threat actor's misuse of Gemini across the attack lifecycle | 高 |
| Figure 7 | p.16 | 二欄清單圖 | North Korean threat actor's misuse of Gemini to support their operations | 中 |
| Figure 8 | p.16 | 五欄 kill chain 圖 | PUKCHONG (aka UNC4899) misuse of Gemini across the attack lifecycle | **內容與 Figure 6 重複，見 6.8** |
| Figure 9 | p.17 | 二欄清單圖 | APT42's misuse of Gemini to support operations | 低（只有兩條） |
| Figure 10 | p.18 | 二欄清單圖 | APT41 misuse of Gemini to support operations | 低（只有兩條） |

**整體觀察**［分析］：這份報告的圖表**沒有任何一張是統計圖**。沒有長條圖、沒有趨勢線、沒有比例。全部都是**清單的視覺化**（生命週期分欄、能力矩陣）或**證據截圖**（原始碼、提示）。這與 Anthropic 2026-09 報告大量使用圖表承載獨家數字的做法**完全相反**。

**這個差異本身要教**：GTIG 這一期**沒有任何可量化的規模指標**（幾個帳號、幾次請求、幾個受害者一律沒有）。所以它是一份**質性報告**，適合回答「對手在做什麼」，不適合回答「有多嚴重」。引用時不要試圖從它推導出任何趨勢數字。

---

### 6.1 Figure 1（PDF p.5）：VBS "StartThinkingRobot" function

**圖片類型**：白底圓角方框內的**原始碼截圖**，VBScript 語法上色（關鍵字藍色、字串紅色、註解綠色、函式名稱亮藍色）。約 40 行，分成 `Sub StartThinkingRobot()` 與 `Function CallGeminiAPI(promptText, apiKey)` 兩段。

**圖上實際可見的關鍵行（逐字）**：

```
Sub StartThinkingRobot()
    On Error Resume Next
    ' This sub would ideally run in a loop, or be scheduled.
    ' If DateDiff("n", g_LastThinkTime, Now) * 60000 >= g_ThinkInterval Then ' Check if interval passed
    If True Then ' For now, let it run once on script start for testing this part
        Dim aiPrompt, aiResponse, newTechnique
        aiPrompt = "Provide a single, small, self-contained VBScript function or code block that helps evade antivirus detection.
        aiResponse = CallGeminiAPI(aiPrompt, g_APIKey)
        g_LastThinkTime = Now
        If Len(aiResponse) > 10 Then ' Basic check for a response
            ' WScript.Echo "Gemini Said: " & aiResponse ' DEBUG ONLY
            ' Placeholder for actual self-modification:
            ' AttemptToUpdateSelf(aiResponse)
            ...
            Dim tempDir : tempDir = CreateObject("WScript.Shell").ExpandEnvironmentStrings("%TEMP%")
            If logFSO.FolderExists(tempDir) Then
                Set logFile = logFSO.OpenTextFile(tempDir & "\thinking_robot_log.txt", 8, True) ' 8 = Append, True = Create
                logFile.WriteLine Now & " - Received from AI: " & vbCrLf & aiResponse
    ...
Function CallGeminiAPI(promptText, apiKey)
    On Error Resume Next
    Dim http, apiUrl, jsonData, modelName
    modelName = "gemini-1.5-flash-latest" ' Ensure this matches the intended model
    apiUrl = "https://generativelanguage.googleapis.com/v1beta/models/" & modelName & ":generateContent?key=" & apiKey
```
（`...` 為本教材為節省篇幅省略的行，省略處為 `Scripting.FileSystemObject` 的建立與變數宣告，不影響邏輯判讀。）

**資料如何流動**：計時器（`g_ThinkInterval`）→ 組出固定提示 → `CallGeminiAPI` 把 API key 直接串在 URL 的 `key=` 參數 → 取得回應 → 唯一的檢查是 `Len(aiResponse) > 10` → 附加寫入 `%TEMP%\thinking_robot_log.txt`。**自我改寫的那一行 `AttemptToUpdateSelf(aiResponse)` 前面有一個單引號，是註解。**

**這張圖傳達的核心訊息**：兩個互相矛盾的訊息同時存在，而且必須一起講。

1. **設計意圖非常清楚**：作者要的是一個會自我進化的變形腳本，連日誌檔名都叫 `thinking_robot_log.txt`。
2. **實作程度非常低**：`On Error Resume Next`（吞掉所有錯誤）、`If True Then`（迴圈邏輯被硬編碼成只跑一次）、`' For now, let it run once on script start for testing this part`（作者自己的測試註解留在裡面）、`' DEBUG ONLY`（除錯輸出沒清掉）、以及**被註解掉的核心函式**。

**這張圖是整份報告最誠實的一頁**［分析］。它把 GTIG 在正文裡用「development or testing phase」帶過的事情，直接攤在讀者眼前。**任何讀過這張圖的人，都不可能得出「AI 惡意程式時代來臨」的結論。** 而絕大多數媒體報導只引用了正文，沒有引用這張圖。

**課堂用法**（本教材推薦的最高價值用法）：

- **練習一**：把圖投影出來，不給任何背景，請學員回答「這段程式碼目前會做什麼？」正確答案是：**呼叫一次 Gemini，把回應寫進暫存檔，然後什麼也不做。**
- **練習二**：請學員指出「如果你是這個作者，下一步要補的三件事是什麼？」（答案：真正的迴圈與排程、輸出的可執行性驗證、把新程式碼寫回自身並保留 API key 與誘餌 payload。）這個練習讓學員從攻擊者的工程視角理解「距離可用還差多遠」。
- **練習三**：`gemini-1.5-flash-latest` 的 `-latest` 標籤。請學員解釋為什麼攻擊者要這樣寫（答案：模型下架時不會壞掉），以及這對防守方的意涵（答案：**單靠封鎖特定模型版本無法處置**）。

---

### 6.2 Figure 2 與 6.3 Figure 3（PDF p.7）：PROMPTSTEAL 的兩段提示

**圖片類型**：兩張淺灰底的**程式碼區塊截圖**，等寬字型、綠色文字，左上角有一個灰色的語言標籤「None」（Figure 3 的標籤旁還有一個下拉箭頭）。**這個「None」標籤透露了截圖來源**［分析］：它是某種程式碼檢視器或筆記工具（語言選擇器設為 None）的畫面，也就是**分析師在自己的工具裡貼出字串後截圖**，而不是從檢體反編譯畫面直接截。

**Figure 2 的完整文字（逐字）**：

> Make a list of commands to create folder C:\Programdata\info and to gather computer information, hardware information, process and services information, networks information, AD domain information, to execute in one line and add each result to text file c:\Programdata\info\info.txt. Return only commands, without markdown

**Figure 3 的完整文字（逐字）**：

> Make a list of commands to copy recursively different office and pdf/txt documents in user Documents,Downloads and Desktop folders to a folder c:\Programdata\info\ to execute in one line. Return only command, without markdown.

**圖上可觀察到的細節**［分析］：

- **兩段提示的英文都有明顯的非母語痕跡**：`Documents,Downloads and Desktop` 沒有空格、`Return only commands` 與 `Return only command` 單複數不一致、`different office and pdf/txt documents` 的 `different` 用得不自然。**這是行為者手寫的，不是模型生成的。**
- **兩段都以 `Return only commands, without markdown` 結尾**，這是同一個作者的固定收尾習慣。
- **路徑大小寫不一致**：Figure 2 前半用 `C:\Programdata\info`，後半用 `c:\Programdata\info\info.txt`。細節不一致同樣指向手寫。

**核心訊息**：這兩張圖證明了三件事。第一，**提示是硬編碼的**，所以可以當靜態特徵。第二，**行為者的收集需求被完整揭露**（主機資訊 ＋ AD 網域資訊 ＋ 文件）。第三，**行為者必須做格式工程**（`without markdown`），證明這是一套真的在跑的整合，不是概念展示。

**課堂用法**：

- 以來源公開片段作離線的字串比對練習，要求同時加入合法程式與正常提示的反例。`without markdown` 等片語也常見於正當工作，不是惡意或 LLM 整合的唯一指紋，不能假設攻擊者無法改寫。
- 進階討論：如果攻擊者把提示改成加密儲存、執行時才解密，這條偵測就失效了。**請學員估計這個防禦的壽命。**（GTIG 已經說「new samples adding obfuscation」，所以答案是：已經失效中。）

---

### 6.4 Figure 4（PDF p.9）：China-nexus 行為者的攻擊生命週期

**圖片類型**：兩層結構的**流程圖 ＋ 分欄清單**。

**上層**：六個圓角方框排成一個環形流程，用灰色虛線箭頭連接。方框的顏色分兩組：**藍框**（Initial Compromise、Establish Foothold、Complete Mission）與**綠框**（Escalate Privilege、Move Laterally、Maintain Presence）。虛線箭頭在中央畫出一個循環，暗示提權、橫向移動、維持存在三者反覆進行。這是 **Mandiant 的 Attack Lifecycle 模型**，不是 Lockheed Martin 的 Cyber Kill Chain。

**下層**：六欄表格，欄首與上層方框同色，欄內是項目符號清單。逐欄內容（逐字抄錄）：

| 階段 | 項目 |
|---|---|
| **Initial Compromise** | Conduct research related to diplomatic efforts and political topics throughout **Asia, Africa and Europe**｜Generate topical phishing material for targets｜Develop tooling to send phishing emails｜Develop tooling to support **smishing**｜**Search for threat detection capabilities related to their own tooling**｜Develop a Python script to scan **government domains** to identify vulnerable **Roundcube and Zimbra** email servers｜Scan for exploits related to multiple different email clients and services｜Improve upon publicly available proof of concept scripts for exploitation｜**Mass exploitation of email servers using n-day exploits** |
| **Establish Foothold** | Malware tooling and development in multiple programming languages (**Python, C#, PHP, Ruby and Go**)｜Develop malware backend that uses **WeChat for C2** infrastructure｜Generate script to encrypt data, likely for C2 development｜Develop a capability to scan for **Bluetooth Low Energy (BLE)** devices and research means to extract additional positioning information from Bluetooth signals on mobile devices |
| **Escalate Privilege** | Check for vulnerabilities of compromised systems likely to identify potential opportunities to escalate privileges｜Research vulnerabilities in **VirtualCenter**, likely in need of immediate assistance after compromising a VMware |
| **Move Laterally** | Troubleshoot Python source code related to **WeChat messages**, likely related to the actors C2 framework for interfacing or controlling **Android implants** |
| **Maintain Presence** | Create **webshells** for persistent access |
| **Complete Mission** | Queries regarding credentials are indicative of remote access to **several compromised organizations**｜Develop Linux command line commands to **compress files under 10MB** in a directory in the last year, likely to prepare information for data theft｜Develop Python and C# tooling to facilitate **theft of emails** from compromised email servers and inboxes｜Develop a script to upload and download from **OneDrive**｜Develop scripts to forward stolen data from compromised servers to adversary-controlled infrastructure |

**數字分布的觀察**［分析］：**九項集中在 Initial Compromise，五項在 Complete Mission，中間四個階段加起來只有六項。** 這個分布不是偶然：

- **頭尾重、中間輕**，說明這個行為者向 Gemini 求助最多的是**進得去**與**拿得走**，而不是**在裡面怎麼走**。
- 這符合一個合理的推測［分析］：橫向移動與提權高度依賴**受害環境的具體狀態**，而 LLM 沒有那個環境的上下文，幫不上太多忙。相反地，寫掃描器、寫釣魚信、寫外洩腳本這些**離線的工程任務**，正是 LLM 最強的地方。
- **這對防守方是好消息也是壞消息**：好消息是「內部移動」目前仍是 AI 幫不上忙的環節，所以內網偵測的相對價值上升；壞消息是**周邊防線的攻擊成本正在快速下降**。

**兩個必須單獨標出的項目**：

1. **「Search for threat detection capabilities related to their own tooling」**：這是 Anthropic GTG-20006 自動化規避閉環的手動版前身（見第 4.3 節）。
2. **「compress files under 10MB in a directory in the last year」**：**10MB 上限 ＋ 一年時間窗**這兩個參數，透露了外洩通道的限制（很可能是郵件附件或某個有大小限制的雲端服務）與情報需求的時間範圍。**兩個數字就能反推外洩手法**，這是「微證據、大結論」的又一個範例，非常適合當課堂練習。

**課堂用法**：把六欄的標題遮住，只給項目清單，請學員自己分配到六個階段。這訓練他們把觀察到的行為對應到攻擊階段，也會暴露一個真實的困難：**很多項目可以放進不只一欄**（例如「掃描 Roundcube 漏洞」既是偵察也是初始入侵）。這正是威脅情報分類的日常難題。

---

### 6.5 Figure 5（PDF p.12）：地下論壇 AI 工具能力矩陣

**圖片類型**：**點矩陣圖（dot matrix）**。深灰色橫幅標題「AI Tools in Underground Forums and Their Capabilities」。左側是 10 個工具名稱（各自在白底圓角方框內），上方是 6 個能力欄位，每欄有彩色標題文字與一個對應的彩色圖示。交會處有彩色圓點代表「該工具宣傳此能力」。

**六個欄位與圖示**（逐字）：

| 欄位 | 顏色 | 圖示 |
|---|---|---|
| Deepfake & Image Generation | 淺藍 | 人像卡片 |
| Malware Development | 紅 | 臭蟲 |
| Phishing | 綠 | 魚鉤 |
| Research & Reconnaissance | 黃 | 放大鏡 |
| Technical Support & Code Generation | 橘 | 齒輪 |
| Vulnerability Exploitation | 深藍 | OK 繃交叉 |

**完整矩陣（本教材逐格判讀）**：

| 工具 | Deepfake & Image | Malware Dev | Phishing | Research & Recon | Tech Support & Code | Vuln Exploitation | 合計 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **DarkDev** | | | ● | | ● | | 2 |
| **EvilAI** | ● | | ● | | | ● | 3 |
| **FraudGPT** | | ● | ● | | ● | ● | 4 |
| **LoopGPT** | | ● | | | ● | | 2 |
| **MalwareGPT** | | ● | ● | | ● | | 3 |
| **NYTHEON AI** | ● | | | | ● | | 2 |
| **SpamGPT** | | | ● | | | | 1 |
| **SpamirMailer Bot** | | | ● | | | | 1 |
| **WormGPT** | ● | ● | ● | ● | ● | ● | **6** |
| **Xanthorox** | ● | | | ● | ● | ● | 4 |
| **各能力合計** | **4** | **4** | **7** | **2** | **7** | **4** | 28 |

**數字分布的核心訊息**［分析］：

1. **Phishing 與 Technical Support & Code Generation 並列第一（各 7 個）。** 正文說「almost every notable tool advertised in underground forums mentioned their ability to support phishing campaigns」，圖上是 10 個裡的 7 個。**「almost every」與「7/10」之間有落差**，引用時應以圖為準（見第 12 節）。
2. **Research & Reconnaissance 最冷門（只有 2 個）。** 這很合理：偵察不是這些工具的賣點，因為**合法的前沿模型就能做偵察，而且做得更好**。買家買這些工具是為了取得**合法模型會拒絕**的東西。
3. **WormGPT 是唯一全能的（6/6）**，Xanthorox 與 FraudGPT 各 4 項。**SpamGPT 與 SpamirMailer Bot 各只有 1 項（Phishing）**，是單一功能的專用工具。
4. **這張圖揭示了一個市場結構**：少數幾個「全能平台」（WormGPT、Xanthorox、FraudGPT）＋ 多個「單點工具」。這與正規 SaaS 市場的結構一模一樣。

**第三方脈絡**［外部，GTIG 報告本身沒有提供這些細節］：

- **WormGPT** 與 **FraudGPT** 都出現於 2023 年，前者是把開源模型去掉安全過濾後透過 Telegram 販售，後者由化名「CanadianKingpin12」在多個論壇與 Telegram 頻道推廣，訂閱價格約每月 200 美元或每年 1,700 美元。
- **Xanthorox** 2024-10 先在私人 Telegram 頻道宣布，2025-02 起公開在暗網論壇廣告。與前輩不同，它**宣稱不是靠越獄或改造既有基礎模型，而是自建多模型架構、完全跑在自己的伺服器上**，價格約每月 300 美元。Trend Micro 有專門的分析文。
- **這個演進方向很重要**：從「改造別人的模型」走向「自架整套」，意味著**處置變得更難**。前者可以靠模型供應商封鎖，後者只能靠執法與金流。

**安全與教學提醒**：上表的工具名稱是**犯罪服務的名稱**。課堂上**不要實際搜尋、下載、連線或註冊這些服務**，也不要把名稱當成封鎖清單直接部署（它們多半沒有固定的網域）。它們在此只作為研究資料。

**課堂用法**：

- **練習**：請學員從圖上推論「這個市場最主要的買家在做什麼生意？」答案：**釣魚與詐騙**，不是入侵。這與一般人對「AI 駭客工具」的想像有落差，值得討論。
- **延伸**：把這張圖與 Table 2 的 KYC 繞過那一列合起來看，指向的是**金融詐欺與帳戶開立詐欺**，對台灣的防詐工作比網路入侵更直接相關。

---

### 6.6 Figure 6（PDF p.14）：suspected China-nexus 行為者的攻擊生命週期

**圖片類型**：與 Figure 4 完全相同的版型（上層六個彩色方框的環形流程 ＋ 下層六欄清單），同樣使用 Mandiant Attack Lifecycle 的六個階段名稱。

**逐欄內容（逐字抄錄）**：

| 階段 | 項目 |
|---|---|
| **Initial Compromise** | Research specific target identifiers｜**SQL injection on MS SQL server** |
| **Establish Foothold** | Develop **ASP and javascript webshells**｜Research into SQL server **xp_dirtree and xp_cmdshell** commands to install webshells and upload files |
| **Escalate Privilege** | Research into malware execution techniques on **macOS**, focusing on the use of **unsigned installer packages** for initial access and subsequent methods for gaining elevated privileges |
| **Move Laterally** | Lateral movement in **VMware vSphere** using CLI tools such as **govc**｜Commands for system service information on **Linux**｜Commands for exploring **Kubernetes** servers, containers and pods |
| **Maintain Presence** | Troubleshoot **CloudFlare TLS** certificate and TLS server errors｜Research **EC2 credentials and AWS session tokens**, likely for accessing victim environments｜**Server connection filtering** for connecting client based on **user-agent, ASN or geographic location**, likely for **geofencing connections to C2 infrastructure** and identifying the source country of victim assets |
| **Complete Mission** | Commands for searching emails in **Zimbra inboxes**｜Commands for listing Windows directories and files while **filtering out uninteresting files such as system-related files**｜**Python tooling for transferring data to a cloud bucket** |

**核心訊息**：這張圖的分布與 Figure 4 幾乎相反，**重心在中段（Move Laterally 與 Maintain Presence 各三項）**。這反映的是一個**已經進到環境裡、在不熟悉的技術棧中摸索**的行為者：vSphere、Kubernetes、EC2、macOS，全部是他不熟的地方。正文明說「attack surfaces they were unfamiliar with」。

**兩個特別值得講的項目**［分析］：

1. **`xp_dirtree` 與 `xp_cmdshell`**：這是 MS SQL Server 上兩個典型的後利用擴充預存程序，`xp_cmdshell` 可執行任意作業系統指令，`xp_dirtree` 常被用來觸發 SMB 連線以竊取 NTLM 雜湊。**這兩個名字一起出現，就足以判定這是一次 MS SQL 後利用**，而且是相當老派、有大量公開資料的手法。**AI 在這裡的價值不是提供新知識，而是替代查資料的時間。**
2. **「Server connection filtering based on user-agent, ASN or geographic location」**：這是**C2 基礎設施的地理圍籬（geofencing）**，目的是只接受來自目標國家的連線，讓資安研究者與沙箱連不上。這是成熟的 OPSEC 作法。同一句的後半「identifying the source country of victim assets」更有意思：**行為者想知道受害資產在哪一國**，這是一個明確的情報需求訊號。

**與 Figure 4 的並讀價值**：兩張圖放在一起，是一堂完整的「AI 在 kill chain 上的價值分布」課。Figure 4 的行為者用 AI 打門（周邊），Figure 6 的行為者用 AI 認路（內部不熟的技術棧）。**兩者都不是用 AI 做「新的攻擊」，而是用 AI 補自己的知識缺口。** 這正是 Anthropic 所說「AI 取代的是人力，不是知識」的另一種表述。

---

### 6.7 Figure 7（PDF p.16）：北韓 UNC1069 的 Gemini 濫用

**圖片類型**：**二欄清單圖**。左欄標題方框為綠色「Reconnaissance」，右欄為藍色「Delivery」。無流程箭頭、無環形結構，比 Figure 4 與 6 簡化很多。使用的是 **Lockheed Martin Cyber Kill Chain 的階段名稱**，而不是 Figure 4 與 6 的 Mandiant 六階段。

**逐欄內容（逐字）**：

| Reconnaissance | Delivery |
|---|---|
| Reconnaissance related to the location of users' **cryptocurrency wallet application data** | Craft **fraudulent instructions impersonating a software update** |
| Gain knowledge of **VPS providers** and possible alternatives for VPS providers | Generate **Spanish-language** work-related excuses and requests to reschedule meetings |
| Research the technical requirements (**optimal programming language, monitoring techniques, and tools**) to set up a Command & Control (C2) server | Create lure material and other messaging related to cryptocurrency |

**核心訊息**：只有六項，而且全部集中在**攻擊開始之前**。沒有任何一項與入侵後的行為有關。**這是一張「準備階段」的圖**，符合北韓加密貨幣竊盜行動的作業模式：社交工程佔絕大部分工作量，真正的技術入侵反而簡單。

**最值得單獨講的一格**：**「Generate Spanish-language work-related excuses and requests to reschedule meetings」**。這一格看起來最不起眼，卻是整份報告地緣影響最大的一項（見第 3.10.3 與第 10.4 節）。

**注意版型不一致**［分析］：Figure 4 與 Figure 6 用 Mandiant 六階段，Figure 7 與 Figure 8 用 Lockheed Kill Chain，Figure 9 與 Figure 10 又各自不同。**同一份報告內用了兩套不同的攻擊階段模型，且未說明理由。** 這在讀者做跨案例比較時會造成困擾，課堂上可以當成「報告製作品質」的討論題。

---

### 6.8 Figure 8（PDF p.16）：一個必須指出的重複問題

**圖片類型**：**五欄清單圖**，欄首標題為 Lockheed Martin Cyber Kill Chain 的階段：Reconnaissance、Weaponization、Delivery、Command and Control、Actions on Objectives。圖說為「Figure 8: PUKCHONG (aka UNC4899) misuse of Gemini across the attack lifecycle」。

**問題**：**這張圖的內容與 Figure 6（suspected China-nexus 行為者）幾乎完全相同**，只是換了階段標籤並刪去最後一欄。逐欄對照：

| Figure 8 的欄位（UNC4899，北韓） | 內容 | Figure 6 的欄位（China-nexus） |
|---|---|---|
| Reconnaissance | Research specific target identifiers；SQL injection on MS SQL server | **Initial Compromise（完全相同）** |
| Weaponization | Develop ASP and javascript webshells；xp_dirtree 與 xp_cmdshell | **Establish Foothold（完全相同）** |
| Delivery | Research into malware execution techniques on macOS... for gaining elevated privileges | **Escalate Privilege（完全相同）** |
| Command and Control | vSphere / govc；Linux system service；Kubernetes | **Move Laterally（完全相同）** |
| Actions on Objectives | CloudFlare TLS；EC2 credentials；server connection filtering | **Maintain Presence（完全相同）** |
| （無第六欄） | Figure 6 的 Complete Mission 三項未出現 | Complete Mission |

**本教材的判讀**［分析，這是本教材的原創發現，GTIG 未承認也未更正］：

1. **這極可能是版面製作時的複製貼上錯誤。** 兩個完全不同的行為者（一個是 suspected China-nexus，一個是北韓的 UNC4899），不可能在 Gemini 上留下逐字相同的行為清單。
2. **重新標籤的結果在語意上是錯的。** 「Research into malware execution techniques on macOS... for gaining **elevated privileges**」被放在 **Delivery** 欄，但它講的是提權；「Troubleshoot CloudFlare TLS certificate」被放在 **Actions on Objectives** 欄，但它講的是維持基礎設施。**如果這是刻意的重新對應，對應本身就不成立。**
3. **正文與圖不符。** UNC4899 的正文只說它「used Gemini for a variety of purposes including developing code, researching exploits, and improving their tooling」，並推測它在發展**邊界設備與現代瀏覽器**的能力。**圖上沒有任何一項與邊界設備或瀏覽器有關**，反而全是 MS SQL、vSphere、Kubernetes、macOS。

**這件事在課堂上的價值極高**，理由是它示範了本課程反覆強調的方法論：

> **圖表必須親自判讀，而且必須與正文交叉比對。** 如果只讀正文，這個問題看不出來；如果只看圖說，也看不出來。**必須把 Figure 6 與 Figure 8 並排逐條比對才會發現。**

**課堂練習（強烈推薦）**：把 Figure 6 與 Figure 8 的內容分別抄成兩張紙發下去，不告訴學員它們來自不同的行為者，請他們找出差異。多數學員會先發現「標籤不同」，再發現「內容一樣」，最後才會問「那到底哪一個才是 UNC4899 的？」**這個提問過程本身，就是情報分析訓練。**

**引用建議**：課堂與報告中引用 UNC4899 時，**只引用正文，不要引用 Figure 8 的內容**。並在第 12 節標明本教材已就此向讀者示警。

---

### 6.9 Figure 9（PDF p.17）：APT42 的 Gemini 濫用

**圖片類型**：**二欄清單圖**，左欄「Reconnaissance」（綠），右欄「Delivery」（藍）。全圖只有兩項，是全報告資訊密度最低的一張。

**逐欄內容（逐字）**：

| Reconnaissance | Delivery |
|---|---|
| Development and testing of a platform using **PII** to derive insights regarding **asset ownership, location, demographics, and behavior related to persons of interest** | Generate topical phishing material |

**核心訊息**：左欄那一句是全報告**唯一一句用「persons of interest（關注人員）」措辭的描述**，也是唯一一句明確指向**個人資料分析平台**的描述。四個分析維度（資產歸屬、位置、人口統計、行為）合起來就是一套標準的**人員檔案（profiling）**框架。

**版型的訊號**［分析］：GTIG 把這一項放在 **Reconnaissance** 欄。這是一個值得注意的分類選擇：**它把「建一個個資分析平台」視為攻擊前的偵察工作，而不是一個獨立的監控行動。** Anthropic 會把同樣的行為放進「監控行動」章節並給它一個 GTG 編號。**同一個行為，兩家用完全不同的分類架構去理解**，這是第 4.7 節的核心論點，這張圖是最直接的證據。

**課堂用法**：把 Figure 9 的左欄與本課程 `../03-surveillance/GTG-34007-iran-surveillance.html` 的 Arman 案件管理流水線並排，問學員：「這兩段描述的是不是同一類活動？如果是，為什麼一家叫它偵察、另一家叫它監控？」這個分類爭議直接影響**法遵、政策與處置強度**，沒有標準答案。

---

### 6.10 Figure 10（PDF p.18）：APT41 的 Gemini 濫用

**圖片類型**：**二欄清單圖**，欄首為「Installation」與「Command and Control」（Lockheed Kill Chain 的後段階段）。同樣只有兩項。

**逐欄內容（逐字）**：

| Installation | Command and Control |
|---|---|
| Technical assistance with an **obfuscation library** | Code development for **OSSTUN** C2 framework |

**核心訊息**：兩項都是**工具開發**，沒有任何一項與實際入侵行為有關。這張圖最有價值的資訊是 **OSSTUN 這個名字**，而它的來源是行為者自己的提示（正文：「a C2 framework called OSSTUN **by the actor**」）。

**這一格的情報價值**［分析］：一個 C2 框架的**內部代號**通常只有在拿到攻擊者的原始碼、對話紀錄或內部文件時才會知道。**模型供應商的提示遙測是一種取得這類「內部命名」情報的新管道。** 對防守方的實務意義是：以後在自家環境裡看到任何與 `OSSTUN` 相關的字串、埠號慣例或設定檔命名，就有一條可以往 APT41 對回去的線索。**但報告沒有給任何 OSSTUN 的技術特徵，所以這條線索目前只是一個名字。**

---

### 6.11 圖表的整體缺陷（本教材的評估）

［分析］把十張圖放在一起看，三個結構性缺陷值得在課堂上指出：

1. **階段模型不一致**：Figure 4 與 6 用 Mandiant 六階段，Figure 7、8、9、10 用 Lockheed Kill Chain，而且欄位數各不相同（2、5、2、2）。**跨案例比較因此變得困難。**
2. **資訊密度落差極大**：Figure 4 有 19 項，Figure 9 與 10 各只有 2 項。後兩張圖**沒有承載任何正文沒說的資訊**，實質上是排版裝飾。
3. **一張圖的內容是錯的**（Figure 8，見 6.8）。

**與 Anthropic 2026-09 報告的對比**：本課程 `../00-index.html` 第七節指出 Anthropic 報告有大量**關鍵數字只存在於圖片內、文字層抓不到**（例如「30 天 2,475 份成品」）。**GTIG 這一期完全相反：圖裡沒有任何正文沒有的數字，因為它根本沒有數字。** 這兩種圖表使用方式，代表兩種不同的報告哲學，值得在方法論課裡並排討論。

---

## 7. IOC 與技術指標

### 7.1 本報告沒有發布任何 IOC

**這是一個必須明確講清楚的事實**：GTIG 這一期**沒有 IOC 附錄、沒有雜湊值、沒有 C2 網域、沒有 IP、沒有 YARA 規則、沒有 Telegram 帳號**。全報告 20 頁裡唯一的網路位址，是 Gemini 官方 API 端點。

這與 GTIG 平常的做法不同：Mandiant 與 GTIG 的傳統威脅報告通常附有完整的指標表與偵測規則。**為什麼這一期沒有？**三個可能解釋［分析］：

1. **本期沒有 Mandiant 事件響應**（見第 2.2 節），所以沒有受害者端的鑑識產物可以發布。
2. **主要案例的基礎設施就是合法服務**：PROMPTFLUX 打 Gemini API，PROMPTSTEAL 打 Hugging Face，QUIETVAULT 外洩到 GitHub。**這些都不能封鎖**，發布出來也沒有防禦價值。
3. **檢體本身可能仍在調查中**，或 GTIG 選擇透過 Google Threat Intelligence 產品而非公開報告交付指標。

**這件事本身是教材**：**「AI 原生的濫用」正在系統性地削弱以 IOC 為核心的偵測模式。** 當攻擊流量的目的地是 `generativelanguage.googleapis.com`、`huggingface.co`、`github.com` 這種每個企業都必須放行的服務時，**網路層的封鎖清單就失去意義，防守必須下沉到端點的程序歸屬與行為關聯。**

### 7.2 報告中可用於偵測的技術指標（本教材整理）

雖然沒有 IOC 表，報告正文與圖表裡散落了一批**可以轉成偵測邏輯的技術指標**。下表由本教材整理，並加上「偵測價值與壽命」評估。

> **安全紅線說明**：下表中的 `generativelanguage.googleapis.com`、`huggingface.co`、`github.com` 是**合法廠商的官方服務端點**，不是攻擊者基礎設施，因此不做 defang（defang 反而會妨礙防守方直接套用）。本報告沒有提供任何攻擊者控制的網域或 IP，所以沒有需要 defang 的惡意指標。無論如何，**課堂上不應對任何指標做主動連線或查詢**。

| 指標 | 型別 | 來源 | 偵測價值與壽命 |
|---|---|---|---|
| `https://generativelanguage.googleapis.com/v1beta/models/<model>:generateContent?key=<key>` | 網路端點（合法） | Figure 1 原始碼 | **單獨無價值**（合法端點）。**與程序歸屬結合後價值極高**：若發起者是 `wscript.exe`、`cscript.exe`、`powershell.exe`、`mshta.exe` 等腳本宿主，或任何非瀏覽器、非已知 AI 應用的程序，即為高度可疑。**壽命長**，因為這是架構性訊號而非字串特徵 |
| `gemini-1.5-flash-latest` | 模型版本字串 | Figure 1 | **低**。`-latest` 標籤的設計就是為了在模型更迭時仍然有效，攻擊者也可隨時改成其他模型。**作為 hunting 關鍵字可用，作為封鎖依據不可用** |
| `%TEMP%\thinking_robot_log.txt` | 檔案路徑 | PDF p.5 與 Figure 1 | **高保真、極短壽**。這是 PROMPTFLUX 特定版本的除錯產物，改一個字串就失效。**只適合做一次性 sweep，不適合長期規則** |
| `thinking_robot`、`Thinging`、`StartThinkingRobot`、`CallGeminiAPI`、`AttemptToUpdateSelf` | 函式與字串名稱 | Figure 1 | **中偏高保真、短壽**。可寫成 YARA 字串規則掃 `.vbs`。攻擊者只要重新命名即失效，但由於 PROMPTFLUX 仍在開發階段，短期內可能有效 |
| `crypted_ScreenRec_webinstall` | 誘餌檔名 | PDF p.6 | **低**。單一檔名，且報告明說誘餌是「varied」。作為 hunting 起點可用 |
| `C:\Programdata\info\`、`C:\Programdata\info\info.txt` | 檔案路徑 | Figure 2 與 3 | **高保真、中等壽命**。這兩個路徑寫死在 PROMPTSTEAL 的提示裡，改動需要同步改提示。**建議直接做成端點規則：非系統程序在 `C:\Programdata\` 下建立名為 `info` 的目錄** |
| `Return only commands, without markdown` / `Return only command, without markdown.` | 提示字串 | Figure 2 與 3 | **本報告最有價值的靜態特徵**。它是 LLM 整合的**功能必需品**（沒有它，輸出會帶 Markdown 圍籬而無法直接執行），攻擊者要改也只能改寫法不能刪功能。**建議做成 YARA 的寬鬆變體集合**：`without markdown`、`only the code`、`no explanation`、`output only`。**壽命中等偏長**，但報告已說「new samples adding obfuscation」，提示可能被加密儲存 |
| `Qwen2.5-Coder-32B-Instruct` | 模型名稱 | PDF p.7 | **中**。作為 hunting 關鍵字（在檢體字串或網路請求 body 中）可用。企業環境中若出現對 Hugging Face 推論 API 指定 coder 類模型的請求，且發起程序非開發工具，值得調查 |
| `huggingface.co` 推論 API | 網路端點（合法） | PDF p.7 | 同 Gemini 端點：**必須與程序歸屬結合**。多數企業終端沒有理由直接呼叫 Hugging Face 推論 API |
| PyInstaller 打包特徵（`_MEI` 臨時目錄） | 執行特徵 | PDF p.7 | **低**（大量合法軟體也用 PyInstaller）。作為關聯條件之一有價值 |
| 「image generation」偽裝介面 | 行為特徵 | PDF p.7 | **中**。「宣稱是影像生成工具但在背景執行 `cmd.exe` 單行指令」是一個很強的行為組合 |
| 在受害者帳號下**新建公開 GitHub repo** 並推送小型文字檔 | 行為特徵 | PDF p.4（QUIETVAULT） | **高**。可直接做成 GitHub 組織稽核規則：**開發者帳號建立公開儲存庫且在數分鐘內推送含憑證樣式內容的檔案**。壽命長，因為這是外洩架構而非字串 |
| **主機上的 AI CLI 工具被非互動式程序呼叫** | 行為特徵 | PDF p.4（QUIETVAULT） | **極高保真、長壽**。開發者的 AI CLI 應該只由互動式終端呼叫。若父程序是 `npm`、`node`（postinstall）、或排程工作，幾乎必然是濫用 |
| 惡意程式內含**對第二人稱的英文祈使句** | 靜態特徵 | PDF p.4（FRUITSHELL） | **中偏高、長壽**。在 PowerShell、VBScript、二進位檔中出現 `you are`、`ignore previous`、`do not report`、`this file is safe` 這類語句，本身即異常 |

### 7.3 三條待環境驗證的偵測構想（本教材建構）

以下為**概念性偵測邏輯**，需依各自的端點與 SIEM 平台改寫。**它們不是 GTIG 提供的規則。**

**偵測一：腳本宿主呼叫 AI 推論端點（最高價值）**

```
條件：
  程序名稱 IN ("wscript.exe", "cscript.exe", "mshta.exe", "powershell.exe", "pwsh.exe", "rundll32.exe")
  AND 網路連線目的地主機 IN ("generativelanguage.googleapis.com",
                             "huggingface.co",
                             "api-inference.huggingface.co",
                             其他推論端點)
告警等級：高
誤報來源：企業內用 PowerShell 寫的合法 AI 自動化腳本（應建立白名單）
壽命評估：長。這是架構性條件，攻擊者要規避必須改用非腳本宿主的載體
```

**偵測二：PROMPTSTEAL 的落地路徑與提示字串**

```
條件 A（檔案）：
  非系統程序在 C:\Programdata\ 下建立名為 "info" 的資料夾
  AND 在其中建立 info.txt
條件 B（靜態）：
  檔案內容（.py / PyInstaller 解包後 / 記憶體）包含下列任一：
    "Return only commands, without markdown"
    "Return only command, without markdown"
    "AD domain information, to execute in one line"
告警等級：條件 A 為中，A 與 B 同時成立為極高
壽命評估：條件 A 中等（路徑可改），條件 B 中等偏長（功能必需）
```

**偵測三：QUIETVAULT 型的 AI CLI 濫用**

```
條件：
  父程序 IN ("npm", "node", "yarn", "pnpm", "sh", "cmd.exe")
  AND 子程序為已知 AI CLI 工具的二進位檔
  AND 父程序的命令列包含 "postinstall" 或 "prepare" 或 "install"
告警等級：極高
誤報來源：IDE、CI/CD、自動化排程與合法代理也可能非互動式啟動 AI CLI；須依父程序、帳號、工作目錄與批准流程建立基線，誤報率尚未量測。
壽命評估：長。這是「借用受害者已登入工具」這個手法的結構性特徵
補強：同時監控 GitHub 組織稽核日誌中「新建公開儲存庫」事件
```

**三條規則的共通設計原則**［分析］：**沒有一條依賴攻擊者控制的字串。** 它們全部建立在「哪個程序做了什麼事」的結構關係上。這是面對「AI 原生濫用」時唯一可持續的偵測策略，因為這類濫用的所有網路目的地都是合法服務、所有內容都是動態生成的。

---

## 8. GTIG 與 Google 的偵測、處置與防線缺口

### 8.1 做了什麼：五個 Mitigations 方塊的統一模式

本報告在五處放了獨立的「Mitigations」方塊（PDF p.6、p.8、p.10、p.12、p.14、p.16、p.18）。它們的措辭高度重複，這個重複本身是訊號［分析］。

**標準三段式**：

1. **停用資產**：「Google has taken action against this actor by **disabling the assets associated with this activity**.」
2. **回饋到模型與分類器**：「Google DeepMind has also used these insights to further strengthen our protections against such misuse by **strengthening both Google's classifiers and the model itself**. This enables the model to **refuse to assist with these types of attacks moving forward**.」
3. **降溫**：多數方塊加一句「These activities are **similar to our findings from January** that detailed how bad actors are leveraging Gemini for **productivity vs. novel capabilities**.」

**兩個值得注意的變體**：

- **TEMP.Zagros 那一則**多了一句：「Google took **additional, broader action to disrupt the threat actor's campaign based on their operational security failures**.」這是唯一一次提到超出「停用帳號」的處置，直接源自行為者把 C2 網域與金鑰交給了 Gemini（見第 3.8 節）。
- **IO 那一則**多了一句明確的負面結論：「For observed IO campaigns, **we did not see evidence of successful automation or any breakthrough capabilities**.」

### 8.2 Google 端的防線體系（PDF p.19「Building AI Safely and Responsibly」）

報告最後一節列出六項防線與投資，逐項抄錄並加上評估：

| 項目 | 報告的描述 | ［分析］評估 |
|---|---|---|
| **AI Principles ＋ 禁止使用政策** | 「Our policy guidelines and prohibited use policies prioritize safety and responsible use」 | 政策層，非技術防線。對已決意濫用者無效 |
| **分類器與模型層雙重更新** | 「These changes, which can be made to **both our classifiers and at the model level**, are essential to maintaining agility in our defenses」 | **這是最實質的一段**。承認防線有兩層、且更新節奏不同：分類器可快速迭代，模型層要等下一次訓練 |
| **Google DeepMind 的威脅建模與紅隊** | 「a **robust evaluation framework that can automatically red team an AI vulnerability to indirect prompt injection attacks**」 | 針對**間接提示注入**的自動化紅隊。與 FRUITSHELL 那條線直接相關，但報告沒有把兩者連起來 |
| **SAIF（Secure AI Framework）** | 「a conceptual framework to secure AI systems」，含開發者工具包 | 業界框架。2026-05 那一期已經用 SAIF 分類法（IIC、RA）描述具體事件，本期只是提及 |
| **Big Sleep** | 「an AI agent developed by Google DeepMind and Google Project Zero, that actively searches and finds unknown security vulnerabilities」。報告說它「found its first real-world security vulnerability and **assisted in finding a vulnerability that was imminently going to be used by threat actors, which GTIG was able to cut off beforehand**」 | **這一句是全報告最重要的攻防對稱性主張**：防守方也在用 AI 找零日，而且搶先攔下了一次。但報告**沒有給出那個漏洞的任何細節**，無法驗證 |
| **CodeMender** | 「an experimental AI-powered agent utilizing the advanced reasoning capabilities of our Gemini models to **automatically fix critical code vulnerabilities**」 | 從「找漏洞」走向「修漏洞」。標示為 experimental |
| **白皮書**《Advancing Gemini's Security Safeguards》 | 在執行摘要中連結 | 本教材未取得該白皮書全文，見第 12 節 |

**「Big Sleep 搶先攔下一個即將被利用的漏洞」這句話，是整份報告最值得放進課程結尾的一句**［分析］。它把整份報告的敘事從「對手在用 AI」翻轉成「雙方都在用 AI，而且防守方在某些賽道上是領先的」。GTIG 2026-05 那一期把這條線推得更遠（首度攔下 AI 開發的零日並完成責任揭露）。**兩期並讀，可以教「AI 攻防的非對稱性到底往哪一邊傾斜」這個開放問題。**

### 8.3 防線缺口：報告自己暴露的與報告沒說的

**(a) 報告自己承認的**

1. **人設前綴有效**（PDF p.8）：Gemini 先拒絕，改稱 CTF 參賽者後就給了可用於利用系統的資訊。**GTIG 沒有說這個問題後來是否被修好**，只說「we have since strengthened both classifiers and the model itself」。
2. **良性與濫用無法從請求本身區分**（PDF p.8）：「if normally posed by a participant of the CTF vs. a threat actor, would be benign inquiries」。這是**結構性限制的自承**，不是實作缺陷。
3. **IO 的效果無法驗證**（PDF p.18）：「we have not identified these generated articles in the wild」。這其實也是一個偵測缺口的自承：**平台側看得到生產，看不到流通。**

**(b) 報告沒說、但可以從文本推出的缺口**［分析］

| 缺口 | 依據 | 意涵 |
|---|---|---|
| **處置只能停用「已知」資產** | 所有 Mitigations 方塊都只說 disabling the assets | PROMPTFLUX 的變體已經散布到可移除磁碟與網路共享。**API key 被撤銷之後，那些已經落地的腳本不會消失，只是不再更新自己** |
| **對「不用自家模型」的濫用完全無能為力** | APT28 選用 Hugging Face 上的 Qwen | **這是本報告最大的結構性盲區**。GTIG 能看到 PROMPTSTEAL 這個檢體，是因為它拿到了樣本，而不是因為它有遙測 |
| **沒有跨供應商的濫用關聯機制** | 全報告沒有提到與其他模型供應商的情報共享 | 一個行為者同時用 Gemini 做偵察、用 Hugging Face 上的開源模型跑 payload、在地下市場買 WormGPT，**三家各自只看到三分之一** |
| **偵測管線本身可能被提示注入** | FRUITSHELL 的存在 | 報告提到 DeepMind 有間接提示注入的自動化紅隊框架，但**沒有說明自家的惡意程式分析管線是否經過同樣的測試** |
| **共享檢體庫的污染** | PROMPTLOCK 事件 | GTIG 把一個學術研究檢體收進「2025 年偵測到的惡意程式」表。**這暴露了樣本來源的驗證環節不足** |
| **沒有量化指標** | 全報告無任何數字 | 無法評估處置的覆蓋率、無法評估趨勢、無法與其他期比較。**這也讓外界無法檢驗「我們已經強化了」這類主張** |

### 8.4 一個值得單獨討論的處置倫理問題

TEMP.Zagros 把 C2 網域與加密金鑰交給 Gemini，Google 據此做了「broader action to disrupt the threat actor's campaign」。

**這件事在課堂上值得辯論**［分析］：

- 模型供應商從使用者提示中取得的資訊，**能不能用於超出「停用該帳號」的處置**？
- 如果可以，界線在哪裡？（通報執法？主動 sinkhole 那個 C2？通知可能的受害者？）
- 這與**一般使用者對提示隱私的期待**如何調和？多數人不會預期自己貼進模型的程式碼會被用於任何形式的行動。
- 對照：本課程 `../07-distillation/00-distillation-intro-and-mitigations.html` 討論的蒸餾偵測，同樣建立在「供應商可以分析使用者流量」這個前提上。**兩者是同一個治理問題的兩個面向。**

這個討論沒有標準答案，但它是**任何要導入企業級 LLM 的組織都必須先想清楚的問題**，對台灣的金融、醫療、政府採購尤其相關。

---

## 9. 第三方驗證與外部來源

### 9.1 本報告的情報來源性質

**大部分是單一來源情報**，但層次比 Anthropic 報告複雜一些。逐案評估：

| 案例／主張 | 是否為單一來源 | 佐證情況 |
|---|---|---|
| **PROMPTSTEAL / APT28** | **否，有獨立佐證** | CERT-UA 2025-07-17 以 LAMEHUG 之名獨立公告，早於 GTIG。多家廠商發布獨立技術分析 |
| **PROMPTFLUX** | **是**（GTIG 單一來源） | 無任何第三方獨立取得檢體的公開紀錄。媒體報導全部轉述 GTIG |
| **PROMPTLOCK** | **否，且原始判斷被修正** | ESET 獨立發現，NYU 出面確認為學術專案 |
| **QUIETVAULT** | **部分** | GTIG 描述為單一來源；第三方把它連到 2025-08 的 Nx npm 事件，但**連結本身不是 GTIG 說的** |
| **FRUITSHELL** | **是** | 報告只有兩行，無任何外部佐證 |
| **CTF 前綴繞過** | **是** | 平台側遙測，外界無法驗證 |
| **TEMP.Zagros 的 OPSEC 失誤** | **是** | 同上。這類「攻擊者在我們平台上做了什麼」的主張，**本質上不可能被外部驗證** |
| **地下市場的 10 個工具** | **否，有大量獨立佐證** | WormGPT、FraudGPT、Xanthorox 均有 Trustwave、Trend Micro、SiliconANGLE 等多家獨立研究 |
| **各國家級行為者的 Gemini 使用細節** | **是** | 平台側遙測 |

**教學結論**：**本報告的可驗證性呈現兩極分布。** 惡意程式與地下市場這兩塊有相當好的外部佐證；「行為者在 Gemini 上做了什麼」這一塊**完全無法驗證**，只能選擇相信或不相信 GTIG。引用時必須分開處理。

### 9.2 外部來源清單

| 來源 | URL | 日期 | 性質 |
|---|---|---|---|
| GTIG 部落格原文 | https://cloud.google.com/blog/topics/threat-intelligence/threat-actor-usage-of-ai-tools | 2025-11-06（頁面標示） | **一手** |
| GTIG PDF 版 | https://services.google.com/fh/files/misc/advances-in-threat-actor-usage-of-ai-tools-en.pdf | PDF 內嵌時間戳 2025-11-05 | **一手**（本教材主要依據） |
| CERT-UA LAMEHUG 公告（經 The Hacker News 轉述） | https://thehackernews.com/2025/07/cert-ua-discovers-lamehug-malware.html | 2025-07 | **獨立查證**。CERT-UA 為烏克蘭國家級 CERT，獨立於 Google |
| Cato Networks CTRL 的 LAMEHUG 分析 | https://www.catonetworks.com/blog/cato-ctrl-threat-research-analyzing-lamehug/ | 2025-07 起 | **獨立查證**（自行分析檢體） |
| Picus Security 的 LAMEHUG 分析 | https://www.picussecurity.com/resource/blog/lamehug-the-first-publicly-documented-case-of-a-malware-integrating-a-llm | 2025-07 起 | **獨立查證** |
| SOC Prime 的 UAC-0001 偵測內容 | https://socprime.com/blog/detect-uac-0001-attacks-with-lamehug/ | 2025-07 起 | **獨立查證**（提供偵測規則） |
| CyberScoop：PromptLock 出自 NYU | https://cyberscoop.com/ai-ransomware-promptlock-nyu-behind-code-discovered-by-security-researchers/ | 2025-08／09 | **獨立查證**。直接推翻 ESET 的原始定性 |
| NYU Tandon 官方新聞稿（Ransomware 3.0） | https://engineering.nyu.edu/news/large-language-models-can-execute-complete-ransomware-attacks-autonomously-nyu-tandon-research | 2025 | **一手**（研究團隊自述） |
| SC Media：PromptLock 由 NYU 研究員開發 | https://www.scworld.com/brief/novel-promptlock-ransomware-developed-by-nyu-researchers | 2025 | **獨立查證** |
| Axios：〈AI-powered malware is here〉 | https://www.axios.com/2025/11/05/google-ai-cybersecurity-malware-report | 2025-11-05 | **僅引述 GTIG**。值得注意的是**日期為 11-05**，與部落格標示的 11-06 不同 |
| SiliconANGLE | https://siliconangle.com/2025/11/05/google-warns-new-era-self-evolving-ai-driven-malware-begun/ | 2025-11-05 | **僅引述 GTIG** |
| The Hacker News：PROMPTFLUX 報導 | https://thehackernews.com/2025/11/google-uncovers-promptflux-malware-that.html | 2025-11 | **僅引述 GTIG** |
| Cybersecurity Dive：〈AI-based malware makes attacks stealthier and more adaptive〉 | https://www.cybersecuritydive.com/news/ai-powered-malware-google/804760/ | 2025-11 | **僅引述 GTIG，但收錄了 Marcus Hutchins 的反面意見** |
| IT Pro：〈Google says you shouldn't worry about AI malware〉 | https://www.itpro.com/business/google-says-leading-ai-malware-strains-are-nowhere-near-good-enough-yet-but-that-wont-last-long-as-hackers-refine-techniques | 2025-11 | **僅引述 GTIG**，但標題正確反映了報告的降溫語氣 |
| 《資安人科技網》（台灣）：〈AI 驅動惡意軟體時代來臨！Google 揭露可自我重寫程式碼的新型威脅〉 | https://www.informationsecurity.com.tw/article/article_detail.aspx?aid=12458 | 2025-11 | **僅引述 GTIG**。台灣主要資安媒體的報導 |
| Trend Micro：Xanthorox 分析 | https://www.trendmicro.com/vinfo/us/security/news/cybercrime-and-digital-threats/the-devil-reviews-xanthorox-a-criminal-focused-analysis-of-the-latest-malicious-llm-offering | 2025 | **獨立查證**（Figure 5 的工具之一） |
| Trustwave SpiderLabs：WormGPT 與 FraudGPT | https://www.trustwave.com/en-us/resources/blogs/spiderlabs-blog/wormgpt-and-fraudgpt-the-rise-of-malicious-llms/ | 2023 起 | **獨立查證** |
| SiliconANGLE：Xanthorox 出現 | https://siliconangle.com/2025/04/07/xanthorox-ai-emerges-new-malicious-threat-cybercrime-communities/ | 2025-04-07 | **獨立查證** |
| Splunk Security Content：QuietVault Analytics Story | https://research.splunk.com/stories/quietvault/ | 2025 起 | **獨立查證**（提供偵測內容） |

### 9.3 最重要的一條反面意見

**Marcus Hutchins 對 PROMPTFLUX 的批評**［外部，經 Cybersecurity Dive 等媒體轉述］：他指業界在「overblowing the significance of AI slop malware」，具體指出三點：

1. 惡意程式裡的提示**假設 Gemini 天生知道怎麼繞過防毒**，但模型並不具備這種知識。
2. **沒有任何熵源**能確保每次「自我改寫」的產出真的與前一版不同。
3. **沒有任何護欄**確保生成的程式碼真的可執行；而且那個函式**根本是被註解掉的、沒有在用**。

**本教材的評估**［分析］：這三點**與 GTIG 自己在報告裡寫的降溫語句方向一致**，而且第三點可以從 Figure 1 的原始碼直接目視確認（見第 6.1 節）。**因此這不是「研究者與廠商對立」的情況，而是「媒體標題與報告內容脫節」的情況。** 課堂上應該把 GTIG、Hutchins、媒體三方的說法並排，讓學員自己判斷是誰誇大了。

**這也是本教材推薦的第 1 節速覽第 4 點的完整依據。**

---

## 10. 課程教學設計

### 10.1 核心教學要點

**要點一：把「AI 濫用」拆成開發期與執行期兩個威脅面**

這是本份報告對課程最大的貢獻。整個 Anthropic 2026-09 報告（以及本課程模組 01 到 08）講的都是**開發期**：攻擊者在自己這一側用 AI 做工程、偵察、編排。GTIG 這一期補上了**執行期**：AI 元件被放進 payload，在受害者的機器上運作。

兩者的防禦著力點完全不同：

| | 開發期 AI 濫用 | 執行期 AI 濫用 |
|---|---|---|
| AI 在哪裡跑 | 攻擊者的環境 | **受害者的環境** |
| 誰付錢 | 攻擊者（或被偷的金鑰持有者） | **視情況**：硬編碼金鑰是攻擊者的，QUIETVAULT 型則是受害者的 |
| 平台側看得到什麼 | 攻擊者的提示與工作流 | **受害者機器發出的請求**，內容可能完全良性 |
| 封鎖帳號的效果 | 能中斷該行動 | **只能中斷該版本**；C2 可更新金鑰 |
| 主要偵測面 | 模型供應商的帳號行為分析 | **端點：程序歸屬 ＋ 出站連線目的地** |
| 本課程對應教材 | 模組 01 至 08 全部 | **本教材 ＋ `gtig-2026-05-ai-threat-tracker.html`（PROMPTSPY）** |

**要點二：狀態欄比描述欄重要**

用 Table 1 教學員讀威脅報告時先找「這件事到底發生了沒有」。五支惡意程式裡，只有一支的 AI 元件是它運作的核心且真的用於實戰。

**要點三：柵欄的失效是結構性的，不是實作性的**

GTIG 的 CTF 案例與 Anthropic 的「overcome on further prompting」是同一個現象在兩家平台上的獨立觀察。**同樣的請求，在不同身分的人手上有不同的性質，而身分不在文字裡。** 這是一個無法靠更好的分類器解決的問題，只能靠存取層（身分驗證、企業租戶）、行為層（跨輪狀態保存）與事後層（處置與調查）分攤。

**要點四：模型供應商正在變成一種新的情報蒐集面**

TEMP.Zagros 把 C2 網域與加密金鑰貼進 Gemini。這件事對三種讀者有三種意義：

- **CTI 分析師**：多了一種情報來源，但拿不到原始資料，且有「越謹慎的對手越隱形」的偏差。
- **紅隊與資安工程師**：**你自己的工具原始碼貼進外部 LLM 時，面對的是完全相同的結構。**
- **治理與法遵**：組織需要明確的政策界定什麼可以貼、貼到哪裡。

**要點五：IOC 模式正在失效，偵測必須下沉到程序關係**

本報告沒有任何 IOC，而且這不是疏漏。當攻擊流量的目的地是每個企業都必須放行的服務時，網路封鎖清單失去意義。第 7.3 節的三條偵測邏輯全部建立在「哪個程序做了什麼」而非「連到哪個網址」。

**要點六：圖表要親自看，而且要交叉比對**

Figure 8 與 Figure 6 的重複問題（第 6.8 節），只有把兩張圖並排逐條比對才會發現。這是本課程方法論原則的一個現成案例。

### 10.2 課堂討論題（皆無標準答案）

**討論題一：誰誇大了？**

GTIG 在報告裡明寫 PROMPTFLUX「does not have the ability to compromise a victim network or device」，Marcus Hutchins 說業界在炒作「AI slop malware」，而全球媒體標題是「AI 惡意程式時代來臨」。**如果你是一家台灣企業的資安長，讀到這三種說法，你會調整什麼防禦投資？如果什麼都不調整，你要怎麼對董事會解釋？**

延伸：**廠商在報告裡寫下降溫語句，是否就免除了被媒體誤讀的責任？**

**討論題二：PROMPTLOCK 的責任歸屬**

NYU 的研究團隊把勒索軟體概念驗證上傳到 VirusTotal 做測試，ESET 據此宣布「第一個 AI 勒索軟體」，GTIG 把它收進「2025 年偵測到的惡意程式」表。**這條錯誤資訊鏈上，誰應該負責？**

- 研究團隊應不應該在上傳前標記樣本、或根本不上傳？
- 廠商應不應該在宣布「第一個」之前先做溯源？
- GTIG 應不應該在得知 NYU 澄清後更正報告？

延伸：**如果你的 SOC 的威脅情資摘要引用了這一筆，你的內部更正流程會怎麼運作？**

**討論題三：模型供應商可以拿使用者的提示做什麼？**

Google 用 TEMP.Zagros 貼進 Gemini 的 C2 網域與加密金鑰，執行了「broader action to disrupt the threat actor's campaign」。**這個行動的正當性界線在哪裡？**

- 停用帳號：多數人會同意。
- 通報執法機關：多數人可能同意。
- 主動對那個 C2 採取行動：爭議開始出現。
- 那如果今天是一家台灣企業的紅隊，把內部工具貼進去除錯呢？

延伸：這與蒸餾偵測（`../07-distillation/00-distillation-intro-and-mitigations.html`）建立在同一個前提上。**如果你反對其中一個，你能不能一致地反對另一個？**

**討論題四：兩份十一月報告**

GTIG 在 2025-11-05/06 說 AI 惡意程式「still nascent」「toward more autonomous」，Anthropic 在 2025-11-13 說發現了「first reported AI-orchestrated cyber espionage campaign」。**一週之內，兩家頂尖機構對同一個問題給出了強度差異極大的答案。**

- 這是觀測差、定義差，還是立場差？
- 如果你只能選一家的說法寫進你的年度威脅評估，你選哪一家？為什麼？
- **如果兩家的商業位置對調，你認為報告的語氣會不會對調？**（這一題要求學員明確標示哪些是推論。）

**討論題五：APT28 為什麼選開源模型？**

APT28 用竊來的 Hugging Face token 呼叫 Qwen2.5-Coder-32B-Instruct，而不是任何一家前沿商業模型。

- 這是**能力取捨**（開源模型較弱但沒柵欄）還是**OPSEC 取捨**（避開商業供應商的遙測）？
- **如果答案是後者，那麼「前沿模型的柵欄越嚴，濫用越會轉移到開源模型」這個推論成立嗎？**
- 如果成立，模型供應商的柵欄投資對**整體社會的風險降低**有多少實質貢獻？

延伸對照：本課程 `../05-bio/case2-weak-model-limit.html` 記錄了 Anthropic 的分類器把請求「降載到最弱模型」的外溢效應。**這是同一個現象在不同尺度上的表現。**

**討論題六：Figure 8 該怎麼處理？**

假設你是一家台灣 CTI 廠商的分析師，你發現一份 Google 報告的圖表內容重複、標籤錯置，而且與正文不符。

- 你會不會對外發表這個發現？
- 你會不會先私下聯繫 GTIG？
- 如果你的客戶已經根據那張圖建立了 UNC4899 的 TTP 檔案，你的更正通知要怎麼寫？
- **一份報告裡有一張錯圖，會不會影響你對其他九張圖的信任？應不應該影響？**

### 10.3 桌面演練建議（可在教室安全執行）

五個演練全部只用本教材抄錄的文字，**不需要也不應該連線、下載或執行任何東西**。各演練的詳細鋪陳見對應的圖表判讀小節。

| # | 演練 | 時間 | 材料 | 任務與講評重點 |
|---|---|---|---|---|
| 一 | **狀態欄盲測**（暖身） | 15 分 | Table 1 五列，遮住 Status 欄（第 3.1 節） | 依 Description 判斷哪幾支是實戰、哪幾支是實驗。多數人會因描述最精彩而誤判 PROMPTFLUX。揭曉後給 Figure 1 原始碼，讓他們看到 `AttemptToUpdateSelf` 是註解掉的 |
| 二 | **提示字串的比對與誤報驗證** | 30 分 | 第 6.2 節的來源片段與合法對照文字 | 比較整句、片語與上下文條件的涵蓋率及誤報；不預設 `without markdown` 等正常格式要求可以單獨認定惡意 |
| 三 | **程序歸屬偵測與誤報盤點** | 45 分 | 第 7.3 節的偵測一 | 分組列出自家組織所有合法會呼叫 AI 推論端點的程序，評估誤報量並收斂條件。**多數組織會發現自己根本不知道有多少程序在呼叫 LLM API，這個盤點的價值高於規則本身** |
| 四 | **圖表交叉比對**（最推薦） | 30 分 | 第 6.6 與 6.8 節的兩張表，分別印出、不說來源 | 找出異同並回答「這兩份資料能不能同時為真？」揭曉後討論「只讀正文我會發現嗎」與「我平常引用廠商圖表時做過幾次這種比對」 |
| 五 | **地下市場的商業模式分析** | 30 分 | 第 6.5 節 Figure 5 矩陣 ＋ Table 2 | 從能力分布推論主要買家在做什麼生意（答案是釣魚與詐騙，不是入侵），並指出 KYC 繞過那一列如何直接對應台灣的帳戶開立詐欺與人頭帳戶問題 |

### 10.4 對台灣的意涵

**(1) 語言門檻消失，台灣的「繁體中文護城河」已經不存在**

本報告最該讓台灣讀者注意的一句，是北韓 UNC1069 用 Gemini 生成**西班牙語的工作藉口與改期會議請求**（PDF p.14），GTIG 的評語是「demonstrating how threat actors can **overcome the barriers of language fluency to expand the scope of their targeting**」。

這對台灣的推論非常直接［分析］：

- 過去台灣組織在面對非中文圈攻擊者時，**繁體中文（以及台灣特有的用語、職場慣例、公文格式）是一層天然的篩選器**。拙劣的簡繁轉換、中國用語、翻譯腔，都是資安意識訓練裡的經典指標。
- **這層篩選器正在快速失效。** LLM 不只能寫出通順的繁體中文，還能模仿特定的公文語氣、學術用語、產業術語。
- **實務建議**：資安意識訓練必須**停止教「看錯字和怪語法」**，改教**流程性驗證**（金流變更一律電話回撥既有號碼、附件一律在隔離環境開啟、任何要求繞過既有流程的請求一律視為紅旗）。**語言線索已經不是可靠訊號。**

**(2) 東亞郵件伺服器是明確的攻擊面**

Figure 4 顯示 China-nexus 行為者用 Gemini 寫腳本掃描**政府網域**上有漏洞的 **Roundcube 與 Zimbra** 郵件伺服器，並進行「mass exploitation using n-day exploits」。

- **Roundcube 與 Zimbra 在台灣的公部門、學術網路與中小企業有相當的部署量。**
- 關鍵字是 **n-day**：這些不是零日，是**已經有修補程式但沒裝**的漏洞。**AI 在這裡提供的 uplift 純粹是掃描與利用的規模與速度。**
- **實務建議**：把郵件伺服器（含 webmail 元件）的修補節奏提升到與 VPN、防火牆同級。這是一個**不需要任何 AI 相關投資就能防住的攻擊面**。

**(3) 開發者憑證與 CI/CD 是新的第一梯隊目標**

QUIETVAULT 竊取 GitHub 與 npm token，並用主機上的 AI CLI 工具搜尋其他機密。台灣的軟體業、金融科技與半導體供應鏈大量使用這套工具鏈。

- **實務建議一**：把 **AI 服務的 API token 納入與雲端金鑰同級的管理**（集中保管、定期輪替、最小權限、外洩掃描）。多數組織目前把 AI token 當成「開發者自己的東西」。
- **實務建議二**：**稽核 npm/pnpm 的 `postinstall` 腳本**，並在 CI/CD 中禁用或沙箱化。
- **實務建議三**：GitHub 組織層級啟用「新建公開儲存庫」的稽核告警（見第 7.3 節偵測三）。

**(4) 地下 AI 工具市場對應的是詐騙，不是入侵**

Figure 5 的能力分布顯示，這個市場的重心是**釣魚**與**程式碼生成**，而 Table 2 明列 deepfake 可用於「bypass know your customer (KYC) security requirements」。

- 這與台灣當前最嚴重的 AI 相關危害**完全對得上**：**投資詐騙、人頭帳戶、深偽名人代言、假交友**。
- 對照本課程 `../06-scams/GTG-15001-dating-app-network.html`（中國交友 app 網絡，4,700+ AI 人設）。
- **實務建議**：金融機構的 eKYC 流程必須假設**攻擊者手上有現成的、訂閱制的 deepfake 服務**。活體偵測（liveness detection）不能只做單一模態，且要能抵抗重放。

**(5) 台灣沒有被本報告點名，但這不是好消息**

**GTIG 這一期完全沒有提到台灣**（沒有台灣的受害者、沒有以台灣為目標的行動、沒有台灣的行為者）。對照之下，Anthropic 2026-09 報告有兩案直接點名台灣（`../03-surveillance/GTG-14020-religious-affairs-taiwan-church.html` 的長老教會、`../03-surveillance/GTG-14022-public-opinion-monitoring-taiwan.html` 的政治人物），一案模擬攻擊台灣 12 個目標（`../04-weapons/GTG-17002-ew-sead-taiwan.html`）。

**這個落差要怎麼解釋**［分析］：

- **不是因為台灣沒有被鎖定**，而是因為 GTIG 這一期的案例選擇偏向惡意程式與全球性的地下市場，而且**沒有監控章節**。
- **更重要的是**：針對台灣的監控與影響力行動，攻擊者未必使用 Gemini。GTIG 只看得到 Gemini。
- **課堂結論**：**「某份報告沒提到台灣」不能推論成「台灣風險較低」。** 要評估台灣面對的 AI 濫用風險，必須把多家報告疊起來看，這正是模組 09 的存在理由。

**(6) 給台灣 CTI 團隊的一條具體建議**

CERT-UA 在 2025-07 就公告了 LAMEHUG，GTIG 在 11 月才以 PROMPTSTEAL 之名納入。**國家級 CERT 的公告往往早於大廠報告四個月以上。** 台灣的 CTI 團隊若只追蹤 Google、Microsoft、Mandiant、CrowdStrike 的報告，會系統性地落後。**建議把 CERT-UA、ENISA、JPCERT/CC、KrCERT 等國家級 CERT 的公告納入固定掃描來源**，這是一個成本極低、效益明確的調整。

---

## 11. 關鍵原文引文

以下八條供講義直接引用，均標註 PDF 頁序。

**引文一：本報告的頭條主張（PDF p.3）**

> 「For the first time, GTIG has identified malware families, such as PROMPTFLUX and PROMPTSTEAL, that use Large Language Models (LLMs) during execution. These tools dynamically generate malicious scripts, obfuscate their own code to evade detection, and leverage AI models to create malicious functions on demand, rather than hard-coding them into the malware. While still nascent, this represents a significant step toward more autonomous and adaptive malware.」

> 譯：GTIG 首次辨識出 PROMPTFLUX、PROMPTSTEAL 這類**在執行期使用大型語言模型**的惡意程式家族。這些工具會動態生成惡意腳本、混淆自身程式碼以規避偵測，並利用 AI 模型**按需產生惡意功能**，而不是把功能硬編碼在惡意程式裡。雖然仍在萌芽階段，這代表朝向**更自主、更能適應的惡意程式**邁出了重要一步。

**引文二：PROMPTSTEAL 的歷史定位（PDF p.7）**

> 「In June, GTIG identified the Russian government-backed actor APT28 (aka FROZENLAKE) using new malware against Ukraine we track as PROMPTSTEAL and reported by CERT-UA as LAMEHUG... **APT28's use of PROMPTSTEAL constitutes our first observation of malware querying an LLM deployed in live operations.**」

> 譯：六月，GTIG 辨識出俄羅斯政府支持的行為者 APT28（別名 FROZENLAKE）對烏克蘭使用一支新惡意程式，我們追蹤為 PROMPTSTEAL，CERT-UA 則以 LAMEHUG 之名通報。**APT28 對 PROMPTSTEAL 的使用，構成我們首次觀察到「查詢 LLM 的惡意程式被部署於實際行動」。**

**引文三：PROMPTFLUX 的降溫聲明（PDF p.6）**

> 「Our intelligence also indicates this activity is **in a development or testing phase, as opposed to being used in the wild**, and **currently does not have the ability to compromise a victim network or device**.」

> 譯：我們的情報也顯示，這項活動**處於開發或測試階段，而非實際在野外使用**，而且**目前不具備攻陷受害者網路或裝置的能力**。

**引文四：柵欄被一句話繞過（PDF p.8）**

> 「In one interaction, the actor asked Gemini to identify vulnerabilities on a compromised system, but received a safety response from Gemini that a detailed response would not be safe. The actor then continued, **reframing the prompt by depicting themselves as a participant in a capture-the-flag (CTF) exercise**... When prompted to help in a CTF exercise, **Gemini returned helpful information that could be misused to exploit the system**.」

> 譯：在一次互動中，該行為者要求 Gemini 辨識某台已遭入侵系統上的漏洞，但收到 Gemini 的安全回應，表示提供詳細答案並不安全。該行為者接著**把提示重新框定為「自己是一場奪旗（CTF）競賽的參賽者」**……當以協助 CTF 競賽的名義提示時，**Gemini 回傳了可被濫用來利用該系統的有用資訊**。

**引文五：良性與濫用無法從請求本身區分（PDF p.8）**

> 「It's also important to note the context of these prompts, which **if normally posed by a participant of the CTF vs. a threat actor, would be benign inquiries**. This nuance in AI use highlights **critical differentiators in benign vs. misuse of AI** that we continue to analyze to balance Gemini functionality with both usability and security.」

> 譯：同樣重要的是要注意這些提示的脈絡：**如果是由一般的 CTF 參賽者、而非威脅行為者提出，這些就會是良性的詢問**。AI 使用上的這種細微差別，凸顯了**良性使用與濫用之間的關鍵區辨難題**，我們持續分析這個問題，以在 Gemini 的功能、易用性與安全性之間取得平衡。

**引文六：攻擊者把 C2 與金鑰交給了模型（PDF p.10）**

> 「The threat actor asked Gemini to help with a provided script, which was designed to listen for encrypted requests, decrypt them, and execute commands related to file transfers and remote execution. **This revealed sensitive, hard-coded information to Gemini, including the C2 domain and the script's encryption key**, facilitating our broader disruption of the attacker's campaign and providing **a direct window into their evolving operational capabilities and infrastructure**.」

> 譯：該威脅行為者請 Gemini 協助處理一支他們提供的腳本，該腳本設計用來監聽加密請求、解密，並執行與檔案傳輸和遠端執行相關的指令。**這向 Gemini 洩漏了敏感的硬編碼資訊，包括 C2 網域與該腳本的加密金鑰**，促成了我們對該攻擊者行動更大範圍的處置，並提供了**直接窺看其演進中的作業能力與基礎設施的窗口**。

**引文七：地下市場的商業化（PDF p.11）**

> 「Pricing models for illicit AI services also reflect those of conventional tools, with many developers **injecting advertisements into the free version** of their services and offering **subscription pricing tiers** to add on more technical features such as image generation, API access, and Discord access for higher prices.」

> 譯：非法 AI 服務的定價模式同樣反映了正規工具的做法：許多開發者在服務的**免費版中插入廣告**，並提供**訂閱制的分級定價**，以更高價格加購影像生成、API 存取與 Discord 存取等進階技術功能。

**引文八：對資訊作戰的負面結論（PDF p.18）**

> 「We have identified Gemini activity that indicates threat actors are soliciting the tool to help create articles or aid them in building tooling to automate portions of their workflow. **However, we have not identified these generated articles in the wild, nor identified evidence confirming the successful automation of their workflows leveraging this newly built tooling. None of these attempts have created breakthrough capabilities for IO campaigns.**」

> 譯：我們辨識出的 Gemini 活動顯示，威脅行為者正在請求這項工具協助撰寫文章，或協助他們建置工具以自動化其工作流程的一部分。**然而，我們並未在野外辨識出這些生成的文章，也未發現證據確認他們利用這些新建工具成功自動化了工作流程。這些嘗試沒有任何一項為資訊作戰行動創造出突破性的能力。**

---

## 12. 未能驗證之處與研究限制

### 12.1 發布日期的不一致

- **部落格頁面標示：November 6, 2025**（2026-09-14 重新抓取確認）。
- **PDF 內嵌的建檔時間戳：2025-11-05 08:14（-05:00）**，修改時間戳為同日 08:14。PDF 封面只印「2025 November」，沒有日期。
- **媒體報導日期：Axios、SiliconANGLE 等多家為 2025-11-05。**

本教材與 meta.json **採用部落格頁面標示的 2025-11-06**，理由是與本模組 `gtig-2026-05-ai-threat-tracker.html` 的處理方式一致（該期同樣採用部落格日期而非媒體日期）。**引用時若需要精確到日，建議同時標註兩個日期。** 無論採哪一個，月份都是 2025-11，因此檔名 slug 不受影響。

### 12.2 Figure 8 的重複問題（本教材的原創發現）

第 6.8 節指出 Figure 8（UNC4899/PUKCHONG）的內容與 Figure 6（suspected China-nexus）逐條相同，僅更換階段標籤並刪去最後一欄。

**未能驗證的部分**：

- 本教材**無法確認這是製作錯誤還是刻意的重新對應**。GTIG 未就此發表任何說明。
- 本教材**未向 GTIG 查證**（本模組的作業範圍不包含對外聯繫）。
- 本教材**未檢視部落格 HTML 版的圖片**，只檢視了 PDF 版的渲染結果。理論上兩版的圖可能不同，但 WebFetch 取得的部落格內容中，Figure 8 的圖說與 PDF 一致。

**因此本教材的立場是**：這是一個**已確認的內容重複**（兩版圖的文字逐條相同，可目視驗證），但**成因未經證實**。課堂引用時應同時說明這一點。

**實務建議**：引用 UNC4899 的 TTP 時只用正文，不用 Figure 8。

### 12.3 PROMPTLOCK 的學術來源，GTIG 未更正

第 3.6 節詳述。三點限制：

- 本教材對 NYU 來源的認定**完全依賴第三方報導**（CyberScoop、SC Media、iTnews、NYU Tandon 官方新聞稿）。**本教材未取得 ESET 的原始研究與其更新版本全文。**
- **ESET 維持其原始判斷**（「the discovered samples represent the first known case of AI-powered ransomware」），因此「PROMPTLOCK 完全不是威脅」這個說法並不精確。準確的說法是：**它是一個學術團隊製作的、功能完整的 AI 勒索軟體概念驗證，被誤認為威脅行為者的產物。**
- 本教材**未能確認 GTIG 在撰寫報告時是否已知悉 NYU 的澄清**。時間上 NYU 的澄清早於報告發布，但不能排除編輯流程已鎖稿。

### 12.4 「almost every」與圖上 7/10 的落差

正文說「almost every notable tool advertised in underground forums mentioned their ability to support phishing campaigns」（PDF p.11），Figure 5 的矩陣顯示 10 個工具裡有 7 個標示 Phishing。

- **本教材的矩陣是以 320 DPI 放大後目視判讀**，可能存在判讀誤差（例如某個淺色圓點被漏看）。
- **正文的「notable tool」可能指涉比圖上 10 個更廣的集合**，或指 GTIG 在論壇上看到的全部廣告而非圖選的 10 個。
- 本教材在第 6.5 節以**圖為準**呈現數字，並在此標明落差。**引用「almost every」這個措辭時應加註「圖上為 7/10」。**

### 12.5 無法驗證的主張（單一來源）

以下主張**只有 GTIG 一方的說法，外部無從驗證**，引用時必須明確標示：

- 所有關於「某行為者在 Gemini 上做了什麼」的描述（CTF 前綴、學生前綴、APT42 的 Data Processing Agent、APT41 的 OSSTUN、UNC1069 的西班牙語誘餌、兩個 China-nexus 行為者的完整生命週期清單）。
- PROMPTFLUX 與 FRUITSHELL 的存在與細節（無第三方獨立取得檢體的公開紀錄）。
- 「Big Sleep 協助找到一個即將被威脅行為者利用的漏洞，GTIG 事先切斷」（PDF p.19）。**報告未給出該漏洞的任何識別資訊**，完全無法驗證。
- 所有 Mitigations 方塊中「我們已經強化了分類器與模型，使其未來會拒絕這類請求」的主張。**沒有任何可驗證的指標。**

### 12.6 本教材未能取得的材料

- **《Advancing Gemini's Security Safeguards》白皮書全文**：報告在執行摘要中連結，但本教材未取得並閱讀。若要深入評估 Google 的防線設計，這份白皮書是必要材料。
- **GTIG 2025-01《Adversarial Misuse of Generative AI》全文**：本報告自述是它的 update，多處以「similar to our findings from January」回引。本教材僅依據本報告的轉述理解其內容。**該報告的獨立教材由其他研究員負責**（模組 09 的平行工作），完成後應回頭補上兩期的逐點對照。
- **CERT-UA 的原始公告（烏克蘭語）**：本教材對 LAMEHUG 的理解來自英語二手報導（The Hacker News、Cato Networks、Picus、SOC Prime）。原始公告的技術細節可能更豐富。
- **地下論壇的原始廣告文**：GTIG 沒有提供任何截圖或引文。Figure 5 的 10 個工具名稱是唯一的原始資料。本教材對這些工具的補充說明全部來自第三方研究，**未接觸任何論壇或服務本身**（依安全紅線）。

### 12.7 第三方報導與原文的出入

- 多家媒體報導 PROMPTFLUX「每小時改寫自己」。**準確的說法是**：這是「Thinging」**變體**的設計（「rewrite the malware's entire source code on an **hourly basis**」，PDF p.6），而原始的「Thinking Robot」版本的迴圈邏輯**被硬編碼成只執行一次**（Figure 1 的 `If True Then`）。兩者不應混為一談。
- 部分報導稱 Google「已停用 PROMPTFLUX 對 Gemini API 的存取並刪除所有相關資產」。**報告原文只說「disabling the assets associated with their activity」**，沒有說「刪除所有相關資產」。
- 部分報導把 PROMPTSTEAL 的模型寫成「Alibaba 的 Qwen」。**這在技術上正確**（Qwen 由阿里雲開發），但**報告原文只寫模型名稱，沒有提到阿里巴巴**，也沒有把這件事與蒸餾或中國供應鏈連結。**不要把 GTIG 沒說的關聯加到 GTIG 頭上。**

### 12.8 本教材的方法限制

- **PDF 全文透過 PyMuPDF 抽取**，圖表內容以 170 至 320 DPI 渲染後用視覺工具逐張判讀。文字層與圖片渲染均可能存在少量誤差，關鍵引文已與部落格 HTML 版交叉比對。
- **WebSearch 配額有限**（找到原文後執行 6 次）。第三方驗證聚焦在 LAMEHUG、PROMPTLOCK、QUIETVAULT、地下市場工具與對 PROMPTFLUX 的批評五個主題。**尚未查證的方向包括**：FRUITSHELL 的外部分析、UNC1069 的 BIGMACHO 後門與 deepfake 活動的獨立報導、APT42 Data Processing Agent 是否有其他機構的對應觀察。
- **所有 IOC 與服務名稱全程未連線、未解析、未查詢**，依本模組安全紅線執行。
- **第 5 節的 MITRE 對應完全由本教材建構**，非 GTIG 官方對應，使用時請標明。
