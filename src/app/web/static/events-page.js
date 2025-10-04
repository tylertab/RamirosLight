import { request } from "./api.js";
import { formatDate, isFutureDate } from "./format.js";
import { sampleEvents } from "./samples.js";

export function initializeEventsPage({ notify }) {
  const list = document.querySelector("#events-page-list");
  const empty = document.querySelector("#events-page-empty");
  const refreshButton = document.querySelector("#events-refresh");
  const createButton = document.querySelector("#events-create");
  const upcomingToggle = document.querySelector("#events-only-upcoming");

  let events = [];

  function renderEventsPage() {
    if (!list || !empty) {
      return;
    }
    const onlyUpcoming = upcomingToggle?.checked ?? false;
    const items = events
      .slice()
      .filter((event) => (onlyUpcoming ? isFutureDate(event.start_date || event.created_at) : true))
      .sort((a, b) => {
        const aDate = new Date(a.start_date || a.created_at || 0).getTime();
        const bDate = new Date(b.start_date || b.created_at || 0).getTime();
        return bDate - aDate;
      });

    list.innerHTML = "";
    if (!items.length) {
      empty.hidden = false;
      return;
    }
    empty.hidden = true;
    items.forEach((event) => {
      const start = event.start_date ? formatDate(event.start_date) : "";
      const end = event.end_date ? formatDate(event.end_date) : "";
      const item = document.createElement("li");
      item.className = "card";
      const titleMarkup = event.id ? `<a href="/events/${event.id}">${event.name}</a>` : event.name;
      item.innerHTML = `
        <div class="card-meta">
          <span class="tag">${event.location || "TBA"}</span>
          ${start ? `<span>${start}${end ? ` – ${end}` : ""}</span>` : ""}
          ${event.federation_id ? `<span>Federation #${event.federation_id}</span>` : ""}
        </div>
        <h3>${titleMarkup}</h3>
      `;
      list.appendChild(item);
    });
  }

  async function loadEventsPage() {
    try {
      events = await request("/events/");
      renderEventsPage();
    } catch (error) {
      events = sampleEvents.map((event, index) => ({
        id: event.id ?? index + 1,
        ...event,
        start_date: event.start_date || new Date(Date.now() + index * 604800000).toISOString(),
        end_date: event.end_date || new Date(Date.now() + index * 604800000 + 86400000).toISOString(),
      }));
      renderEventsPage();
      notify("error", `Unable to load events (${error.message}). Showing sample data.`);
      console.error(error);
    }
  }

  if (refreshButton) {
    refreshButton.addEventListener("click", loadEventsPage);
  }

  if (createButton) {
    createButton.addEventListener("click", () => {
      window.location.href = "/#events";
    });
  }

  if (upcomingToggle) {
    upcomingToggle.addEventListener("change", renderEventsPage);
  }

  loadEventsPage();
}
