import { request } from "./api.js";
import { formatDate } from "./format.js";
import { readAuthToken, storeAuthToken } from "./auth-storage.js";
import { state } from "./state.js";

export function initializeFederationsUploadPage({ notify }) {
  const form = document.querySelector("#federations-upload-form");
  const refreshButton = document.querySelector("#federations-refresh");
  const list = document.querySelector("#federations-submissions");
  const empty = document.querySelector("#federations-submissions-empty");

  function normalizeToken(value) {
    if (!value) {
      return null;
    }
    return value.startsWith("Bearer ") ? value : `Bearer ${value}`;
  }

  function renderSubmissions(submissions) {
    if (!list || !empty) {
      return;
    }
    list.innerHTML = "";
    if (!submissions.length) {
      empty.hidden = false;
      return;
    }
    empty.hidden = true;
    submissions
      .slice()
      .sort((a, b) => new Date(b.submitted_at).getTime() - new Date(a.submitted_at).getTime())
      .forEach((submission) => {
        const submitted = formatDate(submission.submitted_at);
        const processed = submission.verified_at ? formatDate(submission.verified_at) : null;
        const item = document.createElement("li");
        item.className = "card";
        item.innerHTML = `
          <div class="card-meta">
            <span class="tag">${submission.federation_name}</span>
            <span>${submission.status}</span>
            ${submitted ? `<span>${submitted}</span>` : ""}
          </div>
          <h3>${submission.payload_url}</h3>
          <p>${submission.notes || ""}</p>
          ${processed ? `<p>Verified ${processed}</p>` : ""}
        `;
        list.appendChild(item);
      });
  }

  async function loadSubmissions(token) {
    const authHeader = token || normalizeToken(state.federationToken) || normalizeToken(readAuthToken().token);
    if (!authHeader) {
      notify("error", "Provide an access token to view submissions.");
      return;
    }
    state.federationToken = authHeader;
    try {
      const submissions = await request("/federations/submissions", {
        headers: {
          Authorization: authHeader,
        },
      });
      renderSubmissions(submissions);
    } catch (error) {
      if (error.status === 401 || error.status === 403) {
        notify("error", "Token is invalid or lacks required permissions.");
      } else {
        notify("error", `Unable to load submissions: ${error.message}`);
      }
      console.error(error);
    }
  }

  if (form) {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(form);
      const tokenInput = formData.get("token");
      const authHeader = normalizeToken(tokenInput || readAuthToken().token);
      if (!authHeader) {
        notify("error", "A bearer token is required to submit files.");
        return;
      }
      state.federationToken = authHeader;
      if (tokenInput) {
        const rawToken = tokenInput.toString().replace(/^Bearer\s+/i, "");
        storeAuthToken(rawToken, new Date(Date.now() + 3600_000).toISOString(), readAuthToken().tier);
      }
      const payload = Object.fromEntries(formData.entries());
      delete payload.token;
      try {
        await request("/federations/submissions", {
          method: "POST",
          headers: {
            Authorization: authHeader,
          },
          body: JSON.stringify(payload),
        });
        form.reset();
        notify("success", "Submission queued for processing.");
        await loadSubmissions(authHeader);
      } catch (error) {
        notify("error", `Upload failed: ${error.message}`);
        console.error(error);
      }
    });
  }

  if (refreshButton) {
    refreshButton.addEventListener("click", () => {
      loadSubmissions();
    });
  }

  const stored = readAuthToken();
  if (stored.token) {
    state.federationToken = normalizeToken(stored.token);
    loadSubmissions(state.federationToken);
  }
}
