const TOKEN_STORAGE_KEY = "trackeo.auth.token";
const TOKEN_EXPIRY_KEY = "trackeo.auth.expires";
const TOKEN_TIER_KEY = "trackeo.auth.tier";

export function storeAuthToken(token, expiresAt, tier) {
  try {
    if (token) {
      localStorage.setItem(TOKEN_STORAGE_KEY, token);
    }
    if (expiresAt) {
      const value = expiresAt instanceof Date ? expiresAt.toISOString() : String(expiresAt);
      localStorage.setItem(TOKEN_EXPIRY_KEY, value);
    }
    if (tier) {
      localStorage.setItem(TOKEN_TIER_KEY, tier);
    }
  } catch (error) {
    console.warn("Unable to persist auth token", error);
  }
}

export function readAuthToken() {
  try {
    const token = localStorage.getItem(TOKEN_STORAGE_KEY);
    const expires = localStorage.getItem(TOKEN_EXPIRY_KEY);
    return {
      token,
      expiresAt: expires,
      tier: localStorage.getItem(TOKEN_TIER_KEY),
    };
  } catch (error) {
    return { token: null, expiresAt: null, tier: null };
  }
}
