"""閱讀分層與編輯狀態：只呈現有紀錄的核對，不把建置日期當查證日期。"""
from hashlib import sha256
from html import escape, unescape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
PROFILES = {
    "_shared/02-claude-safeguards-and-bypass-paths.md": {
        "prerequisite": "知道 AI 助理可能讀取資料或呼叫工具；不需具備越獄操作經驗。",
        "objective": "區分內容拒絕與系統授權，依案例證據判斷風險並提出可檢查的控制。",
        "deliverable": "交付證據—控制—驗收表，包含正常反例、負責人與仍未知的事項。",
    },
    "00-index.md": {
        "prerequisite": "不需先讀完整報告；先選資安、情報分析或治理角色。",
        "objective": "選定閱讀路徑，分清事件觀察、能力評測與教學推論。",
        "deliverable": "列出本次必讀的三篇教材、預計產出，以及尚缺的知識。",
    },
    "_shared": {
        "prerequisite": "先讀總索引，任選一個案例對照共用框架。",
        "objective": "把跨案例主張拆成證據、分析假設與未知，辨認不同框架的用途。",
        "deliverable": "選兩案填寫證據對照表，列出共通性、一項差異及一項不能下的結論。",
    },
    "01-cyber": {
        "prerequisite": "了解帳號、端點與網路日誌的基本用途；無需執行攻擊。",
        "objective": "區分人類決策與 AI 執行，將攻擊鏈轉成可觀察的防禦假說。",
        "deliverable": "提交一條證據鏈、一條偵測假說、三種正常活動反例及處置建議。",
    },
    "02-influence": {
        "prerequisite": "理解內容、帳號與傳播行為的差別；先讀本模組導論。",
        "objective": "分開衡量產出量、觸及與影響，辨認協同行為與歸因限制。",
        "deliverable": "用虛構貼文建立傳播證據表，說明能證明與不能證明的影響。",
    },
    "03-surveillance": {
        "prerequisite": "理解個資最小化與資訊來源限制；練習只用虛構人物。",
        "objective": "拆解蒐集、分析與處置環節，區分正常研究與高風險監控訊號。",
        "deliverable": "提交虛構情境的資料流圖、三個誤報對象及保護當事人的處置方案。",
    },
    "04-weapons": {
        "prerequisite": "理解風險評估的範圍、控制措施及證據限制。",
        "objective": "只從治理與偵測評估能力提升、人工決策點及供應鏈控制。",
        "deliverable": "完成治理風險登錄表與升級審查條件，不設計或重現武器能力。",
    },
    "05-bio": {
        "prerequisite": "了解雙重用途與分類器漏接／誤攔概念，不需生物實作。",
        "objective": "辨認攔截、降載、漏接與設計範圍外情況的不同治理意義。",
        "deliverable": "以去技術化情境撰寫審查決策與申訴流程，不產生生物操作內容。",
    },
    "06-scams": {
        "prerequisite": "理解交易、客服與帳號生命週期；不接觸真實詐騙對象。",
        "objective": "區分人設產製與已造成損害的證據，設計保護使用者的驗證措施。",
        "deliverable": "針對虛構服務提交風險訊號、正常使用反例與受害者支援流程。",
    },
    "07-distillation": {
        "prerequisite": "了解 API 使用紀錄、憑證權限與模型訓練資料基本概念。",
        "objective": "區分平台指控、可觀察存取行為與尚未證實的訓練用途。",
        "deliverable": "提交 API 異常行為證據表、三種合法高用量反例與人工審查條件。",
    },
    "08-capability-research": {
        "prerequisite": "理解樣本、分母、對照組與測試條件。",
        "objective": "分開閱讀能力指標、實驗成功率與現實世界影響，說明外推限制。",
        "deliverable": "做一張評測數字卡：分子、分母、條件、比較基線及不能外推的結論。",
    },
    "09-external-research": {
        "prerequisite": "先讀證據與方法規範，知道多篇文章可能共享同一資料來源。",
        "objective": "比較不同資料型態與平台可見度，辨認獨立證據、轉述與背景分析。",
        "deliverable": "提交兩份來源的依賴關係表，指出新增的證據與仍無法驗證的主張。",
    },
    "10-practice": {
        "prerequisite": "先讀對應案例；所有資料為虛構或合成，只在本機離線練習。",
        "objective": "交付可追溯的分析、可檢查的防禦規則，以及清楚的驗證限制。",
        "deliverable": "依作業題目提交學員材料、測試結果、誤報分析與處置決策。",
    },
}


def content_digest(text, relative=None):
    # 自動收錄清單的更新不代表導論的論點或查核範圍改變。
    if relative == "09-external-research/00-external-research-intro.md":
        text = re.sub(r"<!-- LEDGER:START -->.*?<!-- LEDGER:END -->", "<!-- LEDGER -->", text, flags=re.S)
    return sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def load_catalog(root=ROOT):
    path = Path(root) / "editorial/catalog.json"
    if not path.exists():
        return {"schema_version": 1, "pages": {}}
    catalog = json.loads(path.read_text(encoding="utf-8"))
    if catalog.get("schema_version") != 1 or not isinstance(catalog.get("pages"), dict):
        raise ValueError("editorial/catalog.json 格式不符")
    return catalog


