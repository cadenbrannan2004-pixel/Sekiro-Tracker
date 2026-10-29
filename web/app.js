const root = document.documentElement;

// Bead regions show in this order; anything not listed goes after, in data order
const REGION_ORDER = [
  "Ashina Outskirts", "Hirata Estate", "Ashina Castle",
  "Sunken Valley", "Senpou Temple", "Ashina Depths",
  "Ashina Castle (Dusk)", "Hirata Estate (Owls Memory)", "Fountainhead Palace",
  "Ashina Castle (Night)",
];

const statusEl = document.getElementById("status");

const PLAY_ICON = `<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M3 1.8v8.4L10 6z"/></svg>`;

// Saved to settings.json beside the app; server.py puts the values back on <html> on load
function saveSetting(key, value) {
  return fetch("/api/settings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ [key]: value }),
  }).catch(() => null);  // server gone; the choice still applies until reload
}

// A data-* value from <html>, or the fallback when it was never set
const setting = (key, fallback) => root.dataset[key] ?? fallback;

// Switches and dropdowns marked data-setting: switches store "on"/"off", dropdowns their value.
// CSS reads most of these straight off <html>; the rest re-render below.
for (const input of document.querySelectorAll("[data-setting]")) {
  const key = input.dataset.setting;
  const current = setting(key, input.dataset.default);
  if (input.type === "checkbox") input.checked = current === "on";
  else input.value = current;
  input.addEventListener("change", () => {
    const value = input.type === "checkbox" ? (input.checked ? "on" : "off") : input.value;
    root.dataset[key] = value;
    saveSetting(key, value);
    if (key === "refresh") startPolling();
    if (key === "newHighlight" || key === "hideCollected") renderAll();
  });
}

// Section switches: on = shown. Hidden ones are a space-separated list CSS matches with ~=
const sectionToggles = [...document.querySelectorAll("[data-section-toggle]")];
const hiddenSections = (root.dataset.hiddenSections || "").split(" ");
for (const input of sectionToggles) {
  input.checked = !hiddenSections.includes(input.dataset.sectionToggle);
  input.addEventListener("change", () => {
    const hidden = sectionToggles.filter((i) => !i.checked).map((i) => i.dataset.sectionToggle);
    root.dataset.hiddenSections = hidden.join(" ");
    saveSetting("hiddenSections", hidden);
    placeVideo();  // closes the player if its section was just hidden
  });
}

// Save file location: blank = auto-detect, which shows as the placeholder
const pathInput = document.getElementById("save-path");
const pathMessage = document.getElementById("save-path-message");

function showPathMessage(text, cls) {
  pathMessage.textContent = text;
  pathMessage.className = `path-message ${cls || ""}`;
}

fetch("/api/settings").then((res) => res.json()).then((info) => {
  pathInput.value = info.savePath;
  pathInput.placeholder = info.detectedSavePath || "No save found automatically";
}).catch(() => {});

document.getElementById("save-path-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const res = await saveSetting("savePath", pathInput.value);
  if (!res) { showPathMessage("Server unreachable", "error"); return; }
  const body = await res.json().catch(() => ({}));
  if (!res.ok) { showPathMessage(body.error || `error ${res.status}`, "error"); return; }
  pathInput.value = pathInput.value.trim().replace(/^"|"$/g, "");
  showPathMessage(pathInput.value ? "Saved. Switching to this file…" : "Saved. Finding your save automatically…", "ok");
  setTimeout(refreshState, 1500);  // the tracker picks it up on its next check
});

document.getElementById("reset-settings").addEventListener("click", async () => {
  if (!confirm("Reset all settings to their defaults? Save names and checklists are kept.")) return;
  await fetch("/api/settings/reset", { method: "POST" }).catch(() => {});
  location.reload();
});

// Theme: follows the system until the settings switch pins one
const themeSwitch = document.getElementById("theme-toggle");
const darkQuery = matchMedia("(prefers-color-scheme: dark)");

function isDark() {
  const pinned = root.dataset.theme;
  return pinned ? pinned === "dark" : darkQuery.matches;
}

