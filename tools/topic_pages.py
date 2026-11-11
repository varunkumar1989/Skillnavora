"""One page per learning topic, each with three tabs: Programme Content, Other Programmes, Learning Tools & Links.

Content is NOT rewritten. Every programme's content is copied from the blocks already generated on
resources.html (same ids, same text). The only change is presentation: external link grids are moved from the
content tab into the "Learning Tools & Links" tab, and in-page '#' links are pointed back at resources.html.
Also builds learning-platform.html (index of all topics) and tools-and-resources.html (all tools in one place).
"""
import copy, os, re
from bs4 import BeautifulSoup
from html import escape as E

# (slug, title, short name, group, content ids, tools ids, kicker)
# content ids: element ids whose content is shown in Programme Content. tools ids: element ids whose
# external links move to Learning Tools & Links (in addition to external link grids found in content).
TOPICS = [
    ("programme-pm", "AI Product Management", "AI Product Management", "Foundations and product",
     ["p-pm"], ["learn-pm"], "Product management"),
    ("programme-genai", "GenAI Launchpad", "GenAI Launchpad (resources for GenAI)", "Foundations and product",
     ["p-genai"], ["learn-genai"], "GenAI"),
    ("programme-data", "AI for Data Engineers (Data Science & AI)", "AI for Data Engineers (Data Science & AI)", "Data and engineering",
     ["p-data"], ["learn-data"], "Data science and AI"),
    ("programme-ai-engineer", "AI Engineer: the complete path", "AI Engineer: the complete path", "Data and engineering",
     ["op-ai-engineer"], [], "AI engineering"),
    ("programme-fde", "Forward Deployed Engineer (FDE)", "Forward Deployed Engineer (FDE)", "Data and engineering",
     ["op-fde"], [], "Forward deployed engineering"),
    ("programme-tool-tutorials", "Tool tutorials", "Tool tutorials", "Tools and building",
     ["p-ai"], [], "Tool tutorials"),
    ("programme-no-code", "No-code, design and automation", "No-code, design and automation", "Tools and building",
     ["learn-build"], [], "No-code and automation"),
    ("programme-digital-marketing", "Digital Marketing", "Digital Marketing (with content creation)", "Business and communication",
     ["op-marketing", "op-content"], [], "Digital marketing"),
    ("programme-sfmc", "Salesforce Marketing Cloud (SFMC)", "Salesforce Marketing Cloud (SFMC)", "Business and communication",
     ["op-sfmc"], [], "Salesforce Marketing Cloud"),
    ("programme-public-speaking", "Public Speaking", "Public Speaking", "Business and communication",
     ["op-speaking"], [], "Public speaking"),
]

GROUP_ORDER = ["Foundations and product", "Data and engineering", "Tools and building", "Business and communication"]


def _external(a):
    return (a.get("href") or "").startswith("http")


def _split(frag, soup):
    """Return (frag, tools). External link grids are removed from frag and returned as tools."""
    tools = []
    # move grids whose anchors are all external links (tool and website cards) into the tools list
    for g in list(frag.find_all("div")):
        if "grid" not in (g.get("class") or []):
            continue
        anchors = g.find_all("a")
        if anchors and all(_external(a) for a in anchors) and g.parent is not None:
            tools.append(g.extract())
    return frag, tools


def _block(soup, el_id):
    el = soup.find(id=el_id)
    return copy.copy(el) if el is not None else None


def _rewrite(html_str):
    """Point in-page links at the Resources page so they still work from the new pages."""
    html_str = re.sub(r'href="#', 'href="resources.html#', html_str)
    return html_str


def _inner(tag):
    return "".join(str(c) for c in tag.contents) if tag is not None else ""


