/* Content for the free "Upskill" pages. Edit freely.
   QUIZZES: answer is the index of the correct option (0 = first). */
const QUIZZES = [
  {
    id: "pm-basics", title: "Product management basics", level: "Beginner", track: "Product",
    questions: [
      { q: "What is a product manager mainly accountable for?", o: ["Writing all the code", "Outcomes: solving the right problem in a way that works for users and the business", "Managing the team's holidays", "Designing every screen"], a: 1, why: "PMs own outcomes. Engineers build, designers design; the PM makes sure the team solves the right problem." },
      { q: "Which is an outcome rather than an output?", o: ["Shipped 12 features", "Wrote 5 PRDs", "Increased week-4 retention from 22% to 28%", "Held 30 meetings"], a: 2, why: "Outcomes are changes in user or business behaviour. Outputs are things the team produced." },
      { q: "In RICE prioritisation, what does the 'C' stand for?", o: ["Cost", "Confidence", "Customers", "Complexity"], a: 1, why: "RICE = Reach × Impact × Confidence ÷ Effort." },
      { q: "A user says: 'I want a faster horse.' What should a PM do first?", o: ["Build a faster horse", "Ignore the user", "Understand the underlying job: getting somewhere quicker", "Run an A/B test"], a: 2, why: "Look past the requested solution to the job the user is trying to get done." },
      { q: "What is the main purpose of an MVP?", o: ["Launch the full product cheaply", "Learn whether an idea works with the least effort", "Impress investors", "Replace user research"], a: 1, why: "An MVP is the smallest thing that tests your riskiest assumption." },
      { q: "Which Kano category is 'expected, and causes dissatisfaction only when missing'?", o: ["Attractive", "Performance", "Must-be", "Indifferent"], a: 2, why: "Must-be features (like a working login) don't delight, but their absence frustrates users." },
      { q: "What belongs in a good problem statement?", o: ["The solution", "Who has the problem, what it is, and why it matters", "A list of features", "The launch date"], a: 1, why: "A clear problem statement names the user, the pain and its impact, without jumping to a solution." },
      { q: "Which is NOT one of the four common product risks?", o: ["Value risk", "Usability risk", "Feasibility risk", "Typography risk"], a: 3, why: "The four risks are value, usability, feasibility and business viability." }
    ]
  },
  {
    id: "metrics", title: "Metrics and analytics", level: "Intermediate", track: "Product",
    questions: [
      { q: "What is a North Star metric?", o: ["The company's revenue", "A single metric that best captures the value users get", "The number of employees", "Daily page views"], a: 1, why: "It reflects delivered user value and predicts long-term success." },
      { q: "Your sign-ups grew 30%, but week-1 retention fell from 40% to 25%. What's the best first step?", o: ["Celebrate", "Segment new users by source and check their activation", "Stop all marketing", "Redesign the logo"], a: 1, why: "Segmenting shows whether new, lower-intent users are diluting retention or the product got worse." },
      { q: "DAU/MAU measures…", o: ["Revenue per user", "Stickiness: how often monthly users come back daily", "Churn", "Conversion rate"], a: 1, why: "A higher DAU/MAU means users return more often." },
      { q: "What is a guardrail metric?", o: ["The main metric you want to move", "A metric that must not get worse while you optimise another", "A vanity metric", "A random metric"], a: 1, why: "For example, protect refund rate while optimising conversion." },
      { q: "In an A/B test, a p-value of 0.03 usually means…", o: ["There's a 3% chance the variant is better", "If there were no real difference, a result this extreme would happen about 3% of the time", "The effect is 3%", "The test failed"], a: 1, why: "A p-value describes how surprising the data would be if there were no effect." },
      { q: "Which is a vanity metric for a meditation app?", o: ["Minutes meditated per active user", "Total app downloads ever", "Week-4 retention", "Sessions completed per week"], a: 1, why: "Cumulative downloads only go up and don't show if users get value." },
      { q: "What does a cohort retention chart show?", o: ["Revenue by month", "How each group of users who joined together keeps using the product over time", "Server uptime", "Ad spend"], a: 1, why: "Cohorts reveal whether retention is improving for newer users." },
      { q: "A funnel goes 1,000 visits → 200 sign-ups → 50 activations. What's the sign-up-to-activation rate?", o: ["5%", "20%", "25%", "50%"], a: 2, why: "50 ÷ 200 = 25%." }
    ]
  },
  {
    id: "ai-basics", title: "AI and LLM foundations", level: "Beginner", track: "AI",
    questions: [
      { q: "What does an LLM fundamentally do?", o: ["Searches the internet", "Predicts the next token based on patterns in its training data", "Runs a database query", "Thinks like a human"], a: 1, why: "LLMs generate text one token at a time from learned patterns." },
      { q: "What is a 'hallucination'?", o: ["A visual bug", "A confident answer that isn't true or supported", "A slow response", "A security breach"], a: 1, why: "LLMs can produce fluent but wrong content, so important answers need grounding and checks." },
      { q: "What does RAG stand for?", o: ["Rapid AI Generation", "Retrieval-Augmented Generation", "Random Answer Generator", "Recursive Agent Graph"], a: 1, why: "RAG retrieves relevant documents and gives them to the model to ground its answer." },
      { q: "Why use RAG instead of only a bigger model?", o: ["It's always cheaper", "To answer from your own, up-to-date data and cite sources", "To make answers longer", "To avoid prompts"], a: 1, why: "RAG grounds answers in specific, current documents the model wasn't trained on." },
      { q: "What is a 'context window'?", o: ["The app's screen size", "How much text the model can consider at once", "The training period", "A browser tab"], a: 1, why: "Everything in the prompt plus the reply must fit in the context window." },
      { q: "What makes an AI 'agent' different from a chatbot?", o: ["It has a name", "It can plan and use tools to take actions towards a goal", "It's always voice-based", "It never makes mistakes"], a: 1, why: "Agents call tools (search, APIs, code) in a loop to complete tasks." },
      { q: "Which is the best way to evaluate an AI feature before launch?", o: ["Ask one colleague", "A test set of real examples with clear pass/fail criteria", "Check that it compiles", "Look at the logo"], a: 1, why: "Evals on representative examples catch regressions and measure quality." },
      { q: "What is a good guardrail for an AI that sends emails to customers?", o: ["Let it send anything", "Human approval before sending, at least at first", "Disable logging", "Use a longer prompt only"], a: 1, why: "Human-in-the-loop review limits the impact of mistakes on real customers." }
    ]
  },
  {
    id: "prompting", title: "Prompting and GenAI tools", level: "Beginner", track: "AI",
    questions: [
      { q: "Which prompt is likely to get the best result?", o: ["'Write something about our product'", "'Write a 120-word launch email for busy clinic owners about our booking app. Friendly tone. End with one call to action.'", "'Email'", "'Make it good'"], a: 1, why: "Specific audience, length, tone and goal give the model what it needs." },
      { q: "What is 'few-shot' prompting?", o: ["Using few words", "Giving the model a few examples of the input and output you want", "Asking three times", "Using a small model"], a: 1, why: "Examples show the pattern and format to follow." },
      { q: "You need the AI's answer in a table. What should you do?", o: ["Hope for the best", "Ask for the exact format, e.g. columns and order", "Use capital letters", "Ask for a long answer"], a: 1, why: "State the output format explicitly." },
      { q: "Best practice when using AI with company data?", o: ["Paste anything anywhere", "Follow your company's AI policy and use approved tools", "Share passwords with the AI", "Never use AI"], a: 1, why: "Approved tools and policies protect customer and company data." },
      { q: "Which tool is best for building a web app from a prompt without code?", o: ["A spreadsheet", "An AI app builder like Lovable", "A PDF reader", "A calculator"], a: 1, why: "AI app builders generate working apps with databases and login." },
      { q: "Which tools are built for automating workflows between apps?", o: ["Zapier, Make and n8n", "Photoshop", "Notepad", "Zoom"], a: 0, why: "They connect apps with triggers and actions, and can include AI steps." },
      { q: "The AI gives a statistic without a source. What should you do?", o: ["Publish it", "Verify it with a reliable source before using it", "Round it up", "Ask the AI to sound more confident"], a: 1, why: "Always check facts and numbers before relying on them." },
      { q: "What's a good way to improve a weak AI answer?", o: ["Start over with the same prompt", "Give feedback: say what's wrong and what you want instead", "Shout in capitals", "Give up"], a: 1, why: "Iterating with specific feedback is the fastest way to a good result." }
    ]
  }
];

