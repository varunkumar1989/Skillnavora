"""Collect practice tests and interview questions from the handbooks into tools/practice_data.json.
Run after the handbooks change:  python3 tools/build_practice.py
Sources: Data Science & AI lessons (quiz and interview blocks), PM Master Handbook (quiz blocks and the interview handbook)."""
import json, os, re, glob, html
import yaml
HERE = os.path.dirname(os.path.abspath(__file__))
DS = "/home/user/data-science-and-ai/course/source/lessons"
PM = "/home/user/product-management-handbook/content"
CAT = json.load(open("/home/user/data-science-and-ai/course/catalog.json"))
PAGE = {f'{t["id"]}-{L["num"]:02d}': ("data-science/" + L["page"], L["title"], t["name"]) for t in CAT["tracks"] for L in t["lessons"]}

SEG = {"pm": "AI Product Management", "data": "Data Science & AI", "genai": "GenAI, Agents & AI Tools", "other": "Other programs"}
TRACK_SEG = {"excel": "data", "sql": "data", "powerbi": "data", "tableau": "data", "python": "data", "ml": "data", "career": "data", "ai-analytics": "genai",
             "genai": "genai", "agents": "genai", "tools": "genai", "sfmc": "other", "marketing": "other", "content": "other", "fde": "other", "speaking": "other"}
TRACK_NAME = {t["id"]: t["name"] for t in CAT["tracks"]}


def md_inline(s):
    s = html.escape(s.strip())
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)


def ds_lessons():
    for f in sorted(glob.glob(DS + "/*/*.md")):
        track = os.path.basename(os.path.dirname(f)); num = int(os.path.basename(f)[:2]); key = f"{track}-{num:02d}"
        if track not in TRACK_SEG or key not in PAGE: continue
        yield track, key, open(f, encoding="utf-8").read()


tests, interview = [], {k: [] for k in SEG}
for track, key, src in ds_lessons():
    page, title, tname = PAGE[key]
    for blk in re.findall(r"^:::quiz\n(.*?)^:::", src, re.S | re.M):
        for q in re.split(r"\n\s*\n", blk.strip()):
            lines = [l for l in q.splitlines() if l.strip()]
            if not lines or not lines[0].startswith("Q:"): continue
            opts, ans, why = [], None, ""
            for l in lines[1:]:
                if l.startswith("* "): ans = len(opts); opts.append(md_inline(l[2:]))
                elif l.startswith("- "): opts.append(md_inline(l[2:]))
                elif l.startswith("> "): why = md_inline(l[2:])
            if ans is not None and len(opts) >= 2:
                tests.append({"seg": TRACK_SEG[track], "topic": tname, "lesson": title, "page": page, "q": md_inline(lines[0][2:]), "o": opts, "a": ans, "h": why})
    for blk in re.findall(r"^:::interview[^\n]*\n(.*?)^:::", src, re.S | re.M):
        for m in re.finditer(r"\*\*Q: (.+?)\*\*\n(.+?)(?=\n\n\*\*Q:|\Z)", blk.strip(), re.S):
            interview[TRACK_SEG[track]].append({"q": md_inline(m.group(1)), "a": md_inline(" ".join(m.group(2).split())), "topic": tname, "page": page})

# PM handbook: quiz blocks (YAML) and the interview handbook
for f in sorted(glob.glob(PM + "/modules/m*.md")):
    src = open(f, encoding="utf-8").read(); n = int(re.search(r"m(\d+)", os.path.basename(f)).group(1))
    for blk in re.findall(r"```quiz\n(.*?)```", src, re.S):
        try: items = yaml.safe_load(blk) or []
        except Exception: continue
        for it in items:
            if not isinstance(it, dict) or "options" not in it: continue
            tests.append({"seg": "pm", "topic": f"PM Module {n}", "lesson": f"Module {n}", "page": f"handbooks/pm/m{n:02d}.html",
                          "q": md_inline(str(it["q"])), "o": [md_inline(str(o)) for o in it["options"]], "a": int(it["answer"]), "h": md_inline(str(it.get("why", "")))})
