"use client";

import { useState } from "react";
import type { ChatMode, ChatResponse } from "@/types";
import { api } from "@/lib/api";
import SourcesPanel from "./SourcesPanel";

const MODES: { id: ChatMode; label: string; hint: string }[] = [
  { id: "bills_mafia", label: "Bills Mafia", hint: "Energetic Buffalo fan" },
  { id: "analyst", label: "Analyst", hint: "Fact-focused, stats-heavy" },
  { id: "simple", label: "Simple", hint: "No football jargon" },
  { id: "debate", label: "Debate", hint: "Multiple perspectives" },
];

const SUGGESTIONS = [
  "Who do we play next?",
  "How did Josh play last week?",
  "What's the AFC East situation?",
  "Preview the next game.",
  "How have we done against Kansas City?",
];

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: ChatResponse["sources"];
  fallback?: boolean;
}

export default function Chat({ context }: { context?: string }) {
  const [mode, setMode] = useState<ChatMode>("bills_mafia");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  async function send(question: string) {
    const q = question.trim();
    if (!q || loading) return;
    setInput("");
    setMessages((m) => [...m, { role: "user", content: q }]);
    setLoading(true);
    try {
      const res = await api.chat(q, mode, context);
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          content: res.answer,
          sources: res.sources,
          fallback: res.fallback,
        },
      ]);
    } catch {
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          content: "I couldn't verify that from the available Bills data.",
          fallback: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="w-full">
      <div className="mb-3 flex flex-wrap gap-1.5">
        {MODES.map((m) => (
          <button
            key={m.id}
            onClick={() => setMode(m.id)}
            className={`rounded-sm px-3 py-1 text-xs font-bold uppercase tracking-wide transition-colors ${
              mode === m.id
                ? "bg-bills-red text-white"
                : "bg-white/10 text-white/80 hover:bg-white/20"
            }`}
            title={m.hint}
          >
            {m.label}
          </button>
        ))}
      </div>

      {messages.length > 0 && (
        <div className="mb-4 space-y-3">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`rounded-sm p-4 ${
                msg.role === "user"
                  ? "bg-white/10 text-white"
                  : "bg-white text-bills-navy"
              }`}
            >
              <p className="whitespace-pre-wrap text-sm leading-relaxed">
                {msg.content}
              </p>
              {msg.role === "assistant" && msg.sources && msg.sources.length > 0 && (
                <SourcesPanel sources={msg.sources} />
              )}
            </div>
          ))}
          {loading && (
            <div className="rounded-sm bg-white/10 p-4 text-sm text-white/70">
              Checking the Bills data…
            </div>
          )}
        </div>
      )}

      <form
        onSubmit={(e) => {
          e.preventDefault();
          send(input);
        }}
        className="flex items-center gap-2"
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask anything about the Bills…"
          className="flex-1 rounded-sm border border-white/20 bg-white/10 px-4 py-3 text-sm text-white placeholder:text-white/50 outline-none focus:border-white/50 focus:bg-white/15"
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded-sm bg-bills-red px-4 py-3 font-display text-sm font-bold uppercase tracking-wide text-white transition-colors hover:bg-bills-red/90 disabled:opacity-50"
        >
          Ask
        </button>
      </form>

      {messages.length === 0 && (
        <div className="mt-3 flex flex-wrap gap-1.5">
          {SUGGESTIONS.map((s) => (
            <button
              key={s}
              onClick={() => send(s)}
              className="rounded-sm border border-white/20 px-3 py-1.5 text-xs text-white/80 transition-colors hover:bg-white/10"
            >
              {s}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
