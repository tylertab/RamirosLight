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

document.querySelector("#api-base").textContent = API_BASE;

const sampleAthletes = [
  {
    full_name: "Ramiro Lightfoot",
    email: "ramiro.lightfoot@example.com",
    role: "athlete",
    password: "Shimmering123",
  },
  {
    full_name: "Sofia Delgado",
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

const state = {
  athletes: [],
  events: [],
};

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
    const created = new Date(athlete.created_at);
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
    const start = new Date(event.start_date);
    const end = new Date(event.end_date);
    item.innerHTML = `
      <h3>${event.name}</h3>
      <div class="card-meta">
        <span class="tag">${event.location}</span>
        <span>${start.toLocaleDateString()} - ${end.toLocaleDateString()}</span>
        ${event.federation_id ? `<span>Federation #${event.federation_id}</span>` : ""}
      </div>
    `;
    eventList.appendChild(item);
  });
}

async function loadAthletes() {
  try {
    const data = await request("/accounts/");
    state.athletes = data;
    renderAthletes();
  } catch (error) {
    notify("error", `Unable to load athletes: ${error.message}`);
    console.error(error);
  }
}

async function loadEvents() {
  try {
    const data = await request("/events/");
    state.events = data;
    renderEvents();
  } catch (error) {
    notify("error", `Unable to load events: ${error.message}`);
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
