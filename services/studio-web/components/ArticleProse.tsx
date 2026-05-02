"use client";

import ReactMarkdown from "react-markdown";

import { stripLeadingH1 } from "@/lib/format";

export function ArticleProse({ markdown }: { markdown: string }) {
  return (
    <section className="flex flex-col gap-6">
      <div
        className="flex items-baseline gap-3 border-b pb-2"
        style={{ borderColor: "var(--hairline)" }}
      >
        <span className="font-serif text-2xl font-semibold leading-none">III.</span>
        <span className="smallcaps text-2xs text-[color:var(--ink-muted)]">Article</span>
      </div>
      <article className="prose-akhada max-w-prose">
        <ReactMarkdown>{stripLeadingH1(markdown)}</ReactMarkdown>
      </article>
    </section>
  );
}
