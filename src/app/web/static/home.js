import { request } from "./api.js";
import { formatDate } from "./format.js";
import { sampleAthletes, sampleEvents } from "./samples.js";
import {
  state,
  hydrateHomeState,
  setAthletes,
  setEvents,
  setRosters,
  setNews,
} from "./state.js";
import { translations } from "./translations.js";

export function initializeHomePage({ initialData, notify }) {
  const athleteList = document.querySelector("#athletes-list");
  const athleteEmpty = document.querySelector("#athletes-empty");
  const athleteForm = document.querySelector("#athlete-form");
  const seedAthletesButton = document.querySelector("#seed-athletes");
  const eventList = document.querySelector("#events-list");
  const eventEmpty = document.querySelector("#events-empty");
  const eventForm = document.querySelector("#event-form");
  const seedEventsButton = document.querySelector("#seed-events");
  const rostersList = document.querySelector("#rosters-list");
  const rostersEmpty = document.querySelector("#rosters-empty");
  const newsList = document.querySelector("#news-list");
  const newsEmpty = document.querySelector("#news-empty");
  const searchInput = document.querySelector("#global-search");
  const searchFilters = document.querySelectorAll(".search-filter");
  const searchResults = document.querySelector("#search-results");
  const searchEmpty = document.querySelector("#search-empty");

  let activeSearchFilter = "all";

  if (initialData) {
    hydrateHomeState(initialData);
  }

  function renderAthletes() {
    if (!athleteList || !athleteEmpty) {
      return;
    }
    athleteList.innerHTML = "";
    if (!state.athletes.length) {
      athleteEmpty.hidden = false;
      return;
    }
    athleteEmpty.hidden = true;
    state.athletes.forEach((athlete) => {
      const item = document.createElement("li");
      item.className = "card";
      const created = athlete.created_at ? new Date(athlete.created_at) : new Date();
      const profileId = athlete.id ?? athlete.user_id ?? null;
      const nameMarkup = profileId
        ? `<a href="/athletes/${profileId}">${athlete.full_name}</a>`
        : athlete.full_name;
      item.innerHTML = `
        <div class="card-meta">
          <span class="tag">${athlete.role}</span>
          <span>${athlete.email}</span>
          <span>${formatDate(created)}</span>
        </div>
        <h3>${nameMarkup}</h3>
      `;
      athleteList.appendChild(item);
    });
  }

  function renderEvents() {
    if (!eventList || !eventEmpty) {
      return;
    }
    eventList.innerHTML = "";
    if (!state.events.length) {
      eventEmpty.hidden = false;
      return;
    }
    eventEmpty.hidden = true;
    state.events.forEach((event) => {
      const item = document.createElement("li");
      item.className = "card";
      const start = event.start_date ? new Date(event.start_date) : null;
      const end = event.end_date ? new Date(event.end_date) : null;
      const dateRange = start && end ? `${formatDate(start)} – ${formatDate(end)}` : "Date TBA";
      const eventLink = event.id ? `<a href="/events/${event.id}">${event.name}</a>` : event.name;
      item.innerHTML = `
        <h3>${eventLink}</h3>
        <div class="card-meta">
          <span class="tag">${event.location}</span>
          <span>${dateRange}</span>
          ${event.federation_id ? `<span>Federation #${event.federation_id}</span>` : ""}
        </div>
      `;
      eventList.appendChild(item);
    });
  }

  function renderRosters() {
    if (!rostersList || !rostersEmpty) {
      return;
    }
    rostersList.innerHTML = "";
    if (!state.rosters.length) {
      rostersEmpty.hidden = false;
      return;
    }
    rostersEmpty.hidden = true;
    state.rosters.forEach((roster) => {
      const updated = roster.updated_at ? formatDate(roster.updated_at) : "";
      const rosterId = roster.id ?? null;
      const titleMarkup = rosterId ? `<a href="/rosters/${rosterId}">${roster.name}</a>` : roster.name;
      const totalAthletes = roster.athlete_count ?? roster.athletes ?? "--";
      const coachName = roster.coach_name ?? roster.coach ?? "TBA";
      const item = document.createElement("li");
      item.className = "card";
      item.innerHTML = `
        <div class="card-meta">
          <span class="tag">${roster.country}</span>
          <span>${roster.division}</span>
          ${updated ? `<span>Updated ${updated}</span>` : ""}
        </div>
        <h3>${titleMarkup}</h3>
        <p>${totalAthletes} athletes · Coach ${coachName}</p>
      `;
      rostersList.appendChild(item);
    });
  }

  function renderNews() {
    if (!newsList || !newsEmpty) {
      return;
    }
    newsList.innerHTML = "";
    if (!state.news.length) {
      newsEmpty.hidden = false;
      return;
    }
    newsEmpty.hidden = true;
    state.news.forEach((article) => {
      const published = article.published_at ? formatDate(article.published_at) : "";
      const item = document.createElement("li");
      item.className = "card";
      item.innerHTML = `
        <div class="card-meta">
          <span class="tag">${article.region}</span>
          ${published ? `<span>${published}</span>` : ""}
        </div>
        <h3>${article.title}</h3>
        <p>${article.excerpt}</p>
      `;
      newsList.appendChild(item);
    });
  }

  function collectSearchResults() {
    const query = searchInput?.value.trim().toLowerCase() ?? "";
    const results = [];
    const includeCategory = (category) => activeSearchFilter === "all" || activeSearchFilter === category;

    if (includeCategory("athletes")) {
      const athletes = (!query ? state.athletes.slice(0, 4) : state.athletes).filter((athlete) => {
        if (!query) return true;
        return (
          athlete.full_name.toLowerCase().includes(query) ||
          (athlete.email && athlete.email.toLowerCase().includes(query))
        );
      });
      athletes.forEach((athlete) => {
        const profileId = athlete.id ?? athlete.user_id ?? null;
        results.push({
          category: "Athletes",
          title: athlete.full_name,
          subtitle: athlete.email,
          detail: athlete.role,
          url: profileId ? `/athletes/${profileId}` : undefined,
        });
      });
    }

    if (includeCategory("events")) {
      const events = (!query ? state.events.slice(0, 4) : state.events).filter((event) => {
        if (!query) return true;
        return (
          event.name.toLowerCase().includes(query) ||
          (event.location && event.location.toLowerCase().includes(query))
        );
      });
      events.forEach((event) => {
        const start = event.start_date ? new Date(event.start_date) : null;
        const end = event.end_date ? new Date(event.end_date) : null;
        const eventId = event.id ?? null;
        results.push({
          category: "Events",
          title: event.name,
          subtitle: event.location,
          detail: start && end ? `${formatDate(start)} – ${formatDate(end)}` : "Dates TBA",
          url: eventId ? `/events/${eventId}` : undefined,
        });
      });
    }

    if (includeCategory("rosters")) {
      const rosters = (!query ? state.rosters.slice(0, 4) : state.rosters).filter((roster) => {
        if (!query) return true;
        return (
          roster.name.toLowerCase().includes(query) ||
          (roster.country && roster.country.toLowerCase().includes(query)) ||
          (roster.coach && roster.coach.toLowerCase().includes(query))
        );
      });
      rosters.forEach((roster) => {
        const rosterId = roster.id ?? null;
        const totalAthletes = roster.athlete_count ?? roster.athletes ?? "--";
        const coachName = roster.coach_name ?? roster.coach ?? "TBA";
        results.push({
          category: "Rosters",
          title: roster.name,
          subtitle: `${roster.country} · ${roster.division ?? ""}`,
          detail: `${totalAthletes} athletes • Coach ${coachName}`,
          url: rosterId ? `/rosters/${rosterId}` : undefined,
        });
      });
    }

    if (includeCategory("news")) {
      const news = (!query ? state.news.slice(0, 4) : state.news).filter((article) => {
        if (!query) return true;
        return (
          article.title.toLowerCase().includes(query) ||
          (article.region && article.region.toLowerCase().includes(query)) ||
          (article.excerpt && article.excerpt.toLowerCase().includes(query))
        );
      });
      news.forEach((article) => {
        const published = article.published_at ? formatDate(article.published_at) : null;
        results.push({
          category: "News",
          title: article.title,
          subtitle: article.region,
          detail: published || article.excerpt,
          description: article.excerpt,
        });
      });
    }

    return results.slice(0, 12);
  }

  function renderSearchResults() {
    if (!searchResults || !searchEmpty) {
      return;
    }
    const results = collectSearchResults();
    if (!results.length) {
      const dictionary = translations[document.documentElement.lang] || translations.en;
      searchResults.hidden = true;
      searchEmpty.hidden = false;
      searchEmpty.textContent = searchInput?.value.trim()
        ? dictionary["search.no_results"] || translations.en["search.no_results"]
        : dictionary["search.empty"] || translations.en["search.empty"];
      return;
    }

    searchResults.hidden = false;
    searchEmpty.hidden = true;
    searchResults.innerHTML = "";
    results.forEach((result) => {
      const item = document.createElement("li");
      item.className = "search-result";
      const titleMarkup = result.url ? `<a href="${result.url}">${result.title}</a>` : result.title;
      item.innerHTML = `
        <div class="search-result-header">
          <span class="tag">${result.category}</span>
          ${result.subtitle ? `<span>${result.subtitle}</span>` : ""}
        </div>
        <h3>${titleMarkup}</h3>
        ${result.description ? `<p>${result.description}</p>` : result.detail ? `<p>${result.detail}</p>` : ""}
      `;
      searchResults.appendChild(item);
    });
  }

  function renderStaticSections() {
    renderAthletes();
    renderEvents();
    renderRosters();
    renderNews();
    renderSearchResults();
  }

  renderStaticSections();

  async function loadAthletes() {
    try {
      const data = await request("/accounts/");
      setAthletes(data || []);
      renderAthletes();
      renderSearchResults();
    } catch (error) {
      const fallback = sampleAthletes.map((athlete, index) => ({
        id: index + 1,
        ...athlete,
        created_at: new Date(Date.now() - index * 86400000).toISOString(),
      }));
      setAthletes(fallback);
      renderAthletes();
      renderSearchResults();
      notify("error", `Live athlete roster unavailable (${error.message}). Showing sample data.`);
      console.error(error);
    }
  }

  async function loadEvents() {
    try {
      const data = await request("/events/");
      setEvents(data || []);
      renderEvents();
      renderSearchResults();
    } catch (error) {
      const fallback = sampleEvents.map((event, index) => ({
        id: event.id ?? index + 1,
        ...event,
        start_date: event.start_date || new Date(Date.now() + index * 604800000).toISOString(),
        end_date:
          event.end_date || new Date(Date.now() + index * 604800000 + 86400000).toISOString(),
      }));
      setEvents(fallback);
      renderEvents();
      renderSearchResults();
      notify("error", `Live event calendar unavailable (${error.message}). Showing sample data.`);
      console.error(error);
    }
  }

  if (athleteForm) {
    athleteForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(athleteForm);
      const payload = Object.fromEntries(formData.entries());
      try {
        await request("/accounts/register", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        athleteForm.reset();
        notify("success", `Athlete "${payload.full_name}" registered successfully.`);
        await loadAthletes();
      } catch (error) {
        if (error.status === 409) {
          notify("error", "This email is already registered.");
        } else {
          notify("error", `Unable to register athlete: ${error.message}`);
        }
        console.error(error);
      }
    });
  }

  if (eventForm) {
    eventForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(eventForm);
      const payload = Object.fromEntries(formData.entries());
      payload.federation_id = payload.federation_id === "" ? null : Number(payload.federation_id);
      try {
        await request("/events/", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        eventForm.reset();
        notify("success", `Event "${payload.name}" created successfully.`);
        await loadEvents();
      } catch (error) {
        notify("error", `Unable to create event: ${error.message}`);
        console.error(error);
      }
    });
  }

  async function seedAthletes() {
    const existingEmails = new Set(state.athletes.map((athlete) => athlete.email));
    for (const athlete of sampleAthletes) {
      if (existingEmails.has(athlete.email)) {
        continue;
      }
      try {
        await request("/accounts/register", {
          method: "POST",
          body: JSON.stringify(athlete),
        });
      } catch (error) {
        if (error.status !== 409) {
          console.warn("Failed to seed athlete", athlete.email, error);
        }
      }
    }
    await loadAthletes();
    notify("success", "Sample athletes are ready.");
  }

  async function seedEvents() {
    const existingNames = new Set(state.events.map((event) => event.name));
    for (const event of sampleEvents) {
      if (existingNames.has(event.name)) {
        continue;
      }
      try {
        await request("/events/", {
          method: "POST",
          body: JSON.stringify(event),
        });
      } catch (error) {
        if (error.status !== 400) {
          console.warn("Failed to seed event", event.name, error);
        }
      }
    }
    await loadEvents();
    notify("success", "Sample events are ready.");
  }

  if (seedAthletesButton) {
    seedAthletesButton.addEventListener("click", async () => {
      seedAthletesButton.disabled = true;
      await seedAthletes();
      seedAthletesButton.disabled = false;
    });
  }

  if (seedEventsButton) {
    seedEventsButton.addEventListener("click", async () => {
      seedEventsButton.disabled = true;
      await seedEvents();
      seedEventsButton.disabled = false;
    });
  }

  if (searchInput) {
    searchInput.addEventListener("input", renderSearchResults);
  }

  searchFilters.forEach((button) => {
    button.addEventListener("click", () => {
      if (button.dataset.filter === activeSearchFilter) {
        return;
      }
      activeSearchFilter = button.dataset.filter;
      searchFilters.forEach((btn) => {
        const isActive = btn === button;
        btn.classList.toggle("active", isActive);
        btn.setAttribute("aria-selected", String(isActive));
        if (isActive) {
          btn.focus();
        }
      });
      renderSearchResults();
    });
  });

  (async () => {
    if (!state.athletes.length) {
      await loadAthletes();
    } else {
      renderAthletes();
      renderSearchResults();
    }
    if (!state.events.length) {
      await loadEvents();
    } else {
      renderEvents();
      renderSearchResults();
    }
    if (!state.rosters.length && initialData?.rosters) {
      setRosters(initialData.rosters);
      renderRosters();
      renderSearchResults();
    }
    if (!state.news.length && initialData?.news) {
      setNews(initialData.news);
      renderNews();
      renderSearchResults();
    }
  })();
}
