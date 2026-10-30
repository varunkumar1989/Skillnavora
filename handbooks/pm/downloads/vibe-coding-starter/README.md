# Fee-Clear Cart — vibe-coding starter (Module 11 project)

A tiny static web prototype that tests one hypothesis: *showing the full estimated total in the cart reduces checkout surprise.*

* **Fictional data**; the delivery-fee “service” is simulated in `app.js`; **no real payments**.
* Open `index.html` directly in a browser — no build step, no server, no API keys.
* Choose “Simulate fee-service failure” to see the honest fallback (“Estimate unavailable” + Retry) instead of an invented number.

## Run locally
Double-click `index.html`, or from this folder:

```bash
python -m http.server 8000
```

then open http://localhost:8000.

## Deploy (GitHub Pages, free for public repositories)
1. Create a new **public** GitHub repository (it contains only dummy data and no secrets).
2. Upload these four files (or `git push` them).
3. Repository **Settings → Pages → Build and deployment → Deploy from a branch**, choose `main` and `/ (root)`, Save.
4. After a minute, GitHub shows the live URL (`https://<user>.github.io/<repo>/`).

## Test checklist
- [ ] Add/remove items; totals update.
- [ ] Change delivery area; fee and total refresh.
- [ ] Simulated failure shows “Estimate unavailable”, Pay is disabled, Retry works.
- [ ] Keyboard only: every control reachable and visibly focused.
- [ ] Reload: cart persists (localStorage); private window: still works without storage.
- [ ] Mobile width (375 px): no horizontal scroll; buttons ≥ 44 px tall.
