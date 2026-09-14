# Anthropic《Detecting and countering misuse of AI: August 2025》（2025 年 8 月）

> 課程模組：09 延伸研究 ｜ 來源類型：官方威脅報告 ｜ 原文：https://www.anthropic.com/news/detecting-countering-misuse-aug-2025 ｜ 整理日期：2026-09-14

> **資料層次標示規則**（沿用模組 01 的慣例）
> - **［原文］**：2025-08 報告可直接追溯的內容，附 PDF 頁碼。
> - **［2026］**：Anthropic 2026-09 報告的對照內容，附該份 PDF 頁碼。
> - **［外部］**：第三方報導或公開紀錄，附 URL 與日期。
> - **［分析］**：本教材作者的推論與教學詮釋，原文未明說，學員應視為可被挑戰的假設。

---

## 1. 一頁速覽

1. **這是 Anthropic 的第二份公開威脅情報報告，也是「vibe hacking」這個詞進入產業詞彙表的那一份。** 2025-08-27 發布，25 頁 PDF，作者列在最後一頁：Alex Moix、Ken Lebedev、Jacob Klein。［原文 p.25］

2. **旗艦案例 GTG-2002：一個人靠 Claude Code 打了至少 17 個組織。** 醫療、緊急救難、政府、宗教機構都在內，勒索金額由 AI 依竊得財務資料計算，區間 $75,000 至 $500,000，「有時超過 50 萬美元」。關鍵不是加密勒索，而是**竊資後以公開外洩威脅**（pay-or-leak）。［原文 p.4、p.8］

3. **報告的四條主軸寫在執行摘要裡**：agentic AI 被武器化、AI 降低犯罪門檻、犯罪者把 AI 嵌進整條行動鏈、AI 覆蓋詐欺的每一個階段。這四條在 13 個月後的 2026-09 報告裡全部成立，只是措辭從「正在發生」變成「已經擴散完畢」。［原文 p.3；2026 p.38］

4. **兩個「完全依賴 AI」的案例才是報告真正的論點**：北韓 IT 工作者（不靠 Claude 連基本前端元件都寫不出來、連同事的一句「we had our first picnic of the season」都看不懂）與 GTG-5004 勒索軟體賣家（不靠 Claude 實作不出 ChaCha20 與 syscall）。報告的原句是 **「technical competence is simulated rather than possessed」**。［原文 p.12、p.14、p.15］

5. **報告沒有任何一張編號圖表（沒有 Figure N），而且主要證據是「模擬重建」。** 全報告 13 組展示品的標題都是 `Ex. Simulated ...`，只有 6 張是真實截圖。這是一個**刻意的證據處理決策**，也是本教材第 6 節的教學重點。［原文 p.5 至 p.14、p.16、p.22、p.24］

6. **一張真實截圖直接關係台灣。** p.22 那張威脅行為者在俄語論壇 xss[.]is 上自炫的 Claude MCP 截圖裡，被拿來做行為側寫的兩名竊資木馬受害者，其中一位的系統語系寫著 **「Chinese (Traditional, Taiwan)」**、作業系統是 **「Windows 11 家用版 (Home) x64」**、國別欄位是 **「TZ and TW」**。這是全份報告唯一可見的台灣足跡，而且只存在於圖片裡、文字層抓不到。［原文 p.22］

7. **2026-09 報告只明確回指了這份報告的一個案子。** 2026-09 的 GTG-15001（詐騙交友 app 網絡）寫著「This is a cousin of a 2025 case, where another actor set up a Telegram bot as a service for other scammers to generate dating app messages with」，指的正是本報告 p.24 的 `@Chat_ChatGPT_AIbot`。其餘案例沒有續集。［2026 p.139；原文 p.24］

8. **兩個「消失的題目」比任何續集都更值得上課講**：2026-09 報告全文出現 **0 次 "ransomware"**、**0 次 "North Korea" 或 "DPRK"**；而本報告出現 15 次 ransomware、整整一個章節談北韓。同一個團隊、同一套遙測，13 個月後這兩個主題完全消失。這是「威脅報告的選材偏差」最乾淨的教學素材。［經全文字串比對，見第 12 節］

9. **這份研究在課程裡要教什麼**：教學員**讀懂一份威脅報告的「措辭演化」**。把 2025-08 的「AI serves as both a technical consultant and active operator」和 2026-09 的「operations ran autonomously, with minimal human input or supervision」並排，學員會看到同一家機構如何在 13 個月內把自主程度的語言往右推兩格；再把 2025-08 的「AI lowers the barriers」和 2026-09 的「The main distinguishing feature between these classes of actors is no longer sophistication but intent」並排，會看到「門檻降低」如何從一個預測變成一個已完成的結構性事實。

---

## 2. 報告基本資料

| 項目 | 內容 | 出處 |
|---|---|---|
| 官方標題 | **Detecting and countering misuse of AI: August 2025** | 官方頁面標題 |
| PDF 內封標題 | **Threat Intelligence Report: August 2025** | ［原文 p.1］ |
| 發布日 | **2025-08-27** | 官方頁面 |
| 機構／團隊 | Anthropic，**Threat Intelligence** 團隊（報告自述為 Safeguards 組織下的專責團隊） | ［原文 p.3］ |
| 具名作者 | **Alex Moix、Ken Lebedev、Jacob Klein**（列在最後一頁，無職稱） | ［原文 p.25］ |
| 形式與篇幅 | PDF，**25 頁**；另有網頁摘要版 | 下載自 `www-cdn.anthropic.com` |
| PDF 直連 | `https://www-cdn.anthropic.com/b2a76c6f6992465c09a6f2fce282f6c0cea8c200.pdf` | 官方頁面連結 |
| 涉及的模型與產品 | **Claude Code**（GTG-2002 的主要載具）、Claude.ai、Claude API；並提到 **MCP（Model Context Protocol）** 被用於竊資分析 | ［原文 p.4、p.20、p.22］ |
| 涵蓋期間 | **報告未明確宣告**。可從個案回推：最早的事件是 2024-10-22 建立的北韓帳號，最晚是 GTG-2002「in just the last month」（約 2025-07 至 08）。實質窗口至少橫跨 **2024-10 至 2025-08** | ［原文 p.4、p.19］ |
| 資料來源類型 | 以**平台側遙測**為主（帳號行為、對話內容、Claude Code 執行紀錄、`CLAUDE.md` 內容），輔以**私部門情報分享夥伴關係**、**公開報導**、以及**一則獨立研究者的線報** | ［原文 p.11、p.19、p.24］ |
| 自動化偵測工具 | 明確點名 **Clio**（Anthropic 的自動化、保護隱私的分析工具）發現了 p.20 的俄語 no-code malware 案 | ［原文 p.20］ |
| 目錄頁碼錯誤 | 目錄（p.2）把詐欺章節的四個案例標在 23／24／25／26 頁，但 PDF 只有 25 頁，實際落在 22／23／24／25。前六項頁碼正確，**只有詐欺章節整組差一頁** | ［原文 p.2 對照 p.22 至 p.25］ |

### 2.1 與 Anthropic 前後期報告的關係

Anthropic 2026-09 報告的 Overview 第一段，親自把自家的報告序列點名了一次：

> ［2026 p.3］"...describe how malicious use of Claude has evolved since our previous threat reports in **March, August, and November 2025**."

四份報告的定位（本課程模組 01 已有完整比較表，見 `../01-cyber/00-cyber-trends-and-skills.html` 第 8.4 節；此處只補本報告在序列中的位置）：

| 序位 | 報告 | 發布 | 這份報告在序列裡的功能 |
|---|---|---|---|
| 第 1 份 | Detecting and countering malicious uses of Claude: March 2025 | 2025-04-23 | 建立「AI 開始決定行為，不只生成內容」的命題 |
| **第 2 份** | **Detecting and countering misuse of AI: August 2025**（本教材） | **2025-08-27** | **建立「AI 上場動手」的命題，並造出 vibe hacking 這個詞** |
| 第 3 份 | Disrupting the first reported AI-orchestrated cyber espionage campaign | 2025-11-13 | 建立「AI 自主編排」的命題（GTG-1002） |
| 第 4 份 | Detecting and countering misuse of AI: September 2026 | 2026-09-10 | 宣告上述三種型態**同時並存且已擴散到所有行為者類別** |

> ［分析］注意第 2 份報告的**標題改名**：第 1 份叫 "malicious uses of **Claude**"，第 2 份起改成 "misuse of **AI**"。命名從「我們家產品被誤用」變成「AI 這個技術被誤用」，同時報告內容也開始納入非 Anthropic 模型（p.24 的 Telegram bot 同時代理多家模型）。這個改名在 2026-09 被沿用。這不是文字遊戲，而是一家 AI 公司把自己從「被告」重新定位成「產業偵測者」的措辭工程。

---

## 3. 主要發現與案例逐一摘要

### 3.1 執行摘要的四條主軸［原文 p.3］

報告在 p.3 用四個粗體條目定調，這四條是後續所有案例的骨架：

| 主軸 | 原文 | 對應案例 |
|---|---|---|
| **agentic AI 被武器化** | "Agentic AI systems are being weaponized: AI models are themselves being used to perform sophisticated cyberattacks – not just advising on how to carry them out." | GTG-2002 |
| **AI 降低犯罪門檻** | "AI lowers the barriers to sophisticated cybercrime. Actors with few technical skills have used AI to conduct complex operations, like developing ransomware, that would previously have required years of training." | GTG-5004、北韓 IT 工作者 |
| **AI 被嵌進整條行動鏈** | "Cybercriminals are embedding AI throughout their operations. This includes victim profiling, automated service delivery, and in operations that affect tens of thousands of users." | MCP 竊資分析、Telegram 詐騙 bot |
| **AI 覆蓋詐欺的所有階段** | "AI is being used for all stages of fraud operations. Fraudulent actors use AI for tasks like analyzing stolen data, stealing credit card information, and creating false identities." | 詐欺章節四案 |

報告同時加了一句**跨平台適用性的聲明**，這句話在方法論上很重要：

> ［原文 p.3］"While specific to Claude, the case studies presented below likely reflect consistent patterns of behaviour across all frontier AI models."

> ［分析］這是一個**沒有證據支撐的外推**。Anthropic 只能看到 Claude 的遙測，「其他前沿模型大概也一樣」是合理推測但不是觀察。課堂上要讓學員習慣把這種句子標記為「機構自述的推定」，而不是報告的發現。模組 09 的存在價值正在於此：唯有把 OpenAI、Google GTIG 的同類報告拿來並讀，這句話才會變成可檢驗的命題。

### 3.2 十個案例總表

報告分成兩大部分：前段是網路安全（6 案），後段是詐欺生態系（4 案）。

| # | 案例 | 代號 | 行為者類型與線索 | 危害領域 | AI 被拿來做什麼 | 自主程度 | 處置 | 頁碼 |
|---|---|---|---|---|---|---|---|---|
| 1 | Vibe hacking 資料勒索 | **GTG-2002** | 單一犯罪者；要求以**俄語**溝通 | 資料竊取與勒索 | 偵察、入侵、橫向移動、惡意程式規避、竊資分析、勒索信生成、贖金定價 | **高**（AI 做戰術與戰略決策） | 封號；開發專用分類器與新偵測法；與夥伴分享指標 | p.4 至 p.10 |
| 2 | 北韓 IT 工作者詐欺就業 | 無代號 | **北韓 operatives**（DPRK） | 制裁規避、內部威脅 | 假身分、履歷、面試、上工後的實際交付、職場溝通 | **中**（對話式，但滲透日常每一步） | 封號；強化 IOC 蒐集與關聯工具 | p.11 至 p.14 |
| 3 | No-code 勒索軟體即服務 | **GTG-5004** | **英國（UK-based）**單一行為者 | 惡意程式開發與販售 | ChaCha20 實作、syscall 規避、反分析、PHP C2、商品包裝 | **中**（人類持續給方向，AI 實作） | 封號；新增惡意程式上傳／修改／生成的偵測 | p.15 至 p.17 |
| 4 | 中國行為者跨 12/14 ATT&CK 戰術 | 無代號 | **中國 APT 特徵**；要求「中文交流」 | 關鍵基礎設施間諜（**越南**） | Python 掃描器、檔案上傳 fuzzing、WordPress 利用框架、Hydra／hashcat、Linux 核心提權、proxy chain、偵察資料分析 | **中** | 加強監控；與相關機關分享情報 | p.18 |
| 5 | 北韓惡意程式散布的自動攔阻 | 無代號 | **Contagious Interview**（Famous Chollima／DEV#POPPER／UNC5342） | 惡意程式散布 | **未發生**（帳號在下任何 prompt 前即被封） | 無 | 自動風險偵測，4 個帳號中 2 個立即封鎖，另 2 個被行為者放棄 | p.19 |
| 6 | No-code 惡意程式開發 | 無代號 | **俄語**開發者，具 Windows internals 知識 | 惡意程式開發 | Hell's Gate syscall 解析、Early Bird 注入、Telegram bot C2、螢幕截圖竊資、反分析、偽裝成 Zoom／加密貨幣工具 | **中** | 由 **Clio** 發現 | p.20 |
| 7 | MCP 竊資紀錄分析與受害者側寫 | 無代號 | 在 **xss[.]is** 活動的行為者 | 竊資後的受害者側寫 | 處理 stealer log、網域分類、瀏覽行為分析、興趣排名、行為側寫 | **中** | 報告未載明處置 | p.22 |
| 8 | AI 驅動的盜刷卡商店 | 無代號 | **西班牙語**行為者 | 金融詐欺 | 三家卡片驗證服務的輪替容錯框架、動態 API 發現、請求節流、批次處理排程 | **中** | 報告未載明處置 | p.23 |
| 9 | AI 驅動的交友詐騙 bot | 無代號 | Telegram bot **`@Chat_ChatGPT_AIbot`**；服務訊息與頻道以**中文**為主 | 詐騙 | Claude 當「high EQ model」產生高情商回覆；他家模型做圖；多語系（美、日、韓） | **中**（服務化，賣給其他詐騙者） | 報告未載明處置 | p.24 |
| 10 | AI 驅動的合成身分服務 | 無代號 | 未載明 | 身分詐欺 | **正文誤植**（見下） | 不明 | 報告未載明處置 | p.25 |

