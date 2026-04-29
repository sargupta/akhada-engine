"use client";

import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://127.0.0.1:8080";

type DebateResponse = {
  debate_id: string;
  topic: string;
  article: string;
  conclusive_remark: string;
  persona_library_version: string;
  weights_version: string;
  n_personas: number;
};

export default function Home() {
  const [topic, setTopic] = useState("MSP for all crops");
  const [nAgents, setNAgents] = useState(50);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DebateResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function runDebate(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch(`${API_BASE}/v1/debates`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          topic,
          n_agents: nAgents,
          cluster_size: Math.min(20, nAgents),
          rounds: 1,
        }),
      });
      if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
      setResult(await res.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <h1>Akhada — Studio</h1>
      <p className="muted">
        V0 scaffold. Hand-curated stub personas, naive flat debate. Real ADK
        orchestration + 500-agent hierarchical topology lands V1.
      </p>

      <form onSubmit={runDebate}>
        <label>
          Topic
          <textarea
            rows={3}
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            required
            minLength={4}
          />
        </label>
        <label>
          Number of agents (V0 stub: 5-50)
          <input
            type="number"
            min={5}
            max={50}
            value={nAgents}
            onChange={(e) => setNAgents(Number(e.target.value))}
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? "Running…" : "Run debate"}
        </button>
      </form>

      {error && (
        <>
          <h2>Error</h2>
          <pre>{error}</pre>
        </>
      )}

      {result && (
        <>
          <h2>Article</h2>
          <pre>{result.article}</pre>
          <h2>Conclusive remark</h2>
          <pre>{result.conclusive_remark}</pre>
          <p className="muted">
            debate_id: {result.debate_id} · personas: {result.n_personas} ·
            library: {result.persona_library_version} · weights:{" "}
            {result.weights_version}
          </p>
        </>
      )}
    </main>
  );
}
