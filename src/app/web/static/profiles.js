import { request } from "./api.js";
import { formatDate } from "./format.js";
import { sampleAthletes } from "./samples.js";

export function initializeProfilesPage({ notify }) {
  const list = document.querySelector("#profiles-list");
  const empty = document.querySelector("#profiles-empty");
  const filterInput = document.querySelector("#profiles-filter");
  const refreshButton = document.querySelector("#profiles-refresh");
  const createButton = document.querySelector("#profiles-create");

  let profiles = [];

  function renderProfiles() {
    if (!list || !empty) {
      return;
    }
    const query = filterInput?.value.trim().toLowerCase() ?? "";
    const filtered = profiles.filter((profile) => {
      if (!query) return true;
      return (
        profile.full_name.toLowerCase().includes(query) ||
        (profile.email && profile.email.toLowerCase().includes(query))
      );
    });

    list.innerHTML = "";
    if (!filtered.length) {
      empty.hidden = false;
      return;
    }
    empty.hidden = true;
    filtered.forEach((profile) => {
      const item = document.createElement("li");
      item.className = "card";
      const created = formatDate(profile.created_at);
      const nameMarkup = profile.id
        ? `<a href="/athletes/${profile.id}">${profile.full_name}</a>`
        : profile.full_name;
      item.innerHTML = `
        <div class="card-meta">
          <span class="tag">${profile.role}</span>
          <span>${profile.email}</span>
          ${created ? `<span>${created}</span>` : ""}
        </div>
        <h3>${nameMarkup}</h3>
      `;
      list.appendChild(item);
    });
  }

  async function loadProfiles() {
    try {
      profiles = await request("/accounts/");
      renderProfiles();
    } catch (error) {
      profiles = sampleAthletes.map((athlete, index) => ({
        ...athlete,
        id: index + 1,
        created_at: new Date(Date.now() - index * 86400000).toISOString(),
      }));
      renderProfiles();
      notify("error", `Unable to fetch live profiles (${error.message}). Showing sample data.`);
      console.error(error);
    }
  }

  if (filterInput) {
    filterInput.addEventListener("input", renderProfiles);
  }

  if (refreshButton) {
    refreshButton.addEventListener("click", loadProfiles);
  }

  if (createButton) {
    createButton.addEventListener("click", () => {
      window.location.href = "/signup";
    });
  }

  loadProfiles();
}
