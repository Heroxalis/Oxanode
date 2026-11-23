
import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "Oxanode",
    template: "%s | Oxanode",
  },
  description:
    "A self-hosted application and infrastructure management platform by Heroxalis.",
  applicationName: "Oxanode",
  authors: [{ name: "Heroxalis" }],
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: [
    { media: "(prefers-color-scheme: dark)", color: "#111018" },
    { media: "(prefers-color-scheme: light)", color: "#f7f6fb" },
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>{children}</body>
    </html>
  );
}
