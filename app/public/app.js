import { renderMarkdown } from "./markdown.js";

const COPY_ICON = `<svg class="copy-icon" width="16" height="16" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>`;
const CHECK_ICON = `<svg class="copy-icon" width="16" height="16" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z"/></svg>`;

/** Lines that end with \\ are one shell command split for the curriculum file. */
function groupCommands(commands) {
  const groups = [];
  let buf = [];
  for (const cmd of commands) {
    buf.push(cmd);
    if (!cmd.trimEnd().endsWith("\\")) {
      groups.push(buf.join("\n"));
      buf = [];
    }
  }
  if (buf.length) groups.push(buf.join("\n"));
  return groups;
}

const STATUS_LABELS = {
  not_started: "Not started",
  in_progress: "In progress",
  done: "Done",
};

let curriculum = null;
let progress = null;
let viewingDayId = null;
let openSeq = 0;

function getPhases() {
  const list = curriculum.phases || curriculum.modules || [];
  if (list.length) {
    return [...list].sort((a, b) => a.phase - b.phase);
  }
  const byPhase = new Map();
  for (const day of curriculum.days || []) {
    if (!byPhase.has(day.phase)) {
      byPhase.set(day.phase, {
        phase: day.phase,
        name: day.phaseLabel || `Phase ${day.phase}`,
      });
    }
  }
  return [...byPhase.values()].sort((a, b) => a.phase - b.phase);
}

function phaseHeading(mod) {
  return `Phase ${mod.phase} — ${mod.name}`;
}

function daysInPhase(phase) {
  return (curriculum.days || [])
    .filter((d) => d.phase === phase)
    .sort((a, b) => a.number - b.number);
}

function dayById(dayId) {
  return (curriculum.days || []).find((d) => d.id === dayId) || null;
}

function repoFileUrl(path) {
  return `/repo/${path.split("/").filter(Boolean).map(encodeURIComponent).join("/")}`;
}

function savedLabel(whenIso) {
  if (!whenIso) return "Progress stays on this computer.";
  return `Saved · ${new Date(whenIso).toLocaleString()}`;
}

async function load() {
  const [cRes, pRes] = await Promise.all([
    fetch("/api/curriculum"),
    fetch("/api/progress"),
  ]);
  if (!cRes.ok || !pRes.ok) throw new Error("Failed to load API");
  curriculum = await cRes.json();
  progress = await pRes.json();
  document.getElementById("subtitle").textContent = curriculum.subtitle || "";
  const hint = document.getElementById("save-status");
  hint.textContent = savedLabel(progress.updatedAt);
  renderGlobalResources();
  renderContinue();

  const params = new URLSearchParams(location.search);
  const urlDay = params.get("day");
  const urlStep = params.get("step");
  const startId =
    urlDay && dayById(urlDay)
      ? urlDay
      : progress.activeDayId || curriculum.days[0]?.id;
  const startDay = dayById(startId);
  let stepIndex;
  if (startDay && urlStep && startId === urlDay) {
    const found = startDay.steps.findIndex((s) => String(s.id) === String(urlStep));
    if (found >= 0) stepIndex = found;
  }
  await openDay(startId, stepIndex);
}

function renderContinue() {
  const day = dayById(progress.activeDayId) || curriculum.days?.[0];
  const btn = document.getElementById("continue-btn");
  if (!day) {
    btn.hidden = true;
    return;
  }
  btn.hidden = false;
  btn.textContent = `Continue · Day ${day.number}`;
}

function renderGlobalResources() {
  const ul = document.getElementById("global-resources");
  ul.innerHTML = "";
  for (const r of curriculum.resources || []) {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.href = repoFileUrl(r.path);
    a.textContent = r.label;
    a.addEventListener("click", (e) => {
      e.preventDefault();
      openDoc(r.path);
    });
    li.appendChild(a);
    ul.appendChild(li);
  }
}

function dayProgress(dayId) {
  return progress.days?.[dayId] || { status: "not_started", steps: {} };
}

function stepStatus(dp, stepId) {
  return dp.steps?.[String(stepId)] || "not_started";
}

