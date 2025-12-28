'use client'

import { motion } from 'framer-motion';
import Link from 'next/link';
import { Sparkles, Zap, Globe, ChevronRight } from 'lucide-react';

export default function Home() {
    return (
        <main className="min-h-screen">
            {/* Hero Section */}
            <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
                {/* Animated Background */}
                <div className="absolute inset-0 z-0">
                    {/* Floating orbs */}
                    <motion.div
                        className="absolute top-20 left-1/4 w-72 h-72 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full opacity-20 blur-3xl"
                        animate={{
                            y: [0, -30, 0],
                            scale: [1, 1.1, 1],
                        }}
                        transition={{
                            duration: 8,
                            repeat: Infinity,
                            ease: "easeInOut"
                        }}
                    />
                    <motion.div
                        className="absolute bottom-20 right-1/4 w-96 h-96 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full opacity-20 blur-3xl"
                        animate={{
                            y: [0, 30, 0],
                            scale: [1, 1.2, 1],
                        }}
                        transition={{
                            duration: 10,
                            repeat: Infinity,
                            ease: "easeInOut"
                        }}
                    />
                </div>

                {/* Content */}
                <div className="relative z-10 max-w-6xl mx-auto px-6 text-center">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                    >
                        <motion.div
                            className="inline-flex items-center gap-2 px-4 py-2 mb-6 glass rounded-full text-sm"
                            whileHover={{ scale: 1.05 }}
                        >
                            <Sparkles className="w-4 h-4 text-purple-400" />
                            <span>Scientific SOTA • Free Premium Voices</span>
                        </motion.div>

                        <h1 className="text-6xl md:text-8xl font-bold mb-6 leading-tight">
                            <span className="gradient-text">Defy Gravity</span>
                            <br />
                            <span className="text-white">with Technoaiamaze</span>
                        </h1>

                        <p className="text-xl md:text-2xl text-gray-300 mb-10 max-w-3xl mx-auto">
                            Create engaging anime marketing videos for your brand.
                            <br />
                            <span className="text-purple-400 font-semibold">Company Logo</span> +
                            <span className="text-pink-400 font-semibold"> Your Script</span> →
                            <span className="text-cyan-400 font-semibold"> Anime Video</span>
                        </p>

                        <div className="flex justify-center">
                            <Link href="/generate">
                                <motion.button
                                    className="btn-primary hover-glow px-8 py-4 text-lg flex items-center gap-2"
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                >
                                    Start Creating
                                    <ChevronRight className="w-5 h-5" />
                                </motion.button>
                            </Link>
                        </div>
                    </motion.div>

                    {/* Stats */}
                    <motion.div
                        className="mt-20 grid grid-cols-3 gap-8 max-w-3xl mx-auto"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.3 }}
                    >
                        <div className="glass-dark p-6 rounded-xl">
                            <div className="text-4xl font-bold gradient-text mb-2">90%</div>
                            <div className="text-sm text-gray-400">Premium Voice Quality</div>
                        </div>
                        <div className="glass-dark p-6 rounded-xl">
                            <div className="text-4xl font-bold gradient-text mb-2">100%</div>
                            <div className="text-sm text-gray-400">Free & Open Source</div>
                        </div>
                        <div className="glass-dark p-6 rounded-xl">
                            <div className="text-4xl font-bold gradient-text mb-2">478</div>
                            <div className="text-sm text-gray-400">Facial Keypoints</div>
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-20 px-6">
                <div className="max-w-6xl mx-auto">
                    <motion.h2
                        className="text-4xl md:text-5xl font-bold text-center mb-16"
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                    >
                        Why <span className="gradient-text">Technoaiamaze</span>?
                    </motion.h2>

                    <div className="grid md:grid-cols-3 gap-8">
                        {/* Feature 1 */}
                        <motion.div
                            className="glass-dark p-8 rounded-2xl hover-glow"
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: 0.1 }}
                            whileHover={{ y: -5 }}
                        >
                            <Zap className="w-12 h-12 text-purple-400 mb-4" />
                            <h3 className="text-2xl font-bold mb-3">Scientific SOTA</h3>
                            <p className="text-gray-400">
                                LivePortrait implicit keypoints + 3D volume rendering.
                                Not simple 2D warping - true facial dynamics.
                            </p>
                        </motion.div>

                        {/* Feature 2 */}
                        <motion.div
                            className="glass-dark p-8 rounded-2xl hover-glow"
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: 0.2 }}
                            whileHover={{ y: -5 }}
                        >
                            <Globe className="w-12 h-12 text-pink-400 mb-4" />
                            <h3 className="text-2xl font-bold mb-3">Premium-Quality FREE</h3>
                            <p className="text-gray-400">
                                Edge-TTS neural voices (AriaNeural, GuyNeural) + Coqui XTTS v2.
                                90% quality of paid services, 0% cost.
                            </p>
                        </motion.div>

                        {/* Feature 3 */}
                        <motion.div
                            className="glass-dark p-8 rounded-2xl hover-glow"
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: 0.3 }}
                            whileHover={{ y: -5 }}
                        >
                            <Sparkles className="w-12 h-12 text-cyan-400 mb-4" />
                            <h3 className="text-2xl font-bold mb-3">AI Enhancement</h3>
                            <p className="text-gray-400">
                                GFPGAN v1.4 restores eyes and skin texture.
                                Hallucinate missing details, not just upscale.
                            </p>
                        </motion.div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 px-6">
                <motion.div
                    className="max-w-4xl mx-auto glass-dark p-12 rounded-3xl text-center"
                    initial={{ opacity: 0, scale: 0.95 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true }}
                >
                    <h2 className="text-4xl md:text-5xl font-bold mb-6">
                        Ready to <span className="gradient-text">Defy Gravity</span>?
                    </h2>
                    <p className="text-xl text-gray-300 mb-8">
                        Create hyper-realistic talking head videos in minutes.
                    </p>
                    <Link href="/generate">
                        <motion.button
                            className="btn-primary hover-glow px-10 py-5 text-xl"
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            Launch Studio
                        </motion.button>
                    </Link>
                </motion.div>
            </section>
        </main>
    );
}
