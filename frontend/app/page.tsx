import Hero from "@/components/Hero";
import NextGameCard from "@/components/NextGameCard";
import LatestResultCard from "@/components/LatestResultCard";
import StandingsTable from "@/components/StandingsTable";
import TrendingList from "@/components/TrendingList";
import DemoBadge from "@/components/DemoBadge";
import { api } from "@/lib/api";
import type { Game, NewsItem, StandingsEntry } from "@/types";

async function safeNextGame(): Promise<Game | null> {
  try {
    return (await api.nextGame()).game;
  } catch {
    return null;
  }
}

async function safeLatest(): Promise<Game | null> {
  try {
    const games = (await api.recentGames(5)).games;
    return games[0] ?? null;
  } catch {
    return null;
  }
}

async function safeStandings(): Promise<StandingsEntry[] | null> {
  try {
    return (await api.standings()).standings;
  } catch {
    return null;
  }
}

async function safeNews(): Promise<NewsItem[] | null> {
  try {
    return (await api.news(5)).news;
  } catch {
    return null;
  }
}

export default async function GameDayPage() {
  const [nextGame, latest, standings, news] = await Promise.all([
    safeNextGame(),
    safeLatest(),
    safeStandings(),
    safeNews(),
  ]);

  const demo = true; // mock provider is active by default

  return (
    <div>
      <Hero />

      <div className="mx-auto max-w-6xl px-4 py-10">
        {demo && (
          <div className="mb-6 flex justify-center">
            <DemoBadge demo={demo} />
          </div>
        )}

        <div className="grid gap-5 md:grid-cols-2">
          {nextGame && <NextGameCard game={nextGame} />}
          {latest && <LatestResultCard game={latest} />}
        </div>

        <div className="mt-5 grid gap-5 lg:grid-cols-2">
          {standings && <StandingsTable standings={standings} />}
          {news && <TrendingList news={news} />}
        </div>
      </div>
    </div>
  );
}
