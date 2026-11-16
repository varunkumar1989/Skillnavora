"""Claude and free AI tools: a guide to running coding agents on free or open-source models.
Written for SkillNavora in original words. Inspired by a free public walkthrough video (credited on the page);
no transcript, prompt or code from that video is copied. Used by gen_site.py: BODY for claude-free-setups.html,
section_html() for the Master Freelancing page, directly under the "Make Money with AI" section."""
import html

E = lambda s: html.escape(str(s), quote=True)
VIDEO = "https://www.youtube.com/watch?v=HsgsYdV1XoQ"

CSS = """<style>
.cf-wrap{max-width:820px;margin-left:auto;margin-right:auto;padding-left:16px;padding-right:16px}
.cf-sec{margin-top:34px}.cf-sec h2{font-size:24px;margin:6px 0 10px}
.cf-sec h3{font-size:18px;margin:18px 0 6px}
.cf-box{border:1px solid var(--line);border-radius:14px;padding:16px 18px;background:var(--surface);margin-top:12px}
.cf-warn{border-left:4px solid #d97706;background:rgba(217,119,6,.08);border-radius:10px;padding:12px 14px;margin:14px 0}
.cf-steps{padding-left:22px;line-height:1.7}
.cf-steps li{margin:4px 0}
.cf-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px;margin-top:14px}
.cf-card{border:1px solid var(--line);border-radius:14px;padding:16px;background:var(--surface);display:flex;flex-direction:column;gap:6px;min-width:0}
.cf-card b{font-size:16px}.cf-card span{color:var(--mu);font-size:14px;line-height:1.5}
.cf-fig{margin:16px 0;text-align:center}.cf-fig img{max-width:100%;height:auto;border-radius:14px}
pre.cf-code{background:var(--surface-2,#f4f5f8);border-radius:10px;padding:12px;overflow-x:auto;font-size:13px}
</style>"""

