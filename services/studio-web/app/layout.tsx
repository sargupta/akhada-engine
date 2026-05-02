import type { Metadata } from "next";

import { ThemeProvider } from "@/components/ThemeProvider";

import "./globals.css";

export const metadata: Metadata = {
  title: "Akhada · Open Debate Engine",
  description:
    "Stress-test public deliberation across 500+ AI personas grounded in Indian Census, NFHS-5 and Lokniti distributions.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="antialiased">
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
