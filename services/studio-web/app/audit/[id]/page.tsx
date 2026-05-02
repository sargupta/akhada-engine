import { Footer } from "@/components/Footer";
import { NavBar } from "@/components/NavBar";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://127.0.0.1:8080";

type AuditEvent = {
  event_id: string;
  seq: number;
  event_type: string;
  prev_hash: string;
  payload_hash: string;
  payload: Record<string, unknown>;
  ts: number;
};

type AuditResponse = {
  debate_id: string;
  topic: string;
  chain_valid: boolean;
  chain_error: string | null;
  events: AuditEvent[];
};

async function fetchAudit(id: string): Promise<AuditResponse | { error: string }> {
  try {
    const res = await fetch(`${API_BASE}/v1/debates/${id}/audit`, {
      cache: "no-store",
    });
    if (!res.ok) return { error: `API ${res.status}: ${await res.text()}` };
    return (await res.json()) as AuditResponse;
  } catch (err) {
    return { error: err instanceof Error ? err.message : String(err) };
  }
}

function shortHash(h: string): string {
  return `${h.slice(0, 8)}…${h.slice(-4)}`;
}

function formatTs(ts: number): string {
  return new Date(ts * 1000).toISOString().replace("T", " ").slice(0, 19) + " UTC";
}

export default async function AuditPage({ params }: { params: { id: string } }) {
  const data = await fetchAudit(params.id);
  const isError = "error" in data;

  return (
    <>
      <NavBar />
      <main className="mx-auto max-w-4xl px-6 py-12">
        <div className="smallcaps text-2xs text-[color:var(--ink-muted)] mb-3">
          Audit & methodology · debate {params.id.slice(0, 8)}
        </div>
        <h1 className="font-serif text-3xl font-semibold leading-tight max-w-prose">
          {isError ? "Audit unavailable" : data.topic}
        </h1>

        {isError ? (
          <pre
            className="mt-6 rounded-md border px-4 py-3 text-sm font-mono"
            style={{
              borderColor: "var(--error-fg)",
              background: "var(--error-bg)",
              color: "var(--error-fg)",
            }}
          >
            {data.error}
          </pre>
        ) : (
          <>
            <div className="mt-4 flex items-center gap-3">
              <span
                className="pill"
                style={
                  data.chain_valid
                    ? {
                        borderColor: "var(--saffron)",
                        color: "var(--saffron-strong)",
                        background: "rgb(200 147 43 / 0.08)",
                      }
                    : {
                        borderColor: "var(--error-fg)",
                        color: "var(--error-fg)",
                        background: "var(--error-bg)",
                      }
                }
              >
                {data.chain_valid ? "Hash chain · verified" : "Hash chain · TAMPERED"}
              </span>
              <span className="font-mono text-2xs uppercase tracking-wider text-[color:var(--ink-muted)]">
                {data.events.length} events
              </span>
            </div>

            {!data.chain_valid && data.chain_error && (
              <pre className="mt-3 font-mono text-2xs text-[color:var(--error-fg)]">
                {data.chain_error}
              </pre>
            )}

            <p className="mt-6 max-w-prose text-[color:var(--ink-muted)]">
              Each debate emits a sequence of audit events. Each event hash-binds
              to the previous via <code className="font-mono">prev_hash</code>;
              tampering with any payload breaks the chain. V1 commits a daily
              Merkle root over all events to a WORM bucket with retention-lock,
              per plan §20.10.
            </p>

            <ol className="mt-8 flex flex-col gap-0">
              {data.events.map((e, i) => (
                <li
                  key={e.event_id}
                  className="grid grid-cols-[3rem_1fr] gap-4 border-t py-5"
                  style={{ borderColor: "var(--hairline)" }}
                >
                  <span className="font-serif text-3xl font-semibold leading-none text-[color:var(--ink-muted)]">
                    {i + 1}.
                  </span>
                  <div className="min-w-0">
                    <div className="flex flex-wrap items-baseline gap-3">
                      <h2 className="font-serif text-lg font-semibold">
                        {e.event_type.replace(/_/g, " ")}
                      </h2>
                      <span className="font-mono text-2xs uppercase tracking-wider text-[color:var(--ink-muted)]">
                        seq {e.seq} · {formatTs(e.ts)}
                      </span>
                    </div>
                    <div className="mt-1 flex flex-wrap gap-x-3 font-mono text-2xs text-[color:var(--ink-muted)]">
                      <span>prev {shortHash(e.prev_hash)}</span>
                      <span aria-hidden>→</span>
                      <span style={{ color: "var(--saffron-strong)" }}>
                        hash {shortHash(e.payload_hash)}
                      </span>
                    </div>
                    <pre
                      className="mt-3 overflow-x-auto rounded-md border px-3 py-2 font-mono text-2xs leading-relaxed"
                      style={{
                        borderColor: "var(--hairline)",
                        background: "var(--bg-elev)",
                      }}
                    >
                      {JSON.stringify(e.payload, null, 2)}
                    </pre>
                  </div>
                </li>
              ))}
            </ol>
          </>
        )}
      </main>
      <Footer debateId={params.id} />
    </>
  );
}
