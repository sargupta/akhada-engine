/**
 * Shorten a UUID-like debate id for display ("0954af7c-…" → "0954af7c").
 */
export function shortId(id: string): string {
  return id.slice(0, 8);
}

/**
 * The orchestrator returns markdown that begins with a `# Debate: <topic>`
 * line; we render the topic separately above the article, so strip it.
 */
export function stripLeadingH1(md: string): string {
  return md.replace(/^# .*\n+/, "");
}
