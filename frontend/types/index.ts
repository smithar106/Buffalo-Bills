export interface Team {
  id: string;
  name: string;
  abbreviation: string;
  city: string;
  conference: string;
  division: string;
}

export interface QuarterScore {
  quarter: number;
  home: number;
  away: number;
}

export interface Game {
  id: string;
  season: number;
  week: number;
  home_team: Team;
  away_team: Team;
  status: "scheduled" | "live" | "final";
  kickoff: string;
  venue: string;
  location: string;
  home_score: number | null;
  away_score: number | null;
  quarter_scores: QuarterScore[];
  source: string;
  retrieved_at: string;
}

export interface StandingsEntry {
  team: Team;
  wins: number;
  losses: number;
  ties: number;
  win_pct: number;
  division_wins: number;
  division_losses: number;
  points_for: number;
  points_against: number;
  season: number;
}

export interface Player {
  id: string;
  name: string;
  number: number;
  position: string;
  height: string;
  weight: number;
  college: string;
  experience: number;
}

export interface PlayerSeasonStat {
  player: Player;
  season: number;
  games_played: number;
  passing_yards: number;
  passing_tds: number;
  interceptions: number;
  rushing_yards: number;
  rushing_tds: number;
  receptions: number;
  receiving_yards: number;
  receiving_tds: number;
  tackles: number;
  sacks: number;
  field_goals_made: number;
  field_goals_attempted: number;
}

export interface TeamStat {
  season: number;
  category: string;
  value: number;
  rank: number;
}

export interface Injury {
  player: Player;
  status: string;
  injury: string;
  updated: string;
}

export interface NewsItem {
  id: string;
  title: string;
  publisher: string;
  published_at: string;
  url: string;
  summary: string;
}

export interface HeadToHead {
  team_a: Team;
  team_b: Team;
  start_season: number;
  end_season: number;
  meetings: Game[];
  team_a_wins: number;
  team_b_wins: number;
}

export interface Play {
  game_id: string;
  play_id: string;
  quarter: number;
  time: string;
  down: number;
  yards_to_go: number;
  description: string;
  offense: string;
  points: number;
}

export interface PlayerGameLogEntry {
  game_id: string;
  season: number;
  week: number;
  opponent: string;
  passing_yards: number;
  passing_tds: number;
  interceptions: number;
  rushing_yards: number;
  rushing_tds: number;
  receptions: number;
  receiving_yards: number;
  receiving_tds: number;
}

export interface Source {
  label: string;
  tool: string;
  retrieved_at: string;
  evidence?: string;
}

export interface ChatResponse {
  answer: string;
  mode: string;
  sources: Source[];
  demo: boolean;
  fallback: boolean;
}

export type ChatMode = "bills_mafia" | "analyst" | "simple" | "debate";

export interface FamilyUser {
  id: number;
  name: string;
}

export interface FamilyPrediction {
  id: number;
  game_id: string;
  user_id: number;
  bills_score: number;
  opponent_score: number;
  first_td_scorer: string;
  allen_passing_yards: number;
  mvp: string;
  locked: boolean;
}

export interface LeaderboardRow {
  name: string;
  weekly_points: number;
  season_points: number;
  correct_picks: number;
}
