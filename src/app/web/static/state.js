import { sampleRosters, sampleFederations, sampleNews, sampleResults } from "./samples.js";

function clone(items, withId = false) {
  return items.map((item, index) =>
    withId ? { id: item.id ?? index + 1, ...item } : { ...item }
  );
}

export const state = {
  athletes: [],
  events: [],
  federations: clone(sampleFederations),
  rosters: clone(sampleRosters, true),
  results: clone(sampleResults),
  news: clone(sampleNews),
  federationToken: null,
};

export function setAthletes(athletes = []) {
  state.athletes = clone(athletes);
}

export function setEvents(events = []) {
  state.events = clone(events);
}

export function setFederations(federations = []) {
  state.federations = clone(federations, true);
}

export function setRosters(rosters = []) {
  state.rosters = clone(rosters, true);
}

export function setResults(results = []) {
  state.results = clone(results);
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
  if (partial.federations && Array.isArray(partial.federations)) {
    setFederations(partial.federations);
  }
  if (partial.rosters && Array.isArray(partial.rosters)) {
    setRosters(partial.rosters);
  }
  if (partial.results && Array.isArray(partial.results)) {
    setResults(partial.results);
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
