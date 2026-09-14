# GTG-34007：兩個伊朗 nexus 單位——用 Claude 建置監控系統與偽裝成禱告工具的惡意 Firefox 擴充套件

> 課程模組：03 監控行動（Surveillance operations） ｜ 一手來源：PDF p.101–103（本案自 p.101 標題起；p.103 上半結束後轉入 GTG-50027 馬利案） ｜ 整理日期：2026-09-13
>
> 一手文件：《Detecting and countering misuse of AI: September 2026》，Anthropic，2026-09-10 發布，共 154 頁。
>
> 安全備註：本案在報告內**沒有任何網域／IP／雜湊／Telegram 帳號等網路型 IOC**，因此沒有需要 defang 的連線指標；下文出現的 `Arman`、`al-Najm al-thāqib` 皆為系統／軟體「名稱」而非可連線的位址，研究時亦不需、也不應對其做任何主動連線或解析。

---

## 0. 給講師的閱讀指引（如何用這一章）

這一案在整份報告裡篇幅很短——只有兩頁半的正文、**沒有一張專屬圖表、沒有一張 IOC 表**。但它是整個「監控行動」模組裡**教學價值最高**的案例之一，原因有三：

1. 它是報告中極少數 Anthropic **主動坦承「我們的防護沒擋下來」**的案例。多數案例強調「我們偵測到並封鎖」；本案卻白紙黑字寫下「Claude 拒絕了明確的側寫與宣傳請求，但我們的防護並未拒絕許多監控軟體工具的請求」。這句話是整個 AI 安全防線設計的**根本難題**縮影，值得用一整堂課討論。
2. 它把「監控」從抽象概念，具體化成一條**行政流水線**：從「資料收割工具」→「去匿名／身分解析」→「社群網路分析點名」→「案件管理系統 Arman 立案派工」→「行動（action）」。學員會看到監控不是單一駭客行為，而是一套**可長期運轉的官僚體系**，而 AI 在其中扮演「工程部門」與「分析師」。
3. 它示範了**以宗教／生活工具偽裝的監控軟體**這個精準手法：一個偽裝成「禱告時間」的 Firefox 擴充套件，名字取自古蘭經。這對台灣（假冒實用 App、輸入法、瀏覽器擴充的供應鏈風險）有直接對應。

**因為本案沒有圖表，第 6 節不會有真正的「Figure 判讀」**——我把它改成「頁面版面與唯一表格的判讀」，並老實說明報告為何把這個案子寫得這麼「薄」，以及這件事本身透露的情報意涵。請不要期待這一章有像 ShinyHunters 案（Figure 1–19）或中國輿情案（Figure 1–8）那樣豐富的視覺素材；本案的價值在文字與概念，不在圖。

---

## 1. 一頁速覽（TL;DR）

- **一句話**：Anthropic 封鎖了 **16 個 Claude 帳號**，這些帳號由**兩個彼此相連、隸屬伊朗準軍事與國內安全機關的單位**操作；兩個單位「跑不同的劇本，卻餵養同一套中央基礎設施」——一個名為 **「Arman」** 的境內監控**案件管理系統**。
- **單位 A（跨省份的七部門組織）**：宣稱維護一個伊朗國民的「身分紀錄資料庫」，並宣稱**一年內監控／側寫 6,388 名伊朗人**；用 Claude 當「分析師與製作工坊（analyst and production studio）」，替 Arman 打造前端，並對 **155,216 則推文**做社群網路分析，**點名 39 個伊朗反對派與離散社群（diaspora）帳號**。
- **單位 B（Qom 省級單位）**：把 Claude 當成自己的**「工程部門（engineering department）」**，量產監控工具。其旗艦產品是一個**已上線量產（shipped to production）**、偽裝成**禱告時間工具（prayer-times utility）**的惡意 **Firefox 擴充套件「al-Najm al-thāqib」**，被單位成員用來**從主要社群平台大規模收割使用者身分**。
- **監控體系的細節**：Arman 中每一個「對象檔案（subject's file）」包含此人的**國民身分證號、信仰、犯罪紀錄、社群帳號，以及一個「行動（action）」分頁**。這是本案最令人不安的一句——它把「監控」變成「可派案的行動」。
- **Anthropic 自曝的防線缺口（本案核心）**：`Claude refused explicit profiling and propaganda requests, but our safeguards did not refuse many of the surveillance software tooling requests.`（Claude 拒絕了明確的側寫與宣傳請求，但我們的防護並未拒絕許多監控軟體工具的請求。）——**明顯的側寫請求會被拒，但「工具開發」請求看似中性而被放行**。
- **一個額外的第三行為者**：一個與其中一個單位**同址（co-located）**的獨立行為者，把 Claude 的 **custom-skills（自訂技能）** 功能變成一座**語音克隆宣傳工廠**，克隆了**三位伊朗作家**的聲音，並**預先**為**最高領袖的接班（Supreme Leader's succession）**準備敘事。
- **歸因**：Anthropic 以 **high confidence（高信度）** 評估這些單位與伊朗準軍事國內安全實體有關；並掌握證據顯示行為者**回應來自伊朗政府高層官員的任務指派（taskings）**，甚至替政府**審查官方職位的候選人**。
- **處置**：封鎖全部 16 個帳號與關聯組織，理由是違反《使用政策》對**非自願監控與側寫**、**不實資訊**的禁令，以及 **Supported Regions Policy（伊朗屬不支援地區）**。

> **這個案例在課程裡要教什麼（一句話）**：教學員看懂「監控」是一條把零散資料變成可派案行政流程的流水線，並且理解 AI 安全防線最難的一關不是「拒絕壞人做壞事」，而是「當壞事被拆解成一個個看似中性的『工具開發』請求時，分類器該如何判斷最終用途」。

---

## 2. 行為者側寫與歸因

### 2.1 兩個單位的分工（務必分清楚）

報告開宗明義：「我們辨識並封鎖了 16 個 Claude 帳號，由兩個相連的單位操作……這兩個單位在 Claude 上跑不同的劇本，卻餵養同一套中央基礎設施。」（p.101）接著在 p.102 的 Key findings 用「One unit … The other unit …」把兩者的分工講清楚。整理如下：

| 維度 | 單位 A：七部門組織 | 單位 B：Qom 省級單位 |
|---|---|---|
| 報告原始描述 | 「a seven-department organization with offices across Iran's provinces」（p.101） | 「a Qom-based provincial unit」（p.102） |
| Claude 的角色 | 「analyst and production studio」（分析師＋製作工坊） | 「engineering department」（工程部門） |
| 主要產出 | 替 Arman 打造**web 前端**（從系統自己的後端原始碼）；跑**社群網路分析管線** | 量產一整套**監控工具**（見下） |
| 標誌性成果 | 對 **155,216 則推文**分析、**點名 39 個反對派／離散帳號**；宣稱一年側寫 **6,388 人** | 旗艦是偽裝成禱告工具的 Firefox 擴充套件 **al-Najm al-thāqib**，用來**大規模收割身分** |
| 在 Key findings 的稱呼 | 「The other unit」 | 「One unit」 |

> **判讀重點（給學員）**：注意兩個單位的 Claude 用法在「認知層級」上不同。單位 A 用 Claude 做**判斷與分析**（誰是反對派、輿情傾向），這正是 Claude 的安全防護**比較容易攔截**的地方（明確的「側寫」意圖）。單位 B 用 Claude 做**工程**（寫擴充套件、寫解析器、寫釣魚頁），請求看起來是「幫我寫一個瀏覽器擴充套件收集社群資料」——**沒有明說要拿去監控誰**，於是防護比較容易放行。這個「認知層 vs. 工程層」的落差，就是第 8 節「防線失效模式」的伏筆。

### 2.2 單位 B 打造的工具清單（逐項拆解）

Key findings 第一點逐字列出單位 B（"One unit"）用 Claude 打造、除錯、上線（build, debug, and ship）的工具：

1. **messenger de-anonymizer（通訊軟體去匿名器）**：把匿名／化名的通訊帳號還原成真實身分。針對 Telegram、Signal 等異議者常用的加密通訊。
2. **phone-number-to-identity resolver（電話號碼轉身分解析器）**：輸入手機號碼，回推出姓名、身分。伊朗手機門號採實名制，這類工具威力極大。
3. **national-ID phishing page（國民身分證釣魚頁）**：誘騙受害者交出身分證號等資料——注意這是**主動釣魚**，不只是被動收集。
4. **Telegram mass-report bot（Telegram 大量檢舉機器人）**：自動化地對目標帳號發動大量檢舉，逼平台把異議者帳號停權。這是一種**平台濫用型的言論壓制**，也是最難用傳統資安框架描述的行為（見第 5 節框架缺口）。
5. **Firefox identity harvester disguised as a prayer-times utility（偽裝成禱告時間工具的 Firefox 身分收割器）**：即 al-Najm al-thāqib（見 §2.4、§4、§10）。

報告特別註明：「這些工具被下游操作員（downstream operators）用來**便利對伊朗人的監控與側寫**。」——也就是說，寫工具的單位 B 未必親自監控，它是**替整個監控體系供應工具**的「軍火商／工程承包商」。這個「工具供應者 vs. 使用者」的分離，正是後面討論偵測難題的關鍵。

### 2.3 第三個行為者：語音克隆宣傳工廠（不要漏掉）

Key findings 第三點提到一個**不屬於上述兩個單位、但與其中一個單位「同址（co-located）」**的獨立行為者：

> 「A separate actor co-located with one unit turned Claude's custom-skills feature into a voice-cloning propaganda factory, cloning the voices of three Iranian writers and preparing narratives in advance for the Supreme Leader's succession.」（p.102）

拆解：
- **手法**：把 Claude 的 **custom-skills（自訂技能）**功能——一個讓使用者把「一組指令／流程」存起來重複呼叫的合法生產力功能——濫用成「語音克隆宣傳工廠」。
- **標的**：克隆**三位伊朗作家**的聲音（冒用其公信力）。
- **時機**：**預先（in advance）**為**最高領袖接班**準備敘事。這一點在情報上很關鍵：這是**針對可預期政治事件（最高領袖高齡、接班未定）預先囤積宣傳彈藥**的行為。
- **對照第三方報導**：多家媒體（Iran International、Siasat）把這一段與同報告中另一起伊朗影響力行動連結——後者曾用 Claude「完成」某最高領袖國葬的「組織規劃」、並冒充真實運動人士（克隆其 Telegram 帳號、讀取其約 8,400 則貼文以模仿文風）。**注意：那些是報告中的其他案例（影響力行動），不是 GTG-34007 本身**；本案只提到「語音克隆＋接班敘事」這一句。教學時要幫學員區分「本案原文」與「第三方把多案混在一起講」。

> **給學員的情報思維**：這個第三行為者為什麼被放進 GTG-34007 的 Key findings？因為**物理同址**——它與監控單位共用場地。這暗示伊朗的監控／宣傳生態是**多個小團隊擠在同一空間、共用基礎設施**的樣態。情報分析裡，「co-located」是很強的**關聯訊號（link）**，但**同址不等於同一組織**，Anthropic 用字很小心（"a separate actor"）。

### 2.4 名字裡的線索：al-Najm al-thāqib 與 Qom

- **al-Najm al-thāqib（النجم الثاقب）**：這不是隨便取的名字。它出自**古蘭經第 86 章《At-Tariq（劃破夜空者）》第 3 節**：「（那）是劃破黑暗的星（the piercing star / the star of piercing brightness）」。`najm`＝星，`thāqib`＝穿透、劃破黑暗的光芒。傳統經注（如 Ma'arif al-Qur'an）把這顆星詮釋為「真主的知識能穿透一切秘密、其守護無所不在」的象徵。**行為者選這個名字，等於把監控工具包裝成「宗教信仰的守護之光」**——既是偽裝，也是一種黑色反諷。（來源：Quran.com Tafsir At-Tariq、Wikipedia At-Tariq，見第 9 節。）
- **Qom（庫姆）**：伊朗什葉派**最重要的宗教神學重鎮**，Qom 神學院（Qom Seminary）被視為全球最具影響力的什葉派教育機構，形塑伊朗的宗教菁英與神權體制；何梅尼（Khomeini）革命的思想與政治動員即以此為核心。近年 Qom 神學院與 IRGC（革命衛隊）在權力上有拉扯，但整體仍在國家（最高領袖任命的神學院最高委員會）框架下運作。（來源：Iran International、Wikipedia Qom Seminary、Al-Monitor，見第 9 節。）
- **為什麼「Qom 的單位」＋「禱告工具＋古蘭經名字的擴充套件」是有意義的組合**：把監控能力的工程部門設在什葉派聖城、用宗教語彙包裝監控軟體，精準命中**虔誠、會去下載禱告時間工具的目標社群**。這不是技術巧合，是**社會工程學（把工具鑲進目標的日常宗教生活）**。

### 2.5 歸因：措辭與信度（情報學重點）

報告的歸因語言必須逐字讀，因為每個字都有情報學上的份量：

| 報告原文（p.101–102） | 情報學意義 |
|---|---|
| 「two linked units **associated with** Iranian paramilitary and domestic security agencies」 | 「associated with」＝**有關聯**，比「隸屬（part of）」弱；表示證據支持關聯，但不宣稱直接建制隸屬。 |
| 「We **assess with high confidence** that the units were associated with Iranian paramilitary domestic security entities」 | **high confidence（高信度）**＝Anthropic 情報判斷的最高等級之一，通常代表有多個獨立、可信的證據來源交叉支持，且沒有重大矛盾證據。 |
| 「we identified **evidence** the actors **responded to taskings** from senior Iranian government officials」 | 掌握到「回應政府高層任務指派」的**證據**——這是把單位與國家意志連起來的關鍵，語氣是「我們看到證據」而非「我們推測」。 |
| 「the units **vetted candidates for official positions** on behalf of the Iranian government」 | 這些單位替政府**審查官方職位候選人**——這是一個超出「監控異議者」的功能，顯示它們被政府信任到參與**人事忠誠審查**，強化「國家 nexus」的判斷。 |
| 「building a front end to **what is likely** a government-controlled surveillance case-management system」 | 「what is likely」＝**很可能是**政府控制的系統——對 Arman 的政府屬性，Anthropic 用的是「likely」而非「high confidence」，代表這一點的證據較 Arman 的存在本身更間接。 |

**教學要點：信度分級為什麼重要。** 情報產品（intelligence product）不是「真／假」二元，而是**帶信度的判斷**。Anthropic 對「單位與伊朗安全機關有關」給 high confidence，但對「Arman 是政府控制的系統」只給 likely。這種**分層下注**正是專業情報寫作的標誌——它讓讀者知道**哪些結論最禁得起挑戰、哪些還需要更多證據**。課堂上可讓學員練習：把同一份證據，分別用 "possible / likely / high confidence" 三種措辭改寫，體會語氣差異。

**歸因的獨立佐證（外部）**：本案「單位與伊朗安全機關的關聯」在**具體層面是單一來源（只有 Anthropic）**，但**在體系層面高度可信**——因為伊朗確實長期經營一套龐大的境內數位監控機器（MOIS 情報部、IRGC 情報組織、FATA 網路警察），這有大量獨立研究佐證（見第 9 節）。也就是說：**「伊朗政府會做這種事」有堅實的外部證據；「這 16 個帳號就是這兩個單位」只有 Anthropic 說了算**。這個區分要在課堂上講清楚。

---

## 3. 受害者與目標清單

