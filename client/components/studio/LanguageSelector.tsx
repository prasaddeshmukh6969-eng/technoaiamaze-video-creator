'use client'

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Globe, CheckCircle } from 'lucide-react';

interface LanguageSelectorProps {
    onLanguageChange: (language: string, autoSelectVoice: boolean) => void;
}

const LANGUAGES = [
    { code: 'en', name: 'English', flag: '🇬🇧', voices: 20 },
    { code: 'hi', name: 'Hindi', flag: '🇮🇳', voices: 4 },
    { code: 'es', name: 'Spanish', flag: '🇪🇸', voices: 15 },
    { code: 'fr', name: 'French', flag: '🇫🇷', voices: 10 },
    { code: 'de', name: 'German', flag: '🇩🇪', voices: 8 },
    { code: 'ja', name: 'Japanese', flag: '🇯🇵', voices: 6 },
    { code: 'zh', name: 'Chinese', flag: '🇨🇳', voices: 10 },
    { code: 'ar', name: 'Arabic', flag: '🇸🇦', voices: 6 },
    { code: 'pt', name: 'Portuguese', flag: '🇵🇹', voices: 8 },
    { code: 'ru', name: 'Russian', flag: '🇷🇺', voices: 5 },
    { code: 'ko', name: 'Korean', flag: '🇰🇷', voices: 4 },
    { code: 'it', name: 'Italian', flag: '🇮🇹', voices: 6 },
    { code: 'ta', name: 'Tamil', flag: '🇮🇳', voices: 2 },
    { code: 'te', name: 'Telugu', flag: '🇮🇳', voices: 2 },
    { code: 'bn', name: 'Bengali', flag: '🇮🇳', voices: 2 },
];

export default function LanguageSelector({ onLanguageChange }: LanguageSelectorProps) {
    const [outputLanguage, setOutputLanguage] = useState('en');
    const [autoSelectVoice, setAutoSelectVoice] = useState(true);

    const handleLanguageChange = (lang: string) => {
        setOutputLanguage(lang);
        onLanguageChange(lang, autoSelectVoice);
    };

    const selectedLang = LANGUAGES.find(l => l.code === outputLanguage);

    return (
        <div className="glass-dark p-6 rounded-2xl">
            <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Globe className="w-5 h-5 text-cyan-400" />
                Output Language
            </h3>

            <div className="space-y-4">
                {/* Language Dropdown */}
                <div>
                    <label className="block text-sm font-medium mb-2">
                        Video Language (script will be translated)
                    </label>
                    <select
                        className="w-full bg-black/30 border border-gray-600 rounded-lg p-3 text-white focus:border-cyan-400 focus:outline-none"
                        value={outputLanguage}
                        onChange={(e) => handleLanguageChange(e.target.value)}
                    >
                        {LANGUAGES.map(lang => (
                            <option key={lang.code} value={lang.code}>
                                {lang.flag} {lang.name} ({lang.voices} voices available)
                            </option>
                        ))}
                    </select>
                </div>

                {/* Language Info */}
                {selectedLang && (
                    <motion.div
                        className="p-3 bg-cyan-500/10 rounded-lg border border-cyan-500/30"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                    >
                        <div className="flex items-center gap-2 text-sm">
                            <CheckCircle className="w-4 h-4 text-cyan-400" />
                            <span className="text-cyan-300">
                                {selectedLang.voices} professional voices available for {selectedLang.name}
                            </span>
                        </div>
                    </motion.div>
                )}

                {/* Auto-select Voice */}
                <div className="flex items-center justify-between p-3 bg-black/20 rounded-lg">
                    <div>
                        <div className="font-medium text-sm">Auto-select Voice</div>
                        <div className="text-xs text-gray-400">Automatically choose the best voice for this language</div>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                        <input
                            type="checkbox"
                            checked={autoSelectVoice}
                            onChange={(e) => {
                                setAutoSelectVoice(e.target.checked);
                                onLanguageChange(outputLanguage, e.target.checked);
                            }}
                            className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-gradient-to-r peer-checked:from-cyan-600 peer-checked:to-blue-600"></div>
                    </label>
                </div>

                {/* Translation Note */}
                <div className="text-xs text-gray-500 p-3 bg-black/10 rounded-lg border border-gray-700">
                    <strong>How it works:</strong> Write your script in any language, and it will be automatically translated to {selectedLang?.name} for the video generation.
                </div>
            </div>
        </div>
    );
}
