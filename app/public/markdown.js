export function escapeHtml(s) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

export function readerHref(path) {
  return `/reader.html?path=${encodeURIComponent(path)}`;
}

/** Small markdown subset for lab docs (headings, lists, code, links, tables). */
export function renderMarkdown(source) {
  const lines = source.replace(/\r\n/g, "\n").split("\n");
  const out = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    if (/^```/.test(line)) {
      i++;
      const block = [];
      while (i < lines.length && !/^```/.test(lines[i])) {
        block.push(lines[i]);
        i++;
      }
      i++;
      out.push(`<pre><code>${escapeHtml(block.join("\n"))}</code></pre>`);
      continue;
    }

    if (/^\|.+\|$/.test(line) && i + 1 < lines.length && /^\|[-:| ]+\|$/.test(lines[i + 1])) {
      const rows = [];
      while (i < lines.length && /^\|.+\|$/.test(lines[i])) {
        if (!/^\|[-:| ]+\|$/.test(lines[i])) {
          const cells = lines[i]
            .slice(1, -1)
            .split("|")
            .map((c) => c.trim());
          rows.push(cells);
        }
        i++;
      }
      if (rows.length) {
        const [head, ...body] = rows;
        out.push(
          "<table><thead><tr>" +
            head.map((c) => `<th>${inline(c)}</th>`).join("") +
            "</tr></thead><tbody>"
        );
        for (const row of body) {
          out.push("<tr>" + row.map((c) => `<td>${inline(c)}</td>`).join("") + "</tr>");
        }
        out.push("</tbody></table>");
      }
      continue;
    }

    if (/^---+$/.test(line.trim())) {
      out.push("<hr />");
      i++;
      continue;
    }

    const h = line.match(/^(#{1,3})\s+(.*)$/);
    if (h) {
      const level = h[1].length;
      out.push(`<h${level}>${inline(h[2])}</h${level}>`);
      i++;
      continue;
    }

    if (/^[-*]\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^[-*]\s+/.test(lines[i])) {
        items.push(`<li>${inline(lines[i].replace(/^[-*]\s+/, ""))}</li>`);
        i++;
      }
      out.push(`<ul>${items.join("")}</ul>`);
      continue;
    }

    if (/^\d+\.\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^\d+\.\s+/.test(lines[i])) {
        items.push(`<li>${inline(lines[i].replace(/^\d+\.\s+/, ""))}</li>`);
        i++;
      }
      out.push(`<ol>${items.join("")}</ol>`);
      continue;
    }

    if (line.trim() === "") {
      i++;
      continue;
    }

    out.push(`<p>${inline(line)}</p>`);
    i++;
  }

  return out.join("\n");
}

function inline(text) {
  let s = escapeHtml(text);
  s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_m, label, href) => {
    const safe = href.startsWith("http") ? href : readerHref(href);
    return `<a href="${escapeHtml(safe)}">${label}</a>`;
  });
  return s;
}
