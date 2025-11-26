export function formatTimestamp(timestamp) {
  if(!timestamp) return ""
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
