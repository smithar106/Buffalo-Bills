import type { Game } from "@/types";
import { formatDate } from "@/lib/format";
import Link from "next/link";

export default function LatestResultCard({ game }: { game: Game }) {
  const isHome = game.home_team.id === "buf";
  const billsScore = isHome ? game.home_score : game.away_score;
  const oppScore = isHome ? game.away_score : game.home_score;
  const opponent = isHome ? game.away_team : game.home_team;
  const won = (billsScore ?? 0) > (oppScore ?? 0);

  return (
    <div className="rounded-sm border border-bills-navy/10 bg-white p-5 shadow-card">
      <div className="flex items-center justify-between">
        <h2 className="font-display text-sm font-bold uppercase tracking-wide text-bills-red">
          Latest result
        </h2>
        <span className="text-xs font-semibold text-bills-steel">
          {formatDate(game.kickoff)}
        </span>
      </div>

      <div className="mt-4 flex items-center justify-between">
        <div className="flex items-baseline gap-2">
          <span className="font-display text-4xl font-bold text-bills-navy">
            {billsScore}
          </span>
          <span className="font-display text-xl font-bold text-bills-steel">
            {oppScore}
          </span>
        </div>
        <div className="text-right">
          <p className="text-sm font-semibold text-bills-navy">
            {isHome ? "vs" : "@"} {opponent.name}
          </p>
          <span
            className={`mt-1 inline-block rounded-sm px-2 py-0.5 text-[11px] font-bold uppercase tracking-wide ${
              won ? "bg-bills-blue/10 text-bills-blue" : "bg-bills-red/10 text-bills-red"
            }`}
          >
            {won ? "Win" : "Loss"}
          </span>
        </div>
      </div>

      <Link
        href={`/games/${game.id}`}
        className="mt-4 block rounded-sm border border-bills-navy/20 px-4 py-2 text-center font-display text-sm font-bold uppercase tracking-wide text-bills-navy transition-colors hover:bg-bills-silver"
      >
        Game details
      </Link>
    </div>
  );
}