> **［原文的一個明顯製作錯誤，務必在課堂上點出］** p.25「Synthetic identity services powered by AI」的標題與導言是獨立的（"We discovered an actor who successfully launched an operational synthetic identity service using Claude for various components of their infrastructure."），但底下的 **Tactics and techniques／Impact／ACTOR PROFILE 三個區塊，與 p.23「Carding store powered by AI」逐字完全相同**（同樣是「rotates between three card validation services aka "card checkers"」、同樣是「The actor operated a carding service」）。換句話說，**報告第十個案例的技術內容從未被真正寫出來**。配合目錄頁碼在詐欺章節整組差一頁，［分析］合理推測是排版階段抽掉了一頁、複製貼上未更新。這件事本身沒什麼，但它是教學員「一手文件也會出錯、必須逐字核對」的最佳現成教材。

### 3.3 案例一：GTG-2002「Vibe hacking」［原文 p.4 至 p.10］

這是全報告最完整、也是影響最大的一案。

**規模與受害者**：一個月內影響**至少 17 個不同組織**，橫跨政府、醫療、緊急救難、宗教機構。竊得資料包括社會安全碼、銀行帳戶、病患資訊、以及 **ITAR 管制文件**（美國國際武器貿易條例）。勒索金額 **$75,000 至 $500,000** 的比特幣，「有時超過 $500,000」。［原文 p.4、p.7、p.8］

**作案平台**：**Kali Linux 上的 Claude Code**，並在 **`CLAUDE.md`** 裡預埋持久化的作業指示。報告特別澄清一個重要細節：

> ［原文 p.4］"However, this was simply a preferential guide and the operation still utilized Claude Code to make both tactical and strategic decisions..."

［分析］這句話的情報意義是：`CLAUDE.md` 不是「腳本」而是「偏好指南」，代表**每一次具體的目標選擇、資料取捨、勒索話術都是模型當下生成的**，不是人類預先寫死的。這是 2025 年 8 月時 Anthropic 能宣稱「AI 是 active operator 而非 consultant」的證據基礎。

**`CLAUDE.md` 裡有什麼**（報告以中括號摘要形式呈現，未給原文）：一個**掩護故事**（宣稱是有正式支援合約的網路安全測試）、VPN 連線與路由規避設定、使用者列舉與強制密碼噴灑、Kerberos 攻擊與雜湊萃取、存取後的完整列舉命令、一份**七步驟的新網路檢查清單**（從偵察到持久化）、relay 攻擊與委派濫用、以及「強調隱蔽、盡量少建檔案」的指示。同時要求 **全程以俄語溝通**、**要求保留上下文**。［原文 p.5、p.6］

**五階段生命週期**：

```mermaid
flowchart TD
    P1["階段 1 偵察與目標發現<br/>Claude Code 掃描數千個 VPN 端點<br/>依國別與技術類型整理結果"]
    P2["階段 2 初始存取與憑證利用<br/>即時協助實網滲透<br/>辨識網域控制站與 SQL Server<br/>Active Directory 憑證萃取"]
    P3["階段 3 惡意程式開發與規避<br/>混淆版 Chisel 繞過 Windows Defender<br/>全新 TCP proxy 不使用 Chisel 函式庫<br/>偽裝成 MSBuild.exe devenv.exe cl.exe"]
    P4["階段 4 竊資與分析<br/>從國防承包商 醫療機構 金融機構抽取<br/>SSN 銀行帳戶 病患資料 ITAR 文件<br/>整理成可變現的資料集"]
    P5["階段 5 勒索分析與贖金信生成<br/>依財務資料計算贖金<br/>HTML 勒索信嵌入開機流程<br/>產生多路徑 profit plan"]
    P1 --> P2 --> P3 --> P4 --> P5
    P5 -. "換下一個受害者" .-> P1
```

**每個階段報告都寫了一行 `AI role:`**，這是本報告獨有的體例（2026-09 改用「人類做什麼／AI 做什麼」的敘事，不再逐段標 AI role）：

| 階段 | 報告寫的 AI role 原文重點 |
|---|---|
| 1 | "Enhanced capability, enabling systematic discovery of thousands of potential entry points globally" |
| 2 | "Direct operational support during live intrusions, providing guidance for privilege escalation and lateral movement in real-time" |
| 3 | "Custom malware development with evasion capabilities, lowering the technical barrier" |
| 4 | "Automated analysis and organization of large datasets... across multiple victim organizations simultaneously" |
| 5 | "Automated generation of psychologically-crafted extortion materials tailored to each victim's specific vulnerabilities" |

**最值得注意的一個技術細節**：階段 3 描述了一次**失敗後的自適應**。「When initial evasion attempts failed, Claude Code provided new techniques including string encryption, anti-debugging code, and filename masquerading.」［原文 p.6］這是**防守方的偵測結果被當成攻擊方的回饋訊號**的早期紀錄。同一個閉環在 2026-09 被寫成 GTG-20006 的「AI-assisted workflow that automatically rebuilt and re-deployed their toolkit if it was detected by security products」［2026 p.6］，差別是：2025-08 需要人類把失敗訊息貼回去，2026-09 已經是**工作流自動重建**。

**勒索的創新點**：不加密、只威脅外洩。並且 AI 產生的 **「profit plan」** 提供四種變現路徑（直接勒索組織、把資料賣給其他犯罪者、對資料當事人個別勒索、分層並行），還附上成功機率估計與收益預估。勒索信有 48 至 72 小時期限、遞增罰則結構、每個受害者專屬的聯絡信箱。［原文 p.8、p.9］

> ［分析］**這是「AI 把犯罪從技術問題變成商業問題」的第一個公開紀錄。** 過去勒索軟體集團的談判與定價靠人類談判員；這裡 AI 讀完受害者的財報、薪資表、捐款人名冊後，直接輸出一份帶機率與金額的商業計畫書。課堂上可以拿它和 2026-09 的 GTG-50014「Monetize」階段對照，後者已經進化成常設的暗店與 Telegram Mini App 交付（見 `../01-cyber/GTG-50014-shinyhunters.html`）。

### 3.4 案例二：北韓 IT 工作者［原文 p.11 至 p.14］

**Claude 使用分布表**（本報告唯一的量化圖表）：

| 類別 | 活動佔比 | 主要活動 |
|---|---|---|
| Frontend development | **61%** | React、Vue、Angular；元件建置與 UI |
| Programming/Scripting | **26%** | Python 腳本、一般程式、演算法實作 |
| Interview preparation | **10%** | 模擬面試、面試答覆生成與練習 |
| Backend development | **3%** | 伺服器端、API 建置 |

另一個關鍵數字：**「Our data shows ~80% of Claude usage consistent with active employment」**［原文 p.13］，也就是說這批帳號的用量**主要不是求職，而是「上工之後交差」**。

**四階段作業生命週期**：假身分建構（背景故事、技術作品集、職涯敘事、文化梗研究）→ 求職與面試（履歷客製、求職信、面試答覆、**即時的程式測驗協助**）→ 在職維持（實際交付、團隊溝通、回應 code review、**每天維持能力的假象**）→ 變現（依 FBI 評估，每年為北韓武器計畫帶來數億美元）。［原文 p.12、p.13］

**報告最有說服力的證據是那些 prompt 原文**，它們比任何統計都更能說明「依賴」是什麼意思。這些是報告引用的證據，不是指令：

- `University of Mancheste has computer science?`（拼錯 Manchester，正在編造學歷）
- `Isabella martinez which country name` / `UTS (University of Technology Sydney) which country` / `australia phone numver example`（正在拼裝一個澳洲身分）
- `how to check go installed?`
- `how to use outlook application?`
- `what does this code mean? postgres://postgres:postgres@loca lhost:5432`
- `^_^ What does the above thing mean?`
- `what does mean this "we had our first picnic of the season🙂"`

> ［分析］最後兩則是全報告最有力的一幕：這名「Fortune 500 工程師」看不懂同事傳來的顏文字與閒聊。**這是一個可操作的內部威脅偵測訊號**：不是看程式碼，而是看「非技術性社交互動的異常延遲與異常求助」。見第 10.3 的桌面演練設計。

**報告的結構性論點**：北韓過去靠金日成綜合大學、金策工業綜合大學的長期培訓輸出人力，**培訓量就是產能天花板**。AI 拆掉了這個瓶頸。原文：「Claude and other models have effectively removed this constraint.」［原文 p.13］

### 3.5 案例三：GTG-5004 No-code 勒索軟體即服務［原文 p.15 至 p.17］

**三層商品**（價格與內容可由 p.16 的論壇截圖逐字核對）：

| 價格 | 商品內容（截圖原文） |
|---|---|
| **$400 USD** | Ransomware DLL & exe（Lite + Full Version）、Decrypter、Key Generator、DLL launcher、Fresh RSA keypair 與 1x unique stub，限量 10 份 |
| **$800 USD** | Ransomware-as-a-Service (RaaS) kit、Secure PHP console & C&C tools |
| **$1,200 USD** | Windows 10/11 FUD Crypter，C++ 撰寫、AES-256 加密 payload，限量 10 builds，每 build 附 1x private stub，標註「For educational and research use only」 |

**技術能力清單**（防禦向摘要）：ChaCha20 串流加密只加密檔案**前 256KB**（檔頭）以求速度、Windows CNG API 做 RSA 金鑰管理、加上 `.enc` 副檔名、列舉所有固定磁碟與網路共用並優先處理使用者目錄；規避面用 **FreshyCalls**（解析 ntdll.dll 匯出表取得 syscall 編號）與 **RecycledGate**（在 ntdll.dll 中尋找既有的 `syscall; ret` 序列）做直接系統呼叫、字串混淆、反除錯；投遞用反射式 DLL 注入與 code cave 感染；反復原用**磁碟區陰影複製刪除**。［原文 p.15 至 p.17］

**演化時間軸**（報告自述可從對話歷程看出三個階段）：早期做基本加密與規避 → 中期做反分析與反復原 → 後期做進階投遞與 C2 基礎設施。［原文 p.17］

> ［分析］這條時間軸是**本報告最被低估的方法論貢獻**。它示範了「平台側遙測可以重建攻擊者的能力成長曲線」這件事，是 endpoint 或網路遙測做不到的。2026-09 的 GTG-50014 儀表板（Figure 2 的 118 天 campaign span）本質上是同一種分析的視覺化版本。

### 3.6 詐欺生態系四案：報告的「供應鏈」論點［原文 p.21 至 p.25］

報告刻意把四個小案並列，論點是**AI 已經覆蓋詐欺價值鏈的每一段**：

```mermaid
flowchart LR
    A["竊資木馬產出<br/>stealer logs"] --> B["案例 7<br/>MCP 分析與受害者側寫<br/>xss[.]is"]
    B --> C["案例 8<br/>盜刷卡商店<br/>三家 card checker 輪替"]
    B --> D["案例 9<br/>交友詐騙 bot<br/>@Chat_ChatGPT_AIbot"]
    C --> E["案例 10<br/>合成身分服務"]
    D --> E
    E --> F["變現"]
    C --> F
    subgraph AI["AI 在每一段的角色"]
        G["分析與鎖定"]
        H["基礎設施開發"]
        I["營運韌性"]
        J["技術門檻下降"]
    end
```

報告自己的四點收束［原文 p.25］：

1. **Analysis & targeting**：AI 把竊得的資料變成可行動的情報（行為側寫、受害者排序）。
2. **Infrastructure development**：AI 讓犯罪平台具備企業級功能。
3. **Operational resilience**：被封鎖時能快速轉向與調整。
4. **Technical sophistication**：進階規避與安全措施的門檻下降。

