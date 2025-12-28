'use client'

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Wand2, Loader2, Copy, CheckCircle, Globe, Clock } from 'lucide-react';

interface ScriptGeneratorProps {
    onUseScript: (script: string) => void;
}

const BUSINESS_CATEGORIES = [
    { id: 'tech', name: '🖥️ Tech & Software', keywords: 'innovation, AI, automation, cloud, digital', colors: 'Blue, Cyan, Purple' },
    { id: 'healthcare', name: '⚕️ Healthcare', keywords: 'care, health, trust, expertise, wellness', colors: 'White, Blue, Green' },
    { id: 'food', name: '🍔 Food & Restaurant', keywords: 'delicious, fresh, quality, taste, authentic', colors: 'Red, Orange, Yellow' },
    { id: 'fashion', name: '👗 Fashion & Beauty', keywords: 'beauty, style, trends, luxury, elegant', colors: 'Pink, Purple, Gold' },
    { id: 'education', name: '📚 Education', keywords: 'learn, grow, success, future, knowledge', colors: 'Blue, Green, Orange' },
    { id: 'realestate', name: '🏠 Real Estate', keywords: 'dream home, investment, location, luxury', colors: 'Gold, Brown, Blue' },
    { id: 'ecommerce', name: '🛒 E-commerce', keywords: 'deals, quality, shop, save, convenient', colors: 'Bright, Multi-color' },
    { id: 'finance', name: '💰 Finance', keywords: 'secure, growth, trust, future, invest', colors: 'Blue, Green, Gold' },
    { id: 'fitness', name: '💪 Fitness', keywords: 'strong, fit, energy, power, transform', colors: 'Red, Orange, Black' },
    { id: 'travel', name: '✈️ Travel', keywords: 'explore, adventure, dream, discover, journey', colors: 'Blue, Green, Orange' },
];

const INDIAN_LANGUAGES = [
    { code: 'en', name: 'English', flag: '🇬🇧', native: 'English' },
    { code: 'hi', name: 'Hindi', flag: '🇮🇳', native: 'हिन्दी' },
    { code: 'ta', name: 'Tamil', flag: '🇮🇳', native: 'தமிழ்' },
    { code: 'te', name: 'Telugu', flag: '🇮🇳', native: 'తెలుగు' },
    { code: 'mr', name: 'Marathi', flag: '🇮🇳', native: 'मराठी' },
    { code: 'gu', name: 'Gujarati', flag: '🇮🇳', native: 'ગુજરાતી' },
    { code: 'bn', name: 'Bengali', flag: '🇮🇳', native: 'বাংলা' },
    { code: 'kn', name: 'Kannada', flag: '🇮🇳', native: 'ಕನ್ನಡ' },
    { code: 'ml', name: 'Malayalam', flag: '🇮🇳', native: 'മലയാളം' },
    { code: 'pa', name: 'Punjabi', flag: '🇮🇳', native: 'ਪੰਜਾਬੀ' },
    { code: 'or', name: 'Odia', flag: '🇮🇳', native: 'ଓଡ଼ିଆ' },
    { code: 'as', name: 'Assamese', flag: '🇮🇳', native: 'অসমীয়া' },
    { code: 'ur', name: 'Urdu', flag: '🇮🇳', native: 'اردو' },
    { code: 'sa', name: 'Sanskrit', flag: '🇮🇳', native: 'संस्कृतम्' },
    { code: 'kok', name: 'Konkani', flag: '🇮🇳', native: 'कोंकणी' },
    { code: 'mni', name: 'Manipuri', flag: '🇮🇳', native: 'মৈতৈলোন্' },
    { code: 'ne', name: 'Nepali', flag: '🇮🇳', native: 'नेपाली' },
];

const VIDEO_DURATIONS = [
    { value: 30, label: '30 seconds', scenes: 2, words: 60 },
    { value: 60, label: '1 minute', scenes: 3, words: 120 },
    { value: 120, label: '2 minutes', scenes: 4, words: 240 },
    { value: 180, label: '3 minutes', scenes: 5, words: 360 },
    { value: 300, label: '5 minutes', scenes: 6, words: 600 },
];

const INTRO_TEMPLATES = [
    { id: 'welcome', name: 'Welcome', template: 'Welcome to [COMPANY]! ' },
    { id: 'introducing', name: 'Product Launch', template: 'Introducing [COMPANY] - ' },
    { id: 'meet', name: 'Service Intro', template: 'Meet [COMPANY], ' },
    { id: 'discover', name: 'Discovery', template: 'Discover [COMPANY] - ' },
    { id: 'experience', name: 'Experience', template: 'Experience the difference with [COMPANY]. ' },
];

