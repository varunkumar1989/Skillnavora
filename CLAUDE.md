# SkillNavora website (skillnavora.in)

Static site deployed by Cloudflare Pages from the `main` branch of this repository. Every push to `main` goes live in a few minutes.

## Owner's standing instruction: publish without waiting
The owner (Varun Kumar) has asked that changes go live automatically, without manual merging:
1. Work on the session's feature branch and commit there.
2. Regenerate pages with `python3 tools/gen_site.py` (never hand-edit generated HTML).
3. Test before publishing: no broken internal links, no file over 25 MB (Cloudflare Pages limit), and a headless-browser check of the pages you changed (menus, tabs, the resource gate, PDF links).
4. When the tests pass, merge into `main` and push it (`git fetch origin main && git merge origin/main`, then `git push origin HEAD:main`), and also push the feature branch. If the push is refused, give the owner the compare link and say what is blocking.
5. Report what went live and how it was tested.

## Content map
- `/data-science/` – Data Science & AI handbook (copied from varunkumar1989/data-science-and-ai `course/`, without `source/`, `print/` and files over 25 MB).
- `/handbooks/` – hub with three tabs (PM, Data Science & AI + DSA, GenAI Launchpad), interactive PM handbook in `handbooks/pm/` (its PDFs link to `/handbook/`), GenAI Launchpad PDF in `handbooks/genai/`.
- `/handbook/` – PM Master Handbook PDFs.
- Resources & AI tools page: four tabs built by `tools/restabs.py`.
- Handbook PDFs and files are behind the details gate (`data-science/assets/gate.js`), which records a `resource` lead via `/api/lead`.
