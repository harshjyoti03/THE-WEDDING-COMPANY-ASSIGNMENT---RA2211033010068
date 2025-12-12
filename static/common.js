const tokenKey = 'token';
const orgKey = 'org_name';
const emailKey = 'email';
const getToken = () => localStorage.getItem(tokenKey);
const setToken = (t) => localStorage.setItem(tokenKey, t);
const clearToken = () => localStorage.removeItem(tokenKey);
const setOrg = (n) => localStorage.setItem(orgKey, n);
const getOrg = () => localStorage.getItem(orgKey);
const setEmail = (e) => localStorage.setItem(emailKey, e);
const getEmail = () => localStorage.getItem(emailKey);
const updateLoginStatus = () => {
  const ls = document.getElementById('loginStatus');
  const btn = document.getElementById('logoutBtn');
  const t = getToken();
  const e = getEmail();
  const o = getOrg();
  if (t && o) {
    if (ls) ls.textContent = `Logged in as ${e} · Org: ${o}`;
    if (btn) btn.style.display = 'inline-block';
  } else {
    if (ls) ls.textContent = 'Not logged in';
    if (btn) btn.style.display = 'none';
  }
};
const requireAuth = () => {
  if (!getToken()) window.location.href = '/login';
};
document.addEventListener('DOMContentLoaded', () => {
  updateLoginStatus();
  const btn = document.getElementById('logoutBtn');
  if (btn) btn.addEventListener('click', () => {
    clearToken();
    localStorage.removeItem(orgKey);
    localStorage.removeItem(emailKey);
    updateLoginStatus();
    window.location.href = '/login';
  });
});

