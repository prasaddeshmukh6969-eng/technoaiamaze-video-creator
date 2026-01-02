'use client'

import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import { Sparkles, Zap, Globe, ChevronRight, Check, Lock, MessageCircle, Languages, LayoutTemplate, Mic, Grid3x3, Image, Calendar, FileSpreadsheet, X } from 'lucide-react';
import { trackPageView, voteFeature } from '@/lib/analytics';

export default function Home() {
    const [showVoteModal, setShowVoteModal] = useState(false);
    const [votingFor, setVotingFor] = useState<string | null>(null);
    const [voteMessage, setVoteMessage] = useState('');

    // Email signup state
    const [email, setEmail] = useState('');
    const [emailLoading, setEmailLoading] = useState(false);
    const [emailMessage, setEmailMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

    // Track page view on mount
    useEffect(() => {
        trackPageView('/');
    }, []);

    const features = [
        {
            id: 1,
            icon: MessageCircle,
            iconColor: 'text-green-400',
            name: 'WhatsApp Optimized',
            description: 'Perfect 9:16 vertical videos for WhatsApp Status. Mobile-first design for Indian businesses.',
            unlocked: true,
            badge: 'LIVE NOW'
        },
        {
            id: 2,
            icon: Languages,
            iconColor: 'text-blue-400',
            name: 'Multi-Language Videos',
            description: 'One script → 10 languages automatically. Hindi, English, Tamil, Telugu, and more.',
            unlocked: true,
            badge: 'LIVE NOW'
        },
        {
            id: 3,
            icon: LayoutTemplate,
            iconColor: 'text-purple-400',
            name: 'Industry Templates',
            description: 'Pre-made templates for Restaurants, Real Estate, Education. Logo → Video in 2 minutes.',
            unlocked: true,
            badge: 'LIVE NOW'
        },
        {
            id: 4,
            icon: Mic,
            iconColor: 'text-pink-400',
            name: 'Voice Cloning',
            description: 'Upload 10 seconds of YOUR voice. All videos use your personal voice, not generic AI.',
            unlocked: false,
            badge: 'COMING SOON'
        },
        {
            id: 5,
            icon: Grid3x3,
            iconColor: 'text-cyan-400',
            name: 'Auto Social Resize',
            description: '1 video → 5 formats. YouTube, Instagram, TikTok, LinkedIn - all sizes automatically.',
            unlocked: false,
            badge: 'COMING SOON'
        },
        {
            id: 6,
            icon: FileSpreadsheet,
            iconColor: 'text-orange-400',
            name: 'Bulk CSV Generation',
            description: 'Upload spreadsheet with 100 names. Generate 100 personalized videos automatically.',
            unlocked: false,
            badge: 'COMING SOON'
        },
        {
            id: 7,
            icon: Image,
            iconColor: 'text-yellow-400',
            name: 'Custom Backgrounds',
            description: 'Replace background with your office, product, or brand image. Professional look instantly.',
            unlocked: false,
            badge: 'COMING SOON'
        },
        {
            id: 8,
            icon: Calendar,
            iconColor: 'text-red-400',
            name: 'Scheduled Posting',
            description: 'Generate + auto-post to Instagram, Facebook, LinkedIn. Calendar view for content planning.',
            unlocked: false,
            badge: 'COMING SOON'
        }
    ];

    const handleVote = async (featureId: string) => {
        setVotingFor(featureId);
        const result = await voteFeature(featureId);
        setVoteMessage(result.message);
        setVotingFor(null);

        // Close modal after 2 seconds
        setTimeout(() => {
            setShowVoteModal(false);
            setVoteMessage('');
        }, 2000);
    };

    const handleEmailSignup = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!email) return;

        setEmailLoading(true);
        setEmailMessage(null);

        const { signupEmail } = await import('@/lib/analytics');
        const result = await signupEmail(email, 'landing_page_hero');

        setEmailLoading(false);

        if (result.success) {
            setEmailMessage({ type: 'success', text: result.message });
            setEmail('');
            setTimeout(() => setEmailMessage(null), 5000);
        } else {
            setEmailMessage({ type: 'error', text: result.message });
        }
    };

    const lockedFeatures = features.filter(f => !f.unlocked);

    return (
        <main className="min-h-screen">
            {/* Hero Section */}
            <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
                {/* Animated Background */}
                <div className="absolute inset-0 z-0">
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
                        className="absolute bottom-20 right-1/4 w-96 h-96 bg-gradient-to-r from-green-500 to-cyan-500 rounded-full opacity-20 blur-3xl"
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
                            <MessageCircle className="w-4 h-4 text-green-400" />
                            <span>Made for WhatsApp Marketing • India-First</span>
                        </motion.div>

                        <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
                            <span className="gradient-text">Marketing Videos</span>
                            <br />
                            <span className="text-white">in 10 Languages</span>
                            <br />
                            <span className="text-gray-300 text-3xl md:text-5xl">for WhatsApp Status</span>
                        </h1>

                        <p className="text-xl md:text-2xl text-gray-300 mb-10 max-w-3xl mx-auto">
                            The ONLY video creator built for Indian businesses.
                            <br />
                            <span className="text-green-400 font-semibold">WhatsApp-optimized</span> •
                            <span className="text-blue-400 font-semibold"> Multi-language</span> •
                            <span className="text-purple-400 font-semibold"> Pre-made Templates</span>
                        </p>

                        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
                            <Link href="/generate">
                                <motion.button
                                    className="btn-primary hover-glow cta-pulse px-8 py-4 text-lg flex items-center gap-2"
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                >
                                    Start Free Trial
                                    <ChevronRight className="w-5 h-5" />
                                </motion.button>
                            </Link>
                            <motion.button
                                className="glass px-8 py-4 text-lg flex items-center gap-2 hover-glow"
                                whileHover={{ scale: 1.05 }}
                            >
                                <Sparkles className="w-5 h-5" />
                                See Demo Video
                            </motion.button>
                        </div>

                        {/* Email Signup Section */}
                        <motion.div
                            className="max-w-md mx-auto mb-8"
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.6 }}
                        >
                            <p className="text-sm text-gray-400 mb-3 text-center">
                                Get early access and exclusive WhatsApp marketing tips 🚀
                            </p>
                            <form onSubmit={handleEmailSignup} className="flex gap-2">
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="Enter your email"
                                    className="flex-1 px-4 py-3 rounded-lg bg-black/50 border border-gray-700 focus:border-cyan-400 focus:outline-none text-white placeholder-gray-500"
                                    required
                                    disabled={emailLoading}
                                />
                                <button
                                    type="submit"
                                    disabled={emailLoading}
                                    className="btn-primary px-6 py-3 whitespace-nowrap disabled:opacity-50"
                                >
                                    {emailLoading ? 'Joining...' : 'Join Waitlist'}
                                </button>
                            </form>
                            {emailMessage && (
                                <motion.div
                                    className={`mt-3 text-sm text-center ${emailMessage.type === 'success' ? 'text-green-400' : 'text-red-400'
                                        }`}
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                >
                                    {emailMessage.text}
                                </motion.div>
                            )}
                        </motion.div>

                        {/* Social Proof */}
                        <div className="flex items-center justify-center gap-6 text-sm text-gray-400">
                            <div className="flex items-center gap-2">
                                <Check className="w-4 h-4 text-green-400" />
                                <span>1 Free Video</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <Check className="w-4 h-4 text-green-400" />
                                <span>No Credit Card</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <Check className="w-4 h-4 text-green-400" />
                                <span>₹2,999/month</span>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* Demo Video Section - HIGH CONVERSION */}
            <section className="py-20 px-6 bg-gradient-to-b from-purple-900/10 to-transparent">
                <div className="max-w-5xl mx-auto">
                    <motion.div
                        className="text-center mb-12"
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                    >
                        <h2 className="text-3xl md:text-4xl font-bold mb-4">
                            See It In <span className="gradient-text">Action</span>
                        </h2>
                        <p className="text-gray-400 text-lg">Watch how easy it is to create WhatsApp marketing videos</p>
                    </motion.div>

                    <motion.div
                        className="relative glass-dark p-4 rounded-2xl hover-glow cursor-pointer group"
                        initial={{ opacity: 0, scale: 0.95 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true }}
                        whileHover={{ scale: 1.02 }}
                    >
                        <div className="relative aspect-video rounded-xl overflow-hidden bg-gradient-to-br from-purple-900/50 to-pink-900/50">
                            <img src="/demo-placeholder.svg" alt="Demo Video" className="w-full h-full object-cover" />
                            <div className="absolute inset-0 flex items-center justify-center">
                                <div className="w-20 h-20 rounded-full bg-white/10 backdrop-blur-sm border-2 border-white/30 flex items-center justify-center group-hover:scale-110 transition-transform">
                                    <ChevronRight className="w-10 h-10 text-white ml-1" />
                                </div>
                            </div>
                        </div>
                        <div className="mt-4 text-center">
                            <p className="text-green-400 font-semibold">✨ Coming Soon: Live Demo</p>
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* Trust Signals & Social Proof */}
            <section className="py-16 px-6">
                <div className="max-w-6xl mx-auto">
                    {/* Trust Badges */}
                    <motion.div
                        className="flex flex-wrap justify-center gap-8 mb-16"
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                    >
                        <div className="flex items-center gap-3 glass px-6 py-3 rounded-full">
                            <Check className="w-5 h-5 text-green-400" />
                            <span className="text-sm font-semibold">No Credit Card Required</span>
                        </div>
                        <div className="flex items-center gap-3 glass px-6 py-3 rounded-full">
                            <Check className="w-5 h-5 text-green-400" />
                            <span className="text-sm font-semibold">1 Free Video</span>
                        </div>
                        <div className="flex items-center gap-3 glass px-6 py-3 rounded-full">
                            <Check className="w-5 h-5 text-green-400" />
                            <span className="text-sm font-semibold">Cancel Anytime</span>
                        </div>
                        <div className="flex items-center gap-3 glass px-6 py-3 rounded-full">
                            <Check className="w-5 h-5 text-green-400" />
                            <span className="text-sm font-semibold">Made in India 🇮🇳</span>
                        </div>
                    </motion.div>

                    {/* Customer Testimonials */}
                    <div className="text-center mb-8">
                        <h3 className="text-2xl md:text-3xl font-bold">
                            Loved by <span className="gradient-text">Indian Businesses</span>
                        </h3>
                    </div>

                    <div className="grid md:grid-cols-3 gap-6">
                        <motion.div
                            className="glass-dark p-6 rounded-xl"
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                        >
                            <div className="flex items-center gap-2 mb-3">
                                <div className="w-10 h-10 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 flex items-center justify-center text-white font-bold">
                                    R
                                </div>
                                <div>
                                    <div className="font-semibold">Rajesh Kumar</div>
                                    <div className="text-xs text-gray-400">Restaurant Owner, Mumbai</div>
                                </div>
                            </div>
                            <div className="text-yellow-400 mb-2">★★★★★</div>
                            <p className="text-sm text-gray-300 italic">
                                "Perfect for my restaurant! Created daily special videos in Hindi and English for WhatsApp. My orders increased 30%!"
                            </p>
                        </motion.div>

                        <motion.div
                            className="glass-dark p-6 rounded-xl"
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: 0.1 }}
                        >
                            <div className="flex items-center gap-2 mb-3">
                                <div className="w-10 h-10 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 flex items-center justify-center text-white font-bold">
                                    P
                                </div>
                                <div>
                                    <div className="font-semibold">Priya Sharma</div>
                                    <div className="text-xs text-gray-400">Real Estate Agent, Delhi</div>
                                </div>
                            </div>
                            <div className="text-yellow-400 mb-2">★★★★★</div>
                            <p className="text-sm text-gray-300 italic">
                                "Game changer! I create property tour videos in 5 languages. Clients love the professional touch."
                            </p>
                        </motion.div>

                        <motion.div
                            className="glass-dark p-6 rounded-xl"
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: 0.2 }}
                        >
                            <div className="flex items-center gap-2 mb-3">
                                <div className="w-10 h-10 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 flex items-center justify-center text-white font-bold">
                                    A
                                </div>
                                <div>
                                    <div className="font-semibold">Amit Patel</div>
                                    <div className="text-xs text-gray-400">Online Tutor, Bangalore</div>
                                </div>
                            </div>
                            <div className="text-yellow-400 mb-2">★★★★★</div>
                            <p className="text-sm text-gray-300 italic">
                                "Saves me hours! My course promos now reach students in their local language. Worth every rupee."
                            </p>
                        </motion.div>
                    </div>
                </div>
            </section>

            {/* Features Grid - Unlocked vs Locked */}
            <section className="py-20 px-6 bg-gradient-to-b from-transparent to-purple-900/20">
                <div className="max-w-7xl mx-auto">
                    <motion.div
                        className="text-center mb-16"
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                    >
                        <h2 className="text-4xl md:text-5xl font-bold mb-4">
                            <span className="gradient-text">8 Powerful Features</span>
                        </h2>
                        <p className="text-xl text-gray-300">
                            3 Live Now • 5 Coming Soon Based on Your Feedback
                        </p>
                    </motion.div>

                    <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                        {features.map((feature, index) => {
                            const Icon = feature.icon;
                            return (
                                <motion.div
                                    key={feature.id}
                                    className={`glass-dark p-6 rounded-2xl relative overflow-hidden ${feature.unlocked ? 'hover-glow border-2 border-green-500/30' : 'opacity-75'
                                        }`}
                                    initial={{ opacity: 0, y: 20 }}
                                    whileInView={{ opacity: feature.unlocked ? 1 : 0.75, y: 0 }}
                                    viewport={{ once: true }}
                                    transition={{ delay: index * 0.1 }}
                                    whileHover={{ y: feature.unlocked ? -5 : 0 }}
                                >
                                    {/* Badge */}
                                    <div className={`absolute top-3 right-3 px-2 py-1 rounded-full text-xs font-bold ${feature.unlocked
                                        ? 'bg-green-500/20 text-green-400'
                                        : 'bg-gray-500/20 text-gray-400'
                                        }`}>
                                        {feature.badge}
                                    </div>

                                    {/* Lock Icon for Locked Features */}
                                    {!feature.unlocked && (
                                        <Lock className="absolute top-3 left-3 w-5 h-5 text-gray-500" />
                                    )}

                                    <Icon className={`w-12 h-12 ${feature.iconColor} mb-4 mt-6`} />
                                    <h3 className="text-xl font-bold mb-2">{feature.name}</h3>
                                    <p className="text-sm text-gray-400 leading-relaxed">
                                        {feature.description}
                                    </p>

                                    {feature.unlocked && (
                                        <div className="mt-4 flex items-center gap-2 text-green-400 text-sm font-semibold">
                                            <Check className="w-4 h-4" />
                                            <span>Available Now</span>
                                        </div>
                                    )}
                                </motion.div>
                            );
                        })}
                    </div>

                    {/* Vote for Next Feature */}
                    <motion.div
                        className="mt-12 text-center glass-dark p-8 rounded-2xl"
                        initial={{ opacity: 0, scale: 0.95 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true }}
                    >
                        <Zap className="w-12 h-12 text-yellow-400 mx-auto mb-4" />
                        <h3 className="text-2xl font-bold mb-2">Which Feature Do YOU Want Next?</h3>
                        <p className="text-gray-400 mb-6">
                            We unlock features based on customer demand. Vote for your favorite!
                        </p>
                        <motion.button
                            className="btn-primary px-6 py-3"
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            onClick={() => setShowVoteModal(true)}
                        >
                            Vote Now
                        </motion.button>
                    </motion.div>
                </div>
            </section>

            {/* Why Technoaiamaze Section */}
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
                        <motion.div
                            className="glass-dark p-8 rounded-2xl"
                            initial={{ opacity: 0, x: -20 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            viewport={{ once: true }}
                        >
                            <MessageCircle className="w-12 h-12 text-green-400 mb-4" />
                            <h3 className="text-2xl font-bold mb-3">Built for WhatsApp</h3>
                            <p className="text-gray-400">
                                Perfect vertical format (9:16) for WhatsApp Status. 30-second optimized videos that Indian customers actually want.
                            </p>
                        </motion.div>

                        <motion.div
                            className="glass-dark p-8 rounded-2xl"
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: 0.1 }}
                        >
                            <Globe className="w-12 h-12 text-blue-400 mb-4" />
                            <h3 className="text-2xl font-bold mb-3">10 Indian Languages</h3>
                            <p className="text-gray-400">
                                Write once in English, get videos in Hindi, Tamil, Telugu, Marathi, Bengali, and more. Reach all of India.
                            </p>
                        </motion.div>

                        <motion.div
                            className="glass-dark p-8 rounded-2xl"
                            initial={{ opacity: 0, x: 20 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: 0.2 }}
                        >
                            <Sparkles className="w-12 h-12 text-purple-400 mb-4" />
                            <h3 className="text-2xl font-bold mb-3">₹2,999 vs ₹15,000</h3>
                            <p className="text-gray-400">
                                Global platforms charge ₹10,000-15,000/month. We're built for India - same quality, 5x cheaper pricing.
                            </p>
                        </motion.div>
                    </div>
                </div>
            </section>

            {/* Pricing Preview */}
            <section className="py-20 px-6 bg-gradient-to-b from-purple-900/20 to-transparent">
                <div className="max-w-4xl mx-auto text-center">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true }}
                    >
                        <h2 className="text-4xl md:text-5xl font-bold mb-6">
                            Simple, Affordable Pricing
                        </h2>
                        <p className="text-xl text-gray-300 mb-8">
                            Start free, upgrade when you're ready
                        </p>

                        <div className="grid md:grid-cols-3 gap-6 mb-12">
                            {/* Free */}
                            <div className="glass-dark p-6 rounded-2xl">
                                <div className="text-sm text-gray-400 mb-2">FREE</div>
                                <div className="text-4xl font-bold mb-4">₹0</div>
                                <ul className="text-sm text-left space-y-2 mb-6">
                                    <li className="flex items-center gap-2">
                                        <Check className="w-4 h-4 text-green-400" />
                                        1 free video
                                    </li>
                                    <li className="flex items-center gap-2">
                                        <Check className="w-4 h-4 text-green-400" />
                                        3 live features
                                    </li>
                                    <li className="flex items-center gap-2 text-gray-500">
                                        <Lock className="w-4 h-4" />
                                        Watermarked
                                    </li>
                                </ul>
                                <button className="w-full py-2 bg-gray-700 rounded-lg">Current</button>
                            </div>

                            {/* Starter */}
                            <div className="glass-dark p-6 rounded-2xl border-2 border-purple-500 relative">
                                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gradient-to-r from-purple-600 to-pink-600 px-4 py-1 rounded-full text-xs font-bold">
                                    MOST POPULAR
                                </div>
                                <div className="text-sm text-gray-400 mb-2">STARTER</div>
                                <div className="text-4xl font-bold mb-4">₹2,999<span className="text-sm text-gray-400">/mo</span></div>
                                <ul className="text-sm text-left space-y-2 mb-6">
                                    <li className="flex items-center gap-2">
                                        <Check className="w-4 h-4 text-green-400" />
                                        10 videos/month
                                    </li>
                                    <li className="flex items-center gap-2">
                                        <Check className="w-4 h-4 text-green-400" />
                                        No watermark
                                    </li>
                                    <li className="flex items-center gap-2">
                                        <Check className="w-4 h-4 text-green-400" />
                                        All 3 live features
                                    </li>
                                </ul>
                                <button className="w-full py-2 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg font-bold">
                                    Start Now
                                </button>
                            </div>

                            {/* Pro */}
                            <div className="glass-dark p-6 rounded-2xl">
                                <div className="text-sm text-gray-400 mb-2">PRO</div>
                                <div className="text-4xl font-bold mb-4">₹7,999<span className="text-sm text-gray-400">/mo</span></div>
                                <ul className="text-sm text-left space-y-2 mb-6">
                                    <li className="flex items-center gap-2">
                                        <Check className="w-4 h-4 text-green-400" />
                                        30 videos/month
                                    </li>
                                    <li className="flex items-center gap-2">
                                        <Check className="w-4 h-4 text-green-400" />
                                        Voice cloning
                                    </li>
                                    <li className="flex items-center gap-2">
                                        <Check className="w-4 h-4 text-green-400" />
                                        Priority support
                                    </li>
                                </ul>
                                <button className="w-full py-2 bg-purple-600 rounded-lg">
                                    Coming Soon
                                </button>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* Final CTA */}
            <section className="py-20 px-6">
                <motion.div
                    className="max-w-4xl mx-auto glass-dark p-12 rounded-3xl text-center"
                    initial={{ opacity: 0, scale: 0.95 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true }}
                >
                    <h2 className="text-4xl md:text-5xl font-bold mb-6">
                        Ready to Market on <span className="gradient-text">WhatsApp</span>?
                    </h2>
                    <p className="text-xl text-gray-300 mb-8">
                        Create your first marketing video in 10 languages - FREE!
                    </p>
                    <Link href="/generate">
                        <motion.button
                            className="btn-primary hover-glow px-10 py-5 text-xl"
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            Start Creating Free
                        </motion.button>
                    </Link>
                </motion.div>
            </section>

            {/* Feature Voting Modal */}
            <AnimatePresence>
                {showVoteModal && (
                    <motion.div
                        className="fixed inset-0 z-50 flex items-center justify-center p-6 bg-black/80 backdrop-blur-sm"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={() => setShowVoteModal(false)}
                    >
                        <motion.div
                            className="glass-dark p-8 rounded-2xl max-w-2xl w-full max-h-[80vh] overflow-y-auto"
                            initial={{ scale: 0.9, y: 20 }}
                            animate={{ scale: 1, y: 0 }}
                            exit={{ scale: 0.9, y: 20 }}
                            onClick={(e) => e.stopPropagation()}
                        >
                            <div className="flex items-center justify-between mb-6">
                                <h2 className="text-3xl font-bold">Vote for Next Feature</h2>
                                <button
                                    onClick={() => setShowVoteModal(false)}
                                    className="glass p-2 rounded-lg hover-glow"
                                >
                                    <X className="w-6 h-6" />
                                </button>
                            </div>

                            <p className="text-gray-400 mb-6">
                                We unlock features based on customer demand. Vote for the feature YOU want to see next!
                            </p>

                            {voteMessage && (
                                <motion.div
                                    className="mb-6 p-4 rounded-lg bg-green-500/20 border border-green-500/30 text-green-400"
                                    initial={{ opacity: 0, y: -10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                >
                                    {voteMessage}
                                </motion.div>
                            )}

                            <div className="space-y-4">
                                {lockedFeatures.map((feature) => {
                                    const Icon = feature.icon;
                                    const featureId = feature.name.toLowerCase().replace(/\s+/g, '_');
                                    const isVoting = votingFor === featureId;

                                    return (
                                        <motion.button
                                            key={feature.id}
                                            className="w-full glass p-4 rounded-xl text-left hover-glow transition-all disabled:opacity-50"
                                            whileHover={{ scale: isVoting ? 1 : 1.02 }}
                                            whileTap={{ scale: isVoting ? 1 : 0.98 }}
                                            onClick={() => handleVote(featureId)}
                                            disabled={isVoting || !!voteMessage}
                                        >
                                            <div className="flex items-start gap-4">
                                                <Icon className={`w-8 h-8 ${feature.iconColor} flex-shrink-0`} />
                                                <div className="flex-1">
                                                    <h3 className="text-lg font-bold mb-1">{feature.name}</h3>
                                                    <p className="text-sm text-gray-400">{feature.description}</p>
                                                </div>
                                                {isVoting && (
                                                    <div className="text-cyan-400 text-sm">Voting...</div>
                                                )}
                                            </div>
                                        </motion.button>
                                    );
                                })}
                            </div>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
        </main>
    );
}