function resolveStepIndex(day, dp) {
  const steps = day.steps || [];
  const saved = dp.currentStepId;
  if (saved) {
    const idx = steps.findIndex((s) => String(s.id) === String(saved));
    if (idx >= 0) return idx;
  }
  return firstOpenIndex(day, dp);
}

function firstOpenIndex(day, dp) {
  const steps = day.steps || [];
  const firstOpen = steps.findIndex((s) => stepStatus(dp, s.id) !== "done");
  return firstOpen >= 0 ? firstOpen : Math.max(steps.length - 1, 0);
}

function closeNav() {
  document.getElementById("layout").classList.remove("nav-open");
}

function renderDayNav() {
  const nav = document.getElementById("day-nav");
  if (!nav) return;

  nav.innerHTML = "";
  const phases = getPhases();

  for (const mod of phases) {
    const details = document.createElement("details");
    details.className = "phase-group";
    const days = daysInPhase(mod.phase);
    const hasViewed = days.some((d) => d.id === viewingDayId);
    const stored = sessionStorage.getItem(`phase-open-${mod.phase}`);
    details.open =
      stored === "1" || (stored !== "0" && (hasViewed || mod.phase === 0));

    const summary = document.createElement("summary");
    summary.className = "phase-heading";
    summary.textContent = phaseHeading(mod);

    const daysWrap = document.createElement("div");
    daysWrap.className = "phase-days";

    if (!days.length) {
      const empty = document.createElement("p");
      empty.className = "phase-empty muted";
      empty.textContent = "Days coming soon";
      const guide = document.createElement("button");
      guide.type = "button";
      guide.className = "phase-guide";
      guide.textContent = "Read the chapter";
      guide.addEventListener("click", () => {
        openDoc(`docs/guides/phase${mod.phase}.md`);
      });
      daysWrap.appendChild(empty);
      daysWrap.appendChild(guide);
    } else {
      for (const day of days) {
        const dp = dayProgress(day.id);
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "day-link" + (day.id === viewingDayId ? " active" : "");
        if (day.id === progress.activeDayId && day.id !== viewingDayId) {
          btn.classList.add("resume");
        }
        const title = document.createElement("span");
        title.className = "day-title";
        title.textContent = `Day ${day.number} · ${day.title}`;
        const dot = document.createElement("span");
        dot.className = `status-dot ${dp.status}`;
        dot.title = STATUS_LABELS[dp.status] || dp.status;
        dot.setAttribute("aria-label", STATUS_LABELS[dp.status] || dp.status);
        btn.appendChild(title);
        btn.appendChild(dot);
        btn.addEventListener("click", () => selectDay(day.id));
        daysWrap.appendChild(btn);
      }
    }

    details.appendChild(summary);
    details.appendChild(daysWrap);
    details.addEventListener("toggle", () => {
      sessionStorage.setItem(
        `phase-open-${mod.phase}`,
        details.open ? "1" : "0"
      );
    });
    nav.appendChild(details);
  }
}

function selectDay(dayId) {
  closeNav();
  return openDay(dayId);
}

function continueLearning() {
  closeNav();
  const dayId = progress.activeDayId || curriculum.days[0]?.id;
  const day = dayById(dayId);
  if (!day) return;
  const idx = firstOpenIndex(day, dayProgress(dayId));
  return openDay(dayId, idx);
}