const CHALLENGES = [
  { id: "upi-onboarding", track: "Product", level: "Beginner", time: "3–4 hours",
    title: "Fix first-time UPI payment drop-off",
    brief: "40% of new users of a UPI payments app don't complete their first payment within 7 days of sign-up. Find out why and propose a fix.",
    deliver: ["Problem statement and 3 likely causes", "Two solution options with trade-offs", "The metric you'd move, plus one guardrail", "A simple wireframe or flow"] },
  { id: "grocery-ai", track: "Product", level: "Intermediate", time: "4–5 hours",
    title: "Design an AI feature for a grocery app",
    brief: "Design an AI feature that helps users build a weekly grocery basket faster, while increasing average order value without hurting order frequency.",
    deliver: ["User problem and target segment", "How the AI works: inputs, model, guardrails", "Success metrics and an experiment plan", "Risks and how you'd handle them"] },
  { id: "tipping-metrics", track: "Product", level: "Intermediate", time: "2–3 hours",
    title: "Metrics for a food-delivery tipping feature",
    brief: "A food-delivery app adds in-app tipping for delivery partners. Define how you'd measure whether it's working for customers, partners and the business.",
    deliver: ["Goal and North Star", "Primary, secondary and guardrail metrics", "A dashboard sketch", "What would make you roll it back"] },
  { id: "clinic-bot-prd", track: "GenAI", level: "Beginner", time: "3 hours",
    title: "PRD for a clinic WhatsApp assistant",
    brief: "Write a one-page PRD for a WhatsApp assistant that answers patient questions and books appointments for a small clinic.",
    deliver: ["Users and top 5 questions to handle", "Conversation flow with handoff to staff", "What the bot must never do", "Launch checklist"] },
  { id: "rag-faq-bot", track: "Engineering", level: "Intermediate", time: "5–6 hours",
    title: "Build a RAG FAQ bot",
    brief: "Build a small app that answers questions from a set of PDFs or web pages, cites its sources and says 'I don't know' when the answer isn't there.",
    deliver: ["GitHub repo with a README", "10-question eval set with results", "Short demo video", "Notes on cost and latency"] },
  { id: "inbox-automation", track: "GenAI", level: "Beginner", time: "2–3 hours",
    title: "Automate an inbox with AI",
    brief: "Use n8n, Zapier or Make to read incoming emails, label them with AI (sales, support, other) and post a daily summary to Slack or email.",
    deliver: ["Screenshot of the workflow", "3 test emails and results", "How you'd handle mistakes", "Time saved per week (estimate)"] }
];

