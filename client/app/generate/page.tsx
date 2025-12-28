'use client'

import { useState } from 'react';
import Studio from '@/components/studio/Studio';
import { motion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';

export default function GeneratePage() {
    return (
        <main className="min-h-screen p-6">
            {/* Header */}
            <motion.div
                className="max-w-7xl mx-auto mb-6"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <Link href="/">
                    <button className="glass px-4 py-2 rounded-lg flex items-center gap-2 hover-glow">
                        <ArrowLeft className="w-4 h-4" />
                        Back to Home
                    </button>
                </Link>
            </motion.div>

            {/* Studio Component */}
            <motion.div
                className="max-w-7xl mx-auto"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
            >
                <Studio />
            </motion.div>
        </main>
    );
}
