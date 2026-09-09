import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ELO | Inteligência Corporativa",
  description: "Experiência web governada do ELO.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