for f in sorted(glob.glob(PM + "/interview/0[1-9]*.md")):
    src = open(f, encoding="utf-8").read(); cat = re.search(r"^category:\s*(.+)$", src, re.M); cat = cat.group(1).strip() if cat else "PM interview"
    for m in re.finditer(r'^\?\?\? question "([^"]+)"\n(.*?)(?=^\?\?\? question|\Z)', src, re.S | re.M):
        head = re.sub(r"^[A-Z]+\d+\s*·\s*\w+\s*[—-]\s*", "", m.group(1)).strip()
        ma = re.search(r"\*\*Model answer:\*\*\s*(.+?)(?:\n\s*\n|\Z)", m.group(2), re.S)
        if not ma: continue
        q = {"q": md_inline(head), "a": md_inline(" ".join(ma.group(1).split())), "topic": cat, "page": "handbooks/pm/interview.html"}
        interview["pm"].append(q)
        if re.search(r"\bAI\b|LLM|agent|model|GenAI|RAG", head): interview["genai"].append(dict(q, topic="AI product questions"))

# Fill-in-the-blank exercises (W3Schools style): answer variants are compared case- and space-insensitively.
EX = [
 ("data", "Excel", "Total of sales in B2:B100", "=___(B2:B100)", ["SUM"], "The function that adds numbers."),
 ("data", "Excel", "Count non-empty cells in A2:A50", "=___(A2:A50)", ["COUNTA"], "COUNT counts numbers only; this one counts anything that is not empty."),
 ("data", "Excel", "Look up the price of the product in E2 from table A:B, exact match", "=XLOOKUP(E2, A:A, ___)", ["B:B"], "The third argument is the column to return."),
 ("data", "Excel", "Lock the reference to C1 when copying the formula", "=A2*___", ["$C$1"], "Dollar signs before the column letter and the row number."),
 ("data", "Excel", "Show 'Pass' when the score in B2 is at least 40", '=IF(B2>=40, "Pass", ___)', ['"Fail"'], "IF needs a value for the false case, in quotes for text."),
 ("data", "Excel", "Sum sales in C:C where region in A:A is 'South'", '=SUMIFS(C:C, A:A, ___)', ['"South"'], "Criteria for text go in quotes."),
 ("data", "SQL", "Select every column from the customers table", "SELECT ___ FROM customers;", ["*"], "One character means all columns."),
 ("data", "SQL", "Keep only orders above 1000", "SELECT * FROM orders ___ amount > 1000;", ["WHERE"], "The clause that filters rows."),
 ("data", "SQL", "Count orders per city", "SELECT city, COUNT(*) FROM orders ___ city;", ["GROUP BY"], "Aggregate per group of a column."),
 ("data", "SQL", "Keep only cities with more than 50 orders", "SELECT city, COUNT(*) FROM orders GROUP BY city ___ COUNT(*) > 50;", ["HAVING"], "WHERE filters rows; this filters groups."),
 ("data", "SQL", "Sort products from most to least expensive", "SELECT * FROM products ORDER BY price ___;", ["DESC"], "The opposite of ASC."),
 ("data", "SQL", "Join orders to customers on customer_id, keeping all customers", "SELECT * FROM customers c ___ JOIN orders o ON c.customer_id = o.customer_id;", ["LEFT"], "Keeps every row from the left table."),
 ("data", "SQL", "Rank salaries within each department", "RANK() OVER (___ BY dept ORDER BY salary DESC)", ["PARTITION"], "Restarts the ranking for each department."),
 ("data", "Python", "Print the length of the list nums", "print(___(nums))", ["len"], "Built-in function for the number of items."),
 ("data", "Python", "Read a CSV file into a DataFrame", "df = pd.___('sales.csv')", ["read_csv"], "pandas reader function for CSV."),
 ("data", "Python", "Average sales per region in pandas", "df.groupby('region')['sales'].___()", ["mean"], "The method for the arithmetic average."),
 ("data", "Python", "Loop over numbers 0 to 4", "for i in ___(5):", ["range"], "Generates a sequence of integers."),
 ("data", "Python", "Create a dictionary entry with key 'city' and value 'Pune'", "person = {___: 'Pune'}", ["'city'", '"city"'], "Keys are usually strings in quotes."),
 ("data", "Power BI", "DAX measure for total sales from the Sales table", "Total Sales = ___(Sales[Amount])", ["SUM"], "Aggregation function in DAX."),
 ("data", "Power BI", "Change the filter context of a measure", "Sales South = ___([Total Sales], Region[Name] = \"South\")", ["CALCULATE"], "The most important DAX function."),
 ("data", "Statistics", "p-value threshold most often used for significance", "alpha = ___", ["0.05", ".05"], "Five percent."),
 ("data", "Machine learning", "Split data into train and test sets in scikit-learn", "X_train, X_test, y_train, y_test = ___(X, y, test_size=0.2)", ["train_test_split"], "A function in sklearn.model_selection."),
 ("genai", "Prompting", "The technique of giving the model a few worked examples in the prompt", "___-shot prompting", ["few"], "Zero-shot gives none; this gives a few."),
 ("genai", "RAG", "RAG stands for Retrieval-Augmented ___", "Retrieval-Augmented ___", ["Generation"], "The model generates an answer from retrieved text."),
 ("genai", "MCP", "MCP stands for Model ___ Protocol", "Model ___ Protocol", ["Context"], "It connects AI apps to context: tools and data."),
 ("genai", "APIs", "HTTP method to create a new record", "___ /api/orders", ["POST"], "GET reads, this creates."),
 ("genai", "APIs", "Status code for 'too many requests'", "HTTP ___", ["429"], "A 4xx code about rate limits."),
 ("genai", "n8n", "Expression for the email field of the current item in n8n", "{{ $___.email }}", ["json"], "Current item data lives here."),
 ("genai", "Claude Code", "File Claude Code reads automatically for project rules", "___.md", ["CLAUDE"], "Created with /init."),
 ("genai", "Embeddings", "Similarity measure most used to compare embeddings", "___ similarity", ["cosine"], "Angle between two vectors."),
 ("pm", "Prioritisation", "RICE stands for Reach, Impact, Confidence and ___", "Reach, Impact, Confidence, ___", ["Effort"], "The cost side of the score."),
 ("pm", "Metrics", "The single metric that best captures the value users get", "___ Star Metric", ["North"], "A compass direction."),
 ("pm", "Discovery", "Framework: people 'hire' products to get a ___ done", "Jobs-to-be-___", ["done"], "JTBD."),
 ("pm", "Experiments", "Test comparing two versions with random users", "___ testing", ["A/B", "AB", "split"], "Two letters with a slash."),
 ("pm", "Agile", "Short, fixed-length iteration in Scrum", "a ___", ["sprint"], "Usually one to four weeks."),
 ("pm", "Strategy", "Analysis of strengths, weaknesses, opportunities and threats", "___ analysis", ["SWOT"], "Four initials."),
 ("other", "SFMC", "SFMC scripting language for send-time personalisation", "___script", ["AMP", "AMPscript"], "Three capital letters."),
 ("other", "Digital marketing", "Return on ad spend formula: revenue ÷ ___", "ROAS = revenue / ___", ["ad spend", "spend"], "What you paid for the ads."),
 ("other", "Digital marketing", "UTM parameter for the campaign name", "utm____", ["campaign"], "source, medium, ___"),
]
exercises = [{"seg": s, "topic": t, "q": html.escape(q), "code": html.escape(c), "ans": a, "h": html.escape(h)} for s, t, q, c, a, h in EX]