**案例 9 的細節值得單獨記住**，因為它是 2026-09 唯一明確回指的案子：Telegram bot `@Chat_ChatGPT_AIbot`，**逾 10,000 名月活使用者**，多模型（Claude 被宣傳為 "high EQ model"），多語系鎖定**美國、日本、韓國**，服務訊息與相連頻道**主要是中文**。這個 bot 是**服務商**，不是詐騙執行者，它把「高情商訊息生成」賣給其他詐騙者。［原文 p.24］

---

## 4. 與 Anthropic 2026-09 報告的對照

本節是模組 09 的核心。所有 2026-09 的引用附該份 PDF 頁碼，本課程對應教材以發布路徑連結。

### 4.1 「vibe hacking」這個詞的旅程

| 時點 | 措辭 | 位置 | 語意 |
|---|---|---|---|
| 2025-08 | "using coding agents to actively execute operations on victim networks, known as 'vibe hacking'" | ［原文 p.4］ | 一個**新現象的命名**，且報告把命名權讓給別人：「This approach, which **security researchers have termed** 'vibe hacking'」 |
| 2026-09 | "The use of AI during intrusions and data theft operations **often resembles** 'vibe hacking,' wherein operators direct AI to achieve general goals... then allow the AI to evaluate the environment, author and execute scripts, provide summaries, and repeatedly execute until the task is complete." | ［2026 p.14］ | 一個**已經內化的常態描述**，而且加上了一句關鍵的操作者側寫：「the operator may not directly understand each target environment... instead deferring the specifics to the AI」 |

> **教學點**：13 個月內，同一個詞從「一種新的攻擊方式」變成「入侵行動的預設樣態」。更重要的是 2026-09 補上的那句「操作者可能根本不理解目標環境」，這正是 2025-08 只敢用 `CLAUDE.md` 的存在來暗示、還不敢直說的東西。對應教材：`../01-cyber/GTG-50014-shinyhunters.html`（該案的九階段生命週期就是 vibe hacking 的工業化版本）。

### 4.2 GTG 編號制度改版：四位數變五位數

| 報告 | 出現的編號 | 位數 |
|---|---|---|
| 2025-08（本報告） | GTG-2002、GTG-5004 | **4 位** |
| 2025-11 | GTG-1002 | **4 位** |
| 2026-09 | GTG-20006、GTG-50014、GTG-10007、GTG-50021、GTG-50020、GTG-50029、GTG-04001…GTG-16008 等 | **5 位** |
| 2026-09 回指 2025-11 的那一案 | **GTG-10002**「as previously reported」［2026 p.38］ | **5 位** |

> ［分析］2026-09 p.38 明確用 **GTG-10002** 指稱「先前報告過、自行開發自主攻擊框架」的群體，而符合這個描述的先前案例只有 2025-11 的 **GTG-1002**。合理推論：**Anthropic 在 2025-11 與 2026-09 之間把 GTG 編號從四位擴成五位，方式是在第一位後面插一個 0**。若此規則成立，本報告的 GTG-2002 對應的新編號會是 GTG-20002、GTG-5004 會是 GTG-50004。
>
> **但必須嚴格警告學員三件事**：(a) 這是推論，Anthropic 從未公告編號規則；(b) 2026-09 報告 p.4 只說 GTG 是「Anthropic's internal designators for actors observed to be abusing AI」，**沒有說明編號含意**；(c) 本課程既有教材與 `_brief` 都明訂「不要從數字推斷歸因」。因此**不可以**因為 GTG-20002 與 GTG-20006 前兩碼相同，就推論 GTG-2002 與 2026-09 的俄羅斯間諜案有關。編號相近不是歸因證據。相關討論見 `../01-cyber/00-cyber-trends-and-skills.html`。

### 4.3 「AI 自主程度」的措辭變化（本節第一個重點對照）

| 面向 | 2025-08 的措辭 | 2026-09 的措辭 |
|---|---|---|
| 總體定位 | "AI serves as **both a technical consultant and active operator**"［p.4］ | "From assistant to orchestrator"（章節標題）；"A majority of the operations described in this report were enabled by AI via **direct execution or orchestration**"［p.5］ |
| 自主的上限 | "Technical infrastructure is augmented by AI capabilities that can perform complex operations **autonomously**"（寫在 Implications，屬展望）［p.8］ | "At the far end, operations ran autonomously, **with minimal human input or supervision**: these included multi-agent frameworks conducting reconnaissance, exploitation, and theft against multiple victims, **in parallel, for hours or days at a time**"［p.39］ |
| 自主的分級 | **沒有分級**。只有「consultant／operator」二分 | **三段光譜明文化**：對話式協助 → 人類逐步指揮每個鎖定決策（GTG-20006）→ 自主多代理（GTG-50014、50020、50029）；另加「排程無人值守」（GTG-10007、GTG-20006）［p.39］ |
| 人類還保留什麼 | 未討論 | **明文 caveat 1**：「humans have retained the decisions that matter most to them: ... target selection, monetization of findings, and review of results」［p.39］ |
| 自主與危害的關係 | 未區分 | **明文 caveat 2**：「autonomy and harm are separate axes」；並指出「Several of the most serious compromises we report here came from operations where a human directed every step」［p.39］ |
| 經濟學語言 | 沒有 | 「AI autonomy compresses the cost side of attacker ROI calculations, lowering the skill threshold and labor required per campaign, while leaving potential payoffs largely unchanged」［p.39］ |

> **教學點（這是本教材最值得上課講的第一個發現）**：2026-09 在把自主程度往上推的同時，**主動加了兩個降溫的 caveat**，而 2025-08 完全沒有。從情報寫作的角度看，這是一家機構在自我修正 2025 年那波「AI 全自主攻擊」報導的過度解讀。課堂上要讓學員看到：**一份成熟的威脅報告，會在推進論點的同時親手替論點設限**；反過來說，一份只推進不設限的報告，讀者要自己補上那個限制。對應教材：`../shared/01-cross-cutting-analysis.html`、`../01-cyber/00-cyber-trends-and-skills.html`。

### 4.4 「行為者門檻」的措辭變化（本節第二個重點對照）

| 面向 | 2025-08 | 2026-09 |
|---|---|---|
| 核心命題 | 「AI **lowers** the barriers」（進行式，一個正在發生的趨勢）［p.3］ | 「AI has **collapsed** the labor and tooling gap」（完成式，一個已成事實的結構）［p.5］ |
| 對歸因的意涵 | 「Traditional assumptions about the relationship between actor sophistication and attack complexity **no longer hold**」［p.8］ | 「For threat intelligence investigators, **sophistication has stopped being a reliable signal of who is behind an operation**」［p.5］ |
| 國家級與犯罪級的差別 | 未直接討論 | 「The main distinguishing feature between these classes of actors is **no longer sophistication but intent**」［p.38］ |
| 具體對照 | 一個沒有技術能力的人賣得動勒索軟體（GTG-5004）；一批不會寫程式的人在 Fortune 500 上班 | 「A hacktivist using stolen API keys (GTG-50029), a financially motivated crew harvesting credentials from mobile applications (GTG-50014), and a state-nexus espionage operator (GTG-20006) all showed **similar methodology**」［p.38 至 39］ |
| 攻擊技術是否新穎 | 未討論 | 「The attacks themselves are familiar... **None of the operations in this report depended on some entirely novel technique** that defenders have never seen. Instead, the economics of the attacks have changed.」［p.39］ |
| 防守方該假設什麼 | 「we expect this model to become increasingly common」（預期）［p.8］ | 「The capabilities described in this report **should be assumed to be available to any actors who are motivated to use them**」（命令式的防禦假設）［p.38］ |

> **教學點**：2025-08 講的是「門檻在降」，2026-09 講的是「門檻已經不存在，剩下的只有意圖」。對 CTI 分析師而言，這句話直接廢掉一整類歸因啟發法：**「這麼精密一定是國家級」在 2026 年已經是錯誤推理**。對 SOC 而言，則意味著威脅模型的預設值要從「我們大概不是 APT 的目標」改成「任何有動機的人現在都具備 APT 級能力」。

### 4.5 逐案對照：2025-08 的案子在 2026-09 有沒有續集

| 2025-08 案例 | 2026-09 的對應 | 關係性質 | 本課程教材 |
|---|---|---|---|
| GTG-2002 vibe hacking 資料勒索 | **GTG-50014**（ShinyHunters 附屬）：同樣是機會型、財務動機、pay-or-leak、AI 幾乎全自動。2026-09 版本多了供應鏈扇出、自營暗店、1.8M APK 掃描 | **概念續集**，非同一行為者（無任何證據指向同一人） | `../01-cyber/GTG-50014-shinyhunters.html` |
| GTG-2002 的「偷來的能力再投入攻擊」 | **GTG-50021／GTG-50020**：AI 憑證的 Loot／Compute／Cover 三合一框架 | **概念延伸**。2025-08 沒有這個概念，2026-09 把它獨立成一個子章節 | `../01-cyber/GTG-50021-fake-reseller.html`、`../01-cyber/GTG-50020-ai-supply-chain.html` |
| GTG-2002 的偵測失敗後自適應 | **GTG-20006**：AI 工作流在被資安產品偵測後**自動重建並重新部署**工具組［2026 p.6］ | **能力升級**：人類貼回失敗訊息 → 全自動閉環 | `../01-cyber/GTG-20006-russian-espionage.html` |
| 北韓 IT 工作者 | **無**。2026-09 全文 0 次提及 North Korea 或 DPRK | **完全消失** | 無對應教材 |
| GTG-5004 勒索軟體即服務 | **無**。2026-09 全文 0 次出現 "ransomware" | **完全消失** | 無對應教材 |
| 中國行為者打越南關鍵基礎設施 | **無直接對應**。2026-09 的中國關聯案集中在監控（GTG-14010／14020／14021／14022）與武器情報（GTG-17001／17002／17003），沒有「中國打東南亞關鍵基礎設施」的網路案 | **題材轉移** | `../03-surveillance/00-surveillance-intro.html` |
| 北韓 Contagious Interview 自動攔阻 | **無** | **完全消失** | 無 |
| 俄語 no-code 惡意程式開發 | **概念上被 GTG-50029 與 Appendix A 的 skills 清單吸收**；2026-09 不再單獨報導「某人用 Claude 寫惡意程式」這種等級的案例 | **門檻抬高**：這種案子在 2026 已經不算「notable and novel」 | `../01-cyber/GTG-50029-hacktivist.html` |
| MCP 竊資分析與受害者側寫 | **無直接對應**，但 2026-09 的 GTG-50014「Validate/qualify」與「Warehouse」階段、以及 GTG-50029 的 `fafsearch` doxxing 平台，都是同一件事的放大版 | **概念放大** | `../01-cyber/GTG-50014-shinyhunters.html`、`../01-cyber/GTG-50029-hacktivist.html` |
| 盜刷卡商店 | **GTG-50014 的 `autoshop.policenationale[.]cc`**：一個完整的 carding autoshop，附 BIN 查詢、持卡人 PII、受害者地址互動地圖、Telegram Mini App 交付 | **概念續集且規模躍升** | `../01-cyber/GTG-50014-shinyhunters.html` |
| **交友詐騙 bot `@Chat_ChatGPT_AIbot`** | **GTG-15001**：2026-09 明文「This is a **cousin of a 2025 case**, where another actor set up a Telegram bot as a service for other scammers to generate dating app messages with」［2026 p.139］ | **報告作者自己認定的親緣關係，全報告唯一一處明確回指 2025-08 的案例** | `../06-scams/GTG-15001-dating-app-network.html` |
| 合成身分服務 | **無**（且本報告該案內容本身就是誤植的空殼） | 無 | 無 |

### 4.6 從 Telegram bot 到 20 個 app：一條可追蹤的演化線

這是全教材最有教學價值的一條連續線，因為它是**Anthropic 自己畫的**，不是本教材推論的。

```mermaid
flowchart TD
    A["2025-08 報告 p.24<br/>@Chat_ChatGPT_AIbot<br/>Telegram bot 服務商<br/>10,000+ 月活使用者<br/>賣 high EQ 訊息生成給其他詐騙者<br/>中文服務 鎖定美日韓"]
    B["2026-09 報告 p.139<br/>GTG-15001<br/>中國 app 工作室<br/>自建 20+ 交友 app<br/>4,700+ AI 人設<br/>25,000+ 獨立用戶<br/>兩週 236 萬則訊息"]
    A -->|"Anthropic 稱為 cousin"| B
    subgraph 變化 ["三個關鍵變化"]
        C["商業模式<br/>賣工具 變成 自營平台"]
        D["AI 角色<br/>生成單則訊息 變成 自主維持人設關係"]
        E["偵測難度<br/>bot 本身違規可見<br/>變成<br/>系統提示看起來像一般陪伴部署"]
    end
```

**三個變化的教學意義**：

