/* Log in, sign up and forgot password. */
(async function () {
  const { client, $, notice, setupMessage, errText } = SN;
  const msg = $("auth-msg");
  const params = new URLSearchParams(location.search);

  if (!client) { setupMessage(msg); document.querySelectorAll(".auth-form, .tabs").forEach(f => f.hidden = true); return; }

  // Admins go to the admin page (unless they asked for their dashboard); everyone else to the dashboard.
  async function goHome() {
    const { data: admin } = await client.rpc("is_admin");
    location.replace(admin && params.get("next") !== "dashboard" ? "admin.html" : "dashboard.html");
  }

  if (await SN.session()) return goHome();

  // Tabs
  const show = name => {
    ["signin", "signup", "forgot"].forEach(n => { $("f-" + n).hidden = n !== name; const t = $("t-" + n); if (t) t.setAttribute("aria-selected", n === name); });
    notice(msg, "", "");
  };
  document.querySelectorAll("[data-show]").forEach(b => b.addEventListener("click", e => { e.preventDefault(); show(b.dataset.show); }));
  show(params.get("mode") === "signup" ? "signup" : "signin");

  const busy = (form, on) => { const b = form.querySelector("button[type=submit]"); b.disabled = on; b.dataset.label = b.dataset.label || b.textContent; b.textContent = on ? "Please wait…" : b.dataset.label; };

  $("f-signin").addEventListener("submit", async e => {
    e.preventDefault(); const f = e.target; busy(f, true);
    const { data, error } = await client.auth.signInWithPassword({ email: f.email.value.trim(), password: f.password.value });
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
      options: { data: { full_name: f.full_name.value.trim() }, emailRedirectTo: location.origin + "/dashboard.html" }
    });
    busy(f, false);
    if (error) return notice(msg, "error", errText(error));
    if (data.session) return location.replace("dashboard.html");
    f.reset();
    notice(msg, "ok", "Almost done! We've sent a confirmation link to your email. Click it to activate your account, then sign in.");
  });

  $("f-forgot").addEventListener("submit", async e => {
    e.preventDefault(); const f = e.target; busy(f, true);
    const { error } = await client.auth.resetPasswordForEmail(f.email.value.trim(), { redirectTo: location.origin + "/reset.html" });
    busy(f, false);
    if (error) return notice(msg, "error", errText(error));
    notice(msg, "ok", "If an account exists for that email, we've sent a link to reset your password.");
  });
})();
