import { ArchetypeCard, type Archetype } from "./ArchetypeCard";

// Five warm tints walking from sand to bronze — same family, no rainbows.
const TONES_LIGHT = ["#E7DEC8", "#D8C9A6", "#C8B488", "#B6A176", "#9E8859"];
const TONES_DARK  = ["#2A2620", "#352F25", "#403828", "#4D4232", "#5C5039"];

export function PanelComposition({
  archetypes,
  total,
}: {
  archetypes: Archetype[];
  total: number;
}) {
  return (
    <section className="flex flex-col gap-6">
      <div
        className="flex items-baseline gap-3 border-b pb-2"
        style={{ borderColor: "var(--hairline)" }}
      >
        <span className="font-serif text-2xl font-semibold leading-none">II.</span>
        <span className="smallcaps text-2xs text-[color:var(--ink-muted)]">
          Panel composition · {total} personas · {archetypes.length} archetypes
        </span>
      </div>

      <StackedBar archetypes={archetypes} total={total} />

      <ul className="grid grid-cols-1 gap-4 md:grid-cols-2">
        {archetypes.map((a, i) => (
          <ArchetypeCard key={a.persona_id} a={a} toneIndex={i} />
        ))}
      </ul>
    </section>
  );
}

function StackedBar({ archetypes, total }: { archetypes: Archetype[]; total: number }) {
  return (
    <div className="flex flex-col gap-2">
      <div
        className="flex h-3 w-full overflow-hidden rounded-sm border"
        style={{ borderColor: "var(--hairline)" }}
        role="img"
        aria-label="Panel composition by archetype"
      >
        {archetypes.map((a, i) => {
          const pct = (a.count / total) * 100;
          return (
            <div
              key={a.persona_id}
              title={a.label}
              aria-label={`${a.label}: ${a.count} of ${total}`}
              className="relative transition-all duration-200 ease-out-soft"
              style={{
                width: `${pct}%`,
                backgroundColor: `var(--bar-${i}, ${TONES_LIGHT[i % TONES_LIGHT.length]})`,
              }}
            >
              <span
                className="absolute inset-0 hidden dark:block"
                style={{ backgroundColor: TONES_DARK[i % TONES_DARK.length] }}
              />
            </div>
          );
        })}
      </div>
      <div className="flex justify-between text-2xs">
        <span className="smallcaps text-[color:var(--ink-muted)]">N = {total}</span>
        <span className="smallcaps text-[color:var(--ink-muted)]">DPP-stratified · V0.5 stub</span>
      </div>
    </div>
  );
}