/* Practice with AI: interview-style questions by track and type. */
const PRACTICE = {
  "Product manager": {
    "Product sense": ["Design a product to help first-time voters in India find their polling booth.", "How would you improve Google Maps for two-wheeler riders?", "Design an app feature that helps people stick to a monthly budget.", "How would you improve the onboarding of a language-learning app?"],
    "Metrics": ["Instagram Reels watch time dropped 10% week over week. How would you investigate?", "What metrics would you track for a quick-commerce app's new 10-minute pharmacy delivery?", "How would you measure the success of a 'Save for later' button in an e-commerce app?"],
    "Strategy": ["Should a food-delivery company launch a grocery delivery business? How would you decide?", "A competitor launched a free version of your paid product. What do you do?", "How would you price a new AI writing feature for a SaaS tool?"],
    "AI product": ["Design an AI assistant for customer support at a bank. What guardrails would you add?", "How would you evaluate whether an AI summary feature is good enough to launch?", "Your AI feature's cost per user is higher than the revenue. What would you do?"],
    "Behavioural": ["Tell me about a time you disagreed with an engineer. What happened?", "Describe a product decision you made with incomplete data.", "Tell me about a launch that didn't go as planned."]
  },
  "Software engineer": {
    "System design": ["Design a URL shortener that handles 10,000 requests per second.", "Design a chat assistant that answers questions from a company's internal docs.", "Design a rate limiter for a public API."],
    "AI engineering": ["How would you reduce hallucinations in a RAG system?", "How would you test a prompt change before deploying it?", "How do you keep LLM costs under control at scale?"],
    "Coding concepts": ["Explain the difference between a process and a thread.", "When would you choose a SQL database over a NoSQL one?", "How does an index speed up a database query, and what does it cost?"],
    "Behavioural": ["Tell me about a production bug you fixed. How did you find it?", "Describe a time you improved a team's development process."]
  },
  "GenAI professional": {
    "Prompting": ["Write a prompt that turns meeting notes into action items with owners and dates.", "How would you get consistent, structured output from an AI model?"],
    "Use cases": ["Which three tasks in your current job would you automate with AI, and how?", "How would you introduce AI tools to a team that's sceptical?"],
    "Responsible AI": ["What data should never be pasted into a public AI tool, and why?", "How would you check an AI-generated report before sending it to a client?"]
  }
};