const TONE_PRESETS = [
    { id: 'professional', name: 'Professional', emoji: '💼', desc: 'Clear and business-focused' },
    { id: 'cinematic', name: 'Cinematic', emoji: '🎬', desc: 'Epic and dramatic' },
    { id: 'attractive', name: 'Attractive', emoji: '🌟', desc: 'Engaging and appealing' },
    { id: 'eyecatching', name: 'Eye-catching', emoji: '⚡', desc: 'Bold and attention-grabbing' },
    { id: 'lovable', name: 'Lovable', emoji: '😊', desc: 'Warm and friendly' },
    { id: 'emotional', name: 'Emotional', emoji: '😢', desc: 'Touching and heartfelt' },
    { id: 'energetic', name: 'Energetic', emoji: '🔥', desc: 'Dynamic and exciting' },
    { id: 'trustworthy', name: 'Trustworthy', emoji: '🤝', desc: 'Reliable and credible' },
];

// Words to keep in English for code-mixing
const KEEP_IN_ENGLISH = [
    'AI', 'ML', 'cloud', 'app', 'website', 'online', 'software', 'digital',
    'technology', 'smartphone', 'internet', 'email', 'WhatsApp', 'Facebook',
    'Instagram', 'YouTube', 'Google', 'Amazon', 'Flipkart', 'Paytm'
];