BODY = CSS + """
<section style="padding-top:28px"><div class="wrap cf-wrap">
  <div class="kicker">Master Freelancing · Claude and AI tools</div>
  <h1 class="sec-h" style="margin:6px 0 10px">Use Claude-style coding agents for free</h1>
  <p class="meta">Coding agents such as Claude Code read your project, write code and run commands in your terminal. The agent is a tool; the model behind it does the thinking. This guide shows how to pair the tool with free or open-source models, what each option is good for, and where the limits and risks are.</p>
  <div class="cf-warn"><b>Read this first.</b> There is no unlimited, free access to the paid Claude models. Free tiers have daily or monthly limits, change often, and sometimes stop. Some providers forbid certain ways of connecting accounts. Check each provider's current terms, limits and billing page before you rely on it, and never trust a label in a menu over the usage or billing log.</div>
  <figure class="cf-fig"><img src="assets/cf/agent-engine.svg" alt="Diagram: a coding agent (the body) can use a local model, a free cloud model or a router as its engine" loading="lazy"><figcaption class="meta">The agent is the body; the model is the engine. You can swap the engine without changing how you work.</figcaption></figure>
  <p class="meta">This guide is original and written for SkillNavora. It was inspired by a free public walkthrough video on the same topic (<a href="%(video)s" target="_blank" rel="noopener">watch it on YouTube</a>). Its prompts and code are not copied here.</p>
</div></section>

<section class="cf-sec"><div class="wrap cf-wrap">
  <h2>Choose your setup</h2>
  <div class="cf-grid">
    <div class="cf-card"><b>1. Ollama (local, offline)</b><span>Models run on your laptop. Private and free, limited by your hardware. Best for privacy and offline work.</span></div>
    <div class="cf-card"><b>2. OpenRouter (cloud, free models)</b><span>One key for many models, including some free ones. Fast, but your prompts go to the provider. Daily limits apply.</span></div>
    <div class="cf-card"><b>3. OpenCode (open-source agent)</b><span>A terminal coding agent you can point at local or cloud models. Good when you want full control.</span></div>
    <div class="cf-card"><b>4. Omni Route (routing)</b><span>A router that tries several providers and switches when one runs out. Convenient, but needs careful terms checks.</span></div>
    <div class="cf-card"><b>5. Kilo Code in VS Code (daily driver)</b><span>An agent inside the free VS Code editor, with free models and your own provider keys.</span></div>
    <div class="cf-card"><b>6. Google Anti-Gravity</b><span>A free AI coding tool that can run commands for you. Useful for setup, but read every permission it asks for.</span></div>
  </div>
  <figure class="cf-fig"><img src="assets/cf/setups.svg" alt="Comparison table of setups by privacy, cost, offline use and daily limits" loading="lazy"><figcaption class="meta">A quick comparison. Check current terms and limits before you rely on any option.</figcaption></figure>
</div></section>

<section class="cf-sec"><div class="wrap cf-wrap">
  <h2>1. Ollama: run models on your own computer</h2>
  <p class="meta">Ollama downloads open-source models and runs them locally. Your files and prompts stay on your machine, and it keeps working with Wi-Fi off once a model is downloaded.</p>
  <div class="cf-box"><h3>Set it up</h3>
    <ol class="cf-steps">
      <li>Download Ollama from its official site (Mac, Linux or Windows) and install it.</li>
      <li>Open its settings and set the <b>context length</b> higher (for example 32K or 64K). Context is how much of your project the model can hold at once; too small and it loses track.</li>
      <li>Pick a small model first to test, and send it a short message. The first message downloads the model.</li>
      <li>Check your hardware before choosing a bigger model: a graphics card with more memory and more RAM runs larger models. Ask an AI assistant to recommend a model for your hardware, then confirm the model is still current.</li>
    </ol>
  </div>
  <figure class="cf-fig"><img src="assets/cf/local-offline.svg" alt="Laptop running a model with Wi-Fi switched off" loading="lazy"><figcaption class="meta">Once a model is on your laptop, it runs without internet.</figcaption></figure>
  <p class="meta"><b>Good for:</b> private code, offline work, unlimited use within your hardware. <b>Limit:</b> smaller models are less capable than the best hosted models.</p>
</div></section>

<section class="cf-sec"><div class="wrap cf-wrap">
  <h2>2. OpenRouter: free cloud models through one key</h2>
  <p class="meta">OpenRouter gives you one API key for many providers' models. Some are free to use within limits.</p>
  <div class="cf-box"><h3>Safe way to start</h3>
    <ol class="cf-steps">
      <li>Create an account and an API key. Give the key a name and an expiry date.</li>
      <li>In the model list, filter for free models before you choose one. Free models change, so check the list each time.</li>
      <li>Set a spending limit on your account, even if you only use free models.</li>
      <li>Store the key in a password manager. Never paste it into a chat, a document or a public file.</li>
      <li>After testing, open the activity log on the OpenRouter site. It shows which model actually answered each request and what it cost. Trust that log over any label in an app.</li>
    </ol>
  </div>
  <p class="meta"><b>Limits:</b> free accounts have per-minute and per-day request caps. A coding agent can send many requests for one task, so a daily cap can run out quickly. <b>Privacy:</b> prompts and files are sent to the provider, so keep client or confidential code on local models.</p>
</div></section>

<section class="cf-sec"><div class="wrap cf-wrap">
  <h2>3. Claude Code with a different model behind it</h2>
  <p class="meta">Claude Code is Anthropic's terminal coding tool. Whether it can use a non-Anthropic model depends on Anthropic's current documentation and on the provider you connect. Follow the official instructions for both, and do not connect an account in a way its provider forbids.</p>
  <div class="cf-warn">Anything a guide says about making a paid model free should be checked against the billing page. A model's name in a menu does not prove which model is answering.</div>
</div></section>

<section class="cf-sec"><div class="wrap cf-wrap">
  <h2>4. OpenCode: an open-source terminal agent</h2>
  <p class="meta">OpenCode is an open-source coding agent you run in the terminal. It can work with models you run locally through Ollama, or with cloud providers you connect yourself. It is a good way to learn how coding agents work, because you choose each model and see each step.</p>
  <p class="meta">Install it from its official project page, read its current setup guide, and start with a local model so nothing leaves your computer.</p>
</div></section>

<section class="cf-sec"><div class="wrap cf-wrap">
  <h2>5. Omni Route: one router, several providers</h2>
  <p class="meta">A router such as Omni Route sends each request to one of several providers, and moves to the next when one is out of quota. It can save you from hitting a single limit in the middle of a task.</p>
  <div class="cf-warn"><b>Check terms before you connect anything.</b> Some free services do not allow their accounts to be used through third-party routers. Connect only the providers whose terms allow it, and use your own keys.</div>
  <figure class="cf-fig"><img src="assets/cf/fallback.svg" alt="Router sending a request to provider 1 (quota used up) and then provider 2 (answers)" loading="lazy"><figcaption class="meta">When one provider is out of quota, the router moves to the next.</figcaption></figure>
  <p class="meta">Keep the router's own key in a password manager. Review what each connected provider receives, because routing means your prompts can reach more than one company.</p>
</div></section>

<section class="cf-sec"><div class="wrap cf-wrap">
  <h2>6. Kilo Code inside VS Code: the daily driver</h2>
  <p class="meta">If you want to code every day without managing a terminal, install VS Code (free), add the Kilo Code extension, and sign in. It comes with some free models, and you can add your own provider keys. Models in its list change, so check which ones are free before a long session.</p>
  <ol class="cf-steps">
    <li>Open a folder for your project and trust it.</li>
    <li>Ask for a small, clear piece of work first, such as one screen or one function.</li>
    <li>Review every change before you accept it, and run the code yourself.</li>
    <li>If a model runs out of quota mid-task, switch to another model in the same chat.</li>
  </ol>
</div></section>

<section class="cf-sec"><div class="wrap cf-wrap">
  <h2>7. Google Anti-Gravity: let an AI do the setup</h2>
  <p class="meta">Some AI coding tools can run terminal commands for you, which is useful for installing models and tools. Describe the job in one clear sentence, then read each permission prompt before you allow it. Google's terms for its free tools apply, so check them.</p>
</div></section>

<section class="cf-sec"><div class="wrap cf-wrap">
  <h2>Rules that protect you</h2>
  <figure class="cf-fig"><img src="assets/cf/safety.svg" alt="Six safety rules for free AI coding setups" loading="lazy"></figure>
  <div class="cf-box">
    <ul class="cf-steps">
      <li><b>Nothing is unlimited.</b> Plan for daily caps, and keep a paid option ready for deadlines.</li>
      <li><b>Free is not private.</b> Hosted providers may store or use prompts. Keep client, personal or confidential code on local models.</li>
      <li><b>Check terms.</b> Some connections are not allowed by the provider. Your account, your responsibility.</li>
      <li><b>Keys are passwords.</b> Store them in a password manager, use expiry dates, and rotate any key you have pasted anywhere public.</li>
      <li><b>Check the bill, not the label.</b> The usage or billing page tells you what you actually paid.</li>
      <li><b>Expect errors.</b> Copy the error message, ask the agent to explain it, and fix one thing at a time.</li>
    </ul>
  </div>
</div></section>

<section class="cf-sec"><div class="wrap cf-wrap">
  <h2>Learn the thinking behind the tools</h2>
  <p class="meta">The tools change every few months. These skills last: how context works, how to write a clear task, how to review AI-written code, and how to test it.</p>
  <p class="meta">Study them on SkillNavora: <a href="ai-academy.html">AI Academy</a>, the <a href="data-science/index.html">free lessons</a>, and the <a href="vaitis.html">Vaitis AI library</a> for tools and step-by-step guides.</p>
  <p class="meta">Credit: the idea for this guide came from <a href="%(video)s" target="_blank" rel="noopener">a free walkthrough video</a>. This page is an independent guide and is not affiliated with any tool or provider it mentions.</p>
</div></section>
""" % {"video": VIDEO}


def section_html():
    """The complete guide, shown under the "Make Money with AI" section on Master Freelancing."""
    inner = BODY.replace('<h1 class="sec-h"', '<h2 class="sec-h"').replace('</h1>', '</h2>')
    return ('<section style="padding-top:24px"><div class="wrap cf-wrap"><h2 class="sec-h" style="margin:0 0 6px">Claude and AI tools: free setups</h2>'
            '<p class="meta" style="max-width:74ch">The complete guide: run coding agents with free or open-source models, with the limits and safety rules for each option. Also on its own page: <a href="claude-free-setups.html">Free Claude and AI coding setups</a>.</p></div></section>'
            + inner)
