// Guards PDFs, workbooks, datasets and other handbook files. Runs before the file is served.
// Only active when the PDF_GATE setting is "on" (see functions/api/pdf-access.js). Nothing is blocked before that.
// While it is on, a visitor needs a valid 24-hour cookie, which they get after the owner approves their email.
import { checkToken, cookieFrom } from "./api/pdf-access.js";

const PROTECTED = /\.(pdf|xlsx|xls|csv|zip|pptx|docx|ipynb)$/i;

export async function onRequest(context) {
  const { request, env, next } = context;
  const url = new URL(request.url);
  if (env.PDF_GATE !== "on" || !PROTECTED.test(url.pathname) || url.pathname.startsWith("/assets/")) return next();
  // Fail closed: if the signing secret is missing, nobody gets the files.
  const email = env.PDF_SECRET ? await checkToken(cookieFrom(request), env.PDF_SECRET) : null;
  if (email) return next();
  const dest = new URL("/access.html", url);
  dest.searchParams.set("next", url.pathname);
  return Response.redirect(dest.toString(), 302);
}
