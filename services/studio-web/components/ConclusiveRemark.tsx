export function ConclusiveRemark({
  remark,
  weightsVersion,
}: {
  remark: string;
  weightsVersion: string;
}) {
  return (
    <section className="flex flex-col gap-6">
      <div
        className="flex items-baseline gap-3 border-b pb-2"
        style={{ borderColor: "var(--hairline)" }}
      >
        <span className="font-serif text-2xl font-semibold leading-none">IV.</span>
        <span className="smallcaps text-2xs text-[color:var(--ink-muted)]">Conclusive remark</span>
      </div>
      <div
        className="relative overflow-hidden rounded-lg border bg-[color:var(--bg-elev)] px-6 py-6"
        style={{ borderColor: "var(--hairline)" }}
      >
        <span
          aria-hidden
          className="absolute left-0 top-0 h-full w-1"
          style={{ background: "var(--saffron)" }}
        />
        <p className="pl-4 font-serif text-lg leading-relaxed">{remark}</p>
        <div className="mt-4 pl-4 font-mono text-2xs uppercase tracking-wider text-[color:var(--ink-muted)]">
          {weightsVersion} · top-5 claims by Bradley-Terry quality score
        </div>
      </div>
    </section>
  );
}
