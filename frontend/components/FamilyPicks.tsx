"use client";

import { useEffect, useState } from "react";
import type { FamilyUser, LeaderboardRow } from "@/types";

const BASE = process.env.API_URL || "http://localhost:8000";

async function get<T>(path: string): Promise<T | null> {
  try {
    const r = await fetch(`${BASE}${path}`);
    if (!r.ok) return null;
    return r.json() as Promise<T>;
  } catch {
    return null;
  }
}

export default function FamilyPicks() {
  const [name, setName] = useState("");
  const [user, setUser] = useState<FamilyUser | null>(null);
  const [board, setBoard] = useState<LeaderboardRow[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem("bills-mafia-user");
    if (stored) setUser(JSON.parse(stored));
    get<{ leaderboard: LeaderboardRow[] }>("/api/family/leaderboard").then(
      (r) => r && setBoard(r.leaderboard),
    );
  }, []);

  async function createUser(e: React.FormEvent) {
    e.preventDefault();
    const n = name.trim();
    if (!n) return;
    const r = await fetch(`${BASE}/api/family/users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: n }),
    });
    if (!r.ok) {
      setError("Couldn't create profile — is the API running?");
      return;
    }
    const data = await r.json();
    setUser(data.user);
    localStorage.setItem("bills-mafia-user", JSON.stringify(data.user));
    setError(null);
  }

  return (
    <div className="space-y-6">
      {!user ? (
        <div className="rounded-sm border border-bills-navy/10 bg-white p-6 shadow-card">
          <h2 className="font-display text-lg font-bold uppercase tracking-tight text-bills-navy">
            Join the family
          </h2>
          <p className="mt-1 text-sm text-bills-steel">
            Add your name to start making weekly picks.
          </p>
          <form onSubmit={createUser} className="mt-4 flex gap-2">
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Your name"
              className="flex-1 rounded-sm border border-bills-navy/20 px-3 py-2 text-sm outline-none focus:border-bills-blue"
            />
            <button
              type="submit"
              className="rounded-sm bg-bills-red px-4 py-2 font-display text-sm font-bold uppercase tracking-wide text-white hover:bg-bills-red/90"
            >
              Join
            </button>
          </form>
          {error && <p className="mt-2 text-xs text-bills-red">{error}</p>}
        </div>
      ) : (
        <p className="text-sm text-bills-navy">
          Picking as <span className="font-bold">{user.name}</span>
        </p>
      )}

      <div className="rounded-sm border border-bills-navy/10 bg-white p-6 shadow-card">
        <h2 className="font-display text-lg font-bold uppercase tracking-tight text-bills-navy">
          Family leaderboard
        </h2>
        {board === null ? (
          <p className="mt-3 text-sm text-bills-steel">
            Leaderboard unavailable — is the API running?
          </p>
        ) : board.length === 0 ? (
          <p className="mt-3 text-sm text-bills-steel">
            No picks yet. Predictions will appear here once the family starts picking.
          </p>
        ) : (
          <table className="mt-3 w-full text-sm">
            <thead>
              <tr className="border-b border-bills-navy/10 text-left text-[11px] font-semibold uppercase tracking-wide text-bills-steel">
                <th className="py-2">Name</th>
                <th className="py-2 text-center">Weekly</th>
                <th className="py-2 text-center">Season</th>
                <th className="py-2 text-center">Correct</th>
              </tr>
            </thead>
            <tbody>
              {board.map((row) => (
                <tr key={row.name} className="border-b border-bills-navy/5 last:border-0">
                  <td className="py-2.5 font-semibold text-bills-navy">{row.name}</td>
                  <td className="py-2.5 text-center tabular">{row.weekly_points}</td>
                  <td className="py-2.5 text-center tabular">{row.season_points}</td>
                  <td className="py-2.5 text-center tabular">{row.correct_picks}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
