const POLL_INTERVAL_MS = 3000;

// Bead regions show in this order; anything not listed goes after, in data order
const REGION_ORDER = [
  "Ashina Outskirts", "Hirata Estate", "Ashina Castle",
  "Sunken Valley", "Senpou Temple", "Ashina Depths",
  "Ashina Castle (Dusk)", "Hirata Estate (Owls Memory)", "Fountainhead Palace",
  "Ashina Castle (Night)",
];

const statusEl = document.getElementById("status");

const PLAY_ICON = `<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M3 1.8v8.4L10 6z"/></svg>`;

// Theme: follows the system until the toggle pins one (saved in localStorage)
const themeBtn = document.getElementById("theme-toggle");
const darkQuery = matchMedia("(prefers-color-scheme: dark)");

function isDark() {
  const pinned = document.documentElement.dataset.theme;
  return pinned ? pinned === "dark" : darkQuery.matches;
}

function syncThemeButton() {
  const dark = isDark();
  document.documentElement.classList.toggle("dark", dark);
  themeBtn.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
}

themeBtn.addEventListener("click", () => {
  const next = isDark() ? "light" : "dark";
  document.documentElement.dataset.theme = next;
  try { localStorage.setItem("theme", next); } catch (e) { /* storage unavailable */ }
  syncThemeButton();
});
darkQuery.addEventListener("change", syncThemeButton);
syncThemeButton();

// Backdrop: the user's background.gif if present, otherwise a few drawn petals
const PETAL_COUNT = 10;
const backdrop = document.getElementById("backdrop");
const bgImage = new Image();
bgImage.onload = () => {
  backdrop.style.backgroundImage = "url(background.gif)";
  backdrop.classList.add("has-gif");
};
bgImage.onerror = () => {
  for (let i = 0; i < PETAL_COUNT; i++) {
    const petal = document.createElement("span");
    petal.className = "petal";
    // Alternate between the left and right gutters so petals aren't hidden behind the panels
    petal.style.left = `${i % 2 ? 88 + Math.random() * 10 : Math.random() * 10}%`;
    petal.style.setProperty("--size", `${14 + Math.random() * 6}px`);
    petal.style.setProperty("--y", `${10 + Math.random() * 80}%`);       // resting spot under reduced motion
    petal.style.setProperty("--r", `${Math.random() * 360}deg`);
    petal.style.animationDuration = `${16 + Math.random() * 12}s`;
    petal.style.animationDelay = `${-Math.random() * 28}s`;  // negative = already mid-fall on load
    backdrop.appendChild(petal);
  }
};
bgImage.src = "background.gif";

function setStatus(text, cls) {
  statusEl.textContent = text;
  statusEl.className = `status ${cls || ""}`;
}

function esc(text) {
  return String(text ?? "").replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);
}

function markFor(value) {
  // true = collected/owned, false = not yet, null = flag not mapped yet
  if (value === true) return "yes";
  if (value === false) return "no";
  return "unknown";
}

const MARK_LABELS = { yes: "Collected", no: "Not yet", unknown: "Flag not mapped" };

// Only https links, so a bad paste can't become a javascript: URL.
// keepSpace leaves an invisible slot so rows without a video still line up.
function videoLink(url, keepSpace) {
  if (!url || !url.startsWith("https://")) {
    return keepSpace ? `<span class="video placeholder" aria-hidden="true"></span>` : "";
  }
  return `<a class="video" href="${esc(url)}" target="_blank" rel="noopener" title="Watch on YouTube" aria-label="Watch on YouTube">${PLAY_ICON}</a>`;
}

// Per slot: keys of items already collected when that slot was first shown.
// Anything collected later counts as new until the row is hovered or focused.
const seenBySlot = {};
let seen = null;
let firstLook = false;

function markNew(li, key) {
  if (firstLook) { seen.add(key); return; }
  if (seen.has(key)) return;
  li.classList.add("new");
  const clear = () => { seen.add(key); li.classList.replace("new", "just-seen"); };
  li.addEventListener("pointerenter", clear, { once: true });
  li.addEventListener("focusin", clear, { once: true });
}

