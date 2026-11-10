
# Topic-by-topic notes, aligned with the topic lists in build_curriculum.MODULES (same order, same count).
NOTES_A = {
"1.1": [
 "Programming is giving a computer exact, ordered instructions. Software is the finished set of those instructions plus the data and settings it uses, for example a mobile banking app, a spreadsheet or a website.",
 "The CPU fetches an instruction from memory, decodes it, executes it (add, compare, move data, jump) and moves to the next one, billions of times a second. Memory (RAM) holds running programs and data; storage (SSD) keeps files when power is off; the operating system shares the CPU, memory and devices between programs.",
 "A programming language is a human-readable way to write instructions. A compiler (C, Go, Rust) translates the whole program into machine code before it runs, which is fast at run time. An interpreter (Python, JavaScript) reads and runs the code as it goes, which is quicker to write and test. Many modern languages mix both (Java and C# compile to bytecode run by a virtual machine).",
 "The frontend is what users see and click: web pages or app screens built with HTML, CSS and JavaScript. The backend runs on servers: it checks rules, stores and reads data, calls other services and returns results. An AI feature usually has a frontend chat box and a backend that calls the model API and the database.",
 "An IDE (integrated development environment) such as VS Code or Cursor combines a code editor with syntax colouring, auto-complete, a terminal, a debugger, Git integration and extensions. A development environment also includes the installed language (Python), package manager (pip, npm) and project settings.",
 "Applications are created by writing code, testing it, packaging it and deploying it to a computer or server. Software communicates over networks using protocols: HTTP for web requests, JSON as the data format, APIs as the agreed contract, and webhooks or queues for events. Example: your app sends an HTTP POST with JSON to an AI API and receives a JSON reply.",
],
"1.2": [
 "Install Python 3 from python.org (Windows: tick 'Add Python to PATH') or with a package manager (brew on macOS, apt on Linux). Check with python --version. Use VS Code with the Python extension. Create a project folder, then a virtual environment (python -m venv .venv) and activate it before installing libraries.",
 "A variable is a name for a value: price = 499. Core types: int (whole numbers), float (decimals), str (text in quotes), bool (True/False), None (no value). Strings support slicing (name[0:3]), methods (.upper(), .split(','), .strip()) and f-strings (f'Total: {price}'). Numbers support + − * / // (whole division) % (remainder) ** (power).",
 "A list is ordered and changeable: leads = ['Asha', 'Ravi']; leads.append('Meera'). A tuple is ordered and fixed: point = (12.9, 77.6). A set holds unique items and supports union and intersection: {'a','b'} & {'b','c'}. A dictionary maps keys to values: customer = {'name': 'Asha', 'plan': 'pro'}; customer['plan'] reads a value. Dictionaries are the Python shape of JSON.",
 "Operators compare and combine values: == != < > <= >=, and, or, not, in. if / elif / else run code only when a condition is true. for loops repeat over each item (for lead in leads:), while loops repeat while a condition holds. break leaves a loop early; continue skips to the next item. range(5) gives 0 to 4.",
 "A function is a named, reusable block: def total(price, qty=1): return price * qty. Parameters are the inputs (qty has a default value). return sends a result back. Keyword arguments (total(price=100, qty=3)) make calls readable. Keep functions small with one job; add a docstring explaining what they do.",
 "A module is one .py file; a package is a folder of modules. import json or from pathlib import Path loads them. File handling: with open('leads.txt', encoding='utf-8') as f: text = f.read() (the with block closes the file). Exceptions handle errors: try: ... except ValueError as e: ... finally: ... so one bad record does not crash the whole job.",
 "A class is a blueprint; an object is one instance. class Lead: def __init__(self, name, phone): self.name = name; self.phone = phone; def label(self): return f'{self.name} ({self.phone})'. Inheritance reuses a parent class: class HotLead(Lead) adds or overrides behaviour. Use classes when data and the actions on it belong together.",
 "json.load / json.dump read and write JSON; the csv module or pandas.read_csv read CSV; pandas.read_excel (with openpyxl) reads Excel. A virtual environment keeps each project's libraries separate. pip install requests installs a package; pip freeze > requirements.txt records versions so others can rebuild the same environment. Reusable code lives in functions and modules that other scripts import.",
],
"1.3": [
 "JavaScript runs in every browser and on servers with Node.js. let and const declare variables (const cannot be reassigned). Functions: function add(a, b) { return a + b } or arrow form const add = (a, b) => a + b. Arrays: [1, 2, 3].map(x => x * 2). Objects: { name: 'Asha', plan: 'pro' } with obj.name access.",
 "ES6 added let/const, arrow functions, template strings (`Hi ${name}`), destructuring (const { name } = user), spread (...items), modules (import/export) and classes. A Promise represents a future result. async/await makes asynchronous code read top to bottom: const res = await fetch(url); const data = await res.json(). JSON.parse and JSON.stringify convert between text and objects.",
 "TypeScript adds types: let price: number; function greet(name: string): string. An interface describes an object's shape: interface Lead { name: string; phone: string; score?: number } (score is optional). The compiler (tsc) reports type errors before the code runs, which prevents a large class of bugs in bigger apps.",
 "JavaScript is flexible and fast to start; TypeScript is safer and easier to maintain as a project grows, and it is the default in most React and Next.js projects. Practical API integration: a typed function fetches an endpoint, checks res.ok, parses JSON into an interface, handles errors with try/catch and shows a loading state in the UI.",
],
"1.4": [
 "Array: items in order with fast access by index. Linked list: items point to the next item; fast insert, slow lookup. Stack: last in, first out (undo history). Queue: first in, first out (job processing). Hash table (Python dict): key to value with near-constant lookup. Tree: hierarchy (folders, org charts); a binary search tree keeps items sorted. Graph: nodes and edges (road maps, social networks, knowledge graphs).",
 "Linear search checks each item (O(n)); binary search halves a sorted list each step (O(log n)). Sorting algorithms include merge sort and quicksort (O(n log n)); in practice use the built-in sorted(). Recursion: a function calls itself on a smaller input until a base case, for example walking a folder tree or computing factorial(n) = n × factorial(n − 1).",
 "Big O describes how time or memory grows as input grows: O(1) constant, O(log n), O(n), O(n log n), O(n²). Space complexity is the extra memory used. Problem decomposition breaks a big problem into small steps you can solve and test one by one: understand inputs and outputs, list cases, solve the simplest case, then generalise.",
],
"1.5": [
 "git init creates a repository; git clone URL copies one from GitHub. git status shows changes; git add stages them; git commit -m 'message' saves a snapshot. git branch feature-x and git switch feature-x create and move to a branch. git merge combines branches. git push sends commits to GitHub; git pull brings others' commits down.",
 "A pull request (PR) proposes merging a branch, shows the diff and collects review comments and CI results. A merge conflict happens when two branches edit the same lines; Git marks the conflict with <<<<<<< ======= >>>>>>>, you keep the right lines, remove the markers, then add and commit. A README.md explains what the project does, how to install and run it, and how to use it.",
 "GitHub Issues track bugs and tasks with labels and assignees; GitHub Projects arranges them on boards. For a portfolio, each project repository needs a clear README with the problem, a screenshot or demo link, the architecture, how to run it and what you learned. Recruiters and clients read READMEs first.",
],
"1.6": [
 "The Software Development Life Cycle (SDLC) runs requirements → design → implementation → testing → deployment → maintenance. Agile delivers in small increments with frequent feedback. Scrum uses fixed sprints (1–4 weeks), roles (product owner, scrum master, developers) and events (planning, daily stand-up, review, retrospective). Kanban visualises work on a board and limits work in progress.",
 "Requirements analysis turns needs into clear, testable statements. Software design chooses the components, data and interfaces. Modular programming splits code into independent parts. Clean code uses meaningful names, short functions, no duplication and comments that explain why, not what.",
 "Code review: a teammate reads your change before merge to catch bugs and share knowledge. Testing: unit tests (pytest) check small parts; integration tests check parts together. Debugging finds the cause of a bug using error messages, print/logging and a debugger with breakpoints. Logging records what happened in production. Documentation explains how to use and maintain the code.",
 "Design patterns are proven solutions: Factory (create objects without naming the exact class), Strategy (swap an algorithm, such as which AI model to call), Observer (notify listeners of events), Adapter (wrap an incompatible API). SOLID: Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion. Refactoring improves structure without changing behaviour, protected by tests. Maintenance fixes bugs and updates dependencies over time.",
],
"1.7": [
 "VS Code is a free, extensible editor. Cursor is an AI-first fork of VS Code with chat and multi-file edits. GitHub hosts code and runs CI. GitHub Copilot suggests code inline. Claude Code is an AI coding agent in the terminal and IDE that reads your repository, edits files and runs commands with your permission.",
 "The terminal runs commands: cd (change folder), ls/dir (list), mkdir (make folder), python app.py (run), git status. Package managers install libraries: pip (Python), npm (JavaScript), brew/apt (system). Debugging tools: breakpoints, step over/into, variable watch, browser DevTools (Console, Network, Elements).",
 "AI assistants speed up drafting, explaining and refactoring, but they can produce code that looks right and is wrong, insecure or outdated. Always read the code, run it, write or run tests, check for hard-coded secrets and unsafe input handling, and understand every line you commit. Never paste customer secrets or personal data into tools your company has not approved.",
],
"2.1": [
 "Structured data fits rows and columns with a fixed schema (customer table). Semi-structured data has labels but flexible shape (JSON API replies, XML, logs). Unstructured data has no schema (emails, PDFs, images, audio, call recordings) and is where LLMs add most value, because they can read it.",
 "CSV: plain text, one row per line, comma-separated; simple but no types. Excel (.xlsx): sheets, formulas and formatting. JSON: nested objects and arrays, the default for APIs. XML: tagged markup, common in older enterprise and government systems.",
 "Validation checks each value against rules (email format, date range, required fields). Data quality covers completeness, accuracy, consistency, timeliness and uniqueness. Integrity is enforced by keys and constraints so references always point to real records. Bad data in means bad AI answers out.",
],
"2.2": [
 "A relational database stores data in tables. Each row is one record; each column is one attribute. A primary key uniquely identifies each row (customer_id). A foreign key in another table points to it (orders.customer_id), linking the tables.",
 "SELECT name, city FROM customers WHERE city = 'Pune' ORDER BY name; GROUP BY city with COUNT(*) aggregates per group; JOIN orders ON orders.customer_id = customers.id combines tables; a subquery nests one query inside another; a CTE (WITH recent AS (...) SELECT ...) names a step for readability; window functions such as ROW_NUMBER() OVER (PARTITION BY city ORDER BY created_at) rank rows within groups.",
 "Aggregate functions: COUNT, SUM, AVG, MIN, MAX. An index (CREATE INDEX ON orders(customer_id)) speeds lookups at a small cost to writes; EXPLAIN shows how a query runs. A transaction groups changes so they all succeed or all roll back. Normalisation splits data into related tables to avoid duplication and update errors.",
 "Install PostgreSQL locally (installer or Docker: docker run -e POSTGRES_PASSWORD=secret -p 5432:5432 postgres) or use a hosted service (Supabase, Neon, RDS, Cloud SQL). Connect with psql or a GUI (pgAdmin, DBeaver). Create a database and a user with only the permissions the app needs.",
],
"2.3": [
 "PostgreSQL: full-featured open-source relational database, the default choice. Supabase: hosted PostgreSQL plus auth, storage, APIs and vector search. MySQL: popular relational database for web apps. MongoDB: document database storing JSON-like records. Redis: in-memory key-value store for caching, sessions and queues. SQLite: a file-based database ideal for prototypes and local apps.",
 "Pinecone: fully managed vector database. Qdrant: open-source vector database you can self-host or use in the cloud. pgvector: a PostgreSQL extension that adds a vector column type and similarity search, so you can keep vectors next to your normal data.",
 "Relational: strict schema, joins and transactions; best for business records. NoSQL: flexible schema and horizontal scale; best for varied documents or very high volumes. Vector: similarity search over embeddings; best for semantic search and RAG. Many AI systems use all three.",
],
"2.4": [
 "An API (application programming interface) is a contract for how software requests data or actions from other software. REST models resources as URLs (/customers/42) and uses HTTP methods. GraphQL exposes one endpoint where the client sends a query listing the exact fields it wants. HTTP methods: GET (read), POST (create), PUT (replace), PATCH (partial update), DELETE (remove).",
 "A request has a method, URL, headers (Content-Type: application/json, Authorization: Bearer <token>) and body. A response has a status code (2xx success, 4xx client error, 5xx server error), headers and body. API keys identify the calling app; OAuth lets a user grant your app limited access without sharing their password. Webhooks are HTTP calls the other system makes to your URL when an event happens.",
 "Rate limits cap requests per period (HTTP 429 means slow down; retry with exponential backoff). Pagination returns results in pages using page/limit or a cursor. API documentation (often OpenAPI/Swagger) lists endpoints, parameters and examples. Postman lets you build, save and test requests and share collections with your team.",
 "Third-party integration: read the docs, get credentials, test in Postman, then write a small client function with timeouts. Error handling: check status codes, retry only safe failures, log errors without secrets. API security: HTTPS only, keys in environment variables or a secrets manager, least-privilege scopes, input validation and verifying webhook signatures.",
],
"2.5": [
 "A data pipeline moves data automatically from sources to destinations. ETL = extract, transform, load (clean before loading). ELT = extract, load, transform (load raw, clean inside the warehouse). Ingestion collects data; transformation reshapes it; cleaning fixes errors and duplicates; validation checks it meets rules before use.",
 "Batch processing handles data in scheduled chunks (nightly sales report). Stream processing handles each event as it arrives (fraud alert in seconds) using tools such as Kafka. Orchestration (Airflow, Dagster, Prefect, n8n) schedules steps, manages dependencies, retries failures and alerts on errors.",
 "A data warehouse (BigQuery, Snowflake, Redshift) stores cleaned, structured data for analytics. A data lake stores raw files of any type cheaply (S3, Azure Data Lake). A lakehouse (Databricks, Iceberg) combines both. Data governance defines ownership, access, quality standards, lineage and retention.",
],
"3.1": [
 "AI is the broad goal of machines doing tasks that need intelligence. Machine learning is the main method: learning patterns from data. Deep learning uses multi-layer neural networks and powers vision, speech and LLMs. Traditional AI predicts or classifies (fraud yes/no); generative AI creates new content (text, images, code).",
 "A neural network has layers of connected units; each connection has a weight. Training shows the network examples, measures the error with a loss function, and adjusts weights using gradient descent. Inference runs the trained network on new input; it is what happens each time your app calls a model. Parameters are the learned weights, often billions in LLMs.",
 "Features are the input variables (age, income, words); labels are the answers in training data. A dataset is split into training, validation and test sets. Limitations: models reflect bias in data, fail on data unlike their training, cannot explain themselves fully, and may be confidently wrong.",
],
"3.2": [
 "Supervised learning uses labelled examples (emails marked spam). Unsupervised learning finds structure in unlabelled data (customer segments). Reinforcement learning learns by trial and reward (game playing, and fine-tuning LLMs with human feedback).",
 "Classification predicts a category (churn: yes/no). Regression predicts a number (house price). Clustering groups similar items without labels (k-means).",
 "Decision tree: a flowchart of if-then splits; easy to explain. Random forest: many trees vote; more accurate and stable. Gradient boosting (XGBoost, LightGBM): trees added one after another to fix previous errors; often the best for tabular data. Neural networks: layered models for images, text and audio.",
 "Feature engineering creates useful inputs (days since last purchase). Preprocessing scales numbers, encodes categories and fills missing values. Training fits the model; validation tunes settings; testing gives the final unbiased score on data never used before.",
],
"3.3": [
 "Accuracy = correct ÷ total. Precision = true positives ÷ predicted positives (when it says yes, how often is it right). Recall = true positives ÷ actual positives (how many real cases it finds). F1 = harmonic mean of precision and recall. Confusion matrix: TP, FP, TN, FN counts. ROC-AUC: how well the model ranks positives above negatives across all thresholds (0.5 random, 1.0 perfect).",
 "MAE = average absolute error; MSE = average squared error (punishes large errors). Overfitting: great on training, poor on new data. Underfitting: poor everywhere. Cross-validation trains and tests on several splits for a reliable estimate. Bias = systematic error from a too-simple model; variance = sensitivity to the training sample. Model drift: data or behaviour changes over time and accuracy falls; detect it with monitoring.",
],
"3.4": [
 "Model serving makes a model available to other software, usually as a REST endpoint returning predictions. Inference APIs (OpenAI, Claude, Vertex AI, SageMaker) host the model for you. Batch inference scores large sets on a schedule; real-time inference answers each request in milliseconds to seconds.",
 "Monitoring tracks prediction volume, latency, errors, input data distribution and accuracy when labels arrive. Versioning gives each model and its training data an ID so you can roll back. Retraining refreshes the model on new data when drift is detected. Production evaluation compares live results with the offline test score.",
],
"4.1": [
 "Generative models learn the patterns of data and produce new samples. Foundation models are large models trained on broad data and adapted to many tasks. LLMs are foundation models for language. Transformers process all tokens in parallel; attention lets each token weigh the importance of every other token, which captures meaning and context.",
 "Tokens are pieces of words; tokenisation splits text into them. The context window is the maximum tokens (input + output) per request. Parameters are learned weights. Temperature controls randomness: 0 is focused and repeatable, higher values are more varied and creative.",
 "Hallucination is a confident but false or unsupported output; reduce it with retrieval (RAG), clear instructions, citations and evaluation. Multimodal AI handles several media types: reading images and PDFs, transcribing audio, generating images or video.",
],
"4.2": [
 "OpenAI API: GPT models via the Responses and Chat Completions APIs. Anthropic Claude API: Claude models via the Messages API, strong at long documents, coding and agentic tool use. Google Gemini API: Gemini models via AI Studio or Vertex AI, with long context and multimodal input. All three use API keys, messages, tool calling and structured outputs.",
 "Open-source and open-weight models (Llama, Mistral, Qwen, Gemma) can run on your own hardware. Hugging Face hosts models, datasets and libraries (transformers). Ollama runs open models locally with one command (ollama run llama3), useful for privacy and offline prototypes.",
 "Model selection compares quality on your own test set, speed, cost per million tokens, context size, data residency and terms. Pricing is per input and output token, with discounts for caching and batch. Limitations include rate limits, outages and model updates. Multi-model architecture routes each task to the best-value model and falls back if one provider fails.",
],
"4.3": [
 "Zero-shot: give only the instruction ('Classify this review as positive or negative'). Few-shot: add 2–5 worked examples so the model copies the pattern and format. Few-shot is the fastest way to improve consistency.",
 "Chain-of-thought asks the model to work through steps before answering, improving maths and multi-step logic. Many current models reason internally; for production, request a clear final answer and, if needed, a brief justification you can show users, and evaluate the final answer.",
 "Role-based prompting sets expertise and tone ('You are a senior insurance claims reviewer'). Structured output asks for JSON matching a schema; many APIs can enforce the schema. Prompt templates insert variables ({customer_name}, {ticket_text}) into a fixed prompt so every call is consistent.",
 "The system instruction sets lasting rules (role, tone, limits, format); the user message carries the specific request. Prompt evaluation runs the prompt on a test set and scores it. Optimisation changes one thing at a time and re-scores. Versioning stores each prompt with an ID so you know which version produced which output.",
],
"4.4": [
 "The context window is everything the model can see in one call. Context management decides what goes in: instructions, the user's request, retrieved documents, tool results and history. Context retrieval fetches only relevant information from databases or documents at the moment it is needed.",
 "Memory keeps useful facts across turns or sessions (user preferences, earlier decisions), stored outside the model and re-inserted when relevant. Conversation history can be truncated or summarised. Context compression shortens long text while keeping key facts. Relevance ranking keeps the most useful items when space is limited.",
 "Long-context strategies: put the most important instructions at the start and the question at the end, use clear section headings or XML-style tags, and quote the relevant passages. For agents, context engineering means giving each step only the tools, state and information it needs, and summarising results instead of passing raw logs.",
],
"4.5": [
 "An embedding model turns text (or images) into a fixed-length list of numbers, for example 1,536 values. Texts with similar meaning land close together in that space. This semantic representation captures meaning rather than exact words.",
 "Similarity search finds the stored vectors closest to a query vector. Cosine similarity measures the angle between vectors (1 = same direction, 0 = unrelated). Other measures are dot product and Euclidean distance; use the one the embedding model recommends.",
 "Count tokens with the provider's tokenizer (tiktoken for OpenAI, the count-tokens endpoint for Claude). Cost = input tokens × input price + output tokens × output price. Choose an embedding model by retrieval quality on your data, languages, dimension size (storage cost) and price; never mix embedding models in one index.",
],
"4.6": [
 "Fine-tuning continues training a pretrained model on your examples so it learns a format, tone or specialised task. Fine-tuning changes behaviour; RAG supplies knowledge. Use RAG for changing facts and citations; use fine-tuning for consistent style, structured outputs or cheaper smaller models.",
 "Supervised fine-tuning uses input-output pairs (often hundreds to thousands, in JSONL format). Prepare clean, varied, correct examples; hold out a test set; compare the tuned model with the base model plus a good prompt. Limits: cost, need for good data, risk of forgetting general skills, and retraining when the base model changes.",
],
"4.7": [
 "Accuracy: is the answer correct? Relevance: does it address the question? Faithfulness/groundedness: is every claim supported by the provided sources? Hallucination evaluation counts unsupported claims, often by checking each claim against the retrieved context.",
 "Response quality covers clarity, completeness, tone and format. Latency is time to first token and total time. Cost per request = tokens used × price. Track all three together: a better answer that is 5× slower or costlier may not be acceptable.",
 "Human evaluation is the gold standard but slow and costly. Automated evaluation uses exact-match rules, code checks or an LLM-as-a-judge with a rubric. Judges can favour longer answers, their own style or the first option shown, so calibrate them against human labels and use clear rubrics.",
],
"4.8": [
 "Lovable is an AI app builder: you describe an app in plain language and it generates a React + TypeScript web app with a live preview. Prompt it like a spec: the user, the screens, the data fields and the actions. Build the frontend one feature at a time and check each one in the preview.",
 "Connect Supabase from Lovable to get a PostgreSQL database, authentication (email, Google login) and APIs. Define tables and row-level security policies. Call external APIs (including AI models) from Supabase Edge Functions so keys stay on the server.",
 "Test every flow (sign-up, create, edit, delete, error cases). Debug with the browser console and Lovable's chat. Sync to GitHub for version control and code review, then deploy with one click or to your own hosting. Limits: generated code may have security gaps, duplicated logic or poor structure; review it before customers use it.",
],
"5.1": [
 "Retrieval-augmented generation (RAG) retrieves relevant information from your own sources and adds it to the prompt so the model answers from that information. It is needed because models do not know your private or recent data, and RAG reduces hallucination and allows citations.",
 "RAG vs fine-tuning: RAG updates knowledge instantly by updating documents; fine-tuning changes behaviour. Architecture: ingest documents → chunk → embed → store; at question time: embed query → retrieve top chunks → build prompt → generate → cite. Grounding means the answer is restricted to, and traceable to, the retrieved sources.",
],
"5.2": [
 "PDF: extract text with PyMuPDF or pdfplumber; Word: python-docx; Excel: pandas/openpyxl; HTML and web pages: BeautifulSoup or a crawler, removing menus and footers. Keep headings and tables, which carry meaning.",
 "OCR (Tesseract, cloud document AI) reads text from scanned images. Document parsing finds structure (titles, sections, tables, lists). Metadata extraction captures title, author, date, source and section. Document classification labels type (invoice, contract, policy) so retrieval can filter by it.",
],
"5.3": [
 "Fixed-size chunking cuts every N tokens; simple and predictable. Semantic chunking splits where the topic changes (headings, paragraphs). Overlapping chunking repeats some tokens between chunks so ideas are not cut in half. Optimise chunk size by testing retrieval on real questions; 300–800 tokens is a common starting range.",
 "Generate embeddings for every chunk with one model, in batches. Store metadata (source, page, section, date, access group) with each chunk for filtering and citation. Store vectors in a vector database with the chunk text and an ID that links back to the source document.",
],
"5.4": [
 "Pinecone: managed, serverless vector database. Qdrant: open source, rich filtering, self-host or cloud. pgvector: vectors inside PostgreSQL. Supabase Vector: pgvector managed by Supabase with helper APIs.",
 "Vector indexing (HNSW, IVF) makes nearest-neighbour search fast on millions of vectors. Semantic search ranks by meaning. Hybrid search combines vector and keyword (BM25) scores. Metadata filtering restricts results (department, date, permissions). Ranking orders results; a reranker can reorder the top results for better precision.",
],
"5.5": [
 "Hybrid retrieval: keyword + vector together. Query rewriting: rephrase or expand the user's question. Reranking: a cross-encoder model scores each candidate against the query. Multi-query retrieval: generate several versions of the question and merge the results.",
 "Contextual retrieval: prepend a short summary of where each chunk sits in its document before embedding. Agentic RAG: an agent decides whether, where and how often to search. Knowledge graphs store entities and relations for multi-hop questions. Multimodal RAG retrieves images, tables and charts as well as text.",
],
"5.6": [
 "Retrieval accuracy: did the right chunks come back? Context relevance: how much retrieved text is relevant. Faithfulness: is the answer supported by context? Answer relevance: does it answer the question? Recall and precision measure finding all relevant chunks vs avoiding irrelevant ones.",
 "Track retrieval latency and cost per query (embedding + search + generation). RAGAS provides standard metrics (faithfulness, answer relevancy, context precision, context recall). Build test datasets from real user questions with reference answers and source passages, and re-run them after every change.",
],
}
