const apiCall = async (path, method, body, requireAuth=false) => {
  const headers = { 'Content-Type': 'application/json' };
  if (requireAuth) {
    const t = localStorage.getItem('token');
    if (t) headers['Authorization'] = `Bearer ${t}`;
  }
  const res = await fetch(path, { method, headers, body: body ? JSON.stringify(body) : undefined });
  const txt = await res.text();
  let data;
  try { data = JSON.parse(txt); } catch { data = { raw: txt }; }
  return { ok: res.ok, status: res.status, data };
};

const setStatus = (el, msg, ok) => {
  el.className = ok ? 'success' : 'error';
  el.textContent = msg;
};

const pretty = (obj) => JSON.stringify(obj, null, 2);

const loginStatus = document.getElementById('loginStatus');
const refreshLoginStatus = () => {
  const token = localStorage.getItem('token');
  const org = localStorage.getItem('org_name');
  const email = localStorage.getItem('email');
  if (token && org) loginStatus.textContent = `Logged in as ${email} · Org: ${org}`;
  else loginStatus.textContent = 'Not logged in';
};

refreshLoginStatus();

document.getElementById('createOrgForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('createOrgName').value.trim();
  const email = document.getElementById('createEmail').value.trim();
  const password = document.getElementById('createPassword').value;
  const out = document.getElementById('createOrgResult');
  out.className = 'muted';
  out.textContent = 'Creating...';
  const r = await apiCall('/org/create', 'POST', { organization_name: name, email, password });
  if (r.ok) {
    out.className = 'success';
    out.textContent = 'Organization created';
  } else {
    out.className = 'error';
    out.textContent = r.data.error || 'Failed';
  }
});

document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = document.getElementById('loginEmail').value.trim();
  const password = document.getElementById('loginPassword').value;
  const out = document.getElementById('loginResult');
  out.className = 'muted';
  out.textContent = 'Signing in...';
  const r = await apiCall('/admin/login', 'POST', { email, password });
  if (r.ok) {
    localStorage.setItem('token', r.data.token);
    localStorage.setItem('org_name', r.data.organization.organization_name);
    localStorage.setItem('email', email);
    out.className = 'success';
    out.textContent = 'Signed in';
    document.getElementById('updateEmail').value = email;
  } else {
    out.className = 'error';
    out.textContent = r.data.error || 'Failed';
  }
  refreshLoginStatus();
});

document.getElementById('getOrgForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('getOrgName').value.trim();
  const out = document.getElementById('getOrgResult');
  out.className = 'muted';
  out.textContent = 'Fetching...';
  const r = await fetch(`/org/get?organization_name=${encodeURIComponent(name)}`);
  const data = await r.json();
  if (r.ok) {
    out.className = 'success';
    out.textContent = pretty(data.organization);
  } else {
    out.className = 'error';
    out.textContent = data.error || 'Failed';
  }
});

document.getElementById('updateOrgForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('updateOrgName').value.trim();
  const email = document.getElementById('updateEmail').value.trim();
  const password = document.getElementById('updatePassword').value;
  const out = document.getElementById('updateOrgResult');
  out.className = 'muted';
  out.textContent = 'Updating...';
  const r = await apiCall('/org/update', 'PUT', { organization_name: name, email, password });
  if (r.ok) {
    out.className = 'success';
    out.textContent = 'Organization updated';
    localStorage.setItem('org_name', r.data.organization.organization_name);
    refreshLoginStatus();
  } else {
    out.className = 'error';
    out.textContent = r.data.error || 'Failed';
  }
});

document.getElementById('deleteOrgForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('deleteOrgName').value.trim();
  const out = document.getElementById('deleteOrgResult');
  out.className = 'muted';
  out.textContent = 'Deleting...';
  const r = await apiCall('/org/delete', 'DELETE', { organization_name: name }, true);
  if (r.ok) {
    out.className = 'success';
    out.textContent = 'Organization deleted';
    localStorage.removeItem('token');
    localStorage.removeItem('org_name');
    refreshLoginStatus();
  } else {
    out.className = 'error';
    out.textContent = r.data.error || 'Failed';
  }
});

