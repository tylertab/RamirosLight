import { request } from "./api.js";

export function initializeSignupPage({ notify }) {
  const form = document.querySelector("#signup-form");

  if (!form) {
    return;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());
    try {
      await request("/accounts/register", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      notify("success", "Account created successfully. Sign in to continue.");
      window.location.href = "/login";
    } catch (error) {
      if (error.status === 409) {
        notify("error", "This email is already registered.");
      } else {
        notify("error", `Unable to create account: ${error.message}`);
      }
      console.error(error);
    }
  });
}
