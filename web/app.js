const POLL_INTERVAL_MS = 3000;

const statusEl = document.getElementById("status");

function setStatus(text, cls) {
  statusEl.textContent = text;
  statusEl.className = `status ${cls || ""}`;
}

function markFor(value) {
  // true = collected/owned, false = not yet, null = flag not mapped yet
  if (value === true) return { cls: "yes", glyph: "✓" };
  if (value === false) return { cls: "no", glyph: "·" };
  return { cls: "unknown", glyph: "?" };
}

function renderChecklist(listEl, countEl, entries) {
  listEl.innerHTML = "";
  let done = 0;
  let mapped = 0;
  for (const [name, value] of entries) {
    if (value !== null) mapped += 1;
    if (value === true) done += 1;

    const li = document.createElement("li");
    const mark = markFor(value);
    li.innerHTML = `<span class="mark ${mark.cls}">${mark.glyph}</span>` +
                    `<span class="item-name">${name || "(unnamed)"}</span>`;
    listEl.appendChild(li);
  }
  if (countEl) {
    countEl.textContent = mapped > 0 ? `${done} / ${mapped} mapped` : "none mapped yet";
  }
}

function renderQuantities(listEl, quantities) {
  listEl.innerHTML = "";
  for (const [name, info] of Object.entries(quantities)) {
    const pct = info.target > 0 ? Math.min(100, (info.have / info.target) * 100) : 0;
    const li = document.createElement("li");
    li.innerHTML = `
      <div class="bar-label"><span>${name}</span><span>${info.have} / ${info.target}</span></div>
      <div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div>
    `;
    listEl.appendChild(li);
  }
}

function renderTools(listEl, countEl, owned) {
  const entries = Object.entries(owned).map(([name, isOwned]) => [name, isOwned]);
  renderChecklist(listEl, countEl, entries);
}

async function refreshState() {
  try {
    const res = await fetch("/api/state");
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      setStatus(body.error || `error ${res.status}`, "error");
      return;
    }
    const report = await res.json();
    setStatus("connected", "ok");

    renderChecklist(
      document.getElementById("beads-list"),
      document.getElementById("beads-count"),
      Object.entries(report.prayer_beads)
    );
    renderTools(
      document.getElementById("tools-list"),
      document.getElementById("tools-count"),
      report.prosthetic_tools.owned
    );
    renderQuantities(
      document.getElementById("quantities-list"),
      report.quantity_targets
    );
  } catch (err) {
    setStatus("server unreachable -- is server.py running?", "error");
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
    block.innerHTML = `<h3><span>${ending.name}</span><span class="count">${doneCount} / ${ending.requirements.length}</span></h3>`;

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
