'use client'

import { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Upload, X, Image as ImageIcon } from 'lucide-react';

interface BrandAssetsProps {
    onLogoChange: (logo: File | null) => void;
    onPhotosChange: (photos: File[]) => void;
}

export default function BrandAssets({ onLogoChange, onPhotosChange }: BrandAssetsProps) {
    const [logo, setLogo] = useState<File | null>(null);
    const [logoPreview, setLogoPreview] = useState<string | null>(null);
    const [photos, setPhotos] = useState<File[]>([]);
    const [photoPreviews, setPhotoPreviews] = useState<string[]>([]);

    const handleLogoUpload = useCallback((file: File) => {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file');
            return;
        }

        setLogo(file);
        setLogoPreview(URL.createObjectURL(file));
        onLogoChange(file);
    }, [onLogoChange]);

    const removeLogo = () => {
        setLogo(null);
        setLogoPreview(null);
        onLogoChange(null);
    };

    const handlePhotosUpload = useCallback((files: FileList) => {
        const imageFiles = Array.from(files).filter(f => f.type.startsWith('image/'));

        if (imageFiles.length === 0) {
            alert('Please upload image files');
            return;
        }

        const newPhotos = [...photos, ...imageFiles].slice(0, 5); // Max 5 photos
        const newPreviews = newPhotos.map(f => URL.createObjectURL(f));

        setPhotos(newPhotos);
        setPhotoPreviews(newPreviews);
        onPhotosChange(newPhotos);
    }, [photos, onPhotosChange]);

    const removePhoto = (index: number) => {
        const newPhotos = photos.filter((_, i) => i !== index);
        const newPreviews = photoPreviews.filter((_, i) => i !== index);

        setPhotos(newPhotos);
        setPhotoPreviews(newPreviews);
        onPhotosChange(newPhotos);
    };

    return (
        <div className="glass-dark p-6 rounded-2xl">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                <ImageIcon className="w-6 h-6 text-pink-400" />
                Brand Assets
            </h2>

            <div className="space-y-6">
                {/* Logo Upload */}
                <div>
                    <label className="block text-sm font-medium mb-2">
                        Company Logo
                    </label>

                    {logoPreview ? (
                        <div className="relative group">
                            <img
                                src={logoPreview}
                                alt="Logo preview"
                                className="max-h-32 mx-auto rounded-lg border-2 border-pink-500/30 bg-black/20 p-4"
                            />
                            <button
                                onClick={removeLogo}
                                className="absolute top-2 right-2 p-1 bg-red-500 rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
                            >
                                <X className="w-4 h-4" />
                            </button>
                        </div>
                    ) : (
                        <div
                            className="border-2 border-dashed border-gray-600 rounded-xl p-8 text-center hover:border-pink-400 transition-colors cursor-pointer"
                            onClick={() => document.getElementById('logo-upload')?.click()}
                        >
                            <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                            <p className="text-sm text-gray-300">Click to upload logo</p>
                            <p className="text-xs text-gray-500 mt-1">PNG, JPG, or SVG recommended</p>
                            <input
                                id="logo-upload"
                                type="file"
                                accept="image/*"
                                className="hidden"
                                onChange={(e) => {
                                    const file = e.target.files?.[0];
                                    if (file) handleLogoUpload(file);
                                }}
                            />
                        </div>
                    )}
                </div>

                {/* Business Photos */}
                <div>
                    <label className="block text-sm font-medium mb-2">
                        Business Photos (Optional, up to 5)
                    </label>
                    <p className="text-xs text-gray-500 mb-3">
                        Upload photos of your products, office, or team to enhance the video
                    </p>

                    <div className="grid grid-cols-3 gap-3 mb-3">
                        {photoPreviews.map((preview, index) => (
                            <motion.div
                                key={index}
                                className="relative group aspect-square"
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                            >
                                <img
                                    src={preview}
                                    alt={`Photo ${index + 1}`}
                                    className="w-full h-full object-cover rounded-lg border border-gray-600"
                                />
                                <button
                                    onClick={() => removePhoto(index)}
                                    className="absolute top-1 right-1 p-1 bg-red-500 rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
                                >
                                    <X className="w-3 h-3" />
                                </button>
                            </motion.div>
                        ))}
                    </div>

                    {photos.length < 5 && (
                        <div
                            className="border-2 border-dashed border-gray-600 rounded-lg p-6 text-center hover:border-pink-400 transition-colors cursor-pointer"
                            onClick={() => document.getElementById('photos-upload')?.click()}
                        >
                            <Upload className="w-6 h-6 text-gray-400 mx-auto mb-2" />
                            <p className="text-sm text-gray-300">
                                {photos.length === 0 ? 'Upload business photos' : 'Add more photos'}
                            </p>
                            <p className="text-xs text-gray-500 mt-1">
                                {5 - photos.length} slots remaining
                            </p>
                            <input
                                id="photos-upload"
                                type="file"
                                accept="image/*"
                                multiple
                                className="hidden"
                                onChange={(e) => {
                                    const files = e.target.files;
                                    if (files) handlePhotosUpload(files);
                                }}
                            />
                        </div>
                    )}
                </div>

                {/* Info Box */}
                <div className="text-xs text-gray-500 p-3 bg-black/10 rounded-lg border border-gray-700">
                    <strong>Tip:</strong> Your logo and photos will be used to create a consistent brand identity in your anime marketing video.
                </div>
            </div>
        </div>
    );
}
