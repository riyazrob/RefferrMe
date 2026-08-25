// Keep existing auth helpers (used by the dashboard)
let authMode = "signup";

function getUserId() {
  return localStorage.getItem("reffery_user_id");
}

function setUserId(id) {
  localStorage.setItem("reffery_user_id", id);
}

function clearUser() {
  localStorage.removeItem("reffery_user_id");
}

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  const userId = getUserId();
  if (userId) headers["X-User-Id"] = userId;

  const res = await fetch(path, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Request failed");
  }
  return res.status === 204 ? null : res.json();
}

function showAuth(mode = "signup") {
  authMode = mode;
  const modal = document.getElementById("auth-modal");
  if (!modal) return;
  modal.classList.remove("hidden");
  document.getElementById("auth-title").textContent = mode === "signup" ? "Sign Up" : "Sign In";
  document.getElementById("name").style.display = mode === "signup" ? "block" : "none";
  document.getElementById("switch-text").textContent = mode === "signup" ? "Already have an account?" : "Need an account?";
  document.getElementById("switch-link").textContent = mode === "signup" ? "Sign in" : "Sign up";
}

function hideAuth() {
  const modal = document.getElementById("auth-modal");
  if (modal) modal.classList.add("hidden");
}

function toggleAuthMode(e) {
  e.preventDefault();
  showAuth(authMode === "signup" ? "login" : "signup");
}

async function handleAuth(e) {
  e.preventDefault();
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const name = document.getElementById("name").value;

  try {
    const user = authMode === "signup"
      ? await api("/signup", { method: "POST", body: JSON.stringify({ email, password, name }) })
      : await api("/login", { method: "POST", body: JSON.stringify({ email, password }) });

    setUserId(user.id);
    window.location.href = "/dashboard";
  } catch (err) {
    alert(err.message);
  }
}

function logout() {
  clearUser();
  window.location.href = "/";
}

// Waitlist / homepage behavior (client-only: collects name/email locally and posts to server)
function showToast(message) {
  const el = document.createElement('div');
  el.className = 'toast';
  el.textContent = message;
  Object.assign(el.style, {
    position: 'fixed', right: '20px', bottom: '20px', background: '#111', color: '#fff', padding: '12px 16px', borderRadius: '10px', zIndex: 9999
  });
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 4000);
}

function sanitize(str) { return (str || '').toString().trim(); }

async function submitWaitlist(name, email, role) {
  // try server POST
  try {
    const res = await fetch('/waitlist', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, email, role }) });
    if (res.ok) return await res.json();
  } catch (e) {
    // network error — fallthrough to local storage
  }
  return null;
}

async function handleWaitlistForm(e) {
  e.preventDefault();
  const form = e.target.closest('form');
  if (!form) return;

  // try several common field names used in the imported template
  const name = sanitize((form.querySelector('input[name="name"]') || form.querySelector('input[name="name-cta"]') || form.querySelector('input[name="name-hero"]') || form.querySelector('#hero-name') || form.querySelector('#wait-name') || form.querySelector('#final-name'))?.value);
  const email = sanitize((form.querySelector('input[name="email"]') || form.querySelector('input[name="email-cta"]') || form.querySelector('input[name="email-hero"]') || form.querySelector('#hero-email') || form.querySelector('#wait-email') || form.querySelector('#final-email'))?.value);
  const roleInput = form.querySelector('input[type="radio"][name^="role"]:checked') || form.querySelector('input[type="radio"][name="role"]:checked');
  const role = roleInput ? roleInput.value : 'both';

  if (!name || !email) { showToast('Please provide name and work email.'); return; }

  const serverResult = await submitWaitlist(name, email, role);
  if (serverResult) {
    showToast('Thanks — you are on the waitlist!');
    form.reset();
    return;
  }

  // fallback: store locally
  const entries = JSON.parse(localStorage.getItem('reffery_waitlist') || '[]');
  entries.push({ name, email, role, ts: new Date().toISOString() });
  localStorage.setItem('reffery_waitlist', JSON.stringify(entries));
  showToast('Thanks — you are on the waitlist! (saved locally)');
  form.reset();
}

// Attach handlers for common waitlist forms on page load
window.addEventListener('DOMContentLoaded', () => {
  const selectors = ['#hero-waitlist-form', '#cta-waitlist-form', 'form.join-form', 'form.hero-form', 'form.waitlist'];
  selectors.forEach(sel => {
    document.querySelectorAll(sel).forEach(f => {
      f.addEventListener('submit', handleWaitlistForm);
    });
  });
});
