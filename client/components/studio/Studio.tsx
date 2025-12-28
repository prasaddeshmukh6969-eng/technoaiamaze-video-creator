'use client'

import { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import { Loader2, Download, AlertCircle, Volume2, Play, Sliders, Upload } from 'lucide-react';
import AvatarSelector from './AvatarSelector';
import ScriptGenerator from './ScriptGenerator';
import LanguageSelector from './LanguageSelector';
import BrandAssets from './BrandAssets';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const VOICE_ARCHETYPES = [
    { id: 'philosopher', voice: 'en-US-GuyNeural', name: 'The Philosopher', description: 'Deep male voice', icon: '🎓' },
    { id: 'storyteller', voice: 'hi-IN-MadhurNeural', name: 'The Storyteller', description: 'Hindi/English', icon: '📖' },
    { id: 'innovator', voice: 'en-US-AriaNeural', name: 'The Innovator', description: 'Energetic female', icon: '⚡' },
    { id: 'professional_male', voice: 'en-GB-RyanNeural', name: 'Professional Male', description: 'British accent', icon: '🎙️' },
    { id: 'professional_female', voice: 'en-GB-SoniaNeural', name: 'Professional Female', description: 'British accent', icon: '🎤' },
    { id: 'indian_english', voice: 'en-IN-NeerjaNeural', name: 'Indian English', description: 'Female voice', icon: '🇮🇳' },
];

interface JobStatus {
    job_id: string;
    status: 'pending' | 'processing' | 'completed' | 'failed';
    progress?: number;
    message?: string;
    result_url?: string;
    error?: string;
}

export default function Studio() {
    const [image, setImage] = useState<File | null>(null);
    const [imagePreview, setImagePreview] = useState<string | null>(null);
    const [text, setText] = useState('');
    const [selectedArchetype, setSelectedArchetype] = useState('philosopher');
    const [poseIntensity, setPoseIntensity] = useState(1.0);
    const [enhance, setEnhance] = useState(true);

    // Marketing Platform State
    const [outputLanguage, setOutputLanguage] = useState('en');
    const [autoSelectVoice, setAutoSelectVoice] = useState(true);
    const [logo, setLogo] = useState<File | null>(null);
    const [businessPhotos, setBusinessPhotos] = useState<File[]>([]);
    const [playingVoice, setPlayingVoice] = useState<string | null>(null);
    const audioRef = useRef<HTMLAudioElement | null>(null);

    const [jobId, setJobId] = useState<string | null>(null);
    const [jobStatus, setJobStatus] = useState<JobStatus | null>(null);
    const [isGenerating, setIsGenerating] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fileInputRef = useRef<HTMLInputElement>(null);
    const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

    const handleVoicePreview = async (voice: string) => {
        try {
            if (audioRef.current) {
                audioRef.current.pause();
                audioRef.current.currentTime = 0;
                audioRef.current = null;
            }

            if (playingVoice === voice) {
                setPlayingVoice(null);
                return;
            }

            setPlayingVoice(voice);

            const audio = new Audio();
            audio.preload = 'auto';
            audio.src = `${API_URL}/api/v1/voices/preview/${voice}`;

            audio.onended = () => setPlayingVoice(null);
            audio.onerror = (e) => {
                console.error('Voice preview failed:', e);
                setPlayingVoice(null);
                setError('Failed to play voice preview. Please try again.');
                setTimeout(() => setError(null), 3000);
            };

            audioRef.current = audio;

            audio.oncanplaythrough = async () => {
                try {
                    await audio.play();
                } catch (playError: any) {
                    console.error('Audio play error:', playError);
                    setPlayingVoice(null);
                    if (playError.name === 'NotAllowedError') {
                        setError('Please click the preview button again to play audio.');
                    } else {
                        setError('Could not play audio. Please try again.');
                    }
                    setTimeout(() => setError(null), 3000);
                }
            };

            audio.load();

        } catch (error) {
            console.error('Voice preview error:', error);
            setPlayingVoice(null);
            setError('Voice preview failed. Please try again.');
            setTimeout(() => setError(null), 3000);
        }
    };

    const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            setImage(file);
            const reader = new FileReader();
            reader.onloadend = () => {
                setImagePreview(reader.result as string);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleAvatarGenerated = async (prompt: string, style: string): Promise<string> => {
        try {
            const formData = new FormData();
            formData.append('prompt', prompt);
            formData.append('style', style);

            const response = await axios.post(`${API_URL}/api/v1/avatars/generate`, formData);
            const avatarUrl = response.data.url;

            const avatarResponse = await fetch(avatarUrl);
            const blob = await avatarResponse.blob();
            const file = new File([blob], 'generated-avatar.png', { type: 'image/png' });

            setImage(file);
            setImagePreview(avatarUrl);

            return avatarUrl;
        } catch (error) {
            console.error('Avatar generation failed:', error);
            throw error;
        }
    };

    const handleGenerate = async () => {
        if (!image) {
            setError('Please upload or generate an avatar image');
            return;
        }
        if (!text.trim()) {
            setError('Please enter a script');
            return;
        }

        try {
            setError(null);
            setIsGenerating(true);
            setJobStatus(null);

            const archetype = VOICE_ARCHETYPES.find(a => a.id === selectedArchetype);

            const formData = new FormData();
            formData.append('image', image);
            formData.append('text', text);
            formData.append('archetype', archetype?.voice || 'en-US-GuyNeural');
            formData.append('pose_intensity', poseIntensity.toString());
            formData.append('enhance', enhance.toString());
            if (outputLanguage !== 'en') {
                formData.append('language', outputLanguage);
            }

            const response = await axios.post(`${API_URL}/api/v1/generate`, formData);
            const { job_id } = response.data;

            setJobId(job_id);
            startPolling(job_id);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to start video generation');
            setIsGenerating(false);
        }
    };

    const startPolling = (jobId: string) => {
        if (pollIntervalRef.current) {
            clearInterval(pollIntervalRef.current);
        }

        pollIntervalRef.current = setInterval(async () => {
            try {
                const response = await axios.get(`${API_URL}/api/v1/status/${jobId}`);
                const status: JobStatus = response.data;

                setJobStatus(status);

                if (status.status === 'completed' || status.status === 'failed') {
                    clearInterval(pollIntervalRef.current!);
                    setIsGenerating(false);
                }
            } catch (err) {
                console.error('Status poll failed:', err);
            }
        }, 2000);
    };

    const handleDownload = () => {
        if (jobStatus?.result_url) {
            window.open(jobStatus.result_url, '_blank');
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 p-4">
            {/* Full-Screen 3-Column Layout */}
            <div className="grid grid-cols-12 gap-4 max-w-[2000px] mx-auto">

                {/* Left Column - Brand & Avatar (3 cols) */}
                <div className="col-span-12 lg:col-span-3 space-y-4">
                    <BrandAssets
                        onLogoChange={(file) => setLogo(file)}
                        onPhotosChange={(files) => setBusinessPhotos(files)}
                    />

                    <AvatarSelector
                        selectedAvatarId={imagePreview}
                        onSelect={(id) => { }}
                        onGenerate={handleAvatarGenerated}
                    />
                </div>

                {/* Center Column - Script & Settings (5 cols) */}
                <div className="col-span-12 lg:col-span-5 space-y-4">
                    <ScriptGenerator onUseScript={(script) => setText(script)} />

                    {/* Script Input */}
                    <motion.div
                        className="glass-dark p-4 rounded-2xl"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                    >
                        <h2 className="text-xl font-bold mb-3 flex items-center gap-2">
                            <Upload className="w-5 h-5 text-cyan-400" />
                            Marketing Script
                        </h2>
                        <textarea
                            className="w-full bg-black/30 border border-gray-600 rounded-lg p-3 text-white placeholder-gray-500 focus:border-purple-400 focu s:outline-none min-h-[120px] text-sm"
                            placeholder="Enter your marketing script..."
                            value={text}
                            onChange={(e) => setText(e.target.value)}
                            maxLength={500}
                        />
                        <div className="text-right text-xs text-gray-500 mt-1">
                            {text.length} / 500
                        </div>
                    </motion.div>

                    {/* Voice & Language - Compact */}
                    <div className="grid grid-cols-2 gap-4">
                        {/* Voice Selection - Compact Grid */}
                        <motion.div
                            className="glass-dark p-4 rounded-2xl col-span-2"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                        >
                            <h2 className="text-lg font-bold mb-3 flex items-center gap-2">
                                <Volume2 className="w-5 h-5 text-cyan-400" />
                                Voice
                            </h2>
                            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                                {VOICE_ARCHETYPES.map((archetype) => (
                                    <motion.div
                                        key={archetype.id}
                                        className={`p-2 rounded-lg border cursor-pointer transition-all ${selectedArchetype === archetype.id
                                            ? 'border-cyan-500 bg-cyan-500/10'
                                            : 'border-gray-600 hover:border-gray-500'
                                            }`}
                                        onClick={() => setSelectedArchetype(archetype.id)}
                                        whileHover={{ scale: 1.02 }}
                                        whileTap={{ scale: 0.98 }}
                                    >
                                        <div className="flex items-center justify-between">
                                            <div className="flex-1">
                                                <div className="flex items-center gap-1 mb-0.5">
                                                    <span className="text-lg">{archetype.icon}</span>
                                                    <span className="font-bold text-xs">{archetype.name}</span>
                                                </div>
                                                <div className="text-[10px] text-gray-400 truncate">{archetype.description}</div>
                                            </div>
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    handleVoicePreview(archetype.voice);
                                                }}
                                                className={`ml-1 p-1.5 rounded transition-all ${playingVoice === archetype.voice
                                                        ? 'bg-cyan-600'
                                                        : 'bg-gray-700 hover:bg-gray-600'
                                                    }`}
                                                title="Preview"
                                            >
                                                {playingVoice === archetype.voice ? (
                                                    <Loader2 className="w-3 h-3 animate-spin" />
                                                ) : (
                                                    <Play className="w-3 h-3" />
                                                )}
                                            </button>
                                        </div>
                                    </motion.div>
                                ))}
                            </div>
                        </motion.div>

                        {/* Language Selector */}
                        <div className="col-span-2">
                            <LanguageSelector
                                onLanguageChange={(lang, autoVoice) => {
                                    setOutputLanguage(lang);
                                    setAutoSelectVoice(autoVoice);
                                }}
                            />
                        </div>
                    </div>

                    {/* Advanced Settings - Compact */}
                    <motion.div
                        className="glass-dark p-4 rounded-2xl"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                    >
                        <h2 className="text-lg font-bold mb-3 flex items-center gap-2">
                            <Sliders className="w-5 h-5 text-cyan-400" />
                            Advanced
                        </h2>
                        <div className="space-y-3">
                            <div>
                                <label className="block text-xs font-medium mb-1">
                                    Head Movement: {poseIntensity.toFixed(1)}x
                                </label>
                                <input
                                    type="range"
                                    min="0"
                                    max="1.5"
                                    step="0.1"
                                    value={poseIntensity}
                                    onChange={(e) => setPoseIntensity(parseFloat(e.target.value))}
                                    className="w-full"
                                />
                                <div className="flex justify-between text-[10px] text-gray-500 mt-0.5">
                                    <span>Static</span>
                                    <span>Natural</span>
                                    <span>Dynamic</span>
                                </div>
                            </div>
                            <div className="flex items-center justify-between">
                                <div>
                                    <div className="font-medium text-sm">GFPGAN Enhancement</div>
                                    <div className="text-xs text-gray-400">AI face restoration</div>
                                </div>
                                <label className="relative inline-flex items-center cursor-pointer">
                                    <input
                                        type="checkbox"
                                        checked={enhance}
                                        onChange={(e) => setEnhance(e.target.checked)}
                                        className="sr-only peer"
                                    />
                                    <div className="w-9 h-5 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-gradient-to-r peer-checked:from-purple-600 peer-checked:to-pink-600"></div>
                                </label>
                            </div>
                        </div>
                    </motion.div>
                </div>

                {/* Right Column - Preview & Generation (4 cols) */}
                <div className="col-span-12 lg:col-span-4 space-y-4">
                    {/* Image Preview */}
                    <motion.div
                        className="glass-dark p-4 rounded-2xl"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                    >
                        <h2 className="text-lg font-bold mb-3">Avatar Preview</h2>
                        {imagePreview ? (
                            <div className="relative">
                                <img
                                    src={imagePreview}
                                    alt="Avatar"
                                    className="w-full rounded-lg"
                                />
                                <button
                                    onClick={() => {
                                        setImage(null);
                                        setImagePreview(null);
                                    }}
                                    className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded text-xs"
                                >
                                    Remove
                                </button>
                            </div>
                        ) : (
                            <div className="border-2 border-dashed border-gray-600 rounded-lg p-8 text-center">
                                <Upload className="w-12 h-12 mx-auto mb-3 text-gray-500" />
                                <p className="text-sm text-gray-400 mb-3">Upload or generate avatar</p>
                                <input
                                    ref={fileInputRef}
                                    type="file"
                                    accept="image/*"
                                    onChange={handleImageChange}
                                    className="hidden"
                                />
                                <button
                                    onClick={() => fileInputRef.current?.click()}
                                    className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg text-sm"
                                >
                                    Upload Image
                                </button>
                            </div>
                        )}
                    </motion.div>

                    {/* Generate Button */}
                    <motion.button
                        className={`w-full py-4 rounded-xl font-bold text-lg transition-all ${isGenerating || !image || !text.trim()
                                ? 'bg-gray-700 cursor-not-allowed opacity-50'
                                : 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 shadow-lg hover:shadow-xl'
                            }`}
                        onClick={handleGenerate}
                        disabled={isGenerating || !image || !text.trim()}
                        whileHover={{ scale: isGenerating ? 1 : 1.02 }}
                        whileTap={{ scale: isGenerating ? 1 : 0.98 }}
                    >
                        {isGenerating ? (
                            <span className="flex items-center justify-center gap-2">
                                <Loader2 className="w-5 h-5 animate-spin" />
                                Generating Video...
                            </span>
                        ) : (
                            'Generate Video'
                        )}
                    </motion.button>

                    {/* Error Message */}
                    {error && (
                        <motion.div
                            className="bg-red-500/10 border border-red-500 rounded-lg p-3"
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                        >
                            <div className="flex items-center gap-2 text-red-400">
                                <AlertCircle className="w-4 h-4" />
                                <span className="text-sm">{error}</span>
                            </div>
                        </motion.div>
                    )}

                    {/* Progress */}
                    {jobStatus && (
                        <motion.div
                            className="glass-dark p-4 rounded-xl"
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                        >
                            <div className="space-y-3">
                                <div className="flex items-center justify-between">
                                    <span className="text-sm font-medium">
                                        {jobStatus.status === 'completed' ? 'Complete!' : 'Processing...'}
                                    </span>
                                    <span className="text-sm text-gray-400">{jobStatus.progress}%</span>
                                </div>

                                <div className="w-full bg-gray-700 rounded-full h-2">
                                    <div
                                        className="bg-gradient-to-r from-purple-600 to-pink-600 h-2 rounded-full transition-all duration-300"
                                        style={{ width: `${jobStatus.progress}%` }}
                                    />
                                </div>

                                <p className="text-xs text-gray-400">{jobStatus.message}</p>

                                {jobStatus.status === 'completed' && jobStatus.result_url && (
                                    <button
                                        onClick={handleDownload}
                                        className="w-full py-2 bg-green-600 hover:bg-green-700 rounded-lg flex items-center justify-center gap-2 text-sm font-medium"
                                    >
                                        <Download className="w-4 h-4" />
                                        Download Video
                                    </button>
                                )}

                                {jobStatus.status === 'failed' && (
                                    <div className="text-red-400 text-xs">
                                        {jobStatus.error || 'Generation failed'}
                                    </div>
                                )}
                            </div>
                        </motion.div>
                    )}
                </div>
            </div>
        </div>
    );
}