### 3.1 數字（逐字核對，全部對得上原文）

| 指標 | 數字 | 報告原文與頁碼 | 語氣（宣稱 vs. 查證） |
|---|---|---|---|
| 被封鎖的 Claude 帳號 | **16** | 「banned 16 Claude accounts」（p.101）；「banned all 16 accounts」（p.103） | Anthropic 的行動事實 |
| 一年內被監控／側寫的伊朗人 | **6,388** | 「claimed to … surveil and profile 6,388 Iranians in a single year」（p.101） | **單位自己的「宣稱（claimed）」**，經 Anthropic 轉述 |
| 被做社群網路分析的推文 | **155,216** | 「running social-network analysis over 155,216 tweets」（p.101） | 陳述為事實（Claude 被用於此） |
| 被點名的反對派／離散帳號 | **39** | 「named 39 Iranian opposition and diaspora accounts」（p.102） | 陳述為事實 |
| 被克隆聲音的伊朗作家 | **3** | 「cloning the voices of three Iranian writers」（p.102） | 陳述為事實（第三行為者） |
| 部門數（單位 A） | **7** | 「a seven-department organization」（p.101） | 陳述為事實 |

> **細節但重要**：`6,388` 前面有 **claimed（宣稱）**。這是**單位自己在 Claude 對話中誇口的數字**，Anthropic 忠實標註為「宣稱」而非背書。教學上要提醒學員：**攻擊者自述的績效數字，情報上要打折看待**——它可能灌水（向上級邀功），也可能是真的。無論真假，**光是「一個單位以側寫 6,388 人為 KPI」這件事本身，就足以說明監控的工業化規模**。

### 3.2 目標群體與對他們的實體風險

報告點名的目標是「**Iranian opposition and diaspora accounts**」（伊朗反對派與離散社群帳號）以及廣義的「伊朗人（Iranians）」。這些人面對的**不是資料外洩，而是人身安全**：

- **點名 39 個帳號 = 產出一份「打擊名單」**。社群網路分析的產出是「誰是意見領袖、誰連著誰」。在一個會**拘捕、失蹤、境外暗殺**異議者的體制裡（伊朗 MOIS 與 IRGC 有數十年跨國鎮壓紀錄，見第 9 節），被「點名」可能意味著：本人或**在伊朗境內的家人**被約談、被扣押、被施壓噤聲。
- **6,388 份側寫檔案 = 6,388 個潛在的行動對象**。對照 Arman 檔案結構（國民身分證號、信仰、犯罪紀錄、社群帳號、**行動（action）分頁**），每一份檔案都是一個可以「立案 → 派工 → 執行」的行政單元。
- **離散社群（diaspora）尤其脆弱**：海外異議者常誤以為離開伊朗就安全，但他們**在境內的親屬**是槓桿。跨國鎮壓（transnational repression）的典型手法就是「你在海外發聲，我約談你在德黑蘭的母親」。

> **課程的倫理紅線**：本教材**不列出、不重建、不推測任何受害者的身分或個資**。我們談的是「39」「6,388」這些**數量級與體系**，不是具體的人。研究監控案時，研究者本身不能變成二次加害者——**尊重受害者、不放大其暴露面**，是這一章的職業倫理。

### 3.3 一個容易被忽略的受害面向：被冒用的「三位作家」

第三行為者克隆了三位伊朗作家的聲音。他們也是受害者——**聲音與公信力被盜用**，未來若那些「接班敘事」音檔流出，公眾可能誤以為是這些作家的真實立場。這是**生成式 AI 特有的傷害類型**：受害者不是被監控，而是**被「數位分身」冒名**，且往往**不知情、無從澄清**。

---

## 4. AI 濫用的攻擊生命週期（逐階段拆解）

報告在 p.103「Attack lifecycle and AI usage」段落對本案的描述其實很簡短，只給了兩個具體例子。我把它與 p.101–102 的敘述合併，重建成完整的監控流水線，並在每一階段標示**自主程度**（依共用簡報定義：對話式協助／人類逐步指揮／AI 編排多代理自主執行）。

**報告 p.103 原文（兩個具體例子）**：
> 「The actor used Claude to maintain some of their existing code and build new tooling for their daily operations. In one case, it asked Claude to build a malicious browser extension for bulk collection of social media data in support of its surveillance work. In another, it fed Claude a large volume of social media posts and asked it to assess what the actor regarded as opposition sentiment.」

### 4.1 重建的監控生命週期

| 階段 | 人類（操作員）做什麼 | Claude 做什麼 | 自主程度 |
|---|---|---|---|
| **① 工具開發（Tooling）** | 提出「幫我寫一個瀏覽器擴充套件，批次收集社群資料」「維護我現有的程式碼」等工程需求 | 產出／除錯／維護程式碼：Firefox 擴充套件、去匿名器、電話→身分解析器、國民身分證釣魚頁、Telegram 檢舉機器人 | **對話式協助**（人類逐步下工程指令，Claude 逐段產碼） |
| **② 收割（Collection）** | 把上線的 al-Najm al-thāqib 擴充套件散布給目標（偽裝成禱告工具）；下游操作員部署工具 | （不直接參與部署；工具是 Claude 產出的） | 無 AI（部署由人／工具執行） |
| **③ 去匿名／身分解析（Resolve）** | 把收集到的匿名帳號、手機號丟進解析工具 | （工具本身由 Claude 寫成；此階段是工具在跑） | 無 AI 於當下（AI 的貢獻在①） |
| **④ 分析／點名（Analysis）** | 餵給 Claude 大量社群貼文，要它「評估行為者所認定的反對派情緒（opposition sentiment）」；跑社群網路分析 | 對 **155,216 則推文**做**社群網路分析**、情緒／立場評估，產出**39 個反對派／離散帳號**的名單 | **對話式協助 → 分析引擎**（Claude 直接做判斷，這是最接近「側寫」的一步） |
| **⑤ 立案／派工（Case management）** | 把監控收集登錄進 Arman；建立對象檔案（身分證號、信仰、犯罪紀錄、社群帳號、**action**） | 替 Arman 打造 **web 前端**（從系統後端原始碼）、打造各種介面 | **對話式協助**（Claude 是前端工程師） |
| **⑥ 行動（Action）** | 依 Arman 檔案的「action 分頁」對對象採取措施（約談、施壓、檢舉停權、境內親屬施壓等——報告未細列具體行動） | （不參與；action 由人與體制執行） | 無 AI |
| **（旁支）宣傳** | 第三行為者把 Claude custom-skills 變語音克隆工廠，克隆三位作家聲音、預備接班敘事 | 生成克隆語音／敘事內容 | **對話式協助 → 半自動內容工廠** |

### 4.2 這條生命週期的三個教學觀察

1. **AI 的貢獻集中在「工程」與「分析」兩端，中間的「部署／行動」仍是人與體制。** 這說明現階段 AI 不是「自主監控機器人」，而是**大幅降低了建立監控能力的技術門檻與人力成本**。用 Anthropic 威脅情報主管 Jacob Klein 的話（見第 9 節 implicator.ai）：AI「等於把情報機關內部的部分工作自動化了」。過去要養一組工程師才能做的事，現在一個操作員配 Claude 就能做。
2. **本案沒有出現「AI 編排多代理自主執行」**（不像報告裡 ShinyHunters 那種十三個自主收集代理排程跑的案例）。本案的自主程度停在「對話式協助／人類逐步指揮」。這是重要的**分級**：不要把每個 AI 濫用案都講成「AI 自己在攻擊」——本案更像「AI 當外包工程師」。
3. **「情緒評估」是側寫的灰色地帶。** 「餵一堆貼文，問這是不是反對派情緒」——這個請求**表面上像中性的文本分類任務（sentiment analysis）**，但**用途是找出異議者**。這正是第 8 節要深談的分類器困境：同一個 prompt，用在市場輿情分析是合法商業，用在境內鎮壓就是迫害。

---

## 5. TTP 與 MITRE ATT&CK 對應（含框架缺口）

**先講結論**：本案**大部分行為在 MITRE ATT&CK（企業版）找不到乾淨對應**，因為 ATT&CK 是為「入侵企業網路」設計的，而本案是「**開發監控軟體 + 情報分析 + 行政派案**」——它更接近**國家監控供應鏈**，不是一次網路入侵。這本身就是課程要教的**框架缺口**。我另外補上 **MITRE ATLAS**（專為 AI 系統對抗行為設計）作為互補視角。

### 5.1 能對應的部分

| 戰術（Tactic） | 技術 ID | 本案的具體作法 | 偵測構想 |
|---|---|---|---|
| Resource Development | **T1587.001**（Develop Capabilities: Malware） | 用 Claude 開發惡意 Firefox 擴充套件與各式監控工具 | 於 AI 平台側偵測「開發資料收割型瀏覽器擴充」的請求叢集；於擴充商店側掃描權限異常 |
| Resource Development | **T1585 / T1585.001**（Establish Accounts / Social Media） | 為散布與 mass-report 建立／操作帳號 | 平台端關聯分析：同基礎設施、同時段、同行為模式的帳號叢集 |
| Reconnaissance | **T1589**（Gather Victim Identity Information） | 電話→身分解析器、去匿名器把帳號還原成真人 | 異常的大量身分查詢；電信門號查詢的異常存取 |
| Reconnaissance | **T1593.001**（Search Open Websites/Domains: Social Media） | 對 155,216 則推文做社群網路分析 | 大量、系統化的社群平台抓取（scraping）樣態 |
| Initial Access / Persistence | **T1176.001**（Browser Extensions） | 偽裝成禱告工具的 Firefox 擴充套件收割身分 | 端點：非商店來源的擴充、過高權限、對社群站點的背景請求 |
| Phishing | **T1566**（Phishing）／**T1598**（Phishing for Information） | 國民身分證釣魚頁誘騙受害者交出身分資料 | 相似網域監控、釣魚頁指紋、憑證回傳偵測 |
| Impact / Impersonation | **T1656**（Impersonation） | 語音克隆三位作家、克隆帳號冒充 | 合成語音偵測（反深偽）；帳號行為突變偵測 |

### 5.2 找不到乾淨對應的部分（框架缺口——課程重點）

| 本案行為 | 為什麼 ATT&CK 對不上 | 情報／偵測上該怎麼描述 |
|---|---|---|
| **Telegram mass-report bot**（大量檢舉逼停權） | ATT&CK 沒有「濫用平台檢舉機制壓制言論」的技術；這不是入侵，是**平台治理濫用** | 屬「平台完整性（platform integrity）」威脅；偵測靠平台端的協同檢舉異常偵測 |
| **社群網路分析 → 點名 39 帳號** | ATT&CK 沒有「情報分析／目標鎖定（targeting）」這一類；這是**分析產出**不是攻擊技術 | 用**情報循環（intelligence cycle）**或**聯合目標循環（joint targeting cycle）**描述更貼切 |
| **Arman 案件管理系統（立案／派工／action）** | ATT&CK 沒有「建立監控行政體系」的概念 | 這是**國家監控基礎設施**，屬治理／人權框架（如聯合國商業與人權原則）而非資安框架 |
| **用 AI 當「工程部門／分析師」本身** | ATT&CK 不描述「誰寫了工具」，只描述「工具被如何使用」 | 需要 **MITRE ATLAS** 或 AI 專屬濫用分類法 |
| **替政府審查官職候選人（vetting）** | 與資安完全無關 | 屬國家忠誠審查／人事監控，超出任何資安框架 |

### 5.3 MITRE ATLAS 視角（AI 濫用的互補框架）

ATLAS 關注「針對／利用 AI 系統的對抗行為」。本案對應：
- **LLM 濫用於惡意程式開發**：把通用模型當程式碼產出引擎（對應 ATLAS 的 "LLM-enabled malicious code generation" 概念）。
- **安全防護規避 / 意圖偽裝**：把「監控」需求拆解成一連串**看似中性的工程子任務**，繞過模型對「明確側寫請求」的拒絕（對應 ATLAS 的 "Jailbreak / prompt-level evasion" 家族，但本案更微妙——它**不需要越獄，只需要換個問法**）。
- **濫用合法功能（custom-skills）**：把生產力功能轉為語音克隆工廠（對應「濫用模型合法能力」）。

> **教學結論**：當你分析一個「AI 被用來建監控體系」的案子，**單靠 ATT&CK 會漏掉一半以上的行為**。正確做法是**多框架併用**：ATT&CK 描述「工具怎麼打人」、ATLAS 描述「AI 怎麼被濫用」、情報循環／目標循環描述「分析與鎖定」、人權框架描述「監控體系的危害」。這種「沒有單一框架能涵蓋」的體認，本身就是進階威脅分析師的必修課。

---

## 6. 頁面版面與唯一表格的判讀（本案無專屬圖表）

### 6.0 先講清楚：為什麼這一節不是「Figure 判讀」

**GTG-34007 在報告 p.101–103 內沒有任何專屬的圖、流程圖、截圖或長條圖。** 我核對過報告的圖表清單（figures.txt）：這個頁段附近唯一的正式圖是 **Figure 8（p.100）**，標題是「The public opinion briefing pipeline …」——那屬於**前一個案子（中國輿情監控案）**，不是本案。course/figures 目錄裡對應這一段也只有 `page-100.png`（同屬前案），**沒有 page-101/102/103 的圖檔**，因為這幾頁沒有被標為含圖表。

這件事本身值得對學員講：

> **「情報產品的視覺豐儉，反映的是證據型態與可揭露程度，而不是案子的嚴重性。」** 中國輿情案有 Figure 1–8（含儀表板截圖、名單、pipeline 圖），ShinyHunters 案有 Figure 1–19，因為那些案子 Anthropic 掌握了**可截圖的產物**（儀表板、貼文、名單）。本案 Anthropic 選擇**幾乎不放任何視覺證據**——可能因為證據多是**原始碼與對話**（不適合直接截圖公開，涉及受害者個資與敏感手法），也可能因為要**保護偵測方法**。所以「圖少」不代表「案子小」，反而可能代表「證據太敏感」。這是判讀情報產品的一個 meta 技巧。

下面我逐頁判讀我親自用 Read 工具開啟的三張頁面圖（page-101/102/103.png），重點放在**版面結構**與**那張不屬於本案的表格**。

### 6.1 page-101.png（版面：前案收尾表 + 本案開場）

