import type {
  ChatMode,
  ChatResponse,
  Game,
  HeadToHead,
  Injury,
  NewsItem,
  Player,
  PlayerGameLogEntry,
  PlayerSeasonStat,
  Play,
  StandingsEntry,
  TeamStat,
} from "@/types";

const BASE = process.env.API_URL || "http://localhost:8000";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export interface NextGameResult {
  game: Game;
  demo: boolean;
}

export interface ScheduleResult {
  games: Game[];
  season: number;
  demo: boolean;
}

export interface StandingsResult {
  standings: StandingsEntry[];
  demo: boolean;
}

export interface RosterResult {
  roster: Player[];
  demo: boolean;
}

export interface PlayerStatsResult {
  player: string;
  stats: PlayerSeasonStat[];
  demo: boolean;
}

export interface TeamStatsResult {
  stats: TeamStat[];
  season: number;
  demo: boolean;
}

export interface InjuriesResult {
  injuries: Injury[];
  demo: boolean;
}

export interface NewsResult {
  news: NewsItem[];
  demo: boolean;
}

export interface PlaysResult {
  game_id: string;
  plays: Play[];
  demo: boolean;
}

export interface GameLogResult {
  player: string;
  game_log: PlayerGameLogEntry[];
  demo: boolean;
}

export interface HeadToHeadResult {
  head_to_head: HeadToHead;
  demo: boolean;
}

export const api = {
  nextGame: () => get<NextGameResult>("/api/next-game"),
  schedule: (season = 2026) => get<ScheduleResult>(`/api/schedule?season=${season}`),
  recentGames: (limit = 5) => get<ScheduleResult>(`/api/games/recent?limit=${limit}`),
  game: (id: string) => get<NextGameResult>(`/api/games/${id}`),
  plays: (id: string) => get<PlaysResult>(`/api/games/${id}/plays`),
  standings: () => get<StandingsResult>("/api/standings"),
  roster: () => get<RosterResult>("/api/roster"),
  playerStats: (player: string, season = 2026) =>
    get<PlayerStatsResult>(`/api/stats/player?player=${encodeURIComponent(player)}&season=${season}`),
  teamStats: (season = 2026) => get<TeamStatsResult>(`/api/stats/team?season=${season}`),
  gameLog: (player: string, season = 2026) =>
    get<GameLogResult>(`/api/stats/player/${encodeURIComponent(player)}/game-log?season=${season}`),
  injuries: () => get<InjuriesResult>("/api/injuries"),
  news: (limit = 5) => get<NewsResult>(`/api/news?limit=${limit}`),
  headToHead: (opponent: string, start = 2018, end = 2026) =>
    get<HeadToHeadResult>(
      `/api/head-to-head?opponent=${encodeURIComponent(opponent)}&start_season=${start}&end_season=${end}`,
    ),
  chat: (question: string, mode: ChatMode, context?: string) =>
    fetch(`${BASE}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, mode, context }),
    }).then((r) => r.json()) as Promise<ChatResponse>,
};
