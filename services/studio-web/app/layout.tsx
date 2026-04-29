import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Akhada — Open Debate Engine",
  description: "500+ AI agents debate any topic, grounded in Indian demographics.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