def build(page, uhero, out):
    res_path = os.path.join(out, "resources.html")
    soup = BeautifulSoup(open(res_path, encoding="utf-8").read(), "html.parser")
    styles = "".join(str(st) for st in soup.find_all("style"))
    built = {}
    for slug, title, short, group, c_ids, t_ids, kicker in TOPICS:
        content_parts, tool_parts = [], []
        for cid in c_ids:
            el = _block(soup, cid)
            if el is None:
                raise SystemExit(f"topic_pages: missing block #{cid} for {slug}")
            # remove the learn-* tools block from content if it sits inside the same panel
            for lid in t_ids:
                for x in el.find_all(id=lid):
                    x.extract()
            _, tg = _split(el, soup)
            content_parts.append(_inner(el))
            tool_parts.extend(str(t) for t in tg)
        for lid in t_ids:
            lb = _block(soup, lid)
            if lb is None:
                raise SystemExit(f"topic_pages: missing tools block #{lid} for {slug}")
            tool_parts.insert(0, str(lb))
        built[slug] = {
            "title": title, "short": short, "group": group, "kicker": kicker,
            "content": _rewrite("".join(content_parts)),
            "tools": styles + _rewrite("".join(tool_parts)),
        }

    order = [t[0] for t in TOPICS]
    for i, (slug, title, short, group, c_ids, t_ids, kicker) in enumerate(TOPICS):
        d = built[slug]
        others = [s for s in order if s != slug]
        other_cards = "".join(
            f'<a class="card" href="{s}.html" style="margin:0 0 10px;display:block;text-decoration:none"><span class="ftag">{E(built[s]["group"])}</span>'
            f'<h3 style="margin:6px 0 2px">{E(built[s]["short"])}</h3><span class="go">Open programme →</span></a>'
            for s in others)
        tabs = ('<div class="tabs" role="tablist" aria-label="Programme sections" id="pt-bar" style="margin:0 0 18px">'
                '<button role="tab" data-pt="content" aria-selected="true">Programme Content</button>'
                '<button role="tab" data-pt="other" aria-selected="false">Other Programmes</button>'
                '<button role="tab" data-pt="tools" aria-selected="false">Learning Tools &amp; Links</button></div>')
        body = (uhero(f"Learning platform · {E(group)}", E(title), f"Everything for {E(short)} in one place: the programme content, related programmes, and tools and learning links.")
                + '<section style="padding-top:24px"><div class="wrap"><a class="btn btn-line btn-sm" href="learning-platform.html" style="margin:0 0 14px;display:inline-block">← All programmes</a>'
                + '<div id="pt-back" hidden style="margin:0 0 12px"><button type="button" class="btn btn-line btn-sm" id="pt-back-btn">← Back to the previous tab</button></div>' + tabs
                + f'<div class="ppanel" id="pp-content" role="tabpanel">{d["content"]}</div>'
                + f'<div class="ppanel" id="pp-other" role="tabpanel" hidden><h2 class="sec-h">Other programmes</h2><p class="meta" style="margin:0 0 14px">Related programmes you can study next. Each one opens on its own page.</p>{other_cards}<p><a class="btn btn-line btn-sm" href="learning-platform.html">All programmes</a> <a class="btn btn-line btn-sm" href="tools-and-resources.html">Tools &amp; learning resources</a></p></div>'
                + f'<div class="ppanel" id="pp-tools" role="tabpanel" hidden><h2 class="sec-h">Learning tools &amp; links</h2><p class="meta" style="margin:0 0 14px">Tools, websites, documentation, tutorials and external learning resources for {E(short)}. Each link opens the provider\'s own site.</p>{d["tools"]}</div>'
                + '</div></section>'
                + """<script>(function(){var b=document.getElementById('pt-bar');if(!b)return;var tabs=[].slice.call(b.querySelectorAll('[role=tab]'));
var back=document.getElementById('pt-back'),bb=document.getElementById('pt-back-btn'),cur=null,stack=[];
function render(){if(back)back.hidden=stack.length===0}
function show(k,push){if(['content','other','tools'].indexOf(k)<0)k='content';if(push&&cur&&cur!==k)stack.push(cur);cur=k;tabs.forEach(function(t){t.setAttribute('aria-selected',t.dataset.pt===k?'true':'false')});['content','other','tools'].forEach(function(p){document.getElementById('pp-'+p).hidden=p!==k});render()}
tabs.forEach(function(t){t.addEventListener('click',function(){show(t.dataset.pt,true);try{history.replaceState(null,'','#'+t.dataset.pt)}catch(e){}})});
if(bb)bb.addEventListener('click',function(){var prev=stack.pop();if(prev){show(prev,false);try{history.replaceState(null,'','#'+prev)}catch(e){}}});
function fromHash(push){show((location.hash||'#content').slice(1),push)}window.addEventListener('hashchange',function(){fromHash(true)});fromHash(false)})();</script>""")
        page(f"{slug}.html", f"{title} · SkillNavora",
             f"{short}: programme content, other programmes, and learning tools and links, on one page.", body, slug + ".html")

    # Index: every topic, grouped
    cards = ""
    for g in GROUP_ORDER:
        items = [t for t in TOPICS if t[3] == g]
        if not items: continue
        cards += f'<h2 class="sec-h" style="margin:26px 0 12px">{E(g)}</h2><div class="grid g3">'
        for slug, title, short, group, *_ in items:
            cards += (f'<a class="card" href="{slug}.html" style="text-decoration:none"><span class="ftag">{E(group)}</span>'
                      f'<h3 style="margin:8px 0 6px">{E(short)}</h3><p>Programme content, related programmes, and tools and links.</p><span class="go">Open →</span></a>')
        if g == "Tools and building":
            import make_money_page
            cards += '<a class="card" href="make-money-course.html" style="text-decoration:none"><span class="ftag">Tools and building</span>'
            '<h3 style="margin:8px 0 6px">Make Money with AI</h3><p>Find, pitch and close a first AI service client while working part time: offer, credibility stack, outreach and discovery calls.</p><span class="go">Open →</span></a>'
        cards += "</div>"
    idx = (uhero("Learning platform", 'All <span class="g">programmes</span>, one page each', "Pick a programme. Each opens on its own page with three tabs: Programme Content, Other Programmes, and Learning Tools & Links.")
           + '<section style="padding-top:24px"><div class="wrap">'
           + '<p class="meta" style="margin:0 0 6px">Start with the foundations on the top row, then build, then take it to business. Every tool and learning link is also collected on the <a href="tools-and-resources.html">Tools &amp; learning resources</a> page.</p>'
           + cards + '</div></section>')
    page("learning-platform.html", "Learning platform: all programmes · SkillNavora",
         "All SkillNavora programmes on one page: product management, GenAI, data, AI engineering, FDE, tool tutorials, no-code, digital marketing, SFMC and public speaking.", idx, "learning-platform.html")

    # Tools hub: all tools and learning links, grouped by programme
    sections = ""
    for slug, title, short, group, *_ in TOPICS:
        d = built[slug]
        sections += f'<h2 class="sec-h" style="margin:26px 0 8px"><a href="{slug}.html#tools" style="color:inherit;text-decoration:none">{E(short)}</a></h2>{d["tools"]}'
    hub = (uhero("Tools & learning resources", 'Tools, websites and <span class="g">learning links</span>', "Every tool, website, documentation page, tutorial and useful link for each programme, in one place. Each link opens the provider's own site.")
           + '<section style="padding-top:24px"><div class="wrap">' + sections + '</div></section>')
    page("tools-and-resources.html", "Tools & learning resources · SkillNavora",
         "Tools, websites, documentation, tutorials and useful learning links for every SkillNavora programme, in one place.", hub, "tools-and-resources.html")
    return len(TOPICS)
