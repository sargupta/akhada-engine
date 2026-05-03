export function Footer({ debateId }: { debateId?: string }) {
  return (
    <footer
      className="mt-24 border-t py-8"
      style={{ borderColor: "var(--hairline)" }}
    >
      <div className="mx-auto flex max-w-6xl flex-col gap-2 px-6 md:flex-row md:items-center md:justify-between">
        <div className="flex flex-col gap-1">
          <div className="font-mono text-2xs uppercase tracking-wider text-[color:var(--ink-muted)]">
            Akhada · open debate engine · AGPL-3.0 · v0.10
          </div>
          <div className="text-2xs text-[color:var(--ink-muted)]">
            A{" "}
            <a
              href="https://github.com/sargupta/akhada-engine"
              className="font-medium tracking-wide text-[color:var(--ink)] underline decoration-[color:var(--saffron)] decoration-1 underline-offset-4 transition-all hover:decoration-2"
            >
              SARGVISION Intelligence
            </a>{" "}
            product.
          </div>
        </div>
        {debateId ? (
          <a
            href={`/audit/${debateId}`}
            className="text-2xs uppercase tracking-wider text-[color:var(--saffron-strong)] hover:underline"
          >
            Audit & methodology →
          </a>
        ) : (
          <span className="font-mono text-2xs uppercase tracking-wider text-[color:var(--ink-muted)]">
            stress-test before stress-tested
          </span>
        )}
      </div>
    </footer>
  );
}
