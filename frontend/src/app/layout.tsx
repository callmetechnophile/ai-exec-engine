import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Analytics } from "@vercel/analytics/react";
import { SpeedInsights } from "@vercel/speed-insights/next";
import { FaInstagram, FaLinkedin } from "react-icons/fa";
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
        className="min-h-full flex flex-col bg-fixed bg-cover bg-center bg-no-repeat relative" 
        style={{ backgroundImage: "url('/bg.png')" }}
      >
        <div className="flex-1 min-h-screen bg-black/70 backdrop-blur-lg">
          {children}
        </div>
        
        {/* Social Links */}
        <div className="fixed bottom-6 left-6 flex items-center gap-4 z-50">
          <a href="https://www.instagram.com/mr.devgenius" target="_blank" rel="noopener noreferrer" className="bg-white/10 hover:bg-white/20 p-3 rounded-full backdrop-blur-md border border-white/10 transition-all text-white/80 hover:text-pink-500 hover:shadow-[0_0_15px_rgba(236,72,153,0.5)] hover:scale-110 shadow-lg">
            <FaInstagram className="w-5 h-5" />
          </a>
          <a href="https://www.linkedin.com/in/callmetechnophile/" target="_blank" rel="noopener noreferrer" className="bg-white/10 hover:bg-white/20 p-3 rounded-full backdrop-blur-md border border-white/10 transition-all text-white/80 hover:text-blue-500 hover:shadow-[0_0_15px_rgba(59,130,246,0.5)] hover:scale-110 shadow-lg">
            <FaLinkedin className="w-5 h-5" />
          </a>
        </div>

        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