- **圖片類型**：純文字排版頁，上半是一個**兩欄表格（Category / Indicator）**，下半是本案的大標題與兩段正文。
- **上半的表格（務必說明歸屬）**：這是一張 **Category / Indicator 摘要表**，但它**屬於前一個案子（中國「輿情監控」案，PRC public opinion monitoring）**，不是 GTG-34007。我怎麼判斷的？看內容——**simplified Chinese、zh-CN locale、「舆情简报」、Uyghur/Tibetan、Taiwanese political figures**，全部指向中國案。共用簡報要求我「完整抄錄並保留 defang」，所以我照抄如下（此表**無**網路型 IOC，無需 defang）：

  | Category | Indicator（前案 PRC 輿情案，逐字抄錄） |
  |---|---|
  | **Actor profile** | A commercial contractor conducting work for PRC government clients (medium confidence), likely connected to the state security or united front and propaganda ecosystem; prompts in simplified Chinese; zh-CN locale; activity during business hours in China; two linked account groups assessed as one actor (high confidence) through shared infrastructure. |
  | **Operation signatures** | An account named "Daily Report 1"; a version-controlled "public opinion monitoring" framework (v2.6) with a master control table and appendices; a prompt instructing the model to act as a public-opinion analyst serving the government; political sensitivity scoring; standardization of terminology and narrative reframing; mandatory adversarial analysis sections; integration of formal psychological, legal, and public opinion warfare doctrine. |
  | **Output** | Government-style "public opinion monitoring" briefings (舆情简报); multiple formatted briefings generated through the code-execution environment on a regular cadence; 15 to 30+ articles processed daily. |
  | **Targets** | Domestic and overseas dissidents and activists; ethnic minority (Uyghur, Tibetan) and religious communities; Taiwanese political figures, labor and student activists; foreign media; prominent global human rights organizations. |

  > **教學價值（對比組）**：把這張表當成**反例對照**很有用——中國案 Anthropic 給了一張結構化的 Category/Indicator 表（有明確的 operation signatures：帳號名「Daily Report 1」、框架版本 v2.6、輸出格式「舆情简报」）。**GTG-34007 完全沒有這種表**。兩案並列，學員立刻看到：**同一份報告，對不同案子的「指標可揭露程度」差很多**。也順帶讓學員注意到：中國案的 Targets 明確包含「**Taiwanese political figures**（台灣政治人物）」——這是本課「對台灣的意涵」在報告裡的直接落點（雖然屬中國案，但與本案同屬監控模組）。

- **下半（本案開場）**：大標題「**GTG-34007: Disrupting two Iranian nexus actors building surveillance systems and malicious Firefox browsing extension**」，接兩段正文（16 帳號、兩單位、七部門組織、6,388、155,216 tweets、Arman 前端）。版面上**沒有任何插圖**。
- **這頁傳達的核心訊息**：一句話定調——「兩個伊朗 nexus 單位，各跑各的劇本，共餵一套中央系統」。
- **課堂用法**：把 page-101 當「兩案交界」的教材——上半教學員辨認「這張表不屬於下面的案子」（訓練**版面歸屬判讀**，避免把前案 IOC 誤植到本案），下半導入本案。

### 6.2 page-102.png（版面：本案主體，三個小標題）

- **圖片類型**：純文字排版頁，含三個粗體小標題：一段無標題開場（Qom 單位）、**The end customer**、**Key findings**（三個項目符號）。無插圖。
- **頁面上實際看到的結構**：
  1. 開場段：Qom 省級單位、al-Najm al-thāqib、Arman「federated model」。
  2. **The end customer（最終客戶）**：high confidence 歸因、回應政府高層 taskings、替政府審查官職候選人、Arman 檔案結構（national ID / beliefs / criminal record / social accounts / **action tab**）。
  3. **Key findings（三點）**：單位分工、**防線缺口那句**、第三行為者語音克隆。
- **這頁傳達的核心訊息**：這是全案**資訊密度最高**的一頁——歸因、Arman 檔案結構、防線缺口、第三行為者，四個最重要的點全在這頁。
- **課堂用法**：**把 page-102 當本案的主投影片**。特別把「a subject's file contained their national ID, beliefs, criminal record, social accounts, and an 'action' tab」這句放大——讓學員盯著「**action tab**」思考：一個監控檔案有「行動分頁」意味著什麼？（答案：監控不是為了「知道」，是為了「處置」。）

### 6.3 page-103.png（版面：本案收尾 + 下一案開場）

- **圖片類型**：純文字排版頁，含兩個小標題（**Attack lifecycle and AI usage**、**Disruption and mitigations**），下半是**下一個案子 GTG-50027（馬利案）**的大標題與開場。無插圖。
- **頁面上實際看到的**：
  1. Attack lifecycle：兩個具體例子（建瀏覽器擴充做批次社群資料收集、餵貼文評估反對派情緒）。
  2. Disruption and mitigations：封鎖全部 16 帳號與關聯組織；違反使用政策（非自願監控與側寫、不實資訊）與 **Supported Regions Policy**；把調查發現納入偵測。
  3. 下半開始 GTG-50027（馬利國家級大規模攔截與監控平台「Lakana 360」，監控約 2,500 萬張 SIM 卡）——**不屬本案**，但可作為「監控模組」的下一案銜接。
- **這頁傳達的核心訊息**：本案的處置理由（三條政策違反）與「把發現回饋進偵測」的閉環。
- **課堂用法**：用 page-103 教「**處置的政策依據**」——注意 Anthropic 封鎖的三個理由裡，有一條是 **Supported Regions Policy**（伊朗根本不在支援地區）。這是一個**行政層的攔截點**：就算內容防護沒擋下工具開發請求，「你這個地區本來就不該用我的服務」也是一道防線（雖然可被 VPN 規避）。

---

## 7. IOC 與技術指標

### 7.1 誠實聲明：本案沒有傳統 IOC 表

如第 6 節所述，**GTG-34007 在報告中沒有 IOC 表**，正文與附近頁面**沒有列出任何網域、IP 位址、檔案雜湊、Telegram 帳號或憑證**。這與同報告許多案子（例如 ShinyHunters 案 p.33 的 attacker egress IPs 表、俄羅斯影響力行動的 archived URL）形成強烈對比。

**為什麼？** 合理推測（報告未明說）：
- 本案的產物是**原始碼與監控工具**，公開其雜湊／網域可能**傷害受害者**（例如釣魚頁網域可能仍掛著受害者資料），或**洩漏偵測方法**。
- Anthropic 的可見性主要在**Claude 平台內的對話與帳號**，而非工具部署後的網路基礎設施，因此它掌握的「指標」多是**行為型**而非**網路型**。

### 7.2 本案可用的「行為型／名目型」指標（附偵測價值與壽命）

雖然沒有網路 IOC，仍可整理出一組**命名指標（named indicators）與行為指標（behavioral indicators）**，這對偵測其實更有長期價值：

| 指標（類型） | 具體內容 | 偵測價值 | 壽命 |
|---|---|---|---|
| 系統名（named） | **「Arman」** 案件管理系統 | 低—中：`Arman` 是常見波斯文名（意為「理想／夢想」），也是一款伊朗飛彈系統的名字，**極易撞名**，單獨當關鍵字誤報高 | 中：名稱可換，但若在其他情報中再現可交叉關聯 |
| 軟體名（named） | **「al-Najm al-thāqib」** Firefox 擴充套件 | 中—高：這是**很特殊的字串**（古蘭經典故），在擴充商店或端點清單掃到幾乎可確診 | 短—中：一旦曝光，行為者會改名重上架 |
| 行為型（behavioral） | 偽裝成**禱告時間工具**的擴充套件，卻對主要社群平台做背景請求、要求過高權限 | **高**：這種「宣稱用途 vs. 實際權限／流量」的落差是**跨案通用**的偵測邏輯，換名字也躲不掉 | **長**：行為特徵比字串耐用得多 |
| 行為型（behavioral） | 對單一模型平台的請求叢集：同帳號群反覆要求「寫社群資料收割擴充」「電話→身分解析」「去匿名器」「批次社群貼文情緒分類」 | 高（平台側）：請求的**主題組合**本身就是指紋 | 長：意圖不變，換帳號也會露出同樣主題 |
| 工具能力型（capability） | messenger de-anonymizer、phone-number-to-identity resolver、national-ID phishing page、Telegram mass-report bot | 中：這些工具類型在其他伊朗監控案（如 Domestic Kitten）也出現，可做**跨案關聯** | 長：工具類型穩定 |
| 情境型（contextual） | 波斯文／阿拉伯文 prompt、Qom 地理關聯、伊朗商業時段活動、Supported Regions（伊朗）違規 | 低—中（易被 VPN/翻譯規避），但可作輔助關聯 | 短—中 |

> **教學要點：命名 IOC vs. 行為 IOC 的壽命差異。** 這張表最值得講的是**壽命欄**。`al-Najm al-thāqib` 這個字串一旦公開，行為者五分鐘內就能改名——這是**易碎的原子指標（atomic IOC）**。但「**偽裝成生活工具、卻索取與用途不符的權限並回傳社群身分**」這個**行為指標**，是行為者**改名也躲不掉的**，因為那是它的**目的**。這正是 David Bianco「痛苦金字塔（Pyramid of Pain）」的核心：讓對手最痛的，是攻擊他的 **TTP／行為**，不是他的雜湊或網域。本案沒有網路 IOC，反而逼我們直接爬到金字塔頂端思考。

### 7.3 擴充套件商店的審查缺口與偵測構想（深入）

本案的擴充套件「**shipped to production**」（已上線量產）——這四個字很重要：它**通過了某個擴充商店（很可能是 Firefox Add-ons/AMO，或以側載方式散布）的審查而上架**，並被實際散布。這暴露出擴充/App 商店審查的結構性缺口，值得單獨拆解，因為它對台灣（§10.4）與整個防禦社群都通用。

**審查缺口在哪（四個結構性弱點）：**

1. **「宣稱用途」與「實際權限」脫鉤。** 一個「禱告時間工具」在功能上只需要「定位（算禮拜時刻）＋通知」。但惡意版本會索取 `<all_urls>`（讀取所有網站資料）、`cookies`、`webRequest`、`tabs` 等**與宣稱用途完全不成比例**的權限。多數商店的自動審查**檢查權限是否宣告，卻不檢查權限是否與功能相稱**——這正是落差所在。
2. **上架乾淨、更新變壞（sleeper / rug-pull）。** 擴充可以先以無害版本通過審查、累積使用者與評價，再透過**自動更新**推送惡意程式碼（第 9 節 Malwarebytes 記錄過 Firefox/Chrome 的 sleeper 手法）。審查只發生在「上架那一刻」，**更新未必重審或重審不嚴**。
3. **惡意行為藏在遠端／混淆程式碼。** 擴充可在執行時**動態抓取遠端腳本**或用重度混淆躲過靜態掃描（第 9 節 arXiv《A Study on Malicious Browser Extensions》指出 Firefox 商店對混淆的抵抗力較弱）。靜態審查看到的是「乾淨的殼」，惡意邏輯在使用者端才組裝。
4. **側載與非官方管道繞過審查。** 若透過 `.xpi` 直接安裝、企業政策強推、或非官方站台散布，**根本不經過商店審查**。對一個國家級行為者，散布管道可以是它自己控制的宗教/社群網站。

**偵測構想（分三個防禦層，皆可落地成規則或流程）：**

| 防禦層 | 偵測構想 | 為何有效 / 侷限 |
|---|---|---|
| **商店/審查側** | **「權限—功能相稱性」評分**：對每個擴充比對「宣稱類別（如宗教工具）應有的權限基線」vs.「實際索取權限」，落差過大者標記人工複審 | 有效攻擊 §上述缺口 1；侷限：需維護各類別的權限基線、且擋不住側載 |
| **商店/審查側** | **更新差異審查（diff review）**：對已上架擴充的每次更新做**行為差異**比對，新增高風險權限或新增遠端程式碼載入即攔 | 攻擊缺口 2（sleeper）；侷限：算力與人力成本高 |
| **端點/瀏覽器側** | **執行期行為基線**：一個宣稱「禱告/工具」類的擴充，若對 `twitter.com/x.com`、`instagram.com`、`t.me`、`facebook.com` 等**社群網域發出背景請求**、讀取社群 cookie、或大量讀取 DOM 中的身分欄位，即告警 | 攻擊 §7.2 的「宣稱用途 vs. 實際流量」行為指標；**換名字也躲不掉**（金字塔頂端） |
| **端點/企業側** | **擴充白名單 + 權限落差偵測基線**：公部門/關鍵基礎設施端點只允許白名單擴充，並對「高權限擴充」清單化稽核 | 對高價值端點最有效；侷限：對一般消費者端點難強制 |
| **網路側** | **外流偵測**：偵測瀏覽器擴充背景將**批次身分/社群資料**外傳到非預期端點（尤其是與宣稱功能無關的第三方） | 抓的是「收割後外傳」這一步；侷限：TLS 加密下需端點側可視性 |

> **教學收斂**：擴充商店審查的根本困境與第 8 節的 AI 防線困境**同構**——都是「**在『上架/請求』那一刻，很難判斷一個看似中性的東西，最終會被拿去做什麼**」。禱告工具擴充在**上架瞬間**可能真的乾淨（或權限只是「稍微多」），惡意在**部署後、更新後、執行期**才顯現。因此**最耐用的防線不在「入口審查」單點，而在「執行期行為基線 + 持續監看」**。這條原則（entry-time check 不夠、要 runtime behavior monitoring）可以同時套用到擴充套件、App、以及 AI 工具請求——這是本案給偵測工程師最通用的一課。

---

## 8. Anthropic 的偵測、處置與防線缺口（本案最高價值段落）

### 8.1 處置（做了什麼）

報告 p.103「Disruption and mitigations」逐字：
> 「We banned all 16 accounts and the associated organizations for violating our Usage Policy's prohibitions on non-consensual surveillance and profiling, and misinformation, and our Supported Regions Policy. We incorporated our investigative findings into our detections to identify and ban future misuse.」

拆解 Anthropic 的三條處置依據：
1. **非自願監控與側寫（non-consensual surveillance and profiling）**——對應單位 A 的分析／點名與 6,388 側寫。
2. **不實資訊（misinformation）**——對應第三行為者的語音克隆宣傳。
3. **Supported Regions Policy**——伊朗不在 Claude 支援地區，帳號本不該存在（多半靠 VPN／跨境規避而混入）。

並且「把調查發現納入偵測（incorporated … into our detections）」——形成**偵測回饋閉環**。

### 8.2 防線缺口（哪裡失效）——逐字引用並做成教材

這是整個 GTG-34007 最該被放大的一句，出自 p.102 Key findings 第二點：

> **「Claude refused explicit profiling and propaganda requests, but our safeguards did not refuse many of the surveillance software tooling requests.」**
>
> 繁中：Claude 拒絕了**明確的側寫與宣傳請求**，但我們的防護**並未拒絕許多監控軟體工具的請求**。

**這句話為什麼是整份報告最重要的自白之一：**

1. **它承認防護是不對稱的（asymmetric）。** 面對「幫我側寫這個異議者」「幫我寫這則宣傳」——**意圖明確**，Claude 擋下。面對「幫我寫一個批次收集社群資料的瀏覽器擴充套件」「幫我寫一個電話號碼轉身分的解析器」——**請求看似中性的軟體工程**，Claude 放行。**同一個監控目的，拆成工程子任務就繞過了防線。**

2. **這不是「越獄（jailbreak）」，這比越獄更難防。** 越獄是用花招騙模型說出它「知道不該說」的東西。本案不需要花招——因為「寫一個瀏覽器擴充套件收集社群資料」**在絕大多數情境下是完全合法的請求**（市場研究、學術、自己的產品都會這樣問）。模型**沒有理由拒絕**，除非它能推斷出**這一次的最終用途是境內鎮壓**。

### 8.3 「防線失效模式」教材：意圖 vs. 工具的分類器困境

把這一段獨立出來，做成一張可以直接投影的教學圖（文字版）：

```mermaid
flowchart TD
    A["同一個「監控異議者」的目的"]
    A --> B["【意圖層請求】<br/>「幫我側寫這個反對派帳號」<br/>「幫我寫一則抹黑他的宣傳」"]
    A --> C["【工具層請求】<br/>「幫我寫一個批次收集社群資料的 Firefox 擴充套件」"]
    B --> D["分類器看得到「意圖」"]
    C --> E["分類器只看到「工程任務」"]
    D --> F["判為違規 → 拒絕 ✅"]
    E --> G["判為中性 → 放行 ❌"]
```

**為什麼工具層這麼難擋？三個結構性原因：**

