import { escapeHtml, renderMarkdown } from "./markdown.js";

function repoFetchPath(path) {
  return `/repo/${path.split("/").filter(Boolean).map(encodeURIComponent).join("/")}`;
}

function deriveDayStatus(dayEntry, dayDef) {
  if (!dayDef) return "untracked";
  const explicit = dayEntry?.status;
  const steps = dayEntry?.steps || {};
  const ids = (dayDef.steps || []).map((s) => String(s.id));
  const vals = ids.map((id) => steps[id] || "not_started");
  if (vals.length && vals.every((v) => v === "done")) return "done";
  if (vals.some((v) => v === "done" || v === "in_progress")) return "in_progress";
  if (explicit === "done") return "done";
  if (explicit === "in_progress") return "in_progress";
  return "not_started";
}

function progressCellHtml(dayNum, progress, curriculum) {
  const dayId = `day-${dayNum}`;
  const dayDef = curriculum?.days?.find((d) => d.id === dayId);
  const dayEntry = progress?.days?.[dayId] || {};
  const st = dayDef ? deriveDayStatus(dayEntry, dayDef) : "untracked";
  const labels = {
    done: "Done",
    in_progress: "In progress",
    not_started: "Not started",
    untracked: "Not in roadmap yet",
  };
  const label = labels[st] || st;
  if (dayDef) {
    return `<a class="prog-icon status-${st}" href="/?day=${encodeURIComponent(dayId)}" title="Day ${dayNum}: ${label}. Open this day" aria-label="Day ${dayNum}: ${label}. Open this day"></a>`;
  }
  return `<span class="prog-icon status-${st}" title="Day ${dayNum}: ${label}" aria-label="Day ${dayNum}: ${label}"></span>`;
}

function parseDayNumber(cellHtml) {
  const tmp = document.createElement("div");
  tmp.innerHTML = cellHtml;
  const text = tmp.textContent.trim();
  const m = text.match(/\*\*(\d+)\*\*/) || text.match(/^(\d+)$/);
  return m ? parseInt(m[1], 10) : null;
}

export function injectProgressColumns(root, progress, curriculum) {
  root.querySelectorAll("table").forEach((table) => {
    const headerRow = table.querySelector("thead tr");
    if (!headerRow) return;
    const headers = [...headerRow.querySelectorAll("th")].map((th) =>
      th.textContent.trim().toLowerCase()
    );
    if (headers.includes("progress")) return;
    const dayIdx = headers.indexOf("day");
    if (dayIdx === -1) return;

    const progTh = document.createElement("th");
    progTh.textContent = "Progress";
    headerRow.children[dayIdx].before(progTh);

    table.querySelectorAll("tbody tr").forEach((tr) => {
      const cells = tr.querySelectorAll("td");
      if (cells.length <= dayIdx) return;
      const dayCell = cells[dayIdx];
      const dayNum = parseDayNumber(dayCell.innerHTML);
      const td = document.createElement("td");
      td.className = "progress-cell";
      td.innerHTML =
        dayNum != null
          ? progressCellHtml(dayNum, progress, curriculum)
          : '<span class="prog-icon status-untracked" title="—" aria-hidden="true"></span>';
      dayCell.before(td);
    });
  });
}

export function refreshProgressCells(root, progress, curriculum) {
  root.querySelectorAll("td.progress-cell").forEach((td) => {
    const dayTd = td.nextElementSibling;
    if (!dayTd) return;
    const dayNum = parseDayNumber(dayTd.innerHTML);
    if (dayNum != null) {
      td.innerHTML = progressCellHtml(dayNum, progress, curriculum);
    }
  });
}

async function loadDocWithProgress(docPath) {
  const isDaily = docPath.replace(/\\/g, "/").endsWith("docs/guides/DAILY_30MIN.md");
  const fetches = [
    fetch(repoFetchPath(docPath)).then((r) => {
      if (!r.ok) throw new Error(`Could not load (${r.status})`);
      return r.text();
    }),
  ];
  if (isDaily) {
    fetches.push(
      fetch("/api/progress").then((r) => (r.ok ? r.json() : {})),
      fetch("/api/curriculum").then((r) => (r.ok ? r.json() : { days: [] }))
    );
  }
  const results = await Promise.all(fetches);
  const text = results[0];
  const progress = isDaily ? results[1] : null;
  const curriculum = isDaily ? results[2] : null;
  return { text, progress, curriculum, isDaily };
}

const params = new URLSearchParams(location.search);
const path = params.get("path");
const backDay = params.get("day");
const backStep = params.get("step");
if (backDay) {
  const back = new URLSearchParams({ day: backDay });
  if (backStep) back.set("step", backStep);
  const backLink = document.querySelector(".reader-bar .back");
  if (backLink) backLink.href = `/?${back.toString()}`;
}

if (!path || path.includes("..")) {
  document.getElementById("content").innerHTML =
    "<p class='error'>Missing or invalid path.</p>";
} else {
  document.getElementById("path-label").textContent = path;
  document.title = `${path} — AILab`;
  loadDocWithProgress(path)
    .then(({ text, progress, curriculum, isDaily }) => {
      const content = document.getElementById("content");
      content.innerHTML = renderMarkdown(text);
      if (isDaily) {
        injectProgressColumns(content, progress, curriculum);
        document.addEventListener("visibilitychange", () => {
          if (document.visibilityState !== "visible") return;
          fetch("/api/progress")
            .then((r) => (r.ok ? r.json() : null))
            .then((fresh) => {
              if (fresh) refreshProgressCells(content, fresh, curriculum);
            });
        });
      }
      content.querySelectorAll("a[href^='/reader.html']").forEach((a) => {
        a.addEventListener("click", (e) => {
          e.preventDefault();
          location.href = a.getAttribute("href");
        });
      });
    })
    .catch((e) => {
      document.getElementById("content").innerHTML = `<p class="error">${escapeHtml(e.message)}</p>`;
    });
}
