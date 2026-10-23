# Turning on the LMS (student and admin logins)

The login, LMS and admin pages are already on the site. They show "coming soon" until you connect a free Supabase project. This takes about 15 minutes.

## 1. Create the project
1. Go to **supabase.com** → **Start your project** → sign in with GitHub.
2. **New project** → name `skillnavora` → set a database password (save it in a password manager) → region **South Asia (Mumbai)** → **Create**.

## 2. Create the tables and security rules
1. In the project, open **SQL Editor** → **New query**.
2. Paste everything from `supabase/schema.sql` → **Run**. You should see "Success. No rows returned". If `schema.sql` changes in a later update, run it again: it keeps your data.

## 3. Set the website address
**Authentication → URL Configuration**:
- **Site URL:** `https://www.skillnavora.in`
- **Redirect URLs:** add `https://www.skillnavora.in/**` and `https://skillnavora.pages.dev/**`

## 4. Connect the website
1. **Project Settings → API Keys** (or **API**): copy the **Project URL** and the **publishable** key (older projects call it **anon public**).
2. In GitHub, edit `assets/config.js` → paste them into `AUTH` → **Commit changes**.

Never paste the **secret** or **service_role** key anywhere on the website. The site refuses to use one, but it would still be visible to anyone who opens the file.

## 5. Make yourself the admin
1. On the website, open **Log in → Create account** and sign up with your email, then click the confirmation link in your inbox.
2. Back in Supabase **SQL Editor**, run (with your email):
   ```sql
   update public.profiles set role = 'admin' where email = 'varunebix@gmail.com';
   ```
3. Log in again: you'll land on the **Admin panel**. Add more admins from its **Admins** tab.

## Email one-time code (the default login)
The login page sends a 6-digit code by email. Supabase's default email sends a link instead, so add the code to the template once:
1. **Authentication → Emails → Templates → Magic link** (also **Confirm signup**).
2. Replace the body with, for example: `Your SkillNavora login code is <b>{{ .Token }}</b>. It expires in 1 hour.` → **Save**.

## Optional: mobile number + OTP
1. **Authentication → Sign In / Providers → Phone** → enable, and connect an SMS provider (Twilio, MessageBird, Vonage or Textlocal; each charges per SMS). For India, SMS senders also need DLT registration with your provider.
2. In `assets/config.js`, set `phone: true` in `AUTH`.

## Optional: "Continue with Google"
1. In Google Cloud Console, create an **OAuth client ID** (type: Web application). Add the redirect URL Supabase shows under **Authentication → Sign In / Providers → Google**.
2. Paste the client ID and secret into that Supabase Google provider and enable it. The Google secret goes only into Supabase, never into the website.
3. In `assets/config.js`, set `google: true` in `AUTH`.

## Good to know
- **Emails:** Supabase's built-in email sender is limited to a few emails an hour and is meant for testing. Before you open sign-ups to many students, set up your own sender under **Authentication → Emails → SMTP Settings** (for example a free Brevo or Resend account).
- **Free plan:** free projects pause after a week with no activity. Open the Supabase dashboard to resume, or upgrade when you have regular students.
- **Backups:** download student data any time from **Table Editor → profiles / submissions → Export to CSV**.

## AI chat assistant ("Ask AI" button)
The assistant answers visitors' questions from `assets/config.js` using Claude. Your API key stays on Cloudflare and is never shown to visitors.
1. Create an API key at **console.anthropic.com → API keys**, and set a monthly spend limit under **Billing → Limits** (for example ₹2,000).
2. In Cloudflare: **Workers & Pages → skillnavora → Settings → Variables and secrets → Add** → type **Secret**, name `ANTHROPIC_API_KEY`, paste the key → **Save**.
3. Same project: **Settings → Build → Build command** → `npm install` → **Save**, then **Deployments → Retry deployment** on the latest one.
4. Open the site and click **Ask AI**. Until the key is set, the assistant answers from your FAQs and offers WhatsApp and counselling.

It uses Claude Opus 5.5 at low effort. To spend less, add a second variable `CHAT_MODEL` = `claude-haiku-5-5`.