async function patchProgress(body) {
  const el = document.getElementById("save-status");
  el.textContent = "Saving…";
  el.classList.remove("error");
  let res;
  try {
    res = await fetch("/api/progress", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } catch {
    el.textContent = "Save failed — is ./lab-ui.sh running?";
    el.classList.add("error");
    return false;
  }
  if (!res.ok) {
    let msg = `Save failed (${res.status})`;
    try {
      const err = await res.json();
      if (err.error) msg = err.error;
    } catch {
      /* ignore */
    }
    el.textContent = msg;
    el.classList.add("error");
    return false;
  }
  progress = await res.json();
  el.textContent = savedLabel(progress.updatedAt);
  renderContinue();
  return true;
}

function allStepsNotStarted(dp, day) {
  return (day.steps || []).every(
    (s) => (dp.steps?.[String(s.id)] || "not_started") === "not_started"
  );
}

function rememberView(dayId, step) {
  viewingDayId = dayId;
  const q = new URLSearchParams({ day: dayId });
  if (step) q.set("step", String(step.id));
  history.replaceState(null, "", `/?${q.toString()}`);
}

async function openDay(dayId, stepIndex) {
  const seq = ++openSeq;
  const day = dayById(dayId);
  if (!day) return;
  const dp = dayProgress(dayId);
  const idx =
    stepIndex !== undefined && stepIndex !== null
      ? stepIndex
      : resolveStepIndex(day, dp);
  const step = (day.steps || [])[idx];
  const patch = {};
  if (step && stepStatus(dp, step.id) === "not_started") {
    patch.dayId = dayId;
    patch.stepId = step.id;
    patch.stepStatus = "in_progress";
    patch.currentStepId = String(step.id);
  } else if (step && String(dp.currentStepId || "") !== String(step.id)) {
    patch.dayId = dayId;
    patch.currentStepId = String(step.id);
  }
  if (Object.keys(patch).length) {
    const ok = await patchProgress(patch);
    if (seq !== openSeq) return;
    if (!ok) {
      rememberView(dayId, step);
      renderDayNav();
      renderDay(dayId, idx);
      return;
    }
  }
  if (seq !== openSeq) return;
  rememberView(dayId, step);
  renderDayNav();
  renderDay(dayId, idx);
}

function attachResetControl(dayRow, dayId, day) {
  const wrap = document.createElement("div");
  wrap.className = "reset-wrap";

  const resetBtn = document.createElement("button");
  resetBtn.type = "button";
  resetBtn.className = "reset-day-btn";
  resetBtn.setAttribute("aria-label", `Reset Day ${day.number} progress`);
  resetBtn.innerHTML = `<svg class="reset-icon" width="16" height="16" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6 0 1.01-.25 1.97-.7 2.8l1.46 1.46A7.93 7.93 0 0 0 20 13c0-4.42-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6 0-1.01.25-1.97.7-2.8L5.24 9.74A7.93 7.93 0 0 0 4 13c0 4.42 3.58 8 8 8v4l5-5-5-5v4z"/></svg>`;

  const confirm = document.createElement("div");
  confirm.className = "reset-confirm hidden";
  confirm.innerHTML = `<span class="reset-confirm-text">Reset this day?</span>`;
  const yes = document.createElement("button");
  yes.type = "button";
  yes.className = "pager-btn reset-yes";
  yes.textContent = "Yes";
  const no = document.createElement("button");
  no.type = "button";
  no.className = "pager-btn reset-no";
  no.textContent = "No";
  confirm.appendChild(yes);
  confirm.appendChild(no);

  function closeConfirm() {
    confirm.classList.add("hidden");
    resetBtn.classList.remove("hidden");
  }

  resetBtn.addEventListener("click", () => {
    resetBtn.classList.add("hidden");
    confirm.classList.remove("hidden");
  });

  no.addEventListener("click", closeConfirm);

  yes.addEventListener("click", async () => {
    closeConfirm();
    const saved = await patchProgress({ dayId, resetDay: true });
    if (!saved) return;
    const dp2 = dayProgress(dayId);
    if (!allStepsNotStarted(dp2, day)) {
      const el = document.getElementById("save-status");
      el.textContent =
        "Reset ignored — stop and restart ./lab-ui.sh, then try again.";
      el.classList.add("error");
      return;
    }
    await openDay(dayId, 0);
  });

  wrap.appendChild(resetBtn);
  wrap.appendChild(confirm);
  dayRow.appendChild(wrap);
}

function appendBody(container, body) {
  const parts = (body || "").split(/\n\n+/).filter(Boolean);
  if (!parts.length) {
    container.appendChild(document.createElement("p"));
    return;
  }
  for (const para of parts) {
    const lines = para.split("\n");
    const numbered = [];
    const prose = [];
    for (const line of lines) {
      if (/^\d+[.)]\s+/.test(line.trim())) numbered.push(line.trim());
      else if (line.trim()) prose.push(line.trim());
    }
    if (numbered.length >= 2) {
      for (const line of prose) {
        const p = document.createElement("p");
        p.textContent = line;
        container.appendChild(p);
      }
      const ol = document.createElement("ol");
      ol.className = "step-tasks";
      for (const line of numbered) {
        const li = document.createElement("li");
        li.textContent = line.replace(/^\d+[.)]\s+/, "");
        ol.appendChild(li);
      }
      container.appendChild(ol);
    } else {
      const p = document.createElement("p");
      p.textContent = para;
      container.appendChild(p);
    }
  }
}

