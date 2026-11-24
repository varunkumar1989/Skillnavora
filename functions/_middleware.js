// Locks paid files and interactive handbooks. Runs before every request.
//
// PAYWALL = "on" (Cloudflare setting): every PDF, workbook, dataset, code bundle and interactive handbook listed in
//   assets/products.json needs a purchase that covers it (or an admin account). Visitors without one are sent to
//   buy.html, which shows the price and the checkout. The pass is a signed cookie set by /api/pdf-access.
// PDF_GATE = "on" (older mode, only when PAYWALL is off): any email the owner approved gets every file.
// Neither on: nothing is blocked.
// Fails closed: if PDF_SECRET is missing while a lock is on, nobody but the site itself gets the files.
import { checkToken, cookieFrom, passFrom } from "./api/pdf-access.js";
import { classify, allowed } from "../assets/paywall-core.js";
import catalog from "../assets/products.json";

const MEMBERS = /^\/members(\.html)?$/;
const PROTECTED = /\.(pdf|xlsx|xls|csv|zip|pptx|docx|ipynb)$/i;

// Tells the page's script (assets/gate.js) that the paywall is on, so it checks access before opening a file
// instead of showing the free details form. The flag grants nothing: every file is still checked here.
function flagPaywall(res) {
  if (!(res.headers.get("content-type") || "").includes("text/html")) return res;
  const out = new Response(res.body, res);
  out.headers.append("set-cookie", "sn_pw=1; Path=/; Max-Age=3600; Secure; SameSite=Lax");
  return out;
}

// Files in the repository that are not part of the website: build scripts, bot and database files, research,
// project notes and source code. They answer "not found" so they cannot be downloaded from the live site.
const PRIVATE_DIR = /^\/(tools|whatsapp-agent|research|supabase|learning-coach|functions|Grokbot-Mastery-Course|AI-Models-and-Agents-Guide)\//i;   // the folder only: /tools (the Tool tutorials page) stays public
const PRIVATE_FILE = /^\/(CLAUDE\.md|AGENTS\.md|README\.md|wrangler\.toml|netlify\.toml|\.gitignore|\.dev\.vars|_headers|_redirects)$/i;
const SOURCE_EXT = /\.(py|pyc|sh|mjs|toml|sql)$/i;
const isPrivate = p => {
  let path = p;
  try { path = decodeURIComponent(p); } catch {}
  if (PRIVATE_DIR.test(path) || PRIVATE_FILE.test(path) || SOURCE_EXT.test(path)) return true;
  return /\.md$/i.test(path) && !/\/downloads\//i.test(path);   // .md templates under downloads/ are public on purpose
};

async function notFound(env, url) {
  try {
    const page = await env.ASSETS.fetch(new URL("/404.html", url));
    return new Response(page.body, { status: 404, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" } });
  } catch {
    return new Response("Not found", { status: 404, headers: { "content-type": "text/plain; charset=utf-8", "cache-control": "no-store" } });
  }
}

export async function onRequest(context) {
  const { request, env, next } = context;
  const url = new URL(request.url);
  if (isPrivate(url.pathname)) return notFound(env, url);
  if (url.pathname.startsWith("/api/") || url.pathname.startsWith("/assets/")) return next();

  // Members library: always locked (whatever the PAYWALL setting). Admins, emails the owner approved and all-access
  // buyers get in; everyone else is asked to sign in and request access. Fails closed without PDF_SECRET.
  if (MEMBERS.test(url.pathname)) {
    const pass = await passFrom(request, env);
    if (pass && (pass.a || (pass.p || []).includes("all-access"))) {
      const res = await next(); const out = new Response(res.body, res); out.headers.set("cache-control", "private, no-store"); return out;
    }
    const dest = new URL("/access.html", url); dest.searchParams.set("next", "/members.html");
    return Response.redirect(dest.toString(), 302);
  }

  if (env.PAYWALL === "on") {
    const info = classify(url.pathname, catalog);
    if (info.kind === "open") return flagPaywall(await next());
    const pass = await passFrom(request, env);
    if (allowed(info, pass ? { admin: !!pass.a, products: pass.p || [] } : null)) {
      const res = await next();
      // Paid content must not be stored by shared caches.
      const out = new Response(res.body, res);
      out.headers.set("cache-control", "private, no-store");
      return out;
    }
    const dest = new URL("/buy.html", url);
    dest.searchParams.set("for", url.pathname);
    return Response.redirect(dest.toString(), 302);
  }

  if (env.PDF_GATE !== "on" || !PROTECTED.test(url.pathname)) return next();
  const email = env.PDF_SECRET ? await checkToken(cookieFrom(request), env.PDF_SECRET) : null;
  if (email) return next();
  const dest = new URL("/access.html", url);
  dest.searchParams.set("next", url.pathname);
  return Response.redirect(dest.toString(), 302);
}
