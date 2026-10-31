import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ClientProviders } from "@/components/providers";
import { Sidebar } from "@/components/layout/sidebar";
import { Navbar } from "@/components/layout/navbar";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "Linux for DevOps — From Zero to Production",
  description: "Interactive Linux learning platform for DevOps engineers.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full">
      <body className={`h-full ${inter.className} antialiased`}>
        <ClientProviders>
          <div className="flex flex-col h-full">
            <Navbar />
            <div className="flex-1 flex overflow-hidden">
              <Sidebar />
              <main className="flex-1 overflow-y-auto bg-background">{children}</main>
            </div>
          </div>
        </ClientProviders>
      </body>
    </html>
  );
}
