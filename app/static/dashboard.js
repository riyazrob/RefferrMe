document.addEventListener("DOMContentLoaded", () => {
  if (!getUserId()) {
    window.location.href = "/";
    return;
  }
  initDashboard();
  setupNavigation();
});

function setupNavigation() {
  document.querySelectorAll(".sidebar nav a").forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();
      switchPanel(link.dataset.panel);
    });
  });
}

function switchPanel(name) {
  document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".sidebar nav a").forEach(a => a.classList.remove("active"));
  document.getElementById(`panel-${name}`)?.classList.add("active");
  document.querySelector(`[data-panel="${name}"]`)?.classList.add("active");

  if (name === "referrals") searchReferrals();
  if (name === "my-requests") loadMyRequests();
  if (name === "referrer") loadMyReferrals();
  if (name === "incoming") loadIncoming();
  if (name === "notifications") loadNotifications();
}

async function initDashboard() {
  try {
    const user = await api("/me");
    document.getElementById("user-info").innerHTML =
      `<strong>${user.name}</strong><br>${user.email}<br>Role: ${user.role} · Rep: ${user.reputation_score}`;

    const stats = document.getElementById("stats-grid");
    stats.innerHTML = `
      <div class="stat-card"><div class="value">${user.reputation_score}</div><div class="label">Reputation</div></div>
      <div class="stat-card"><div class="value">${user.active_role}</div><div class="label">Active Role</div></div>
      <div class="stat-card"><div class="value">${user.availability.replace("_", " ")}</div><div class="label">Availability</div></div>
    `;

    const profile = await api("/profile/candidate").catch(() => null);
    if (profile) populateProfile(profile);
  } catch {
    logout();
  }
}

function populateProfile(p) {
  ["resume_text","linkedin_url","skills","experience","education","github_url",
   "portfolio_url","work_authorization","preferred_locations"].forEach(id => {
    const el = document.getElementById(id);
    if (el && p[id]) el.value = p[id];
  });
  if (p.ai_summary) {
    const box = document.getElementById("ai-analysis");
    box.classList.remove("hidden");
    box.innerHTML = `<h3>AI Analysis</h3><p><strong>Readiness:</strong> ${p.referral_readiness_score}%</p><p>${p.ai_summary}</p><pre>${p.resume_suggestions || ""}</pre>`;
  }
}

async function saveProfile(e) {
  e.preventDefault();
  const data = {};
  ["resume_text","linkedin_url","skills","experience","education","github_url",
   "portfolio_url","work_authorization","preferred_locations"].forEach(id => {
    data[id] = document.getElementById(id).value;
  });
  try {
    await api("/profile/candidate", { method: "PUT", body: JSON.stringify(data) });
    alert("Profile saved!");
  } catch (err) { alert(err.message); }
}

async function analyzeProfile() {
  try {
    const p = await api("/profile/candidate/analyze", { method: "POST" });
    populateProfile(p);
    switchPanel("profile");
  } catch (err) { alert(err.message); }
}

async function becomeReferrer() {
  try {
    await api("/auth/become-referrer", { method: "POST" });
    alert("You are now a referrer!");
    initDashboard();
  } catch (err) { alert(err.message); }
}

async function searchReferrals() {
  const params = new URLSearchParams();
  const company = document.getElementById("search-company")?.value;
  const role = document.getElementById("search-role")?.value;
  const tech = document.getElementById("search-tech")?.value;
  if (company) params.set("company", company);
  if (role) params.set("role", role);
  if (tech) params.set("technology", tech);

  const list = document.getElementById("referral-list");
  try {
    const referrals = await api(`/referrals/search?${params}`);
    if (!referrals.length) { list.innerHTML = "<p>No referrals found.</p>"; return; }
    list.innerHTML = referrals.map(r => `
      <div class="list-item">
        <h3>${r.job_title} at ${r.company}</h3>
        <div class="meta">${r.location || "Location TBD"} · ${r.slots - r.slots_filled} slots left</div>
        <p>${(r.required_skills || "").slice(0, 150)}</p>
        <div class="actions">
          <button class="btn primary sm" onclick="requestReferral(${r.id})">Request Referral</button>
        </div>
      </div>
    `).join("");
  } catch (err) { list.innerHTML = `<p>Error: ${err.message}</p>`; }
}

async function requestReferral(id) {
  const cover = prompt("Cover message (optional):") || "";
  try {
    const req = await api(`/requests/referrals/${id}`, {
      method: "POST",
      body: JSON.stringify({ cover_message: cover }),
    });
    alert(`Request sent! AI Match: ${req.match_score}%`);
    switchPanel("my-requests");
  } catch (err) { alert(err.message); }
}

