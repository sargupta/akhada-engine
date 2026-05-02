"use client";

import { useState } from "react";

import { ProgressIndicator } from "./ProgressIndicator";

const SAMPLE_TOPIC =
  "Should the central government extend MSP guarantees to all 23 crops, including pulses and oilseeds, on a legally backed basis?";

export function ConfigurePanel({
  loading,
  onRun,
}: {
  loading: boolean;
  onRun: (topic: string, n: number) => void;
}) {
  const [topic, setTopic] = useState(SAMPLE_TOPIC);
  const [n, setN] = useState(50);

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onRun(topic, n);
      }}
      className="lg:sticky lg:top-20 flex flex-col gap-5"
    >
      <div
        className="flex items-baseline gap-3 border-b pb-2"
        style={{ borderColor: "var(--hairline)" }}
      >
        <span className="font-serif text-2xl font-semibold leading-none">I.</span>
        <span className="smallcaps text-2xs text-[color:var(--ink-muted)]">Configure debate</span>
      </div>

      <label className="block">
        <span className="mb-2 block text-xs font-medium uppercase tracking-wider text-[color:var(--ink-muted)]">
          Topic
        </span>
        <textarea
          rows={4}
          required
          minLength={4}
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          className="input font-serif text-base leading-relaxed"
        />
      </label>

      <div className="grid grid-cols-2 gap-4">
        <label className="block">
          <span className="mb-2 block text-xs font-medium uppercase tracking-wider text-[color:var(--ink-muted)]">
            Personas
          </span>
          <input
            type="number"
            min={5}
            max={50}
            value={n}
            onChange={(e) => setN(Number(e.target.value) || 50)}
            className="input font-mono text-sm"
          />
        </label>
        <label className="block opacity-60">
          <span className="mb-2 flex items-center gap-1 text-xs font-medium uppercase tracking-wider text-[color:var(--ink-muted)]">
            Rounds <span className="pill">V1</span>
          </span>
          <input type="number" disabled value={1} className="input font-mono text-sm" />
        </label>
      </div>

      <label className="block opacity-60">
        <span className="mb-2 flex items-center gap-1 text-xs font-medium uppercase tracking-wider text-[color:var(--ink-muted)]">
          Language <span className="pill">V1</span>
        </span>
        <select disabled className="input text-sm">
          <option>English (en-IN)</option>
        </select>
      </label>

      {loading ? (
        <ProgressIndicator />
      ) : (
        <div className="flex items-center justify-between pt-2">
          <button type="submit" className="btn-primary">
            <span>Run debate</span>
            <span aria-hidden>→</span>
          </button>
          <button type="button" className="btn-secondary" onClick={() => setTopic(SAMPLE_TOPIC)}>
            Use sample
          </button>
        </div>
      )}

      <p
        className="border-t pt-4 text-2xs leading-relaxed text-[color:var(--ink-muted)]"
        style={{ borderColor: "var(--hairline)" }}
      >
        V0.5 stub: 5 hand-curated archetypes cycled to fill N. Real ADK fan-out, 22-language synthesis,
        and live-stream cluster view land at V1.
      </p>
    </form>
  );
}
