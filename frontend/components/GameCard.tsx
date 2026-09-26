import type { Game } from "@/types";
import { formatDate, formatTime } from "@/lib/format";
import Link from "next/link";

export default function GameCard({ game }: { game: Game }) {
  const isHome = game.home_team.id === "buf";
  const opponent = isHome ? game.away_team : game.home_team;
  const billsScore = isHome ? game.home_score : game.away_score;
  const oppScore = isHome ? game.away_score : game.home_score;

  const won = game.status === "final" && (billsScore ?? 0) > (oppScore ?? 0);
  const lost = game.status === "final" && !won;

  return (
    <Link
      href={`/games/${game.id}`}
      className="block rounded-sm border border-bills-navy/10 bg-white p-4 shadow-card transition-shadow hover:shadow-lift"
    >
      <div className="flex items-center justify-between text-xs text-bills-steel">
        <span className="font-bold uppercase tracking-wide">Week {game.week}</span>
        <span>
          {formatDate(game.kickoff)} · {formatTime(game.kickoff)}
        </span>
      </div>

      <div className="mt-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="flex h-8 w-8 items-center justify-center rounded-sm bg-bills-navy text-[10px] font-bold text-white">
            BUF
          </span>
          <span className="font-display text-sm font-bold text-bills-navy">
            {isHome ? "vs" : "@"}
          </span>
          <span className="flex h-8 w-8 items-center justify-center rounded-sm bg-bills-silver text-[10px] font-bold text-bills-navy">
            {opponent.abbreviation}
          </span>
        </div>

        {game.status === "final" ? (
          <div className="text-right">
            <p className="font-display text-lg font-bold tabular text-bills-navy">
              {billsScore}–{oppScore}
            </p>
            <span
              className={`text-[11px] font-bold uppercase ${
                won ? "text-bills-blue" : lost ? "text-bills-red" : "text-bills-steel"
              }`}
            >
              {won ? "W" : lost ? "L" : "—"}
            </span>
          </div>
        ) : (
          <span className="rounded-sm bg-bills-blue/10 px-2 py-0.5 text-[11px] font-bold uppercase text-bills-blue">
            {game.status}
          </span>
        )}
      </div>
    </Link>
  );
}
