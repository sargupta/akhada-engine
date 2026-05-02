import { Footer } from "@/components/Footer";
import { NavBar } from "@/components/NavBar";

export default function DebateDetail({ params }: { params: { id: string } }) {
  return (
    <>
      <NavBar />
      <main className="mx-auto max-w-3xl px-6 py-16">
        <div className="smallcaps text-2xs text-[color:var(--ink-muted)] mb-4">
          Debate {params.id.slice(0, 8)}
        </div>
        <h1 className="font-serif text-3xl font-semibold leading-tight">Live cluster view</h1>
        <p className="mt-4 max-w-prose text-[color:var(--ink-muted)]">
          V0.5 stub. The V1 build streams cluster utterances via SSE from{" "}
          <code className="mx-1 font-mono text-sm">
            GET /v1/debates/{params.id}/stream
          </code>{" "}
          and lights up each cluster panel as positions emerge.
        </p>
      </main>
      <Footer debateId={params.id} />
    </>
  );
}