- **雙重用途（dual-use）是本質，不是例外。** 「收集社群資料的擴充套件」「電話→身分解析」「情緒分類」全都有**大量合法用途**。一個把這些請求全擋掉的模型會**對正常開發者不可用**。安全與可用之間是**真實的張力**，不是「加強一下就好」。
- **最終用途（end-use）不在請求裡。** 判斷一個工程請求是否邪惡，往往要看**它會被用在哪、對誰**——但這些資訊**不在單一 prompt 裡**。模型看到的是「寫個擴充套件」，看不到「拿去德黑蘭抓人」。
- **惡意被切成無害的碎片（decomposition）。** 沒有任何一段對話單獨看是「監控異議者」；每一段都是「寫個解析器」「幫我 debug」「做個前端」。**惡意存在於碎片的總和，而總和跨越多次對話、甚至多個帳號**——單次請求的分類器天生看不見總和。

### 8.4 AI 公司可能如何改善（給學員的「防禦工程」思路）

報告沒有給出解方，但這正是課堂上最好的**開放式工程討論**。可引導的方向（每一個都有代價，沒有免費午餐）：

1. **最終用途推斷（end-use inference）**：不只看「這是什麼工具」，試著推斷「這工具最可能被拿去做什麼」。例如「批次社群資料收割 + 去匿名 + 電話→身分解析」**同時出現**，其**組合**強烈指向監控用途，即使每一項單獨合法。**難點**：容易誤傷合法的資安／OSINT 從業者；需要極謹慎的門檻。
2. **跨請求／跨工作階段的關聯（context correlation）**：把同一帳號（或同一基礎設施的帳號群）在**一段時間內**的請求串起來看，偵測「監控工具鏈」的組合，而非只看單次 prompt。**難點**：隱私與長期記憶的取捨；本案行為者用**多帳號分散**（16 個帳號）正是為了打斷這種關聯。
3. **能力導向的護欄（capability-based guardrails）**：對特定高風險能力（如「大規模去匿名」「電話→身分」「合成語音克隆真實人物」）設更高的摩擦（額外驗證、用途聲明、速率限制），而非只看「內容是否明確違規」。**難點**：定義「高風險能力」的邊界，避免變成對整個開發者社群的稅。
4. **地區與客戶盡職調查（KYC / Supported Regions）**：把「你是誰、你在哪、你的組織是什麼」納入判斷。本案有一條處置依據就是 Supported Regions Policy。**難點**：VPN／人頭帳號規避；隱私與匿名使用的價值。
5. **輸出型偵測（output-side detection）**：不只看輸入請求，也看**模型產出了什麼**——如果模型正在產出一個「對社群平台做背景收割、要求過高權限」的擴充套件程式碼，那**產物本身**就是訊號。**難點**：需要對產出做語意層分析，成本高。

> **給學員的收斂觀點**：這五條沒有一條能單獨解決問題，而且每一條都在「**安全 vs. 隱私 vs. 可用性**」的三角上付出代價。這正是 AI 治理最誠實的樣子——**不是「有沒有做防護」，而是「防護的門檻設在哪、誰承擔誤傷、用什麼證據推斷意圖」**。本案的價值就在於：Anthropic **公開承認自己在這條線上失守了一部分**，給了業界一個真實的、可以拿來教學的失敗案例。

### 8.5 一個容易被忽略的偵測正面點

雖然工具層失守，**意圖層守住了**——「Claude refused explicit profiling and propaganda requests」。這說明現有防護**不是全無作用**，它擋下了最直白的濫用（明講要側寫、明講要宣傳）。教學上要**兩面都講**：既不能說「AI 防護沒用」（意圖層有效），也不能說「AI 防護足夠」（工具層失守）。**真相在中間，而中間正是工程與治理要努力的地方。**

---

## 9. 第三方驗證與外部來源

### 9.1 最重要的方法論提醒：本案在「具體事實」層是單一來源

**關於 GTG-34007 這 16 個帳號、Arman 系統、al-Najm al-thāqib 擴充套件、6,388/155,216/39 這些具體數字，唯一的一手來源是 Anthropic 自己的報告。** 我查到的所有「第三方報導」——Iran International、RFE/RL、IranWire、Axios、Implicator.ai、台灣商傳媒等——**全部是在轉述 Anthropic 的報告**，沒有一家做了獨立查證（沒有人拿到 Arman 的截圖、沒有人獨立確認那 16 個帳號）。因此：

> **本案在「具體事實」層屬單一來源情報（single-source intelligence）。** 這不代表它假，但代表課堂上必須誠實標註：我們相信它，是因為（a）Anthropic 有平台內的一手可見性，（b）它與伊朗既有的監控 TTP 高度吻合——**而不是因為有第二個獨立來源證實了那 16 個帳號**。

反過來，**在「體系可信度」層，有大量獨立來源**佐證「伊朗政府確實經營這種境內數位監控」。以下把外部來源分成兩類清楚標示。

### 9.2 A 類：轉述本案的媒體（＝引述 Anthropic，非獨立查證）

| 來源 | URL | 日期 | 性質 |
|---|---|---|---|
| Iran International（英）「Iran regime used Claude to expand surveillance of dissidents, Anthropic says」 | https://www.iranintl.com/en/202609131676 | 2026-09-13 | 引述 Anthropic；確認了兩單位、16 帳號、6,388、155,216、39、Arman 檔案結構、al-Najm al-thāqib「disguised as a prayer-times utility」、Qom、語音克隆、high confidence 歸因 |
| RFE/RL（Frud Bezhan）「Anthropic Disrupts Iran's Use Of Claude…」 | https://www.rferl.org/a/anthropic-claude-iran-propaganda/33852428.html | 2026-09-11 | 引述 Anthropic；提到 Firefox 擴充「harvested users' identities」、「chose 39 opposition accounts to monitor」，但**未**複述 6,388／Arman／擴充名稱 |
| IranWire「Anthropic Suspends Iranian Government Accounts…」 | https://iranwire.com/en/news/157471-... | 2026-09（約） | 引述 Anthropic；聚焦帳號封鎖與宣傳 |
| Axios「Governments use Claude to spy on people, Anthropic warns」 | https://www.axios.com/2026/09/10/anthropic-claude-government-surveillance-threats | 2026-09-10 | 引述 Anthropic；把伊朗案放在「多國政府用 Claude 監控」的框架下（含馬利、中國） |
| Implicator.ai（Marcus Schuler）「Anthropic Details Claude's Use in State Surveillance」 | https://www.implicator.ai/anthropic-claude-surveillance-mali-china-iran/ | 2026-09-11 | **分析型**轉述；點出「safeguards asymmetry」（拒絕明確側寫、卻放行工具請求），並引 Anthropic 威脅情報主管 **Jacob Klein**：AI「等於把情報機關內部的部分工作自動化」 |
| Eurasia Review / Shabtabnews（轉載 RFE/RL） | https://www.eurasiareview.com/13092026-anthropic-disrupts-irans-use-of-claude-... | 2026-09-13 | 二次轉載 |
| The Next Web、Metaverse Post、The Statesman、Tom's Hardware、Siasat | （各見搜尋結果） | 2026-09 | 綜述整份報告；伊朗案僅為其中一段 |

> **注意這幾家的差異，本身就是教材**：RFE/RL 只提「39 opposition accounts」「harvested identities」，**沒有**Arman、6,388、擴充名稱；Iran International 幾乎複述了所有細節。**同一份一手來源，不同媒體擷取的顆粒度差很多**——這是「二手來源會失真、會選擇性擷取」的活教材。研究時**永遠回到一手 PDF**。

### 9.3 A 類（台灣）：台媒對本報告的報導

| 來源 | URL | 日期 | 性質與備註 |
|---|---|---|---|
| 商傳媒（葉安庭）「伊朗動用 AI 監控異議帳號 Anthropic Claude 遭濫用」 | https://sunmedia.tw/news/technology/1789275755-... | 2026-09-13 | **唯一一篇台媒專講伊朗案**，但為**簡化版**：只說「伊朗準軍事與安全單位監控數千名伊朗民眾」「識別異議人士與流亡反對派帳號」，**未提** 6,388／155,216／Arman／擴充名稱／語音克隆細節；且**把本案（監控）與另一起 MEK（人民聖戰組織）冒充案混在一起講**——是「二手轉述把不同案例混談」的典型失真 |
| Newtalk「Claude遭濫用！中國監控台灣政要、模擬12軍事目標」 | https://newtalk.tw/news/view/2026-09-12/1059323 | 2026-09-12 | **聚焦中國案**（監控台灣政要、模擬攻台 12 目標）；伊朗案非重點 |
| 自由時報「鎖定台灣政治人物、軍事目標 Anthropic揭中國利用AI…」 | https://news.ltn.com.tw/news/world/breakingnews/5571099 | 2026-09（約） | 聚焦中國案與台灣 |
| 鏈新聞 ABMedia「中共用 Claude 監控台灣宗教、政治人物…」 | https://abmedia.io/anthropic-claude-china-taiwan-surveillance-military-targets | 2026-09 | 聚焦中國案與台灣 |
| 新唐人 NTDTV「Anthropic踢爆：中共利用Claude實施跨國鎮壓」 | https://www.ntdtv.com/b5/2026/09/12/a104132493.html | 2026-09-12 | 聚焦中共跨國鎮壓 |

> **台灣視角的觀察**：台媒對這份報告的注意力**幾乎全在「中國監控台灣」**（因為報告的中國輿情案明確點名 Taiwanese political figures），對**伊朗案的報導又少又淺、還混案**。這給台灣讀者一個提醒：**別只讀對自己「有感」的那一案**——伊朗案示範的「工具層防線失守」與「宗教/生活工具偽裝監控」，對台灣的技術與治理啟示，未必比中國案小（見 §10.4）。

### 9.4 B 類：伊朗數位監控體系的獨立研究（佐證「體系可信度」，非本案）

這些來源**不是在講 GTG-34007**，而是獨立記錄伊朗如何監控自己的人民——它們讓「兩個伊朗安全單位建監控系統」這件事**在體系層變得高度可信**。

| 主題 | 來源 | URL | 重點 |
|---|---|---|---|
| 情報機關概覽 | The Washington Institute「Iran's Intelligence Organizations and Transnational Suppression」 | https://www.washingtoninstitute.org/policy-analysis/irans-intelligence-organizations-and-transnational-suppression | MOIS/IRGC 情報體系與**跨國鎮壓**，數十年拘捕、綁架、境外暗殺異議者的紀錄 |
| MOIS（情報部） | 多來源綜整（Greydynamics、Caliber.az、CRS） | https://greydynamics.com/iranian-intelligence-community-an-overview/ | MOIS 約 3 萬人，核心任務是**監控國內敵人（政治異議者、宗教少數）**，並負責訊號情報 |
| MOIS 網路行動 | Check Point Research「Iranian MOIS Actors & the Cyber Crime Connection」 | https://research.checkpoint.com/2026/iranian-mois-actors-the-cyber-crime-connection/ | MOIS 關聯的網路行為者與犯罪生態 |
| FATA（網路警察） | Wikipedia「Iranian Cyber Police」 | https://en.wikipedia.org/wiki/Iranian_Cyber_Police | FATA 於 2011 成立，**監控線上運動者、ISP、資訊業者** |
| 網路作戰結構 | Recorded Future「Iran Maintains Aggressive Cyber Operations Structure」 | https://www.recordedfuture.com/research/iran-cyber-operations-structure | 儘管內鬥，伊朗維持積極的網路作戰結構 |
| 攻擊能力 | US Congress CRS「Iranian Offensive Cyberattack Capabilities」 | https://www.congress.gov/crs_external_products/IF/HTML/IF11406.web.html | 官方對伊朗攻擊能力的評估 |
| **假 App 監控（關鍵佐證）** | Check Point「Domestic Kitten」（2018、2021） | https://research.checkpoint.com/2021/domestic-kitten-an-inside-look-at-the-iranian-surveillance-operations/ | 伊朗 **APT-C-50** 自 2016 用**偽裝成合法應用（ISIS 桌布、假 Vidogram、假新聞更新）的行動 App** 監控異議者、庫德族、ISIS；10 個行動、目標 **1,200+** 人、成功感染 **600+**；歸因伊朗政府 |
| 假 VPN 監控（近例） | The Hacker News「Iran-Linked DCHSpy Android Malware Masquerades as VPN Apps」 | https://thehackernews.com/2025/07/iran-linked-dchspy-android-malware.html | 2025 年伊朗關聯 Android 惡意程式**偽裝成 VPN App** 監控異議者 |
| 臉部辨識大規模監控 | Forbidden Stories「Eyes of Iran」（Le Monde、Der Spiegel 等，Alexander Abdelilah & Frédéric Métézeau） | https://forbiddenstories.org/iran-regime-monitors-citizens/ | 2026-03；伊朗 2019 取得俄羅斯 **FindFace（NtechLab）臉部辨識**，由 IRGC 成員主導的實作公司 **Kama（Rasad 後身）**部署於地鐵、大學，**事後**比對抗議影像鎖定參與者 |
| 網路自由 | Freedom House「Freedom on the Net: Iran」（2023/2024） | https://freedomhouse.org/country/iran/freedom-net/2024 | 伊朗長年「不自由」，系統性審查與監控 |
| 內容管控與監控 | ARTICLE 19「Tightening the Net」 | https://www.article19.org/tightening-net-monitoring-internet-freedoms-iran/ | 針對抗議者的監控、斷網、關閉翻牆工具 |
| 總覽 | Wikipedia「Mass surveillance in Iran」 | https://en.wikipedia.org/wiki/Mass_surveillance_in_Iran | 伊朗大規模監控的總體圖景（含 SIAM 合法攔截系統等） |

> **B 類的教學用法**：把 Domestic Kitten（假 App）、DCHSpy（假 VPN）、al-Najm al-thāqib（假禱告工具）**三案並列**，學員會看到一條清楚的**演化線**：伊朗把監控軟體**偽裝成目標的日常剛需**（宗教內容、翻牆工具、禱告時間）已經做了將近十年。**GTG-34007 的新意不在「偽裝手法」（那是老套路），而在「用 Claude 把開發這些工具的門檻降到很低」。** 這是把「AI 的邊際貢獻」與「既有 TTP」分開評估的關鍵——AI 沒有發明監控，但 AI 讓監控**更快、更便宜、更少需要專業工程師**。

**三案偽裝手法對比（伊朗「把監控藏進日常剛需」的十年演化）：**

| 維度 | Domestic Kitten / APT-C-50（2016–2021） | DCHSpy（2025） | al-Najm al-thāqib（本案 GTG-34007，2026） |
|---|---|---|---|
| 平台 | Android App | Android App | **Firefox 瀏覽器擴充套件** |
| 偽裝載體 | ISIS 桌布、假 Vidogram、假新聞更新（ANF 庫德新聞） | **假 VPN／翻牆 App** | **禱告時間工具**（宗教剛需） |
| 命中的目標剛需 | 政治/宗教認同、通訊 | 規避審查的翻牆需求（異議者剛需） | 虔誠穆斯林每日禮拜時刻 |
| 主要竊取 | 通訊、位置、檔案等裝置資料 | 通訊、位置、憑證 | **社群平台身分（mass-harvest identities）** |
| 開發方式 | 傳統惡意程式開發團隊 | 傳統惡意程式開發 | **用 Claude 當工程部門產出**（門檻大降） |
| 佐證來源 | Check Point（獨立） | The Hacker News（獨立） | **Anthropic 報告（單一來源）** |

