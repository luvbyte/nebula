import Toastify from "toastify-js";
// import "toastify-js/src/toastify.css";

export function toast(message, tp = "success") {
  if (!message || message === "") return;

  const styles = {
    success: "linear-gradient(to right, #00b09b, #96c93d)",
    error: "linear-gradient(to right, #f85032, #e73827)",
    warning: "linear-gradient(to right, #f7971e, #ffd200)",
    info: "linear-gradient(to right, #2193b0, #6dd5ed)"
  };

  Toastify({
    text: message.toString(),
    duration: 2000,
    gravity: "bottom",
    position: "center",
    stopOnFocus: true,
    style: {
      background: styles[tp] || styles.info
    }
  }).showToast();
}

export function formatTimestamp(timestamp) {
  if (!timestamp) return "";
  const now: any = new Date();
  const date: any = new Date(timestamp);

  const diffMs = now - date;
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHour = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHour / 24);

  // --- Recent times ---
  if (diffSec < 60) {
    return diffSec <= 1 ? "just now" : `${diffSec} seconds ago`;
  }

  if (diffMin < 60) {
    return `${diffMin} min ago`;
  }

  if (diffHour < 24) {
    return `${diffHour} hours ago`;
  }

  // --- Date formatting helpers ---
  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"
  ];
  const month = months[date.getMonth()];
  const day = date.getDate();

  let hour = date.getHours();
  const minute = date.getMinutes().toString().padStart(2, "0");
  const ampm = hour >= 12 ? "PM" : "AM";
  hour = hour % 12 || 12; // convert to 12-hour clock

  const timeStr = `${hour}:${minute} ${ampm}`;

  const thisYear = now.getFullYear();
  const year = date.getFullYear();

  // --- Today ---
  if (diffDay === 0) {
    return timeStr;
  }

  // --- Yesterday or older within same year ---
  if (year === thisYear) {
    return `${month} ${day} at ${timeStr}`;
  }

  // --- Previous years ---
  return `${year} ${month} ${day} at ${timeStr}`;
}
