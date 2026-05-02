"use client";

import { useState } from "react";

import { ConclusiveRemark } from "@/components/ConclusiveRemark";
import { ConfigurePanel } from "@/components/ConfigurePanel";
import { EmptyState } from "@/components/EmptyState";
import { Footer } from "@/components/Footer";
import { HeroHeader } from "@/components/HeroHeader";
import { NavBar } from "@/components/NavBar";
import { PanelComposition } from "@/components/PanelComposition";
import { ResultHeader } from "@/components/ResultHeader";
import { ArticleProse } from "@/components/ArticleProse";
import type { Archetype } from "@/components/ArchetypeCard";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://127.0.0.1:8080";

type DebateResponse = {
  debate_id: string;
  topic: string;
  article: string;
  conclusive_remark: string;
  persona_library_version: string;
  weights_version: string;
  n_personas: number;
  panel_archetypes: Archetype[];
};

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<DebateResponse | null>(null);

  async function runDebate(topic: string, n: number) {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch(`${API_BASE}/v1/debates`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          topic,
          n_agents: n,
          cluster_size: Math.min(20, n),
          rounds: 1,
        }),
      });
      if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
      setResult((await res.json()) as DebateResponse);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <NavBar />
      <main className="relative">
        <HeroHeader />
        <div className="mx-auto grid max-w-6xl grid-cols-1 gap-12 px-6 lg:grid-cols-[360px_1fr]">
          <aside>
            <ConfigurePanel loading={loading} onRun={runDebate} />
          </aside>
          <section className="flex flex-col gap-12">
            {error && (
              <div
                className="rounded-md border px-4 py-3 text-sm"
                style={{
                  borderColor: "var(--error-fg)",
                  background: "var(--error-bg)",
                  color: "var(--error-fg)",
                }}
              >
                <div className="smallcaps text-2xs">Error</div>
                <div className="mt-1 font-mono text-xs">{error}</div>
              </div>
            )}
            {!result && !error && <EmptyState />}
            {result && (
              <>
                <ResultHeader
                  debateId={result.debate_id}
                  topic={result.topic}
                  n={result.n_personas}
                  libVersion={result.persona_library_version}
                  weightsVersion={result.weights_version}
                />
                <PanelComposition
                  archetypes={result.panel_archetypes}
                  total={result.n_personas}
                />
                <ArticleProse markdown={result.article} />
                <ConclusiveRemark
                  remark={result.conclusive_remark}
                  weightsVersion={result.weights_version}
                />
              </>
            )}
          </section>
        </div>
      </main>
      <Footer debateId={result?.debate_id} />
    </>
  );
}
