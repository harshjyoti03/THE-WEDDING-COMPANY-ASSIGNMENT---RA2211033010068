const apiCreate = async (name, email, password) => {
  const r = await fetch('/org/create', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ organization_name: name, email, password }) });
  const j = await r.json();
  return { ok: r.ok, data: j };
};
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('createOrgForm');
  const out = document.getElementById('createOrgResult');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('createOrgName').value.trim();
    const email = document.getElementById('createEmail').value.trim();
    const password = document.getElementById('createPassword').value;
    out.className = 'muted';
    out.textContent = 'Creating...';
    const r = await apiCreate(name, email, password);
    if (r.ok) {
      out.className = 'success';
      out.textContent = 'Organization created';
    } else {
      out.className = 'error';
      out.textContent = r.data.error || 'Failed';
    }
  });
});

