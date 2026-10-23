# SkillNavora

Website for [skillnavora.in](https://www.skillnavora.in), by Varun Kumar. Plain HTML, hosted free on Cloudflare Pages. Every commit to `main` goes live in about a minute.

## Pages

| Page | File |
|---|---|
| Home | `index.html` |
| Programs (courses, prices, 12-week roadmap) | `programs.html` |
| Mentoring (booking) | `mentoring.html` |
| Free resources (handbook PDFs) | `resources.html` |
| Case studies | `case-studies.html` |
| Blog and posts | `blog.html`, `blog/*.html` |
| About | `about.html` |
| Contact | `contact.html` |
| Privacy policy, 404 | `privacy.html`, `404.html` |
| Log in, reset password | `login.html`, `reset.html` |
| Student dashboard | `dashboard.html` |
| Admin panel | `admin.html` |

## Change most things in one file: `assets/config.js`

- **`SITE`**: email, phone, WhatsApp, city, LinkedIn, Instagram, YouTube, booking link (Calendly or Cal.com), Web3Forms key.
- **`PROGRAMS`**: the course cards on the Programs page: name, price, what's included and the button link. Leave `price` empty to show "Ask for fees".
- **`TESTIMONIALS`**: real quotes from students. The section appears on Home and Mentoring once you add one.

Phone numbers work with or without `91`, and links with or without `https://`.

## Student and admin logins

Powered by Supabase (free). Follow [`supabase/README.md`](supabase/README.md) to switch them on: create a project, run `supabase/schema.sql`, and paste the project URL and publishable key into `AUTH` in `assets/config.js`.

## Change text on a page

Open the page's `.html` file, click the pencil icon, use Ctrl+F to find the words, edit them and commit.

## Add a blog post

Copy one of the files in `blog/`, rename it, change the title, description and text, then add a card for it in `blog.html` and a line in `sitemap.xml`.

## Logo

`assets/logo-mark.svg` is the compass icon (header, footer and browser tab). `assets/skillnavora-logo.svg` is the full logo with the wordmark. `assets/compass-original.png` is the original icon.

## Cloudflare Pages settings

| Setting | Value |
|---|---|
| Production branch | `main` |
| Framework preset | None |
| Build command | *(leave empty)* |
| Build output directory | `/` *(leave empty)* |
