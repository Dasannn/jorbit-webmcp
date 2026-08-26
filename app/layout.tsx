import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Jorbit WebMCP Spike",
  description: "Minimal WebMCP vertical slice for Jorbit",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