async function loadMyRequests() {
  const list = document.getElementById("my-requests-list");
  try {
    const reqs = await api("/requests/mine");
    if (!reqs.length) { list.innerHTML = "<p>No requests yet.</p>"; return; }
    list.innerHTML = reqs.map(r => `
      <div class="list-item">
        <h3>Referral #${r.referral_id}</h3>
        <span class="badge ${r.status === 'accepted' ? 'success' : 'warning'}">${r.status.replace(/_/g, " ")}</span>
        <div class="match-score">${r.match_score}% match</div>
        <pre>${r.match_explanation || ""}</pre>
        ${r.status === 'accepted' ? `<button class="btn success sm" onclick="advanceStatus(${r.id}, 'submitted')">Mark Submitted</button>` : ""}
        ${r.status === 'offer_received' ? `<button class="btn success sm" onclick="markHired(${r.id})">Mark Hired 🎉</button>` : ""}
      </div>
    `).join("");
  } catch (err) { list.innerHTML = `<p>Error: ${err.message}</p>`; }
}

async function advanceStatus(id, status) {
  try {
    await api(`/requests/${id}/status`, { method: "PATCH", body: JSON.stringify({ status }) });
    loadMyRequests();
  } catch (err) { alert(err.message); }
}

async function markHired(id) {
  try {
    await api(`/requests/${id}/mark-hired`, { method: "POST" });
    alert("Congratulations! Availability set to Not Looking.");
    initDashboard();
    loadMyRequests();
  } catch (err) { alert(err.message); }
}

async function createReferral(e) {
  e.preventDefault();
  const data = {
    company: document.getElementById("ref-company").value,
    job_title: document.getElementById("ref-title").value,
    job_link: document.getElementById("ref-link").value,
    job_id: document.getElementById("ref-job-id").value,
    job_description: document.getElementById("ref-description").value,
    slots: parseInt(document.getElementById("ref-slots").value) || 1,
  };
  try {
    const ref = await api("/referrals", { method: "POST", body: JSON.stringify(data) });
    const parsed = await api(`/referrals/${ref.id}/parse`, { method: "POST" });
    await api(`/referrals/${ref.id}/publish`, { method: "POST" });
    alert(`Referral published! AI parsed: ${parsed.required_skills}`);
    document.getElementById("referral-form").reset();
    loadMyReferrals();
  } catch (err) { alert(err.message); }
}

async function loadMyReferrals() {
  const list = document.getElementById("my-referrals-list");
  try {
    const refs = await api("/referrals/mine");
    if (!refs.length) { list.innerHTML = "<p>No referrals posted yet.</p>"; return; }
    list.innerHTML = refs.map(r => `
      <div class="list-item">
        <h3>${r.job_title} at ${r.company}</h3>
        <span class="badge">${r.status}</span>
        <div class="meta">${r.slots_filled}/${r.slots} slots filled</div>
      </div>
    `).join("");
  } catch (err) { list.innerHTML = `<p>Error: ${err.message}</p>`; }
}

async function loadIncoming() {
  const list = document.getElementById("incoming-list");
  try {
    const reqs = await api("/requests/incoming");
    if (!reqs.length) { list.innerHTML = "<p>No incoming requests.</p>"; return; }
    list.innerHTML = reqs.map(r => `
      <div class="list-item">
        <h3>Request #${r.id}</h3>
        <div class="match-score">${r.match_score}% match</div>
        <p><strong>Recommendation:</strong> ${r.ai_recommendation}</p>
        <pre>${r.match_explanation || ""}</pre>
        <p>${r.cover_message || ""}</p>
        <span class="badge">${r.status.replace(/_/g, " ")}</span>
        ${r.status === 'requested' ? `
          <div class="actions">
            <button class="btn success sm" onclick="reviewRequest(${r.id}, true)">Accept</button>
            <button class="btn danger sm" onclick="reviewRequest(${r.id}, false)">Decline</button>
          </div>
        ` : ""}
      </div>
    `).join("");
  } catch (err) { list.innerHTML = `<p>Error: ${err.message}</p>`; }
}

async function reviewRequest(id, accept) {
  try {
    await api(`/requests/${id}/review`, { method: "POST", body: JSON.stringify({ accept }) });
    loadIncoming();
  } catch (err) { alert(err.message); }
}

async function loadNotifications() {
  const list = document.getElementById("notifications-list");
  try {
    const notes = await api("/notifications");
    if (!notes.length) { list.innerHTML = "<p>No notifications.</p>"; return; }
    list.innerHTML = notes.map(n => `
      <div class="list-item ${n.read ? '' : 'unread'}">
        <h3>${n.title}</h3>
        <div class="meta">${new Date(n.created_at).toLocaleString()}</div>
        <p>${n.message}</p>
      </div>
    `).join("");
  } catch (err) { list.innerHTML = `<p>Error: ${err.message}</p>`; }
}
