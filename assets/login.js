/* Log in with email + password (or Google for students); sign up with any method.
   After signing in, shows "What are you looking for?" (LMS, programs, admin). */
(async function () {
  const { client, $, notice, setupMessage, errText } = SN;
  const msg = $("auth-msg"), params = new URLSearchParams(location.search);
  const want = params.get("next") || "";
  const safeNext = /^(lms|admin)\.html(\?[^#<>"']*)?$/.test(want) ? want : "";
  const A = typeof AUTH !== "undefined" ? AUTH : {};
  const say = (k, t) => notice(msg, k, t);
  const adminMode = params.get("role") === "admin";
  let signup = !adminMode && params.get("mode") === "signup";
  const steps = ["s-email", "s-code", "s-phone", "s-pcode", "s-pass", "s-signpw", "s-setpw", "s-forgot", "s-choose"];
  const show = id => { steps.forEach(s => { const el = $(s); if (el) el.hidden = s !== id; }); msg.hidden = true; $("methods").hidden = adminMode || ["s-choose", "s-code", "s-pcode", "s-setpw", "s-forgot"].includes(id); paintMethods(id); };

  if (!client) { setupMessage(msg); $("auth-forms").hidden = true; return; }

  async function done() {
    if (safeNext) return location.replace(safeNext);
    const { data: admin } = await client.rpc("is_admin");
    $("go-admin").hidden = !admin;
    $("auth-title").textContent = "What are you looking for?"; $("auth-sub").hidden = true; $("switch").hidden = true;
    show("s-choose");
  }
  if (await SN.session()) return done();

  // Log in: email + password (students can also use Google). Admin: email + password only.
  // Sign up: every option (email + password, Google, email code, mobile, WhatsApp).
  function paintMethods(id) {
    const set = (el, on) => { const e = $(el); if (e) e.hidden = !on; };
    set("m-google", A.google && !adminMode);
    set("m-pass", false);
    set("m-signpw", signup && id !== "s-signpw");
    set("m-email", signup && id !== "s-email");
    set("m-phone", signup && A.phone && id !== "s-phone");
    set("m-wa", signup && A.whatsapp);
  }
  const mode = () => {
    if (adminMode) {
      $("auth-title").textContent = "Admin login";
      $("auth-sub").textContent = "For the SkillNavora team. Log in with your admin email and password.";
      $("switch").innerHTML = 'Not an admin? <a class="linkbtn" href="login.html">Student login</a>';
      return;
    }
    $("auth-title").textContent = signup ? "Create your account" : "Log in to your account";
    $("auth-sub").textContent = signup ? "Choose how you'd like to sign up." : "Log in with your email and password, or with Google.";
    $("name-row").hidden = !signup;
    $("switch").innerHTML = signup ? 'Already have an account? <button type="button" class="linkbtn" id="sw">Log in</button>' : 'Don\'t have an account? <button type="button" class="linkbtn" id="sw">Sign up</button>';
    $("sw").addEventListener("click", () => { signup = !signup; mode(); show(signup ? "s-signpw" : "s-pass"); });
  };
  mode(); show(signup ? "s-signpw" : "s-pass");

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
    afterSignup();
  });

  // ---- Mobile OTP, by SMS or WhatsApp (both are verified as type "sms") ----
  let phone = "", channel = "sms";
  const via = c => { channel = c; $("phone-go").textContent = c === "whatsapp" ? "Get OTP on WhatsApp" : "Get OTP"; delete $("phone-go").dataset.l; show("s-phone"); $("f-phone").phone.focus(); };
  $("m-phone").addEventListener("click", () => via("sms"));
  $("m-wa").addEventListener("click", () => via("whatsapp"));
  $("f-phone").addEventListener("submit", async e => {
    e.preventDefault(); const f = e.target, b = f.querySelector("button[type=submit]");
    phone = f.cc.value + f.phone.value.replace(/\D/g, "");
    if (phone.replace(/\D/g, "").length < 10) return say("error", "Please enter a valid mobile number.");
    busy(b, true, "Sending OTP…");
    const { error } = await client.auth.signInWithOtp({ phone, options: { ...meta(), channel } });
    busy(b, false);
    if (error) return say("error", errText(error));
    $("pcode-to").textContent = phone + (channel === "whatsapp" ? " on WhatsApp" : ""); show("s-pcode"); $("f-pcode").token.focus();
  });
  $("f-pcode").addEventListener("submit", async e => {
    e.preventDefault(); const f = e.target, b = f.querySelector("button[type=submit]"); busy(b, true, "Verifying…");
    const { error } = await client.auth.verifyOtp({ phone, token: f.token.value.trim(), type: "sms" });
    busy(b, false);
    if (error) return say("error", /expired|invalid/i.test(error.message) ? "That OTP is wrong or has expired. Try again." : errText(error));
    afterSignup();
  });

  // ---- Google ----
  if (A.google) {
    $("m-google").addEventListener("click", async () => {
      const { error } = await client.auth.signInWithOAuth({ provider: "google", options: { redirectTo: location.origin + "/" + (safeNext || "lms.html") } });
      if (error) say("error", errText(error));
    });
  }

  // After a code sign-up, offer to set a password for email + password login.
  function afterSignup() { if (!signup) return done(); $("auth-title").textContent = "Welcome to SkillNavora"; $("auth-sub").hidden = true; show("s-setpw"); $("f-setpw").password.focus(); }
  $("f-setpw").addEventListener("submit", async e => {
    e.preventDefault(); const f = e.target, b = f.querySelector("button[type=submit]"); busy(b, true);
    const { error } = await client.auth.updateUser({ password: f.password.value });
    busy(b, false);
    if (error) return say("error", errText(error));
    done();
  });
  $("setpw-skip").addEventListener("click", done);

  // ---- Sign up with email + password ----
  $("f-signpw").addEventListener("submit", async e => {
    e.preventDefault(); const f = e.target, b = f.querySelector("button[type=submit]");
    if (f.password.value.length < 8) return say("error", "Please use a password of at least 8 characters.");
    busy(b, true, "Creating account…");
    const { data, error } = await client.auth.signUp({ email: f.email.value.trim(), password: f.password.value,
      options: { data: { full_name: f.full_name.value.trim() }, emailRedirectTo: location.origin + "/lms.html" } });
    busy(b, false);
    if (error) return say("error", errText(error));
    if (data && data.session) return done();
    say("ok", "Account created. We've emailed you a link to confirm your address. Click it, then log in with your email and password.");
  });

  // ---- Password ----
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