function syncThemeSwitch() {
  const dark = isDark();
  root.classList.toggle("dark", dark);
  themeSwitch.checked = dark;
}

themeSwitch.addEventListener("change", () => {
  const next = themeSwitch.checked ? "dark" : "light";
  root.dataset.theme = next;
  saveSetting("theme", next);
  syncThemeSwitch();
});
darkQuery.addEventListener("change", syncThemeSwitch);
syncThemeSwitch();

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
// key names the row so the inline player can find it again after a re-render.
function videoLink(url, keepSpace, key) {
  if (!url || !url.startsWith("https://")) {
    return keepSpace ? `<span class="video placeholder" aria-hidden="true"></span>` : "";
  }
  return `<a class="video" href="${esc(url)}" target="_blank" rel="noopener" data-video-key="${esc(key)}" title="Watch video" aria-label="Watch video">${PLAY_ICON}</a>`;
}

// Inline player: a video arrow opens the video in a slot under its row, and opening
// another (or clicking the same arrow) closes it. The lists rebuild on every poll and
// moving an iframe reloads it, so the player lives outside them and sits over an
// empty slot that each render puts back in place.
const player = document.createElement("div");
player.id = "video-player";
player.hidden = true;
player.innerHTML = `<div class="video-bar"><a class="video-external" target="_blank" rel="noopener">Open on YouTube</a>` +
                   `<button type="button" class="video-close" aria-label="Close video">×</button></div>` +
                   `<iframe title="Video guide" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>`;
document.body.appendChild(player);
const playerFrame = player.querySelector("iframe");
let openVideoKey = null;

// youtu.be/ID?t=72 or youtube.com/watch?v=ID&t=1m12s -> embed URL; null for anything else
function embedUrl(url) {
  let u;
  try { u = new URL(url); } catch (e) { return null; }
  const host = u.hostname.replace(/^(www|m)\./, "");
  let id = null;
  if (host === "youtu.be") id = u.pathname.slice(1);
  else if (host === "youtube.com") {
    id = u.pathname === "/watch" ? u.searchParams.get("v") : (u.pathname.match(/^\/(?:embed|shorts|live)\/([^/]+)/) || [])[1];
  }
  if (!id || !/^[\w-]+$/.test(id)) return null;
  const t = (u.searchParams.get("t") || u.searchParams.get("start") || "").match(/^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s?)?$/);
  const start = t ? (+t[1] || 0) * 3600 + (+t[2] || 0) * 60 + (+t[3] || 0) : 0;
  return `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0` + (start ? `&start=${start}` : "");
}

// Grows (or shrinks) the slot so the rows below glide out of the way, while the player
// is revealed top-down over it. Returns the slot's animation, or null if motion is off.
function slideVideo(slot, closing) {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return null;
  const open = { height: `${slot.scrollHeight}px`, marginTop: "6px", marginBottom: "12px" };
  const shut = { height: "0px", marginTop: "0px", marginBottom: "0px" };
  const shown = { clipPath: "inset(0 0 0 0)" };
  const hidden = { clipPath: "inset(0 0 100% 0)" };
  const timing = { duration: 280, easing: "cubic-bezier(0.2, 0.8, 0.2, 1)" };
  const anim = slot.animate(closing ? [open, shut] : [shut, open], timing);
  player.animate(closing ? [shown, hidden] : [hidden, shown], timing);
  const follow = () => { positionPlayer(); if (anim.playState === "running") requestAnimationFrame(follow); };
  requestAnimationFrame(follow);
  return anim;
}

function closeVideo(animate = false) {
  const slot = document.querySelector(".video-slot");
  openVideoKey = null;
  document.querySelector("a.playing")?.classList.remove("playing");
  const finish = () => {
    if (openVideoKey) return;  // another video opened mid-slide
    playerFrame.src = "about:blank";  // stops playback
    player.hidden = true;
    placeVideo();
  };
  const anim = animate && slot ? slideVideo(slot, true) : null;
  if (anim) anim.finished.then(finish, () => {});
  else finish();
}

