"""
Antigravity AI - Animation Engine
Supports multiple engines: HeyGen (production), LivePortrait (free/unreliable), SadTalker (local)
"""
import logging
import asyncio
from typing import Dict, Optional
from pathlib import Path

from core.config import settings

logger = logging.getLogger(__name__)


class Animator:
    """
    Multi-Engine Animation Wrapper
    
    Supports:
    - HeyGen API (recommended): Reliable, paid, production-ready
    - LivePortrait (fallback): Free, unreliable, HuggingFace Spaces
    - SadTalker (future): Local inference, requires GPU
    """
    
    def __init__(self):
        self.engine_name = settings.ANIMATION_ENGINE
        self.primary_engine = None
        self.fallback_engine = None
        
        # Initialize engines based on configuration
        self._initialize_engines()
    
    def _initialize_engines(self):
        """Initialize animation engines based on configuration"""
        
        if self.engine_name == "heygen":
            try:
                from engines.heygen_wrapper import heygen_engine
                self.primary_engine = heygen_engine
                logger.info("✅ Primary engine: HeyGen API")
                
                # Fallback to LivePortrait if HeyGen fails
                from engines.sadtalker_wrapper import sadtalker_engine
                self.fallback_engine = sadtalker_engine
                logger.info("  Fallback engine: LivePortrait (HuggingFace)")
                
            except ImportError as e:
                logger.error(f"Failed to load HeyGen engine: {e}")
                self.engine_name = "liveportrait"
        
        if self.engine_name == "liveportrait":
            from engines.sadtalker_wrapper import sadtalker_engine
            self.primary_engine = sadtalker_engine
            logger.info("✅ Primary engine: LivePortrait (HuggingFace)")
            logger.warning("⚠️ LivePortrait is unreliable. Consider using HeyGen for production.")
    
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
            pose_intensity: Animation intensity (0.0-1.5)
            fps: Frames per second
            options: Additional options (e.g. mode="anime")
        
        Returns:
            dict with video_path, status, source, and metadata
        """
        options = options or {}
        is_anime = options.get("mode") == "anime"
        
        logger.info(f"🎬 Animation request: engine={self.engine_name}, anime={is_anime}")
        
        # Try primary engine
        try:
            if is_anime and hasattr(self.primary_engine, 'animate_anime_character'):
                logger.info("Using anime animation mode")
                result = await self.primary_engine.animate_anime_character(
                    image_path=image_path,
                    audio_path=audio_path,
                    output_path=output_path,
                    style=options.get("style", "anime")
                )
            else:
                logger.info("Using standard animation mode")
                result = await self.primary_engine.generate_video(
                    image_path=image_path,
                    audio_path=audio_path,
                    output_path=output_path,
                    options=options
                )
            
            # Check if primary engine succeeded
            if result.get("status") == "success":
                logger.info(f"✅ {self.engine_name} animation successful")
                return result
            
            # Primary engine returned graceful failure
            logger.warning(f"⚠️ {self.engine_name} returned: {result.get('status')}")
            
            # Try fallback if available
            if self.fallback_engine:
                logger.info("Attempting fallback engine...")
                return await self._try_fallback(image_path, audio_path, output_path, options)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ {self.engine_name} failed: {str(e)}")
            
            # Try fallback
            if self.fallback_engine:
                logger.info("Attempting fallback engine...")
                return await self._try_fallback(image_path, audio_path, output_path, options)
            
            # No fallback available
            return {
                "video_path": None,
                "status": "failed",
                "source": self.engine_name,
                "error": str(e)
            }
    
    async def _try_fallback(
        self,
        image_path: str,
        audio_path: str,
        output_path: str,
        options: Dict
    ) -> Dict:
        """Try fallback engine"""
        try:
            is_anime = options.get("mode") == "anime"
            
            if is_anime and hasattr(self.fallback_engine, 'animate_anime_character'):
                result = await self.fallback_engine.animate_anime_character(
                    image_path=image_path,
                    audio_path=audio_path,
                    output_path=output_path,
                    style=options.get("style", "anime")
                )
            else:
                result = await self.fallback_engine.generate_video(
                    image_path=image_path,
                    audio_path=audio_path,
                    output_path=output_path,
                    options=options
                )
            
            if result.get("status") == "success":
                logger.info("✅ Fallback engine successful")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Fallback engine also failed: {str(e)}")
            return {
                "video_path": None,
                "status": "failed",
                "source": "all_engines_failed",
                "error": f"Primary and fallback engines failed. Last error: {str(e)}"
            }
    
    def clear_gpu_memory(self):
        """Clear GPU memory (no-op for API-based engines)"""
        pass


# Global instance
animator = Animator()

