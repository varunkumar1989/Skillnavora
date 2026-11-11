# Course Overview: What Exactly Is "Grokbot"?

Before learning a platform, be certain which platform you are learning. The name "Grokbot" is used for at least three different things, and they are not interchangeable.

## 0.1 The three meanings of "Grokbot"

| Name as written | What it is | Who makes it | Is it what this course teaches? |
|---|---|---|---|
| **Grok Bot** (also written Grokbot) | An agent app: "a team of always-on agents" that "have their own computer, work inside tools and apps like you do, and keep working 24/7" **[Third-party, quoting xAI's announcement]** | xAI | **Yes, main subject** |
| **GrokBot crawler** | A web crawler user agent that third-party bot trackers attribute to xAI, used to fetch web content for Grok models **[Third-party, unverified]** | Attributed to xAI | Covered only in Module 10 (for site owners) |
| **pftq/GrokBot** | An unrelated Windows application on GitHub | An independent developer | No |

The course also teaches the **xAI Grok API** (developer access to Grok models, billed per token), because Grok Bot runs on Grok models and any custom product you build will use the API.

```
                ┌──────────────────────────────┐
                │        xAI Grok models        │  ← the "brains" (e.g. Grok 4.x)
                └──────────────┬───────────────┘
           ┌───────────────────┼────────────────────┐
           ▼                   ▼                    ▼
   ┌───────────────┐   ┌───────────────┐   ┌────────────────┐
   │ Grok chat app │   │   Grok Bot    │   │  xAI Grok API  │
   │ (grok.com, X) │   │ (agent app)   │   │ (developers)   │
   │ subscription  │   │ plan-based    │   │ pay per token  │
   └───────────────┘   └───────────────┘   └────────────────┘
      you chat           agents act for       you build your
                         you on schedules     own product
```

## 0.2 What is reported about Grok Bot

All points below are **[Third-party]**, from coverage found by web search on 11 November 2026. xAI's own announcement and documentation pages could not be opened from the environment used to write this course.

- **Announced:** 11 August 2026 by xAI.
- **What it does:** lets you create named AI agents that work inside apps and websites, connect to tools such as **Gmail** and **Slack**, learn a task by watching you do it, and run on **schedules**.
- **Model:** reported to run on **Grok 4.6** at launch.
- **Form:** desktop and mobile apps.
- **Usage and plans:** at least one reviewer reported that Grok Bot "seems to burn through its usage allowance quickly" and that it is "not very clear how much usage each price plan actually gives you". **Plan prices for Grok Bot could not be verified.**

## 0.3 How to confirm you have the right product

1. Open xAI's announcement: <https://x.ai/news/introducing-grok-bot>.
2. Open the Grok Bot documentation: <https://docs.x.ai/grok-bot/overview>.
3. Check that the app you install is published by xAI in the official app stores.
4. For the API, check that the base URL and keys come from xAI's console, not a reseller.
5. Do not confuse **Grok** (xAI) with **Groq** (a different company that sells fast inference for open models). The names differ by one letter.

> **Warning.** Many third-party sites copy each other. Where two sources disagree (for example on which Grok model is the current flagship, or whether all models share the same price), this course says so and does not pick a winner.

## 0.4 How the course is organised

Modules 1 and 2 give you the concepts. Module 3 (tokens) and Module 4 (pricing) teach the economics. Modules 5 to 8 teach you to build. Module 9 applies everything to business cases, and Module 10 makes it production-ready. The capstones put it all together.

## 0.5 Sources for this overview

- xAI announcement (official, not reachable when written): <https://x.ai/news/introducing-grok-bot>
- Grok Bot docs (official, not reachable when written): <https://docs.x.ai/grok-bot/overview.md>
- MindStudio explainer: <https://www.mindstudio.ai/blog/grokbot-xai-agent-app>
- No Code Founders guide: <https://www.nocodefounders.com/guides/grokbot-explained-simply>
- Zapier blog: <https://zapier.com/blog/grok-bot/>
- Flavio Copes, deep dive: <https://flaviocopes.com/grok-bot/>
- Createwith review: <https://www.createwith.com/blog/we-both-tried-grokbot-we-disagree>
- T2 Online news: <https://t2online.in/tech/tech-news/xai-launches-grok-bot-to-handle-tasks-across-apps-and-websites/2007230>
- Crawler listings: <https://botcrawl.com/bots/grokbot>, <https://promptwatch.com/bots/grokbot>
- Unrelated project: GitHub `pftq/GrokBot`
