"""
Technoaiamaze - Production-Grade LivePortrait with Failure Resistance
GUARANTEED to never block video generation pipeline
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
import time
from core.config import settings

logger = logging.getLogger(__name__)


class LivePortraitCircuitBreaker:
    """Prevent cascading failures from HF Space"""
    
    def __init__(self, failure_threshold=2, timeout=300):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = 0
        self.is_open = False
    
    def record_success(self):
        self.failure_count = 0
        self.is_open = False
    
    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.is_open = True
            logger.warning(f"🔴 LivePortrait circuit breaker OPEN")
    
    def can_attempt(self) -> bool:
        if not self.is_open:
            return True
        if time.time() - self.last_failure_time > self.timeout:
            logger.info("🔄 LivePortrait circuit breaker reset")
            self.is_open = False
            self.failure_count = 0
            return True
        return False


class LivePortraitEngine:
    """
    Production-Grade LivePortrait with Total Failure Resistance
    
    KEY PRINCIPLE: Video generation MUST succeed even if LivePortrait fails
    """
    
    def __init__(self, space_url: str = "KwaiVGI/LivePortrait"):
        self.space_url = space_url
        self.client = None
        self.is_available = False
        self.circuit_breaker = LivePortraitCircuitBreaker()
        
        logger.info(f"🎬 LivePortrait Engine initialized (HARDENED MODE)")
    
    async def generate_video(
        self,
        image_path: str,
        audio_path: str,
        output_path: str,
        options: Optional[Dict] = None,
        timeout: int = 180
    ) -> Dict:
        """
        PRODUCTION-GRADE video generation with GUARANTEED result
        
        NEVER throws fatal error
        ALWAYS returns a result (success or graceful failure)
        """
        logger.info(f"🎬 Video generation starting...")
        logger.info(f"  Image: {image_path}")
        logger.info(f"  Audio: {audio_path}")
        
        # Check circuit breaker
        if not self.circuit_breaker.can_attempt():
            logger.warning("⚡ LivePortrait circuit OPEN - returning immediate graceful failure")
            return self._graceful_failure("circuit_breaker_open", image_path, audio_path)
        
        try:
            # Attempt with timeout
            logger.info(f"Attempting LivePortrait generation (timeout: {timeout}s)...")
            
            result = await asyncio.wait_for(
                self._attempt_liveportrait_generation(image_path, audio_path, output_path, options),
                timeout=timeout
            )
            
            # SUCCESS!
            self.circuit_breaker.record_success()
            logger.info(f"✅✅✅ LIVEPORTRAIT SUCCESS ✅✅✅")
            return result
            
        except asyncio.TimeoutError:
            logger.error(f"⏱️ LivePortrait timeout after {timeout}s")
            self.circuit_breaker.record_failure()
            return self._graceful_failure("timeout", image_path, audio_path)
            
        except Exception as e:
            logger.error(f"❌ LivePortrait failed: {type(e).__name__}: {str(e)}")
            self.circuit_breaker.record_failure()
            return self._graceful_failure("error", image_path, audio_path, str(e))
    
    async def _attempt_liveportrait_generation(
        self,
        image_path: str,
        audio_path: str,
        output_path: str,
        options: Optional[Dict]
    ) -> Dict:
        """Actual LivePortrait call - can fail"""
        
        # Initialize client
        if self.client is None:
            if settings.HF_TOKEN:
                self.client = Client(self.space_url, hf_token=settings.HF_TOKEN)
            else:
                self.client = Client(self.space_url)
        
        # Call API
        result = self.client.predict(
            image_path,
            audio_path,
            True,  # relative_motion
            True,  # do_crop
            True,  # paste_back
            api_name="/gpu_wrapped_execute_video"
        )
        
        # Extract video
        if isinstance(result, str):
            video_url = result
        elif isinstance(result, (list, tuple)) and len(result) > 0:
            video_url = result[0]
            if isinstance(video_url, dict) and "video" in video_url:
                video_url = video_url["video"]
        else:
            raise ValueError(f"Unexpected result: {result}")
        
        # Download
        await self._download_file(video_url, output_path)
        
        return {
            "video_path": output_path,
            "status": "success",
            "source": "liveportrait_hf"
        }
    
    def _graceful_failure(
        self,
        reason: str,
        image_path: str,
        audio_path: str,
        error_detail: str = ""
    ) -> Dict:
        """
        GUARANTEED graceful failure response
        
        Returns structured failure that allows pipeline to continue
        """
        logger.warning(f"⚠️ GRACEFUL FAILURE MODE")
        logger.warning(f"  Reason: {reason}")
        if error_detail:
            logger.warning(f"  Detail: {error_detail}")
        logger.warning(f"  ✅ Returning graceful failure - pipeline can continue")
        
        return {
            "video_path": None,
            "status": "graceful_failure",
            "reason": reason,
            "error": error_detail,
            "source": "liveportrait_failed",
            "image_path": image_path,
            "audio_path": audio_path,
            "message": (
                "LivePortrait temporarily unavailable. "
                "Please use 'Upload Avatar' for reliable video generation."
            )
        }
    
    async def _download_file(self, url: str, output_path: str):
        """Download file with error handling"""
        try:
            if os.path.exists(url):
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
                    else:
                        raise RuntimeError(f"Download failed: HTTP {response.status}")
        except Exception as e:
            logger.error(f"Download error: {e}")
            raise


    async def animate_anime_character(
        self,
        image_path: str,
        audio_path: str,
        output_path: str,
        style: str = "anime"
    ) -> Dict:
        """
        Generate anime animation (Delegates to standard generation for now)
        """
        logger.info(f"🎨 Generating Anime animation ({style})")
        return await self.generate_video(
            image_path=image_path,
            audio_path=audio_path,
            output_path=output_path,
            options={"mode": "anime", "style": style}
        )


# Global instance
sadtalker_engine = LivePortraitEngine()
