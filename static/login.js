const apiLogin = async (email, password) => {
  const r = await fetch('/admin/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) });
  const j = await r.json();
  return { ok: r.ok, data: j };
};
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('loginForm');
  const out = document.getElementById('loginResult');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    out.className = 'muted';
    out.textContent = 'Signing in...';
    const r = await apiLogin(email, password);
    if (r.ok) {
      setToken(r.data.token);
      setOrg(r.data.organization.organization_name);
      setEmail(email);
      out.className = 'success';
      out.textContent = 'Signed in';
      window.location.href = '/dashboard';
    } else {
      out.className = 'error';
      out.textContent = r.data.error || 'Failed';
    }
    updateLoginStatus();
  });
});

