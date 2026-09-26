import GameCard from "@/components/GameCard";
import DemoBadge from "@/components/DemoBadge";
import { api } from "@/lib/api";
import type { Game } from "@/types";

export const metadata = { title: "Schedule — Bills Mafia AI" };

export default async function SchedulePage() {
  let games: Game[] = [];
  let demo = false;
  try {
    const res = await api.schedule(2026);
    games = res.games;
    demo = res.demo;
  } catch {
    // fall through to empty state
  }

  const finals = games.filter((g) => g.status === "final");
  const upcoming = games.filter((g) => g.status !== "final");

  return (
    <div className="mx-auto max-w-6xl px-4 py-10">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="font-display text-3xl font-bold uppercase tracking-tight text-bills-navy">
          Schedule
        </h1>
        <DemoBadge demo={demo} />
      </div>

      {games.length === 0 ? (
        <p className="text-sm text-bills-steel">
          Schedule unavailable — is the API running?
        </p>
      ) : (
        <div className="space-y-8">
          <section>
            <h2 className="mb-3 font-display text-sm font-bold uppercase tracking-wide text-bills-red">
              Upcoming
            </h2>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {upcoming.map((g) => (
                <GameCard key={g.id} game={g} />
              ))}
            </div>
          </section>
          <section>
            <h2 className="mb-3 font-display text-sm font-bold uppercase tracking-wide text-bills-red">
              Results
            </h2>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {finals.map((g) => (
                <GameCard key={g.id} game={g} />
              ))}
            </div>
          </section>
        </div>
      )}
    </div>
  );
}
