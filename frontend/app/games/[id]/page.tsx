import DemoBadge from "@/components/DemoBadge";
import Chat from "@/components/Chat";
import { api } from "@/lib/api";
import { formatDate, formatTime } from "@/lib/format";
import type { Game, Play } from "@/types";

export const metadata = { title: "Game — Bills Mafia AI" };

const GAME_QUESTIONS = [
  "What changed after halftime?",
  "Why did Buffalo lose?",
  "Who had the biggest impact?",
  "How did Josh perform under pressure?",
];

function QuarterTable({ game }: { game: Game }) {
  if (!game.quarter_scores.length) return null;
  return (
    <div className="overflow-hidden rounded-sm border border-bills-navy/10 bg-white shadow-card">
      <div className="border-b border-bills-navy/10 px-4 py-2">
        <h2 className="font-display text-sm font-bold uppercase tracking-wide text-bills-red">
          Scoring by quarter
        </h2>
      </div>
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-bills-navy/10 text-[11px] font-semibold uppercase tracking-wide text-bills-steel">
            <th className="px-4 py-2 text-left">Team</th>
            {game.quarter_scores.map((q) => (
              <th key={q.quarter} className="px-2 py-2 text-center">
                Q{q.quarter}
              </th>
            ))}
            <th className="px-4 py-2 text-right">Final</th>
          </tr>
        </thead>
        <tbody>
          {[game.home_team, game.away_team].map((team) => {
            const isHome = team.id === game.home_team.id;
            const quarters = game.quarter_scores.map((q) =>
              isHome ? q.home : q.away,
            );
            const total = isHome ? game.home_score : game.away_score;
            return (
              <tr key={team.id} className="border-b border-bills-navy/5">
                <td className="px-4 py-2 font-semibold text-bills-navy">
                  {team.abbreviation}
                </td>
                {quarters.map((val, i) => (
                  <td key={i} className="px-2 py-2 text-center tabular">
                    {val}
                  </td>
                ))}
                <td className="px-4 py-2 text-right font-display font-bold tabular text-bills-navy">
                  {total}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

function ScoringPlays({ plays }: { plays: Play[] }) {
  const scoring = plays.filter((p) => p.points > 0);
  if (!scoring.length) return null;
  return (
    <div className="rounded-sm border border-bills-navy/10 bg-white p-5 shadow-card">
      <h2 className="font-display text-sm font-bold uppercase tracking-wide text-bills-red">
        Scoring plays
      </h2>
      <ul className="mt-3 divide-y divide-bills-navy/5">
        {scoring.map((p) => (
          <li key={p.play_id} className="flex items-start gap-3 py-2.5 text-sm">
            <span className="rounded-sm bg-bills-blue/10 px-1.5 py-0.5 text-[11px] font-bold text-bills-blue">
              Q{p.quarter} {p.time}
            </span>
            <span className="flex-1 text-bills-navy">{p.description}</span>
            <span className="font-bold tabular text-bills-navy">{p.points} pts</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default async function GamePage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  let game: Game | null = null;
  let plays: Play[] = [];
  let demo = false;
  try {
    const g = await api.game(id);
    game = g.game;
    demo = g.demo;
    const p = await api.plays(id);
    plays = p.plays;
  } catch {
    // fall through
  }

  if (!game) {
    return (
      <div className="mx-auto max-w-6xl px-4 py-10">
        <p className="text-sm text-bills-steel">Game not found.</p>
      </div>
    );
  }

  const isHome = game.home_team.id === "buf";
  const billsScore = isHome ? game.home_score : game.away_score;
  const oppScore = isHome ? game.away_score : game.home_score;
  const opponent = isHome ? game.away_team : game.home_team;

  return (
    <div className="mx-auto max-w-6xl px-4 py-10">
      <div className="flex items-center justify-between">
        <p className="text-xs font-semibold uppercase tracking-wide text-bills-steel">
          Week {game.week} · {formatDate(game.kickoff)} · {formatTime(game.kickoff)}
        </p>
        <DemoBadge demo={demo} />
      </div>

      <div className="mt-4 flex items-end justify-between">
        <div>
          <h1 className="font-display text-4xl font-bold uppercase tracking-tight text-bills-navy">
            Bills {isHome ? "vs" : "@"} {opponent.name}
          </h1>
          <p className="mt-1 text-sm text-bills-steel">
            {game.venue} · {game.location}
          </p>
        </div>
        {game.status === "final" && (
          <div className="text-right">
            <p className="font-display text-5xl font-bold tabular text-bills-navy">
              {billsScore}–{oppScore}
            </p>
            <span
              className={`text-sm font-bold uppercase ${
                (billsScore ?? 0) > (oppScore ?? 0)
                  ? "text-bills-blue"
                  : "text-bills-red"
              }`}
            >
              {(billsScore ?? 0) > (oppScore ?? 0) ? "Bills win" : "Bills loss"}
            </span>
          </div>
        )}
      </div>

      <div className="mt-8 grid gap-5 lg:grid-cols-2">
        <QuarterTable game={game} />
        <ScoringPlays plays={plays} />
      </div>

      <div className="mt-10 rounded-sm border border-bills-navy/10 bg-bills-navy p-6">
        <h2 className="mb-1 font-display text-sm font-bold uppercase tracking-wide text-bills-red">
          Ask about this game
        </h2>
        <p className="mb-4 text-sm text-white/70">
          Grounded answers using this game&apos;s box score and play-by-play.
        </p>
        <div className="mb-4 flex flex-wrap gap-1.5">
          {GAME_QUESTIONS.map((q) => (
            <span
              key={q}
              className="rounded-sm border border-white/20 px-3 py-1.5 text-xs text-white/80"
            >
              {q}
            </span>
          ))}
        </div>
        <Chat context={game.id} />
      </div>
    </div>
  );
}
