import { shortId } from "@/lib/format";

export function ResultHeader({
  debateId,
  topic,
  n,
  libVersion,
  weightsVersion,
  backend,
  openingsFailed,
}: {
  debateId: string;
  topic: string;
  n: number;
  libVersion: string;
  weightsVersion: string;
  backend: "offline-stub" | "online-gemini";
  openingsFailed: number;
}) {
  const isOnline = backend === "online-gemini";
  return (
    <header className="flex flex-col gap-3 pb-2">
      <div className="flex flex-wrap items-center gap-3">
        <span className="smallcaps text-2xs text-[color:var(--ink-muted)]">
          Debate {shortId(debateId)}
        </span>
        <span
          className="pill"
          style={
            isOnline
              ? {
                  borderColor: "var(--saffron)",
                  color: "var(--saffron-strong)",
                  background: "rgb(200 147 43 / 0.08)",
                }
              : undefined
          }
          title={
            isOnline
              ? "Real Gemini Flash + Pro inference"
              : "Deterministic V0 stub — set AKHADA_OFFLINE=false + GOOGLE_API_KEY to flip"
          }
        >
          {isOnline ? "Online · Gemini" : "Offline · stub"}
        </span>
        {openingsFailed > 0 && (
          <span className="pill" title={`${openingsFailed} R1 openings fell back to placeholders`}>
            {openingsFailed} fallback
          </span>
        )}
      </div>
      <h2 className="font-serif text-3xl font-semibold leading-tight max-w-prose">{topic}</h2>
      <div className="flex flex-wrap gap-x-3 font-mono text-2xs uppercase tracking-wider text-[color:var(--ink-muted)]">
        <span>{n} personas</span>
        <span aria-hidden>·</span>
        <span>{libVersion}</span>
        <span aria-hidden>·</span>
        <span>{weightsVersion}</span>
      </div>
    </header>
  );
}
