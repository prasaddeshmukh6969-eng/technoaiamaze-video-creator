'use client'

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, Sparkles, MessageCircle, Languages, LayoutTemplate } from 'lucide-react';
import Link from 'next/link';
import { trackPageView, trackTemplateClick } from '@/lib/analytics';

export default function GeneratePage() {
    const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);
    const [step, setStep] = useState<'choose' | 'customize' | 'generate'>('choose');

    // Track page view on mount
    useEffect(() => {
        trackPageView('/generate');
    }, []);

    const templates = [
        {
            id: 'restaurant',
            name: '🍽️ Restaurant Promo',
            description: 'Daily specials, offers, menu items',
            example: 'This week only! Try our Butter Chicken for just ₹299'
        },
        {
            id: 'real_estate',
            name: '🏠 Property Listing',
            description: 'Apartments, villas, commercial spaces',
            example: '3 BHK in Whitefield, 1450 sq ft, ₹85 lakhs only!'
        },
        {
            id: 'education',
            name: '📚 Course Promotion',
            description: 'Tutoring, online courses, coaching',
            example: 'Enroll now in NEET coaching! Limited seats'
        },
        {
            id: 'custom',
            name: '✨ Custom Video',
            description: 'Create your own from scratch',
            example: 'Full control over avatar, script, and voice'
        }
    ];

    return (
        <main className="min-h-screen p-6">
            {/* Header */}
            <motion.div
                className="max-w-5xl mx-auto mb-8"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <Link href="/">
                    <button className="glass px-4 py-2 rounded-lg flex items-center gap-2 hover-glow mb-6">
                        <ArrowLeft className="w-4 h-4" />
                        Back to Home
                    </button>
                </Link>

                <div className="text-center mb-8">
                    <h1 className="text-4xl md:text-5xl font-bold mb-4">
                        Create Your <span className="gradient-text">WhatsApp Video</span>
                    </h1>
                    <p className="text-gray-400 text-lg">
                        Choose a template or start from scratch - video ready in 2 minutes!
                    </p>
                </div>
            </motion.div>

            {/* Template Selection */}
            {step === 'choose' && (
                <motion.div
                    className="max-w-5xl mx-auto"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <div className="grid md:grid-cols-2 gap-6">
                        {templates.map((template, index) => (
                            <motion.div
                                key={template.id}
                                className="glass-dark p-6 rounded-xl cursor-pointer hover-glow transition-all"
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 }}
                                whileHover={{ scale: 1.02 }}
                                onClick={() => {
                                    trackTemplateClick(template.id); // Track the click
                                    setSelectedTemplate(template.id);
                                    setStep('customize');
                                }}
                            >
                                <div className="flex items-start gap-4">
                                    <div className="text-4xl">{template.name.split(' ')[0]}</div>
                                    <div className="flex-1">
                                        <h3 className="text-xl font-bold mb-2">
                                            {template.name.substring(3)}
                                        </h3>
                                        <p className="text-gray-400 text-sm mb-3">
                                            {template.description}
                                        </p>
                                        <div className="glass px-3 py-2 rounded text-xs text-gray-300 italic">
                                            "{template.example}"
                                        </div>
                                    </div>
                                </div>

                                <div className="mt-4 flex items-center justify-between text-sm">
                                    <div className="flex items-center gap-2 text-green-400">
                                        <MessageCircle className="w-4 h-4" />
                                        <span>WhatsApp Ready</span>
                                    </div>
                                    <div className="flex items-center gap-2 text-blue-400">
                                        <Languages className="w-4 h-4" />
                                        <span>10 Languages</span>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </div>

                    {/* Features Banner */}
                    <motion.div
                        className="mt-12 glass-dark p-6 rounded-xl text-center"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.4 }}
                    >
                        <h3 className="text-xl font-bold mb-3">
                            ✨ All Videos Include
                        </h3>
                        <div className="flex flex-wrap justify-center gap-6 text-sm">
                            <div className="flex items-center gap-2">
                                <MessageCircle className="w-5 h-5 text-green-400" />
                                <span>9:16 WhatsApp Format</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <Languages className="w-5 h-5 text-blue-400" />
                                <span>Multi-Language Support</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <LayoutTemplate className="w-5 h-5 text-purple-400" />
                                <span>Professional Templates</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <Sparkles className="w-5 h-5 text-yellow-400" />
                                <span>AI-Powered</span>
                            </div>
                        </div>
                    </motion.div>
                </motion.div>
            )}

            {/* Customization Step (Coming Soon) */}
            {step === 'customize' && (
                <motion.div
                    className="max-w-3xl mx-auto text-center"
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                >
                    <div className="glass-dark p-12 rounded-2xl">
                        <div className="text-6xl mb-6">🚀</div>
                        <h2 className="text-3xl font-bold mb-4">
                            Feature Coming Soon!
                        </h2>
                        <p className="text-gray-400 mb-6">
                            We're building the {selectedTemplate} template customization interface.
                            <br />
                            For now, the backend needs to be deployed to enable video generation.
                        </p>
                        <button
                            onClick={() => setStep('choose')}
                            className="btn-primary hover-glow px-6 py-3"
                        >
                            Back to Templates
                        </button>
                    </div>
                </motion.div>
            )}
        </main>
    );
}

