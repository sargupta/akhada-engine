import type { Config } from "tailwindcss";
import typography from "@tailwindcss/typography";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        // Warm institutional palette — never pure white, never pure black.
        cream: {
          50: "#FCFAF5",
          100: "#F8F4ED",
          200: "#F2EBDD",
          300: "#E7DEC8",
        },
        ink: {
          50:  "#5C5750",
          100: "#3D3933",
          200: "#2A2722",
          300: "#1A1814",
          900: "#0E1014",
        },
        saffron: {
          400: "#D9A744",
          500: "#C8932B",
          600: "#A77918",
        },
        hairline: {
          light: "#E0D7C2",
          dark: "#262421",
        },
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        serif: ['"Source Serif 4"', "ui-serif", "Georgia", "serif"],
        mono: ['"IBM Plex Mono"', "ui-monospace", "monospace"],
      },
      fontSize: {
        // 12 / 14 / 16 / 18 / 20 / 24 / 32 / 48 — disciplined scale.
        "2xs": ["0.6875rem", { lineHeight: "1rem", letterSpacing: "0.04em" }],
        xs:   ["0.75rem",   { lineHeight: "1.1rem", letterSpacing: "0.03em" }],
        sm:   ["0.875rem",  { lineHeight: "1.35rem" }],
        base: ["1rem",      { lineHeight: "1.6rem" }],
        lg:   ["1.125rem",  { lineHeight: "1.75rem" }],
        xl:   ["1.25rem",   { lineHeight: "1.85rem" }],
        "2xl":["1.5rem",    { lineHeight: "2.1rem" }],
        "3xl":["2rem",      { lineHeight: "2.4rem" }],
        "4xl":["3rem",      { lineHeight: "3.4rem", letterSpacing: "-0.02em" }],
      },
      maxWidth: {
        prose: "65ch",
      },
      boxShadow: {
        card: "0 1px 0 rgb(0 0 0 / 0.04), 0 1px 3px rgb(0 0 0 / 0.06)",
        elev: "0 1px 0 rgb(0 0 0 / 0.06), 0 8px 22px rgb(0 0 0 / 0.07)",
      },
      transitionTimingFunction: {
        "out-soft": "cubic-bezier(0.16, 1, 0.3, 1)",
      },
    },
  },
  plugins: [typography],
};

export default config;