// rows: [{name, collected, region?, source?, video?}] -- collected null = flag not mapped yet
// tag: "source" shows BOSS/CHEST/..., "region" shows the area name on the right
function renderChecklist(listEl, rows, { tag, videos, group = listEl.id } = {}) {
  listEl.innerHTML = "";
  for (const row of rows) {
    const li = document.createElement("li");
    const mark = markFor(row.collected);
    li.className = mark;
    let tagHtml = "";
    if (tag === "source" && row.source) tagHtml = `<span class="source">${esc(row.source)}</span>`;
    if (tag === "region" && row.region) tagHtml = `<span class="region-tag">${esc(row.region)}</span>`;
    li.innerHTML = `<span class="mark ${mark}" role="img" aria-label="${MARK_LABELS[mark]}"></span>` +
                    `<span class="item-name">${esc(row.name || "(unnamed)")}</span>` +
                    tagHtml +
                    (videos ? videoLink(row.video, true) : "");
    if (row.collected === true) markNew(li, `${group}:${row.name}`);
    listEl.appendChild(li);
  }
  return rows.filter((r) => r.collected === true).length;
}

// Leads with what's left, since that's what the player is hunting for
function countText(done, rows) {
  const left = rows.length - done;
  if (left === 0) return "Complete";
  const unmapped = rows.filter((r) => r.collected === null).length;
  return `${left} left` + (unmapped ? ` · ${unmapped} unmapped` : "");
}

function renderTotal(id, done, total) {
  const left = total - done;
  document.getElementById(`${id}-total`).innerHTML = `${done}<small> / ${total}</small>` +
    ` <span class="stat-left">${left ? `${left} left` : "Complete"}</span>`;
  document.getElementById(`${id}-bar`).style.width = `${total ? (done / total) * 100 : 0}%`;
}

const normalizeRegion = (name) => (name || "Other").replace(/\s+/g, " ").trim();

function renderRegions(container, beads) {
  const groups = new Map();
  for (const bead of beads) {
    const region = normalizeRegion(bead.region);
    if (!groups.has(region)) groups.set(region, []);
    groups.get(region).push(bead);
  }
  const rank = (r) => (REGION_ORDER.includes(r) ? REGION_ORDER.indexOf(r) : REGION_ORDER.length);
  const regions = [...groups.keys()].sort((a, b) => rank(a) - rank(b));

  container.innerHTML = "";
  let done = 0;
  for (const region of regions) {
    const rows = groups.get(region);
    const block = document.createElement("div");
    block.className = "region";
    block.innerHTML = `<h3><span>${esc(region)}</span><span class="count"></span></h3><ul class="checklist"></ul>`;
    const regionDone = renderChecklist(block.querySelector("ul"), rows, { tag: "source", videos: true, group: `beads:${region}` });
    block.querySelector(".count").textContent = countText(regionDone, rows);
    done += regionDone;
    container.appendChild(block);
  }
  return done;
}

// Checkbox targets (the esoteric texts) render as collected/not-yet rows;
// counted ones (Lapis Lazuli, Treasure Carp Scale) keep progress bars below them
function renderQuantities(textsEl, listEl, quantities) {
  const entries = Object.entries(quantities);
  const textRows = entries
    .filter(([, info]) => info.checkbox)
    .map(([name, info]) => ({ name, collected: info.complete }));
  renderChecklist(textsEl, textRows);

  listEl.innerHTML = "";
  for (const [name, info] of entries.filter(([, info]) => !info.checkbox)) {
    const pct = info.target > 0 ? Math.min(100, (info.have / info.target) * 100) : 0;
    const li = document.createElement("li");
    li.innerHTML = `
      <div class="bar-label"><span>${esc(name)}</span><span class="qty">${info.have} / ${info.target}</span></div>
      <div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div>
    `;
    listEl.appendChild(li);
  }
}

let selectedSlot = null;
let lastData = null;

try { selectedSlot = localStorage.getItem("selectedSlot"); } catch (e) { /* storage unavailable */ }

function ngLabel(entry) {
  const ng = entry.stats && entry.stats.ng_plus;
  if (ng === undefined) return "";
  return ng === 0 ? "NG" : `NG+${ng}`;
}

function renderTabs(slots) {
  const nav = document.getElementById("slot-tabs");
  nav.innerHTML = "";
  for (const [id, entry] of Object.entries(slots)) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "tab" + (id === selectedSlot ? " active" : "");
    const ng = ngLabel(entry);
    btn.innerHTML = `Slot ${Number(id) + 1}` + (ng ? `<span class="ng">${ng}</span>` : "");
    btn.addEventListener("click", () => {
      selectedSlot = id;
      try { localStorage.setItem("selectedSlot", id); } catch (e) { /* ignore */ }
      renderAll();
    });
    nav.appendChild(btn);
  }
}