function renderStepCard(day, dayId, step, dp) {
  const card = document.createElement("article");
  card.className = "step";
  const head = document.createElement("div");
  head.className = "step-head";
  const h3 = document.createElement("h3");
  h3.innerHTML = `<span class="step-num">${step.id}</span>${step.title}`;
  head.appendChild(h3);
  const st = stepStatus(dp, step.id);
  const label = document.createElement("span");
  label.className = `badge ${st}`;
  label.textContent = STATUS_LABELS[st] || st;
  head.appendChild(label);
  card.appendChild(head);
  if (step.durationMinutes) {
    const d = document.createElement("p");
    d.className = "muted";
    d.textContent = `~${step.durationMinutes} min`;
    card.appendChild(d);
  }
  if (step.journalGuide) {
    const jHead = document.createElement("p");
    jHead.className = "journal-label";
    jHead.textContent = "Read first — journal guide";
    card.appendChild(jHead);
    const guide = document.createElement("div");
    guide.className = "step-journal-guide";
    for (const para of step.journalGuide.split(/\n\n+/).filter(Boolean)) {
      const p = document.createElement("p");
      p.textContent = para;
      guide.appendChild(p);
    }
    card.appendChild(guide);
  }
  const bodyWrap = document.createElement("div");
  bodyWrap.className = "step-body";
  appendBody(bodyWrap, step.body || "");
  card.appendChild(bodyWrap);
  if (step.why) {
    const why = document.createElement("p");
    why.className = "why";
    why.textContent = step.why;
    card.appendChild(why);
  }
  if (step.commands?.length) {
    const ul = document.createElement("ul");
    ul.className = "commands";
    for (const cmd of groupCommands(step.commands)) {
      const li = document.createElement("li");
      li.className = "command-line";
      const code = document.createElement("code");
      code.textContent = cmd;
      const copy = document.createElement("button");
      copy.type = "button";
      copy.className = "copy-btn";
      copy.setAttribute("aria-label", "Copy command");
      copy.title = "Copy command";
      copy.innerHTML = COPY_ICON;
      copy.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(cmd);
          copy.innerHTML = CHECK_ICON;
          copy.setAttribute("aria-label", "Copied");
          copy.title = "Copied";
        } catch {
          copy.setAttribute("aria-label", "Copy failed");
          copy.title = "Copy failed";
        }
        setTimeout(() => {
          copy.innerHTML = COPY_ICON;
          copy.setAttribute("aria-label", "Copy command");
          copy.title = "Copy command";
        }, 1200);
      });
      li.appendChild(code);
      li.appendChild(copy);
      ul.appendChild(li);
    }
    card.appendChild(ul);
  }
  if (step.links?.length) {
    const links = document.createElement("div");
    links.className = "step-links";
    step.links.forEach((link, i) => {
      if (i) links.appendChild(document.createTextNode(" · "));
      const a = document.createElement("a");
      a.href = repoFileUrl(link.path);
      a.textContent = link.label;
      a.addEventListener("click", (e) => {
        e.preventDefault();
        openDoc(link.path);
      });
      links.appendChild(a);
    });
    card.appendChild(links);
  }
  return card;
}

