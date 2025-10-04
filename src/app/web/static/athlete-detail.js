import { request } from "./api.js";
import { formatDate } from "./format.js";
import { translations } from "./translations.js";

export function initializeAthleteDetailPage({ notify }) {
  const hero = document.querySelector("#athlete-detail");
  const nameEl = document.querySelector("#athlete-name");
  const subtitleEl = document.querySelector("#athlete-subtitle");
  const emailLink = document.querySelector("#athlete-email");
  const bioContainer = document.querySelector("#athlete-bio");
  const historyList = document.querySelector("#athlete-history");
  const historyEmpty = document.querySelector("#athlete-history-empty");
  const rostersList = document.querySelector("#athlete-rosters");
  const rostersEmpty = document.querySelector("#athlete-rosters-empty");

  if (!hero) {
    return;
  }

  const athleteId = hero.dataset.athleteId;

  function t(key) {
    const dictionary = translations[document.documentElement.lang] || translations.en;
    return dictionary[key] || translations.en[key] || key;
  }

  async function loadAthleteDetail() {
    if (!athleteId) {
      return;
    }
    try {
      const detail = await request(`/athletes/${athleteId}`);
      if (nameEl) {
        nameEl.textContent = detail.full_name;
      }
      if (subtitleEl) {
        const segments = [detail.role, detail.country].filter(Boolean);
        subtitleEl.textContent = segments.join(" · ");
      }
      if (emailLink) {
        emailLink.href = detail.email ? `mailto:${detail.email}` : "#";
        emailLink.textContent = detail.email || "—";
      }
      if (bioContainer) {
        bioContainer.innerHTML = "";
        if (detail.bio) {
          const paragraph = document.createElement("p");
          paragraph.textContent = detail.bio;
          bioContainer.appendChild(paragraph);
        } else {
          bioContainer.textContent = "This athlete has not published a biography yet.";
        }
        if (detail.highlight_video_url) {
          const highlight = document.createElement("p");
          const link = document.createElement("a");
          link.href = detail.highlight_video_url;
          link.target = "_blank";
          link.rel = "noopener";
          link.textContent = "Watch highlight video";
          highlight.appendChild(link);
          bioContainer.appendChild(highlight);
        }
      }

      if (historyList && historyEmpty) {
        historyList.innerHTML = "";
        const entries = detail.track_history ?? [];
        if (!entries.length) {
          historyEmpty.hidden = false;
          historyEmpty.textContent = t("athlete_detail.history_empty");
        } else {
          historyEmpty.hidden = true;
          entries.forEach((entry) => {
            const item = document.createElement("li");
            const eventDate = entry.event_date ? formatDate(entry.event_date) : "";
            item.innerHTML = `
              <strong>${entry.event}</strong>
              ${eventDate ? `<span>${eventDate}</span>` : ""}
              <span>${entry.result}</span>
              ${entry.video_url ? `<a href="${entry.video_url}" target="_blank" rel="noopener">Watch race</a>` : ""}
            `;
            historyList.appendChild(item);
          });
        }
      }

      if (rostersList && rostersEmpty) {
        rostersList.innerHTML = "";
        const rosters = detail.rosters ?? [];
        if (!rosters.length) {
          rostersEmpty.hidden = false;
          rostersEmpty.textContent = t("athlete_detail.rosters_empty");
        } else {
          rostersEmpty.hidden = true;
          rosters.forEach((roster) => {
            const item = document.createElement("li");
            item.className = "card";
            const updated = roster.updated_at ? formatDate(roster.updated_at) : "";
            item.innerHTML = `
              <div class="card-meta">
                <span class="tag">${roster.country}</span>
                <span>${roster.division}</span>
                ${updated ? `<span>${updated}</span>` : ""}
              </div>
              <h3><a href="/rosters/${roster.id}">${roster.name}</a></h3>
              <p>${roster.athlete_count} athletes · Coach ${roster.coach_name}</p>
            `;
            rostersList.appendChild(item);
          });
        }
      }
    } catch (error) {
      notify("error", `Unable to load athlete (${error.message}).`);
      console.error(error);
    }
  }

  loadAthleteDetail();
}
