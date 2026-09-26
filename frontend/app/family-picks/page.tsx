import FamilyPicks from "@/components/FamilyPicks";

export const metadata = { title: "Family Picks — Bills Mafia AI" };

export default function FamilyPicksPage() {
  return (
    <div className="mx-auto max-w-6xl px-4 py-10">
      <h1 className="mb-6 font-display text-3xl font-bold uppercase tracking-tight text-bills-navy">
        Family picks
      </h1>
      <FamilyPicks />
    </div>
  );
}
