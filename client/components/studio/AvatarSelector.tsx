import { useState } from 'react';
import { motion } from 'framer-motion';
import { Wand2, Loader2, RefreshCw } from 'lucide-react';

interface AvatarSelectorProps {
    selectedAvatarId: string | null;
    onSelect: (avatarId: string) => void;
    onGenerate: (prompt: string, style: string) => Promise<string>; // Returns generated avatar URL
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function AvatarSelector({ selectedAvatarId, onSelect, onGenerate }: AvatarSelectorProps) {
    // Simplified: Always show generation form (no gallery)
    const [prompt, setPrompt] = useState('');
    const [style, setStyle] = useState('anime');
    const [isGenerating, setIsGenerating] = useState(false);
    const [generatedAvatar, setGeneratedAvatar] = useState<string | null>(null);

    const handleGenerateClick = async () => {
        if (!prompt.trim()) return;

        setIsGenerating(true);
        try {
            const url = await onGenerate(prompt, style);
            setGeneratedAvatar(url);
        } catch (error) {
            console.error('Avatar generation failed:', error);
        } finally {
            setIsGenerating(false);
        }
    };

    return (
        <div className="glass-dark p-6 rounded-2xl">
            {/* Title - No Tabs */}
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                <span className="text-2xl">👤</span>
                Generate Anime Avatar
            </h2>

            {/* Generation Form - Always Visible */}
            <div className="space-y-4">
                <div>
                    <label className="block text-sm font-medium mb-2">Style</label>
                    <div className="grid grid-cols-2 gap-2">
                        {['anime', 'cartoon'].map((s) => (
                            <button
                                key={s}
                                className={`py-2 rounded-lg text-sm capitalize border transition-all ${style === s
                                    ? 'bg-pink-600/20 border-pink-500 text-pink-300'
                                    : 'border-gray-700 hover:border-gray-500 text-gray-400'
                                    }`}
                                onClick={() => setStyle(s)}
                            >
                                {s}
                            </button>
                        ))}
                    </div>
                </div>

                <div>
                    <label className="block text-sm font-medium mb-2">Description</label>
                    <textarea
                        className="w-full bg-black/30 border border-gray-600 rounded-lg p-3 text-sm text-white placeholder-gray-500 focus:border-pink-500 focus:outline-none min-h-[100px]"
                        placeholder="e.g., Professional businessman in suit, friendly smile..."
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                    />
                </div>

                <button
                    className={`w-full btn-primary py-3 flex items-center justify-center gap-2 ${isGenerating || !prompt.trim() ? 'opacity-50 cursor-not-allowed' : ''
                        }`}
                    onClick={handleGenerateClick}
                    disabled={isGenerating || !prompt.trim()}
                >
                    {isGenerating ? (
                        <>
                            <Loader2 className="w-4 h-4 animate-spin" />
                            Generating...
                        </>
                    ) : (
                        <>
                            <Wand2 className="w-4 h-4" />
                            Generate Avatar
                        </>
                    )}
                </button>

                {generatedAvatar && (
                    <div className="mt-4">
                        <div className="text-sm text-green-400 mb-2 flex items-center gap-2">
                            <RefreshCw className="w-3 h-3" />
                            Generated Successfully
                        </div>
                        <img
                            src={generatedAvatar}
                            alt="Generated Avatar"
                            className="w-full rounded-lg border border-gray-600"
                        />
                    </div>
                )}
            </div>
        </div>
    );
}
