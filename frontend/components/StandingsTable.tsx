import type { StandingsEntry } from "@/types";

export default function StandingsTable({
  standings,
}: {
  standings: StandingsEntry[];
}) {
  return (
    <div className="overflow-hidden rounded-sm border border-bills-navy/10 bg-white shadow-card">
      <div className="border-b border-bills-navy/10 px-5 py-3">
        <h2 className="font-display text-sm font-bold uppercase tracking-wide text-bills-red">
          AFC East
        </h2>
      </div>
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-bills-navy/10 text-left text-[11px] font-semibold uppercase tracking-wide text-bills-steel">
            <th className="px-5 py-2">Team</th>
            <th className="px-2 py-2 text-center">W</th>
            <th className="px-2 py-2 text-center">L</th>
            <th className="px-2 py-2 text-center">T</th>
            <th className="px-5 py-2 text-right">Pct</th>
          </tr>
        </thead>
        <tbody>
          {standings.map((s) => (
            <tr
              key={s.team.id}
              className={`border-b border-bills-navy/5 last:border-0 ${
                s.team.id === "buf" ? "bg-bills-blue/5 font-bold" : ""
              }`}
            >
              <td className="px-5 py-2.5">
                <span className="flex items-center gap-2">
                  <span className="flex h-6 w-6 items-center justify-center rounded-sm bg-bills-navy text-[10px] font-bold text-white">
                    {s.team.abbreviation}
                  </span>
                  {s.team.name}
                </span>
              </td>
              <td className="px-2 py-2.5 text-center tabular">{s.wins}</td>
              <td className="px-2 py-2.5 text-center tabular">{s.losses}</td>
              <td className="px-2 py-2.5 text-center tabular">{s.ties}</td>
              <td className="px-5 py-2.5 text-right tabular">
                {s.win_pct.toFixed(3).replace("0.", ".")}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
