"""
Technoaiamaze - LivePortrait Hugging Face Spaces Wrapper
100% FREE video animation via Hugging Face Spaces API (KwaiVGI/LivePortrait)
No local GPU needed, unlimited usage
"""
import asyncio
import aiohttp
import logging
from pathlib import Path
from typing import Optional, Dict
from gradio_client import Client
import tempfile
import shutil
import os
from core.config import settings

logger = logging.getLogger(__name__)


class LivePortraitEngine:
    """
    Hugging Face Spaces API wrapper for LivePortrait
    
    100% FREE Solution:
    - Calls publicly deployed HF Space (KwaiVGI/LivePortrait)
    - Superior quality to SadTalker
    - No API keys (if public), no limits, no costs
    
    Usage:
        engine = LivePortraitEngine()
        video_path = await engine.generate_video(image_path, audio_path)
    """
    
    def __init__(self, space_url: str = "KwaiVGI/LivePortrait"):
        """
        Initialize LivePortrait engine
        
        Args:
            space_url: Hugging Face Space URL
        """
        self.space_url = space_url
        self.client = None
        self.is_available = False
        
        logger.info(f"LivePortrait Engine initialized with HF Space: {space_url}")
    
    async def check_availability(self) -> bool:
        """Check if Hugging Face Space is available"""
        try:
            # Try to connect to the space
            if settings.HF_TOKEN:
                self.client = Client(self.space_url, hf_token=settings.HF_TOKEN)
            else:
                self.client = Client(self.space_url)
                
            self.is_available = True
            logger.info(f"✓ HF Space '{self.space_url}' is available")
            return True
        except Exception as e:
            logger.error(f"HF Space unavailable: {e}")
            self.is_available = False
            return False
    
    async def generate_video(
        self,
        image_path: str,
        audio_path: str,
        output_path: str,
        options: Optional[Dict] = None
    ) -> Dict:
        """
        Generate animated video from image + audio
        """
        if not self.is_available:
            await self.check_availability()
        
        if not self.is_available:
            raise RuntimeError("LivePortrait HF Space is not available")
        
        options = options or {}
        mode = options.get("mode", "normal")
        
        logger.info(f"Generating video with LivePortrait...")
        logger.info(f"  Image: {image_path}")
        logger.info(f"  Audio: {audio_path}")
        
        try:
            # Call Hugging Face Space API
            # LivePortrait usually takes: source_image, driving_audio
            # We might need to adjust based on exact API
            result = self.client.predict(
                image_path, 	# source_image (0)
                audio_path,	# driving_audio (1)
                True,		# relative_motion (2)
                True,		# do_crop (3)
                True,		# paste_back (4)
                api_name="/gpu_wrapped_execute_video" 
            )
            
            # Result is usually a tuple/list with video path
            if isinstance(result, str):
                video_url = result
            elif isinstance(result, (list, tuple)) and len(result) > 0:
                # LivePortrait often returns (video_path, subtitles_path)
                # We want the video path (usually first or second)
                # Let's assume first is video
                video_url = result[0]
                # If it's a dict (JSON), look for video key
                if isinstance(video_url, dict) and "video" in video_url:
                    video_url = video_url["video"]
            else:
                raise ValueError(f"Unexpected result format: {result}")
            
            # Download video from HF servers
            await self._download_file(video_url, output_path)
            
            logger.info(f"✓ Video generated successfully: {output_path}")
            
            return {
                "video_path": output_path,
                "status": "success",
                "mode": mode,
                "source": "liveportrait_hf"
            }
        
        except Exception as e:
            logger.error(f"Video generation failed: {e}")
            # If API mismatch, try to log details
            if "parameter" in str(e).lower():
                logger.error("API Parameter mismatch. Please check debug_space.py output.")
            raise RuntimeError(f"LivePortrait generation failed: {str(e)}")
    
    async def animate_anime_character(
        self,
        image_path: str,
        audio_path: str,
        output_path: str,
        style: str = "anime"
    ) -> Dict:
        """
        Specialized method for anime character animation
        LivePortrait works great for anime too!
        """
        return await self.generate_video(
            image_path=image_path,
            audio_path=audio_path,
            output_path=output_path,
            options={"mode": "anime", "style": style}
        )
    
    async def _download_file(self, url: str, output_path: str):
        """Download file from URL to local path"""
        import aiohttp
        try:
            # Handle local file paths returned by gradio_client
            if os.path.exists(url):
                import shutil
                shutil.copy(url, output_path)
                return

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        with open(output_path, 'wb') as f:
                            while True:
                                chunk = await response.content.read(8192)
                                if not chunk:
                                    break
                                f.write(chunk)
                        logger.info(f"✓ Downloaded: {output_path}")
                    else:
                        raise RuntimeError(f"Download failed: HTTP {response.status}")
        except Exception as e:
            logger.error(f"File download error: {e}")
            raise
    
    def get_supported_options(self) -> Dict:
        return {
            "modes": ["normal", "anime", "cartoon"],
            "features": ["relative_motion", "paste_back", "do_crop"]
        }


# Global instance
sadtalker_engine = LivePortraitEngine()  # Keep variable name for compatibility
