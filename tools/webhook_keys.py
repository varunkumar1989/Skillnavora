"""Plain-language section for non-coders: webhook addresses and keys. Shown at the top of web-automation.html."""
import html
E = html.escape

STEPS = [
    ("Pick the tool that will receive the message", "For example n8n, Make or Zapier. Each one has a step called Webhook (or Catch Hook). Add it to your automation and open it."),
    ("Copy the address it shows you", "The tool shows a web address. Copy the whole thing. Some tools show two: a test address for trying things and a live address for real work. Use the test one first."),
    ("Paste the address into the app that sends messages", "In the other app's settings, look for Webhook, Notifications or Integrations. Paste the address and save."),
    ("Send a test", "Trigger the event once, for example place a test order. The receiving tool should show the message. If it does not, check the address and try again."),
    ("Turn it on for real use", "Switch to the live address only after the test works, and keep the test address for changes later."),
]

KEY_RULES = [
    "Never paste a key into a chat, email, shared document, screenshot or public post.",
    "Store keys in the tool's secure settings, or in a password manager, not in a notes file.",
    "Give each tool its own key, so you can cancel one without breaking the others.",
    "Use the smallest access the tool needs. A tool that only reads orders does not need permission to delete them.",
    "Check who has access to your accounts and remove people who no longer work with you.",
]

LEAK = [
    "Cancel the key in the app that gave it to you, then create a new one. The old key stops working straight away.",
    "Put the new key into the tools that need it.",
    "Check the activity log for anything you did not expect, and remove any messages or actions you did not start.",
    "If customer data may have been exposed, follow your company's data-protection steps and tell the people affected.",
]

GLOSSARY = [
    ("Webhook (automatic message)", "An automatic message one app sends to another when something happens, such as a new order."),
    ("Webhook address", "The web address that receives those messages. Think of it as a letterbox: anyone who knows it can drop a message in, so keep it private."),
    ("Key", "A long secret code that proves an app is allowed to use a service, like a key card to a building. Anyone holding it can act as you."),
    ("Signing secret", "A secret code a service uses to stamp each message it sends. The receiving tool checks the stamp, so it knows the message really came from that service and was not faked."),
    ("Test address", "A safe address for trying things. Messages sent here do not start real actions."),
    ("Live address", "The address used for real work. Messages sent here do start real actions, so use it only after testing."),
]

FAQ = [
    ("Do I need to know how to code?", "No. Most tools have buttons for webhooks and keys. You copy, paste and test. The course's technical sections are for people who want to write code."),
    ("Is the webhook address the same as a password?", "Not exactly, but treat it as private. Anyone with the address can send messages to it, so do not share it publicly."),
    ("My key is in a shared document. What now?", "Treat it as leaked. Follow the steps above to cancel it and create a new one."),
    ("Why does the receiving tool say 'signature not valid'?", "The message did not carry the correct stamp. Check that the signing secret in the receiving tool matches the one in the sending service, with no extra spaces."),
]

def section():
    steps = "".join(f"<li><b>{E(t)}</b><br>{E(d)}</li>" for t, d in STEPS)
    rules = "".join(f"<li>{E(r)}</li>" for r in KEY_RULES)
    leak = "".join(f"<li>{E(r)}</li>" for r in LEAK)
    gloss = "".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td></tr>" for a, b in GLOSSARY)
    faq = "".join(f"<details class='card' style='padding:12px 16px;margin:8px 0'><summary style='cursor:pointer;font-weight:700'>{E(q)}</summary><p style='margin:8px 0 0'>{E(a)}</p></details>" for q, a in FAQ)
    return f"""<section id="wh-start" style="padding-top:8px"><div class="wrap">
<div class="card" style="border:2px solid #6C4CF5;padding:22px 24px;margin:0 0 26px">
<div class="kicker">Start here · no coding needed</div>
<h2 class="sec-h" style="font-size:26px;margin:6px 0 8px">Webhook addresses and keys, in plain words</h2>
<p class="sub" style="max-width:820px">A webhook is an automatic message from one app to another. Its address tells the message where to go. A key proves an app is allowed to use a service. This section explains both step by step, and the rest of the course goes deeper.</p>

<h3 style="margin:22px 0 8px">What is a webhook, in one picture?</h3>
<p style="max-width:820px">Think of a shop bell. When a customer comes in, the bell rings and the shopkeeper knows at once. A webhook is a bell between two apps: when something happens in one app (a new order, a payment, a form filled), it rings the other app straight away, so you do not have to keep checking by hand.</p>

<h3 style="margin:22px 0 8px">What is a webhook address?</h3>
<p style="max-width:820px">It is the address the message is sent to, like a letterbox address. It looks like a long web link. Anyone who knows it can send messages to it, so keep it to yourself and only paste it where it is needed.</p>

<h3 style="margin:22px 0 8px">How to set up a webhook (five steps)</h3>
<ol style="max-width:820px;line-height:1.6">{steps}</ol>

<h3 style="margin:22px 0 8px">What is a key?</h3>
<p style="max-width:820px">A key is a long secret code. It works like a key card to an office: it proves your app may enter. A key given to someone else lets them act as you, so treat it like a bank password.</p>

<h3 style="margin:22px 0 8px">What is a signing secret?</h3>
<p style="max-width:820px">Some services stamp every message with a secret code, like a wax seal. The receiving tool checks the stamp. If the stamp is missing or wrong, the tool should ignore the message, because it may have been faked. You copy the signing secret once from the service, and paste it into the receiving tool's settings.</p>

<h3 style="margin:22px 0 8px">Safety rules for keys and addresses</h3>
<ul style="max-width:820px;line-height:1.6">{rules}</ul>

<h3 style="margin:22px 0 8px">If a key or address leaks</h3>
<ol style="max-width:820px;line-height:1.6">{leak}</ol>

<h3 style="margin:22px 0 8px">Words you will see</h3>
<table style="width:100%;border-collapse:collapse;font-size:15px;max-width:820px"><tr><th style="text-align:left;border-bottom:1px solid #ddd;padding:8px">Word</th><th style="text-align:left;border-bottom:1px solid #ddd;padding:8px">What it means</th></tr>{gloss}</table>

<h3 style="margin:22px 0 8px">Common questions</h3>
{faq}
<p class="meta" style="margin-top:12px">Tools change their menus often. If a button name is different, look for the same idea: Webhook, Catch Hook, Integrations, or Secret.</p>
</div></div></section>"""
