/* Log in, create account, forgot password, and Google sign-in. */
(async function () {
  const { client, $, notice, setupMessage, errText } = SN;
  const msg = $("auth-msg");
  const params = new URLSearchParams(location.search);
  const want = params.get("next") || "";
  const safeNext = /^(lms|admin)\.html(\?[^#<>"']*)?$/.test(want) ? want : "";

  if (!client) { setupMessage(msg); document.querySelectorAll(".form,.seg,.gbtn,.or").forEach(f => f.hidden = true); return; }

  // Admins go to the admin panel unless they asked for a specific page.
  async function goHome() {
    if (safeNext) return location.replace(safeNext);
    const { data: admin } = await client.rpc("is_admin");
    location.replace(admin ? "admin.html" : "lms.html");
  }
  if (await SN.session()) return goHome();

  const g = $("google");
  if (typeof AUTH !== "undefined" && AUTH.google) {
    g.hidden = false; $("or").hidden = false;
    g.addEventListener("click", async () => {
      const { error } = await client.auth.signInWithOAuth({ provider: "google", options: { redirectTo: location.origin + "/" + (safeNext || "lms.html") } });
      if (error) notice(msg, "error", errText(error));
    });
  }

  const show = name => {
    ["signin", "signup", "forgot"].forEach(n => { $("f-" + n).hidden = n !== name; const t = $("t-" + n); if (t) t.setAttribute("aria-selected", n === name); });
    $("auth-title").textContent = name === "signup" ? "Create your account" : name === "forgot" ? "Reset your password" : "Welcome back";
    notice(msg, "", ""); msg.hidden = true;
  };
  document.querySelectorAll("[data-show]").forEach(b => b.addEventListener("click", e => { e.preventDefault(); show(b.dataset.show); }));
  show(params.get("mode") === "signup" ? "signup" : "signin");

  const busy = (form, on) => { const b = form.querySelector("button[type=submit]"); b.disabled = on; b.dataset.label = b.dataset.label || b.textContent; b.textContent = on ? "Please wait…" : b.dataset.label; };

  $("f-signin").addEventListener("submit", async e => {
    e.preventDefault(); const f = e.target; busy(f, true);
    const { error } = await client.auth.signInWithPassword({ email: f.email.value.trim(), password: f.password.value });
    busy(f, false);
    if (error) return notice(msg, "error", errText(error));
    goHome();
  });

  $("f-signup").addEventListener("submit", async e => {
    e.preventDefault(); const f = e.target;
    if (f.password.value.length < 8) return notice(msg, "error", "Please use a password of at least 8 characters.");
    busy(f, true);
    const { data, error } = await client.auth.signUp({
      email: f.email.value.trim(), password: f.password.value,
      options: { data: { full_name: f.full_name.value.trim() }, emailRedirectTo: location.origin + "/lms.html" }
    });
    busy(f, false);
    if (error) return notice(msg, "error", errText(error));
    if (data.session) return location.replace(safeNext || "lms.html");
    f.reset();
    notice(msg, "ok", "Almost done! We've sent a confirmation link to your email. Click it to activate your account.");
  });

  $("f-forgot").addEventListener("submit", async e => {
    e.preventDefault(); const f = e.target; busy(f, true);
    const { error } = await client.auth.resetPasswordForEmail(f.email.value.trim(), { redirectTo: location.origin + "/reset.html" });
    busy(f, false);
    if (error) return notice(msg, "error", errText(error));
    notice(msg, "ok", "If an account exists for that email, we've sent a link to reset your password.");
  });
})();
