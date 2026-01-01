import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
    subsets: ["latin"],
    weight: ['300', '400', '500', '600', '700', '800', '900'],
    display: 'swap',
});

export const metadata: Metadata = {
    title: "Technoaiamaze - WhatsApp Marketing Videos in 10 Languages | India's #1 AI Video Creator",
    description: "Create WhatsApp Status videos in Hindi, English & 8+ languages. Perfect for Indian businesses. Restaurant templates, Real Estate videos, Course promos. ₹2,999/month. Start FREE!",
    keywords: "whatsapp video maker, whatsapp status video creator, hindi video creator, multi language video, indian business marketing, restaurant video, real estate video, ai video generator india, marketing video maker, video creator for small business",
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
