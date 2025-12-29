'use client'

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Mail, Phone, Lock, User } from 'lucide-react';

interface AuthModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSuccess: () => void;
    onLogin: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
    onRegister: (email: string, phone: string, password: string) => Promise<{ success: boolean; error?: string }>;
}

export default function AuthModal({ isOpen, onClose, onSuccess, onLogin, onRegister }: AuthModalProps) {
    const [mode, setMode] = useState<'login' | 'register'>('register');
    const [email, setEmail] = useState('');
    const [phone, setPhone] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            let result;
            if (mode === 'register') {
                result = await onRegister(email, phone, password);
            } else {
                result = await onLogin(email, password);
            }

            if (result.success) {
                onSuccess();
                setEmail('');
                setPhone('');
                setPassword('');
            } else {
                setError(result.error || 'Authentication failed');
            }
        } catch (err) {
            setError('An unexpected error occurred');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
                    {/* Backdrop */}
                    <motion.div
                        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                    />

                    {/* Modal */}
                    <motion.div
                        className="relative w-full max-w-md bg-gradient-to-br from-gray-900 to-purple-900 rounded-2xl shadow-2xl overflow-hidden"
                        initial={{ scale: 0.9, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 0.9, opacity: 0 }}
                    >
                        {/* Close button */}
                        <button
                            onClick={onClose}
                            className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors z-10"
                        >
                            <X className="w-6 h-6" />
                        </button>

                        {/* Header with glassmorphic effect */}
                        <div className="relative p-6 bg-white/5 backdrop-blur-sm border-b border-white/10">
                            <h2 className="text-2xl font-bold text-white mb-2">
                                {mode === 'login' ? 'Welcome Back!' : 'Create Account'}
                            </h2>
                            <p className="text-gray-300 text-sm">
                                {mode === 'login'
                                    ? 'Login to continue creating amazing videos'
                                    : 'Register to start creating AI-powered videos'}
                            </p>
                        </div>

                        {/* Mode Toggle */}
                        <div className="flex p-2 m-6 bg-black/20 rounded-lg">
                            <button
                                onClick={() => setMode('register')}
                                className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all ${mode === 'register'
                                        ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                                        : 'text-gray-400 hover:text-white'
                                    }`}
                            >
                                Register
                            </button>
                            <button
                                onClick={() => setMode('login')}
                                className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all ${mode === 'login'
                                        ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                                        : 'text-gray-400 hover:text-white'
                                    }`}
                            >
                                Login
                            </button>
                        </div>

                        {/* Form */}
                        <form onSubmit={handleSubmit} className="p-6 space-y-4">
                            {/* Email */}
                            <div>
                                <label className="block text-sm font-medium text-gray-300 mb-2">
                                    <Mail className="w-4 h-4 inline mr-2" />
                                    Email
                                </label>
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                    className="w-full px-4 py-3 bg-black/30 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:border-purple-400 focus:outline-none transition-colors"
                                    placeholder="your@email.com"
                                />
                            </div>

                            {/* Phone (Register only) */}
                            {mode === 'register' && (
                                <div>
                                    <label className="block text-sm font-medium text-gray-300 mb-2">
                                        <Phone className="w-4 h-4 inline mr-2" />
                                        Phone Number
                                    </label>
                                    <input
                                        type="tel"
                                        value={phone}
                                        onChange={(e) => setPhone(e.target.value)}
                                        required
                                        className="w-full px-4 py-3 bg-black/30 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:border-purple-400 focus:outline-none transition-colors"
                                        placeholder="+1234567890"
                                    />
                                    <p className="text-xs text-gray-400 mt-1">Include country code (e.g., +91 for India)</p>
                                </div>
                            )}

                            {/* Password */}
                            <div>
                                <label className="block text-sm font-medium text-gray-300 mb-2">
                                    <Lock className="w-4 h-4 inline mr-2" />
                                    Password
                                </label>
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                    minLength={6}
                                    className="w-full px-4 py-3 bg-black/30 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:border-purple-400 focus:outline-none transition-colors"
                                    placeholder="••••••••"
                                />
                                {mode === 'register' && (
                                    <p className="text-xs text-gray-400 mt-1">Minimum 6 characters</p>
                                )}
                            </div>

                            {/* Error Message */}
                            {error && (
                                <div className="p-3 bg-red-500/10 border border-red-500 rounded-lg text-red-400 text-sm">
                                    {error}
                                </div>
                            )}

                            {/* Submit Button */}
                            <button
                                type="submit"
                                disabled={isLoading}
                                className="w-full py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold rounded-lg shadow-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {isLoading ? (
                                    <span className="flex items-center justify-center gap-2">
                                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                        Processing...
                                    </span>
                                ) : (
                                    mode === 'login' ? 'Login' : 'Create Account'
                                )}
                            </button>
                        </form>

                        {/* Footer */}
                        <div className="p-6 bg-white/5 border-t border-white/10 text-center text-sm text-gray-400">
                            {mode === 'login' ? (
                                <p>
                                    Don't have an account?{' '}
                                    <button
                                        onClick={() => setMode('register')}
                                        className="text-purple-400 hover:text-purple-300 font-medium"
                                    >
                                        Register here
                                    </button>
                                </p>
                            ) : (
                                <p>
                                    Already have an account?{' '}
                                    <button
                                        onClick={() => setMode('login')}
                                        className="text-purple-400 hover:text-purple-300 font-medium"
                                    >
                                        Login here
                                    </button>
                                </p>
                            )}
                        </div>
                    </motion.div>
                </div>
            )}
        </AnimatePresence>
    );
}
