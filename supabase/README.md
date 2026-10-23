# Turning on student and admin logins

The login, dashboard and admin pages are already on the site. They show "coming soon" until you connect a free Supabase project. This takes about 15 minutes.

## 1. Create the project
1. Go to **supabase.com** → **Start your project** → sign in with GitHub.
2. **New project** → name `skillnavora` → set a database password (save it in a password manager) → region **South Asia (Mumbai)** → **Create**.

## 2. Create the tables and security rules
1. In the project, open **SQL Editor** → **New query**.
2. Paste everything from `supabase/schema.sql` → **Run**. You should see "Success. No rows returned".

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

## Good to know
- **Emails:** Supabase's built-in email sender is limited to a few emails an hour and is meant for testing. Before you open sign-ups to many students, set up your own sender under **Authentication → Emails → SMTP Settings** (for example a free Brevo or Resend account).
- **Free plan:** free projects pause after a week with no activity. Open the Supabase dashboard to resume, or upgrade when you have regular students.
- **Backups:** download student data any time from **Table Editor → profiles / submissions → Export to CSV**.
