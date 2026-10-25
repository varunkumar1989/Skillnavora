# SkillNavora

Website and LMS for [skillnavora.in](https://www.skillnavora.in). Plain HTML, hosted free on Cloudflare Pages; logins and course data on Supabase. Every commit to `main` goes live in about a minute.

## Pages

| Menu | Page | File |
|---|---|---|
| Home | Hero, programs, career support, free tools, FAQs | `index.html` |
| Programs ▾ | All programs | `programs.html` |
| | AI-First Product Management | `program/ai-product-management.html` |
| | AI-First Data Science | `program/ai-data-science.html` |
| | GenAI Launchpad | `program/genai-launchpad.html` |
| | For business | `business.html` |
| Upskill for free ▾ | Quiz zone · Challenges · Practice with AI · Resources | `quiz.html`, `challenges.html`, `practice.html`, `resources.html` |
| LMS | Overview · My courses · PM Handbook · My events · Submissions · Achievements · Profile | `lms.html` |
| (admins) | Admin panel | `admin.html` |
| Events · Job board · Reviews | Events, PM/AI/Data Science job board, reviews | `events.html`, `jobs.html`, `reviews.html` |
| Careers ▾ | Join our team · Become a mentor | `careers.html`, `mentor.html` |
| Enroll now | Application form | `apply.html` |
| Contact | Contact | `contact.html` |
| Footer | Privacy, terms, refund policy, login | `privacy.html`, `terms.html`, `refund.html`, `login.html` |

## Edit almost everything in `assets/config.js`

- **`SITE`**: email, phone, WhatsApp, address, social links, counselling booking link, the announcement banner.
- **`AUTH`**: Supabase project URL and publishable key (see `supabase/README.md`), Google login on/off.
- **`COURSES`**: each program's name, cohort, start date, enrolment deadline (shows a countdown), fee, enrol/payment link, duration, who it's for, outcomes, curriculum modules, projects and tools.
- **`TOPBAR`**: the announcement bar at the top of every page.
- **`AUDIENCE`**, **`MOAT`**, **`COMPARE`**, **`JOB_ASSIST`**: who it's for, what makes you different, the comparison table, and job assistance.
- **`MENTORS`**, **`TESTIMONIALS`**: real mentors and reviews. Their sections stay hidden until you add one.
- **`SUPPORT`**, **`FAQS`**, **`EVENTS`**, **`JOBS`**: career support cards, FAQs, public events and extra jobs.
- **`SITE.popupMinutes`**: when the "Not sure if this is for you?" pop-up appears (0 turns it off). **`SITE.chatbot`**: the Ask AI button.

## Campaign links
Add `?utm_source=instagram&utm_campaign=launch` (or linkedin, whatsapp, youtube…) to links in your posts and ads. Each application and counselling request records where the visitor came from; you'll see it in **Admin → Applications**.

Quizzes, challenges and practice questions are in **`assets/content.js`**.

## Running the LMS

1. Set up Supabase once: [`supabase/README.md`](supabase/README.md).
2. A student creates an account (Log in → Create account).
3. In **Admin → Enrolments**, enrol them in a program after they pay.
4. After each class, add the recording and slides in **Admin → Course materials**. Only enrolled students can see them.
5. Schedule live sessions in **Admin → Events**; students register and rate them in **My events**.
6. Review submissions in **Admin → Submissions**; students see your feedback in their LMS.

## Form notifications (email and WhatsApp)
Every form (apply, counselling, sign-up card, mentor, careers, contact, business) posts to `functions/api/lead.js`, which saves it to Supabase (Admin → Applications) and sends you a message. Add these in Cloudflare → Workers & Pages → skillnavora → Settings → Variables and secrets (type **Secret**), then redeploy:
- **Email (Resend, free):** `RESEND_API_KEY` and `NOTIFY_EMAIL` (the email you signed up to Resend with).
- **Email (Web3Forms, free, alternative):** `WEB3FORMS_KEY`.
- **WhatsApp (CallMeBot, free):** `CALLMEBOT_PHONE` (e.g. 919211315006) and `CALLMEBOT_APIKEY`.

## PM Master Handbook (login only)
- The LMS has a **PM Handbook** tab with the interactive handbook (a shared Claude artifact) and the PDFs in `handbook/`.
- `functions/handbook/_middleware.js` only serves `/handbook/*` to logged-in learners: the site stores the learner's Supabase login in a cookie, and the function checks it with Supabase before sending the PDF. Visitors who aren't logged in go to the login page.
- To update the PDFs, replace the files in `handbook/` (keep the same names) and push.

## Cloudflare Pages settings

| Setting | Value |
|---|---|
| Production branch | `main` |
| Framework preset | None |
| Build command | *(leave empty)* |
| Build output directory | `/` *(leave empty)* |
