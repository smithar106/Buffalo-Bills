import DemoBadge from "@/components/DemoBadge";
import Chat from "@/components/Chat";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/format";
import type { HeadToHead } from "@/types";

export const metadata = { title: "History — Bills Mafia AI" };

async function safeH2H(opponent: string): Promise<HeadToHead | null> {
  try {
    return (await api.headToHead(opponent)).head_to_head;
  } catch {
    return null;
  }
}

function HeadToHeadBlock({ h2h }: { h2h: HeadToHead }) {
  return (
    <div className="rounded-sm border border-bills-navy/10 bg-white p-5 shadow-card">
      <h2 className="font-display text-sm font-bold uppercase tracking-wide text-bills-red">
        Bills vs {h2h.team_b.name}
      </h2>
      <p className="mt-1 text-xs text-bills-steel">
        {h2h.start_season}–{h2h.end_season} ·{" "}
        <span className="font-bold text-bills-navy">
          Bills {h2h.team_a_wins} — {h2h.team_b_wins} {h2h.team_b.abbreviation}
        </span>
      </p>
      <ul className="mt-4 divide-y divide-bills-navy/5">
        {h2h.meetings.map((g) => {
          const isHome = g.home_team.id === "buf";
          const billsScore = isHome ? g.home_score : g.away_score;
          const oppScore = isHome ? g.away_score : g.home_score;
          return (
            <li key={g.id} className="flex items-center justify-between py-2 text-sm">
              <span className="text-bills-steel">
                {g.season} · {formatDate(g.kickoff)}
              </span>
              <span className="font-display font-bold tabular text-bills-navy">
                {billsScore}–{oppScore}
              </span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export default async function HistoryPage() {
  const [chiefs, dolphins] = await Promise.all([
    safeH2H("Chiefs"),
    safeH2H("Dolphins"),
  ]);

  return (
    <div className="mx-auto max-w-6xl px-4 py-10">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="font-display text-3xl font-bold uppercase tracking-tight text-bills-navy">
          History
        </h1>
        <DemoBadge demo />
      </div>

      <div className="grid gap-5 lg:grid-cols-2">
        {chiefs && <HeadToHeadBlock h2h={chiefs} />}
        {dolphins && <HeadToHeadBlock h2h={dolphins} />}
      </div>

      <div className="mt-10 rounded-sm border border-bills-navy/10 bg-bills-navy p-6">
        <h2 className="mb-2 font-display text-sm font-bold uppercase tracking-wide text-bills-red">
          Ask History
        </h2>
        <p className="mb-4 text-sm text-white/70">
          Explore Bills history — playoff runs, rivalries, the Josh Allen era.
        </p>
        <Chat />
      </div>
    </div>
  );
}
