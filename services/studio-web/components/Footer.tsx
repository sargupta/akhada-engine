export function Footer({ debateId }: { debateId?: string }) {
  return (
    <footer
      className="mt-24 border-t py-8"
      style={{ borderColor: "var(--hairline)" }}
    >
      <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-3 px-6">
        <div className="font-mono text-2xs uppercase tracking-wider text-[color:var(--ink-muted)]">
          Akhada · open debate engine · AGPL-3.0 · v0.5
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
