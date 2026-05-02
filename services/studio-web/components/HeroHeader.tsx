export function HeroHeader() {
  return (
    <header className="mx-auto max-w-6xl px-6 pt-16 pb-12">
      <div className="smallcaps text-2xs text-[color:var(--ink-muted)] mb-6">
        Akhada · Open Debate Engine · v0.5 research preview
      </div>
      <h1 className="font-serif text-4xl md:text-[3.25rem] font-semibold leading-[1.08] tracking-tight max-w-[28ch]">
        Stress-test public deliberation,{" "}
        <span className="italic text-[color:var(--ink-muted)]">
          before public deliberation stress-tests you.
        </span>
      </h1>
      <p className="mt-6 max-w-2xl text-lg text-[color:var(--ink-muted)]">
        Akhada runs hundreds of biographically-grounded AI personas — drawn from
        Census, NFHS-5, and Lokniti distributions — through a structured debate
        on a policy topic, then synthesises a sourced article and a Bradley-Terry
        quality-weighted conclusive remark.{" "}
        <a
          href="#how"
          className="underline decoration-[color:var(--saffron)] decoration-1 underline-offset-4 transition-all hover:decoration-2"
        >
          How it works ↓
        </a>
      </p>
    </header>
  );
}
