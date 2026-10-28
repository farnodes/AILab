const STATUS_LABELS = {
  not_started: "Not started",
  in_progress: "In progress",
  done: "Done",
};

let curriculum = null;
let progress = null;

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
  if (progress.updatedAt) {
    hint.textContent = `Loaded from learner/progress.json · ${new Date(
      progress.updatedAt
    ).toLocaleString()}`;
  }
  renderGlobalResources();
  renderDayNav();
  renderDay(progress.activeDayId || curriculum.days[0]?.id);
}

function repoHref(path) {
  return `/reader.html?path=${encodeURIComponent(path)}`;
}

function renderGlobalResources() {
  const ul = document.getElementById("global-resources");
  ul.innerHTML = "";
  for (const r of curriculum.resources || []) {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.href = repoHref(r.path);
    a.textContent = r.label;
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
  const firstOpen = steps.findIndex(
    (s) => stepStatus(dp, s.id) !== "done"
  );
  return firstOpen >= 0 ? firstOpen : steps.length - 1;
}

function renderDayNav() {
  const nav = document.getElementById("day-nav");
  if (!nav) return;

  nav.innerHTML = "";
  const active = progress.activeDayId;
  const phases = getPhases();

  for (const mod of phases) {
    const details = document.createElement("details");
    details.className = "phase-group";
    const days = daysInPhase(mod.phase);
    const hasActiveDay = days.some((d) => d.id === active);
    const stored = sessionStorage.getItem(`phase-open-${mod.phase}`);
    details.open =
      stored === "1" || (stored !== "0" && (hasActiveDay || mod.phase === 0));

    const summary = document.createElement("summary");
    summary.className = "phase-heading";
    summary.textContent = phaseHeading(mod);

    const daysWrap = document.createElement("div");
    daysWrap.className = "phase-days";

    if (!days.length) {
      const empty = document.createElement("p");
      empty.className = "phase-empty muted";
      empty.textContent = "Days coming soon";
      daysWrap.appendChild(empty);
    } else {
      for (const day of days) {
        const dp = dayProgress(day.id);
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "day-link" + (day.id === active ? " active" : "");
        btn.innerHTML = `<span>Day ${day.number} · ${day.title}</span><span class="badge ${dp.status}">${STATUS_LABELS[dp.status] || dp.status}</span>`;
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

async function selectDay(dayId) {
  await patchProgress({ dayId, activeDayId: dayId });
  renderDayNav();
  renderDay(dayId);
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
  const when = progress.updatedAt
    ? new Date(progress.updatedAt).toLocaleString()
    : "ok";
  el.textContent = `Saved to disk · ${when}`;
  return true;
}

function allStepsNotStarted(dp, day) {
  return (day.steps || []).every(
    (s) => (dp.steps?.[String(s.id)] || "not_started") === "not_started"
  );
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
    renderDayNav();
    renderDay(dayId, 0);
  });

  wrap.appendChild(resetBtn);
  wrap.appendChild(confirm);
  dayRow.appendChild(wrap);
}

function statusSelect(value, onChange) {
  const sel = document.createElement("select");
  sel.className = "status-select";
  for (const [k, label] of Object.entries(STATUS_LABELS)) {
    const opt = document.createElement("option");
    opt.value = k;
    opt.textContent = label;
    if (k === value) opt.selected = true;
    sel.appendChild(opt);
  }
  sel.addEventListener("change", () => onChange(sel.value));
  return sel;
}

function renderStepCard(day, dayId, step, dp) {
  const st = stepStatus(dp, step.id);
  const card = document.createElement("article");
  card.className = "step";
  const head = document.createElement("div");
  head.className = "step-head";
  const h3 = document.createElement("h3");
  h3.innerHTML = `<span class="step-num">${step.id}</span>${step.title}`;
  head.appendChild(h3);
  head.appendChild(
    statusSelect(st, async (v) => {
      const ok = await patchProgress({
        dayId,
        stepId: step.id,
        stepStatus: v,
        currentStepId: String(step.id),
      });
      if (ok) {
        renderDayNav();
        renderDay(dayId);
      }
    })
  );
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
  const parts = (step.body || "").split(/\n\n+/).filter(Boolean);
  if (parts.length === 0) {
    bodyWrap.appendChild(document.createElement("p"));
  } else {
    for (const para of parts) {
      const p = document.createElement("p");
      p.textContent = para;
      bodyWrap.appendChild(p);
    }
  }
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
    for (const cmd of step.commands) {
      const li = document.createElement("li");
      const code = document.createElement("code");
      code.textContent = cmd;
      li.appendChild(code);
      ul.appendChild(li);
    }
    card.appendChild(ul);
  }
  if (step.outcome) {
    const out = document.createElement("p");
    out.className = "step-outcome";
    out.textContent = `Success check: ${step.outcome}`;
    card.appendChild(out);
  }
  if (step.links?.length) {
    const links = document.createElement("div");
    links.className = "step-links";
    for (const link of step.links) {
      const a = document.createElement("a");
      a.href = repoHref(link.path);
      a.textContent = link.label;
      links.appendChild(a);
      links.appendChild(document.createTextNode(" · "));
    }
    card.appendChild(links);
  }
  return card;
}

async function goToStep(dayId, day, index) {
  const step = day.steps[index];
  if (!step) return;
  await patchProgress({ dayId, currentStepId: String(step.id) });
  renderDay(dayId, index);
}

function renderDay(dayId, stepIndexOverride) {
  const day = curriculum.days.find((d) => d.id === dayId);
  const main = document.getElementById("main");
  if (!day) {
    main.innerHTML = "<p class='error'>Day not found</p>";
    return;
  }

  const dp = dayProgress(dayId);
  const steps = day.steps || [];
  const stepIndex =
    stepIndexOverride !== undefined
      ? stepIndexOverride
      : resolveStepIndex(day, dp);
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
  prevBtn.addEventListener("click", () => goToStep(dayId, day, stepIndex - 1));

  const counter = document.createElement("span");
  counter.className = "pager-counter";
  counter.textContent = `Step ${stepIndex + 1} of ${steps.length}`;

  const nextBtn = document.createElement("button");
  nextBtn.type = "button";
  nextBtn.className = "pager-btn";
  nextBtn.textContent = "Next";
  nextBtn.disabled = stepIndex >= steps.length - 1;
  nextBtn.addEventListener("click", () => goToStep(dayId, day, stepIndex + 1));

  const dots = document.createElement("div");
  dots.className = "step-dots";
  steps.forEach((s, i) => {
    const dot = document.createElement("button");
    dot.type = "button";
    const st = stepStatus(dp, s.id);
    dot.className = `step-dot status-${st}`;
    dot.title = `Step ${s.id}: ${s.title} (${STATUS_LABELS[st]})`;
    if (i === stepIndex) dot.classList.add("active");
    dot.addEventListener("click", () => goToStep(dayId, day, i));
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
  if (step) {
    stepsEl.appendChild(renderStepCard(day, dayId, step, dp));
  }
  frag.appendChild(stepsEl);

  const actions = document.createElement("div");
  actions.className = "step-actions";
  const markDone = document.createElement("button");
  markDone.type = "button";
  markDone.className = "pager-btn primary";
  markDone.textContent =
    stepStatus(dp, step?.id) === "done" ? "Marked done" : "Mark step done";
  markDone.disabled = stepStatus(dp, step?.id) === "done";
  markDone.addEventListener("click", async () => {
    if (!step) return;
    const ok = await patchProgress({
      dayId,
      stepId: step.id,
      stepStatus: "done",
      currentStepId: String(step.id),
    });
    if (!ok) return;
    renderDayNav();
    const dp2 = dayProgress(dayId);
    const nextIdx = steps.findIndex((s) => stepStatus(dp2, s.id) !== "done");
    if (nextIdx >= 0 && nextIdx !== stepIndex) {
      await patchProgress({
        dayId,
        currentStepId: String(steps[nextIdx].id),
      });
      renderDay(dayId, nextIdx);
    } else {
      renderDay(dayId, stepIndex);
    }
  });
  actions.appendChild(markDone);
  frag.appendChild(actions);

  main.innerHTML = "";
  main.appendChild(frag);
}

load().catch((e) => {
  document.getElementById("main").innerHTML = `<p class="error">${e.message}</p>`;
});
