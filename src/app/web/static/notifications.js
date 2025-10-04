export function createNotifier(container) {
  return function notify(type, message) {
    if (!container) {
      return;
    }
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => {
      toast.classList.add("fade");
      toast.addEventListener(
        "transitionend",
        () => toast.remove(),
        { once: true }
      );
      toast.style.opacity = "0";
    }, 3500);
  };
}
