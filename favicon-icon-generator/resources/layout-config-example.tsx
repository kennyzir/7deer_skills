/**
 * Next.js Layout Configuration Example
 * 
 * This shows how to properly configure icons in Next.js App Router
 */

import type { Metadata } from "next";

export async function generateMetadata(): Promise<Metadata> {
  return {
    title: "Your App Name",
    description: "Your app description",
    
    // Icon configuration
    icons: {
      icon: [
        { url: "/icon.svg", type: "image/svg+xml" },
        { url: "/favicon.svg", type: "image/svg+xml" },
      ],
      shortcut: "/icon.svg",
      apple: [
        { url: "/apple-icon.png", sizes: "180x180", type: "image/png" },
      ],
      other: [
        {
          rel: "mask-icon",
          url: "/icon.svg",
        },
      ],
    },
    
    // PWA manifest
    manifest: "/manifest.json",
    
    // Other metadata...
  };
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        {/* Icon links for maximum compatibility */}
        <link rel="icon" href="/icon.svg" type="image/svg+xml" />
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
        <link rel="apple-touch-icon" href="/apple-icon.png" sizes="180x180" />
      </head>
      <body>{children}</body>
    </html>
  );
}