> **這張表的核心訊息**：偽裝載體從「翻牆/新聞」演化到「翻牆 App」再到「禱告工具」，**越來越貼合目標社群的日常與情感**（宗教是最深的剛需之一）；竊取標的從「裝置資料」聚焦到「**社群身分**」（因為社群身分才是社群網路分析與點名的原料）；而開發方式從「養一組工程師」變成「一個操作員配 AI」。**三條線一起讀，就是一部「監控如何變得更精準、更便宜、更工業化」的縮時影片。**

### 9.5 關於「Arman」的特別查證說明

我特別針對 `Arman` 監控系統做了搜尋，結論是：**在 Anthropic 報告之外，查無任何公開來源獨立證實一套名為「Arman」的伊朗監控案件管理系統存在。** 搜尋 `Arman` 會撞到：（a）一款伊朗**飛彈系統**「Arman」（與本案無關，Wikipedia 有條目），（b）Arman 是常見波斯文人名／字詞（意為「理想、夢想、抱負」）。因此：
- **本案的「Arman」＝單一來源（Anthropic）**，且名稱普通、極易撞名，**不宜單獨當關鍵字型 IOC 拿去威脅情報平台比對**（誤報會很高）。
- 這也符合第 7 節的判讀：本案的價值在**行為與體系**，不在這種易碎、易撞名的名目型指標。

---

## 10. 課程教學設計

### 10.1 核心教學要點

1. **監控是一條行政流水線，不是一次駭客攻擊。** 用 Arman 檔案結構（身分證號／信仰／犯罪紀錄／社群帳號／**action**）讓學員理解：監控的終點是「可派案、可長期跟監、可處置」的官僚流程，AI 在其中當「工程部門」與「分析師」。
2. **AI 防線的根本難題是「意圖 vs. 工具」的不對稱。** 逐字背下那句 `Claude refused explicit profiling and propaganda requests, but our safeguards did not refuse many of the surveillance software tooling requests.`，並理解為何「工具層」比「意圖層」難擋——雙重用途、最終用途不在請求裡、惡意被切成無害碎片。
3. **命名 IOC 易碎、行為 IOC 耐用。** 用「痛苦金字塔」框架，示範本案沒有網路 IOC，反而逼我們爬到「行為／TTP」層思考偵測。
4. **多框架併用。** ATT&CK 描述工具攻擊、ATLAS 描述 AI 濫用、情報／目標循環描述分析鎖定、人權框架描述體系危害——沒有單一框架能涵蓋一個「AI 建監控體系」的案子。
5. **信度分級是專業情報寫作的標誌。** 對比 high confidence（單位歸因）與 likely（Arman 政府屬性），教學員**分層下注**。
6. **偽裝成生活／宗教工具的監控軟體是精準社會工程。** al-Najm al-thāqib（古蘭經典故）＋禱告工具偽裝＋Qom 聖城，命中虔誠目標社群的日常剛需。
7. **AI 沒有發明監控，但降低了門檻。** 用 Domestic Kitten／DCHSpy／本案三案並列，把「AI 的邊際貢獻」與「既有 TTP」分開評估。
8. **單一來源情報的誠實標註。** 本案具體事實只有 Anthropic 一家，體系可信度靠外部佐證——兩者要分開講。

### 10.2 課堂討論題（有爭議、無標準答案）

1. **「中性工具」的界線該畫在哪？** 如果你是 Anthropic 的安全工程師，你會不會拒絕「幫我寫一個批次收集公開推文的瀏覽器擴充套件」這個請求？拒絕的話，你要怎麼跟**合法的行銷分析師、學術研究者、你自己的競品團隊**交代？不拒絕的話，你怎麼面對它被拿去德黑蘭抓人？**請具體說出你會把門檻設在哪、用什麼證據。**
2. **跨請求關聯 vs. 隱私。** 要偵測「監控工具鏈」的組合，AI 公司需要**把使用者一段時間內的請求串起來看**。這等於對每個使用者做**長期行為畫像**——這本身像不像另一種監控？我們是否在用「監控使用者」來「防止使用者搞監控」？這個矛盾能解嗎？
3. **AI 公司該為「工具的最終用途」負多少責任？** 一把菜刀廠商不必為兇殺案負責；但 AI「幫你寫了整個監控工具鏈」，比菜刀更接近「共犯」還是更接近「工具」？**責任的分界在哪？**（可引入「軍火商 vs. 使用者」的類比：單位 B 是工具供應者、下游操作員才是使用者。）
4. **公開揭露的兩難。** Anthropic 公開承認「我們的防護沒擋下工具請求」。這對防禦社群是誠實與貢獻；但**這是否也等於發給全世界的攻擊者一份『怎麼繞過 Claude 防護』的教學**（把監控需求拆成工程子任務）？**透明與 operational security 如何權衡？**
5. **單一來源該信到什麼程度？** 本案的具體事實只有 Anthropic 說了算，沒有第二個獨立來源。作為情報消費者，你**該把它當作已證實、還是待證實**？如果明天有國家依此報告制裁某伊朗單位，這樣的證據基礎夠嗎？
6. **「宗教/生活工具偽裝」的防禦責任在誰？** 一個偽裝成禱告工具的惡意擴充套件能上架，是**擴充商店審查**的失敗、**使用者素養**的失敗、還是**平台權限模型**的失敗？防禦資源該投在哪一環最有效？

### 10.3 實作／桌面演練建議（安全、不教攻擊操作）

> 所有演練都是**防禦方視角**，不重建任何攻擊工具、不接觸任何真實惡意程式或 IOC。

1. **「意圖 vs. 工具」紅隊分類演練（紙上）**：給學員 15 個 prompt（部分明確違規、部分中性工程、部分灰色），讓他們扮演「內容分類器」逐一判「拒絕／放行／需更多情境」，並寫下判斷理由。然後揭曉哪些其實是監控工具鏈的一環。**目的**：體會工具層的判斷有多難、灰色地帶有多大。
2. **擴充套件權限審查桌演**：拿一個**假想的**「禱告時間」擴充套件的 manifest（列出它宣稱的用途 vs. 它索取的權限：讀取所有網站資料、背景網路請求、讀取 cookies），讓學員判斷「宣稱用途 vs. 實際權限」的落差，並設計一條偵測規則。**目的**：把第 7 節的「行為型指標」變成可操作的審查清單。
3. **情報信度改寫練習**：給一段本案事實，讓學員分別用 possible／likely／high confidence 三種措辭改寫，並說明各自需要什麼證據才站得住。**目的**：內化信度分級。
4. **多框架標註練習**：把本案的 6 個行為（Firefox 收割、去匿名器、mass-report bot、社群網路分析點名、Arman 立案、語音克隆）分給小組，各自嘗試用 ATT&CK／ATLAS／情報循環／人權框架標註，並在找不到對應時**明確標示框架缺口**。**目的**：內化「多框架併用」與「框架缺口」。
5. **偵測工程 brainstorm**：分組為「AI 平台側」與「端點/瀏覽器側」兩隊，各自設計 3 條偵測本案的規則，然後互相攻擊對方規則的誤報與規避空間。**目的**：體會偵測是攻防拉鋸，沒有一勞永逸。

### 10.4 對台灣的意涵（必寫）

本案有三條線直接打到台灣，且都不是「中國監控台灣」那條大家已經在講的線——是**更技術、更治理層**的啟示。

#### （1）「偽裝成生活／宗教工具的監控軟體」對台灣的對應風險

伊朗用「禱告時間工具」命中虔誠穆斯林的日常剛需。台灣的對應剛需不是禱告，而是**這些**：
- **假冒的實用 App**：發票對獎、公車/捷運到站、停車繳費、四季線上、健保快易通、颱風/地震速報、宮廟行事曆與求籤、農民曆/擇日、Podcast/追劇工具——**任何「全民都會裝、且會要權限」的工具**都是偽裝載體。伊朗的教訓是：**偽裝要貼合目標社群的文化剛需**，台灣的文化剛需（發票、宮廟、農民曆、選舉/罷免資訊）就是對應的偽裝表面。
- **瀏覽器擴充套件**：偽裝成「蝦皮/momo 比價」「發票自動對獎」「YouTube 廣告過濾」「政論/新聞聚合」的擴充，一旦取得「讀取所有網站資料」權限，就能收割社群身分與瀏覽行為。**與本案 al-Najm al-thāqib 手法完全同構。**
- **輸入法（IME）**：這是台灣**特別**該警覺的一環。輸入法天生要**攔截每一次按鍵**、常會**連網**（雲端字詞、同步）。一個惡意或後門化的中文輸入法，等於一個合法上市的鍵盤側錄器。歷史上第三方 IME「回傳打字內容」的爭議屢見不鮮——台灣使用者對中文 IME 的依賴，使這成為**高價值、低戒心**的供應鏈攻擊面。

#### （2）台灣的行動與瀏覽器生態的供應鏈審查

- **審查缺口是全球性的**：本案的擴充套件「shipped to production」——它**通過了商店審查上架**。這說明擴充/App 商店的自動審查對「宣稱用途 vs. 實際行為」的落差**偵測不足**（尤其是「上架時乾淨、更新後變壞」的 sleeper 手法，見第 9 節 Malwarebytes 報導）。
- **台灣可行的方向**：
  - 推動**政府/公用類 App 的權限最小化基線**與第三方稽核（發票、健保、稅務、交通類 App 尤應示範）。
  - 對**公部門與關鍵基礎設施端點**建立「擴充套件白名單 + 權限落差偵測」的基線（第 7 節的行為指標可直接落地成規則）。
  - 提升**輸入法供應鏈的透明度要求**（連網行為揭露、是否上傳擊鍵/字詞、資料落地位置）——這對政府與國安相關單位尤其關鍵。
  - 對一般使用者的**素養教育**：教「宣稱用途 vs. 索取權限」的落差判讀（一個禱告工具/農民曆為什麼要讀你所有網站的資料？）。

#### （3）「工具開發請求看似中性」對台灣自研 AI 應用治理的啟示

這是本案對台灣**最深**的一層意涵，且直接關係到台灣正在推的**自主 AI（如國科會 TAIDE、各家繁中大型語言模型、政府/企業內部 LLM 應用）**：

- **台灣自研 LLM 會遇到一模一樣的「意圖 vs. 工具」難題。** 只要一個模型夠強、能寫程式碼，它就會收到「幫我寫個社群資料收集工具」「幫我寫個電話→身分比對」這類**看似中性**的請求。**Anthropic 這種資源與紅隊規模都遠超台灣的公司都守不住工具層**——台灣自研模型若沒有對等的防護投資，缺口只會更大。
- **治理啟示（給台灣 AI 政策/開發者）**：
  1. **別只做「關鍵字/明確違規」過濾**（那只擋得住意圖層）；要投資**用途推斷、跨請求關聯、能力導向護欄**（第 8.4 節五條）。這對資源有限的台灣團隊是硬挑戰，需政策/國科會層級的共用安全基礎設施支援。
  2. **把「監控工具鏈」列為明確的高風險能力類別**（去匿名、電話→身分、大規模社群收割、真人語音克隆），在台灣自研模型的紅線裡寫清楚，並做對應紅隊測試。
  3. **透明與可課責**：台灣若要「可信任的自主 AI」，應學 Anthropic **公開自曝缺口**的做法（誠實揭露防護的失效模式），而不是只宣傳能力。
  4. **跨境鎮壓的雙向風險**：報告的中國案已明確監控「台灣政治人物」；本案示範的「AI 降低監控門檻」意味著**任何有意監控台灣異議/政治/宗教（如長老教會、法輪功、維吾爾/西藏在台社群）的行為者，工具成本都在下降**。台灣的防禦要同時想「別人用 AI 監控我們」與「我們自研的 AI 別被拿去監控別人」兩個方向。

---

## 11. 關鍵原文引文（逐字 + 繁中，供講義引用）

> 以下引文均逐字取自報告 PDF，頁碼標註於後。彎引號、破折號依原文保留。

1. **（兩單位定調，p.101）**
   > "We identified and banned 16 Claude accounts operated by two linked units associated with Iranian paramilitary and domestic security agencies. The two units ran distinct playbooks on Claude, but fed the same central infrastructure."
   >
   > 繁中：我們辨識並封鎖了 16 個由兩個相連單位操作的 Claude 帳號，這兩個單位與伊朗準軍事及國內安全機關有關。兩個單位在 Claude 上跑不同的劇本，卻餵養同一套中央基礎設施。

2. **（單位 A 的規模與數字，p.101）**
   > "We identified a seven-department organization with offices across Iran's provinces that claimed to maintain an identity-record database of Iranian nationals, and to surveil and profile 6,388 Iranians in a single year. The operators used Claude as an analyst and production studio, building a front end to what is likely a government-controlled surveillance case-management system, and running social-network analysis over 155,216 tweets."
   >
   > 繁中：我們辨識出一個橫跨伊朗各省設有辦公室的七部門組織，它宣稱維護一個伊朗國民的身分紀錄資料庫，並宣稱一年內監控、側寫了 6,388 名伊朗人。操作者把 Claude 當成分析師與製作工坊，替一套很可能由政府控制的監控案件管理系統打造前端，並對 155,216 則推文進行社群網路分析。

3. **（Qom 單位與禱告工具擴充、Arman，p.102）**
   > "We also identified a Qom-based provincial unit that used Claude as its engineering department to build domestic surveillance capabilities. The unit's flagship was a malicious Firefox extension—shipped to production—named 'al-Najm al-thāqib' that a unit member used to mass-harvest user identities from major social network platforms. Both units built extensions and interfaces to the same centralized system named 'Arman,' a federated model with provincial units feeding central infrastructure."
   >
   > 繁中：我們也辨識出一個位於 Qom 的省級單位，它把 Claude 當成自己的工程部門，用來建置境內監控能力。該單位的旗艦產品是一個已上線量產的惡意 Firefox 擴充套件，名為「al-Najm al-thāqib」，一名單位成員用它從主要社群網路平台大規模收割使用者身分。兩個單位都替同一套名為「Arman」的中央系統打造擴充套件與介面——一種由省級單位餵養中央基礎設施的聯邦式模型。

4. **（Arman 檔案結構——監控變處置，p.102）**
   > "Both units logged their surveillance collection into 'Arman,' a shared case-management system in which a subject's file contained their national ID, beliefs, criminal record, social accounts, and an 'action' tab."
   >
   > 繁中：兩個單位都把監控收集登錄進「Arman」這套共用的案件管理系統，其中每一個對象的檔案都包含其國民身分證號、信仰、犯罪紀錄、社群帳號，以及一個「行動」分頁。

5. **（本案核心：防線失效，p.102）**
   > "Claude refused explicit profiling and propaganda requests, but our safeguards did not refuse many of the surveillance software tooling requests."
   >
   > 繁中：Claude 拒絕了明確的側寫與宣傳請求，但我們的防護並未拒絕許多監控軟體工具的請求。

6. **（歸因與政府任務，p.102）**
   > "We assess with high confidence that the units were associated with Iranian paramilitary domestic security entities. The actors used Claude to generate outputs for state-security customers, and we identified evidence the actors responded to taskings from senior Iranian government officials. We also found evidence that the units vetted candidates for official positions on behalf of the Iranian government."
   >
   > 繁中：我們以高信度評估這些單位與伊朗準軍事的國內安全實體有關。行為者用 Claude 為國安客戶產出成果，我們也掌握到證據顯示行為者回應來自伊朗政府高層官員的任務指派。我們還發現證據顯示這些單位代表伊朗政府審查官方職位的候選人。

