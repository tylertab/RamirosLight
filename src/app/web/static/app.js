const API_BASE = "/api/v1";
const notifications = document.querySelector("#notifications");
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
const heroExploreButton = document.querySelector("#hero-explore");
const heroSubscribeButton = document.querySelector("#hero-subscribe");
const premiumSection = document.querySelector("#premium");
const searchSection = document.querySelector("#search");

document.querySelector("#api-base").textContent = API_BASE;

const sampleAthletes = [
  {
    full_name: "Ramiro Lightfoot",
    email: "ramiro.lightfoot@example.com",
    role: "athlete",
    password: "Shimmering123",
  },
  {
    full_name: "Sofía Delgado",
    email: "sofia.delgado@example.com",
    role: "athlete",
    password: "Sprinter123",
  },
  {
    full_name: "Liam O'Connor",
    email: "liam.oconnor@example.com",
    role: "athlete",
    password: "Hurdles123",
  },
];

const sampleEvents = [
  {
    name: "Aurora Indoor Classic",
    location: "Oslo, Norway",
    start_date: "2024-02-10",
    end_date: "2024-02-12",
    federation_id: null,
  },
  {
    name: "Sunset Coast Invitational",
    location: "Porto, Portugal",
    start_date: "2024-04-22",
    end_date: "2024-04-24",
    federation_id: null,
  },
  {
    name: "Highlands Distance Festival",
    location: "Edinburgh, Scotland",
    start_date: "2024-09-14",
    end_date: "2024-09-15",
    federation_id: null,
  },
];

const sampleRosters = [
  {
    name: "Club Andino Quito",
    country: "Ecuador",
    division: "U20",
    athletes: 18,
    coach: "María Torres",
    updated_at: "2024-08-11T13:45:00Z",
  },
  {
    name: "São Paulo Relays",
    country: "Brazil",
    division: "Senior",
    athletes: 26,
    coach: "Igor Almeida",
    updated_at: "2024-08-09T09:20:00Z",
  },
  {
    name: "Bogotá Altitude Club",
    country: "Colombia",
    division: "U18",
    athletes: 14,
    coach: "Carolina Ríos",
    updated_at: "2024-08-02T18:10:00Z",
  },
];

const sampleNews = [
  {
    title: "Camila Torres sets new 400m South American record",
    region: "Buenos Aires, AR",
    published_at: "2024-08-13T12:00:00Z",
    excerpt: "The 21-year-old from Córdoba clocked 50.82s at the Copa Cono Sur finale.",
  },
  {
    title: "Bogotá Marathon expands elite field for 2025",
    region: "Bogotá, CO",
    published_at: "2024-08-10T08:30:00Z",
    excerpt: "Trackeo partners with local organizers to deliver real-time splits in Spanish and English.",
  },
  {
    title: "Brazilian U20 relay camp launches in São Paulo",
    region: "São Paulo, BR",
    published_at: "2024-08-05T16:15:00Z",
    excerpt: "Coaches gain access to workload dashboards via the Trackeo Coach tier.",
  },
];

const state = {
  athletes: [],
  events: [],
  rosters: sampleRosters,
  news: sampleNews,
};

let activeSearchFilter = "all";

function notify(type, message) {
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;
  notifications.appendChild(toast);
  setTimeout(() => {
    toast.classList.add("fade");
    toast.addEventListener(
      "transitionend",
      () => toast.remove(),
      { once: true }
    );
    toast.style.opacity = "0";
  }, 3500);
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    const error = new Error(detail?.detail || response.statusText || "Request failed");
    error.status = response.status;
    error.payload = detail;
    throw error;
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

function renderAthletes() {
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
    item.innerHTML = `
      <div class="card-meta">
        <span class="tag">${athlete.role}</span>
        <span>${athlete.email}</span>
        <span>${created.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" })}</span>
      </div>
      <h3>${athlete.full_name}</h3>
    `;
    athleteList.appendChild(item);
  });
}

function renderEvents() {
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
    const dateRange = start && end ? `${start.toLocaleDateString()} – ${end.toLocaleDateString()}` : "Date TBA";
    item.innerHTML = `
      <h3>${event.name}</h3>
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
  rostersList.innerHTML = "";
  if (!state.rosters.length) {
    rostersEmpty.hidden = false;
    return;
  }
  rostersEmpty.hidden = true;
  state.rosters.forEach((roster) => {
    const updated = roster.updated_at ? new Date(roster.updated_at) : null;
    const item = document.createElement("li");
    item.className = "card";
    item.innerHTML = `
      <div class="card-meta">
        <span class="tag">${roster.country}</span>
        <span>${roster.division}</span>
        ${updated ? `<span>Updated ${updated.toLocaleDateString()}</span>` : ""}
      </div>
      <h3>${roster.name}</h3>
      <p>${roster.athletes} athletes · Coach ${roster.coach}</p>
    `;
    rostersList.appendChild(item);
  });
}

function renderNews() {
  newsList.innerHTML = "";
  if (!state.news.length) {
    newsEmpty.hidden = false;
    return;
  }
  newsEmpty.hidden = true;
  state.news.forEach((article) => {
    const published = article.published_at ? new Date(article.published_at) : null;
    const item = document.createElement("li");
    item.className = "card";
    item.innerHTML = `
      <div class="card-meta">
        <span class="tag">${article.region}</span>
        ${published ? `<span>${published.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" })}</span>` : ""}
      </div>
      <h3>${article.title}</h3>
      <p>${article.excerpt}</p>
    `;
    newsList.appendChild(item);
  });
}

function collectSearchResults() {
  const query = searchInput.value.trim().toLowerCase();
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
      results.push({
        category: "Athletes",
        title: athlete.full_name,
        subtitle: athlete.email,
        detail: athlete.role,
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
      results.push({
        category: "Events",
        title: event.name,
        subtitle: event.location,
        detail: start && end ? `${start.toLocaleDateString()} – ${end.toLocaleDateString()}` : "Dates TBA",
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
      results.push({
        category: "Rosters",
        title: roster.name,
        subtitle: `${roster.country} · ${roster.division}`,
        detail: `${roster.athletes} athletes • Coach ${roster.coach}`,
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
      const published = article.published_at ? new Date(article.published_at) : null;
      results.push({
        category: "News",
        title: article.title,
        subtitle: article.region,
        detail: published
          ? `${published.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" })}`
          : article.excerpt,
        description: article.excerpt,
      });
    });
  }

  return results.slice(0, 12);
}

