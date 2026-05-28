import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Analytics } from "@vercel/analytics/react";
import { SpeedInsights } from "@vercel/speed-insights/next";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "SUNDAY",
  description: "Autonomous AI-powered engineering research and component extraction.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased dark`}
    >
      <body 
        className="min-h-full flex flex-col bg-fixed bg-cover bg-center bg-no-repeat" 
        style={{ backgroundImage: "url('/bg.png')" }}
      >
        <div className="flex-1 min-h-screen bg-black/70 backdrop-blur-lg">
          {children}
        </div>
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
