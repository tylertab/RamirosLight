import { sampleRosters, sampleNews } from "./samples.js";

function clone(items, withId = false) {
  return items.map((item, index) =>
    withId ? { id: item.id ?? index + 1, ...item } : { ...item }
  );
}

export const state = {
  athletes: [],
  events: [],
  rosters: clone(sampleRosters, true),
  news: clone(sampleNews),
  federationToken: null,
};

export function setAthletes(athletes = []) {
  state.athletes = clone(athletes);
}

export function setEvents(events = []) {
  state.events = clone(events);
}

export function setRosters(rosters = []) {
  state.rosters = clone(rosters, true);
}

export function setNews(news = []) {
  state.news = clone(news);
}

export function updateHomeState(partial = {}) {
  if (partial.athletes && Array.isArray(partial.athletes)) {
    setAthletes(partial.athletes);
  }
  if (partial.events && Array.isArray(partial.events)) {
    setEvents(partial.events);
  }
  if (partial.rosters && Array.isArray(partial.rosters)) {
    setRosters(partial.rosters);
  }
  if (partial.news && Array.isArray(partial.news)) {
    setNews(partial.news);
  }
}

export function hydrateHomeState(initialHomeData) {
  if (!initialHomeData) {
    return;
  }
  updateHomeState(initialHomeData);
}
