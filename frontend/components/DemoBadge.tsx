export default function DemoBadge({ demo }: { demo?: boolean }) {
  if (!demo) return null;
  return (
    <span className="inline-flex items-center gap-1 rounded-sm border border-bills-red/30 bg-bills-red/10 px-2 py-0.5 text-[11px] font-bold uppercase tracking-wide text-bills-red">
      Demo data
    </span>
  );
}
