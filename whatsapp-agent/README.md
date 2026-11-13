# WhatsApp agent knowledge base

`SkillNavora_WhatsApp_Agent_Knowledge.xlsx` is the source the WhatsApp agent answers from. It is generated from the website's own data, so it stays in step with the site.

## Rebuild after website changes
```
python3 whatsapp-agent/build_kb.py
```
Needs Python 3 with `openpyxl` (`pip install openpyxl`) and Node.js.

## Import into Google Sheets
1. Open Google Sheets, then File > Import > Upload, and choose the .xlsx file.
2. Choose "Replace spreadsheet" or "Insert new sheets", then Import data.

## Rules for the agent
- Read `START_HERE` first. Answer only from these tabs, with the source link.
- Yellow rows are marked CONFIRM. Do not quote them until the owner confirms.
- Never promise a job, placement or salary.

## Reply on WhatsApp or Messenger for free (no AI key)

The free workflow uses no AI model. The Code node (`n8n/match_answer.js`) finds the answer, or the page or PDF that covers the topic, and the send node replies.

```
WhatsApp Trigger ─► HTTP Request (GET https://www.skillnavora.in/assets/knowledge_qa.json) ─► Code (match_answer.js) ─► WhatsApp Business Cloud: Send message
```

### WhatsApp (Meta WhatsApp Business Cloud API: free for replies to customer messages)
1. Go to developers.facebook.com, choose **Create app**, pick **Business**, and add the **WhatsApp** product. Meta gives you a free test number. To go live, add your own number. It must not be registered in the normal WhatsApp app.
2. In n8n, add a **WhatsApp Trigger** node (keep the name "WhatsApp Trigger"). Create a credential with the app's ID and secret, and set the event to **messages**.
3. Add the **HTTP Request** node (GET the URL above).
4. Add a **Code** node. Paste `match_answer.js` and set the mode to "Run Once for All Items".
5. Add **WhatsApp Business Cloud → Send Message**:
   - Phone Number ID: from the Meta app
   - Recipient: `{{ $json.to }}`
   - Text: `{{ $json.reply }}`
   - Credential: an access token. Use a permanent System User token from Meta Business settings. Paste it only into the n8n credential, never into a chat.
6. Activate the workflow. Meta can only send messages to n8n if it has a public HTTPS address. n8n Cloud provides one. A self-hosted n8n needs a public URL.

### Facebook Messenger or Instagram DM (free)
1. In the same Meta app, add **Messenger** (or Instagram), then connect your Facebook Page and generate a **Page access token**.
2. In n8n, add a **Webhook** node named "Messenger Webhook" (POST). Add a second path for GET that responds with `{{ $json.query["hub.challenge"] }}` so Meta can verify it. Paste the webhook URL and your verify token into Meta. Subscribe to `messages`.
3. Connect HTTP Request, then Code (`match_answer.js`), then an **HTTP Request** to send:
   - POST `https://graph.facebook.com/v21.0/me/messages`
   - Header: `Authorization: Bearer <page token>` (store it in an n8n credential)
   - Body: `{"recipient":{"id":"{{ $json.to }}"},"messaging_type":"RESPONSE","message":{"text":"{{ $json.reply }}"}}`

Test locally: `node whatsapp-agent/n8n/test_match.js`.

## Telegram bot (free, about 10 minutes)
1. In Telegram, open **@BotFather** and send `/newbot`. Choose a name and a username ending in `bot`. BotFather replies with a **token**. Paste the token only into n8n, never into a chat.
2. In n8n, add a **Telegram Trigger** node (keep the name "Telegram Trigger"). Create a Telegram credential with the token and set Updates to `message`.
3. Add an **HTTP Request** node (GET https://www.skillnavora.in/assets/knowledge_qa.json).
4. Add a **Code** node. Paste in `match_answer.js` and set the mode to "Run Once for All Items".
5. Add a **Telegram → Send Message** node: Chat ID `{{ $json.to }}`, Text `{{ $json.reply }}`. Under Additional Fields, turn **Append n8n Attribution** off.
6. **Activate** the workflow. Your public link is `https://t.me/<your_bot_username>`. Telegram needs a public HTTPS address for n8n: n8n Cloud provides one.

## Instagram DMs and Facebook Messenger: import-ready workflow
File: `n8n/messenger_instagram_workflow.json`. In n8n, choose **Workflows → Import from File**. One workflow handles both Messenger and Instagram.

Before you start you need: a Facebook Page, an Instagram **Professional** account (Business or Creator) linked to that Page, and a Meta developer account.

1. **Meta app:** at developers.facebook.com, go to My Apps → Create app → Business. Add the **Messenger** product, then **Instagram** (choose "API setup with Facebook login").
2. **Page token:** in Messenger → Settings → Access tokens, add your Page and choose **Generate token**.
   - In n8n: open **Send reply**, then Credential → **Header Auth**.
   - Name: `Authorization`. Value: `Bearer <token>`.
   - Paste the token only into n8n.
3. **Webhook:** in n8n, open **Messenger Webhook**, copy the **Production URL**, and activate the workflow.
   - In Meta, under Messenger → Settings → Webhooks, paste the URL as the Callback URL.
   - Verify token: `skillnavora-verify` (change it in both places if you like).
   - Choose **Verify and save**, then subscribe the Page to `messages` and `messaging_postbacks`.
   - Do the same for Instagram (Webhooks → Instagram → `messages`).
4. **Test** by sending a DM from a different account (an admin or tester of the app). Until Meta approves the app, only people with a role in the app get replies.
5. **Go live:** in App Review, request `pages_messaging` (Messenger) and `instagram_manage_messages` (Instagram), and switch the app to **Live**.

The workflow ignores the Page's own messages and read receipts, so it never replies to itself. Replies are limited to 990 characters, within Instagram's 1,000-character limit.

## WhatsApp auto-reply: import-ready workflows
- `n8n/whatsapp_free_workflow.json`: WhatsApp Trigger → Get knowledge → Find answer → Send WhatsApp reply. Free, no AI.
- `n8n/whatsapp_ai_workflow.json`: the same, plus an AI step. When the knowledge file has no answer, it asks **Grok** (xAI) and answers only from your facts. A ready **Claude** node sits beside it; reconnect to it if you prefer Claude. If the AI call fails, the free fallback reply is sent.

Setup:
1. **Meta app:** at developers.facebook.com/apps, create an app with use case **Other**, type **Business**. Add **WhatsApp**. Under WhatsApp → API Setup, copy the **Phone number ID** and add your own phone as a test recipient.
2. **Import:** in n8n, choose Workflows → Import from File.
3. **WhatsApp Trigger credential:** the app's **App ID** and **App Secret** (App settings → Basic).
4. **Send WhatsApp reply:**
   - Credential: an access token plus your Business Account ID. Use a permanent System User token from Business settings.
   - Paste your Phone number ID in place of `PASTE_YOUR_PHONE_NUMBER_ID`.
5. **AI version only** (Header Auth credentials):
   - Grok: name `Authorization`, value `Bearer <xAI key>` (from console.x.ai). Check the model name.
   - Claude: name `x-api-key`, value `<Anthropic key>`.
   - Both APIs are paid per use.
6. **Activate** the workflow, then send a WhatsApp message to the test number.
