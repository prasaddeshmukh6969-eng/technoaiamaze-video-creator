import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
    subsets: ["latin"],
    weight: ['300', '400', '500', '600', '700', '800', '900'],
    display: 'swap',
});

export const metadata: Metadata = {
    title: "Technoaiamaze - Anime Marketing Video Creator",
    description: "Create engaging anime marketing videos for your brand. Upload your company logo, enter your script, and generate professional anime videos with AI-powered animation and voice synthesis.",
    keywords: "anime video, marketing video, company branding, anime character, text-to-speech, AI animation, business video",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className={inter.className}>
                {children}
            </body>
        </html>
    );
}