function renderDay(dayId, stepIndexOverride) {
  const day = dayById(dayId);
  const main = document.getElementById("main");
  if (!day) {
    main.innerHTML = "<p class='error'>Day not found</p>";
    return;
  }

  const dp = dayProgress(dayId);
  const steps = day.steps || [];
  const stepIndex =
    stepIndexOverride !== undefined ? stepIndexOverride : resolveStepIndex(day, dp);
  const step = steps[stepIndex];
  const doneCount = steps.filter((s) => stepStatus(dp, s.id) === "done").length;

  const frag = document.createDocumentFragment();
  const header = document.createElement("div");
  header.className = "day-header";
  header.innerHTML = `
    <div class="meta">
      <span>Phase ${day.phase} · ${day.phaseLabel || ""}</span>
      <span>~${day.timeBoxMinutes} min</span>
      <span>${doneCount} / ${steps.length} steps done</span>
    </div>
    <h2>Day ${day.number} — ${day.title}</h2>
    <p>${day.summary || ""}</p>
  `;

  const dayRow = document.createElement("div");
  dayRow.className = "day-status-row";
  const dayLabel = document.createElement("span");
  dayLabel.className = "day-status-label";
  dayLabel.textContent = "Day progress";
  const badge = document.createElement("span");
  badge.className = `badge day-badge ${dp.status}`;
  badge.textContent = STATUS_LABELS[dp.status] || dp.status;
  dayRow.appendChild(dayLabel);
  dayRow.appendChild(badge);
  if (dp.status === "done") {
    const note = document.createElement("span");
    note.className = "muted day-done-note";
    note.textContent = "All steps completed.";
    dayRow.appendChild(note);
  }
  attachResetControl(dayRow, dayId, day);
  header.appendChild(dayRow);
  frag.appendChild(header);

  if (day.reference && stepIndex === 0) {
    const ref = document.createElement("div");
    ref.className = "ref-card";
    ref.innerHTML = "<strong>Quick reference</strong>";
    const dl = document.createElement("dl");
    for (const [k, v] of Object.entries(day.reference)) {
      const dt = document.createElement("dt");
      dt.textContent = k;
      const dd = document.createElement("dd");
      dd.textContent = v;
      dl.appendChild(dt);
      dl.appendChild(dd);
    }
    ref.appendChild(dl);
    frag.appendChild(ref);
  }

  const pager = document.createElement("nav");
  pager.className = "step-pagination";
  pager.setAttribute("aria-label", "Steps");

  const prevBtn = document.createElement("button");
  prevBtn.type = "button";
  prevBtn.className = "pager-btn";
  prevBtn.textContent = "Previous";
  prevBtn.disabled = stepIndex <= 0;
  prevBtn.addEventListener("click", () => openDay(dayId, stepIndex - 1));

  const counter = document.createElement("span");
  counter.className = "pager-counter";
  counter.textContent = `Step ${stepIndex + 1} of ${steps.length}`;

  const nextBtn = document.createElement("button");
  nextBtn.type = "button";
  nextBtn.className = "pager-btn";
  nextBtn.textContent = "Next";
  nextBtn.disabled = stepIndex >= steps.length - 1;
  nextBtn.addEventListener("click", () => openDay(dayId, stepIndex + 1));

  const dots = document.createElement("div");
  dots.className = "step-dots";
  steps.forEach((s, i) => {
    const dot = document.createElement("button");
    dot.type = "button";
    const st = stepStatus(dp, s.id);
    dot.className = `step-dot status-${st}`;
    dot.textContent = st === "done" ? "✓" : String(i + 1);
    dot.title = `Step ${s.id}: ${s.title} (${STATUS_LABELS[st]})`;
    dot.setAttribute(
      "aria-label",
      `Step ${i + 1}: ${s.title} (${STATUS_LABELS[st]})`
    );
    if (i === stepIndex) dot.classList.add("active");
    dot.addEventListener("click", () => openDay(dayId, i));
    dots.appendChild(dot);
  });

  const pagerMid = document.createElement("div");
  pagerMid.className = "pager-mid";
  pagerMid.appendChild(counter);
  pagerMid.appendChild(dots);

  pager.appendChild(prevBtn);
  pager.appendChild(pagerMid);
  pager.appendChild(nextBtn);
  frag.appendChild(pager);

  const stepsEl = document.createElement("div");
  stepsEl.className = "steps steps-single";
  if (step) stepsEl.appendChild(renderStepCard(day, dayId, step, dp));
  frag.appendChild(stepsEl);

  const actions = document.createElement("div");
  actions.className = "step-actions";
  if (step?.outcome) {
    const out = document.createElement("p");
    out.className = "step-outcome";
    out.textContent = `Success check: ${step.outcome}`;
    actions.appendChild(out);
  }
  const markDone = document.createElement("button");
  markDone.type = "button";
  markDone.className = "pager-btn primary";
  markDone.textContent =
    step && stepStatus(dp, step.id) === "done" ? "Marked done" : "Mark step done";
  markDone.disabled = !step || stepStatus(dp, step.id) === "done";
  markDone.addEventListener("click", async () => {
    if (!step) return;
    const ok = await patchProgress({
      dayId,
      activeDayId: dayId,
      stepId: step.id,
      stepStatus: "done",
      currentStepId: String(step.id),
    });
    if (!ok) return;
    renderDayNav();
    const dp2 = dayProgress(dayId);
    const nextIdx = steps.findIndex((s) => stepStatus(dp2, s.id) !== "done");
    if (nextIdx >= 0) await openDay(dayId, nextIdx);
    else await openDay(dayId, stepIndex);
  });
  actions.appendChild(markDone);
  frag.appendChild(actions);

  main.innerHTML = "";
  main.appendChild(frag);
}

