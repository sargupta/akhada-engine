// V0 stub. V1 wires SSE live cluster view.
export default function DebateDetail({ params }: { params: { id: string } }) {
  return (
    <main>
      <h1>Debate {params.id}</h1>
      <p className="muted">
        V0 stub. V1 streams live cluster utterances via SSE from
        <code> GET /v1/debates/{params.id}/stream</code>.
      </p>
    </main>
  );
}
