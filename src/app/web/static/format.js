export function formatDateTime(value) {
  if (!value) {
    return "";
  }
  const date = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "";
  }
  return date.toLocaleString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function formatTimeRange(start, end) {
  const startDate = start ? (start instanceof Date ? start : new Date(start)) : null;
  const endDate = end ? (end instanceof Date ? end : new Date(end)) : null;
  if (startDate && Number.isNaN(startDate.getTime())) {
    return "";
  }
  if (endDate && Number.isNaN(endDate.getTime())) {
    return "";
  }
  if (startDate && endDate) {
    const sameDay = startDate.toDateString() === endDate.toDateString();
    const startText = startDate.toLocaleString(undefined, {
      month: sameDay ? undefined : "short",
      day: sameDay ? undefined : "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
    const endText = endDate.toLocaleString(undefined, {
      month: sameDay ? undefined : "short",
      day: sameDay ? undefined : "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
    return `${startText} – ${endText}`;
  }
  if (startDate) {
    return startDate.toLocaleString(undefined, {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }
  if (endDate) {
    return endDate.toLocaleString(undefined, {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }
  return "";
}

export function formatDate(value) {
  if (!value) {
    return "";
  }
  const date = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(date.getTime())) {
    return typeof value === "string" ? value : "";
  }
  return date.toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export function isFutureDate(value) {
  const date = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(date.getTime())) {
    return false;
  }
  return date.getTime() >= Date.now() - 86400000;
}
