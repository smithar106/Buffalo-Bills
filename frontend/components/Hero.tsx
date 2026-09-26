import Chat from "./Chat";

export default function Hero() {
  return (
    <section className="stadium-glow text-white">
      <div className="mx-auto max-w-6xl px-4 py-14 sm:py-20">
        <div className="mx-auto max-w-2xl">
          <p className="field-band text-center font-display text-xs font-semibold uppercase tracking-[0.35em] text-white/70">
            Unofficial fan project
          </p>
          <h1 className="mt-3 text-center font-display text-5xl font-bold uppercase leading-none tracking-tight sm:text-7xl">
            Bills Mafia <span className="text-bills-red">AI</span>
          </h1>
          <p className="mt-4 text-center text-lg text-white/80">
            Your family&apos;s Buffalo football intelligence agent.
          </p>

          <div className="mt-8">
            <p className="mb-2 font-display text-sm font-bold uppercase tracking-wide text-bills-red">
              Ask the Mafia
            </p>
            <Chat />
          </div>
        </div>
      </div>
    </section>
  );
}
