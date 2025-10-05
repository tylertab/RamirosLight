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
      const clubCountValue =
        federation.clubs ?? federation.club_count ?? 0;
      const formattedClubs =
        typeof clubCountValue === "number"
          ? clubCountValue.toLocaleString()
          : clubCountValue;
      item.innerHTML = `
        <h3>${federation.name}</h3>
        <div class="card-meta">
          <span>${translate("home.federations_country")}: ${federation.country}</span>
          <span>${translate("home.federations_clubs", { count: formattedClubs })}</span>
        </div>
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
    emailForm.addEventListener("submit", (event) => {
      event.preventDefault();
      if (!emailForm.reportValidity()) {
        return;
      }
      const email = emailInput.value.trim();
      if (!email) {
        notify("error", translate("home.email_error"));
        return;
      }
      notify("success", translate("home.email_success", { email }));
      emailInput.value = "";
      emailInput.focus({ preventScroll: true });
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
