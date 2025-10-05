import { request } from "./api.js";
import { sampleFederations, sampleResults } from "./samples.js";
import { hydrateHomeState, setFederations, setResults, state } from "./state.js";
import { translations } from "./translations.js";

function translate(key, replacements = {}) {
  const locale = document.documentElement.lang;
  const dictionary = translations[locale] || translations.en;
  const fallback = translations.en;
  const template = dictionary[key] ?? fallback[key] ?? key;
  return template.replace(/\{(\w+)\}/g, (match, token) => {
    return token in replacements ? replacements[token] : match;
  });
}

export function initializeHomePage({ initialData, notify }) {
  if (initialData) {
    hydrateHomeState(initialData);
  }

  if (!state.federations.length) {
    setFederations(sampleFederations);
  }

  if (!state.results.length) {
    setResults(sampleResults);
  }

  const federationsList = document.querySelector("#federations-list");
  const federationsEmpty = document.querySelector("#federations-empty");
  const resultsList = document.querySelector("#results-list");
  const resultsEmpty = document.querySelector("#results-empty");
  const emailForm = document.querySelector("#email-signup");
  const emailInput = document.querySelector("#email-address");
  const headerEmailButton = document.querySelector("#header-email");

  function renderFederations() {
    if (!federationsList || !federationsEmpty) {
      return;
    }
    federationsList.innerHTML = "";
    if (!state.federations.length) {
      federationsEmpty.hidden = false;
      return;
    }

    federationsEmpty.hidden = true;
    state.federations.forEach((federation) => {
      const item = document.createElement("li");
      item.className = "card";
      const clubs = Array.isArray(federation.clubs)
        ? federation.clubs
        : [];
      const clubCount = clubs.length;
      const rosterCount = clubs.reduce((total, club) => {
        if (!club || !Array.isArray(club.rosters)) {
          return total;
        }
        return total + club.rosters.length;
      }, 0);
      const highlightClubs = clubs
        .slice(0, 3)
        .map((club) => club.name)
        .filter(Boolean)
        .join(", ");
      item.innerHTML = `
        <h3>${federation.name}</h3>
        <div class="card-meta">
          <span>${translate("home.federations_country")}: ${federation.country ?? "–"}</span>
          <span>${translate("home.federations_clubs", { count: clubCount })}</span>
          <span>${translate("home.federations_rosters", { count: rosterCount })}</span>
        </div>
        ${
          highlightClubs
            ? `<p class="card-footnote">${highlightClubs}</p>`
            : ""
        }
      `;
      federationsList.appendChild(item);
    });
  }

  function renderResults() {
    if (!resultsList || !resultsEmpty) {
      return;
    }
    resultsList.innerHTML = "";
    if (!state.results.length) {
      resultsEmpty.hidden = false;
      return;
    }

    resultsEmpty.hidden = true;
    state.results.forEach((result) => {
      const item = document.createElement("li");
      item.className = "card";
      const medalistItems = (result.medalists || [])
        .map((medalist) => `<li>${medalist}</li>`)
        .join("");
      item.innerHTML = `
        <div class="card-meta">
          <span>${translate("home.results_event")}: ${result.event}</span>
          <span>${translate("home.results_discipline")}: ${result.discipline}</span>
        </div>
        <ul class="medalist-list" aria-label="${translate("home.results_medalists")}">
          ${medalistItems}
        </ul>
      `;
      resultsList.appendChild(item);
    });
  }

  function renderHome() {
    renderFederations();
    renderResults();
  }

  renderHome();

  window.addEventListener("trackeo:locale-change", renderHome);

  if (emailForm && emailInput) {
    emailForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (!emailForm.reportValidity()) {
        return;
      }
      const email = emailInput.value.trim();
      if (!email) {
        notify("error", translate("home.email_error"));
        return;
      }
      try {
        const locale = document.documentElement.lang || "en";
        const response = await request("/subscribers", {
          method: "POST",
          body: JSON.stringify({ email, locale }),
        });
        const confirmedEmail = response?.email || email;
        notify("success", translate("home.email_success", { email: confirmedEmail }));
        emailInput.value = "";
        emailInput.focus({ preventScroll: true });
      } catch (error) {
        if (error.status === 409) {
          notify("info", translate("home.email_duplicate", { email }));
          return;
        }
        notify("error", translate("home.email_failure"));
      }
    });
  }

  function focusEmailForm() {
    if (!emailInput) {
      return;
    }
    emailInput.focus({ preventScroll: true });
  }

  if (headerEmailButton) {
    headerEmailButton.addEventListener("click", () => {
      if (emailForm) {
        emailForm.scrollIntoView({ behavior: "smooth", block: "center" });
      }
      focusEmailForm();
    });
  }
}
