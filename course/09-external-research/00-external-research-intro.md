# 模組 09 導論：延伸研究，其他機構的 AI 濫用研究

> 課程模組：09 延伸研究 ｜ 整理日期：2026-09-14 ｜ 維護方式：每週由排程研究代理自動增補，人工事後審核

## 1. 這個模組是什麼

模組 01 到 08 逐案拆解 Anthropic 2026-09 的威脅情報報告。那份報告最大的方法論限制，是它幾乎全部建立在**單一平台的遙測**上：Anthropic 只看得到 Claude 上發生的事。要判斷一個趨勢是「AI 濫用的普遍現象」還是「某一家平台的觀察偏差」，就必須拿其他平台、其他機構的同類研究來對照。

本模組收錄這些同類研究，每份一份教材，固定十二節，其中第 4 節「與 Anthropic 2026-09 報告的對照」是全模組的核心：同一個行為者在不同平台留下什麼痕跡、哪些 TTP 跨平台重複出現、哪些結論只有一家說了算。

## 2. 收錄標準

- **一手來源**：機構官方發布的報告、部落格長文、PDF，或同行審查的學術論文。新聞轉述只能當佐證。
- **同類主題**：AI 模型被濫用的實際案例與趨勢，或針對這類濫用的偵測與防線研究。
- **固定掃描來源**：Anthropic、OpenAI、Google GTIG、Microsoft、Meta、英國 NCSC、美國 CISA、ENISA、Europol、Graphika、DFRLab、Recorded Future、CSET、RAND、arXiv，以及台灣的國家資通安全研究院與 TWCERT／CC。
- **排除**：無新資料的評論、無法取得原文的二手報導、與 AI 濫用無直接關係的一般資安報告。

## 3. 怎麼讀這個模組

建議兩條路徑：

1. **時間軸**：先讀 Anthropic 自己的前作（2025-03、2025-08、2025-11、2026-02），看同一家平台的觀察怎麼從「對話式協助」演變到「agentic 編排」，再回頭讀 2026-09 報告的趨勢章節。
2. **橫向比較**：挑觀察期間接近的 OpenAI 與 Google GTIG 報告，和 2026-09 報告並讀，先對齊行為者、TTP 與分類定義，再檢查底層資料是否獨立。三家轉述同一線索仍可能是單一來源；兩家有獨立遙測則可能支持指定的跨平台主張，沒有固定的機構數門檻。

每份教材第 9 節應分開標示「來源類型、資料獨立性、驗證了哪個主張」。媒體轉述、官方編目與第三方評論，不自動增加事件證據。共用判讀規則見[證據與方法](../shared/04-evidence-and-methods.html)。

## 4. 收錄清單

下表由建置腳本依各教材的中繼資料自動產生，新到舊排序。

