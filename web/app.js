const POLL_INTERVAL_MS = 3000;

const statusEl = document.getElementById("status");

function setStatus(text, cls) {
  statusEl.textContent = text;
  statusEl.className = `status ${cls || ""}`;
}

function markFor(value) {
  // true = collected/owned, false = not yet, null = flag not mapped yet
  if (value === true) return { cls: "yes", glyph: "✓" };
  if (value === false) return { cls: "no", glyph: "○" };
  return { cls: "unknown", glyph: "?" };
}

// Only https links, so a bad paste can't become a javascript: URL
function videoLink(url) {
  if (!url || !url.startsWith("https://")) return "";
  return `<a class="video" href="${url}" target="_blank" rel="noopener" title="Watch on YouTube">▶</a>`;
}

// rows: [{name, collected, region?, source?}] -- collected null = flag not mapped yet
function renderChecklist(listEl, countEl, rows) {
  listEl.innerHTML = "";
  for (const row of rows) {
    const li = document.createElement("li");
    const mark = markFor(row.collected);
    li.className = mark.cls;
    li.innerHTML = `<span class="mark ${mark.cls}">${mark.glyph}</span>` +
                    `<span class="item-name">${row.name || "(unnamed)"}` +
                    (row.region ? `<span class="item-region">${row.region}</span>` : "") +
                    `</span>` +
                    (row.source ? `<span class="source">${row.source}</span>` : "") +
                    videoLink(row.video);
    listEl.appendChild(li);
  }
  const done = rows.filter((r) => r.collected === true).length;
  const unmapped = rows.filter((r) => r.collected === null).length;
  if (countEl) {
    countEl.textContent = `${done} / ${rows.length}` + (unmapped ? ` · ${unmapped} unmapped` : "");
  }
  return done;
}

function renderTotal(valueEl, barEl, done, total) {
  valueEl.innerHTML = `${done} <small>/ ${total}</small>`;
  barEl.style.width = `${total ? (done / total) * 100 : 0}%`;
}

function renderQuantities(listEl, quantities) {
  listEl.innerHTML = "";
  for (const [name, info] of Object.entries(quantities)) {
    const pct = info.target > 0 ? Math.min(100, (info.have / info.target) * 100) : 0;
    const li = document.createElement("li");
    if (info.checkbox) {
      const mark = markFor(info.complete);
      li.innerHTML = `<div class="bar-label"><span>${name}</span><span class="mark ${mark.cls}">${mark.glyph}</span></div>`;
      listEl.appendChild(li);
      continue;
    }
    li.innerHTML = `
      <div class="bar-label"><span>${name}</span><span>${info.have} / ${info.target}</span></div>
      <div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div>
    `;
    listEl.appendChild(li);
  }
}

let selectedSlot = null;
let lastData = null;

try { selectedSlot = localStorage.getItem("selectedSlot"); } catch (e) { /* storage unavailable */ }

function slotLabel(id, entry) {
  const ng = entry.stats && entry.stats.ng_plus;
  const base = `Slot ${Number(id) + 1}`;
  return ng === undefined ? base : `${base} · ${ng === 0 ? "NG" : "NG+" + ng}`;
}

function renderTabs(slots) {
  const nav = document.getElementById("slot-tabs");
  nav.innerHTML = "";
  for (const [id, entry] of Object.entries(slots)) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "tab" + (id === selectedSlot ? " active" : "");
    btn.textContent = slotLabel(id, entry);
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

  const report = slots[selectedSlot].report;
  const beads = renderChecklist(
    document.getElementById("beads-list"),
    document.getElementById("beads-count"),
    report.prayer_beads
  );
  const gourds = renderChecklist(
    document.getElementById("gourds-list"),
    document.getElementById("gourds-count"),
    report.gourd_seeds
  );
  renderTotal(document.getElementById("beads-total"), document.getElementById("beads-bar"),
              beads, report.prayer_beads.length);
  renderTotal(document.getElementById("gourds-total"), document.getElementById("gourds-bar"),
              gourds, report.gourd_seeds.length);
  renderChecklist(
    document.getElementById("tools-list"),
    document.getElementById("tools-count"),
    Object.entries(report.prosthetic_tools.owned).map(([name, collected]) => ({ name, collected }))
  );
  renderQuantities(
    document.getElementById("quantities-list"),
    report.quantity_targets
  );
}

async function refreshState() {
  try {
    const res = await fetch("/api/state");
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      setStatus(body.error || `error ${res.status}`, "error");
      return;
    }
    lastData = await res.json();
    setStatus("connected", "ok");
    renderAll();
  } catch (err) {
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

  for (const ending of data.endings) {
    const doneCount = ending.requirements.filter((r) => r.checked).length;
    const block = document.createElement("div");
    block.className = "ending";
    block.innerHTML = `<h3><span>${ending.name}${videoLink(ending.video)}</span><span class="count">${doneCount} / ${ending.requirements.length}</span></h3>`;

    const ul = document.createElement("ul");
    for (const req of ending.requirements) {
      const li = document.createElement("li");
      const checkboxId = `req-${req.id}`;
      li.innerHTML = `<input type="checkbox" id="${checkboxId}" ${req.checked ? "checked" : ""}>` +
                      `<label for="${checkboxId}">${req.text}</label>`;
      ul.appendChild(li);

      li.querySelector("input").addEventListener("change", async (event) => {
        await toggleRequirement(req.id, event.target.checked);
        loadEndings(); // refresh counts
      });
    }
    block.appendChild(ul);
    container.appendChild(block);
  }
}

refreshState();
loadEndings();
setInterval(refreshState, POLL_INTERVAL_MS);

// Lets SekiroApp.py shut down when this tab closes (404/405 under plain server.py, harmless)
addEventListener("pagehide", () => navigator.sendBeacon("/api/bye"));
