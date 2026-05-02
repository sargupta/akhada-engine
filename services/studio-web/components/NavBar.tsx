import Link from "next/link";

import { ThemeToggle } from "./ThemeToggle";

export function NavBar() {
  return (
    <nav
      className="sticky top-0 z-40 backdrop-blur"
      style={{ background: "color-mix(in srgb, var(--bg) 92%, transparent)" }}
    >
      <div
        className="mx-auto flex h-14 max-w-6xl items-center justify-between border-b px-6"
        style={{ borderColor: "var(--hairline)" }}
      >
        <Link href="/" className="flex items-baseline gap-2 transition-opacity hover:opacity-80">
          <span className="font-serif text-xl font-semibold tracking-tight">Akhada</span>
          <span className="smallcaps text-2xs text-[color:var(--ink-muted)]">अखाड़ा</span>
        </Link>
        <div className="flex items-center gap-3">
          <span className="pill">Research mode · v0.5</span>
          <ThemeToggle />
        </div>
      </div>
    </nav>
  );
}
