import { request } from "./api.js";
import { formatDate, formatDateTime, formatTimeRange } from "./format.js";
import { buildSampleEventDetail } from "./samples.js";
import { translations } from "./translations.js";

export function initializeEventDetailPage({ initialData, notify }) {
  const root = document.querySelector("#event-detail");
  const nameElement = document.querySelector("#event-detail-name");
  const metaElement = document.querySelector("#event-detail-meta");
  const summaryLocation = document.querySelector("#event-summary-location");
  const summaryDates = document.querySelector("#event-summary-dates");
  const summaryFederation = document.querySelector("#event-summary-federation");
  const summaryStatus = document.querySelector("#event-summary-status");
  const sessionsList = document.querySelector("#event-session-list");
  const sessionsEmpty = document.querySelector("#event-sessions-empty");
  const disciplinesContainer = document.querySelector("#event-discipline-container");
  const disciplinesEmpty = document.querySelector("#event-disciplines-empty");
  const latestUpdateLabel = document.querySelector("#event-latest-update");
  const refreshButton = document.querySelector("#event-refresh");
  const demoButton = document.querySelector("#event-generate-demo");

  if (!root) {
    return;
  }

  const rawEventId = Number.parseInt(root.dataset.eventId || "", 10);
  const eventId = Number.isNaN(rawEventId) ? null : rawEventId;
  let detail = initialData ?? null;

  function t(key) {
    const dictionary = translations[document.documentElement.lang] || translations.en;
    return dictionary[key] || translations.en[key] || key;
  }

  function statusLabel(status) {
    if (!status) {
      return "";
    }
    const normalized = String(status).toLowerCase();
    const key = `event_detail.status.${normalized}`;
    const label = t(key);
    return label === key ? String(status) : label;
  }

  function createStatusChip(status) {
    if (!status) {
      return "";
    }
    const label = statusLabel(status);
    const normalized = String(status).toLowerCase();
    return `<span class="status-chip status-${normalized}">${label}</span>`;
  }

  function renderHeader() {
    if (!detail) {
      return;
    }
    if (nameElement) {
      nameElement.textContent = detail.name || "—";
    }
    if (metaElement) {
      const parts = [];
      if (detail.location) {
        parts.push(detail.location);
      }
      if (detail.start_date && detail.end_date) {
        parts.push(`${formatDate(detail.start_date)} – ${formatDate(detail.end_date)}`);
      } else if (detail.start_date) {
        parts.push(formatDate(detail.start_date));
      }
      const liveCount = Array.isArray(detail.sessions)
        ? detail.sessions.filter((session) => session.status === "live").length
        : 0;
      const totalSessions = detail.sessions?.length ?? 0;
      if (liveCount > 0) {
        parts.push(
          liveCount === 1
            ? t("event_detail.meta.live_sessions").replace("{count}", String(liveCount))
            : t("event_detail.meta.live_sessions_plural").replace("{count}", String(liveCount))
        );
      } else if (totalSessions > 0) {
        parts.push(
          totalSessions === 1
            ? t("event_detail.meta.sessions_single")
            : t("event_detail.meta.sessions").replace("{count}", String(totalSessions))
        );
      }
      metaElement.textContent = parts.join(" · ") || "";
    }
  }

  function renderSummary() {
    if (!detail) {
      return;
    }
    if (summaryLocation) {
      summaryLocation.textContent = detail.location || "—";
    }
    if (summaryDates) {
      if (detail.start_date && detail.end_date) {
        summaryDates.textContent = `${formatDate(detail.start_date)} – ${formatDate(detail.end_date)}`;
      } else if (detail.start_date) {
        summaryDates.textContent = formatDate(detail.start_date);
      } else {
        summaryDates.textContent = "—";
      }
    }
    if (summaryFederation) {
      summaryFederation.textContent = detail.federation_id ? `#${detail.federation_id}` : "—";
    }
    if (summaryStatus) {
      const sessionStatuses = Array.isArray(detail.sessions)
        ? detail.sessions.map((session) => session.status)
        : [];
      const disciplineStatuses = Array.isArray(detail.disciplines)
        ? detail.disciplines.map((discipline) => discipline.status)
        : [];
      let summaryKey = "scheduled";
      if (disciplineStatuses.includes("live") || sessionStatuses.includes("live")) {
        summaryKey = "live";
      } else if (disciplineStatuses.includes("finalized") || sessionStatuses.includes("completed")) {
        summaryKey = "finalized";
      } else if (sessionStatuses.includes("completed")) {
        summaryKey = "completed";
      }
      summaryStatus.innerHTML = createStatusChip(summaryKey);
    }
    if (latestUpdateLabel) {
      if (detail.latest_update) {
        latestUpdateLabel.textContent = `${t("event_detail.last_update")}: ${formatDateTime(detail.latest_update)}`;
      } else {
        latestUpdateLabel.textContent = t("event_detail.last_update");
      }
    }
  }

  function renderSessions() {
    if (!sessionsList || !sessionsEmpty) {
      return;
    }
    sessionsList.innerHTML = "";
    const sessions = Array.isArray(detail?.sessions) ? detail.sessions.slice() : [];
    if (!sessions.length) {
      sessionsEmpty.hidden = false;
      return;
    }
    sessionsEmpty.hidden = true;
    sessions
      .sort((a, b) => {
        const aTime = a.start_time ? new Date(a.start_time).getTime() : 0;
        const bTime = b.start_time ? new Date(b.start_time).getTime() : 0;
        return aTime - bTime;
      })
      .forEach((session) => {
        const item = document.createElement("li");
        item.className = "session-item";
        const metaParts = [];
        const timeRange = formatTimeRange(session.start_time, session.end_time);
        if (timeRange) {
          metaParts.push(timeRange);
        }
        if (session.venue) {
          metaParts.push(session.venue);
        }
        item.innerHTML = `
          <div class="session-header">
            <h4>${session.name}</h4>
            <div class="session-meta">
              ${metaParts.map((part) => `<span>${part}</span>`).join("")}
            </div>
            ${createStatusChip(session.status)}
          </div>
        `;
        sessionsList.appendChild(item);
      });
  }

  function renderDisciplines() {
    if (!disciplinesContainer || !disciplinesEmpty) {
      return;
    }
    disciplinesContainer.innerHTML = "";
    const disciplines = Array.isArray(detail?.disciplines) ? detail.disciplines.slice() : [];
    if (!disciplines.length) {
      disciplinesEmpty.hidden = false;
      return;
    }
    disciplinesEmpty.hidden = true;
    const groups = new Map();
    disciplines.forEach((discipline) => {
      const key = discipline.session?.name || t("event_detail.group_unscheduled");
      if (!groups.has(key)) {
        groups.set(key, []);
      }
      groups.get(key).push(discipline);
    });

    groups.forEach((items, group) => {
      const section = document.createElement("section");
      section.className = "discipline-group";
      section.innerHTML = `
        <header>
          <h4>${group}</h4>
          <p>${t("event_detail.disciplines_hint")}</p>
        </header>
      `;
      const list = document.createElement("ul");
      list.className = "discipline-list";
      items
        .slice()
        .sort((a, b) => (a.order ?? 0) - (b.order ?? 0))
        .forEach((discipline) => {
          const item = document.createElement("li");
          item.className = "discipline";
          const entries = Array.isArray(discipline.entries) ? discipline.entries : [];
          item.innerHTML = `
            <div class="discipline-header">
              <div>
                <h5>${discipline.name}</h5>
                <span>${discipline.category || ""}</span>
              </div>
              ${createStatusChip(discipline.status)}
            </div>
            <div class="discipline-meta">
              <span>${formatTimeRange(discipline.scheduled_start, discipline.scheduled_end)}</span>
              <span>${discipline.venue || ""}</span>
            </div>
            ${entries.length ? "" : `<p>${t("event_detail.scoreboard_empty")}</p>`}
          `;
          if (entries.length) {
            const table = document.createElement("table");
            table.innerHTML = `
              <thead>
                <tr>
                  <th>${t("event_detail.table_position")}</th>
                  <th>${t("event_detail.table_lane")}</th>
                  <th>${t("event_detail.table_athlete")}</th>
                  <th>${t("event_detail.table_team")}</th>
                  <th>${t("event_detail.table_result")}</th>
                  <th>${t("event_detail.table_points")}</th>
                  <th>${t("event_detail.table_status")}</th>
                </tr>
              </thead>
              <tbody></tbody>
            `;
            const tbody = table.querySelector("tbody");
            entries.forEach((entry) => {
              const row = document.createElement("tr");
              row.innerHTML = `
                <td>${entry.position ?? ""}</td>
                <td>${entry.lane ?? ""}</td>
                <td>${entry.athlete_name}</td>
                <td>${entry.team_name ?? ""}</td>
                <td>${entry.result ?? ""}</td>
                <td>${entry.points ?? ""}</td>
                <td>${statusLabel(entry.status)}</td>
              `;
              tbody.appendChild(row);
            });
            item.appendChild(table);
          }
          list.appendChild(item);
        });
      section.appendChild(list);
      disciplinesContainer.appendChild(section);
    });
  }

  function renderAll() {
    if (!detail) {
      return;
    }
    renderHeader();
    renderSummary();
    renderSessions();
    renderDisciplines();
  }

  if (detail) {
    renderAll();
  }

  async function loadEventDetail() {
    if (!eventId) {
      detail = buildSampleEventDetail();
      renderAll();
      return;
    }
    try {
      detail = await request(`/events/${eventId}`);
      renderAll();
    } catch (error) {
      detail = buildSampleEventDetail(eventId);
      renderAll();
      notify("error", `${t("event_detail.refresh_error") || ""} (${error.message}). Showing demo data.`);
      console.error(error);
    }
  }

  if (refreshButton) {
    refreshButton.addEventListener("click", () => {
      loadEventDetail();
    });
  }

  if (demoButton) {
    demoButton.addEventListener("click", async () => {
      if (!eventId) {
        detail = buildSampleEventDetail();
        renderAll();
        notify("success", t("event_detail.generate_toast"));
        return;
      }
      try {
        demoButton.disabled = true;
        await request(`/events/${eventId}/demo`, {
          method: "POST",
          body: JSON.stringify({
            start_time: new Date().toISOString(),
            include_results: true,
          }),
        });
        notify("success", t("event_detail.generate_toast"));
        await loadEventDetail();
      } catch (error) {
        notify("error", `${t("event_detail.demo_error") || ""} (${error.message}).`);
        console.error(error);
      } finally {
        demoButton.disabled = false;
      }
    });
  }

  if (!detail) {
    loadEventDetail();
  }
}
