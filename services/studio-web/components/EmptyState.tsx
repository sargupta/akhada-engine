const STAGES = [
  {
    roman: "I.",
    label: "R0 · Framing",
    body: "A framer agent restates the topic, surfaces its sub-questions, and retrieves an evidence pack via Vertex RAG.",
  },
  {
    roman: "II.",
    label: "R1 · Openings (parallel)",
    body: "500 personas — drawn by k-DPP from a 5,000-persona library — open in parallel with 80–150 word, persona-conditioned statements.",
  },
  {
    roman: "III.",
    label: "R2 · Cluster + super-cluster synthesis",
    body: "Twenty-five clusters of twenty, then five super-clusters, debate sparsely (S²-MAD). Each cluster's verbatim minority dissent is preserved by design.",
  },
  {
    roman: "IV.",
    label: "R3 · Conclusive remark",
    body: "Bradley-Terry quality-weighted top-K claims, calibrated against a held-out human-graded debate set. Cites the winning argument, not the winning side.",
  },
];

export function EmptyState() {
  return (
    <section
      id="how"
      className="flex flex-col gap-6 rounded-lg border px-6 py-10 md:px-10 md:py-12"
      style={{ borderColor: "var(--hairline)", background: "var(--bg-elev)" }}
    >
      <div className="smallcaps text-2xs text-[color:var(--ink-muted)]">What you will see</div>
      <h2 className="font-serif text-2xl font-semibold leading-tight max-w-prose">
        Four pipeline stages. One audit-traceable output.
      </h2>
      <ol className="mt-2 flex flex-col gap-0">
        {STAGES.map((s) => (
          <li
            key={s.roman}
            className="grid grid-cols-[3.5rem_1fr] gap-4 border-t py-5"
            style={{ borderColor: "var(--hairline)" }}
          >
            <span className="font-serif text-3xl font-semibold leading-none text-[color:var(--ink-muted)]">
              {s.roman}
            </span>
            <div>
              <div className="text-sm font-medium uppercase tracking-wider">{s.label}</div>
              <p className="mt-1.5 max-w-prose text-base leading-relaxed text-[color:var(--ink-muted)]">
                {s.body}
              </p>
            </div>
          </li>
        ))}
      </ol>
    </section>
  );
}
