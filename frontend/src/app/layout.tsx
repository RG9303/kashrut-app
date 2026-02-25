import { Outfit, Inter } from "next/font/google";
import "./globals.css";

const outfit = Outfit({
  variable: "--font-outfit",
  subsets: ["latin"],
});

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export const metadata = {
  title: "KosherScan API Client",
  description: "Digital Mashgiach - AI powered Kashrut scanner",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body
        className={`${outfit.variable} ${inter.variable} antialiased bg-slate-900 text-slate-50 min-h-screen relative overflow-x-hidden`}
        style={{
          background: 'radial-gradient(circle at 50% 0%, #1e293b 0%, #0f172a 100%)',
          fontFamily: 'var(--font-outfit), sans-serif',
        }}
      >
        {children}
      </body>
    </html>
  );
}