export default function ScriptGenerator({ onUseScript }: ScriptGeneratorProps) {
    const [companyName, setCompanyName] = useState('');
    const [keywords, setKeywords] = useState('');
    const [category, setCategory] = useState('tech');
    const [introTemplate, setIntroTemplate] = useState('welcome');
    const [tone, setTone] = useState('professional');
    const [scriptLanguage, setScriptLanguage] = useState('en');
    const [duration, setDuration] = useState(60); // Default 1 minute
    const [generatedScript, setGeneratedScript] = useState('');
    const [isGenerating, setIsGenerating] = useState(false);
    const [copied, setCopied] = useState(false);

    const selectedCategory = BUSINESS_CATEGORIES.find(c => c.id === category);
    const selectedDuration = VIDEO_DURATIONS.find(d => d.value === duration);
    const selectedLanguage = INDIAN_LANGUAGES.find(l => l.code === scriptLanguage);

    const generateScript = () => {
        setIsGenerating(true);

        setTimeout(() => {
            const intro = INTRO_TEMPLATES.find(t => t.id === introTemplate);
            const company = companyName || (scriptLanguage === 'hi' ? 'आपकी कंपनी' : 'Your Company');
            const categoryKeywords = keywords || selectedCategory?.keywords || '';
            const keywordsList = categoryKeywords.split(',').map(k => k.trim()).filter(k => k);

            const numScenes = selectedDuration?.scenes || 3;
            let script = '';

            // Generate script based on duration
            for (let i = 1; i <= numScenes; i++) {
                if (i === 1) {
                    // Scene 1: Opening Hook
                    script += scriptLanguage === 'hi' ? `[दृश्य 1: शुरुआत]\n` : scriptLanguage === 'en' ? `[Scene 1: Opening]\n` : `[காட்சி 1: தொடக்கம்]\n`;
                    script += intro?.template.replace('[COMPANY]', company) || '';

                    if (tone === 'cinematic') {
                        script += scriptLanguage === 'hi'
                            ? `एक ऐसी दुनिया में जहां उत्कृष्टता मायने रखती है, ${company} अपनी ${keywordsList[0] || 'सेवाओं'} के प्रति प्रतिबद्धता के साथ अलग खड़ा है।\n\n`
                            : `In a world where excellence defines success, ${company} stands apart with our unwavering commitment to ${keywordsList[0] || 'excellence'}.\n\n`;
                    } else {
                        script += scriptLanguage === 'hi'
                            ? `हम ${keywordsList.slice(0, 2).join(' और ')} में विशेषज्ञ हैं।\n\n`
                            : `We specialize in delivering ${keywordsList.slice(0, 2).join(' and ')} that exceeds expectations.\n\n`;
                    }
                } else if (i === 2 && numScenes >= 2) {
                    // Scene 2: The Challenge
                    script += scriptLanguage === 'hi' ? `[दृश्य 2: चुनौती]\n` : `[Scene 2: The Challenge]\n`;
                    script += scriptLanguage === 'hi'
                        ? `क्या आप ${keywordsList[0] || 'समाधान'} की तलाश में हैं जो वास्तव में काम करे? बाजार में बहुत विकल्प हैं, लेकिन ${company} अलग क्यों है?\n\n`
                        : `Are you searching for ${keywordsList[0] || 'solutions'} that truly deliver? In a crowded marketplace, what makes ${company} different?\n\n`;
                } else if (i === 3 && numScenes >= 3) {
                    // Scene 3: Our Solution
                    script += scriptLanguage === 'hi' ? `[दृश्य 3: हमारा समाधान]\n` : `[Scene 3: Our Solution]\n`;
                    script += scriptLanguage === 'hi'
                        ? `${company} में, हम सिर्फ सेवाएं नहीं देते - हम अनुभव बनाते हैं। हमारी ${keywordsList[1] || 'टीम'} हर दिन ${keywordsList[2] || 'innovation'} के साथ काम करती है।\n\n`
                        : `At ${company}, we don't just provide services - we create experiences. Our team brings ${keywordsList[2] || 'innovation'} to every project.\n\n`;
                } else if (i === 4 && numScenes >= 4) {
                    // Scene 4: Key Features
                    script += scriptLanguage === 'hi' ? `[दृश्य 4: हमें क्यों चुनें]\n` : `[Scene 4: Why Choose Us]\n`;
                    script += scriptLanguage === 'hi'
                        ? `✨ ${keywordsList[0] || 'quality'} जिस पर आप भरोसा कर सकते हैं\n⚡ ${keywordsList[1] || 'fast'} और reliable परिणाम\n🎯 Customer satisfaction हमारी priority\n💡 वर्षों के experience के साथ proven expertise\n\n`
                        : `✨ ${keywordsList[0] || 'Quality'} you can trust\n⚡ ${keywordsList[1] || 'Fast'} and reliable delivery\n🎯 Customer satisfaction is our priority\n💡 Proven expertise\n\n`;
                } else if (i === 5 && numScenes >= 5) {
                    // Scene 5: Social Proof
                    script += scriptLanguage === 'hi' ? `[दृश्य 5: सफलता की कहानियां]\n` : `[Scene 5: Success Stories]\n`;
                    script += scriptLanguage === 'hi'
                        ? `हजारों खुश customers पहले से ही ${company} पर trust करते हैं। उनकी success stories हमें inspire करती हैं। आप अगले हो सकते हैं!\n\n`
                        : `Thousands of satisfied customers already trust ${company}. Their success stories inspire us. You could be next!\n\n`;
                } else if (i === numScenes) {
                    // Final Scene: Call to Action
                    script += scriptLanguage === 'hi' ? `[दृश्य ${i}: अभी action लें]\n` : `[Scene ${i}: Take Action Now]\n`;
                    script += scriptLanguage === 'hi'
                        ? `${company} - जहां आपके सपने मिलते हैं हमारी expertise से। आज ही contact करें और difference experience करें।\n\n`
                        : `${company} - where your vision meets our expertise. Contact us today and experience the difference.\n\n`;
                }
            }

            // Closing
            script += scriptLanguage === 'hi'
                ? `[समापन]\nधन्यवाद! हम आपसे connect होने के लिए excited हैं।`
                : `[Closing]\nThank you! We look forward to connecting with you.`;

            setGeneratedScript(script);
            setIsGenerating(false);
        }, 1500);
    };

    const copyToClipboard = () => {
        navigator.clipboard.writeText(generatedScript);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    const useScript = () => {
        onUseScript(generatedScript);
    };

    return (
        <div className="glass-dark p-6 rounded-2xl">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                <Wand2 className="w-6 h-6 text-purple-400" />
                AI Script Generator
            </h2>

            <div className="space-y-4">
                {/* Script Language - Compact Grid */}
                <div>
                    <label className="block text-sm font-medium mb-2 flex items-center gap-2">
                        <Globe className="w-4 h-4" />
                        Script Language
                    </label>
                    <select
                        className="w-full bg-black/30 border border-gray-600 rounded-lg p-2 text-white focus:border-cyan-400 focus:outline-none text-sm"
                        value={scriptLanguage}
                        onChange={(e) => setScriptLanguage(e.target.value)}
                    >
                        {INDIAN_LANGUAGES.map(lang => (
                            <option key={lang.code} value={lang.code}>
                                {lang.flag} {lang.name} ({lang.native})
                            </option>
                        ))}
                    </select>
                </div>

                {/* Video Duration */}
                <div>
                    <label className="block text-sm font-medium mb-2 flex items-center gap-2">
                        <Clock className="w-4 h-4" />
                        Video Duration
                    </label>
                    <select
                        className="w-full bg-black/30 border border-gray-600 rounded-lg p-2 text-white focus:border-purple-400 focus:outline-none text-sm"
                        value={duration}
                        onChange={(e) => setDuration(parseInt(e.target.value))}
                    >
                        {VIDEO_DURATIONS.map(dur => (
                            <option key={dur.value} value={dur.value}>
                                {dur.label} ({dur.scenes} scenes, ~{dur.words} words)
                            </option>
                        ))}
                    </select>
                </div>

                {/* Company Name */}
                <div>
                    <label className="block text-sm font-medium mb-2">Company Name</label>
                    <input
                        type="text"
                        className="w-full bg-black/30 border border-gray-600 rounded-lg p-2 text-white placeholder-gray-500 focus:border-purple-400 focus:outline-none text-sm"
                        placeholder={scriptLanguage === 'hi' ? 'जैसे, TechCorp' : 'e.g., TechCorp'}
                        value={companyName}
                        onChange={(e) => setCompanyName(e.target.value)}
                    />
                </div>

                {/* Business Category */}
                <div>
                    <label className="block text-sm font-medium mb-2">Business Category</label>
                    <select
                        className="w-full bg-black/30 border border-gray-600 rounded-lg p-2 text-white focus:border-purple-400 focus:outline-none text-sm"
                        value={category}
                        onChange={(e) => setCategory(e.target.value)}
                    >
                        {BUSINESS_CATEGORIES.map(cat => (
                            <option key={cat.id} value={cat.id}>{cat.name}</option>
                        ))}
                    </select>
                </div>

                {/* Tone Presets - Compact */}
                <div>
                    <label className="block text-sm font-medium mb-2">Marketing Tone</label>
                    <div className="grid grid-cols-4 gap-2">
                        {TONE_PRESETS.map(preset => (
                            <motion.button
                                key={preset.id}
                                className={`p-2 rounded-lg border transition-all text-center ${tone === preset.id
                                    ? 'bg-gradient-to-br from-purple-600/20 to-pink-600/20 border-purple-500'
                                    : 'border-gray-700 hover:border-gray-500'
                                    }`}
                                onClick={() => setTone(preset.id)}
                                whileHover={{ scale: 1.02 }}
                                whileTap={{ scale: 0.98 }}
                                title={preset.desc}
                            >
                                <div className="text-xl">{preset.emoji}</div>
                                <div className="text-xs font-semibold mt-1">{preset.name}</div>
                            </motion.button>
                        ))}
                    </div>
                </div>

                {/* Generate Button */}
                <button
                    className={`w-full btn-primary py-3 flex items-center justify-center gap-2 ${isGenerating ? 'opacity-50 cursor-not-allowed' : ''}`}
                    onClick={generateScript}
                    disabled={isGenerating}
                >
                    {isGenerating ? (
                        <>
                            <Loader2 className="w-5 h-5 animate-spin" />
                            {scriptLanguage === 'hi' ? 'बनाया जा रहा है...' : 'Generating...'}
                        </>
                    ) : (
                        <>
                            <Wand2 className="w-5 h-5" />
                            {scriptLanguage === 'hi' ? 'स्क्रिप्ट बनाएं' : 'Generate Script'}
                        </>
                    )}
                </button>

                {/* Generated Script Preview */}
                {generatedScript && (
                    <motion.div
                        className="mt-4 p-4 bg-gradient-to-br from-purple-900/20 to-pink-900/20 rounded-lg border border-purple-500/30"
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                    >
                        <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-semibold text-purple-300">
                                {scriptLanguage === 'hi' ? 'स्क्रिप्ट:' : 'Generated Script:'}
                            </span>
                            <button
                                onClick={copyToClipboard}
                                className="text-xs px-3 py-1 rounded-md bg-purple-600/20 hover:bg-purple-600/30 flex items-center gap-1"
                            >
                                {copied ? (
                                    <>
                                        <CheckCircle className="w-3 h-3" />
                                        {scriptLanguage === 'hi' ? 'कॉपी!' : 'Copied!'}
                                    </>
                                ) : (
                                    <>
                                        <Copy className="w-3 h-3" />
                                        {scriptLanguage === 'hi' ? 'कॉपी' : 'Copy'}
                                    </>
                                )}
                            </button>
                        </div>
                        <textarea
                            className="w-full bg-black/20 border border-purple-500/20 rounded-lg p-3 text-white text-sm min-h-[250px] focus:outline-none"
                            value={generatedScript}
                            onChange={(e) => setGeneratedScript(e.target.value)}
                        />
                        <button
                            onClick={useScript}
                            className="w-full mt-3 py-2 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg font-semibold hover:from-purple-700 hover:to-pink-700 transition-all"
                        >
                            {scriptLanguage === 'hi' ? 'इस्तेमाल करें →' : 'Use This Script →'}
                        </button>
                    </motion.div>
                )}
            </div>
        </div>
    );
}
