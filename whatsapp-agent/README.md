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
