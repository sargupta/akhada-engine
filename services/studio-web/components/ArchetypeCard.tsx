export type Archetype = {
  persona_id: string;
  label: string;
  state: string;
  religion: string;
  age_band: string;
  education: string;
  primary_language: string;
  literacy: string;
  count: number;
};

// Editorial short headline + a representative two-book pull quote keyed on
// the V0.5 fixture personas. V1 will read this from the persona record itself.
const SHORT_HEADLINE: Record<string, string> = {
  "akh-p-fixture-001": "Primary-school teacher, urban Karnataka",
  "akh-p-fixture-002": "Marginal farmer, rural Bihar",
  "akh-p-fixture-003": "Fintech founder, urban Maharashtra",
  "akh-p-fixture-004": "Returnee senior nurse, urban Kerala",
  "akh-p-fixture-005": "Retired Lt. Col., urban Punjab",
};

const TOP_BOOKS_SAMPLE: Record<string, [string, string]> = {
  "akh-p-fixture-001": ["The Argumentative Indian (Sen)", "Samskara (Ananthamurthy)"],
  "akh-p-fixture-002": ["Ramcharitmanas (Tulsidas)", "JP Narayan, Sampoorna Kranti speeches"],
  "akh-p-fixture-003": ["Annihilation of Caste (Ambedkar)", "Why Nations Fail (Acemoglu and Robinson)"],
  "akh-p-fixture-004": ["The God of Small Things (Roy)", "Goat Days (Benyamin)"],
  "akh-p-fixture-005": ["Guru Granth Sahib", "A History of the Sikhs (K. Singh)"],
};

export function ArchetypeCard({ a, toneIndex: _toneIndex }: { a: Archetype; toneIndex: number }) {
  const headline = SHORT_HEADLINE[a.persona_id] ?? a.label;
  const books = TOP_BOOKS_SAMPLE[a.persona_id];

  return (
    <li
      className="group relative flex flex-col gap-3 rounded-lg border bg-[color:var(--bg-elev)] px-5 py-5 transition-all duration-200 ease-out-soft hover:-translate-y-0.5 hover:shadow-elev"
      style={{ borderColor: "var(--hairline)" }}
    >
      <div className="flex items-start gap-4">
        <span
          className="inline-flex h-7 min-w-[2.75rem] items-center justify-center rounded-sm px-2 font-mono text-xs font-semibold"
          style={{ background: "var(--saffron)", color: "#14110C" }}
        >
          ×{a.count}
        </span>
        <div className="min-w-0 flex-1">
          <h3 className="font-serif text-lg font-semibold leading-snug">{headline}</h3>
          <div className="mt-1 flex flex-wrap items-center gap-x-2 font-mono text-2xs uppercase tracking-wider text-[color:var(--ink-muted)]">
            <span>{a.state}</span>
            <span aria-hidden>·</span>
            <span>{a.religion}</span>
            <span aria-hidden>·</span>
            <span>{a.primary_language}</span>
            <span aria-hidden>·</span>
            <span>{a.literacy}</span>
          </div>
        </div>
      </div>

      {books && (
        <blockquote
          className="border-l-2 pl-3 font-serif text-sm italic leading-snug text-[color:var(--ink-muted)]"
          style={{ borderColor: "var(--hairline)" }}
        >
          “{books[0]} · {books[1]}”
        </blockquote>
      )}

      <div className="mt-1 flex items-center justify-between text-2xs">
        <span className="font-mono text-[color:var(--ink-muted)]">{a.persona_id}</span>
        <span className="text-[color:var(--saffron-strong)] opacity-0 transition-opacity duration-150 group-hover:opacity-100">
          View full bio →
        </span>
      </div>
    </li>
  );
}
