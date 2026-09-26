import DemoBadge from "@/components/DemoBadge";
import { api } from "@/lib/api";
import type { Player } from "@/types";

export const metadata = { title: "Roster — Bills Mafia AI" };

export default async function RosterPage() {
  let roster: Player[] = [];
  let demo = false;
  try {
    const res = await api.roster();
    roster = res.roster;
    demo = res.demo;
  } catch {
    // fall through
  }

  const ordered = [...roster].sort((a, b) => a.number - b.number);

  return (
    <div className="mx-auto max-w-6xl px-4 py-10">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="font-display text-3xl font-bold uppercase tracking-tight text-bills-navy">
          Roster
        </h1>
        <DemoBadge demo={demo} />
      </div>

      <div className="overflow-hidden rounded-sm border border-bills-navy/10 bg-white shadow-card">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-bills-navy/10 text-left text-[11px] font-semibold uppercase tracking-wide text-bills-steel">
              <th className="px-4 py-2">#</th>
              <th className="px-4 py-2">Name</th>
              <th className="px-4 py-2">Pos</th>
              <th className="px-4 py-2">Ht</th>
              <th className="px-4 py-2">Wt</th>
              <th className="px-4 py-2">Exp</th>
              <th className="px-4 py-2">College</th>
            </tr>
          </thead>
          <tbody>
            {ordered.map((p) => (
              <tr
                key={p.id}
                className="border-b border-bills-navy/5 last:border-0 hover:bg-bills-silver"
              >
                <td className="px-4 py-2.5 font-display text-base font-bold text-bills-blue tabular">
                  {p.number}
                </td>
                <td className="px-4 py-2.5 font-semibold text-bills-navy">
                  {p.name}
                </td>
                <td className="px-4 py-2.5 text-bills-steel">{p.position}</td>
                <td className="px-4 py-2.5 tabular">{p.height}</td>
                <td className="px-4 py-2.5 tabular">{p.weight}</td>
                <td className="px-4 py-2.5 tabular">{p.experience}</td>
                <td className="px-4 py-2.5 text-bills-steel">{p.college}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
