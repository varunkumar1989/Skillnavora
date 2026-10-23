/* Set a new password after clicking the reset link in the email. */
(async function () {
  const { client, $, notice, setupMessage, errText } = SN;
  const msg = $("auth-msg"), f = $("f-reset");
  if (!client) { setupMessage(msg); f.hidden = true; return; }
  // The reset link signs the user in for this one purpose; give it a moment to be read from the URL.
  await new Promise(r => setTimeout(r, 400));
  if (!(await SN.session())) {
    f.hidden = true;
    return notice(msg, "error", "This reset link has expired or was already used. Request a new one from the Log in page.");
  }
  f.addEventListener("submit", async e => {
    e.preventDefault();
    if (f.password.value.length < 8) return notice(msg, "error", "Please use a password of at least 8 characters.");
    if (f.password.value !== f.confirm.value) return notice(msg, "error", "The two passwords don't match.");
    const { error } = await client.auth.updateUser({ password: f.password.value });
    if (error) return notice(msg, "error", errText(error));
    notice(msg, "ok", "Password updated. Taking you to your dashboard…");
    setTimeout(() => location.replace("dashboard.html"), 1200);
  });
})();
