"use client";

import { useEffect, useState } from "react";

const STAGES = [
  { num: "R0", name: "Framing" },
  { num: "R1", name: "Openings" },
  { num: "R2", name: "Cluster reps" },
  { num: "R3", name: "Final synthesis" },
];

export function ProgressIndicator() {
  const [current, setCurrent] = useState(0);
  useEffect(() => {
    const t = setInterval(() => setCurrent((c) => Math.min(c + 1, STAGES.length - 1)), 600);
    return () => clearInterval(t);
  }, []);
  return (
    <div
      className="flex flex-col gap-2 rounded-md border px-4 py-3"
      style={{ borderColor: "var(--hairline)" }}
    >
      <span className="smallcaps text-2xs text-[color:var(--ink-muted)]">Running…</span>
      <ul className="flex flex-col gap-1">
        {STAGES.map((s, i) => (
          <li key={s.num} className="flex items-center gap-3 text-sm">
            <span
              className={`font-mono text-xs w-8 ${
                i <= current ? "text-[color:var(--saffron-strong)]" : "text-[color:var(--ink-muted)]"
              }`}
            >
              {s.num}
            </span>
            <span className={i <= current ? "" : "text-[color:var(--ink-muted)]"}>{s.name}</span>
            {i < current && (
              <span className="ml-auto text-[color:var(--saffron-strong)]" aria-hidden>
                ✓
              </span>
            )}
            {i === current && (
              <span
                className="ml-auto inline-block h-1.5 w-1.5 animate-pulse rounded-full bg-[color:var(--saffron)]"
                aria-hidden
              />
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
