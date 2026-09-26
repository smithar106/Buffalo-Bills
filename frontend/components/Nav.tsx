"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const LINKS = [
  { href: "/", label: "Game Day" },
  { href: "/schedule", label: "Schedule" },
  { href: "/stats", label: "Stats" },
  { href: "/roster", label: "Roster" },
  { href: "/history", label: "History" },
  { href: "/family-picks", label: "Family Picks" },
];

export default function Nav() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-40 border-b border-bills-navy/10 bg-bills-white/95 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3">
        <Link href="/" className="flex items-center gap-2">
          <span className="flex h-8 w-8 items-center justify-center rounded-sm bg-bills-red font-display text-lg font-bold leading-none text-white">
            B
          </span>
          <span className="font-display text-lg font-bold uppercase tracking-tight text-bills-navy">
            Bills Mafia <span className="text-bills-blue">AI</span>
          </span>
        </Link>

        <nav className="flex items-center gap-1 overflow-x-auto">
          {LINKS.map((link) => {
            const active =
              link.href === "/"
                ? pathname === "/"
                : pathname.startsWith(link.href);
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-semibold transition-colors ${
                  active
                    ? "bg-bills-navy text-white"
                    : "text-bills-navy/70 hover:bg-bills-silver hover:text-bills-navy"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