function readerPageHref(path) {
  const q = new URLSearchParams({ path });
  if (viewingDayId) q.set("day", viewingDayId);
  const day = dayById(viewingDayId);
  const stepId = new URLSearchParams(location.search).get("step");
  if (stepId) q.set("step", stepId);
  else if (day) {
    const dp = dayProgress(viewingDayId);
    if (dp.currentStepId) q.set("step", String(dp.currentStepId));
  }
  return `/reader.html?${q.toString()}`;
}

function resolveDocPath(base, rel) {
  const stack = base.split("/").filter(Boolean).slice(0, -1);
  for (const part of rel.split("/")) {
    if (!part || part === ".") continue;
    if (part === "..") stack.pop();
    else stack.push(decodeURIComponent(part));
  }
  return stack.join("/");
}

function bindDocLinks(root, basePath) {
  root.querySelectorAll("a").forEach((a) => {
    const href = a.getAttribute("href") || "";
    if (!href.startsWith("/reader.html")) return;
    a.addEventListener("click", (e) => {
      e.preventDefault();
      let next = new URL(href, location.origin).searchParams.get("path");
      if (!next) return;
      if (next.startsWith(".")) next = resolveDocPath(basePath, next);
      openDoc(next);
    });
  });
}

async function openDoc(path) {
  const panel = document.getElementById("doc-panel");
  const body = document.getElementById("doc-body");
  const label = document.getElementById("doc-label");
  document.getElementById("layout").classList.add("with-doc");
  panel.hidden = false;
  label.textContent = path;
  document.getElementById("doc-full").href = readerPageHref(path);
  body.innerHTML = "<p class='muted'>Loading…</p>";
  try {
    const res = await fetch(repoFileUrl(path));
    if (!res.ok) throw new Error(`Could not load (${res.status})`);
    body.innerHTML = renderMarkdown(await res.text());
    bindDocLinks(body, path);
  } catch (e) {
    body.textContent = e.message;
    body.classList.add("error");
  }
}

function closeDoc() {
  document.getElementById("doc-panel").hidden = true;
  document.getElementById("layout").classList.remove("with-doc");
  document.getElementById("doc-body").classList.remove("error");
}

document.getElementById("continue-btn").addEventListener("click", () => {
  continueLearning();
});
document.getElementById("days-toggle").addEventListener("click", () => {
  document.getElementById("layout").classList.toggle("nav-open");
});
document.getElementById("nav-backdrop").addEventListener("click", closeNav);
document.getElementById("doc-close").addEventListener("click", closeDoc);

load().catch((e) => {
  document.getElementById("main").innerHTML = `<p class="error">${e.message}</p>`;
});
