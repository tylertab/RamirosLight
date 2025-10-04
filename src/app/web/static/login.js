import { API_BASE, request } from "./api.js";
import { storeAuthToken } from "./auth-storage.js";
import { state } from "./state.js";

export function initializeLoginPage({ notify }) {
  const form = document.querySelector("#login-form");

  if (!form) {
    return;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const params = new URLSearchParams();
    formData.forEach((value, key) => {
      params.append(key, value);
    });
    try {
      const response = await fetch(`${API_BASE}/accounts/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: params.toString(),
      });
      if (!response.ok) {
        throw new Error("Incorrect credentials");
      }
      const data = await response.json();
      storeAuthToken(data.access_token, data.expires_at, data.subscription_tier);
      state.federationToken = data.access_token;
      notify("success", "Signed in successfully. Token stored for secure uploads.");
      window.location.href = "/";
    } catch (error) {
      notify("error", error.message || "Unable to sign in.");
      console.error(error);
    }
  });
}