function positionPlayer() {
  const slot = document.querySelector(".video-slot");
  if (!slot) return;
  const r = slot.getBoundingClientRect();
  // scrollHeight is the slot's full size even while it is sliding open or shut
  Object.assign(player.style, {
    top: `${r.top + scrollY}px`, left: `${r.left + scrollX}px`, width: `${r.width}px`, height: `${slot.scrollHeight}px`,
  });
}

// Puts the empty slot under the open video's row (under the whole strip for boss cards)
function placeVideo(animate = false) {
  document.querySelector(".video-slot")?.remove();
  if (!openVideoKey) return;
  const link = document.querySelector(`a[data-video-key="${CSS.escape(openVideoKey)}"]`);
  if (!link || !link.getClientRects().length) { closeVideo(); return; }  // row gone or view hidden
  link.classList.add("playing");
  const after = link.closest(".boss-scroller") || link.closest("li") || link;
  const slot = document.createElement(after.tagName === "LI" ? "li" : "div");
  slot.className = "video-slot";
  slot.innerHTML = `<div class="video-slot-bar"></div><div class="video-slot-frame"></div>`;
  after.after(slot);
  positionPlayer();
  if (animate) slideVideo(slot, false);
}

document.addEventListener("click", (event) => {
  const link = event.target.closest("a[data-video-key]");
  if (!link || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey) return;
  if (setting("videos", "inline") === "youtube") return;  // the link's own new-tab behaviour
  const src = embedUrl(link.href);
  if (!src) return;  // not YouTube: let it open in a new tab as before
  event.preventDefault();
  if (link.dataset.videoKey === openVideoKey) { closeVideo(true); return; }
  document.querySelector("a.playing")?.classList.remove("playing");
  openVideoKey = link.dataset.videoKey;
  playerFrame.src = src;
  player.querySelector(".video-external").href = link.href;
  player.hidden = false;
  placeVideo(true);
});
player.querySelector(".video-close").addEventListener("click", () => closeVideo(true));
new ResizeObserver(positionPlayer).observe(document.body);
addEventListener("resize", positionPlayer);

// Per slot: keys of items already collected when that slot was first shown.
// Anything collected later counts as new until the row is hovered or focused,
// or until the timed highlight setting runs out.
const seenBySlot = {};
let seen = null;
let firstLook = false;
const newSince = {};  // "slot:key" -> when it first showed as new
const HIGHLIGHT_MS = { "1m": 60_000, "5m": 300_000 };

function markNew(li, key) {
  const mode = setting("newHighlight", "seen");
  if (firstLook || mode === "off") { seen.add(key); return; }
  if (seen.has(key)) return;
  const since = newSince[`${selectedSlot}:${key}`] ??= Date.now();
  if (Date.now() - since > HIGHLIGHT_MS[mode]) { seen.add(key); return; }  // undefined limit -> false
  li.classList.add("new");
  const clear = () => { seen.add(key); li.classList.replace("new", "just-seen"); };
  li.addEventListener("pointerenter", clear, { once: true });
  li.addEventListener("focusin", clear, { once: true });
}

// Small meter for a prosthetic tool's Sculptor upgrades
function upgradeMeter({ have, total }) {
  const pct = total ? (have / total) * 100 : 0;
  return `<span class="upgrade${have === total ? " done" : ""}" title="${have} of ${total} upgrades">` +
         `<span class="upgrade-track"><span class="upgrade-fill" style="width:${pct}%"></span></span>` +
         `<span class="upgrade-count">${have}/${total}</span></span>`;
}