<!-- LEDGER:START -->
| 機構 | 發布 | 原文標題 | 教材 |
|---|---|---|---|
| Hacktron AI（獨立資安研究）（Hacktron AI） | 2026-09-13 | [Hacking OpenAI (libheif Heist)](https://www.hacktron.ai/blog/hacking-openai) | [用 Claude Opus 5 攻進 OpenAI：libheif 影像鏈與 CTF 框定繞過](hacktron-2026-09-openai-libheif-rce.html) |
| 微軟威脅情報團隊（Microsoft Threat Intelligence） | 2026-09-10 | [Detect and disrupt AI-themed attacks with Microsoft Defender](https://www.microsoft.com/en-us/security/blog/2026/09/10/detect-and-disrupt-ai-themed-attacks-with-microsoft-defender/) | [冒用 AI 品牌的攻擊與處置](microsoft-2026-09-ai-themed-attacks-defender.html) |
| Google 威脅情報小組（Google GTIG） | 2026-09-09 | [GTIG AI Threat Tracker: From Prompting to Autonomy – The Evolution of Adversarial AI](https://cloud.google.com/blog/topics/threat-intelligence/from-prompting-to-autonomy-the-evolution-of-adversarial-ai) | [從提示到自主：對抗性 AI](gtig-2026-09-ai-threat-tracker.html) |
| Mandiant（Google Cloud）（Mandiant） | 2026-08-18 | [Staying Ahead of Adversarial AI Through Agentic Source Code Review](https://cloud.google.com/blog/topics/threat-intelligence/staying-ahead-of-adversarial-ai-through-agentic-source-code-review) | [防禦側的 agentic 漏洞探勘](mandiant-2026-08-agentic-vulnerability-discovery.html) |
| 微軟威脅情報團隊（Microsoft Threat Intelligence） | 2026-07-31 | [CaptiveCrunch: Midnight Blizzard targets travelers worldwide for malware delivery and credential theft](https://www.microsoft.com/en-us/security/blog/2026/07/31/captivecrunch-midnight-blizzard-targets-travelers-worldwide-for-malware-delivery-and-credential-theft/) | [旅館 WiFi 劫持與 CaptiveCrunch](microsoft-2026-07-captivecrunch-storm-2945.html) |
| 微軟威脅情報團隊（Microsoft Threat Intelligence） | 2026-06-08 | [AI brands as bait: How threat actors are using the AI hype in social engineering](https://www.microsoft.com/en-us/security/blog/2026/06/08/ai-brands-as-bait-how-threat-actors-are-using-the-ai-hype-in-social-engineering/) | [AI 品牌作誘餌：四條行動線](microsoft-2026-06-ai-brands-as-bait.html) |
| Google 威脅情報小組（Google GTIG） | 2026-05-12 | [GTIG AI Threat Tracker: Adversaries Leverage AI for Vulnerability Exploitation, Augmented Operations, and Initial Access](https://cloud.google.com/blog/topics/threat-intelligence/ai-vulnerability-exploitation-initial-access) | [AI 漏洞利用與初始存取](gtig-2026-05-ai-threat-tracker.html) |
| 微軟威脅情報團隊（Microsoft Threat Intelligence） | 2026-03-06 | [AI as tradecraft: How threat actors operationalize AI](https://www.microsoft.com/en-us/security/blog/2026/03/06/ai-as-tradecraft-how-threat-actors-operationalize-ai/) | [AI 作為技術手法：力量倍增器](microsoft-2026-03-ai-as-tradecraft.html) |
| OpenAI 威脅情報團隊（OpenAI） | 2026-02-25 | [Disrupting malicious uses of AI](https://openai.com/index/disrupting-malicious-ai-uses/) | [AI 濫用處置報告 2026-02](openai-2026-02-disrupting-malicious-uses.html) |
| Anthropic（Anthropic） | 2026-02-23 | [Detecting and preventing distillation attacks](https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks) | [偵測與防範蒸餾攻擊](anthropic-2026-02-distillation-disclosure.html) |
| Google 威脅情報小組（Google GTIG） | 2026-02-13 | [GTIG AI Threat Tracker: Distillation, Experimentation, and (Continued) Integration of AI for Adversarial Use](https://cloud.google.com/blog/topics/threat-intelligence/distillation-experimentation-integration-ai-adversarial-use) | [蒸餾、實驗與對抗性 AI 整合](gtig-2026-02-ai-threat-tracker.html) |
| 數位發展部（moda） | 2026-01-28 | [公部門人工智慧應用參考手冊 V1.0](https://www-api.moda.gov.tw/File/Get/moda/zh-tw/WwHCroVhwWy52dw) | [台灣AI導入與資安驗收](moda-2026-01-public-sector-ai-playbook.html) |
| Anthropic 威脅情報團隊（Anthropic） | 2025-11-13 | [Disrupting the first reported AI-orchestrated cyber espionage campaign](https://www.anthropic.com/news/disrupting-AI-espionage) | [首起 AI 編排網路間諜行動](anthropic-2025-11-ai-orchestrated-espionage.html) |
| Google 威脅情報小組（Google GTIG） | 2025-11-06 | [GTIG AI Threat Tracker: Advances in Threat Actor Usage of AI Tools](https://cloud.google.com/blog/topics/threat-intelligence/threat-actor-usage-of-ai-tools) | [執行期 AI 惡意程式登場](gtig-2025-11-ai-threat-tracker.html) |
| OpenAI 威脅情報團隊（OpenAI） | 2025-10-07 | [Disrupting malicious uses of AI: October 2025](https://openai.com/global-affairs/disrupting-malicious-uses-of-ai-october-2025/) | [AI 濫用處置報告 2025-10](openai-2025-10-disrupting-malicious-uses.html) |
| Anthropic 威脅情報團隊（Anthropic） | 2025-08-27 | [Detecting and countering misuse of AI: August 2025](https://www.anthropic.com/news/detecting-countering-misuse-aug-2025) | [AI 濫用報告 2025-08](anthropic-2025-08-threat-intel-report.html) |
| OpenAI 威脅情報團隊（OpenAI） | 2025-06-05 | [Disrupting malicious uses of AI: June 2025](https://openai.com/global-affairs/disrupting-malicious-uses-of-ai-june-2025/) | [AI 濫用處置報告 2025-06](openai-2025-06-disrupting-malicious-uses.html) |
| 英國國家網路安全中心（NCSC） | 2025-05-07 | [Impact of AI on cyber threat from now to 2027](https://www.ncsc.gov.uk/report/impact-ai-cyber-threat-now-2027) | [AI威脅政府概率評估](ncsc-2025-05-ai-cyber-threat-2027.html) |
| Anthropic 威脅情報團隊（Anthropic） | 2025-04-23 | [Detecting and countering malicious uses of Claude: March 2025](https://www.anthropic.com/news/detecting-and-countering-malicious-uses-of-claude-march-2025) | [首份 Claude 濫用報告](anthropic-2025-04-malicious-uses-report.html) |
| Google 威脅情報小組（Google GTIG） | 2025-01-30 | [Adversarial Misuse of Generative AI](https://cloud.google.com/blog/topics/threat-intelligence/adversarial-misuse-generative-ai) | [生成式 AI 的對抗性濫用](gtig-2025-01-adversarial-misuse-generative-ai.html) |
| Fang等研究團隊（Fang et al.） | 2024-04-17 | [LLM Agents can Autonomously Exploit One-day Vulnerabilities](https://arxiv.org/abs/2404.08144v2) | [已知漏洞代理實驗判讀](arxiv-2024-04-one-day-agent-benchmark.html) |
<!-- LEDGER:END -->

## 5. 維護方式

每週一由排程的研究代理掃描固定來源，找出尚未收錄的新研究，依 `_brief.md` 的規格寫成教材與中繼資料，重新建置後發布。收錄與否的判斷、以及教材內容，都由人工事後審核；發現錯誤時直接修改教材並重新發布即可。