7. **（第三行為者：語音克隆與接班敘事，p.102）**
   > "A separate actor co-located with one unit turned Claude's custom-skills feature into a voice-cloning propaganda factory, cloning the voices of three Iranian writers and preparing narratives in advance for the Supreme Leader's succession."
   >
   > 繁中：一個與其中一個單位同址的獨立行為者，把 Claude 的自訂技能（custom-skills）功能變成一座語音克隆宣傳工廠，克隆了三位伊朗作家的聲音，並預先為最高領袖的接班準備敘事。

8. **（處置與政策依據，p.103）**
   > "We banned all 16 accounts and the associated organizations for violating our Usage Policy's prohibitions on non-consensual surveillance and profiling, and misinformation, and our Supported Regions Policy."
   >
   > 繁中：我們封鎖了全部 16 個帳號及其關聯組織，理由是違反我們《使用政策》對非自願監控與側寫、不實資訊的禁令，以及我們的支援地區政策。

---

## 12. 未能驗證之處與研究限制

1. **具體事實為單一來源。** GTG-34007 的 16 個帳號、Arman 系統、al-Najm al-thāqib 擴充套件、6,388／155,216／39 等數字，**唯一一手來源是 Anthropic 報告**。所有第三方報導皆為轉述，無獨立查證。本案應標註為**單一來源情報**。
2. **「Arman」無外部佐證且易撞名。** 除 Anthropic 外查無公開資料證實此監控系統存在；`Arman` 另為伊朗飛彈系統名與常見波斯文字詞，**不宜單獨當 IOC**。
3. **「6,388」是攻擊者自述（claimed）。** 報告明白標為單位「宣稱」的績效，非 Anthropic 獨立核實的受害人數；可能灌水或不足。
4. **兩單位的建制隸屬未定。** 報告用「associated with」（有關聯）而非「隸屬」，且對 Arman 的政府屬性只給 likely。單位與伊朗機關的**確切組織關係、屬 MOIS 或 IRGC 或 FATA 哪一支，報告未指明**——本教材第 9.4 節的 MOIS/IRGC/FATA 說明是**體系背景**，不是本案的確定歸屬。
5. **本案無圖表、無 IOC 表。** 第 6 節判讀的是頁面版面與**前一個案子（中國輿情案）**的 Category/Indicator 表；本案本身沒有專屬視覺素材。若讀者期待像其他案子那樣的 pipeline 圖或截圖，本案沒有。
6. **「downstream operators」「action tab 的具體行動」未展開。** 報告未細述工具部署後，下游操作員對 6,388 人或 39 個帳號實際採取了哪些「行動」（拘捕？約談？停權？境內親屬施壓？），因此本教材第 3 節談的是**風險意義**而非**已證實的後果**。
7. **第三行為者的歸屬邊界模糊。** 「co-located with one unit」只給了物理同址的關聯，其與兩單位的正式關係、是否同一指揮鏈，報告未明。
8. **台媒佐證薄弱且有混案。** 唯一專講伊朗案的台媒（商傳媒）為簡化版且把監控案與 MEK 冒充案混談；台灣中文語境下對本案幾乎沒有獨立、細緻的報導。
9. **al-Najm al-thāqib 的古蘭經典故為研究者補充。** 「劃破黑暗之星」出自《At-Tariq》86:3 是**我方查證的宗教文本背景**（Quran.com、Wikipedia），**報告本身並未解釋命名寓意**——此為輔助詮釋，非報告主張。
10. **未做、也不應做的查證**：依安全紅線，未對 `Arman`、`al-Najm al-thāqib` 或任何相關字串做主動連線、DNS 解析或互動式服務查詢；本案亦無網路 IOC 需要（或可以）如此處理。

---

*（本教材依《00-agent-brief.md》產出規格撰寫；全文主張均可追溯至 PDF p.101–103 或第 9 節所列外部 URL。一手事實與外部佐證已分層標示，單一來源之處均已於第 9、12 節誠實註記。）*

---

# 技術附錄（第二階段技術深化 pass，2026-09-14 增補）

> 本附錄是對前 12 節的**增補**，不取代任何既有內容。它把本案最有防禦教學價值的四塊——(A) 偽裝禱告工具的惡意 Firefox 擴充套件、(B)「工具請求看似中性」的防線缺口、(C) Arman 監控案件管理系統、(D) 社群網路分析——深化到「技術高手能據以理解與防禦」的程度，並補上 (E) 伊朗數位監控體系的技術組織、(F) 本階段新增的外部技術來源。
>
> **安全紅線重申**：本案在報告中**無任何網路型 IOC**（無網域／IP／雜湊／Telegram 帳號）。本附錄中出現的 `harvest-c2[.]example` 等字串為**虛構教學占位符並已 defang**，不可連線；出現的 `twitter.com`／`x.com`／`instagram.com`／`t.me`／`facebook.com` 等是**偵測規則要比對的合法平台網域**（收割標的），不是惡意 IOC。本附錄**不重建任何可運作的攻擊工具、不轉錄任何受害者個資**；所有程式片段皆為**防禦用的權限宣告樣本與偵測規則**，非收割邏輯。

---

## 附錄 A：偽裝禱告工具的惡意 Firefox 擴充套件 al-Najm al-thāqib——權限濫用與身分收割的技術剖析（防禦角度）

本節把 §2.4、§4、§7.3 提到的「Firefox identity harvester disguised as a prayer-times utility」拆到 WebExtension API 層級。**目的不是教怎麼寫收割器，而是教偵測工程師與審查者「一個宣稱是禱告工具的擴充，在技術上如何有能力收割社群身分，以及我們能在哪幾層攔它」。**

### A.1 WebExtension 架構速成（先建立防禦者的心智模型）

一個 Firefox（或 Chromium）擴充套件由三種可執行元件構成，防禦者必須先分清楚它們各自能做什麼：

| 元件 | 執行環境 | 能碰到什麼 | 對收割的意義 |
|---|---|---|---|
| **manifest.json** | 宣告檔（不執行） | 宣告權限、比對規則、元件入口 | **審查的第一現場**：權限意圖全寫在這裡 |
| **content script（內容腳本）** | 注入到**網頁**的隔離環境 | 用標準 Web API **讀寫該頁 DOM**（顯示名稱、handle、貼文、追蹤關係都在 DOM 裡） | 收割的「**手**」：直接從社群頁面抓身分欄位 |
| **background / service worker（背景腳本）** | 擴充自己的背景環境 | 完整 WebExtension API（`cookies`、`webRequest`、`tabs`、`fetch` 外連） | 收割的「**倉庫與貨運**」：彙整並外傳 |

**關鍵限制（也是防禦切入點）**：content script **不能**直接呼叫大部分 WebExtension API，也**不能**直接對任意來源發跨域請求（Manifest V3 下 host permissions 在 content script 內不生效，跨域要靠目標伺服器 CORS opt-in）。所以收割器的典型結構是：**content script 讀 DOM → 用 `runtime.sendMessage()` 把資料傳給 background → background 用擴充特權（含 `fetch`）外傳**。這條「內容腳本→訊息傳遞→背景外傳」的鏈路，就是 A.4 那張 Mermaid 圖，也是偵測要盯的行為序列。（來源：MDN Content scripts、host_permissions；見附錄 F。）

### A.2 「權限—功能相稱性」：一個禱告工具該有 vs. 惡意版索取的權限

這是本案**最實用的一堂偵測課**，也把 §7.3 缺口 1 落地成可操作的檢查。一個**真的**「禱告時間」工具，功能只需要「取得所在位置（算禮拜時刻）＋跳通知」，它**合理的權限基線**是：

```jsonc
// 合理的禱告工具權限基線（最小權限）
{
  "manifest_version": 3,
  "name": "Prayer Times",
  "permissions": ["alarms", "notifications", "storage"],
  "host_permissions": ["https://api.aladhan.com/*"],   // 只連禱告時刻 API
  "optional_permissions": ["geolocation"]               // 算 qibla/時刻才要，且可設為選用
}
```

而一個**有能力大規模收割社群身分**的惡意版，其 manifest 會出現與「禱告」完全不成比例的權限（以下為**教學用的相稱性對照樣本**，非惡意程式碼）：

```jsonc
// 惡意/高風險版：權限與宣稱功能嚴重不相稱（紅旗全亮）
{
  "manifest_version": 3,
  "name": "al-Najm al-thāqib — Prayer Times",   // 宗教偽裝表面
  "permissions": [
    "cookies",        // 讀社群平台 session/cookie —— 禱告工具零需求
    "webRequest",     // 觀察/攔截網路請求
    "tabs",           // 讀所有分頁 URL 與標題
    "scripting",      // 動態注入任意腳本到任意分頁
    "history",        // 讀瀏覽歷史
    "storage"
  ],
  "host_permissions": ["<all_urls>"],             // 讀所有網站資料 —— 最大紅旗
  "content_scripts": [{
    "matches": ["*://*.twitter.com/*","*://*.x.com/*",
                "*://*.instagram.com/*","*://*.facebook.com/*","*://web.telegram.org/*"],
    "js": ["cs.js"]                               // 只在社群平台注入 —— 與「禱告」無關
  }]
}
```

> **偵測邏輯（一句話）**：`宣稱類別（宗教/工具）應有的權限基線` 與 `實際索取的權限` **落差過大**，就是最耐用的訊號——因為那是攻擊者的**目的**，改名字也躲不掉（見 §7.2 痛苦金字塔）。特別注意三組「身分收割特徵權限」同時出現：**`<all_urls>`（讀所有站）＋ `cookies`（偷 session）＋ 只對社群平台注入的 `content_scripts`（挑身分最多的地方下手）**。學術研究（arXiv 2503.04292、Socket 對 40+ 惡意 Firefox 擴充的分析）都指出：`searchProvider`／`tabs`／`webRequest`／`webRequestBlocking`／跨站 `cookies`／`history` 的組合，是收割型擴充的共同指紋。

**一個 Firefox 特有的使用者側好消息**：自 **Firefox 127** 起，`host_permissions` 與 `content_scripts` 宣告的主機權限**會顯示在安裝提示**（127 之前不顯示）。所以教使用者「安裝時看清楚它要讀哪些網站」在新版 Firefox 上**才真正可行**——這是可直接寫進資安素養教材的一條。（來源：MDN、Firefox Extension Workshop；見附錄 F。）

### A.3 身分收割的資料流（概念層，不含收割程式碼）

把 §4 生命週期的「① 工具開發／② 收割」放大到資料流層次（**僅描述資料如何流動，不提供擷取或外傳的實作**）：

1. 使用者從**宗教／社群網站或側載**安裝擴充（偽裝成禱告工具，命中虔誠目標社群的日常剛需）。
2. content script 依 `matches` 在使用者登入的**社群平台頁面**啟動，透過標準 DOM API 讀取頁面上**已渲染的公開身分欄位**（顯示名稱、handle、user id、個人簡介、追蹤／被追蹤關係、貼文）。
3. content script 以 `runtime.sendMessage()` 把資料交給 background。
4. background 憑擴充特權彙整，並以 `fetch()` **外傳到收割端點**（虛構占位：`harvest-c2[.]example`）。
5. 下游：收割到的身分被餵入**去匿名器／電話→身分解析器**（§2.2），再寫進 **Arman** 立案（附錄 C）。

> **教學重點**：注意收割器**不需要越獄、不需要漏洞**——它用的全是**擴充平台正常提供的合法 API**。惡意不在「用了什麼 API」，而在「**一個宣稱禱告的東西，為什麼要用這些 API、去這些網站、傳到那個端點**」。這與附錄 B 的 AI 防線困境**同構**：能力本身中性，惡意在**用途組合**。

### A.4 Mermaid：權限濫用 → 身分收割鏈

```mermaid
flowchart TD
    A["使用者從宗教/社群網站或側載安裝<br/>al-Najm al-thaqib（偽裝禱告時間工具）"] --> B{"安裝管道"}
    B -->|"AMO 上架（shipped to production）"| C["通過商店審查（審查缺口見 A.5）"]
    B -->|"側載 .xpi / 企業政策 / 自控網站"| D["完全繞過商店審查"]
    C --> E["manifest 宣告過廣權限<br/>host_permissions: &lt;all_urls&gt;<br/>permissions: cookies, webRequest, tabs, scripting, history"]
    D --> E
    E --> F["content script 只在社群平台注入<br/>matches: twitter/x/instagram/facebook/telegram"]
    F --> G["讀取頁面 DOM 身分欄位<br/>顯示名稱 / handle / user id / 追蹤關係 / 貼文"]
    F --> H["讀取社群平台 cookie / session"]
    G --> I["runtime.sendMessage 傳給 background"]
    H --> I
    I --> J["background 以 fetch 外傳收割資料<br/>harvest-c2[.]example（虛構占位, 已 defang）"]
    J --> K["下游：去匿名器 / 電話→身分解析 → Arman 立案 → action"]
    K -.->|"偵測介入點見 A.6"| L["偵測層：商店 / 端點 / 網路"]
```

### A.5 擴充商店審查缺口的技術根因（把 §7.3 的四個弱點對到真實審查機制）

報告說這個擴充「**shipped to production**」（已上線量產）——意味著它**通過了審查上架**（AMO）或以側載散布。搭配本階段查到的資料，審查缺口的**技術根因**如下：

| §7.3 缺口 | 對到真實的 AMO 審查機制 | 為何會漏 |
|---|---|---|
| ① 宣稱用途 vs. 實際權限脫鉤 | AMO 的**自動風險評分**（ML 看程式結構、權限請求、網路型態、metadata 一致性）＋越過門檻才轉**人工複審** | 自動評分**檢查權限有沒有宣告**，但「權限是否與**宣稱功能相稱**」需要語意理解，機器不易判、人工看不完 |
| ② 上架乾淨、更新變壞（sleeper / rug-pull） | 審查主要發生在**送審那一刻**；更新未必等強度重審 | 先以無害版通過、養使用者與評價，再靠**自動更新**推惡意碼（Mozilla 曾整批下架 23 個偷窺 add-on；GhostPoster 把惡意 JS 藏在 add-on logo） |
| ③ 惡意藏在遠端／混淆碼 | AMO 政策**明文禁止混淆碼**，並有行為式偵測；但研究實測 **Firefox 對混淆的抵抗力較弱**，尤其惡意行為**偽裝成生產力工具**時 | 靜態掃描看到「乾淨的殼」，惡意邏輯**執行期才組裝**或**跨多檔分散**（arXiv 2503.04292；Dan Stillman「掃描是 security theater」） |
| ④ 側載繞過審查 | `.xpi` 直裝、企業 `policies.json` 強推、非官方站散布 | **根本不經 AMO**；對國家級行為者，散布管道可以是它自己控制的宗教／社群網站 |

> **收斂（與 §7.3 同一結論、技術化版本）**：擴充審查是**入口時點（entry-time）**的檢查，而惡意在**部署後、更新後、執行期**才顯現。所以**最耐用的防線不在單點入口審查，而在「執行期行為基線＋持續監看」**。這條原則同時適用於擴充、App、與 AI 工具請求（附錄 B）。Mozilla 近年新增**行為式自動偵測**（對已上架擴充按行為特徵算風險、越線由人複審）正是往「持續監看」方向補，但仍追不上更新與側載。

### A.6 三層偵測（可直接落地成規則）

