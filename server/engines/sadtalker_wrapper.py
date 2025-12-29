"""
Technoaiamaze - LivePortrait Hugging Face Spaces Wrapper
100% FREE video animation via Hugging Face Spaces API (KwaiVGI/LivePortrait)
With comprehensive error handling and fallback mechanisms
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
    Hugging Face Spaces API wrapper for LivePortrait with error recovery
    """
    
    def __init__(self, space_url: str = "KwaiVGI/LivePortrait"):
        self.space_url = space_url
        self.client = None
        self.is_available = False
        
        logger.info(f"LivePortrait Engine initialized with HF Space: {space_url}")
    
    async def check_availability(self) -> bool:
        """Check if Hugging Face Space is available"""
        try:
            logger.info(f"Checking HF Space availability: {self.space_url}")
            
            if settings.HF_TOKEN:
                logger.info("Using HF_TOKEN for authentication")
                self.client = Client(self.space_url, hf_token=settings.HF_TOKEN)
            else:
                logger.warning("No HF_TOKEN - using public access (may have limitations)")
                self.client = Client(self.space_url)
                
            self.is_available = True
            logger.info(f"✓ HF Space '{self.space_url}' is available")
            return True
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ HF Space unavailable: {error_msg}", exc_info=True)
            logger.error(f"   Exception type: {type(e).__name__}")
            
            # Check for specific error types
            if "rate limit" in error_msg.lower():
                logger.error("   → Rate limit exceeded on HuggingFace")
            elif "not found" in error_msg.lower() or "404" in error_msg:
                logger.error(f"   → Space '{self.space_url}' not found or moved")
            elif "timeout" in error_msg.lower():
                logger.error("   → Connection timeout - HF Space may be overloaded")
            
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
        Generate animated video from image + audio with comprehensive error handling
        """
        if not self.is_available:
            logger.info("Checking LivePortrait availability...")
            await self.check_availability()
        
        if not self.is_available:
            raise RuntimeError(
                "LivePortrait HF Space is not available. "
                "Please check https://huggingface.co/spaces/KwaiVGI/LivePortrait "
                "or use avatar upload instead of generation."
            )
        
        options = options or {}
        mode = options.get("mode", "normal")
        
        logger.info(f"Starting LivePortrait video generation...")
        logger.info(f"  Image: {image_path}")
        logger.info(f"  Audio: {audio_path}")
        logger.info(f"  Output: {output_path}")
        logger.info(f"  Mode: {mode}")
        
        try:
            # Try the API call with detailed error capture
            logger.info(f"Calling LivePortrait API endpoint...")
            
            result = self.client.predict(
                image_path,     # source_image (0)
                audio_path,     # driving_audio (1)
                True,           # relative_motion (2)
                True,           # do_crop (3)
                True,           # paste_back (4)
                api_name="/gpu_wrapped_execute_video" 
            )
            
            logger.info(f"✓ API call successful")
            logger.info(f"  Result type: {type(result)}")
            logger.info(f"  Result length: {len(result) if isinstance(result, (list, tuple)) else 'N/A'}")
            
            # Handle result
            if isinstance(result, str):
                video_url = result
                logger.info(f"  Result is string: {video_url[:100]}...")
            elif isinstance(result, (list, tuple)) and len(result) > 0:
                video_url = result[0]
                logger.info(f"  Result is tuple/list, first element: {video_url}")
                if isinstance(video_url, dict) and "video" in video_url:
                    video_url = video_url["video"]
                    logger.info(f"  Extracted video from dict: {video_url}")
            else:
                error_msg = f"Unexpected result format: {type(result)} - {result}"
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            # Download video
            logger.info(f"Downloading generated video...")
            await self._download_file(video_url, output_path)
            
            logger.info(f"✓✓✓ Video generated successfully: {output_path}")
            
            return {
                "video_path": output_path,
                "status": "success",
                "mode": mode,
                "source": "liveportrait_hf"
            }
        
        except Exception as e:
            # COMPREHENSIVE ERROR LOGGING
            error_type = type(e).__name__
            error_msg = str(e)
            
            logger.error("=" * 80)
            logger.error("❌❌❌ LIVEPORTRAIT GENERATION FAILED ❌❌❌")
            logger.error("=" * 80)
            logger.error(f"Exception Type: {error_type}")
            logger.error(f"Exception Message: {error_msg}")
            logger.error(f"Image Path: {image_path}")
            logger.error(f"Audio Path: {audio_path}")
            logger.error(f"HF Space: {self.space_url}")
            logger.error(f"Has HF Token: {bool(settings.HF_TOKEN)}")
            logger.error("=" * 80, exc_info=True)
            
            # Provide helpful error messages
            if "upstream" in error_msg.lower() and "gradio" in error_msg.lower():
                detailed_error = (
                    f"HuggingFace Space Error: {error_msg}\n\n"
                    "This error comes from the HuggingFace Space itself. Common causes:\n"
                    "1. Space is temporarily down or restarting\n"
                    "2. Space is overloaded with requests\n"
                    "3. Input format incompatible with current Space version\n"
                    "4. Rate limiting on free tier\n\n"
                    "SOLUTIONS:\n"
                    "• Use 'Upload Avatar' instead of 'Generate Avatar'\n"
                    "• Try again in a few minutes\n"
                    "• Check Space status: https://huggingface.co/spaces/KwaiVGI/LivePortrait"
                )
            elif "api_name" in error_msg.lower() or "parameter" in error_msg.lower():
                detailed_error = (
                    f"API Mismatch Error: {error_msg}\n\n"
                    "The LivePortrait Space API has changed.\n"
                    "The code needs to be updated to match the new API structure.\n\n"
                    "WORKAROUND: Use 'Upload Avatar' feature instead."
                )
            elif "timeout" in error_msg.lower():
                detailed_error = f"Timeout Error: {error_msg}\n\nThe Space is slow. Try again or use avatar upload."
            else:
                detailed_error = f"LivePortrait Error: {error_msg}\n\nUse 'Upload Avatar' as alternative."
            
            raise RuntimeError(detailed_error)
    
    async def animate_anime_character(
        self,
        image_path: str,
        audio_path: str,
        output_path: str,
        style: str = "anime"
    ) -> Dict:
        """Specialized method for anime character animation"""
        return await self.generate_video(
            image_path=image_path,
            audio_path=audio_path,
            output_path=output_path,
            options={"mode": "anime", "style": style}
        )
    
    async def _download_file(self, url: str, output_path: str):
        """Download file from URL to local path"""
        try:
            # Handle local file paths returned by gradio_client
            if os.path.exists(url):
                logger.info(f"File is local, copying: {url}")
                shutil.copy(url, output_path)
                logger.info(f"✓ Copied local file to: {output_path}")
                return

            # Download from URL
            logger.info(f"Downloading from URL: {url[:100]}...")
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        with open(output_path, 'wb') as f:
                            while True:
                                chunk = await response.content.read(8192)
                                if not chunk:
                                    break
                                f.write(chunk)
                        logger.info(f"✓ Downloaded to: {output_path}")
                    else:
                        raise RuntimeError(f"Download failed: HTTP {response.status}")
                        
        except Exception as e:
            logger.error(f"File download error: {e}", exc_info=True)
            raise
    
    def get_supported_options(self) -> Dict:
        return {
            "modes": ["normal", "anime", "cartoon"],
            "features": ["relative_motion", "paste_back", "do_crop"]
        }


# Global instance
sadtalker_engine = LivePortraitEngine()
