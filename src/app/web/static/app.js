import { API_BASE } from "./api.js";
import { createNotifier } from "./notifications.js";
import { applyLocale, readStoredLocale } from "./translations.js";
import { initializeHomePage } from "./home.js";
import { initializeProfilesPage } from "./profiles.js";
import { initializeEventsPage } from "./events-page.js";
import { initializeEventDetailPage } from "./event-detail.js";
import { initializeRostersPage } from "./rosters-page.js";
import { initializeAthleteDetailPage } from "./athlete-detail.js";
import { initializeRosterDetailPage } from "./roster-detail.js";
import { initializeLoginPage } from "./login.js";
import { initializeSignupPage } from "./signup.js";
import { initializeFederationsUploadPage } from "./federations-upload.js";

const body = document.body;
const pageId = body?.dataset?.page ?? "home";
const notificationsElement = document.querySelector("#notifications");
const notify = createNotifier(notificationsElement);
const localeSwitcher = document.querySelector("#locale-switcher");
const headerLoginButton = document.querySelector("#header-login");
const headerEmailButton = document.querySelector("#header-email");
const apiBaseLabel = document.querySelector("#api-base");

if (apiBaseLabel) {
  apiBaseLabel.textContent = API_BASE;
}

function parseInitialData(selector) {
  const element = document.querySelector(selector);
  if (!element?.textContent) {
    return null;
  }
  try {
    return JSON.parse(element.textContent.trim());
  } catch (error) {
    console.warn(`Unable to parse initial data for ${selector}`, error);
    return null;
  }
}

const initialHomeData = parseInitialData("#initial-home-data");
const initialEventData = parseInitialData("#initial-event-data");

const storedLocale = readStoredLocale();
const activeLocale = applyLocale(storedLocale || navigator.language?.slice(0, 2) || "en", {
  switcher: localeSwitcher,
});

if (localeSwitcher) {
  localeSwitcher.value = activeLocale;
  localeSwitcher.addEventListener("change", (event) => {
    applyLocale(event.target.value, { switcher: localeSwitcher });
  });
}

if (headerLoginButton) {
  headerLoginButton.addEventListener("click", () => {
    window.location.href = "/login";
  });
}

if (headerEmailButton) {
  headerEmailButton.addEventListener("click", () => {
    if (pageId !== "home") {
      window.location.href = "/#hero";
    }
  });
}

switch (pageId) {
  case "home":
    initializeHomePage({ initialData: initialHomeData, notify });
    break;
  case "profiles":
    initializeProfilesPage({ notify });
    break;
  case "events":
    initializeEventsPage({ notify });
    break;
  case "event-detail":
    initializeEventDetailPage({ initialData: initialEventData, notify });
    break;
  case "rosters":
    initializeRostersPage({ notify });
    break;
  case "athlete-detail":
    initializeAthleteDetailPage({ notify });
    break;
  case "roster-detail":
    initializeRosterDetailPage({ notify });
    break;
  case "login":
    initializeLoginPage({ notify });
    break;
  case "signup":
    initializeSignupPage({ notify });
    break;
  case "federations-upload":
    initializeFederationsUploadPage({ notify });
    break;
  default:
    break;
}
