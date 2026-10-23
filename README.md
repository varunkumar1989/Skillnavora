# SkillNavora

Website and LMS for [skillnavora.in](https://www.skillnavora.in). Plain HTML, hosted free on Cloudflare Pages; logins and course data on Supabase. Every commit to `main` goes live in about a minute.

## Pages

| Menu | Page | File |
|---|---|---|
| Home | Hero, programs, career support, free tools, FAQs | `index.html` |
| Programs ▾ | All programs | `programs.html` |
| | AI-First Product Management | `program/ai-product-management.html` |
| | AI-First Software Engineering | `program/ai-software-engineering.html` |
| | GenAI Launchpad | `program/genai-launchpad.html` |
| Upskill for free ▾ | Quiz zone · Challenges · Practice with AI · Resources | `quiz.html`, `challenges.html`, `practice.html`, `resources.html` |
| LMS | Overview · My courses · My events · Submissions · Achievements · Profile | `lms.html` |
| (admins) | Admin panel | `admin.html` |
| Contact us | Contact | `contact.html` |
| Footer | Privacy, terms, refund policy, login | `privacy.html`, `terms.html`, `refund.html`, `login.html` |

## Edit almost everything in `assets/config.js`

- **`SITE`**: email, phone, WhatsApp, address, social links, counselling booking link, the announcement banner.
- **`AUTH`**: Supabase project URL and publishable key (see `supabase/README.md`), Google login on/off.
- **`COURSES`**: each program's name, cohort, start date, enrolment deadline (shows a countdown), fee, enrol/payment link, duration, who it's for, outcomes, curriculum modules, projects and tools.
- **`SUPPORT`**, **`FAQS`**, **`TESTIMONIALS`**: career support cards, FAQs and real reviews.

Quizzes, challenges and practice questions are in **`assets/content.js`**.

## Running the LMS

1. Set up Supabase once: [`supabase/README.md`](supabase/README.md).
2. A student creates an account (Log in → Create account).
3. In **Admin → Enrolments**, enrol them in a program after they pay.
4. After each class, add the recording and slides in **Admin → Course materials**. Only enrolled students can see them.
5. Schedule live sessions in **Admin → Events**; students register and rate them in **My events**.
6. Review submissions in **Admin → Submissions**; students see your feedback in their LMS.

## Cloudflare Pages settings

| Setting | Value |
|---|---|
| Production branch | `main` |
| Framework preset | None |
| Build command | *(leave empty)* |
| Build output directory | `/` *(leave empty)* |
