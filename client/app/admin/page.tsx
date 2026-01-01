'use client'

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Eye, Users, MousePointerClick, Mail, ThumbsUp, RefreshCw } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface AnalyticsStats {
    total_visitors: number;
    unique_visitors: number;
    page_views: { [key: string]: number };
    template_clicks: { [key: string]: number };
    template_clicks_total: number;
    email_signups: number;
    emails: Array<{ email: string; timestamp: string }>;
    feature_votes: { [key: string]: number };
    feature_votes_total: number;
}

export default function AdminDashboard() {
    const [password, setPassword] = useState('');
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [stats, setStats] = useState<AnalyticsStats | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const fetchStats = async (pwd: string) => {
        setLoading(true);
        setError('');

        try {
            const response = await fetch(`${API_URL}/api/v1/analytics/stats?password=${pwd}`);

            if (response.ok) {
                const data = await response.json();
                setStats(data);
                setIsAuthenticated(true);
            } else {
                setError('Invalid password');
                setIsAuthenticated(false);
            }
        } catch (err) {
            setError('Failed to fetch analytics');
        } finally {
            setLoading(false);
        }
    };

    const handleLogin = (e: React.FormEvent) => {
        e.preventDefault();
        fetchStats(password);
    };

    const handleRefresh = () => {
        if (isAuthenticated) {
            fetchStats(password);
        }
    };

    if (!isAuthenticated) {
        return (
            <div className="min-h-screen flex items-center justify-center p-6">
                <motion.div
                    className="glass-dark p-8 rounded-2xl max-w-md w-full"
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                >
                    <h1 className="text-3xl font-bold mb-6 text-center">
                        📊 Analytics Dashboard
                    </h1>

                    <form onSubmit={handleLogin} className="space-y-4">
                        <div>
                            <label className="block text-sm text-gray-400 mb-2">
                                Admin Password
                            </label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Enter password"
                                className="w-full px-4 py-3 rounded-lg bg-black/50 border border-gray-700 focus:border-purple-500 outline-none"
                                required
                            />
                        </div>

                        {error && (
                            <div className="text-red-400 text-sm text-center">
                                {error}
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full btn-primary py-3 rounded-lg hover-glow"
                        >
                            {loading ? 'Loading...' : 'Access Dashboard'}
                        </button>
                    </form>

                    <p className="text-xs text-gray-500 text-center mt-4">
                        Default password: technoaiamaze2026
                    </p>
                </motion.div>
            </div>
        );
    }

    if (!stats) {
        return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
    }

    const templateNames: { [key: string]: string } = {
        'restaurant': '🍽️ Restaurant',
        'real_estate': '🏠 Real Estate',
        'education': '📚 Education',
        'custom': '✨ Custom'
    };

    const featureNames: { [key: string]: string } = {
        'voice_cloning': 'Voice Cloning',
        'bulk_generation': 'Bulk Generation',
        'auto_resize': 'Auto Resize',
        'custom_backgrounds': 'Custom Backgrounds',
        'scheduled_posts': 'Scheduled Posts'
    };

    return (
        <div className="min-h-screen p-6">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <motion.h1
                        className="text-4xl font-bold"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                    >
                        📊 Analytics Dashboard
                    </motion.h1>

                    <button
                        onClick={handleRefresh}
                        className="glass px-4 py-2 rounded-lg flex items-center gap-2 hover-glow"
                        disabled={loading}
                    >
                        <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                        Refresh
                    </button>
                </div>

                {/* Overview Stats */}
                <div className="grid md:grid-cols-4 gap-6 mb-8">
                    <StatCard
                        icon={Eye}
                        label="Total Visitors"
                        value={stats.total_visitors}
                        color="text-blue-400"
                    />
                    <StatCard
                        icon={Users}
                        label="Unique Visitors"
                        value={stats.unique_visitors}
                        color="text-green-400"
                    />
                    <StatCard
                        icon={MousePointerClick}
                        label="Template Clicks"
                        value={stats.template_clicks_total}
                        color="text-purple-400"
                    />
                    <StatCard
                        icon={Mail}
                        label="Email Signups"
                        value={stats.email_signups}
                        color="text-pink-400"
                    />
                </div>

                {/* Template Clicks */}
                <motion.div
                    className="glass-dark p-6 rounded-xl mb-6"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                >
                    <h2 className="text-2xl font-bold mb-4">🎯 Template Interest</h2>
                    <div className="space-y-3">
                        {Object.entries(stats.template_clicks).map(([id, count]) => (
                            <div key={id} className="flex items-center justify-between">
                                <span className="text-gray-300">{templateNames[id] || id}</span>
                                <div className="flex items-center gap-4">
                                    <div className="w-64 h-8 bg-black/50 rounded-full overflow-hidden">
                                        <div
                                            className="h-full bg-gradient-to-r from-purple-500 to-pink-500"
                                            style={{
                                                width: `${stats.template_clicks_total > 0 ? (count / stats.template_clicks_total) * 100 : 0}%`
                                            }}
                                        />
                                    </div>
                                    <span className="text-xl font-bold w-16 text-right">{count}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </motion.div>

                {/* Feature Votes */}
                {stats.feature_votes_total > 0 && (
                    <motion.div
                        className="glass-dark p-6 rounded-xl mb-6"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                    >
                        <h2 className="text-2xl font-bold mb-4">⭐ Feature Votes</h2>
                        <div className="space-y-3">
                            {Object.entries(stats.feature_votes)
                                .sort(([, a], [, b]) => (b as number) - (a as number))
                                .map(([id, count]) => (
                                    <div key={id} className="flex items-center justify-between">
                                        <span className="text-gray-300">{featureNames[id] || id}</span>
                                        <div className="flex items-center gap-4">
                                            <div className="w-64 h-8 bg-black/50 rounded-full overflow-hidden">
                                                <div
                                                    className="h-full bg-gradient-to-r from-blue-500 to-cyan-500"
                                                    style={{
                                                        width: `${stats.feature_votes_total > 0 ? (count / stats.feature_votes_total) * 100 : 0}%`
                                                    }}
                                                />
                                            </div>
                                            <span className="text-xl font-bold w-16 text-right">{count}</span>
                                        </div>
                                    </div>
                                ))}
                        </div>
                    </motion.div>
                )}

                {/* Email List */}
                {stats.emails.length > 0 && (
                    <motion.div
                        className="glass-dark p-6 rounded-xl"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3 }}
                    >
                        <h2 className="text-2xl font-bold mb-4">📧 Email Signups ({stats.emails.length})</h2>
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead>
                                    <tr className="text-left border-b border-gray-700">
                                        <th className="pb-2">Email</th>
                                        <th className="pb-2">Date</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {stats.emails.map((item, idx) => (
                                        <tr key={idx} className="border-b border-gray-800">
                                            <td className="py-2 text-gray-300">{item.email}</td>
                                            <td className="py-2 text-gray-400 text-sm">
                                                {new Date(item.timestamp).toLocaleString()}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </motion.div>
                )}
            </div>
        </div>
    );
}

// Stat Card Component
function StatCard({ icon: Icon, label, value, color }: any) {
    return (
        <motion.div
            className="glass-dark p-6 rounded-xl"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            whileHover={{ scale: 1.02 }}
        >
            <div className="flex items-start justify-between">
                <div>
                    <p className="text-gray-400 text-sm mb-1">{label}</p>
                    <p className="text-4xl font-bold">{value}</p>
                </div>
                <Icon className={`w-8 h-8 ${color}`} />
            </div>
        </motion.div>
    );
}