EXTRA_IV = {
 "genai": [("What is the difference between an LLM, a chatbot and an AI agent?", "An LLM is the model that predicts text; a chatbot is an interface that lets people talk to it; an agent wraps a model with instructions, tools, memory and a loop so it can take multi-step actions toward a goal."),
           ("How do you reduce hallucinations in a production AI feature?", "Ground answers in retrieved sources (RAG) with citations, ask for 'I don't know' when context is missing, constrain outputs with schemas, evaluate on a labelled test set, and add human review for high-impact answers."),
           ("How would you estimate the monthly cost of an LLM feature?", "Requests per month x (input tokens x input price + output tokens x output price), plus embeddings and infrastructure; reduce with caching, smaller models for simple turns, shorter prompts and output limits."),
           ("What is the role of evaluation sets in GenAI products?", "They are the regression tests of AI: real, labelled examples that measure accuracy, groundedness, safety and tone before every prompt, model or data change ships.")],
 "pm": [("How would you decide whether to build an AI feature at all?", "Start from a user problem and its value; check that AI is better than rules or UX fixes, that data and quality are achievable, that errors are acceptable or reviewable, and that cost per use fits the business model; then prototype and test with users.")]}
for seg, items in EXTRA_IV.items():
    for q, a in items: interview[seg].append({"q": md_inline(q), "a": md_inline(a), "topic": "Extra", "page": "handbooks/index.html"})
for k in interview: interview[k] = interview[k][:100]
data = {"segments": SEG, "tests": tests, "exercises": exercises, "interview": interview}
json.dump(data, open(os.path.join(HERE, "practice_data.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("tests:", {s: sum(t["seg"] == s for t in tests) for s in SEG}, "| exercises:", len(exercises), "| interview:", {k: len(v) for k, v in interview.items()})