// rows: [{name, collected, region?, source?, video?, upgrades?}] -- collected null = flag not mapped yet
// tag: "source" shows BOSS/CHEST/..., "region" shows the area name on the right
function renderChecklist(listEl, rows, { tag, videos, group = listEl.id } = {}) {
  listEl.innerHTML = "";
  for (const row of rows) {
    const li = document.createElement("li");
    const mark = markFor(row.collected);
    li.className = mark;
    // Owned but not fully upgraded still counts as something to do for "Hide collected items"
    if (row.upgrades && row.upgrades.have < row.upgrades.total) li.classList.add("upgrading");
    let tagHtml = "";
    if (tag === "source" && row.source) tagHtml = `<span class="source">${esc(row.source)}</span>`;
    if (tag === "region" && row.region) tagHtml = `<span class="region-tag">${esc(row.region)}</span>`;
    li.innerHTML = `<span class="mark ${mark}" role="img" aria-label="${MARK_LABELS[mark]}"></span>` +
                    `<span class="item-name">${esc(row.name || "(unnamed)")}</span>` +
                    tagHtml +
                    (row.upgrades ? upgradeMeter(row.upgrades) : "") +
                    (videos ? videoLink(row.video, true, `${group}:${row.name}`) : "");
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
    block.classList.toggle("complete", regionDone === rows.length);  // hidden by "Hide collected items"
    done += regionDone;
    container.appendChild(block);
  }
  return done;
}

// Checkbox targets (the esoteric texts) render as collected/not-yet rows;
// counted ones (Lapis Lazuli, Treasure Carp Scale) keep progress bars below them,
// and the ninjutsu get their own list under those
function renderQuantities(textsEl, listEl, ninjutsuEl, quantities) {
  const entries = Object.entries(quantities);
  const checkRows = (group) => entries
    .filter(([, info]) => info.checkbox && (info.group || "") === group)
    .map(([name, info]) => ({ name, collected: info.complete, video: info.video }));
  renderChecklist(textsEl, checkRows(""), { videos: true });
  const ninjutsuRows = checkRows("ninjutsu");
  const ninjutsu = renderChecklist(ninjutsuEl, ninjutsuRows, { videos: true });
  document.getElementById("ninjutsu-count").textContent = countText(ninjutsu, ninjutsuRows);

  listEl.innerHTML = "";
  for (const [name, info] of entries.filter(([, info]) => !info.checkbox)) {
    const pct = info.target > 0 ? Math.min(100, (info.have / info.target) * 100) : 0;
    const li = document.createElement("li");
    li.innerHTML = `
      <div class="bar-label"><span class="item-name">${esc(name)}</span><span class="qty">${info.have} / ${info.target}</span>${videoLink(info.video, true, `qty:${name}`)}</div>
      <div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div>
    `;
    listEl.appendChild(li);
  }
}

const TROPHY_ICON = `<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M3 1h6v1.5h2V4a2.5 2.5 0 0 1-2.2 2.5A3 3 0 0 1 6.8 8.4V10H8.5v1h-5v-1h1.7V8.4a3 3 0 0 1-2-1.9A2.5 2.5 0 0 1 1 4V2.5h2zm-1 2.5V4a1.5 1.5 0 0 0 1 1.4V3.5zm8 0H9v1.9A1.5 1.5 0 0 0 10 4z"/></svg>`;

function achievementLine(name) {
  return name
    ? `<span class="achievement">${TROPHY_ICON}${esc(name)}</span>`
    : `<span class="achievement none">No Steam achievement</span>`;
}

const BOSS_MARK_LABELS = { yes: "Defeated", no: "Not yet", unknown: "Not readable" };

async function toggleBoss(bossId, checked) {
  await fetch("/api/bosses", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id: bossId, checked }),
  });
  refreshState();
}

// One card per boss: a Steam achievement marks it automatically, bosses without one get a checkbox
function renderBossCards(listEl, bosses) {
  listEl.innerHTML = "";
  for (const boss of bosses) {
    const li = document.createElement("li");
    const mark = markFor(boss.defeated);
    li.className = `boss-card ${mark}` + (boss.manual ? " manual" : "");
    const checkboxId = `boss-${boss.id}`;
    const status = boss.manual
      ? `<input type="checkbox" id="${esc(checkboxId)}" ${boss.defeated ? "checked" : ""}>`
      : `<span class="mark ${mark}" role="img" aria-label="${BOSS_MARK_LABELS[mark]}"></span>`;
    const title = boss.manual ? `<label for="${esc(checkboxId)}">${esc(boss.name)}</label>` : esc(boss.name);
    li.innerHTML = `<div class="boss-top">${status}${videoLink(boss.video, false, `boss:${boss.id}`)}</div>` +
                   `<h3>${title}</h3>` +
                   `<span class="region-tag">${esc(boss.region)}</span>` +
                   (boss.manual
                     ? `<span class="achievement none">No Steam achievement so check it yourself</span>`
                     : achievementLine(boss.achievement)) +
                   (boss.note ? `<span class="boss-note">${esc(boss.note)}</span>` : "");
    if (boss.manual) {
      li.querySelector("input").addEventListener("change", (event) => toggleBoss(boss.id, event.target.checked));
    } else if (boss.defeated === true) {
      markNew(li, `bosses:${boss.name}`);
    }
    listEl.appendChild(li);
  }
  return bosses.filter((b) => b.defeated === true).length;
}

