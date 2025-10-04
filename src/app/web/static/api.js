export const API_BASE = "/api/v1";

export async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let detail = null;
    try {
      detail = await response.json();
    } catch (error) {
      detail = null;
    }
    const error = new Error(detail?.detail || response.statusText || "Request failed");
    error.status = response.status;
    error.payload = detail;
    throw error;
  }

  if (response.status === 204) {
    return null;
  }

  try {
    return await response.json();
  } catch (error) {
    return null;
  }
}