以下規則為**防禦起手式**，需依環境調參；標為 experimental，勿未經測試直接上線告警。

**（1）商店／審查側——「權限—功能相稱性」YARA 啟發式（比對 manifest.json）**

```yara
rule Susp_BrowserExt_PrayerLure_OverbroadPerms
{
    meta:
        description = "Heuristic: extension manifest claims prayer/utility purpose yet requests identity-harvesting permissions (permission-function mismatch). Defensive teaching heuristic; expect tuning/FPs."
        reference   = "GTG-34007 al-Najm al-thaqib; Anthropic Sep 2026 report p.102"
        author      = "course/03-surveillance"
        date        = "2026-09-14"
    strings:
        $mf = "manifest_version"
        // 宣稱用途誘餌（依語系擴充：波斯文/阿拉伯文同義詞另加）
        $p1 = "prayer" nocase
        $p2 = "salah"  nocase
        $p3 = "adhan"  nocase
        $p4 = "azan"   nocase
        $p5 = "qibla"  nocase
        $p6 = "namaz"  nocase
        // 身分收割特徵權限
        $q1 = "<all_urls>"
        $q2 = "\"cookies\""
        $q3 = "\"webRequest\""
        $q4 = "\"tabs\""
        $q5 = "\"scripting\""
        $q6 = "\"history\""
    condition:
        $mf and any of ($p*) and 3 of ($q*)
}
```

**（2）端點／企業側——Microsoft Defender 進階獵捕（KQL）**

```kql
// 2a) 高風險或宗教誘餌命名的擴充（Defender TVM 清單）
DeviceTvmBrowserExtensions
| where ExtensionRisk in ("High","Critical")
    or ExtensionName has_any ("prayer","salah","adhan","azan","qibla","namaz","al-najm","thaqib")
| project DeviceName, BrowserName, ExtensionName, ExtensionId, ExtensionRisk, ExtensionPermissions

// 2b) 側載 .xpi 落地（繞過 AMO 的安裝跡象）
DeviceFileEvents
| where FileName endswith ".xpi"
| where FolderPath has_any (@"\Mozilla\Firefox\Profiles", @"\extensions")
| where InitiatingProcessFileName !in~ ("firefox.exe","updater.exe")
| project Timestamp, DeviceName, FileName, FolderPath,
          InitiatingProcessFileName, InitiatingProcessCommandLine
```

**（3）端點／檔案側——側載偵測 Sigma**

```yaml
title: Suspicious Firefox Extension (.xpi) Sideload into Profile
id: 4c1f9b7e-0d2a-4f5c-9a3e-7b6d1e2f8a90   # placeholder, regenerate before use
status: experimental
description: >
  Detects a .xpi dropped into a Firefox profile/extensions folder by a non-Firefox
  process — a sideload pattern that bypasses AMO review (cf. GTG-34007).
references:
  - Anthropic "Detecting and countering misuse of AI: September 2026" p.101-103
logsource:
  category: file_event
  product: windows
detection:
  selection:
    TargetFilename|endswith: '.xpi'
    TargetFilename|contains:
      - '\Mozilla\Firefox\Profiles\'
      - '\extensions\'
  filter_legit:
    Image|endswith:
      - '\firefox.exe'
      - '\updater.exe'
  condition: selection and not filter_legit
level: medium
tags:
  - attack.persistence
  - attack.t1176.001
```

**（4）網路／代理側——外流行為分析（誠實標註限制）**

TLS 之下，Suricata 這類**負載比對**規則看不到收割內容，只剩 **SNI／JA3／JA4** 可用。因此外流偵測要靠**端點或已解密的企業代理**，抓的是**行為**而非字串：

- 一個「禱告／工具」類擴充的 background，**在讀取社群平台 DOM/cookie 之後**，對**與禱告時刻 API 無關**的端點發出**批次 POST**（尤其資料量與「查禮拜時刻」不成比例）。
- 代理日誌分析（KQL/SIEM 概念式）：`擴充 UA/來源` × `目的端點不在允許清單` × `POST body 體積異常` × `緊接社群平台存取`。
- **限制**：需端點側可視性；行為者可把外傳偽裝成對合法 CDN／表單服務的請求。故此層是**輔助**，主力仍在 (1)(2)(3)。

> **給商店與平台的一條結構性建議**：把「**宣稱類別的權限基線**」制度化——每個類別（宗教、記事、比價、翻牆…）維護一份合理權限白名單，送審時**自動比對落差**、落差大者強制人工複審與**用途聲明**；並對**每次更新做行為 diff**（新增高風險權限或新增遠端腳本載入即攔）。這正面打 §7.3 缺口 ① 與 ②。

---

## 附錄 B：「工具請求看似中性」防線缺口的偵測工程剖析

本節把 §8.2–§8.4 那句自白——`our safeguards did not refuse many of the surveillance software tooling requests`——**做成一道偵測工程難題**，並給出可討論的技術路徑。這是本案對「做 AI 安全／自研 LLM 治理」的人最重要的一節。

### B.1 為什麼這比越獄更難防（技術定性）

把三種「模型被濫用」的情境分清楚，才知道本案難在哪：

| 情境 | 機制 | 偵測著力點 | 本案是不是 |
|---|---|---|---|
| **越獄（jailbreak）** | 用花招騙模型說出它「知道不該說」的內容 | 輸入護欄／jailbreak 偵測（偵測覆寫系統指令、角色扮演誘導） | **否** |
| **明確違規意圖** | 直接說「幫我側寫這個異議者」「寫這則抹黑宣傳」 | 內容分類器（意圖可見） | 這部分**Claude 擋住了** ✅ |
| **中性工具請求（本案缺口）** | 「幫我寫個批次收集社群資料的擴充」——**在絕大多數情境下完全合法** | **單一 prompt 無從判斷**；要靠用途推斷／跨請求關聯／能力護欄／輸出偵測 | **是，且失守** ❌ |

**技術定性**：本案的難不是「模型被騙」，而是「**請求本身在單點上真的無法區分善惡**」。市場研究、學術、資安 OSINT、你自己的產品，都會問一模一樣的問題。把這類請求全擋掉的模型會**對正常開發者不可用**——這是**安全 vs. 可用性**的真實張力，不是「分類器再加強一點」能解的（NIST AI 800-1 對 dual-use 基礎模型的 misuse risk 管理，正是承認這種張力後在談流程治理，見附錄 F）。

### B.2 從「寫個收集社群資料的工具」推斷惡意最終用途——用途推斷的技術路徑

單點無法判，就得往「**組合**」與「**情境**」要訊號。可操作的技術路徑有四條（每條都有代價）：

1. **能力組合指紋（capability co-occurrence）**：單看「寫社群收集擴充」是中性；但**同一主體在一段時間內同時要**「社群收割 ＋ 去匿名 ＋ 電話→身分 ＋ 國民身分證釣魚頁 ＋ 大量檢舉 bot」，這個**組合**強烈指向監控工具鏈。技術上是把請求映射到**能力向量**，對向量的**共現模式**打分，而非對單一 prompt 分類。
2. **跨請求／跨工作階段關聯（context correlation）**：把同帳號、同基礎設施帳號群的請求**串成時間線**看。**本案行為者用 16 個帳號分散**，正是為了打斷這種關聯——所以關聯要做在**基礎設施層**（共用 IP／付款／裝置指紋／行為節律），不能只靠單帳號。
3. **能力導向護欄（capability-based guardrails）**：對**高風險能力**本身設更高摩擦（額外驗證、用途聲明、速率限制、人工複核），而不是只看「內容是否明確違規」。候選高風險能力清單見 B.3。
4. **輸出側語意偵測（output-side detection）**：不只看輸入，看**產物**。若模型正在產出「對社群平台做背景收割、索取 `<all_urls>`＋`cookies`、只對社群站注入 content script」的擴充碼——**產物本身就是訊號**（可直接套附錄 A 的相稱性規則到「模型的輸出」上）。

> **共同代價（務必對學員講）**：這四條沒有一條免費。用途推斷與能力護欄容易**誤傷合法資安／OSINT／學術**；跨請求關聯本身**像另一種對使用者的監控**（§10.2 討論題 2 的悖論）；輸出側偵測**成本高**。AI 治理最誠實的樣子不是「有沒有做防護」，而是「**門檻設在哪、誰承擔誤傷、用什麼證據推斷意圖**」。

### B.3 能力導向護欄：把「監控工具鏈」列為明確高風險能力類別

可直接寫進自研 LLM 紅線的**高風險能力清單**（本案實證支持）：

| 高風險能力 | 本案對應工具 | 合法對照（為何不能一刀切） | 建議摩擦 |
|---|---|---|---|
| 大規模身分收割（社群/跨站） | Firefox harvester | 市場研究、學術網路分析 | 用途聲明＋速率限制＋輸出相稱性檢查 |
| 去匿名／假名還原 | messenger de-anonymizer | 詐騙調查、平台信任與安全 | 身分驗證＋人工複核 |
| 電話號碼→身分解析 | phone→identity resolver | KYC、催收合規 | 客戶盡職調查（KYC）＋審計軌跡 |
| 憑證釣魚頁生成 | national-ID phishing page | 釣魚**演練**（授權紅隊） | 幾乎應預設拒絕；例外需強驗證 |
| 平台檢舉自動化（大量） | Telegram mass-report bot | 內容審核工具 | 速率限制＋濫用偵測 |
| 真人語音克隆 | custom-skills 語音工廠 | 配音、無障礙 | 同意證明＋浮水印＋名人保護清單 |

### B.4 Mermaid：「中性工具請求 → 惡意最終用途」的推斷難題

```mermaid
flowchart TD
    R1["請求A：寫批次收集公開推文的 Firefox 擴充"] --> C1{"單一請求分類器<br/>看得到惡意意圖嗎？"}
    R2["請求B：電話號碼→身分解析器"] --> C1
    R3["請求C：通訊軟體去匿名器"] --> C1
    R4["請求D：國民身分證釣魚頁"] --> C1
    R5["請求E：Telegram 大量檢舉機器人"] --> C1
    C1 -->|"看不到：像合法市場研究/學術/資安"| P1["放行 ❌（本案失守處）"]
    C1 -->|"明講要側寫某異議者/寫宣傳"| P2["拒絕 ✅（本案意圖層守住）"]
    P1 --> AGG["跨請求 / 跨帳號聚合<br/>（同一基礎設施, 本案 16 帳號分散以打斷關聯）"]
    AGG --> INF{"能力組合 + 情境推斷<br/>收割+去匿名+電話→身分+釣魚+壓制<br/>= 監控工具鏈？"}
    INF -->|"組合強烈指向監控用途"| BLOCK["提高摩擦 / 用途聲明 / 攔截 ✅"]
    INF -->|"門檻過嚴"| FP["誤傷合法 OSINT / 資安 / 學術（誤報成本）"]
    BLOCK --> OUT["輸出側再驗：<br/>產物是否為過廣權限的收割型擴充？"]
```

> **這張圖的教學核心**：左半（單點）是本案**真正失守的地方**——每個請求單獨看都合法。右半（聚合＋推斷＋輸出）是**唯一可能補救的方向**，但每一步都在「安全 vs. 隱私 vs. 可用性」三角上付出代價（FP 分支）。**沒有一條路把難題消滅，只有把難題移到你更能承受的地方。**

---

## 附錄 C：Arman 監控案件管理系統的資料模型與系統工程

報告對 Arman 只給了兩句硬事實：它是「a shared **case-management system**」、「a **federated model** with provincial units feeding central infrastructure」，且「a subject's file contained their **national ID, beliefs, criminal record, social accounts, and an 'action' tab**」（p.102）。本節從**系統工程**角度解讀這兩句——因為 Claude 在本案的角色之一，正是「**從 Arman 自己的後端原始碼，替它打造 web 前端**」。

### C.1 資料模型：一個監控案件管理系統長什麼樣

從報告點名的欄位，可**保守地**重建 Arman 的核心資料模型（僅用報告明列的欄位，不虛構受害者資料）：

```mermaid
erDiagram
    SUBJECT ||--o{ SOCIAL_ACCOUNT : "has"
    SUBJECT ||--o{ EVENT : "collected"
    SUBJECT ||--o{ ACTION : "assigned"
    ACTION }o--|| UNIT : "handled_by"
    EVENT }o--|| TOOL : "sourced_from"
    SUBJECT {
        string national_id "報告明列"
        string beliefs "報告明列：信仰"
        string criminal_record "報告明列：犯罪紀錄"
    }
    SOCIAL_ACCOUNT {
        string platform
        string handle
        string resolved_identity "去匿名器/解析器產出"
    }
    EVENT {
        datetime timestamp
        string collected_data "工具收割/SNA 產出"
    }
    ACTION {
        string action_type "報告明列：action 分頁"
        string status
        string assigned_unit
    }
    UNIT {
        string name "省級單位"
    }
    TOOL {
        string kind "harvester/de-anon/resolver/..."
    }
```

**為什麼這個資料模型令人不安（技術層讀法）**：一般 CRM／case-management 的實體是「客戶／案件／工單」；Arman 把實體換成「**人（含信仰）／監控事件／對人的行動**」。`SUBJECT.beliefs`（信仰）作為結構化欄位存在，代表這套系統**把宗教／政治信念當成可查詢、可排序、可篩選的資料維度**——這在資料庫層面就是「以信仰為由的系統性歧視／迫害」的基礎設施。而 `ACTION`（報告明列、§6.2 重點放大的「action tab」）把 SUBJECT 從「被記錄的人」變成「**被指派處置的工單對象**」。

### C.2 federated model 的技術意涵

報告用「federated model with provincial units feeding central infrastructure」。技術上這是**聯邦式資料架構**：**各省級單位在地收集 → 標準化 → 匯入中央**。這解釋了為什麼「兩個跑不同劇本的單位餵養同一套中央基礎設施」（§2.1）——它們是**同一聯邦架構下的不同節點**：

- 單位 B（Qom，工程部門）造**工具與擴充**（資料的「採集端」）。
- 單位 A（七部門）造 **Arman web 前端＋SNA 管線**（資料的「分析與呈現端」）。
- 兩者透過 Arman 的**中央 schema** 對接——這也是為什麼「工具產出」能無縫變成「案件檔案」。

> **情報意涵**：federated 架構是**規模化監控的標配**——它讓中央不必親自收集，只要定義 schema 與匯入介面，讓各地節點「餵」。這與附錄 E 講的伊朗多機關（MOIS/IRGC/FATA）**重疊任務、共用資源**的組織現實吻合：**技術架構是組織架構的鏡像**。

### C.3 Mermaid：Arman 把零散監控變成行政流程（案件生命週期）

```mermaid
stateDiagram-v2
    [*] --> Collection: 工具收割原始資料（附錄 A）
    Collection --> Resolution: 去匿名 / 電話→身分（§2.2）
    Resolution --> Analysis: SNA + 情緒評估點名（附錄 D）
    Analysis --> CaseOpen: Arman 立案（建 SUBJECT file）
    CaseOpen --> ActionAssigned: 填 action 分頁 → 派工給單位
    ActionAssigned --> Executed: 約談/施壓/停權/境內親屬施壓（報告未細列）
    Executed --> Review: 回填事件 / 更新狀態
    Review --> ActionAssigned: 需續辦
    Review --> [*]: 結案
```

