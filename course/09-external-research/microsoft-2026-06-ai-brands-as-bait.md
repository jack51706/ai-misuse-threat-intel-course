# 微軟《AI brands as bait: How threat actors are using the AI hype in social engineering》（2026-06）

> 課程模組：09 延伸研究 ｜ 來源類型：官方威脅報告 ｜ 原文：[AI brands as bait: How threat actors are using the AI hype in social engineering](https://www.microsoft.com/en-us/security/blog/2026/06/08/ai-brands-as-bait-how-threat-actors-are-using-the-ai-hype-in-social-engineering/) ｜ 整理日期：2026-09-21
>
> 證據邊界：本篇只核對微軟官方部落格該篇原文，沒有取得其底層遙測、樣本或處置紀錄。第 7 節 IOC 完整抄錄自原文並一律保持 defang，**課堂與演練絕不得對其連線、解析或查詢**。ATT&CK 對應、偵測構想與演練設計是本教材的教學分析。本篇是[冒用 AI 品牌的攻擊與處置](microsoft-2026-09-ai-themed-attacks-defender.html)（2026-09-10）的技術底稿，兩篇為同一機構的同一條研究線。

## 1. 一頁速覽

- **學習目標：**用一份帶完整 IOC 的一手報告，練習把「品牌冒用」這條與模型完全無關的攻擊線，接進既有的釣魚、惡意廣告與供應鏈偵測流程。
- 這份報告記錄四條行動線：ChatGPT 主題的付款資料釣魚、**Claude 主題的 AiTM 憑證與 token 收割**、假「AI Windows 外掛」惡意廣告投遞 Vidar、以及假 DeepSeek V4 安裝程式放上 GitHub。
- Claude 主題行動觸及**超過 2,000 個組織**，地理集中在美國（62%）、英國（18%）、印度（9%），產業集中在資訊科技（56%）、商業服務（21%）、金融服務（8%）。
- 假 DeepSeek V4 行動的速度是全篇最值得教的數字：DeepSeek 官方在 2026-04-24 宣布 V4 預覽，攻擊者在 **45 分鐘內**建好 GitHub 組織、repo 與 release。
- 該假 repo 在四天內累積 91 顆星、27 次 fork；2026-04-28 測試時，GitHub 搜尋「DeepSeek-V4 installer」**唯一**結果就是它，Bing 對「Deepseek v4 weights github」把它排在官方 Hugging Face 之上。
- 兩個具名行為者：初始存取掮客 **Storm-3075**，以及提供惡意程式簽章即服務（MSaaS）的 **Fox Tempest**。微軟撤銷了歸因於 Fox Tempest 的**逾 1,000 張**程式碼簽章憑證，並於 2026-05 與 Resecurity 合作瓦解其基礎設施。
- 同一支 loader 雜湊出現在 GPT-5.5、Claude Code、Kimi、Seedance、Gemma、GrokCLI、Manus AI、FraudGPT 等多種 AI 品牌的冒名下，證明這是**一套可輪換品牌的投遞基礎設施**，不是針對某一家的行動。
- **這份研究在課程裡要教什麼：**它給 [GTG-50021 假 Claude 轉售商](../01-cyber/GTG-50021-fake-reseller.html)提供了另一個平台、另一種遙測的對照面，並示範一件 Anthropic 側看不到的事：冒用 Claude 品牌的攻擊，**完全不需要碰到 Claude**。

## 2. 報告基本資料

| 欄位 | 核對結果 |
|---|---|
| 機構 | Microsoft Threat Intelligence 與 Microsoft Defender Security Research Team |
| 發布日期 | 2026-06-08 |
| 文件形式 | 官方部落格長文，17 張圖，含 IOC 表與緩解建議清單 |
| 資料型態 | 微軟產品遙測（郵件、端點、身分）加自行測試（搜尋結果排名為研究者於 2026-04-28 實測） |
| 觀察期間 | 原文未給單一起訖；IOC 表的 first seen 最早為 2026-03-10，last seen 最晚為 2026-05-21 |
| 具名行為者 | Storm-3075（初始存取掮客）、Fox Tempest（MSaaS） |
| 與前後期的關係 | 2026-09-10《Detect and disrupt AI-themed attacks with Microsoft Defender》是本篇的高層次續篇，不帶 IOC |

**體裁判讀（本教材分析）：**本篇比 9 月那篇「情報密度高、產品成分低」。它給出可核對的 IOC、時間戳、地理與產業分布，以及研究者自行做的搜尋排名測試。搜尋排名那一段特別值得注意：那是**研究者主動實測**的結果，不是被動遙測，證據性質不同，引用時要分開標註。

## 3. 主要發現與案例逐一摘要

### 3.1 四條行動線總表

| 行動 | 入口 | AI 品牌 | 目標資料／酬載 | 規模數字（原文） |
|---|---|---|---|---|
| ChatGPT 付款資料釣魚 | 郵件 | ChatGPT Plus | 姓名、地址、完整信用卡號、有效期、驗證碼 | 4,500 封（97% 南非）；另一變體單日最高 100,000 封（瑞士、奧地利、南非） |
| Claude 主題 AiTM | 郵件加 PDF 附件 | Anthropic／Claude | 憑證與 access token | 逾 2,000 個組織；美 62%、英 18%、印 9% |
| 假 AI Windows 外掛 | 免費影音盜版站的惡意廣告 | Flux Pro AI（仿名） | Vidar stealer | 2026-03-13 單次行動觸及逾 66,000 台裝置（日、南非、美、法最多） |
| 假 DeepSeek V4 安裝程式 | GitHub 加搜尋引擎 | DeepSeek V4 | Vidar 與其他惡意程式 | 四天 91 星、27 fork；兩個 102 MB .7z 檔 |

### 3.2 ChatGPT 主題：用合法服務串成轉址鏈

誘餌是「To ensure your ChatGPT Plus continues to work – please update your payment method」，威脅七天內降級。

技術上最值得教的是**轉址鏈全部用合法服務**：先經某企業的 Bitrix24 CRM，再經 Amazon 的 `awstrack[.]me` 追蹤網域，再經 Rebrandly 短網址，最後才落到被入侵的 `legendarytrendsbay[.]shop`。中間還有一道自製的 CAPTCHA 樣式「Update payment」按鈕，把自動化分析擋在外面。

**本教材分析：**這條鏈上前三跳都是正常商業服務，網域信譽、分類與白名單全數失效。可用的訊號只剩下「鏈的形狀」：一封外部郵件連續經過 CRM、雲端追蹤與短網址三跳才抵達收款頁，這個**序列**本身才是異常，單看任何一跳都正常。

### 3.3 Claude 主題：假申訴流程與 AiTM

寄件者名稱用「Anthropic Teams」與「Anthropic PBC」，主旨是「Claude Appeal Request」加日期，內容宣稱帳號違反 Acceptable Use Policy，要求查看附件的申訴程序。附件名為 `Fill and Sign Claude Appeal Form.pdf`，要求使用者複製一組申訴 ID 再點「Claude Appeal」連結。

點下去之後：先到 `dash.awaydouble[.]org`，顯示 Cloudflare 驗證頁當作反自動化閘門；通過後到 `servicing.pureplantcravings[.]com`，顯示「Account Appeal Notice」與一組一次性存取碼。原文指出落地頁原始碼**有依行動裝置與桌機分流的條件式轉址邏輯**，最終頁很可能是仿造的 Microsoft 登入流程，用以攔截驗證 token。

**本教材分析：**這是全篇設計最細的一條。三點值得課堂拆解：

1. **誘餌選的是「帳號違規申訴」，不是「訂閱到期」。**違規通知製造的是恐懼與急迫，而且受害者會傾向不聲張、不向同事求證，社交查核這道防線被誘餌本身關掉了。
2. **PDF 只是中繼。**附件不含惡意程式，只含說明與連結，因此附件沙箱引爆可能判定無害。
3. **一次性存取碼是社交工程道具。**它讓受害者以為自己在走一個正規的驗證流程，同時給攻擊者一個自然的理由要求輸入更多資訊。

被冒用的是 Anthropic 的品牌，最終被竊的卻是 Microsoft 的登入 token。**受害、冒名與處置分屬三方**，這是本課治理討論的核心素材。

### 3.4 假 AI Windows 外掛：簽章與沙箱規避

入口是免費影音盜版站的內嵌惡意廣告，彈出「Awesome AI Windows plugin」宣稱提供高畫質免費串流，語境與正在看盜版的使用者完全吻合。下載檔名 `ProFluxeFlowAi-win-Setup.exe`，仿冒真實產品 Flux Pro AI 的命名，託管在 GitHub 的 `shippingtechnologymovie` repo 的 `AI-techVideos` 資料夾。

兩項技術細節：

- **簽章濫用：**該惡意程式用一張經由 Artifact Signing 取得的微軟核發程式碼簽章憑證做了詐簽，指紋 `4f5c5b3ef45cfff7721754487a86aeff9a2e6e32`，歸因於 Fox Tempest 的 MSaaS。
- **沙箱規避：**執行後先顯示一個「Continue」打勾對話框，要使用者點擊才繼續。自動化沙箱不會點，因此觀察不到惡意行為。

酬載鏈：使用者互動後於 `AppData\Local\` 落下 Python 下載器（`pythonw.exe` 與 `LICENSE.txt`），腳本從 C2 `brokeapt[.]com` 載入 shellcode，最終投遞 Vidar。同一基礎設施也被觀察到投遞 Lumma Stealer、Hijack Loader 與 Oyster。

### 3.5 假 DeepSeek V4：45 分鐘與搜尋毒化

時間線（原文 Figure 15）：DeepSeek 官方 2026-04-24 宣布 V4 預覽，攻擊者**45 分鐘內**建立 GitHub 組織 `DeepSeek-V4`、repo `deepseek-V4`、release tag `deepseek-V4`。

可信度包裝：盜用自合法 `deepseek-ai/DeepSeek-V2` repo 的鯨魚品牌圖、真實的 V4 對 Claude Opus 4.6／GPT-5.4／Gemini 3.1 Pro 的評測分數圖、針對搜尋查詢最佳化的標籤（`deepseek-v4-download`、`deepseek-v4-installer`），以及一個重複 SEO 文案的 `llms.txt`，目的是讓 AI 輔助的搜尋引擎也抓得到。

搜尋毒化結果（研究者 2026-04-28 實測）：GitHub 搜尋「DeepSeek-V4 installer」與「DeepSeek V4 install」時，惡意 repo 是**唯一**結果；Bing 對「Deepseek v4 weights github」把它排第一，在官方 Hugging Face 之上；Google 把它與其 fork 排進類似查詢的前四名。

破綻（原文「Staging details revealing the deception」一節）：repo 只有 README、LICENSE、`llms.txt` 與空殼的 assets 與 inference 目錄，沒有任何模型程式碼；九筆 commit 全部在 2026-04-24 由單一作者一次推上；README 宣稱 MIT 授權但 repo metadata 寫 Apache 2.0。四天累積 91 星、27 fork，原文明說**無法確認其中多少是自然流量、多少是灌水**。

酬載：兩個 102 MB 的 .7z 檔，內含偽裝成安裝程式的 Win32 PE。檔案雜湊在三天內輪換三次，檔名與 release 頁面不變。共用 loader（SHA-256 `5455341e…`）下載並安裝 Vidar 與其他惡意程式。

**本教材分析：**「45 分鐘」與「雜湊三天換三次、檔名不變」這兩個數字放在一起，就是一堂完整的 IOC 壽命課。以雜湊為中心的封鎖清單在這條行動線上的有效期是**以天計**；真正穩定的識別特徵是 repo 結構異常（無程式碼、單日單人 commit、授權宣告不一致）與檔名模式，那些三天沒變。

### 3.6 品牌輪換基礎設施

同一支共用 loader 雜湊出現在 GPT-5.5、Claude Code、Kimi、Seedance、Gemma、GrokCLI、Manus AI、FraudGPT 等多個冒名之下。**本教材分析：**這表示「被冒用的品牌」是這套基礎設施最廉價、最常替換的一個參數。任何以品牌為單位的偵測規則，壽命等於下一個熱門模型發布的間隔。

### 3.7 Fox Tempest 與簽章即服務

微軟把 Storm-3075 使用的簽章基礎設施歸因於 Fox Tempest，一個財務動機行為者，經營 MSaaS 供多個下游使用。原文的論證值得整段引用給學生：簽章成本高昂，但對一個鎖定數萬到數十萬台感染的行動，換來的作業系統信任與使用者信任是划算的，而且**已簽章的惡意程式在感染生命週期早期偵測率較低，等於延長有效散布窗口**。

處置：微軟撤銷逾 1,000 張歸因於 Fox Tempest 的簽章憑證；2026-05 微軟 Digital Crimes Unit 與 Resecurity 合作瓦解其基礎設施與存取模式。

## 4. 與 Anthropic 2026-09 報告的對照

| 本課教材 | 對照點 | 兩造差異與不可作的推論 |
|---|---|---|
| [GTG-50021：假 Claude 轉售商與憑證收割](../01-cyber/GTG-50021-fake-reseller.html) | **最直接的對照**：同樣是拿 Claude 品牌當招牌收割憑證 | Anthropic 看到的是冒充轉售、導向其平台的流量；微軟看到的是冒充 Anthropic 寄信、導向仿造 Microsoft 登入頁。**最終要竊的東西不同**，兩份文件沒有共享任何 IOC，不能主張同一行為者 |
| [GTG-50020：AI 供應鏈](../01-cyber/GTG-50020-ai-supply-chain.html) | 兩者都指向 AI 生態系的信任鏈 | Anthropic 案攻擊的是 AI 開發流程內部（評測沙箱、金鑰）；本篇攻擊的是使用者取得 AI 工具的通路（GitHub、搜尋、廣告）。同一條供應鏈的上下游兩端 |
| [GTG-50014：ShinyHunters 附屬產業鏈](../01-cyber/GTG-50014-shinyhunters.html) | 都呈現犯罪服務的模組化分工 | Fox Tempest 的 MSaaS 與 Storm-3075 的 IAB 角色，是本篇對「犯罪即服務」最清楚的證據。Anthropic 側看不到這一層，因為這些環節根本不使用模型 |
| [GTG-15001：交友 app 詐騙網絡](../06-scams/GTG-15001-dating-app-network.html) | 都以消費者財務資料為目標 | Anthropic 案的 AI 是生產工具；本篇的 AI 是誘餌題材。兩者在偵測上沒有交集 |
| [網路行動導論](../01-cyber/00-cyber-trends-and-skills.html) | uplift 三軸的反例 | **本篇沒有任何證據顯示攻擊者使用 AI 產生這些攻擊。**原文從頭到尾談的是 AI 熱度被當成誘餌。把本篇的規模數字算進「AI uplift」是分類錯誤 |
| [安全防護與繞過路徑專題](../shared/02-claude-safeguards-and-bypass-paths.html) | 模型護欄的管轄邊界 | 這四條行動線**沒有一條經過模型推論**。Anthropic 的任何模型層防護、分類器或帳號封鎖都攔不到，能處置的只有郵件、端點、憑證與程式碼託管平台 |
| [證據與方法](../shared/04-evidence-and-methods.html) | 來源獨立性判準 | 本篇與 9 月那篇是同一機構的同一條線，**不構成互證**。與 Anthropic 報告的主題重疊也不是驗證，因為兩邊的遙測看的是不同的東西 |
| [微軟 2026-03 AI as tradecraft](microsoft-2026-03-ai-as-tradecraft.html) | 同機構立場延續 | 微軟持續主張 AI 是力量倍增器而非編排者；本篇甚至更退一步，記錄的是與模型無關的品牌濫用 |

**核心教學點（本教材分析）：**這份報告是檢驗「AI 威脅」定義最好的試金石。四條行動線全部冠上 AI 之名，卻沒有一條需要 AI 參與。若一份年度統計把這類事件算進「AI 相關攻擊」，數字會膨脹，且與 Anthropic 報告的案例在方法論上完全不可加總。模組 09 的價值正在這裡：**對照不只是找相同，更是找出哪些東西根本不該放在同一張表上。**

## 5. TTP 與 MITRE ATT&CK 對應

原文未發布逐案 ATT&CK 對照。下表為本教材的條件式對應，不是微軟的官方映射。

| 戰術 | 技術 | 本報告對應的作法 | 偵測構想（假說，需本地遙測驗證） |
|---|---|---|---|
| 資源開發 | [T1583.001：Domains](https://attack.mitre.org/techniques/T1583/001/) | `awaydouble[.]org`、`brokeapt[.]com` 等專用網域 | 新註冊網域加首次出現於郵件連結的時間差 |
| 資源開發 | [T1583.008：Malvertising](https://attack.mitre.org/techniques/T1583/008/) | 盜版影音站內嵌廣告導向假外掛 | 端點下載來源鏈含廣告網路轉址 |
| 資源開發 | [T1587.002：Code Signing Certificates](https://attack.mitre.org/techniques/T1587/002/) | Fox Tempest MSaaS，逾 1,000 張憑證遭撤銷 | 簽章者與發行者的歷史檔案量；新簽章者首次出現即散布數萬份 |
| 資源開發 | [T1584.006：Web Services](https://attack.mitre.org/techniques/T1584/006/) | 濫用 Bitrix24、`awstrack[.]me`、Rebrandly、GitHub | 外部郵件連結連續三跳經過合法服務才落地 |
| 初始入侵 | [T1566.001：Spearphishing Attachment](https://attack.mitre.org/techniques/T1566/001/) | `Fill and Sign Claude Appeal Form.pdf` | PDF 內含外連結但無巨集或酬載，沙箱判無害仍需記錄連結 |
| 初始入侵 | [T1566.002：Spearphishing Link](https://attack.mitre.org/techniques/T1566/002/) | ChatGPT Plus 付款更新誘餌 | 品牌關鍵字加寄送速率加外部寄件基礎設施 |
| 初始入侵 | [T1204.002：Malicious File](https://attack.mitre.org/techniques/T1204/002/) | 假 DeepSeek `.7z`、假 AI 外掛 exe | 從 GitHub release 下載的可執行檔，與 repo 建立時間差小於數日 |
| 執行 | [T1059.006：Python](https://attack.mitre.org/techniques/T1059/006/) | `AppData\Local\` 下的 `pythonw.exe` 下載器 | 使用者目錄下的 Python 直譯器執行外部載入的 shellcode |
| 防禦規避 | [T1553.002：Code Signing](https://attack.mitre.org/techniques/T1553/002/) | 詐簽的微軟核發憑證 | 簽章有效但發行時間新、簽章者無其他正當產品 |
| 防禦規避 | [T1497：Virtualization/Sandbox Evasion](https://attack.mitre.org/techniques/T1497/) | 「Continue」打勾對話框擋自動分析 | 需互動才展開行為的樣本，應轉人工或互動式分析佇列 |
| 憑證存取 | [T1557：Adversary-in-the-Middle](https://attack.mitre.org/techniques/T1557/) | Claude 主題落地頁攔截驗證 token | token 簽發位置與既有裝置指紋不符 |
| 憑證存取 | [T1528：Steal Application Access Token](https://attack.mitre.org/techniques/T1528/) | 仿造的 Microsoft 登入流程 | 授權同意事件的來源 IP 與使用者常態地理不符 |
| 蒐集 | [T1005：Data from Local System](https://attack.mitre.org/techniques/T1005/) | Vidar、Lumma 等 infostealer | 瀏覽器憑證庫短時間被大量讀取 |
| 跨階段 | 無單一技術 ID | **搜尋引擎與 GitHub 搜尋毒化** | **框架缺口**：ATT&CK 有 malvertising 與 SEO 相關的 T1583.008，但對「在程式碼託管平台內部做搜尋排名操縱」沒有對應技術；`llms.txt` 這種針對 AI 搜尋的最佳化更無位置 |

**缺口說明（本教材分析）：**兩個缺口值得記錄。第一，ATT&CK 不描述誘餌題材，「AI 品牌」整條線沒有欄位。第二，把 `llms.txt` 放進假 repo，是為了讓**AI 輔助的搜尋引擎**抓到並推薦，這是一種新的「對 AI 檢索管道下毒」行為，現行框架無對應技術，值得自建追蹤欄位。

## 6. 圖表判讀

原文有 17 張圖，全部是攻擊鏈示意圖或介面截圖，**沒有一張是可驗算的統計圖表**。本教材未下載圖檔，以下依原文圖說整理重點四張。

| 圖 | 原文圖說 | 課堂用法（本教材分析） |
|---|---|---|
| Figure 5 | “Attack chain of Claude-themed phishing campaign leading to AiTM” | 攻擊鏈判讀主教材。要求學員標出每一跳需要哪一種遙測才看得到，並指出哪一跳失去紀錄就無法還原是否成功 |
| Figure 10 | “Redirect logic identified in landing page source code, differentiating between mobile device and desktop systems” | 分流邏輯的意義：同一 URL 對不同裝置回不同內容，**單次取樣的分析結論可能是錯的**。這是威脅情報取樣偏差的具體案例 |
| Figure 15 | “Fake DeepSeek V4 campaign timeline and attack chain” | 時間線判讀：把官方公告、repo 建立、首次下載、雜湊輪換四個時點標出來，用來計算 IOC 的實際有效壽命 |
| Figure 16 | 假 repo 含盜用 logo、SEO 標籤、單一貢獻者 `graphrtest` 拋棄式帳號、四天 91 星 | 可信度訊號的拆解練習：哪些訊號可偽造（星數、logo、標籤），哪些較難偽造（commit 歷史分布、授權一致性） |

其餘圖為郵件與落地頁截圖（Figure 2、3、4、6、7、8、9、12、13、14、17）與另外兩張攻擊鏈圖（Figure 1、11）。**提醒：**能被截圖示範的樣本通常已被攔截，存在倖存者偏差，不能當作「典型樣貌」的母體。

## 7. IOC 與技術指標

以下完整抄錄自原文 IOC 表，**一律保持 defang 格式**。原文部分指標以未 defang 形式呈現，本教材統一改為 defang。**任何情況下不得對這些指標連線、解析、提交沙箱或查詢互動式服務。**

| 指標 | 類型 | 原文說明 | First seen | Last seen | 偵測價值與壽命（本教材分析） |
|---|---|---|---|---|---|
| `791efb555eefb7215e96659a1353a97416743b66bdd72705493129c64057d40e` | SHA-256 | Claude 主題 PDF 附件 | 2026-04-20 | 2026-04-20 | 壽命極短（單日）。回溯查郵件保存紀錄有價值，前瞻封鎖幾乎無價值 |
| `hxxp://dash.awaydouble[.]org/0v2auth` | URL | PDF 內嵌 URL | 2026-04-20 | 2026-04-20 | 同上。但網域層 `awaydouble[.]org` 可留作歷史比對 |
| `hxxps://github[.]com/shippingtechnologymovie/AI-techVideos/releases/download/13123/ProFluxeFlowAi-win-Setup.exe` | URL | 惡意程式託管（已下架） | 2026-03-13 | 2026-03-14 | 已下架。價值在於**模式**：GitHub release 路徑加 AI 產品仿名 |
| `c7c5072df9f83f4c440a5c3bb4be1d5f6c67bbf78f196406ca20d27b43b975b8` | SHA-256 | `ProFluxeFlowAi-win-Setup.exe` | 2026-03-13 | 2026-03-14 | 兩天壽命 |
| `4f5c5b3ef45cfff7721754487a86aeff9a2e6e32` | SignerSha-1 | 程式碼簽章憑證 | 2026-03-13 | 2026-03-14 | **本表壽命最長的一類**。簽章者身分比檔案雜湊穩定，適合建長期觀察清單 |
| `brokeapt[.]com` | Domain | Python loader C2 | 2026-03-10 | 2026-05-20 | 逾兩個月，**本表最耐久的網路指標**，優先納入 DNS 層偵測（僅被動比對，不主動解析） |
| `pan.ssffaa19[.]xyz` | Domain | Vidar C2 | 2026-03-13 | 2026-03-14 | 兩天。`.xyz` 加隨機字串子網域，模式比單一值有用 |
| `pan.rongtv[.]xyz` | Domain | Vidar C2 | 2026-03-13 | 2026-03-14 | 同上，與前者同構，可抽成模式規則 |
| `hxxps://github[.]com/DeepSeek-V4/deepseek-V4/releases/download/deepseek-V4/deepseek-v4-pro_x64.7z` | URL | 假 DeepSeek repo（已下架） | 2026-04-24 | 2026-04-28 | 四天。教學重點：URL 不變而其下的檔案雜湊換了三次 |
| `0a26238f6c516de5885457c93042531aa59bc206a9537cebf5267cedc6c68531` | SHA-256 | `deepseek-v4-pro_x64.7z`（v1） | 2026-04-24 | 2026-05-18 | 雜湊輪換第一版 |
| `8610d4fb0ec5b525071c2aaec4df0f8fcbb3673aba58a7e1959fc44e83c0e2ca` | SHA-256 | `deepseek-v4-flash_x64.7z`（v1） | 2026-04-24 | 2026-04-28 | 四天 |
| `99231deb373997364381d1eb513d2d42231d418c3a2db9007c5af9bd56ab9371` | SHA-256 | `deepseek-v4-flash_x64.7z`（v2） | 2026-04-26 | 2026-04-28 | 兩天 |
| `25270cc429ada8028b5b33220ed412c47907ecceea7377d608fac5af01bed56a` | SHA-256 | `deepseek-v4-pro_x64.7z`（v2） | 2026-04-26 | 2026-04-28 | 兩天 |
| `56d722b0331bf0aaa86bb37483486c6dff6ad9427fc473ed7c3226c21a9bdd23` | SHA-256 | 解壓後的 PE 執行檔 | 2026-04-26 | 2026-04-28 | 兩天 |
| `5455341ed1bbe75a664fca2dd0794c508e1874f75360253a7ff5bc119bc92d80` | SHA-256 | 共用 loader（跨多個 AI 品牌冒名） | 2026-04-12 | 2026-05-21 | **價值最高的檔案指標**：逾一個月，且橫跨多個品牌冒名，是連結各行動線的樞紐 |

其他原文提及但未列入 IOC 表的字串（供回溯比對，同樣不得查詢）：落地頁 `servicing.pureplantcravings[.]com`、被入侵的收款頁 `legendarytrendsbay[.]shop`、GitHub 組織 `DeepSeek-V4`、貢獻者帳號 `graphrtest`、repo `shippingtechnologymovie`。

**IOC 壽命總結（本教材分析）：**14 筆指標中，10 筆壽命在四天以內，只有 3 筆超過一個月（`brokeapt[.]com`、共用 loader 雜湊、簽章者指紋）。這正是本課反覆強調的原則：**把偵測投資放在結構與行為，不要放在會被輪換的值上。**

## 8. 該機構的偵測、處置與防線缺口

**處置（原文陳述）：**撤銷逾 1,000 張歸因於 Fox Tempest 的程式碼簽章憑證；2026-05 Digital Crimes Unit 與 Resecurity 合作瓦解 Fox Tempest 的基礎設施與存取模式；假 GitHub repo 與惡意程式託管頁面已下架（IOC 表註記 taken down）。

**緩解建議（原文列出，逐項摘要）：**啟用 Defender XDR 的自動攻擊中斷；對所有帳號強制 MFA 並移除排除名單，「require MFA from all devices in all locations at all times」；使用 Microsoft Authenticator 的 passkey 與 MFA，並以條件式存取政策配合；特權帳號使用抗釣魚 MFA；啟用 Office 365 的 Zero-hour auto purge（ZAP）以在取得新情資後追溯隔離已投遞郵件；設定 Safe Links 在點擊時重新檢查連結；採用會封鎖惡意網站的瀏覽器與 SmartScreen；啟用 network protection 阻擋惡意網域。

**防線缺口（本教材分析）：**

1. **緩解建議幾乎全是微軟自家產品設定。**對不使用該生態系的組織，這份清單的可移植性有限。可移植的原則其實只有三條：抗釣魚 MFA、工作階段層級的追溯處置、以及點擊時（而非投遞時）的連結檢查。
2. **三條非郵件路徑沒有對應的緩解措施。**惡意廣告、GitHub 散布與搜尋毒化這三條路徑，原文只描述現象，緩解清單裡沒有任何一項直接針對它們。搜尋引擎排名的處置責任在誰，原文未談。
3. **沒有誤報率、沒有漏接案例。**逾 1,000 張憑證撤銷是分子，沒有分母（Fox Tempest 總共取得多少張？撤銷後多久恢復供應？）。
4. **平台責任邊界空白。**GitHub 讓一個 45 分鐘內建好、無任何程式碼的 repo 佔據搜尋首位四天，原文沒有討論託管平台的偵測責任。被冒名的 Anthropic、OpenAI、DeepSeek 能做什麼，也未著墨。
5. **簽章生態的結構問題未解。**憑證是經由 Artifact Signing 正當取得後詐用。撤銷是事後補救，取得環節的把關為何失效，原文未揭露。

## 9. 第三方驗證與外部來源

| 來源 | 日期 | 本篇使用範圍與證據地位 |
|---|---|---|
| [微軟官方原文](https://www.microsoft.com/en-us/security/blog/2026/06/08/ai-brands-as-bait-how-threat-actors-are-using-the-ai-hype-in-social-engineering/) | 2026-06-08 | 直接來源核對，**不是**第三方驗證 |
| [微軟 2026-09-10 續篇](https://www.microsoft.com/en-us/security/blog/2026/09/10/detect-and-disrupt-ai-themed-attacks-with-microsoft-defender/) | 2026-09-10 | 同機構同一條線的後續，**不構成互證** |
| Resecurity（原文提及的合作方） | 2026-05 | 原文陳述其參與瓦解 Fox Tempest。**本次未取得 Resecurity 自身的公開說明**，故無法確認為獨立佐證 |
| [MITRE ATT&CK 各技術頁](https://attack.mitre.org/techniques/T1557/) | 查閱 2026-09-21 | 只核對技術定義，不驗證微軟的任何主張 |
| [本課 GTG-50021 教材](../01-cyber/GTG-50021-fake-reseller.html) | 原報告 2026-09-10 | Anthropic 平台側遙測。主題重疊但**無共享 IOC**，不得宣稱同一行為者 |

**單一來源判定：**本篇所有事件主張、遙測數字、歸因（Storm-3075、Fox Tempest）與處置成果，**目前皆為微軟單一來源**。搜尋排名那一段是微軟研究者於 2026-04-28 的自行測試，屬**該機構的一手實測**，性質上仍是同一來源；任何人想複現也已不可能，因為 repo 已下架。截至本次查閱，沒有取得任何第三方對本篇數字的獨立重現。

## 10. 課程教學設計

### 10.1 核心教學要點

學員完成後應能：(1) 用本篇 14 筆 IOC 的 first/last seen，實際算出不同指標類型的壽命分布，並據以排定偵測投資順序；(2) 說明 AiTM 與詐簽為何讓「檢查網址」與「檢查數位簽章」兩種傳統教育同時失效；(3) 判定一份冠上 AI 之名的報告，其事件是否真的涉及 AI，並說明錯誤歸類會造成什麼統計後果。

### 10.2 課堂討論題

1. 假 DeepSeek repo 在 GitHub 搜尋中是「唯一結果」，在 Bing 排名高於官方 Hugging Face。程式碼託管平台與搜尋引擎對此有沒有偵測責任？如果有，門檻應該訂在哪裡（45 分鐘？無程式碼？單人單日 commit？）
2. 冒用 Anthropic 品牌、竊取 Microsoft token、由微軟處置、在 GitHub 散布。四方之中誰該主責通報受害者？台灣的法規與通報機制能處理這種跨方事件嗎？
3. 本篇 14 筆 IOC 有 10 筆壽命不到四天。那麼情資分享機制（ISAC、TWCERT/CC）交換 IOC 的實際效益是什麼？該改交換什麼？
4. 「Continue 打勾才執行」擋掉自動沙箱。如果把沙箱改成會自動點擊所有按鈕，會產生什麼新問題？
5. Fox Tempest 的 MSaaS 讓惡意程式取得微軟核發的有效簽章。對一個把「有效數位簽章」寫進白名單政策的組織，這代表什麼？政策該怎麼改才不會退回全面封鎖？
6. 這四條行動線都沒有用到 AI。若你負責撰寫公司的年度威脅報告，要不要把它們算進「AI 相關事件」？兩種選擇各會誤導誰？

### 10.3 桌面演練建議

**虛構情境：**某台灣金控的資安團隊（受規管、需留存稽核軌跡）發現三件事：(a) 三名員工收到「Claude 帳號違規申訴」郵件，其中一人開了 PDF 並點了連結；(b) 一名開發者從 GitHub 下載了「某新模型的離線安裝包」；(c) 端點管理系統回報一支**具有效微軟簽章**的新程式在 12 台機器上執行。

學員只使用課堂提供的虛構紀錄與本篇 IOC 表，**全程不得對任何網域、URL 或雜湊連線、解析或提交查詢**。交付一份三頁以內的處置與改善建議，須包含：

1. 三件事的**優先順序**與判定理由，說明各自最快能取得的決定性證據是什麼。
2. 針對 (a)：若確認為 AiTM，列出密碼重設以外必須執行的工作階段層級動作，並說明每一項的驗收證據。
3. 針對 (c)：既然簽章有效，還有哪些欄位可用來判斷可疑（提示：對照本篇的簽章者指紋壽命分析）。
4. 一張「偵測投資排序表」：用本篇 IOC 的 first/last seen 算出壽命，把偵測資源分配到結構性特徵而非單一值，並標明每一項所需的遙測來源與目前是否具備。
5. 一項需要跨部門協調的措施（例如開發者取得第三方 AI 工具的官方來源清單），標負責人、時程與例外處理。

| 配分（本課設計） | 合格條件 |
|---|---|
| 25 分 | 三件事優先排序合理，並指出各自的決定性證據 |
| 25 分 | 偵測投資排序以實際壽命計算為依據，不是憑印象 |
| 20 分 | 對 AiTM 提出工作階段層級（而非密碼層級）處置，含驗收證據 |
| 15 分 | 每項措施有負責人、完成證據與例外期限 |
| 15 分 | 明確分開原文陳述、本教材分析與本地假說 |

對演練 IOC 執行任何查詢或連線、或把本篇事件直接歸類為「AI 攻擊」，必須修正後重繳。

### 10.4 對台灣的意涵

- **誘餌語境高度適用。**台灣企業與機關使用的生成式 AI 服務多為境外訂閱，收到英文的「帳號違規」「付款更新」通知是常態，使用者缺乏可靠的真偽判準。「申訴」誘餌尤其危險，因為它讓受害者傾向不聲張。
- **開發者取得管道的風險最高。**中文技術社群大量透過轉載安裝包、鏡像站與第三方整理的 repo 取得工具，這正是假 DeepSeek 行動的理想通道。建議機關與企業建立「官方下載來源清單」，並把它接進[公部門人工智慧應用參考手冊](moda-2026-01-public-sector-ai-playbook.html)所要求的 AI 工具盤點。
- **簽章白名單政策需重檢。**不少本地組織以「有有效數位簽章」作為端點執行政策的放行條件。Fox Tempest 的 MSaaS 直接打穿這個假設，但全面封鎖不可行，應改以簽章者歷史檔案量與首次出現時間為輔助欄位。
- **IOC 交換機制的定位。**本篇證明多數 IOC 壽命以天計。台灣的情資分享應同時交換**結構性特徵與偵測邏輯**（例如「GitHub release 下載的可執行檔，其 repo 建立時間差小於 N 天」），而不只是交換會迅速失效的雜湊與網域清單。
- **跨方通報的空白。**冒名方、受害方、處置方與託管方分屬四個境外實體時，台灣受害組織的通報路徑目前並不清楚，這是值得政策層面討論的缺口。

## 11. 關鍵原文引文

| 英文原文 | 繁中理解 | 出處 |
|---|---|---|
| “To ensure your ChatGPT Plus continues to work – please update your payment method” | 為確保您的 ChatGPT Plus 持續運作，請更新付款方式 | ChatGPT 主題行動的郵件主旨 |
| sender names “Anthropic Teams” and “Anthropic PBC” | 寄件者名稱冒用「Anthropic Teams」與「Anthropic PBC」 | Claude 主題行動 |
| “Fill and Sign Claude Appeal Form.pdf” | 假申訴表單 PDF 的檔名 | Claude 主題行動附件 |
| “Awesome AI Windows plugin” | 假外掛的廣告名稱 | 惡意廣告行動 |
| the repository embedded “SEO-optimized tags” and an `llms.txt` repeating SEO copy “for AI-assisted search engine discovery” | 假 repo 內嵌 SEO 最佳化標籤，並用 `llms.txt` 重複文案，目的是讓 AI 輔助的搜尋引擎找到它 | 假 DeepSeek 行動 |
| the README claimed MIT licensing while repository metadata specified Apache 2.0 | README 宣稱 MIT 授權，repo metadata 卻寫 Apache 2.0 | Staging details revealing the deception |
| signed malware “typically exhibits lower detection rates early in infection lifecycles, extending effective distribution windows” | 已簽章的惡意程式在感染生命週期早期偵測率通常較低，因而延長了有效散布窗口 | Fox Tempest 一節 |
| “require MFA from all devices in all locations at all times” | 對所有裝置、所有地點、所有時間一律要求 MFA | 緩解建議 |
| “Zero-hour auto purge (ZAP) … retroactively neutralize malicious phishing, spam, or malware messages that have already been delivered to mailboxes” | ZAP 可在事後追溯中和已投遞到信箱的惡意郵件 | 緩解建議 |

原文未標示頁碼，以上定位到章節。全文以[官方原文](https://www.microsoft.com/en-us/security/blog/2026/06/08/ai-brands-as-bait-how-threat-actors-are-using-the-ai-hype-in-social-engineering/)為準。

## 12. 未能驗證之處與研究限制

- 本次查核**只核對官方部落格網頁**，沒有取得微軟的底層遙測、樣本、憑證撤銷清單或處置紀錄。
- 規模數字（4,500 封、100,000 封／日、2,000 個組織、66,000 台裝置、逾 1,000 張憑證）**皆未揭露分母與計數單位**，本教材只引用不換算。地理與產業百分比的母體為微軟可見的部分，不是全球母體。
- 91 星與 27 fork 中自然流量與灌水的比例，**原文明說無法確認**，本教材不作推論。
- 搜尋排名結果是微軟研究者 2026-04-28 的單次實測。搜尋結果因地區、個人化與時間而異，且 repo 已下架，**任何人皆無法複現**。
- Storm-3075 與 Fox Tempest 的歸因依據，原文未揭露。Storm-xxxx 與 Tempest 是微軟內部代號體系，與其他機構的編目無自動對應關係。
- Resecurity 參與瓦解一事，**本次未取得該公司自身的公開說明**，故不計為獨立佐證。
- 本篇與 [GTG-50021](../01-cyber/GTG-50021-fake-reseller.html) 是否指向同一行為者，**未知**；兩邊沒有公開可比對的 IOC，本教材不作此推論。
- 第 5 節的 ATT&CK 對應、第 7 節的壽命分析與偵測價值評註、第 10 節的演練與評分規準，皆為本教材的教學分析與設計，**不是**微軟發布的內容，也未經實測驗證誤報率。
- 本篇的四條行動線**沒有證據顯示攻擊者使用 AI 產生攻擊內容**。若未來有此類證據出現，應另行補註，不可回溯改寫本篇結論。
