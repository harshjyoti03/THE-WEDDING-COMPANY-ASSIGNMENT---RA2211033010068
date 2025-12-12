const apiCall = async (path, method, body, auth=false) => {
  const headers = { 'Content-Type': 'application/json' };
  if (auth) {
    const t = getToken();
    if (t) headers['Authorization'] = `Bearer ${t}`;
  }
  const r = await fetch(path, { method, headers, body: body ? JSON.stringify(body) : undefined });
  const j = await r.json();
  return { ok: r.ok, data: j };
};
document.addEventListener('DOMContentLoaded', () => {
  requireAuth();
  const org = getOrg();
  const getInput = document.getElementById('getOrgName');
  if (org && getInput) getInput.value = org;
  const updEmail = document.getElementById('updateEmail');
  if (updEmail) updEmail.value = getEmail() || '';
  const delInput = document.getElementById('deleteOrgName');
  if (org && delInput) delInput.value = org;
  const getForm = document.getElementById('getOrgForm');
  const getOut = document.getElementById('getOrgResult');
  getForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('getOrgName').value.trim();
    getOut.className = 'muted';
    getOut.textContent = 'Fetching...';
    const r = await fetch(`/org/get?organization_name=${encodeURIComponent(name)}`);
    const j = await r.json();
    if (r.ok) {
      getOut.className = 'success';
      getOut.textContent = JSON.stringify(j.organization, null, 2);
    } else {
      getOut.className = 'error';
      getOut.textContent = j.error || 'Failed';
    }
  });
  const updForm = document.getElementById('updateOrgForm');
  const updOut = document.getElementById('updateOrgResult');
  updForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('updateOrgName').value.trim();
    const email = document.getElementById('updateEmail').value.trim();
    const password = document.getElementById('updatePassword').value;
    updOut.className = 'muted';
    updOut.textContent = 'Updating...';
    const r = await apiCall('/org/update', 'PUT', { organization_name: name, email, password });
    if (r.ok) {
      updOut.className = 'success';
      updOut.textContent = 'Organization updated';
      setOrg(r.data.organization.organization_name);
    } else {
      updOut.className = 'error';
      updOut.textContent = r.data.error || 'Failed';
    }
    updateLoginStatus();
  });
  const delForm = document.getElementById('deleteOrgForm');
  const delOut = document.getElementById('deleteOrgResult');
  delForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('deleteOrgName').value.trim();
    delOut.className = 'muted';
    delOut.textContent = 'Deleting...';
    const r = await apiCall('/org/delete', 'DELETE', { organization_name: name }, true);
    if (r.ok) {
      delOut.className = 'success';
      delOut.textContent = 'Organization deleted';
      clearToken();
      localStorage.removeItem('org_name');
      localStorage.removeItem('email');
      updateLoginStatus();
      window.location.href = '/login';
    } else {
      delOut.className = 'error';
      delOut.textContent = r.data.error || 'Failed';
    }
  });
});

