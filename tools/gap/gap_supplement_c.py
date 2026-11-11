"""Supplement C: interviews, scenarios, capstone briefs, agents and AI tools, tool directory, 12-month roadmap, readiness check."""

C_SECTIONS = [
 ("C1", "Data Engineering and Analytics Interview Questions", [
  ("ETL vs ELT", "ETL transforms before loading; ELT loads raw data and transforms inside the warehouse. ELT suits cloud warehouses and keeps raw data for rebuilds. Choose ETL when data must be masked before it lands."),
  ("What is idempotency?", "A pipeline is idempotent if running it twice leaves the same result. Use MERGE on a business key, staging tables and run IDs."),
  ("Batch vs streaming?", "Batch processes data in scheduled chunks with simpler tooling. Streaming processes events continuously for low latency, at higher complexity. Choose by the freshness the business needs."),
  ("Star vs snowflake schema?", "A star schema has denormalised dimensions and simple joins, which is fast for BI. A snowflake normalises dimensions, saving space and adding joins."),
  ("What is a surrogate key and why use it?", "A system-generated key for a dimension row, so history (SCD Type 2) and source key changes do not break facts."),
  ("How do you handle late-arriving data?", "Reprocess the affected window (backfill), use watermarks that allow a lag, and make loads idempotent."),
  ("What does a dbt test check?", "Built-in tests check not null, unique, accepted values and relationships; custom tests are SQL queries that should return zero rows."),
  ("What is Airflow used for?", "Scheduling and monitoring workflows as DAGs with dependencies, retries and alerts. It does not process large data itself."),
  ("Spark shuffle and partitions?", "A shuffle moves data between machines during joins and groupBy; reduce it with good partitioning, broadcast small tables and avoid skew."),
  ("Warehouse vs lakehouse?", "A warehouse is optimised for SQL on structured data; a lakehouse adds open table formats on cheap storage for both files and SQL."),
  ("How do you test a data pipeline?", "Unit tests for transformations, data tests for quality, contract tests for source schemas, and a staging run compared with production totals."),
  ("What is CDC?", "Change data capture reads inserts, updates and deletes from a database log, so downstream systems stay current without full reloads."),
 ]),
 ("C2", "Seven Business Scenario Interviews (with answer frameworks)", [
  ("Sales declined by 20%. How would you investigate?", "Clarify the period and the scope. Check data quality first (did the data load fully?). Split the decline by region, product, channel, customer segment and price. Compare with last year and with marketing and stock events. Form two or three hypotheses, test each, and recommend actions with expected impact."),
  ("Customer churn increased. What would you analyse?", "Define churn precisely. Build cohorts and see which cohorts churn. Compare churned and retained customers on usage, support tickets, price changes and product fit. Check onboarding funnel drop-offs. Recommend an experiment, not a guess."),
  ("A dashboard is slow. How would you optimise it?", "Find the slow visuals and queries. Reduce the data model (remove unused columns, aggregate at the right grain), use summary tables or incremental refresh, simplify DAX or SQL, check relationships and cardinality, and cache where the platform allows."),
  ("A data pipeline failed. How would you troubleshoot?", "Confirm impact and mitigate (re-run or stop downstream). Read the first error, check upstream freshness and schema changes, reproduce on a sample, fix the root cause, add a test or alert, and write a short review."),
  ("An AI assistant gives incorrect answers. How would you investigate?", "Log the exact prompt, retrieved context and model version. Check whether the right documents were retrieved. Compare answers with a labelled test set. Separate retrieval failures from generation failures. Add failing cases to the evaluation set and fix the cause."),
  ("An enterprise customer wants to automate a manual workflow. How would you design it?", "Map the current process and the exceptions. Pick the high-volume, low-risk steps to automate first. Design the flow with systems, data, approvals for risky actions, logging and fallbacks. Pilot with success metrics, then scale."),
  ("A stakeholder asks for a dashboard but cannot define requirements. How would you proceed?", "Ask about the decision the dashboard supports, who uses it and how often. Sketch two or three mock screens, get feedback, agree the first five metrics and a definition for each, then build a first version in a short cycle."),
 ]),
 ("C3", "Behavioural Interviews and STAR Answers", [
  ("Tell me about yourself", "Two minutes: current role, one relevant project with a result, the skills you want to use in this role, and why this company."),
  ("Explain a difficult project", "Situation (context and stakes), Task (your role), Action (what you did, with trade-offs), Result (measured outcome), Learning."),
  ("Describe a problem you solved", "Pick a problem with data or a process change. Show how you found the root cause and what changed afterwards."),
  ("Explain a conflict with a stakeholder", "Show that you understood their goal, aligned on data and the decision, and kept the relationship."),
  ("Describe a failed project", "Own the failure, explain what you missed, what it cost, and what you do differently now."),
  ("How do you prioritise work?", "Value, urgency, effort and risk; agree priorities with the owner; say no to low-value requests with a reason."),
  ("How do you explain technical concepts to non-technical stakeholders?", "Start with the business question, use one visual, use plain words, check understanding, and give the decision needed."),
 ]),
 ("C4", "Eight Capstone Project Briefs and Portfolio Checklist", [
  ("Project 1: Business analytics dashboard", "Excel cleaning, SQL analysis, Power BI dashboard, KPI reporting and recommendations. Deliverables: dataset, cleaning log, SQL file, PBIX, one-page summary."),
  ("Project 2: Customer churn prediction", "Python, pandas, statistics, a classification model, evaluation with precision, recall and ROC-AUC, and a business interpretation with a retention plan."),
  ("Project 3: End-to-end data engineering pipeline", "Extract from an API, load raw files, transform with dbt or SQL into bronze, silver and gold layers, orchestrate with Airflow or a scheduler, and run data-quality checks. Deliverables: repository, architecture diagram, run instructions, quality report."),
  ("Project 4: AI-powered data analyst", "Upload a CSV or Excel, ask questions in natural language, generate and validate SQL or Python, create charts and a business summary. Validation: compare generated results with a manual check."),
  ("Project 5: Enterprise RAG knowledge assistant", "Ingest documents, chunk, embed, store in a vector index, retrieve, answer with citations, evaluate faithfulness and recall on a labelled question set."),
  ("Project 6: AI agent for business operations", "Design the agent, add tool calls to two business APIs, orchestrate steps, add human approval for risky actions, and monitor each run."),
  ("Project 7: MCP-powered business assistant", "An MCP server with read tools for a database and one business app, scoped permissions, logs, and an AI client that uses it."),
  ("Project 8: Industry-specific capstone (choose one)", "Real estate lead and customer analytics; education analytics and an AI learning assistant; financial document processing and analytics; customer service intelligence; e-commerce customer intelligence. Each needs: business problem, users, data sources, requirements, architecture, data flow diagram, implementation steps, tests, metrics, limitations, future work, GitHub repository, demo video and documentation."),
  ("Portfolio checklist (all projects)", "GitHub repository with README, requirements file, tests, sample data (or a public dataset link), screenshots, a 3-minute demo video, a one-page business summary and a limitations section."),
 ]),
 ("C5", "AI Agents: LangGraph, CrewAI, AutoGen and Agent Evaluation", [
  ("LangGraph: stateful agents as graphs", "Nodes are steps, edges decide the next step, and state is saved between steps. Use it when you need control, retries and human approval. Official docs: docs.langchain.com (LangGraph overview)."),
  ("CrewAI: role-based agent teams", "Agents have roles, goals and tasks; a crew runs them in sequence or with a manager. Good for quick prototypes. Official docs: docs.crewai.com."),
  ("AutoGen concepts", "Conversational multi-agent framework where agents message each other. Understand the concept even if you use another framework. Check the official project for the current version."),
  ("Agent evaluation and monitoring", "Measure task completion rate, tool success rate, accuracy, latency and cost per task; keep traces of each run; run a regression test set after every change; test for security (prompt injection and tool misuse)."),
 ]),
 ("C6", "Context Engineering, Model Choice and AI Analytics Checklist", [
  ("Context engineering", "Choose what goes into each model call: instructions, relevant retrieved passages, short history and tool results. Keep it small and relevant, label each part, and log what was sent."),
  ("Choosing and comparing models", "Compare OpenAI, Anthropic Claude and Google Gemini on your own test set for quality, latency, context length, data terms and cost. Pricing and model names change, so check the official pricing page on the day you decide."),
  ("AI analytics checklist", "Define the question. Check the data quality. Ask the AI for a method, then verify the numbers yourself on a sample. Document the prompt and the output. Note limitations and personal data handling before sharing."),
 ]),
 ("C7", "Tools and Learning Resources Directory (categories from the prompt)", [
  ("How to use this directory", "Each entry needs: purpose, beginner explanation, official site, official docs, official tutorial, free or paid status, the course module it supports, learning order and an exercise. Check the official pages before you rely on prices or features; record the date you checked."),
  ("Categories", "1 Excel and spreadsheets; 2 SQL and databases; 3 Power BI and BI platforms; 4 Python and coding environments; 5 Statistics and mathematics; 6 Machine learning; 7 Data engineering; 8 Cloud platforms; 9 Generative AI; 10 RAG and vector databases; 11 AI agents; 12 MCP and API development; 13 No-code automation; 14 Git and development; 15 Product and project management; 16 Portfolio and interview preparation."),
  ("Tool evaluation sheet (for AI and no-code tools)", "What it does; why use it; who should use it; main features; free, freemium or paid features and limits; strengths; weaknesses; alternatives; practical example; official documentation; exercise."),
 ]),
 ("C8", "Realistic 12-Month Roadmap (beginner)", [
  ("Months 1 to 2: Foundation", "Excel (module 1), SQL basics (module 2), basic statistics (module 7 start), business analytics basics. About 10 hours a week. Milestone: a cleaned dataset with a 5-metric summary. Assessment: a timed SQL test and an Excel cleaning exercise."),
  ("Months 3 to 4: Business intelligence", "Power BI (module 3), star schema and DAX, dashboard design. About 10 hours a week. Milestone: a published dashboard with row-level security. Assessment: dashboard review against a rubric."),
  ("Months 5 to 6: Programming and data", "Python (module 6), pandas, visualisation, Git and GitHub. About 12 hours a week. Milestone: a Python EDA on a public dataset in GitHub. Assessment: code review with tests."),
  ("Months 7 to 8: Machine learning and statistics", "Statistics (module 7), supervised learning, evaluation, a churn model. About 12 hours a week. Milestone: a churn model with a business recommendation. Assessment: model evaluation and explanation."),
  ("Months 9 to 10: Data engineering and cloud", "Warehouse concepts, ETL and ELT, dbt, Airflow, one cloud (see Supplement A). About 12 hours a week. Milestone: a three-layer pipeline with tests. Assessment: pipeline review and a failure drill."),
  ("Months 11: GenAI, agents and MCP", "LLM APIs, RAG, agents, MCP (modules 5 and 8). About 12 hours a week. Milestone: a RAG assistant with citations and an evaluation. Assessment: evaluation report."),
  ("Month 12: Portfolio and interviews", "Two capstone projects published, resume, LinkedIn, mock interviews and the readiness check (C9). About 15 hours a week. Milestone: three mock interviews and two published projects. Assessment: interview rubric."),
  ("What employers generally expect", "Working projects with code and data, clear documentation, measured results, the ability to explain trade-offs and a steady learning record. The programme makes no promise of employment or any salary."),
 ]),
 ("C9", "Career Readiness Check", [
  ("Self-check (answer yes or no)", "I can write SQL joins, window functions and cohorts from memory. I can build a dashboard with a star schema and DAX measures. I can clean data and explain every step. I can explain a model's metrics to a non-technical person. I have two published projects with READMEs. I can describe an ETL pipeline and its tests. I can explain RAG and a basic agent. I can explain privacy basics for personal data."),
  ("Scoring", "Ten or more yes: ready to apply for analyst roles with a portfolio. Seven to nine: complete the missing topics in the matching supplement and build one more project. Fewer than seven: return to the foundation months of the roadmap."),
 ]),
 ("C10", "Cheat Sheets and Glossary (index)", [
  ("Cheat sheets (now built: PDF 14, Quick Reference and Cheat Sheets)", "Excel formulas; SQL commands (SELECT, joins, window functions, CTEs); DAX (CALCULATE, filter context, time intelligence); Python syntax and pandas commands; statistics formulas; ML metrics (precision, recall, F1, ROC-AUC, MAE, RMSE, R-squared); API terms (endpoint, method, status code, header, token); MCP terms (host, client, server, tool, resource, prompt); common AI terms (token, context window, embedding, RAG, agent)."),
  ("Glossary (now built: PDF 15, Data Science and AI Glossary)", "Each entry: term, simple definition, real example, related terms, and acronym in full. It covers the terms in Supplements A and B and the course."),
 ]),
]

# topics that close the remaining audit gaps
from gap_supplement_more import C_MORE
C_SECTIONS += C_MORE
