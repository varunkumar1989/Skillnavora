// PM Master Handbook PDFs (/handbook/*) are for logged-in learners only.
// The LMS stores the learner's Supabase access token in the "sn_hb" cookie;
// we check it with Supabase before serving the file.
const SUPABASE_URL = "https://rnncabqtcxxivuyjwoja.supabase.co";
const SUPABASE_KEY = "sb_publishable_9sKPYxU3MHQfNT43n3d95A_bVLZi7BP"; // publishable key, safe to include

export async function onRequest(ctx) {
  const { request, env } = ctx;
  const url = new URL(request.url);
  const m = (request.headers.get("Cookie") || "").match(/(?:^|;\s*)sn_hb=([^;]+)/);
  if (m) {
    const base = env.SUPABASE_URL || SUPABASE_URL;
    const r = await fetch(base.replace(/\/$/, "") + "/auth/v1/user", {
      headers: { apikey: env.SUPABASE_KEY || SUPABASE_KEY, Authorization: "Bearer " + decodeURIComponent(m[1]) }
    }).catch(() => null);
    if (r && r.ok) {
      const res = await ctx.next();
      const h = new Headers(res.headers);
      h.set("Cache-Control", "private, no-store");
      h.set("X-Robots-Tag", "noindex");
      return new Response(res.body, { status: res.status, statusText: res.statusText, headers: h });
    }
  }
  return new Response(null, {
    status: 302,
    headers: { Location: url.origin + "/login.html?next=" + encodeURIComponent("lms.html?tab=handbook"), "Cache-Control": "no-store" }
  });
}