// Account-wide, so this is the same whichever slot tab is open
function renderBosses(account) {
  const countFor = (done, rows) => countText(done, rows.map((b) => ({ collected: b.defeated })));
  const required = account.required || [];
  const hidden = account.hidden || [];

  const done = renderBossCards(document.getElementById("boss-cards"), required);
  renderTotal("bosses", done, required.length);
  let count = countFor(done, required);
  if (account.man_without_equal === true) count = "Man Without Equal unlocked";
  else if (!account.steam_available) count += " · Steam achievements not found";
  document.getElementById("bosses-count").textContent = count;

  const hiddenDone = renderBossCards(document.getElementById("hidden-boss-cards"), hidden);
  document.getElementById("hidden-bosses-count").textContent = countFor(hiddenDone, hidden);
}

// Arrow buttons page the strip by most of its visible width
for (const btn of document.querySelectorAll(".scroll-btn")) {
  btn.addEventListener("click", () => {
    const strip = document.getElementById(btn.dataset.target);
    const dir = btn.classList.contains("next") ? 1 : -1;
    strip.scrollBy({ left: dir * strip.clientWidth * 0.8, behavior: "smooth" });
  });
}

let selectedSlot = root.dataset.selectedSlot ?? null;
let lastData = null;

function ngLabel(entry) {
  const ng = entry.stats && entry.stats.ng_plus;
  if (ng === undefined) return "";
  return ng === 0 ? "NG" : `NG+${ng}`;
}

// Custom name from settings, or the default "Slot N"
function slotLabel(id) {
  const names = (lastData && lastData.names) || {};
  return names[id] || `Slot ${Number(id) + 1}`;
}

function renderTabs(slots) {
  const nav = document.getElementById("slot-tabs");
  nav.innerHTML = "";
  for (const [id, entry] of Object.entries(slots)) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "tab" + (id === selectedSlot && !showingSettings ? " active" : "");
    const ng = ngLabel(entry);
    btn.innerHTML = esc(slotLabel(id)) + (ng ? `<span class="ng">${ng}</span>` : "");
    btn.addEventListener("click", () => {
      selectedSlot = id;
      showingSettings = false;
      saveSetting("selectedSlot", id);
      renderAll();
    });
    nav.appendChild(btn);
  }
  document.getElementById("settings-tab").classList.toggle("active", showingSettings);
}

// Settings view: one name field per save
let showingSettings = false;
let settingsKey = null;  // which slots the fields were built for, so polling doesn't wipe typing

document.getElementById("settings-tab").addEventListener("click", () => {
  showingSettings = true;
  settingsKey = null;
  renderAll();
});

async function saveSlotName(id, name, savedEl) {
  const res = await fetch("/api/slot-names", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ slot: id, name }),
  });
  if (!res.ok) return;
  const body = await res.json();
  lastData.names = { ...lastData.names };
  if (body.name) lastData.names[id] = body.name;
  else delete lastData.names[id];
  renderTabs(lastData.slots || {});
  savedEl.classList.add("show");
  setTimeout(() => savedEl.classList.remove("show"), 1200);
}

