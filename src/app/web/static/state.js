import { sampleFederations, sampleResults } from "./samples.js";

function clone(items, withId = false) {
  return items.map((item, index) =>
    withId ? { id: item.id ?? index + 1, ...item } : { ...item }
  );
}

export const state = {
  federations: clone(sampleFederations, true),
  results: clone(sampleResults),
  federationToken: null,
};

export function setFederations(federations = []) {
  state.federations = clone(federations, true);
}

export function setResults(results = []) {
  state.results = clone(results);
}

export function updateHomeState(partial = {}) {
  if (partial.federations && Array.isArray(partial.federations)) {
    setFederations(partial.federations);
  }
  if (partial.results && Array.isArray(partial.results)) {
    setResults(partial.results);
  }
}

export function hydrateHomeState(initialHomeData) {
  if (!initialHomeData) {
    return;
  }
  updateHomeState(initialHomeData);
}