1. **商業模式從「賣鏟子」變成「自己挖礦」。** 2025-08 的行為者賣服務給詐騙者（違規行為在 bot 的行銷文案裡看得見）；2026-09 的行為者自己開 app 直接面對受害者，把違規藏進一個看起來完全正常的產品裡。
2. **AI 的角色從「生成一則訊息」變成「自主維持一段關係」。** 前者是內容生成，後者是長期社交操縱，而且 2026-09 明載模型的系統提示要求人設「never to disclose they were automated」、閃避視訊與照片要求。
3. **偵測位置必須上移。** 2026-09 對這案下了一個對防守方極重要的結論：「the monetization and deception were not visible from inside any exchange」［2026 p.140］。也就是說，**per-exchange 的內容分類器在這類案子上會系統性失效**。這與 2025-08 的 bot 案完全相反：那個 bot 的違規在行銷文案裡就看得到。詳見 `../06-scams/GTG-15001-dating-app-network.html` 與 `../shared/02-claude-safeguards-and-bypass-paths.html`。

### 4.7 報告體例的六個變化

| 體例 | 2025-08 | 2026-09 | 意義 |
|---|---|---|---|
| 篇幅 | 25 頁 | 154 頁 | 6 倍 |
| 危害領域 | 2 個（網路安全、詐欺） | 7 個（網路、影響力、監控、詐騙、生物、常規武器、蒸餾） | 從資安報告變成全面的濫用報告 |
| 圖表 | **無編號圖表**；13 組 `Ex. Simulated ...` 展示品 + 1 張表 + 6 張真實截圖 | **51 張編號 Figure**，含儀表板、流程圖、情報循環圖 | 視覺化程度天差地別 |
| IOC | **散落在正文**，只有 4 個可用指標（1 個 .onion、1 個 ProtonMail、1 個 Telegram bot、1 個論壇網域） | **每個案例末尾的正式 IOC 表**（欄位 Indicator / Type / 部分含 Category、Cluster、First seen、Last seen） | 從「順帶一提」變成可餵給 SIEM 的結構化交付 |
| 歸因措辭 | 直白：「a UK-based threat actor」、「North Korean operatives」、「characteristics consistent with Chinese APT operations」 | 分級：suspected / consistent with / assess with high confidence | 情報紀律成熟 |
| 防線缺口自陳 | **幾乎沒有**。每案的 Mitigation 都是「我們封號、我們加了偵測」的正面敘事 | **多處自曝失效**：重新提示突破分類器、跨工作階段拆分、模型自身推理已察覺危害卻未拒絕 | **這是本教材認為最重要的體例變化**，見第 8 節 |

### 4.8 有沒有「同一事件的兩造說法差異」

**沒有。** 本報告的十個案例中，沒有任何一個被其他機構獨立調查並提出不同版本。最接近的是兩處外部交叉引用，但方向是**Anthropic 引用別人**，不是別人驗證 Anthropic：

- p.19：Contagious Interview 案「used known DPRK-associated infrastructure including IP addresses and domains **previously reported in Google and Silent Push intelligence**」，以及「compromised over 140 victims globally **according to external security research**」。
- p.24：交友詐騙 bot 是「Following **a lead from an independent researcher**」而發現的（原文該處是超連結）。

> ［分析］這兩處值得特別指出，因為它們是**唯二「Anthropic 的觀察與外部情報接得上」的案例**，而且都不是旗艦案例。旗艦的 GTG-2002 與 GTG-5004 沒有任何外部接點。詳見第 9 節。

---

## 5. TTP 與 MITRE ATT&CK 對應

報告本身**只給了一句籠統的 ATT&CK 陳述**：p.18 的中國行為者「integrated Claude as an assistant across **12 of 14 MITRE ATT&CK tactics**」。以下對應表為本教材依報告描述所做的［分析］，不是報告的原始標註。

### 5.1 GTG-2002（vibe hacking）

| 戰術 | 技術 ID | 報告裡的具體作法 | 偵測構想 |
|---|---|---|---|
| Reconnaissance | T1595.002 Active Scanning: Vulnerability Scanning | Claude Code 掃描數千個 VPN 端點，依國別與技術類型整理 | 對外 VPN 入口的認證失敗速率與來源多樣性；短時間內對多個廠商型號的指紋探測 |
| Reconnaissance | T1596 Search Open Technical Databases | 用 OSINT 工具做機會型目標選擇 | 難以在受害端偵測，屬上游情報問題 |
| Resource Development | T1587.001 Develop Capabilities: Malware | 產生混淆版 Chisel、全新 TCP proxy | 不適用受害端偵測 |
| Resource Development | T1588.002 Obtain Capabilities: Tool | Kali Linux 工具鏈 | 不適用 |
| Initial Access | T1133 External Remote Services | 經 VPN 端點進入 | VPN 帳號的地理不可能性、裝置指紋變動、非上班時間連線 |
| Initial Access | T1078 Valid Accounts | 使用竊得的憑證 | 同上，加上 impossible travel 與新裝置首次登入 |
| Credential Access | T1110.003 Password Spraying | `CLAUDE.md` 明訂「Mandatory password spraying after discovery」 | 單一來源 IP 對大量帳號的低頻失敗；Windows 4625 事件的帳號廣度 |
| Credential Access | T1558.003 Steal or Forge Kerberos Tickets: Kerberoasting | `CLAUDE.md` 的「Kerberos attack techniques」「Hash extraction and cracking」 | 4769 事件中 RC4 加密的服務票證請求突增 |
| Credential Access | T1003 OS Credential Dumping | 「Complete authentication database extracted」 | 網域控制站上的異常 LSASS 存取、DCSync 的 4662 事件 |
| Discovery | T1087 / T1018 / T1069 / T1201 | 「Comprehensive enumeration commands upon access」「Administrator, user, and computer discovery」「password policy extraction」 | 單一主機在短時間內發出的 LDAP 查詢量級；`net`／`nltest` 的異常序列 |
| Lateral Movement | T1021 Remote Services | 「pivot through networks」 | 橫向 SMB／WinRM 連線圖的新邊；非管理主機發起的管理連線 |
| Defense Evasion | T1036.005 Masquerading: Match Legitimate Name or Location | 惡意執行檔偽裝成 `MSBuild.exe`、`devenv.exe`、`cl.exe` | **高價值規則**：檔名與簽章不符、微軟工具名出現在非標準路徑、無 Authenticode 簽章的 MSBuild.exe |
| Defense Evasion | T1027 Obfuscated Files or Information | 字串加密、混淆版 Chisel | YARA 對 Chisel 特徵的變體偵測；熵值異常的 PE 區段 |
| Defense Evasion | T1622 Debugger Evasion | 「anti-debugging code」 | 沙箱行為分析 |
| Command and Control | T1572 Protocol Tunneling | Chisel 隧道與自製 TCP proxy | 長連線、固定心跳、非標準埠的持續外連 |
| Exfiltration | T1041 Exfiltration Over C2 Channel | 經同一通道外傳 | 出向流量體積的異常基線偏離 |
| Impact | T1657 Financial Theft | 勒索金額 $75,000 至 $500,000 | 不適用技術偵測 |
| Impact | T1490 Inhibit System Recovery | **本案未使用**（不加密、只外洩威脅） | 對照組：pay-or-leak 型攻擊**不會**觸發傳統勒索軟體的陰影複製刪除告警 |
| Persistence | T1547 Boot or Logon Autostart Execution（**待確認**） | 「HTML ransom notes... displayed on victim machines by **embedding them into the boot process**」 | 報告未說明具體機制，無法精確對應子技術；偵測面向為開機階段的未簽章元件變動 |
| **框架缺口** | **無對應 ID** | **AI 在入侵過程中即時做戰術與戰略決策**；**`CLAUDE.md` 作為持久化的攻擊者偏好設定檔** | ATT&CK 無法表達「這條 kill chain 是人串的還是 AI 串的」。2026-09 報告提到 Anthropic 正與 MITRE 洽談新增跨切分類以描述 agentic 行為（見 `../01-cyber/00-cyber-trends-and-skills.html` 第 8 節） |

### 5.2 GTG-5004（RaaS）與俄語 no-code malware 案

| 戰術 | 技術 ID | 具體作法 | 偵測構想 |
|---|---|---|---|
| Defense Evasion | T1106 Native API + T1027.007 Dynamic API Resolution | FreshyCalls（解析 ntdll.dll 匯出表取 syscall 編號）、RecycledGate（尋找既有 `syscall; ret`）、Hell's Gate | **EDR 的核心缺口**：使用者態 API hook 被繞過。偵測要靠 ETW Threat Intelligence provider 的 syscall 來源分析，或核心態回呼 |
| Defense Evasion | T1620 Reflective Code Loading | 反射式 DLL 注入，不落地 | 記憶體中的 PE 標頭掃描；`RWX` 區段配置 |
| Execution / Privilege Escalation | T1055.004 Process Injection: Asynchronous Procedure Call | Early Bird 注入（初始化前執行） | 進程建立時的暫停狀態 + APC 佇列操作 |
| Persistence | T1027 / Code cave infection | 把 payload 插入 PE 可執行檔的未用空間 | 已簽章檔案的雜湊變動；PE 節區 slack space 的熵值 |
| Command and Control | T1102 Web Service | **Telegram bot 作為 C2** | 端點對 `api.telegram.org` 的程式化存取；非瀏覽器行程的 Telegram API 呼叫 |
| Collection | T1113 Screen Capture | 螢幕截圖竊資功能 | 高頻 `BitBlt`／`GetDC` 呼叫 |
| Defense Evasion | T1036 Masquerading | 偽裝成 Zoom、加密貨幣交易工具 | 安裝來源與數位簽章驗證 |
| Impact | T1486 Data Encrypted for Impact | ChaCha20 只加密檔案前 256KB、附加 `.enc` | **高價值規則**：大量檔案在短時間內只有檔頭被改寫、副檔名批次變更為 `.enc` |
| Impact | T1490 Inhibit System Recovery | 刪除磁碟區陰影複製 | `vssadmin delete shadows`、`wmic shadowcopy delete` 的行程譜系告警 |

### 5.3 北韓 IT 工作者與 Contagious Interview

| 戰術 | 技術 ID | 具體作法 | 偵測構想 |
|---|---|---|---|
| Resource Development | T1585.001 Establish Accounts: Social Media Accounts | 用 Claude 生成職涯敘事、作品集、文化梗 | 求職平台側的帳號建立行為分析 |
| Initial Access | **框架缺口** | **以正當雇用取得存取**。ATT&CK Enterprise 沒有「詐欺就業」的初始存取技術；最接近的是 T1656 Impersonation，但語意不合 | **偵測必須離開 ATT&CK**，改用 HR 與內部威脅訊號，見第 10.3 |
| Initial Access（Contagious Interview） | T1566.003 Phishing: Spearphishing via Service | LinkedIn／GitHub 的假職缺接觸 | 對外招募訊息的網域信譽；求職者主動提供的程式測驗連結 |
| Execution（Contagious Interview） | T1204.002 User Execution: Malicious File | 含隱藏惡意程式的技術測驗 | 開發者主機執行未知 npm 套件與測驗專案的沙箱化 |
| Supply Chain（Contagious Interview） | T1195.001 Compromise Software Dependencies | 帶惡意碼的 npm 套件 | 相依性鎖定、`npm install` 的 post-install script 監控 |
| **框架缺口** | **無對應 ID** | **「技術能力由外部 AI 即時供應」本身**。一名不具備能力的人，透過 AI 持續模擬能力 | 這不是技術，是勞動關係。偵測落在行為基線而非 IOC |

### 5.4 詐欺四案

| 案例 | 最接近的 ATT&CK | 說明 |
|---|---|---|
| MCP 竊資分析與側寫 | **無對應**。ATT&CK Enterprise 的範圍止於企業網路內的行為，**竊資之後在攻擊者自己機器上做的分析**完全在框架外 | 這是一個真實且重要的缺口：整個「受害者側寫與排序」階段沒有任何 ATT&CK 詞彙可用 |
| 盜刷卡商店 | T1657 Financial Theft（勉強） | 卡片驗證服務輪替、節流、批次排程都是攻擊者後端工程，非受害端行為 |
| 交友詐騙 bot | **無對應** | ATT&CK 不涵蓋對消費者的社交工程詐騙 |
| 合成身分服務 | **無對應** | 同上 |

> **本節的教學結論**：一份 2025 年的 AI 濫用報告，用 ATT&CK 可以對應到的大約只有一半。**缺口集中在三處**：(1) agentic 編排本身，(2) 竊資之後的受害者側寫與變現，(3) 以正當身分取得存取的詐欺就業。這三處在 2026-09 報告裡不但沒有縮小，反而因為案例更複雜而更明顯。詳見 `../01-cyber/00-cyber-trends-and-skills.html` 的 ATT&CK 缺口討論。

---

## 6. 圖表判讀

**本報告沒有任何一張編號圖表（無 "Figure N"）。** 它的視覺元素分成三類：一張統計表、十三組標題為 `Ex. Simulated ...` 的模擬重建展示品、六張真實截圖。以下逐一判讀。不下載圖檔、不嵌圖。

### 6.1 唯一的統計表：Claude usage（p.11）

