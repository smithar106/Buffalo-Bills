import DemoBadge from "@/components/DemoBadge";
import { api } from "@/lib/api";
import { formatStatLabel } from "@/lib/format";
import type { TeamStat } from "@/types";

export const metadata = { title: "Stats — Bills Mafia AI" };

export default async function StatsPage() {
  let stats: TeamStat[] = [];
  let demo = false;
  try {
    const res = await api.teamStats(2026);
    stats = res.stats;
    demo = res.demo;
  } catch {
    // fall through
  }

  return (
    <div className="mx-auto max-w-6xl px-4 py-10">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="font-display text-3xl font-bold uppercase tracking-tight text-bills-navy">
          Team stats
        </h1>
        <DemoBadge demo={demo} />
      </div>

      {stats.length === 0 ? (
        <p className="text-sm text-bills-steel">Stats unavailable.</p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {stats.map((s) => (
            <div
              key={s.category}
              className="rounded-sm border border-bills-navy/10 bg-white p-5 shadow-card"
            >
              <p className="text-xs font-semibold uppercase tracking-wide text-bills-steel">
                {formatStatLabel(s.category)}
              </p>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="font-display text-4xl font-bold text-bills-navy">
                  {Number.isInteger(s.value) ? s.value : s.value.toFixed(1)}
                </span>
              </div>
              <p className="mt-2 text-xs text-bills-steel">
                NFL rank: <span className="font-bold text-bills-navy">{s.rank}</span>
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
