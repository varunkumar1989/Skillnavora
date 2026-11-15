/* Paywall rules shared by the server (functions/_middleware.js and the payment functions) and the buy page.
   Which file or page belongs to which product, and whether a buyer's purchases unlock it.
   The price list itself is assets/products.json. */

// Files that are locked: documents, workbooks, datasets and code bundles.
export const FILE = /\.(pdf|xlsx|xls|csv|zip|pptx|docx|ipynb)$/i;

// Glob to regular expression: * stays inside one folder, ** crosses folders.
export function globToRe(glob) {
  let re = "";
  for (let i = 0; i < glob.length; i++) {
    const c = glob[i];
    if (c === "*" && glob[i + 1] === "*") { re += ".*"; i++; if (glob[i + 1] === "/") i++; }
    else if (c === "*") re += "[^/]*";
    else re += c.replace(/[.+?^${}()|[\]\\]/g, "\\$&");
  }
  return new RegExp("^" + re + "$", "i");
}
const cache = new Map();
const match = (path, globs) => (globs || []).some(g => { let r = cache.get(g); if (!r) { r = globToRe(g); cache.set(g, r); } return r.test(path); });

// "/handbook/A%20B.pdf" -> "handbook/A B.pdf"; "/ai-master-course-handbook" -> "ai-master-course-handbook.html"
export function normalise(pathname) {
  let p = String(pathname || "");
  try { p = decodeURIComponent(p); } catch {}
  p = p.replace(/^\/+/, "");
  if (p === "" || p.endsWith("/")) p += "index.html";
  else if (!/\.[a-z0-9]{2,5}$/i.test(p)) p += ".html";
  return p;
}

// What a path is: open (no lock), private (admins only), or locked (with the product that sells it).
export function classify(pathname, catalog) {
  const path = normalise(pathname);
  if (path.startsWith("assets/")) return { kind: "open", path };
  if (match(path, catalog.private)) return { kind: "private", path };
  const isFile = FILE.test(path);
  if (isFile && match(path, catalog.exempt)) return { kind: "open", path };
  if (!isFile && match(path, catalog.open_pages)) return { kind: "open", path };
  for (const p of catalog.products) {
    if ((isFile && match(path, p.files)) || (!isFile && match(path, p.pages))) {
      return { kind: "locked", path, product: p.id, single: isFile && /\.pdf$/i.test(path) && !match(path, catalog.bundle_only) };
    }
  }
  // Any other document is still locked; the all-access pass unlocks it.
  if (isFile) return { kind: "locked", path, product: "all-access", single: /\.pdf$/i.test(path) && !match(path, catalog.bundle_only) };
  return { kind: "open", path };
}

// Does this buyer (admin flag and list of purchased items) get the path?
export function allowed(info, ent) {
  if (!info || info.kind === "open") return true;
  if (!ent) return false;
  if (ent.admin) return true;
  if (info.kind === "private") return false;
  const owned = new Set(ent.products || []);
  return owned.has("all-access") || owned.has(info.product) || (info.single && owned.has("file:" + info.path));
}

// The price of an item: a product id, or "file:<path>" for a single PDF part. Returns null if it is not for sale.
export function priceOf(item, catalog) {
  if (typeof item !== "string" || item.length > 300 || item.includes("..")) return null;
  if (item.startsWith("file:")) {
    const info = classify("/" + item.slice(5), catalog);
    if (info.kind !== "locked" || !info.single) return null;
    return { item: "file:" + info.path, name: "Single PDF: " + info.path.split("/").pop().replace(/\.pdf$/i, "").replace(/[-_]+/g, " "),
             inr: catalog.single_pdf.inr, usd: catalog.single_pdf.usd };
  }
  const p = catalog.products.find(x => x.id === item);
  return p ? { item: p.id, name: p.name, inr: p.inr, usd: p.usd } : null;
}