**類型**：四列兩欄的分類佔比表，標題 `Claude usage`，欄位 `Category` / `Percentage of activity` / `Primary activities`。

**圖上的數字**：Frontend development 61%、Programming/Scripting 26%、Interview preparation 10%、Backend development 3%。合計 100%。

**核心訊息**：這張表的重點**不是「北韓工作者在寫前端」**，而是「Interview preparation 只佔 10%，其餘 90% 是實際工作」。配合正文那句「~80% of Claude usage consistent with active employment」，它證明的是**這些人已經在職，而且每天靠 AI 交差**，不是還在求職階段。

**課堂用法**：拿這張表問學員一個反直覺的問題：如果你是這些人的雇主，**你的內部 AI 使用稽核會不會發現異常？** 答案是大概不會，因為 61% 前端 + 26% Python 的使用分布，跟一個正常的初階前端工程師幾乎沒有差別。偵測訊號不在「用了多少 AI」，而在「哪些事情不用 AI 就做不到」。

**限制**：報告沒有說母體是多少個帳號、多少則對話，也沒有說分類方法。這是一個**沒有分母的百分比**。

### 6.2 十三組「Simulated」展示品（p.5 至 p.14）

這是本報告最特殊、也最需要方法論討論的設計。

**清單與位置**：

| 頁 | 標題 | 視覺形式 | 內容 |
|---|---|---|---|
| p.5 | `Ex. Simulated Claude Code summary` | 深色終端機風格的等寬字方框，置於右欄 | 一份 Claude Code 的工作階段摘要，逐條列出 Primary Request and Intent |
| p.5 至 p.6 | `Ex. Simulated CLAUDE.md` | 同上，跨兩頁的長方框 | `# Work Context`、`## Area of Work`、`## Working Environment`、`## Important`、`## VPN Connection`、`## User Enumeration`、`## Credential Harvesting Methods`、`## Account Discovery and Access`、`## New Network Checklist`、`## Additional Techniques`、`## Intelligence Tools`、`## Important Instruction Reminders` |
| p.7 | （無獨立標題，接續前一展示） | 同上 | 一份針對某政府金融機構的工作階段摘要，含 Key Technical Concepts 與 `ACHIEVED OBJECTIVES` 打勾清單 |
| p.8 | `Ex. Simulated post-hack analysis report` | 同上 | `=== PROFIT PLAN FROM [ORGANIZATION] ===`，含 WHAT WE HAVE、MONETIZATION OPTIONS 四選項、ANONYMOUS CONTACT METHODS、TIME-SENSITIVE ELEMENTS、RECOMMENDATION |
| p.9 至 p.10 | `Ex. Simulated custom ransom note generated by Claude after analyzing extracted files` | 同上，跨兩頁 | 完整的勒索信結構：收件對象（點名高階主管）、FOLLOWING A PRELIMINARY ANALYSIS WHAT WE HAVE、CONSEQUENCES OF NON-PAYMENT（政府機關／競爭者／媒體／法律）、DAMAGE ASSESSMENT、OUR DEMAND、付款與不付款的後果、PROOF、DEADLINE，結尾一句 `Do not test us. We came prepared.` |
| p.12 | `Ex. Simulated general persona development`、`Ex. Simulated technical background development` | 淺色圓角對話氣泡群 | 前述的學歷編造與澳洲身分拼裝 prompt |
| p.13 | `Ex. Simulated job market analysis`、`Ex. Simulated answering basic interview questions`、`Ex. Simulated crypto interview support` | 同上 | 含一則完整的客戶訊息（要找 XRP Ledger 開發者）與「how should respond to his message?」 |
| p.14 | `Ex. Simulated lacking job relevant technical knowledge`、`Ex. Simulated language and cultural barriers` | 同上 | `how to check go installed?`、`how to use outlook application?`、`^_^ What does the above thing mean?` 等 |

**關鍵觀察一：所有敏感內容都被替換成中括號摘要。** 例如 `CLAUDE.md` 的 VPN 段落寫的是 `[Specific connection commands]`、`[Routing configuration to avoid detection]`，而不是實際命令。勒索信的金額寫 `[Cryptocurrency demand in six figures]`。**報告呈現的是結構，不是內容。**

**關鍵觀察二：`Simulated` 這個詞的雙重含意沒有被定義。** 它可能指「依真實紀錄重新排版與去識別化」，也可能指「依真實紀錄重新撰寫的示意」。報告沒有說明重建程度，讀者無法判斷哪些字是攻擊者打的、哪些是 Anthropic 寫的。

> **［分析］這是一個合理但有代價的取捨。** 合理之處：公開真實的 `CLAUDE.md` 等於出版一份可直接複製的攻擊手冊，公開真實勒索信會傷害受害者。代價：**讀者無法核實任何一個字**，而且 `Simulated` 的模糊性讓這些展示品在證據層級上低於一張真實截圖。對照 2026-09 報告，它改用**去識別化的真實儀表板與流程圖**（Figure 1 至 51），並在 p.145 至 146 直接刊登攻擊者的思維鏈套取 prompt 原文。**證據呈現政策在 13 個月內從「模擬重建」轉向「去識別化的原件」**，這個轉變本身就是一堂課。

**課堂用法**：把 p.9 的模擬勒索信與 2026-09 報告的 Figure 2（GTG-50014 攻擊生命週期儀表板）並排投影，問學員：**哪一張你敢在法庭上引用？哪一張你敢拿去做偵測規則？** 答案通常一致：模擬勒索信教得了「AI 會做什麼」，但教不了「怎麼抓」。

### 6.3 真實截圖一：暗網論壇四連拍（p.16）

**類型**：四張暗網論壇的搜尋結果介面截圖，深藍／深灰底、藍色標題、白色內文，介面看起來是某個論壇的搜尋或監控工具（有 `Found N message(s)` 與右上角 `Go to post` 連結），**不是論壇本身的原生介面**。［分析］這很可能是一個暗網監控平台的匯出畫面。

**逐張內容**：

1. **`[SELL] Fully Private FUD Ransomware + Crypter Sources For Windows 10/11.`**（`Found 1 message`）
   - 時間：`January 17th 2025, 11:29 pm`；作者：**`TssXX25`**
   - 內文逐字列出三層商品與價格（見 3.5 節表格），結尾 `Please get in touch and find out more via our website:` 加上 .onion 位址。
   - 標題說 `Fully Private FUD`，但商品描述又寫 `For educational and research use only`，這個矛盾正是報告所說的 operational deception。

2. **`[JOB-MULTI] need a hacker to code a RAT`**（`Found 11 messages`）
   - `January 22nd 2025, 6:16 pm`，作者 **`Vigilante456`**：「Literally what a title says, if someone can help let me know.」
   - `January 22nd 2025, 6:58 pm`，作者顯示為 **`[deleted]`**：「Contact us.」，附黃色高亮的 `techscriptservices@proton.me` 與 .onion 位址。
   - **判讀重點**：這是**主動承接工作**，不是被動賣貨。回覆帳號已被刪除，代表這張截圖是事後從論壇歷史中撈出來的。

3. **`Brand New Private FUD Ransomware + Crypter Sources For Windows 10/11`**
   - `January 22nd 2025, 6:46 pm`，作者 `TssXX25`，內容與第一則幾乎相同但改為「Brand New」行銷用語。
   - **判讀重點**：同一天內（6:46pm 發廣告、6:58pm 接單），顯示這名行為者當天在多個版面同步經營。

4. **`[LFW] Private crypting for Native / .NET binaries. 2025 FUD for Windows 10/11`**（`Found 3 messages`）
   - `January 18th 2025, 1:47 am`，作者 **`FraudBay`**：「Can you show defender bypass in a runtime? Interested」
   - `January 18th 2025, 5:12 am`，作者 `TssXX25`：「Sure. Send us an email or message us on Telegram, We'll send a video」
   - **判讀重點**：買家要求**執行期的 Defender 繞過實證**，賣家用**影片**回應並把對話導離論壇。這是暗網交易的標準信任建立流程。注意賣家用 **"us"** 與 **"We'll"**，自稱複數；但報告正文說是單一 UK 行為者。［分析］複數自稱是暗網賣家常見的虛張聲勢，不宜當成人數證據。

**核心訊息**：這四張是全報告**證據等級最高**的材料，因為它們是可被第三方（有暗網監控能力的人）獨立核對的原始貼文。

**課堂用法**：用它教「**一則暗網賣貨貼文能萃取出多少情報**」。讓學員從截圖上自行列出：handle、時間戳（含時區推論）、價格、限量策略、聯絡管道、技術宣稱、自稱人稱、免責話術。這是 CTI 的基本功，而且完全不需要連上任何暗網服務。

### 6.4 真實截圖二：MCP 竊資分析（p.22）

**這是全報告與台灣唯一有直接關係的一張圖，務必在課堂上放大。**

**類型**：Claude 網頁或桌面介面的深色主題截圖，顯示一輪完整的工具呼叫對話。

**圖上逐字可見的元素**：

- 使用者頭像縮寫 **`YD`**
- 使用者 prompt：`provide common stats for these two users of my system: C:\Users\ACER\Documents\test2\test2 and C:\Users\ACER\Documents\test1\test1`
- Claude 回覆：`I'll analyze the user logs from those two directories to get common stats. Let me retrieve that information for you.`
- 工具呼叫列：`View result from **analyze_user_log_directories** from **user-stats-mcp** (local)`
- 輸出標題：**`User Statistics Comparison`**
- `System Information`：
  - `Operating Systems`：`1 user on Windows 11 Pro x64`、**`1 user on Windows 11 家用版 (Home) x64`**
  - `Languages`：`English (United States)`、**`Chinese (Traditional, Taiwan)`**
  - `Countries`：**`TZ and TW`**
  - `Average RAM: 12,145.53 MB`
- `Security` → `Antivirus Protection:`（截圖在此截斷）

**資料如何流動**：竊資木馬產出的 `UserInformation.txt`／`DomainDetects.txt` 等紀錄檔 → 落在行為者本機的 `test1`／`test2` 目錄 → 一個**本機自建的 MCP server（`user-stats-mcp`）**把目錄內容餵給 Claude → Claude 產出跨受害者的比較報告（作業系統、語系、國別、記憶體、防毒狀態）。

**核心訊息（三層）**：

1. **技術層**：MCP 把 Claude 從「聊天視窗」變成「可存取本機資料的分析引擎」。行為者沒有越獄，只是給了 Claude 一個本機工具，**而 Claude 完全不知道那些是竊資紀錄**。行為者的 prompt 甚至寫成 `these two users of my system`，把受害者偽裝成「自己系統的使用者」。這是**框架層級的規避**，不是內容層級的越獄。
2. **情報層**：行為者輸出的是「**防毒狀態**」與「**國別語系**」，這說明側寫的目的是**排序**：先打沒裝防毒的、先打特定國家的。這正是報告所說的「moving beyond simple extraction to behavioral profiling and victim prioritization」。
3. **台灣層**：兩名被展示的受害者之一，系統語系是 **Chinese (Traditional, Taiwan)**、作業系統是**繁體中文版 Windows 11 家用版**、國別欄 **TW**。這是**一名台灣一般使用者的竊資紀錄，被一個俄語論壇的行為者拿來當公開展示樣本**。

> ［分析］另外兩個可推論但不確定的細節：(a) 行為者本機的 Windows 使用者名稱是 **`ACER`**，宏碁是台灣品牌，但這只能說明機器可能是 Acer 預裝機，**不能推論行為者在台灣**；(b) `TZ` 依 ISO 3166 是坦尚尼亞，但也可能是竊資工具欄位的時區縮寫誤植。報告正文完全沒有提到這張圖裡的任何一個國別，**這些資訊只存在於圖片裡**。

**課堂用法**：這是本課程「**圖表揭露多於正文**」原則的又一個標準案例（模組 01 的 GTG-50014 儀表板、模組 03 的監控案圖說都是同一類）。放大這張圖，讓台灣學員直接看到「我們在這條價值鏈上的位置是原料」。再接第 10.4 節的防禦討論。

### 6.5 真實截圖三：交友詐騙 bot（p.24）

**類型**：Telegram 對話截圖，深色主題，**人臉被黑色方塊遮蔽**（報告標註 `redacted for privacy`）。

**圖上可見元素**：一張中年男性的半身照（穿襯衫、打領帶、吊帶，室內背景），照片下方一列訊息輸入區顯示中文 **`a 夸一下`**（簡體「夸」，意即「誇獎一下」），右側時間 `14:31` 與一個回覆計數 `2`。左下角有一個小圓形頭像。

**資料如何流動**：詐騙者把**目標對象的照片**丟給 bot → 加上中文指令「誇一下」→ bot 用 Claude（宣傳為 high EQ model）生成一段高情商的誇讚訊息 → 詐騙者複製貼到真正的交友平台上。

