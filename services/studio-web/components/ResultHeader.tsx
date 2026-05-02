import { shortId } from "@/lib/format";

export function ResultHeader({
  debateId,
  topic,
  n,
  libVersion,
  weightsVersion,
}: {
  debateId: string;
  topic: string;
  n: number;
  libVersion: string;
  weightsVersion: string;
}) {
  return (
    <header className="flex flex-col gap-3 pb-2">
      <div className="smallcaps text-2xs text-[color:var(--ink-muted)]">
        Debate {shortId(debateId)}
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