function renderAll() {
  if (!lastData) return;
  const slots = lastData.slots || {};
  const ids = Object.keys(slots);
  if (ids.length === 0) {
    setStatus("no active save slots found", "error");
    renderTabs({});
    return;
  }
  if (!(selectedSlot in slots)) selectedSlot = ids[0];  // saved choice vanished -> fall back
  renderTabs(slots);

  firstLook = !(selectedSlot in seenBySlot);
  seen = seenBySlot[selectedSlot] ??= new Set();

  const report = slots[selectedSlot].report;

  const beads = renderRegions(document.getElementById("beads-regions"), report.prayer_beads);
  renderTotal("beads", beads, report.prayer_beads.length);

  const gourdRows = report.gourd_seeds;
  const gourds = renderChecklist(document.getElementById("gourds-list"), gourdRows, { tag: "region", videos: true });
  document.getElementById("gourds-count").textContent = countText(gourds, gourdRows);
  renderTotal("gourds", gourds, gourdRows.length);

  const toolRows = Object.entries(report.prosthetic_tools.owned).map(([name, collected]) => ({ name, collected }));
  const tools = renderChecklist(document.getElementById("tools-list"), toolRows, { videos: true });
  document.getElementById("tools-count").textContent = countText(tools, toolRows);
  renderTotal("tools", tools, toolRows.length);

  renderQuantities(document.getElementById("texts-list"), document.getElementById("quantities-list"),
                   report.quantity_targets);
}

function agoText(seconds) {
  if (seconds < 60) return `${Math.max(0, Math.round(seconds))}s ago`;
  if (seconds < 3600) return `${Math.round(seconds / 60)}m ago`;
  return `${Math.round(seconds / 3600)}h ago`;
}

let connected = false;

function renderConnected() {
  if (!connected || !lastData) return;
  const file = lastData.save_file || "save file";
  const updated = lastData.updated ? ` · updated ${agoText(Date.now() / 1000 - lastData.updated)}` : "";
  setStatus(`Watching ${file}${updated}`, "ok");
}

async function refreshState() {
  try {
    const res = await fetch("/api/state");
    if (!res.ok) {
      connected = false;
      const body = await res.json().catch(() => ({}));
      setStatus(body.error || `error ${res.status}`, "error");
      return;
    }
    lastData = await res.json();
    connected = true;
    renderConnected();
    renderAll();
  } catch (err) {
    connected = false;
    setStatus("server unreachable, is server.py running?", "error");
  }
}

async function toggleRequirement(reqId, checked) {
  await fetch("/api/endings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id: reqId, checked }),
  });
}

async function loadEndings() {
  const res = await fetch("/api/endings");
  const data = await res.json();
  const container = document.getElementById("endings");
  container.innerHTML = "";

  let completeCount = 0;
  for (const ending of data.endings) {
    const doneCount = ending.requirements.filter((r) => r.checked).length;
    const complete = ending.requirements.length > 0 && doneCount === ending.requirements.length;
    if (complete) completeCount++;

    const block = document.createElement("div");
    block.className = "ending" + (complete ? " complete" : "");
    const progress = complete
      ? `<span class="count done">Complete</span>`
      : `<span class="count">${doneCount} / ${ending.requirements.length}</span>`;
    const guide = ending.video && ending.video.startsWith("https://")
      ? `<a class="guide" href="${esc(ending.video)}" target="_blank" rel="noopener">${PLAY_ICON}Watch the ending guide</a>`
      : "";
    block.innerHTML = `<h3><span>${esc(ending.name)}</span>${progress}</h3>${guide}`;

    const ul = document.createElement("ul");
    for (const req of ending.requirements) {
      const li = document.createElement("li");
      const checkboxId = `req-${req.id}`;
      li.innerHTML = `<input type="checkbox" id="${esc(checkboxId)}" ${req.checked ? "checked" : ""}>` +
                      `<label for="${esc(checkboxId)}">${esc(req.text)}</label>`;
      ul.appendChild(li);

      li.querySelector("input").addEventListener("change", async (event) => {
        await toggleRequirement(req.id, event.target.checked);
        loadEndings(); // refresh counts
      });
    }
    block.appendChild(ul);
    container.appendChild(block);
  }
  renderTotal("endings", completeCount, data.endings.length);
}

refreshState();
loadEndings();
setInterval(refreshState, POLL_INTERVAL_MS);
setInterval(renderConnected, 1000);  // keeps "updated Xs ago" ticking between polls

// Lets SekiroApp.py shut down when this tab closes (404/405 under plain server.py, harmless)
addEventListener("pagehide", () => navigator.sendBeacon("/api/bye"));