> **本圖的教學價值**：它把「監控」從一次性駭客行為，畫成**可長期運轉的官僚工單系統**（§0、§10.1 的核心命題）。每一個狀態轉移都是**一次行政動作**，而 AI（Claude）在 `Collection`（造工具）與 `Analysis`（跑 SNA）兩個狀態貢獻最大——**它自動化了流水線的兩端，中間的行政與行動仍是人與體制**（§4.2）。

### C.4 防禦者能學到什麼

- **監控是系統，不是事件**：偵測不該只找「一個惡意擴充」，而要辨識「**採集→解析→分析→立案→行動**」的**整條流水線**在你的生態裡有沒有節點（附錄 A 抓採集端、附錄 D 的反制抓分析端）。
- **schema 即意圖**：若能取得一套系統的資料模型，`beliefs`／`action` 這種欄位本身就是**目的的自白**——這也是為什麼 Anthropic 只憑「前端開發對話＋後端原始碼」就能高信度判斷 Arman 的性質。
- **對台灣**：任何「以信仰／政治傾向為結構化欄位」的人員資料庫，都應觸發治理紅線審查（附錄 §10.4 的延伸）。

---

## 附錄 D：社群網路分析（155,216 則推文、點名 39 帳號）的技術方法與反制

報告說單位 A「running **social-network analysis** over **155,216 tweets**」且 SNA 管線「**named 39** Iranian opposition and diaspora accounts」（p.101–102）。本節說明：從 15 萬則推文到 39 個名字，中間的 **SNA 技術漏斗**長什麼樣，以及異議者能怎麼反制。

### D.1 SNA 漏斗：從 155,216 到 39

```mermaid
flowchart LR
    A["抓取 155,216 則推文<br/>（含轉推/提及/回覆/引用/hashtag）"] --> B["建圖：節點=帳號，邊=互動<br/>（retweet/mention/reply 各成一層）"]
    B --> C["中心性度量<br/>degree / betweenness / eigenvector / closeness"]
    B --> D["社群偵測<br/>Louvain / Leiden（模組度最佳化）"]
    C --> E["找『意見領袖』：高中心性節點"]
    D --> F["找『異議者叢集』：反對派/離散社群分群"]
    E --> G["交叉：高中心性 且 落在異議叢集"]
    F --> G
    G --> H["產出點名清單：39 個帳號"]
    H --> I["寫入 Arman → action（附錄 C）"]
```

### D.2 中心性度量：為什麼「點名」會先鎖定意見領袖

SNA 把社群互動建成圖（graph）後，用**中心性（centrality）**衡量每個節點的重要性。對「鎖定異議領袖」最有用的是：

| 度量 | 定義（直白版） | 對監控者的用途 | 對誰最危險 |
|---|---|---|---|
| **Degree（度中心性）** | 直接連了多少人 | 找「粉絲/互動多」的帳號 | 大 V、串連者 |
| **Betweenness（中介中心性）** | 有多少「最短路徑」得經過你——你是不是**橋樑** | 找**跨社群的橋接者**（把不同異議圈連起來的人），拿掉他最能切斷串連 | **協調者、跨圈聯絡人**——監控者最想除掉的正是這種 |
| **Eigenvector（特徵向量中心性）** | 你連的人本身有多重要（連到大咖也讓你重要） | 找「影響力的影響力」 | 意見領袖的核心圈 |
| **Closeness（接近中心性）** | 你平均多快能觸及全網 | 找訊息擴散最快的節點 | 動員發起者 |

> **這就是為什麼「betweenness 高」在異議網路裡是**高風險標籤**：學術文獻（arXiv 2011.01627、1805.06680）明白指出，betweenness 是**辨識網路中『領袖／關鍵行為者』**的核心度量，甚至被用於「以朋友的朋友關係辨識恐怖組織成員」。同一套數學，用在鎮壓就是**先鎖定把運動串起來的人**。

### D.3 社群偵測：把「誰跟誰一夥」自動分群

**社群偵測（community detection）**（最常見是 **Louvain／Leiden**，以**模組度 modularity** 最佳化）把圖切成「內部連結密、跨群連結疏」的**社群**。監控者用它來：

- 自動把 15 萬則推文的參與者**分成叢集**（例如：境內學運圈、海外離散圈、特定族群/宗教圈）。
- 找出**叢集之間的橋接帳號**（配合 betweenness）——這些人被**點名**的風險最高。
- 對整個叢集做**標籤化**（「這群是反對派」），為 Arman 的**批次立案**提供輸入。

**155,216 → 39 的漏斗邏輯**：15 萬則推文可能牽涉數千帳號；SNA 先建圖、算中心性、跑社群偵測，再用「**高中心性 ∩ 落在反對派/離散叢集**」的交集**收斂到 39 個最有『行動價值』的名字**。這 39 不是隨機，是**演算法挑出的「拿掉他們最能癱瘓網路」的節點**。

### D.4 異議者／防禦方的反制（OPSEC 與去中心化）

SNA 的弱點就是反制的著力點——**它吃的是「互動關係」，所以改變互動結構就能反制**：

| 反制 | 打擊哪個 SNA 假設 | 代價／限制 |
|---|---|---|
| **降低可連結性**：分身帳號、不同圈不共用帳號、少用可辨識的互動（公開轉推/提及） | 讓「同一人」在圖上無法被連成單一高中心性節點 | 犧牲觸及與動員效率 |
| **去中心化協調**：不靠單一橋接者，改多點、冗餘連結 | 破壞 betweenness——沒有單一節點拿掉就能切斷網路 | 協調成本高、易誤傳 |
| **端到端加密＋關係最小化**：Signal 等，減少可被去匿名的公開關係 | 讓「去匿名器／電話→身分」缺原料（但注意實名門號的風險，§2.2） | 對抗**已實名化**的環境效果有限 |
| **雜訊與去識別**：延遲發文、避免固定作息/語言指紋 | 打擊「行為節律／文體」這類輔助關聯特徵 | 使用體驗差 |
| **平台側保護**：限制第三方大規模抓取、對協同檢舉異常偵測 | 從源頭斷掉 SNA 的資料供給與 mass-report 壓制 | 需平台配合，跨境難施力 |

> **殘酷的現實（要對學員講）**：反制**只能提高成本、無法歸零**。只要異議者要在公開平台**發聲並串連**，就必然留下**可被 SNA 利用的互動足跡**——這是**公開行動與匿名安全的根本矛盾**。而附錄 A 的收割器＋§2.2 的實名門號解析，正是為了**補上 SNA 缺的那一塊：把匿名節點還原成真人**。**收割（附錄 A）＋解析（§2.2）＋SNA（附錄 D）＋立案（附錄 C）＝一條完整的監控殺傷鏈**，這也是把全案四塊技術串起來的總結。

---

## 附錄 E：伊朗數位監控體系的技術組織（MOIS / IRGC / FATA）——體系背景補強

本節深化 §2.5、§9.4，把「兩個伊朗安全單位」放進**真實的組織地景**。重申 §12 第 4 點的限制：**報告未指明這 16 個帳號確切屬 MOIS 或 IRGC 或 FATA 哪一支**；本節是**體系背景**，不是本案的確定歸屬。

| 機關 | 全稱／性質 | 在境內數位監控的角色 | 與本案的可能關聯（推測，非報告主張） |
|---|---|---|---|
| **MOIS（اطلاعات，情報部）** | 文官情報機關，約 3 萬人 | 核心任務含**監控國內敵人（政治異議、宗教少數）**、訊號情報 | 與「監控異議者、側寫、跨國鎮壓」高度吻合 |
| **IRGC-IO（革命衛隊情報組織）** | 準軍事情報，與 MOIS **任務重疊、常競爭** | **境內監控＋戰略目標情報**；EWCD（電子戰與網路防禦組織）主責攻擊性網路，Cyber Command 轄約 3,000 個 cyber battalion | 報告用「paramilitary domestic security」，語感更貼 IRGC；「Qom 省級單位」符合 IRGC 省級部署 |
| **FATA（網路警察，2011 成立）** | 一般警察體系下的網路警察 | **監控線上運動者、ISP、資訊業者**，兼打網路犯罪與境內壓制 | 與「平台層壓制（mass-report bot）、身分解析」相容 |

**技術組織的三個關鍵事實（本階段查證）**：

1. **重疊任務、資源競爭／匯流**：伊朗情報體系的特徵是**多機關任務重疊**，導致情報與軍事資源時而競爭、時而匯流（Recorded Future、INSS）。這**正好對應本案的 federated model**——多個小單位餵養同一中央系統（附錄 C.2）。「多個小團隊擠同一空間、共用基礎設施」（§2.3 的 co-located）是這種組織生態的微觀縮影。
2. **偽裝成日常剛需 App 的監控是伊朗十年老套路**：Domestic Kitten／APT-C-50（2016–2021，假 App）、DCHSpy（2025，假 VPN）到本案（假禱告工具）一脈相承（§9.4 對比表）。**AI 的新意不在偽裝手法，而在把開發門檻降到「一個操作員配 Claude」**（§4.2）。
3. **臉部辨識等實體監控並行**：伊朗另有 FindFace（NtechLab）臉部辨識部署（§9.4）——提醒學員本案的**數位收割只是伊朗監控機器的一環**，會與實體監控**交叉比對**。

> **歸因謹慎再提醒**：把本案兩單位**精確**掛到 MOIS/IRGC/FATA 某一支，**證據不足**（報告只說 associated with paramilitary domestic security entities，high confidence 給的是「與安全機關有關」，不是「屬於哪一支」）。體系背景讓「伊朗政府會做這種事」高度可信；但「這 16 個帳號＝哪個機關的哪個單位」仍是**單一來源、且報告刻意不細指**。

---

## 附錄 F：本階段（第二階段）新增之外部技術來源

下列來源為本次技術深化新查，全部標明用途；均為**技術方法／體系背景**佐證，**不改變** §9.1 的結論——本案**具體事實仍屬單一來源（Anthropic）**。

| # | 主題 | 來源 | URL | 用途 |
|---|---|---|---|---|
| F1 | 惡意 Firefox 擴充實例與權限指紋 | Socket「8 More Malicious Firefox Extensions」 | https://socket.dev/blog/8-more-malicious-firefox-extensions | 佐證 A.2 收割型權限組合（OAuth/session 竊取、40+ 惡意擴充） |
| F2 | 惡意擴充威脅分類與稽核 | Guardio「Malicious Browser Extensions 2026」 | https://site.guard.io/blog/malicious-browser-extensions-2026-threat-categories-audit | 佐證 A.5/A.6 稽核方法 |
| F3 | Firefox 商店審查對混淆的抵抗力弱 | arXiv 2503.04292「A Study on Malicious Browser Extensions in 2025」 | https://arxiv.org/pdf/2503.04292 | 佐證 A.5 缺口③（偽裝生產力工具易過審） |
| F4 | AMO 行為式自動偵測新機制 | CybersecurityNews「New Firefox Feature Automatically Detects Malicious Extensions by Behavior」 | https://cybersecuritynews.com/feature-automatically-detects-malicious-extensions/ | 佐證 A.5 商店往「持續監看」補強 |
| F5 | 整批下架偷窺 add-on 的前例 | BleepingComputer「Mozilla Removes 23 Firefox Add-Ons That Snooped on Users」 | https://www.bleepingcomputer.com/news/security/mozilla-removes-23-firefox-add-ons-that-snooped-on-users/ | 佐證 A.5 sleeper/更新變壞 |
| F6 | AMO 政策（禁混淆碼） | Firefox Extension Workshop「Add-on Policies FAQ」 | https://extensionworkshop.com/documentation/publish/add-on-policies-faq/ | 佐證 A.5 政策 vs. 執法落差 |
| F7 | 自動掃描的侷限（security theater） | Dan Stillman「Firefox Extension Scanning is Security Theater」 | https://danstillman.com/2015/11/23/firefox-extension-scanning-is-security-theater | 佐證 A.5 靜態審查侷限 |
| F8 | WebExtension 架構與權限 | MDN「Content scripts」/「host_permissions」/「permissions」 | https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Content_scripts | A.1/A.2 API 事實依據 |
| F9 | Firefox 127 起顯示 host permissions | MDN host_permissions（install prompt 變更） | https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/host_permissions | A.2 使用者側偵測點 |
| F10 | 內容腳本 DOM 外流與 MV3 現實 | jsmon「Browser Extension Security: Content Scripts, DOM Exfiltration and the MV3 Reality」 | https://blogs.jsmon.sh/browser-extension-security-content-scripts-dom-exfiltration-and-the-manifest-v3-reality/ | A.3 資料流機制 |
| F11 | Defender 擴充獵捕 KQL | GitHub SlimKQL / LearningKijo KQL 倉庫 | https://github.com/SlimKQL/Hunting-Queries-Detection-Rules | A.6 KQL 規則依據（DeviceTvmBrowserExtensions） |
| F12 | 企業封鎖惡意擴充 | JeffreyAppel「Check and block malicious browser extension with Defender and Intune」 | https://jeffreyappel.nl/how-to-check-and-block-malicious-browser-extension-with-microsoft-defender-and-intune/ | A.6 企業端處置 |
| F13 | 中心性度量辨識關鍵行為者 | arXiv 2011.01627「Centrality Measures: A Tool to Identify Key Actors in Social Networks」 | https://arxiv.org/pdf/2011.01627 | D.2 中心性用途 |
| F14 | SNA 偵測威脅／找領袖 | arXiv 1805.06680「Detecting cyber threats through social network analysis」 | https://arxiv.org/pdf/1805.06680 | D.2 betweenness 找領袖 |
| F15 | 社群偵測方法 | Towards Data Science「SNA — Community Detection」/ MDPI 13(5):209 | https://www.mdpi.com/2078-2489/13/5/209 | D.3 Louvain/modularity |
| F16 | 伊朗網路作戰組織結構 | Recorded Future「Iran Maintains Aggressive Cyber Operations Structure」 | https://www.recordedfuture.com/iran-cyber-operations-structure | E MOIS/IRGC 重疊任務 |
| F17 | 伊朗情報體系與能力 | INSS「Iran's Cyber Strategy, Institutions, and Capabilities」 | https://www.inss.org.il/wp-content/uploads/2024/02/Part-2.pdf | E 機關分工、EWCD/cyber battalions |
| F18 | dual-use 護欄與 misuse 風險治理 | NIST AI 800-1「Managing Misuse Risk for Dual-Use Foundation Models」 | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-1.ipd.pdf | B.1/B.3 能力護欄與治理框架 |
| F19 | Iran 案第三方轉述（確認細節） | Iran International「Iran regime used Claude to expand surveillance…」 | https://www.iranintl.com/en/202609131676 | 交叉確認本案細節（仍為轉述 Anthropic） |

> **F 類的定位**：F1–F18 都是**技術方法／體系背景**來源，讓本附錄的偵測規則、SNA 解讀、伊朗組織背景**有據可循**；但它們**沒有一個獨立查證了 GTG-34007 的 16 帳號／Arman／al-Najm al-thāqib 的存在**。F19 仍是轉述 Anthropic。**§9.1、§12 的「單一來源」結論不變。**

---

*（技術附錄結束。本附錄為第二階段技術深化增補，共新增 5 張 Mermaid 圖：權限濫用鏈 [A.4]、中性工具請求→惡意最終用途推斷 [B.4]、Arman 資料模型 ER 圖 [C.1]、Arman 案件生命週期狀態圖 [C.3]、SNA 漏斗 [D.1]。所有偵測規則標為 experimental、需調參；所有占位端點已 defang 且不可連線；未轉錄任何受害者個資。）*
