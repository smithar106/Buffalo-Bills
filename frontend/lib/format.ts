export function formatDate(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
  });
}

export function formatTime(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "2-digit",
  });
}

export function timeAgo(iso: string): string {
  const then = new Date(iso).getTime();
  const now = Date.now();
  const mins = Math.max(0, Math.floor((now - then) / 60000));
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins} min ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  return `${days}d ago`;
}

export function formatStatLabel(category: string): string {
  const labels: Record<string, string> = {
    points_per_game: "Points / game",
    points_allowed_per_game: "Points allowed / game",
    passing_yards_per_game: "Passing yards / game",
    rushing_yards_per_game: "Rushing yards / game",
    total_yards_per_game: "Total yards / game",
  };
  return labels[category] ?? category.replace(/_/g, " ");
}