function renderSearchResults() {
  const results = collectSearchResults();
  if (!results.length) {
    searchResults.hidden = true;
    searchEmpty.hidden = false;
    searchEmpty.textContent = searchInput.value.trim()
      ? "No matches yet. Try adjusting your filters or spelling."
      : "Start typing to explore Trackeo's data universe.";
    return;
  }

  searchResults.hidden = false;
  searchEmpty.hidden = true;
  searchResults.innerHTML = "";
  results.forEach((result) => {
    const item = document.createElement("li");
    item.className = "search-result";
    item.innerHTML = `
      <div class="search-result-header">
        <span class="tag">${result.category}</span>
        ${result.subtitle ? `<span>${result.subtitle}</span>` : ""}
      </div>
      <h3>${result.title}</h3>
      ${result.description ? `<p>${result.description}</p>` : result.detail ? `<p>${result.detail}</p>` : ""}
    `;
    searchResults.appendChild(item);
  });
}

async function loadAthletes() {
  try {
    const data = await request("/accounts/");
    state.athletes = data;
    renderAthletes();
    renderSearchResults();
  } catch (error) {
    const fallback = sampleAthletes.map((athlete, index) => ({
      ...athlete,
      created_at: new Date(Date.now() - index * 86400000).toISOString(),
    }));
    state.athletes = fallback;
    renderAthletes();
    renderSearchResults();
    notify("error", `Live athlete roster unavailable (${error.message}). Showing sample data.`);
    console.error(error);
  }
}

async function loadEvents() {
  try {
    const data = await request("/events/");
    state.events = data;
    renderEvents();
    renderSearchResults();
  } catch (error) {
    const fallback = sampleEvents.map((event, index) => ({
      ...event,
      start_date: event.start_date || new Date(Date.now() + index * 604800000).toISOString(),
      end_date: event.end_date || new Date(Date.now() + (index * 604800000) + 86400000).toISOString(),
    }));
    state.events = fallback;
    renderEvents();
    renderSearchResults();
    notify("error", `Live event calendar unavailable (${error.message}). Showing sample data.`);
    console.error(error);
  }
}

function serializeForm(form) {
  const formData = new FormData(form);
  return Object.fromEntries(formData.entries());
}

athleteForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = serializeForm(athleteForm);
  try {
    await request("/accounts/register", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    athleteForm.reset();
    notify("success", `Athlete \"${payload.full_name}\" registered successfully.`);
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

eventForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = serializeForm(eventForm);
  if (payload.federation_id === "") {
    payload.federation_id = null;
  } else {
    payload.federation_id = Number(payload.federation_id);
  }
  try {
    await request("/events/", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    eventForm.reset();
    notify("success", `Event \"${payload.name}\" created successfully.`);
    await loadEvents();
  } catch (error) {
    notify("error", `Unable to create event: ${error.message}`);
    console.error(error);
  }
});

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

seedAthletesButton.addEventListener("click", async () => {
  seedAthletesButton.disabled = true;
  await seedAthletes();
  seedAthletesButton.disabled = false;
});

seedEventsButton.addEventListener("click", async () => {
  seedEventsButton.disabled = true;
  await seedEvents();
  seedEventsButton.disabled = false;
});

searchInput.addEventListener("input", renderSearchResults);

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

if (heroExploreButton && searchSection) {
  heroExploreButton.addEventListener("click", () => {
    searchSection.scrollIntoView({ behavior: "smooth", block: "center" });
    searchInput.focus({ preventScroll: true });
  });
}

if (heroSubscribeButton && premiumSection) {
  heroSubscribeButton.addEventListener("click", () => {
    premiumSection.scrollIntoView({ behavior: "smooth", block: "start" });
  });
}

renderRosters();
renderNews();
renderSearchResults();

async function initialize() {
  await loadAthletes();
  if (!state.athletes.length) {
    await seedAthletes();
  }
  await loadEvents();
  if (!state.events.length) {
    await seedEvents();
  }
}

initialize();