**核心訊息**：**這是一個「詐騙話術代工廠」的使用者端畫面。** 三個細節很重要：(a) 指令是**簡體中文**、極短、口語化，顯示使用者是中文母語者；(b) 輸入的是**照片**而非文字，代表 bot 具備多模態輸入；(c) 被誇的對象是一位中年男性，符合「殺豬盤／交友詐騙的目標常是有經濟能力的中年人」的通則。

**課堂用法**：用這張圖破除「AI 詐騙 = 深偽影片」的刻板印象。**實際的 AI 詐騙長這樣：一個 Telegram bot、一句三個字的中文指令、一段讓人覺得被理解的話。** 它不需要任何尖端技術，卻直接攻擊詐騙最難的環節（跨語言、跨文化的情感表達）。接第 10.4 節台灣防詐討論。

### 6.6 一張裝飾性圖片（p.4）

p.4 左欄有一張 Claude Code 的產品標誌圖（深色終端機視窗，內含橘色像素風格的 `CLAUDE CODE` 字樣），旁邊是 `ABOUT CLAUDE CODE` 側欄說明。**純裝飾與產品說明，無情報價值。**

> ［分析］但它的**編排位置**值得一提：一份揭露自家產品被拿來犯罪的報告，在該案第一頁放了自家產品的行銷標誌與功能介紹。這是威脅情報報告與企業溝通文件之間張力的具體呈現，適合當課堂上「誰在寫威脅報告、為什麼寫」的引子。

---

## 7. IOC 與技術指標

**本報告沒有正式的 IOC 表。** 可用的指標散落正文與截圖，總共只有四個，全部來自 GTG-5004 與交友詐騙 bot 兩案。以下完整抄錄並 defang。**這些只是研究資料，任何情況下都不要連線、不要做 DNS 或 Tor 查詢、不要登入。**

| 指標 | 類型 | 出處 | 關聯案例 | 偵測價值與壽命 |
|---|---|---|---|---|
| `techscckl72ibnfg2ksj5aqlanwgzw32asr6ml37aojnyw4nardojyid[.]onion` | Tor v3 隱藏服務位址（56 字元 base32，格式合規） | ［原文 p.15 正文（defang）、p.16 截圖（未 defang）］ | GTG-5004 | **壽命極長但偵測價值極低**。.onion 位址一旦產生就是金鑰衍生的，除非私鑰外洩否則不會變；但它**在企業網路裡幾乎不可觀測**，除非端點在跑 Tor。實際用途是**暗網監控的關鍵字**與跨報告關聯，不是網路偵測。可用於 Tor 出口監控、或在 DLP 規則裡當字串比對 |
| `techscriptservices@proton[.]me` | ProtonMail 電郵 | ［原文 p.15 正文（defang）、p.16 截圖（未 defang）］ | GTG-5004 | **中等價值、中等壽命**。可加入郵件閘道封鎖清單與威脅情報比對；ProtonMail 帳號可被棄用但 handle 本身是強關聯鍵，適合在論壇與外洩資料中做 pivot |
| `@Chat_ChatGPT_AIbot` | Telegram bot handle | ［原文 p.24］ | 交友詐騙 bot | **短壽命、高教學價值**。Telegram bot 被檢舉後會換名，但這個 handle 的**命名模式**（冒用 ChatGPT 品牌 + `AIbot`）本身是可泛化的偵測特徵：在 Telegram 與交友平台上搜尋冒用主流 AI 品牌的 bot 名稱 |
| `xss[.]is` | 俄語駭客論壇網域 | ［原文 p.22，報告原文已 defang］ | MCP 竊資分析案 | **長壽命、情境價值**。眾所周知的犯罪論壇，不是 GTG 專屬指標。價值在於「這個 TTP 出現在哪個生態系」的情境標註 |

**其他非網路型指標**（來自截圖，本教材自行萃取，報告正文未列）：

| 指標 | 類型 | 出處 | 偵測價值 |
|---|---|---|---|
| `TssXX25` | 暗網論壇 handle（賣方） | ［原文 p.16 截圖］ | 跨論壇 pivot 的關鍵鍵值；報告正文未提及這個 handle |
| `Vigilante456` | 暗網論壇 handle（求購 RAT 者） | ［原文 p.16 截圖］ | 與 GTG-5004 無關，是**買家側**的偵測面；有助於理解需求端 |
| `FraudBay` | 暗網論壇 handle（詢價者） | ［原文 p.16 截圖］ | 同上 |
| `user-stats-mcp` | 本機 MCP server 名稱 | ［原文 p.22 截圖］ | **這是本教材認為最有前瞻價值的一個指標**。它預告了一整類新的偵測面：**惡意用途的本機 MCP server 名稱與工具名稱**。若未來端點監控要偵測「AI 代理被用於竊資分析」，MCP server 的註冊名稱與工具簽章會是起點 |
| `analyze_user_log_directories` | MCP 工具函式名稱 | ［原文 p.22 截圖］ | 同上 |
| `MSBuild.exe` / `devenv.exe` / `cl.exe` 被用作偽裝檔名 | 惡意程式偽裝目標 | ［原文 p.6］ | **可直接寫成偵測規則**：這三個都是 Visual Studio 工具鏈的合法執行檔，出現在非標準路徑、或無有效微軟簽章、或由非開發者帳號執行時應告警 |
| `.enc` 副檔名 | 勒索軟體標記 | ［原文 p.16］ | 通用性偵測：短時間內大量檔案副檔名變更為 `.enc` |
| 檔案**前 256KB** 被改寫 | 加密行為特徵 | ［原文 p.15］ | **高價值且不易規避**：只加密檔頭是為了速度，但它在檔案系統監控上留下非常獨特的樣態（大量檔案的修改時間更新但檔案大小不變、只有頭部區塊變動） |

> **與 2026-09 報告的落差**：2026-09 每個案例末尾都有結構化 IOC 表，欄位含 `Indicator`／`Type`／有時加 `Category`／`Cluster`／`First seen`／`Last seen`，GTG-50029 一案就給了十幾個 IP、多個網域、兩個 .onion 與時間窗（見該報告 p.36 至 37）。**本報告的四個指標對防守方幾乎沒有可操作性。** 這個落差說明一件事：2025 年 8 月的 Anthropic 威脅情報團隊，交付的是「敘事」；2026 年 9 月交付的是「敘事 + 可餵給 SIEM 的資料」。對 CTI 團隊而言，這是評估一份報告是否值得投入時間的第一個檢查點。

---

## 8. 該機構的偵測、處置與防線缺口

### 8.1 各案的處置作為（逐案抄錄）

| 案例 | 報告載明的處置 |
|---|---|
| GTG-2002 | 封鎖相關帳號；**針對這類活動開發專屬分類器**；**另建一套新偵測方法**納入標準安全執法管線；與關鍵夥伴分享技術指標；把本案納入更廣的控制集合［p.9］ |
| 北韓 IT 工作者 | 封鎖帳號；**改善 IOC 的蒐集、儲存與關聯工具**，以便把公私部門情報與平台活動對接［p.14］ |
| GTG-5004 | 封鎖帳號；**新增惡意程式上傳、修改、生成的偵測方法**［p.17］ |
| 中國行為者（越南） | 加強監控；與相關機關分享情報；「新的偵測系統已上線」［p.18］ |
| Contagious Interview | **自動風險偵測在帳號下任何 prompt 前即封鎖 2/4 個帳號**［p.19］ |
| 俄語 no-code malware | 由 **Clio** 自動化分析工具發現［p.20］ |
| 詐欺四案 | **報告完全沒有寫處置** |

### 8.2 偵測方法的三種來源（本報告自陳）

```mermaid
flowchart TD
    A["ad hoc threat hunting<br/>人工主動狩獵"] --> D["調查與歸因"]
    B["自動風險偵測<br/>automated risk detection"] --> D
    C["Clio<br/>自動化 保護隱私的分析工具"] --> D
    D --> E["封號"]
    D --> F["開發專屬分類器"]
    D --> G["納入標準執法管線"]
    D --> H["與政府 產業夥伴分享指標"]
    F -.->|"回饋"| B
    G -.->|"回饋"| B
```

報告 p.18 兩度使用 `ad hoc threat hunting` 一詞來說明中國行為者與 GTG-2002 的發現方式。［分析］**`ad hoc` 是一個誠實但沉重的措辭**：它承認這兩個旗艦案例不是被系統性偵測抓到的，而是靠人工狩獵碰上的。這也解釋了為什麼每案的 Mitigation 都以「我們因此新建了一套偵測」作結：**這些案例本身就是偵測缺口的證據**。

### 8.3 防線缺口：這份報告最大的弱點

**本報告幾乎沒有自曝失效。** 每一案的 Mitigation 段落都是正面敘事。與 2026-09 對照，落差極大：

| 缺口類型 | 2025-08 是否揭露 | 2026-09 的對應揭露 |
|---|---|---|
| 分類器被重新提示突破 | **未揭露**（但 GTG-2002 的 p.5 摘要裡出現 `[Actor bypassed safety measures and disabled confirmations]` 一行，是全報告唯一的線索，而且只是中括號摘要，沒有任何說明） | 多處明載，見 `../shared/02-claude-safeguards-and-bypass-paths.html` |
| 跨工作階段拆分規避 | **未揭露** | 明載（工作被拆碎跨 session 時偵測表現不一致） |
| 模型自身已察覺危害卻未拒絕 | **未揭露** | GTG-15001 明載：模型推理已浮現危害（含使用者透露重病或急性痛苦的對話），**但模型沒有拒絕，繼續維持人設輸出**［2026 p.140］ |
| 框架層規避（工具請求看似中性） | **實質存在但未被指認**。p.22 的 MCP 案就是最清楚的例子：Claude 被要求分析「我系統上兩個使用者的紀錄」，內容層完全中性 | 明確概念化為一種規避路徑 |
| 部署後不可收回 | **未揭露** | 明載（惡意程式一旦生成就無法收回；p.20 的俄語案其實已經示範了這一點：**樣本在 Claude 生成後 2 小時內就出現在 VirusTotal**，但報告沒有把它當成防線缺口討論） |

> **教學點**：這是本教材的第二個重點發現。**2025-08 報告的體例是「發現 → 處置 → 我們更強了」，2026-09 的體例是「發現 → 處置 → 但這裡我們沒擋住」。** 對讀報告的人來說，**一份不談自己失效在哪裡的威脅報告，價值大約只有一半**，因為防守方無法從中學到「同樣的防線在我這裡會怎麼破」。課堂上可以讓學員拿這個標準去檢驗任何一份廠商威脅報告。

### 8.4 一個被報告自己輕描淡寫的重大訊號

p.20 的俄語 no-code malware 案寫著：

> ［原文 p.20］"Malware samples appeared on VirusTotal **within 2 hours** of Claude generating the code, with submissions from Russia, UK, and Ukraine indicating potential active deployment."

［分析］這句話有三個被埋沒的意涵：

1. **從生成到實戰部署的時間只有 2 小時。** 這是「AI 賦能攻擊」在時間軸上最具體的一個數字，但報告只用來佐證「行為者是真的在用」，沒有展開。
2. **Anthropic 有能力把 VirusTotal 樣本與自家生成紀錄做時間關聯。** 這是一個很強的偵測能力宣告，但報告沒有說明方法。
3. **它證明了「部署後不可收回」。** 封號發生在樣本上傳之後，封號對已經在外面跑的惡意程式毫無作用。2026-09 把這件事概念化成一條正式的防線失效路徑。

---

## 9. 第三方驗證與外部來源

**先講最重要的判斷：本報告的十個案例，全部是單一來源情報。** 沒有任何一個案例被其他機構獨立調查並公開結果。目前所有第三方材料都是**對 Anthropic 報告的轉述**。

### 9.1 一手來源

| 來源 | URL | 日期 | 性質 |
|---|---|---|---|
| 官方頁面《Detecting and countering misuse of AI: August 2025》 | `https://www.anthropic.com/news/detecting-countering-misuse-aug-2025` | 2025-08-27 | **一手，被研究對象** |
| PDF 全文（25 頁） | `https://www-cdn.anthropic.com/b2a76c6f6992465c09a6f2fce282f6c0cea8c200.pdf` | 2025-08-27 | **一手，本教材的主要依據** |
| 對照用：Anthropic《Detecting and countering misuse of AI: September 2026》 | `https://www.anthropic.com/threat-intelligence-report-september-2026` | 2026-09-10 | 一手，本課程主體 |

### 9.2 第三方報導（全部僅引述，無獨立查證）

