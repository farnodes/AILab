/** Structured exercise submissions — validation + formatting. */

export function submissionQuestions(step) {
  const qs = step?.submissionQuestions;
  return Array.isArray(qs) && qs.length ? qs : null;
}

export function emptyAnswers(questions) {
  return Object.fromEntries(questions.map((q) => [q.id, ""]));
}

export function isMcqQuestion(q) {
  return q?.input === "mcq" && Array.isArray(q.options) && q.options.length > 0;
}

export function optionLabel(q, optionId) {
  if (!optionId) return "";
  for (const opt of q.options || []) {
    if (opt.id === optionId) return opt.label || optionId;
  }
  return optionId;
}

export function normalizeLoadedSubmission(data, questions) {
  if (questions) {
    const answers = { ...emptyAnswers(questions) };
    if (data?.answers && typeof data.answers === "object") {
      for (const q of questions) {
        const v = data.answers[q.id];
        if (typeof v === "string") answers[q.id] = v;
      }
    } else if (typeof data?.content === "string" && data.content.trim()) {
      answers[questions[0].id] = data.content;
    }
    return answers;
  }
  return null;
}

export function validateAnswers(questions, answers) {
  const fieldErrors = {};
  const messages = [];

  for (const q of questions) {
    const raw = answers[q.id];
    const val = typeof raw === "string" ? raw.trim() : "";
    const label = q.label || q.id;

    if (isMcqQuestion(q)) {
      const validIds = new Set((q.options || []).map((o) => o.id));
      if (q.required !== false && !val) {
        fieldErrors[q.id] = "Select one option.";
        messages.push(`${label}: required`);
        continue;
      }
      if (val && !validIds.has(val)) {
        fieldErrors[q.id] = "Invalid choice.";
        messages.push(`${label}: invalid option`);
        continue;
      }
      if (val && q.correctOptionId && val !== q.correctOptionId) {
        fieldErrors[q.id] = "Not quite—read the chapter and try another option.";
        messages.push(`${label}: incorrect`);
      }
      continue;
    }

    if (q.required !== false && !val) {
      fieldErrors[q.id] = "This answer is required.";
      messages.push(`${label}: required`);
      continue;
    }
    if (!val) continue;

    const minLen = q.minLength ?? 0;
    if (minLen && val.length < minLen) {
      fieldErrors[q.id] = `At least ${minLen} characters.`;
      messages.push(`${label}: too short`);
    }

    const maxLen = q.maxLength ?? 20_000;
    if (val.length > maxLen) {
      fieldErrors[q.id] = `At most ${maxLen} characters.`;
      messages.push(`${label}: too long`);
    }

    for (const needle of q.mustContain || []) {
      if (!String(needle).trim()) continue;
      if (!val.toLowerCase().includes(String(needle).toLowerCase())) {
        const msg = q.mustContainHint || `Include “${needle}”.`;
        fieldErrors[q.id] = fieldErrors[q.id]
          ? `${fieldErrors[q.id]} ${msg}`
          : msg;
        messages.push(`${label}: missing keyword`);
      }
    }
  }

  return { ok: Object.keys(fieldErrors).length === 0, fieldErrors, messages };
}

export function answersToProgressMarkdown(questions, answers) {
  const parts = [];
  for (const q of questions) {
    const val = (answers[q.id] || "").trim();
    if (!val) continue;
    const text = isMcqQuestion(q) ? optionLabel(q, val) : val;
    parts.push(`**${q.label}**\n\n${text}`);
  }
  return parts.join("\n\n");
}

export function answersToPlainText(questions, answers) {
  return questions
    .map((q) => {
      const val = (answers[q.id] || "").trim();
      if (!val) return "";
      const text = isMcqQuestion(q) ? optionLabel(q, val) : val;
      return `${q.label}\n${text}`;
    })
    .filter(Boolean)
    .join("\n\n");
}
