"""
Antigravity AI - Animation Engine
Integrates SadTalker via Hugging Face Spaces for 100% FREE video generation
"""
import logging
import asyncio
from typing import Dict, Optional
from pathlib import Path

from core.config import settings
from engines.sadtalker_wrapper import sadtalker_engine

logger = logging.getLogger(__name__)


class Animator:
    """
    Animation Engine Wrapper
    
    Delegates to SadTalkerEngine for actual video generation.
    Supports both real photos and anime avatars.
    """
    
    def __init__(self):
        self.engine = sadtalker_engine
        logger.info("Animator initialized with SadTalker Engine")
    
    async def generate_animation(
        self,
        image_path: str,
        audio_path: str,
        output_path: str,
        pose_intensity: float = 1.0,
        fps: int = 25,
        options: Optional[Dict] = None
    ) -> Dict:
        """
        Generate animated video from portrait + audio
        
        Args:
            image_path: Static portrait image
            audio_path: Audio file
            output_path: Output video path
            pose_intensity: Maps to SadTalker pose_style (0.0-1.5 -> 0-45)
            fps: Frames per second (fixed by SadTalker usually)
            options: Additional options (e.g. mode="anime")
        
        Returns:
            dict with video_path, duration, frame_count
        """
        # Map pose_intensity (0.0-1.5) to SadTalker pose_style (0-45)
        # 0.0 -> 0 (Static)
        # 1.0 -> 20 (Natural)
        # 1.5 -> 45 (Dynamic)
        pose_style = int(min(pose_intensity * 20, 45))
        
        # Check if anime mode
        options = options or {}
        is_anime = options.get("mode") == "anime"
        
        if is_anime:
            logger.info("Using Anime mode for animation")
            return await self.engine.animate_anime_character(
                image_path=image_path,
                audio_path=audio_path,
                output_path=output_path,
                style=options.get("style", "anime")
            )
        else:
            logger.info(f"Using Real mode for animation (pose_style={pose_style})")
            return await self.engine.generate_video(
                image_path=image_path,
                audio_path=audio_path,
                output_path=output_path,
                options={"mode": "normal"}
            )
    
    def clear_gpu_memory(self):
        """No-op for API-based engine"""
        pass


# Global instance
animator = Animator()