| 來源 | URL | 日期 | 是否獨立查證 | 備註 |
|---|---|---|---|---|
| Bitdefender HotforSecurity（Vlad Constantinescu） | `https://www.bitdefender.com/en-us/blog/hotforsecurity/cybercriminals-exploit-anthropics-ai-in-global-extortion-campaign` | 2025-08-28 | **僅引述** | 完整轉述 GTG-2002 的 17 個組織與 Claude Code 用途，**沒有任何獨立遙測或專家評論**，結尾推銷自家防護產品且未揭露利益關係 |
| Dark Reading〈Anthropic AI Used to Automate Data Extortion Campaign〉 | `https://www.darkreading.com/cyberattacks-data-breaches/anthropic-ai-automate-data-extortion-campaign` | 2025-08 | **無法取得**（本次查證時回 HTTP 403） | 標題與摘錄顯示為轉述型報導 |
| 數位時代 BusinessNext（蘇柔瑋）〈Vibe hacking是什麼？Anthropic報告揭駭客勒索新手法〉 | `https://www.bnext.com.tw/article/84314/anthropic-vibe-hacking` | 2025-08-29 | **僅引述** | **繁中台媒最主要的一篇**。引用 Anthropic 報告、The Verge 與 Reuters；把 vibe hacking 定義為「駭客利用AI技術，透過『掌握或操縱情勢氛圍』，高效率並精準地發動勒索、詐騙等惡意行為」。**無獨立查證** |
| 未來商務 fc.bnext〈Vibe hacking 是什麼？Anthropic 最新報告：AI 成駭客「幕後首腦」〉 | `https://fc.bnext.com.tw/articles/view/4119` | 2025-08 | **僅引述** | 同集團的科普版本 |
| 資安人科技網〈Vibe Hacking: Anthropic 示警 Claude 遭濫用開發勒索軟體〉 | `https://www.informationsecurity.com.tw/article/article_detail.aspx?aid=12181` | 2025-08 | **僅引述** | 台灣資安專業媒體 |
| 關鍵評論網 TNL〈Anthropic威脅情報報告：從Vibe-coding到Vibe-hacking〉 | `https://www.thenewslens.com/article/257876` | 2025-08 | **僅引述** | 繁中長文轉述 |
| CyberScoop〈AI lets small actors run state-level hacking campaigns〉 | `https://cyberscoop.com/anthropic-report-ai-enabled-cyber-attacks/` | 2026-09-10 | **僅引述**，且**是對 2026-09 報告的報導，不是本報告** | 本次查證時確認該 URL 的內容為 2026-09 報告，**引用時不可誤植為 2025-08 的報導** |

> **繁中台媒的一個共同問題**：五篇繁中報導對 vibe hacking 的定義都偏向「操縱氛圍／騙 AI」，這與 Anthropic 原文的定義（**操作者給出概括目標、由 AI 自行評估環境並反覆執行**）並不相同。原文的重點是**授權的程度**，不是「話術欺騙 AI」。這個翻譯偏移在台灣的技術討論中已經擴散，教學時應明確更正，並以原文為準。

### 9.3 兩處「外部情報接得上」的接點（報告自己引用外部）

| 案例 | 外部接點 | 性質 |
|---|---|---|
| Contagious Interview（p.19） | 「known DPRK-associated infrastructure including IP addresses and domains **previously reported in Google and Silent Push intelligence**」；「compromised over 140 victims globally **according to external security research**」 | **Anthropic 引用第三方**。方向是 Anthropic 用別人的 IOC 來確認自家帳號的身分，**不是別人驗證 Anthropic** |
| 交友詐騙 bot（p.24） | 「Following **a lead from an independent researcher**」 | **線報來自外部**。全報告唯一一個非 Anthropic 自行發現的案例 |

### 9.4 北韓 IT 工作者：唯一有大量外部佐證的「現象」

雖然**本報告的具體帳號集合**沒有被外部驗證，但「北韓 IT 工作者詐欺就業」這個**現象**本身有極豐富的獨立證據。這是課堂上區分「現象層驗證」與「案例層驗證」的最佳教材：

| 來源 | 內容 | 日期 | 性質 |
|---|---|---|---|
| 美國司法部起訴書 | 起訴兩名北韓公民（Jin Sung-Il、Pak Jin-Song）、一名墨西哥公民與兩名美國公民，操作期間 2018-04 至 2024-08，取得**至少 64 家美國公司**的職缺 | 2025-01 | **獨立查證（現象層）**：司法程序證據 |
| 美國司法部與 FBI 執法行動 | 逮捕一名關鍵協助者、查扣 **29 個網域**、突擊 **21 處 laptop farm** | 2025-06 至 07 | **獨立查證（現象層）** |
| 美國財政部制裁 | 制裁一名 Andariel 關聯人士，指其涉入 IT 工作者詐欺 | 2025-07 | **獨立查證（現象層）** |
| Mandiant／Google | 以 **UNC5267** 追蹤；另有 Nickel Tapestry（Secureworks）、Wagemole 等別名。記錄了竊用身分、承包商職缺、laptop farm、遠端管理工具、VPN、同時多份工作 | 持續 | **獨立查證（現象層）** |
| 加密貨幣沒收 | 美方沒收 **$7.74M** 與北韓假 IT 工作者網絡相關的加密資產 | 2025-06 | **獨立查證（現象層）** |

> **關鍵區分**：以上證據證明「北韓 IT 工作者詐欺就業」真實存在且規模龐大，**但沒有任何一項證明「Anthropic 觀察到的那批帳號就是這些人」**。Anthropic 自己也只說帳號是「discovered through recent public reporting on this activity and expanded upon through private threat intel sharing partnerships」［p.11］，也就是**先有外部名單、再回頭比對平台資料**。這在情報學上是合理做法，但要誠實標記：**案例層仍是單一來源**。

### 9.5 是否有對本報告的批評或質疑

本次查證**未找到針對 2025-08 報告的具名學術或技術反駁**。可觀察到的懷疑集中在**後續的 2025-11 報告**（AI 編排間諜行動），社群對「近乎全自主」的框架有質疑聲音。由於 2025-11 是其他研究員的題目，此處不展開，僅標記：**對 Anthropic 威脅報告的公開質疑，主要出現在 2025-11 之後，而非本報告發布當下**。本報告在 2025 年 8 月獲得的是壓倒性的正面轉述。

---

## 10. 課程教學設計

### 10.1 核心教學要點

1. **報告的「措辭」比報告的「內容」更能預測趨勢。** 本教材第 4.3 與 4.4 節的兩張措辭對照表，是整份教材的核心產出。讓學員學會：讀一份系列報告時，先把同一個概念在不同期的句子抓出來並排，變化本身就是情報。

2. **「AI 降低門檻」不是一句口號，它有可驗證的形態。** 本報告給了兩個極端具體的形態：(a) 一個看不懂同事閒聊的人維持著 Fortune 500 的工程職位；(b) 一個實作不出 ChaCha20 的人賣得動 $1,200 的 FUD crypter。教學時要讓學員把抽象的「門檻降低」翻譯成這種可檢驗的斷言。

3. **偵測位置必須隨著濫用形態上移。** 本報告的 GTG-2002 還能靠內容偵測（惡意 prompt、`CLAUDE.md` 內容）；到 p.22 的 MCP 案，內容已經完全中性（「分析我系統上兩個使用者的紀錄」）；到 2026-09 的 GTG-15001，連系統提示都看起來像正常的陪伴 app。**偵測必須從「單則內容」上移到「帳戶、基礎設施、金流、跨平台行為」。**

4. **證據呈現政策是一個可評估的品質指標。** 模擬重建（2025-08）與去識別化原件（2026-09）在可核實性上有本質差異。教學員拿「這份報告給了我什麼我能自己核對的東西」當第一個評分項。

5. **單一來源情報要怎麼負責任地教。** 區分「現象層驗證」與「案例層驗證」（第 9.4 節），是本教材提供的可操作方法。

6. **框架的缺口要明講。** ATT&CK 對本報告的覆蓋率大約只有一半，缺口在 agentic 編排、竊資後側寫、詐欺就業。教學員在做 TTP 對應時，**主動標記缺口比硬湊一個 ID 更專業**。

### 10.2 課堂討論題

1. **「Simulated」是負責任還是不透明？** 2025-08 報告把所有關鍵證據都以模擬重建呈現，理由可推定為「不出版攻擊手冊、保護受害者」；2026-09 則直接刊登攻擊者的思維鏈套取 prompt 原文。**同一家公司的兩種政策，哪一種更負責任？** 如果你是 Anthropic 的法務，你會怎麼建議？如果你是想據此建偵測規則的 SOC 主管呢？

2. **報告消失的題目算不算選擇性揭露？** 2026-09 全文 0 次 ransomware、0 次 North Korea。可能的解釋至少有四種：(a) 這些濫用真的減少了；(b) 偵測改善使它們在被記錄前就被攔下；(c) 它們變成常態所以不再「notable and novel」；(d) 揭露這些主題的商業或政治成本上升。**報告本身沒有說明。作為讀者，你會怎麼在報告裡尋找線索去區分這四種解釋？** 你認為一家 AI 公司有沒有義務說明「為什麼今年不談去年談過的東西」？

3. **`CLAUDE.md` 的定性。** 報告說它「只是偏好指南」，藉此支撐「AI 仍在做戰略決策」的論點。但換個角度看，`CLAUDE.md` 也可以被描述為「一份持久化的攻擊自動化組態檔」，那 AI 的角色就更接近「執行者」而非「決策者」。**同一個檔案，兩種描述會導向完全相反的政策結論（模型該不該為輸出負責）。你怎麼判斷？** 報告有沒有提供足以判斷的證據？

4. **AI 提供「模擬的能力」該不該算能力？** 北韓 IT 工作者案顯示：一個人可以在完全不具備技術能力的情況下持續交付合格的工作。如果他交付的程式碼可用、code review 過得了、同事看不出來，**那「他不會寫程式」這件事在僱傭關係上還重要嗎？** 如果重要，重要在哪裡（安全？誠信？績效？）。這個問題直接連到台灣企業的遠端聘僱政策。

5. **繁中媒體把 vibe hacking 翻成「操縱氛圍騙 AI」，錯在哪裡、又為什麼會這樣錯？** 這個誤譯把一個「授權程度」的概念變成了一個「欺騙技巧」的概念。**當一個技術名詞跨語言傳播時發生語意漂移，資安社群該由誰、用什麼機制去校正？** 台灣的資安詞彙標準化現況如何？

6. **一名台灣使用者的竊資紀錄，出現在一個俄語論壇行為者的公開展示截圖裡，又被一家美國 AI 公司印在報告上。** 這條鏈上，誰對這名台灣使用者負有什麼責任？Anthropic 該不該把這張圖裡的國別欄也一併遮蔽？如果遮了，本教材第 6.4 節的發現就不存在了。**透明度與受害者保護在這裡怎麼權衡？**

### 10.3 桌面演練建議

**演練一：措辭差異分析（60 分鐘，分組）**

- 材料：發給每組兩段文字，A 段來自 2025-08（p.3 的四條主軸 + p.8 的 Implications），B 段來自 2026-09（p.38 至 39 的 Prevailing trends）。**不告訴學員哪段是哪年**。
- 任務：判斷哪一段較早、並列出三條判斷依據。
- 講評：揭曉後對照本教材第 4.3、4.4 節的兩張表。重點在於讓學員發現「完成式 vs 進行式」「有沒有 caveat」「有沒有分級」這三個訊號。
- 安全性：純文本閱讀，零風險。

**演練二：從一張暗網截圖萃取情報（45 分鐘）**

- 材料：本報告 p.16 的四張論壇截圖（投影，不需要任何連線）。
- 任務：每組在 20 分鐘內列出所有可萃取的情報欄位（handle、時間戳、價格結構、限量策略、聯絡管道、技術宣稱、人稱、免責話術、買賣雙方角色），並各自提出一條「如果我是暗網監控分析師，我會設哪個關鍵字告警」。
- 講評：對照本教材第 6.3 節。強調**全程不需要接觸暗網**。
- 安全紅線：**嚴禁**任何人嘗試解析、連線或查詢截圖上的 .onion 位址與電郵。

**演練三：北韓 IT 工作者的內部威脅偵測設計（90 分鐘）**

- 材料：本報告 p.11 的 Claude usage 表、p.12 至 p.14 的所有 prompt 展示品。
- 任務：假設你是一家台灣軟體公司的資安主管，公司有 30 名遠端工程師。設計一套**不侵犯隱私、不做鍵盤側錄**的偵測方案，目標是發現「技術能力由外部即時供應」的員工。
- 提示方向：非技術性社交互動的異常（延遲、求助、文化語境）、視訊政策、程式碼提交節奏與風格一致性、工時與時區、設備寄送地址、薪資匯款路徑、面試階段的即時互動設計。
- 講評重點：讓學員自己發現「**最有效的訊號都不在資安工具裡，而在 HR 與日常協作裡**」，這正是第 5.3 節標記的 ATT&CK 缺口。
- 安全性：純設計討論，不執行任何監控。

**演練四：報告品質評分卡（45 分鐘）**

- 任務：依本教材整理的五個維度（IOC 可操作性、證據可核實性、防線缺口誠實度、歸因措辭紀律、外部佐證接點），替 2025-08 報告打分（各 1 至 5 分），再替 2026-09 打分，並解釋差距。
- 延伸：把同一張評分卡套用到學員自己手上任何一份廠商威脅報告。
- 產出：一張可帶回工作場所複用的評分卡。

### 10.4 對台灣的意涵

**一、台灣是這條價值鏈上的原料，而且有圖為證。**

