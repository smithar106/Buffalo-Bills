"use client";

import { useState } from "react";
import type { Source } from "@/types";
import { timeAgo } from "@/lib/format";

export default function SourcesPanel({ sources }: { sources: Source[] }) {
  const [open, setOpen] = useState<string | null>(null);

  if (!sources.length) return null;

  return (
    <div className="mt-3 border-t border-bills-navy/10 pt-3">
      <p className="mb-2 text-[11px] font-bold uppercase tracking-wide text-bills-steel">
        Sources
      </p>
      <div className="flex flex-wrap gap-1.5">
        {sources.map((s, i) => (
          <button
            key={i}
            onClick={() => setOpen(open === s.label ? null : s.label)}
            className="rounded-sm bg-bills-silver px-2.5 py-1 text-xs font-semibold text-bills-navy transition-colors hover:bg-bills-blue/10"
          >
            {s.label}
          </button>
        ))}
      </div>

      {sources.map((s, i) =>
        open === s.label ? (
          <div
            key={`detail-${i}`}
            className="mt-2 rounded-sm border border-bills-navy/10 bg-bills-silver/60 p-3 text-xs text-bills-navy"
          >
            <div className="flex items-center justify-between gap-2">
              <span className="font-bold">{s.label}</span>
              <span className="text-bills-steel">
                retrieved {timeAgo(s.retrieved_at)}
              </span>
            </div>
            <p className="mt-1 text-bills-steel">via {s.tool}</p>
            {s.evidence && (
              <p className="mt-1 font-mono text-[11px] leading-relaxed text-bills-navy/80">
                {s.evidence}
              </p>
            )}
          </div>
        ) : null,
      )}
    </div>
  );
}
