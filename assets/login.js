/* Log in / sign up: email one-time code (default), mobile OTP, Google, or password.
   After signing in, shows "What are you looking for?" (LMS, programs, admin). */
(async function () {
  const { client, $, notice, setupMessage, errText } = SN;
  const msg = $("auth-msg"), params = new URLSearchParams(location.search);
  const want = params.get("next") || "";
  const safeNext = /^(lms|admin)\.html(\?[^#<>"']*)?$/.test(want) ? want : "";
  const A = typeof AUTH !== "undefined" ? AUTH : {};
  const say = (k, t) => notice(msg, k, t);
  const steps = ["s-email", "s-code", "s-phone", "s-pcode", "s-pass", "s-forgot", "s-choose"];
  const show = id => { steps.forEach(s => { const el = $(s); if (el) el.hidden = s !== id; }); msg.hidden = true; $("methods").hidden = ["s-choose", "s-code", "s-pcode"].includes(id); };

  if (!client) { setupMessage(msg); $("auth-forms").hidden = true; return; }

  async function done() {
    if (safeNext) return location.replace(safeNext);
    const { data: admin } = await client.rpc("is_admin");
    $("go-admin").hidden = !admin;
    $("auth-title").textContent = "What are you looking for?"; $("auth-sub").hidden = true; $("switch").hidden = true;
    show("s-choose");
  }
  if (await SN.session()) return done();

  // Sign up vs log in only changes the wording and the name field.
  let signup = params.get("mode") === "signup";
  const mode = () => {
    $("auth-title").textContent = signup ? "Create your account" : "Log in to your account";
    $("auth-sub").textContent = signup ? "Enter your details and we'll email you a sign-in link." : "Enter your email and we'll send you a sign-in link.";
    $("name-row").hidden = !signup;
    $("switch").innerHTML = signup ? 'Already have an account? <button type="button" class="linkbtn" id="sw">Log in</button>' : 'Don\'t have an account? <button type="button" class="linkbtn" id="sw">Sign up</button>';
    $("sw").addEventListener("click", () => { signup = !signup; mode(); show("s-email"); });
  };
  mode(); show("s-email");

  const busy = (b, on, t) => { b.disabled = on; b.dataset.l = b.dataset.l || b.textContent; b.textContent = on ? (t || "Please wait…") : b.dataset.l; };
  const meta = () => signup && $("f-email").full_name.value.trim() ? { data: { full_name: $("f-email").full_name.value.trim() } } : {};

  // ---- Email one-time code ----
  let email = "";
  $("f-email").addEventListener("submit", async e => {
    e.preventDefault(); const f = e.target, b = f.querySelector("button[type=submit]");
    email = f.email.value.trim(); busy(b, true, "Sending…");
    const { error } = await client.auth.signInWithOtp({ email, options: { shouldCreateUser: true, emailRedirectTo: location.origin + "/lms.html", ...meta() } });
    busy(b, false);
    if (error) return say("error", errText(error));
    $("code-to").textContent = email; show("s-code"); $("f-code").token.focus();
  });
  $("f-code").addEventListener("submit", async e => {
    e.preventDefault(); const f = e.target, b = f.querySelector("button[type=submit]"); busy(b, true, "Verifying…");
    const { error } = await client.auth.verifyOtp({ email, token: f.token.value.trim(), type: "email" });
    busy(b, false);
    if (error) return say("error", /expired|invalid/i.test(error.message) ? "That code is wrong or has expired. Check it, or send a new one." : errText(error));
    done();
  });

  // ---- Mobile OTP ----
  let phone = "";
  if (A.phone) $("m-phone").hidden = false;
  $("f-phone").addEventListener("submit", async e => {
    e.preventDefault(); const f = e.target, b = f.querySelector("button[type=submit]");
    phone = f.cc.value + f.phone.value.replace(/\D/g, "");
    if (phone.replace(/\D/g, "").length < 10) return say("error", "Please enter a valid mobile number.");
    busy(b, true, "Sending OTP…");
    const { error } = await client.auth.signInWithOtp({ phone, options: meta() });
    busy(b, false);
    if (error) return say("error", errText(error));
    $("pcode-to").textContent = phone; show("s-pcode"); $("f-pcode").token.focus();
  });
  $("f-pcode").addEventListener("submit", async e => {
    e.preventDefault(); const f = e.target, b = f.querySelector("button[type=submit]"); busy(b, true, "Verifying…");
    const { error } = await client.auth.verifyOtp({ phone, token: f.token.value.trim(), type: "sms" });
    busy(b, false);
    if (error) return say("error", /expired|invalid/i.test(error.message) ? "That OTP is wrong or has expired. Try again." : errText(error));
    done();
  });

  // ---- Google ----
  if (A.google) {
    $("m-google").hidden = false;
    $("m-google").addEventListener("click", async () => {
      const { error } = await client.auth.signInWithOAuth({ provider: "google", options: { redirectTo: location.origin + "/" + (safeNext || "lms.html") } });
      if (error) say("error", errText(error));
    });
  }

  // ---- Password (optional) ----
  $("f-pass").addEventListener("submit", async e => {
    e.preventDefault(); const f = e.target, b = f.querySelector("button[type=submit]"); busy(b, true);
    const { error } = await client.auth.signInWithPassword({ email: f.email.value.trim(), password: f.password.value });
    busy(b, false);
    if (error) return say("error", errText(error));
    done();
  });
  $("f-forgot").addEventListener("submit", async e => {
    e.preventDefault(); const f = e.target, b = f.querySelector("button[type=submit]"); busy(b, true);
    const { error } = await client.auth.resetPasswordForEmail(f.email.value.trim(), { redirectTo: location.origin + "/reset.html" });
    busy(b, false);
    say(error ? "error" : "ok", error ? errText(error) : "If an account exists for that email, we've sent a link to reset your password.");
  });

  document.querySelectorAll("[data-step]").forEach(b => b.addEventListener("click", e => { e.preventDefault(); show(b.dataset.step); }));
})();
