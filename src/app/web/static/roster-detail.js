import { request } from "./api.js";
import { formatDate } from "./format.js";
import { translations } from "./translations.js";

export function initializeRosterDetailPage({ notify }) {
  const hero = document.querySelector("#roster-detail");
  const nameEl = document.querySelector("#roster-name");
  const subtitleEl = document.querySelector("#roster-subtitle");
  const ownerLink = document.querySelector("#roster-owner");
  const divisionEl = document.querySelector("#roster-division");
  const coachEl = document.querySelector("#roster-coach");
  const updatedEl = document.querySelector("#roster-updated");
  const athletesList = document.querySelector("#roster-athletes");
  const athletesEmpty = document.querySelector("#roster-athletes-empty");

  if (!hero) {
    return;
  }

  const rosterId = hero.dataset.rosterId;

  function t(key) {
    const dictionary = translations[document.documentElement.lang] || translations.en;
    return dictionary[key] || translations.en[key] || key;
  }

  async function loadRosterDetail() {
    if (!rosterId) {
      return;
    }
    try {
      const detail = await request(`/rosters/${rosterId}`);
      if (nameEl) {
        nameEl.textContent = detail.name;
      }
      if (subtitleEl) {
        const segments = [detail.country, detail.division, `${detail.athlete_count} athletes`].filter(Boolean);
        subtitleEl.textContent = segments.join(" · ");
      }
      if (divisionEl) {
        divisionEl.textContent = detail.division || "—";
      }
      if (coachEl) {
        coachEl.textContent = detail.coach_name || "TBA";
      }
      if (updatedEl) {
        updatedEl.textContent = detail.updated_at ? formatDate(detail.updated_at) : "—";
      }
      if (ownerLink) {
        if (detail.owner) {
          ownerLink.textContent = `${detail.owner.full_name} (${detail.owner.email})`;
          ownerLink.href = detail.owner.email ? `mailto:${detail.owner.email}` : "#";
        } else {
          ownerLink.textContent = "No owner assigned";
          ownerLink.href = "/rosters";
        }
      }

      if (athletesList && athletesEmpty) {
        athletesList.innerHTML = "";
        const athletes = detail.athletes ?? [];
        if (!athletes.length) {
          athletesEmpty.hidden = false;
          athletesEmpty.textContent = t("roster_detail.athletes_empty");
        } else {
          athletesEmpty.hidden = true;
          athletes.forEach((athlete) => {
            const item = document.createElement("li");
            item.className = "card";
            item.innerHTML = `
              <div class="card-meta">
                <span class="tag">Athlete</span>
                <span>${athlete.email}</span>
              </div>
              <h3><a href="/athletes/${athlete.id}">${athlete.full_name}</a></h3>
              ${athlete.bio ? `<p>${athlete.bio}</p>` : ""}
            `;
            athletesList.appendChild(item);
          });
        }
      }
    } catch (error) {
      notify("error", `Unable to load roster (${error.message}).`);
      console.error(error);
    }
  }

  loadRosterDetail();
}
