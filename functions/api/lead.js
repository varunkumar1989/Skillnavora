// Saves a form submission (application, counselling, mentor, careers, contact) to
// Supabase and notifies the SkillNavora team by email and/or WhatsApp.
//
// Optional Cloudflare secrets (Pages → Settings → Variables and secrets):
//   RESEND_API_KEY, NOTIFY_EMAIL   email via resend.com (free plan; without a verified
//                                  domain it can only send to your own Resend login email)
//   CALLMEBOT_PHONE, CALLMEBOT_APIKEY  WhatsApp message to your own number via callmebot.com
//   WEB3FORMS_KEY                  email via web3forms.com (alternative to Resend)
const SUPABASE_URL = "https://rnncabqtcxxivuyjwoja.supabase.co";
const SUPABASE_KEY = "sb_publishable_9sKPYxU3MHQfNT43n3d95A_bVLZi7BP"; // publishable key, safe to include

const FIELDS = { kind: 20, course_id: 40, first_name: 80, last_name: 80, email: 200, phone: 20, linkedin: 300, experience: 40, role: 80, message: 2000, preferred_time: 80, source: 200 };
const BASE_KINDS = ["application", "counselling"];
const LABEL = { application: "Application", counselling: "Counselling call", mentor: "Mentor application", career: "Careers application", contact: "Contact form" };
const json = (o, status = 200) => new Response(JSON.stringify(o), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } });

export async function onRequestPost({ request, env }) {
  let body;
  try { body = await request.json(); } catch { return json({ ok: false, error: "bad_json" }, 400); }
  const row = {};
  for (const [k, max] of Object.entries(FIELDS)) {
    const v = body[k];
    if (v != null && v !== "") row[k] = String(v).slice(0, max).trim();
  }
  if (!row.first_name || !row.phone || !/^[0-9+ ()-]{7,20}$/.test(row.phone)) return json({ ok: false, error: "invalid" }, 400);
  if (row.email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(row.email)) delete row.email;
  if (row.course_id && !/^[a-z0-9-]{1,40}$/.test(row.course_id)) delete row.course_id;
  row.kind = LABEL[row.kind] ? row.kind : "application";

  // 1. Save to Supabase (falls back to a base kind if the database hasn't been updated yet)
  const base = (env.SUPABASE_URL || SUPABASE_URL).replace(/\/$/, ""), key = env.SUPABASE_KEY || SUPABASE_KEY;
  const insert = r => fetch(base + "/rest/v1/applications", { method: "POST",
    headers: { apikey: key, ...(key.startsWith("sb_") ? {} : { Authorization: "Bearer " + key }), "content-type": "application/json", prefer: "return=minimal" },
    body: JSON.stringify(r) }).then(x => x.ok).catch(() => false);
  let saved = await insert(row);
  if (!saved && !BASE_KINDS.includes(row.kind)) {
    saved = await insert({ ...row, kind: "counselling", message: ("[" + LABEL[row.kind] + "] " + (row.message || "")).slice(0, 2000) });
  }

  // 2. Notify the team
  const lines = [
    "New SkillNavora " + LABEL[row.kind].toLowerCase(),
    "Name: " + [row.first_name, row.last_name].filter(Boolean).join(" "),
    "Phone: " + row.phone,
    row.email && "Email: " + row.email,
    row.course_id && "Program: " + row.course_id,
    row.role && "Role: " + row.role,
    row.experience && "Experience: " + row.experience,
    row.linkedin && "LinkedIn: " + row.linkedin,
    row.preferred_time && "Preferred time: " + row.preferred_time,
    row.message && "Message: " + row.message,
    row.source && "Source: " + row.source
  ].filter(Boolean);
  const text = lines.join("\n"), subject = lines[0] + ": " + row.first_name;
  const jobs = [];
  if (env.RESEND_API_KEY && env.NOTIFY_EMAIL) jobs.push(fetch("https://api.resend.com/emails", { method: "POST",
    headers: { authorization: "Bearer " + env.RESEND_API_KEY, "content-type": "application/json" },
    body: JSON.stringify({ from: env.NOTIFY_FROM || "SkillNavora <onboarding@resend.dev>", to: env.NOTIFY_EMAIL.split(",").map(s => s.trim()), subject, text, reply_to: row.email || undefined }) }).then(r => r.ok));
  if (env.WEB3FORMS_KEY) jobs.push(fetch("https://api.web3forms.com/submit", { method: "POST",
    headers: { "content-type": "application/json", accept: "application/json" },
    body: JSON.stringify({ access_key: env.WEB3FORMS_KEY, subject, from_name: "SkillNavora website", message: text, replyto: row.email }) }).then(r => r.ok));
  if (env.CALLMEBOT_PHONE && env.CALLMEBOT_APIKEY) jobs.push(fetch("https://api.callmebot.com/whatsapp.php?phone=" + encodeURIComponent(env.CALLMEBOT_PHONE) +
    "&text=" + encodeURIComponent(text.slice(0, 1500)) + "&apikey=" + encodeURIComponent(env.CALLMEBOT_APIKEY)).then(r => r.ok));
  const sent = (await Promise.all(jobs.map(j => j.catch(() => false)))).filter(Boolean).length;

  return json({ ok: saved || sent > 0, saved, notified: sent });
}
