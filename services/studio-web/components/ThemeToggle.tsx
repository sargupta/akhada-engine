"use client";

import { Moon, Sun } from "lucide-react";

import { useTheme } from "./ThemeProvider";

export function ThemeToggle() {
  const { theme, toggle } = useTheme();
  return (
    <button
      onClick={toggle}
      type="button"
      aria-label={`switch to ${theme === "light" ? "dark" : "light"} mode`}
      className="inline-flex h-8 w-8 items-center justify-center rounded-md text-[color:var(--ink-muted)] transition-colors duration-150 hover:bg-[color:var(--hairline)]/40 hover:text-[color:var(--ink)]"
    >
      {theme === "light" ? <Moon size={16} strokeWidth={1.6} /> : <Sun size={16} strokeWidth={1.6} />}
    </button>
  );
}