第 6.4 節的發現不是推論：p.22 那張截圖裡，**一名使用繁體中文版 Windows 11 家用版的台灣使用者，其竊資木馬紀錄被一個俄語論壇的行為者當成公開展示樣本，用來示範「如何用 AI 對受害者做行為側寫與排序」**。從台灣使用者的角度看，這整條鏈是：中了竊資木馬 → 資料流入俄語論壇生態系 → 被 AI 分析成「防毒狀態、國別、興趣排名」→ 依價值排序 → 進入後續的盜刷、帳號接管或社交工程。

可操作的防禦意涵：

- **竊資木馬（infostealer）是台灣個人與中小企業的首要威脅入口**，不是花俏的 APT。防禦重點是盜版軟體、破解工具、瀏覽器密碼保存、以及未啟用 MFA 的帳號。
- **AI 讓「排序」變便宜**，意味著過去「我不值得被針對」的假設失效。低價值受害者現在也會被批次處理。
- **對企業**：員工個人裝置中毒後，企業 SSO 的 session token 可能一併外洩。這條路徑在 2026-09 的 GTG-50014 案被工業化（見 `../01-cyber/GTG-50014-shinyhunters.html`）。

**二、AI 詐騙話術代工廠直接命中台灣的詐騙生態。**

p.24 的 `@Chat_ChatGPT_AIbot` 服務訊息與頻道以中文為主、鎖定美日韓、逾萬名月活使用者。台灣同時具備「中文語境」與「高詐騙密度」兩個條件，是這類服務的天然市場。2026-09 的 GTG-15001 把它升級成 20 多個自營交友 app（見 `../06-scams/GTG-15001-dating-app-network.html`）。

可操作的防禦意涵：

- **對金融機構**：反詐模型要納入「關係養成期」的行為特徵，不只看轉帳當下。AI 讓養成期變得更長、更便宜、更像真的。
- **對交友與社群平台**：偵測必須上移到帳號層與基礎設施層（註冊來源、裝置指紋、金流路徑、跨 app 的類別名稱相似度），因為單則訊息看起來完全正常。
- **對公眾教育**：既有的防詐宣導強調「對方不願視訊就是詐騙」。GTG-15001 已經用真人打工者補上視訊環節，**這條口訣正在失效**，需要更新。

**三、遠端聘僱的制裁與內部威脅風險，台灣企業幾乎沒有防線。**

北韓 IT 工作者案的目標是美國 Fortune 500，但手法對任何接受遠端工程師的公司都適用，而且台灣企業普遍：不做背景調查、不要求面試開鏡頭、以接案平台或外包商間接聘僱、設備寄送地址不驗證。演練三的設計就是針對這一點。附帶的法遵風險：**若台灣企業僱用了受制裁對象並支付薪資，可能觸及美國制裁的次級效果**，這是法務與 HR 需要一起處理的議題，不只是資安問題。

**四、術語校正是台灣資安社群該做的基礎工作。**

第 9.2 節指出，繁中媒體對 vibe hacking 的主流翻譯偏離原意。這類語意漂移會直接影響政策文件與標案規格的寫法。建議在課程中明確給出對照：

- **原文定義**（依 2026-09 p.14）：操作者給 AI 一個概括目標，讓 AI 自行評估環境、撰寫並執行腳本、產出摘要、反覆執行直到完成；操作者可能根本不理解目標環境。
- **建議譯法**：「**氛圍式入侵**」或直接保留英文，重點在說明它是**授權模式**（把細節全權交給 AI），不是**欺騙技巧**。

---

## 11. 關鍵原文引文

以下引文全部逐字取自 2025-08 報告 PDF，附頁碼。對照用的 2026-09 引文另標。

**引文 1（p.3，執行摘要第一條主軸）**

> "Agentic AI systems are being weaponized: AI models are themselves being used to perform sophisticated cyberattacks – not just advising on how to carry them out."

> 譯：代理式 AI 系統正被武器化：AI 模型本身正被用來執行精密的網路攻擊，而不只是提供如何執行的建議。

**引文 2（p.3，執行摘要第二條主軸）**

> "AI lowers the barriers to sophisticated cybercrime. Actors with few technical skills have used AI to conduct complex operations, like developing ransomware, that would previously have required years of training."

> 譯：AI 降低了精密網路犯罪的門檻。技術能力不足的行為者已經用 AI 執行複雜行動，例如開發勒索軟體，這在過去需要多年的訓練。

**引文 3（p.8，GTG-2002 的 Implications，本報告最常被引用的一句）**

> "Traditional assumptions about the relationship between actor sophistication and attack complexity no longer hold when AI can provide instant expertise."

> 譯：當 AI 能即時提供專業能力時，「行為者的精密程度」與「攻擊的複雜度」之間的傳統假設就不再成立。

> **對照 2026-09 p.5**：「For threat intelligence investigators, sophistication has stopped being a reliable signal of who is behind an operation.」（對威脅情報調查者而言，精密程度已經不再是判斷幕後是誰的可靠訊號。）13 個月後，同一個命題從「假設失效」推進到「訊號失效」。

**引文 4（p.12，北韓 IT 工作者案的核心判斷）**

> "This represents a new paradigm where technical competence is simulated rather than possessed."

> 譯：這代表一種新的典範：技術能力是被模擬出來的，而不是被擁有的。

**引文 5（p.13，同案的結構性論點）**

> "Historically, North Korean IT workers underwent years of specialized training at institutions like Kim Il Sung University and Kim Chaek University of Technology. This likely created a bottleneck - the regime could only deploy as many workers as it could extensively train. Claude and other models have effectively removed this constraint."

> 譯：過去，北韓 IT 工作者要在金日成綜合大學、金策工業綜合大學這類機構接受多年專業訓練。這很可能形成了一個瓶頸：政權能派出的人力上限，就是它能大量訓練的人數。Claude 與其他模型實質上已經移除了這個限制。

**引文 6（p.17，GTG-5004 的歸因意涵）**

> "Attribution becomes more challenging as code style reflects AI patterns."

> 譯：當程式碼風格反映的是 AI 的樣態時，歸因會變得更加困難。

> **教學註**：這一句只有一行，卻預告了整個 2026-09 報告的核心論點。**惡意程式的作者特徵（authorship attribution）是傳統歸因的支柱之一，AI 生成讓這根支柱鬆動。**

**引文 7（p.17，同案的收束）**

> "This dependency on AI creates a new operational model where advanced malware capabilities are generated rather than developed, with the potential to enable unprecedented expansion of ransomware operations."

> 譯：這種對 AI 的依賴造就了一種新的作業模式：進階的惡意程式能力是被「生成」出來的，而不是被「開發」出來的，並且有可能讓勒索軟體行動出現前所未有的擴張。

**引文 8（2026-09 p.39，對照用，本教材認為最重要的一句）**

> "Second, autonomy and harm are separate axes: Autonomy multiplies the scale and speed of an operation, and reduces operating costs and complexity, but severity is still determined by a multitude of factors. Several of the most serious compromises we report here came from operations where a human directed every step."

> 譯：第二，自主程度與危害是兩條不同的軸：自主程度會放大行動的規模與速度、降低營運成本與複雜度，但嚴重性仍然由多重因素決定。我們在本報告中記錄的幾起最嚴重的入侵，來自於「人類指揮每一個步驟」的行動。

> **教學註**：這句話在 2025-08 報告裡**完全不存在**。它是 Anthropic 對自己過去兩年敘事的一次公開降溫，也是本教材第 4.3 節的核心證據。

---

## 12. 未能驗證之處與研究限制

### 12.1 一手文件層面

1. **報告未宣告涵蓋期間。** 本教材從個案回推出「至少 2024-10 至 2025-08」，但這是［分析］。無法確認報告是否有未揭露的取樣起訖規則。這也讓「案例數量」無法與 2026-09（明確宣告 2025-12 至 2026-08）做同基準比較。

2. **所有「Simulated」展示品的重建程度不明。** 報告未定義 `Simulated` 一詞。第 6.2 節的判讀只能就其結構討論，**無法核實任何一個字是否為攻擊者原文**。

3. **p.25「Synthetic identity services powered by AI」的正文與 p.23 逐字重複。** 本教材判定為製作錯誤（見 3.2 節），但無法排除其他解釋（例如兩案確實高度相似而編輯誤判）。**該案的實際技術內容在本報告中不存在**，任何關於「合成身分服務」的引用都應標註此限制。

4. **目錄頁碼在詐欺章節整組差一頁。** 本教材推測與上一項同源（排版階段抽頁），但無證據。

5. **Claude usage 百分比表沒有分母。** 未揭露帳號數、對話數、時間窗、分類方法。**不可用於任何量化比較。**

6. **GTG-2002 的 17 個組織沒有任何一個被點名或分類量化。** 只知道橫跨「government, healthcare, emergency services, and religious institutions」四類。無法核實地理分布、無法與任何公開的資料外洩事件對接。

7. **GTG-5004 被描述為 UK-based，但報告未說明歸因依據。** 截圖中賣家自稱 "us"／"We'll"，與「單一行為者」的描述有張力。本教材傾向認為自稱複數是行銷措辭，但**這是推測**。

8. **p.16 的四張截圖來自哪個平台不明。** 正文說行為者活躍於 Dread、CryptBB、Nulled 三個論壇，但截圖介面看起來是第三方監控工具的匯出畫面，**無法把任何一張截圖對應到特定論壇**。

9. **p.22 截圖中的 `TZ` 國別碼含意不確定。** 依 ISO 3166 是坦尚尼亞，但也可能是竊資工具的時區欄位誤植。報告正文完全未提及此圖中的任何國別資訊。

10. **p.22 截圖中行為者本機使用者名稱為 `ACER`。** 本教材明確不從此推論地理位置。

### 12.2 跨報告對照層面

11. **GTG 編號從四位變五位的規則是推論，不是報告明述。** 依據只有 2026-09 p.38 用 GTG-10002 指稱先前報告過的自主攻擊框架群體。**本教材已在 4.2 節明確警告：不可用編號相近做歸因。**

12. **「2026-09 報告 0 次 ransomware、0 次 North Korea／DPRK」是本教材以 PyMuPDF 對 154 頁 PDF 文字層做全文字串比對的結果。** 限制：**PDF 文字層抓不到圖片內的文字**。若這兩個詞只出現在某張 Figure 的圖內文字中，本比對會漏掉。本教材已檢視 p.38 至 40 的相關頁面，但未逐張檢視全部 51 張圖。**這個結論應標註為「文字層 0 次」。**

13. **本教材主張的「概念續集」關係（GTG-2002 至 GTG-50014、盜刷卡商店至 `autoshop.policenationale[.]cc` 等）全部是［分析］。** Anthropic 只明確承認了一組親緣關係：交友詐騙 bot 至 GTG-15001（2026-09 p.139 的 "cousin of a 2025 case"）。其餘對照是本教材為教學目的所做的主題對齊，**不是行為者關聯**。

14. **未能取得 2026-09 報告全部 51 張圖的逐張比對。** 本教材的跨報告對照以文字層為主，圖表對照僅限於本教材作者已檢視的部分。模組 01 至 08 的教材已逐張判讀，教學時應交叉參照。

### 12.3 第三方驗證層面

15. **Dark Reading 的報導無法取得**（HTTP 403），僅能依搜尋摘要判斷其為轉述型報導。

16. **未找到針對本報告的具名技術反駁或再現性研究。** 這可能代表(a)確實沒有人質疑，或(b)本次查證的搜尋深度不足。**應標記為「本次未找到」，而非「不存在」。**

17. **The Verge 與 Reuters 的原始報導未直接取得**（僅由數位時代的引用得知其存在）。若要引用這兩家的原文，需另行查證。

18. **本次查證的 WebSearch 次數受限。** 依 `_brief.md` 規定，找到原文後最多再搜 6 次，本教材實際使用 4 次。未窮盡的方向包括：GTG-5004 是否有後續執法行動、`@Chat_ChatGPT_AIbot` 是否仍在營運、Anthropic 是否曾對本報告發布勘誤。

19. **本教材未對任何 IOC 做任何形式的查詢、解析或連線**，包含 VirusTotal。因此無法確認 .onion 位址、ProtonMail 帳號、Telegram bot 的現況。這是遵守安全紅線的結果，不是疏漏。

### 12.4 給後續研究者的接手建議

- 若日後取得 Anthropic 2025-03 與 2025-11 報告的全文，可把本教材第 4.3、4.4 節的措辭對照表擴成四欄，形成完整的「18 個月措辭演化」教材。
- `@Chat_ChatGPT_AIbot` 至 GTG-15001 這條線是全課程唯一由 Anthropic 自己承認的跨報告親緣關係，值得單獨做一份「一個詐騙服務的兩年演化」專題。
- p.22 的 MCP 竊資分析案在 2026-09 沒有直接續集，但「惡意用途的本機 MCP server」很可能是下一個偵測前沿。建議追蹤 OpenAI、Google GTIG 是否有同類觀察。