function renderSettings(slots) {
  const ids = Object.keys(slots);
  const key = ids.join(",");
  const list = document.getElementById("slot-names");
  if (key === settingsKey || list.contains(document.activeElement)) return;
  settingsKey = key;

  list.innerHTML = "";
  if (ids.length === 0) {
    list.innerHTML = `<li class="settings-empty">No saves found yet.</li>`;
    return;
  }
  const names = lastData.names || {};
  for (const id of ids) {
    const li = document.createElement("li");
    const inputId = `slot-name-${id}`;
    const ng = ngLabel(slots[id]);
    li.innerHTML = `<label for="${inputId}">Slot ${Number(id) + 1}${ng ? `<span class="ng">${ng}</span>` : ""}</label>` +
                   `<input id="${inputId}" type="text" maxlength="32" autocomplete="off" placeholder="Slot ${Number(id) + 1}">` +
                   `<span class="saved" aria-live="polite">Saved</span>`;
    const input = li.querySelector("input");
    input.value = names[id] || "";
    input.addEventListener("keydown", (event) => { if (event.key === "Enter") input.blur(); });
    input.addEventListener("change", () => saveSlotName(id, input.value, li.querySelector(".saved")));
    list.appendChild(li);
  }
}

function renderAll() {
  renderView();
  placeVideo();
}

function renderView() {
  if (!lastData) return;
  const slots = lastData.slots || {};
  const ids = Object.keys(slots);
  if (!(selectedSlot in slots)) selectedSlot = ids[0] ?? null;  // saved choice vanished -> fall back
  renderTabs(slots);

  document.getElementById("settings-view").hidden = !showingSettings;
  document.getElementById("tracker-view").hidden = showingSettings;
  if (showingSettings) {
    renderSettings(slots);
    return;
  }
  if (ids.length === 0) {
    setStatus("no active save slots found", "error");
    return;
  }

  firstLook = !(selectedSlot in seenBySlot);
  seen = seenBySlot[selectedSlot] ??= new Set();

  const report = slots[selectedSlot].report;

  const beads = renderRegions(document.getElementById("beads-regions"), report.prayer_beads);
  renderTotal("beads", beads, report.prayer_beads.length);

  const gourdRows = report.gourd_seeds;
  const gourds = renderChecklist(document.getElementById("gourds-list"), gourdRows, { tag: "region", videos: true });
  document.getElementById("gourds-count").textContent = countText(gourds, gourdRows);
  renderTotal("gourds", gourds, gourdRows.length);

  const toolVideos = report.prosthetic_tools.videos || {};
  const toolUpgrades = report.prosthetic_tools.upgrades || {};  // missing until the tracker re-reads the save
  const toolRows = Object.entries(report.prosthetic_tools.owned)
    .map(([name, collected]) => ({ name, collected, video: toolVideos[name], upgrades: toolUpgrades[name] }));
  const tools = renderChecklist(document.getElementById("tools-list"), toolRows, { videos: true });
  const upgradeTotals = Object.values(toolUpgrades);
  const upgradesDone = upgradeTotals.reduce((sum, u) => sum + u.have, 0);
  const upgradesMax = upgradeTotals.reduce((sum, u) => sum + u.total, 0);
  document.getElementById("tools-count").textContent = countText(tools, toolRows) +
    (upgradesMax ? ` · ${upgradesDone} / ${upgradesMax} upgrades` : "");
  renderTotal("tools", tools, toolRows.length);

  renderQuantities(document.getElementById("texts-list"), document.getElementById("quantities-list"),
                   document.getElementById("ninjutsu-list"), report.quantity_targets);

  renderBosses(lastData.bosses || {});
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
      ? `<a class="guide" href="${esc(ending.video)}" target="_blank" rel="noopener" data-video-key="${esc(`ending:${ending.name}`)}">${PLAY_ICON}Watch the ending guide</a>`
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
  placeVideo();
}

// Restarted when the refresh setting changes
let pollTimer = null;
function startPolling() {
  clearInterval(pollTimer);
  pollTimer = setInterval(refreshState, Number(setting("refresh", "3")) * 1000);
}

refreshState();
loadEndings();
startPolling();
setInterval(renderConnected, 1000);  // keeps "updated Xs ago" ticking between polls

// Lets SekiroApp.py shut down when this tab closes (404/405 under plain server.py, harmless)
addEventListener("pagehide", () => navigator.sendBeacon("/api/bye"));
