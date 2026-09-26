import type { Game } from "@/types";
import { formatDate, formatTime } from "@/lib/format";
import Link from "next/link";

export default function NextGameCard({ game }: { game: Game }) {
  const isHome = game.home_team.id === "buf";
  const opponent = isHome ? game.away_team : game.home_team;

  return (
    <div className="rounded-sm border border-bills-navy/10 bg-white p-5 shadow-card">
      <div className="flex items-center justify-between">
        <h2 className="font-display text-sm font-bold uppercase tracking-wide text-bills-red">
          Next game
        </h2>
        <span className="text-xs font-semibold text-bills-steel">
          Week {game.week}
        </span>
      </div>

      <div className="mt-4 flex items-center justify-between">
        <div>
          <p className="font-display text-2xl font-bold uppercase leading-none text-bills-navy">
            {isHome ? "vs" : "@"} {opponent.abbreviation}
          </p>
          <p className="mt-1 text-sm text-bills-steel">{opponent.name}</p>
        </div>
        <div className="flex h-14 w-14 items-center justify-center rounded-sm bg-bills-navy font-display text-2xl font-bold text-white">
          {opponent.abbreviation}
        </div>
      </div>

      <dl className="mt-4 grid grid-cols-2 gap-x-4 gap-y-2 border-t border-bills-navy/10 pt-4 text-sm">
        <div>
          <dt className="text-xs font-semibold uppercase tracking-wide text-bills-steel">
            Date
          </dt>
          <dd className="font-semibold text-bills-navy">
            {formatDate(game.kickoff)}
          </dd>
        </div>
        <div>
          <dt className="text-xs font-semibold uppercase tracking-wide text-bills-steel">
            Time
          </dt>
          <dd className="font-semibold text-bills-navy">
            {formatTime(game.kickoff)}
          </dd>
        </div>
        <div>
          <dt className="text-xs font-semibold uppercase tracking-wide text-bills-steel">
            Location
          </dt>
          <dd className="font-semibold text-bills-navy">{game.location}</dd>
        </div>
      </dl>

      <Link
        href={`/games/${game.id}`}
        className="mt-4 block rounded-sm bg-bills-navy px-4 py-2 text-center font-display text-sm font-bold uppercase tracking-wide text-white transition-colors hover:bg-bills-blue"
      >
        Game preview
      </Link>
    </div>
  );
}
