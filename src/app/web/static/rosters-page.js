import { request } from "./api.js";
import { formatDate } from "./format.js";
import { sampleRosters } from "./samples.js";

export function initializeRostersPage({ notify }) {
  const list = document.querySelector("#rosters-page-list");
  const empty = document.querySelector("#rosters-page-empty");
  const refreshButton = document.querySelector("#rosters-refresh");
  const filterInput = document.querySelector("#rosters-filter");

  let rosters = [];

  function renderRostersPage() {
    if (!list || !empty) {
      return;
    }
    const query = filterInput?.value.trim().toLowerCase() ?? "";
    const filtered = rosters.filter((roster) => {
      if (!query) return true;
      return (
        roster.name.toLowerCase().includes(query) ||
        (roster.country && roster.country.toLowerCase().includes(query)) ||
        (roster.coach && roster.coach.toLowerCase().includes(query))
      );
    });

    list.innerHTML = "";
    if (!filtered.length) {
      empty.hidden = false;
      return;
    }
    empty.hidden = true;
    filtered.forEach((roster) => {
      const updated = roster.updated_at ? formatDate(roster.updated_at) : "";
      const rosterId = roster.id ?? null;
      const totalAthletes = roster.athlete_count ?? roster.athletes ?? "--";
      const coachName = roster.coach_name ?? roster.coach ?? "TBA";
      const titleMarkup = rosterId ? `<a href="/rosters/${rosterId}">${roster.name}</a>` : roster.name;
      const item = document.createElement("li");
      item.className = "card";
      item.innerHTML = `
        <div class="card-meta">
          <span class="tag">${roster.country}</span>
          <span>${roster.division || ""}</span>
          ${updated ? `<span>${updated}</span>` : ""}
        </div>
        <h3>${titleMarkup}</h3>
        <p>${totalAthletes} athletes · Coach ${coachName}</p>
      `;
      list.appendChild(item);
    });
  }

  async function loadRostersPage() {
    try {
      rosters = await request("/rosters/");
      renderRostersPage();
    } catch (error) {
      rosters = sampleRosters.map((roster, index) => ({
        id: roster.id ?? index + 1,
        ...roster,
      }));
      renderRostersPage();
      notify("error", `Unable to load rosters (${error.message}). Showing sample data.`);
      console.error(error);
    }
  }

  if (filterInput) {
    filterInput.addEventListener("input", renderRostersPage);
  }

  if (refreshButton) {
    refreshButton.addEventListener("click", loadRostersPage);
  }

  loadRostersPage();
}
