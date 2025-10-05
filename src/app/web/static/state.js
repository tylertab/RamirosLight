import { sampleFederations, sampleResults } from "./samples.js";

function cloneFederations(federations = []) {
  return federations.map((federation, federationIndex) => ({
    id: federation.id ?? federationIndex + 1,
    name: federation.name,
    country: federation.country,
    website: federation.website,
    clubs: (federation.clubs ?? []).map((club, clubIndex) => ({
      id: club.id ?? federationIndex * 100 + clubIndex + 1,
      name: club.name,
      city: club.city,
      country: club.country,
      rosters: (club.rosters ?? []).map((roster, rosterIndex) => ({
        id: roster.id ?? clubIndex * 100 + rosterIndex + 1,
        name: roster.name,
        division: roster.division,
        coach_name: roster.coach_name,
        athlete_count: roster.athlete_count,
        updated_at: roster.updated_at,
      })),
    })),
  }));
}

function cloneResults(results = []) {
  return results.map((result) => ({ ...result }));
}

export const state = {
  federations: cloneFederations(sampleFederations),
  results: cloneResults(sampleResults),
  federationToken: null,
};

export function setFederations(federations = []) {
  state.federations = cloneFederations(federations);
}

export function setResults(results = []) {
  state.results = cloneResults(results);
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