def review_for(relative, text, catalog):
    recorded = catalog.get("pages", {}).get(relative)
    if not recorded:
        return {"state": "pending", "label": "待審：新教材", "checked_on": None,
                "scope": "尚無編輯審核紀錄。", "pending": ["來源、數字與適用範圍待核對。"]}
    if recorded.get("content_sha256") != content_digest(text, relative):
        return {"state": "pending", "label": "待審：內容已變更", "checked_on": None,
                "scope": "本文已不同於最近的審核版本，舊查核日期不適用於新內容。",
                "pending": ["需重新檢視修訂差異及其引用來源。"]}
    result = dict(recorded)
    result["state"] = "scoped" if result.get("source_checked_on") else "structure"
    result["label"] = "已核對指定來源項目" if result["state"] == "scoped" else "結構已檢查・來源待逐項複核"
    return result


def flatten_headings(tokens):
    headings = []
    for token in tokens:
        name = unescape(re.sub(r"<[^>]+>", "", token["name"]))
        headings.append({"id": token["id"], "name": name, "level": token["level"]})
        headings.extend(flatten_headings(token.get("children", [])))
    return headings


def reading_layers(tokens):
    headings = flatten_headings(tokens)
    top = [h for h in headings if h["level"] == 2] or headings
    if not top:
        return {"快速理解": [], "課堂必讀": [], "技術／分析進階": []}
    quick = [h for h in top if re.search(r"速覽|摘要|這.*是什麼|核心.*命題|學習目標|案例背景", h["name"])]
    quick = quick[:1] or top[:1]
    core = [h for h in top if re.search(r"生命週期|主要發現|證據|圖表|偵測.*缺口|方法|研究限制|未能驗證|限制與", h["name"])]
    core = [h for h in core if h not in quick][:4] or [h for h in top if h not in quick][:3]
    advanced = [h for h in top if re.search(r"附錄|技術|演練|教學設計|作業|評量|驗收|講師", h["name"])]
    advanced = [h for h in advanced if h not in quick + core][:3]
    if not advanced:
        advanced = [h for h in top if h not in quick + core][-2:]
    return {"快速理解": quick, "課堂必讀": core, "技術／分析進階": advanced}


def render_learning_panel(relative, text, tokens, root=ROOT):
    catalog = load_catalog(root)
    review = review_for(relative, text, catalog)
    module = relative.split("/")[0]
    profile = PROFILES.get(relative, PROFILES.get(module, PROFILES["_shared"]))
    up = "../" * relative.count("/")
    links = []
    for title, headings in reading_layers(tokens).items():
        items = "、".join(f'<a href="#{escape(h["id"], quote=True)}">{escape(h["name"])}</a>' for h in headings)
        links.append(f'<li><strong>{title}</strong>：{items or "本文為短篇說明，可直接通讀。"}</li>')
    checked = review.get("source_checked_on")
    source_date = f'指定來源項目核對：{escape(checked)}' if checked else "來源逐項查證：尚未完成"
    structure_date = review.get("checked_on")
    dates = (f'結構檢查：{escape(structure_date)} · ' if structure_date else "") + source_date
    pending = "；".join(review.get("pending", ["未逐項核對的主張仍待查證。"] ))
    notes = "；".join(review.get("changes", [])) or "導讀分層與審核資訊已集中於本頁入口。"
    scope = review.get("scope", "僅完成導讀分層、章節連結與結構檢查。")
    if checked:
        scope += " 指定來源項目：" + review.get("source_check_scope", "詳見編輯紀錄。")
    detection = review.get("detection_level", "教學示意／未完成環境驗證")
    if module in {"00-index.md", "_shared"}:
        detection = "引用各案例的驗證限制；分類不代表實測防禦效果"
    return f'''<section class="learning-panel" aria-label="閱讀路徑與查核狀態" data-review-state="{review['state']}">
<p class="review-badge">{escape(review['label'])}</p>
<p class="review-date">{dates}</p>
<details class="learning-paths"><summary>閱讀分層與本篇學習產出</summary>
<p><strong>先備知識</strong>：{escape(profile['prerequisite'])}</p>
<p><strong>學習目標</strong>：{escape(profile['objective'])}</p><ol>{''.join(links)}</ol>
<p><strong>完成後交付</strong>：{escape(profile['deliverable'])}</p>
<p><a href="{up}10-practice/00-practice-guide.html">各模組作業與評分規準</a> · <a href="{up}_shared/04-evidence-and-methods.html">證據、數字與框架的共同規範</a></p>
</details>
<details class="review-details"><summary>查核範圍、修訂與待驗證事項</summary>
<p><strong>本次範圍</strong>：{escape(scope)}</p>
<p><strong>重要修訂</strong>：{escape(notes)}</p>
<p><strong>待驗證</strong>：{escape(pending)}</p>
<p><strong>偵測成熟度</strong>：{escape(detection)}。合成資料測試不代表正式環境的準確率。</p>
<p><a href="{up}_shared/05-editorial-review-and-changelog.html">全站查核與公開勘誤</a></p>
</details></section>'''
