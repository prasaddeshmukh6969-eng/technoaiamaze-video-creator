"""
HeyGen API Integration - Production-Ready Talking Head Video Generation
FREE tier: 10 credits/month, then pay-as-you-go
"""
import asyncio
import aiohttp
import logging
import time
from pathlib import Path
from typing import Optional, Dict
import os

logger = logging.getLogger(__name__)


class HeyGenEngine:
    """
    HeyGen API Integration for reliable talking head video generation
    
    Pricing:
    - Free: 10 API credits/month (10 videos)
    - Pro: $99/month for 100 credits
    - Scale: $330/month for 660 credits
    
    1 credit = 1 minute of video generation
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("HEYGEN_API_KEY")
        self.base_url = "https://api.heygen.com/v2"
        self.is_available = self.api_key is not None
        
        if not self.is_available:
            logger.warning("⚠️ HeyGen API key not found. Set HEYGEN_API_KEY environment variable.")
        else:
            logger.info("✅ HeyGen Engine initialized")
    
    async def generate_video(
        self,
        image_path: str,
        audio_path: str,
        output_path: str,
        options: Optional[Dict] = None
    ) -> Dict:
        """
        Generate talking head video using HeyGen API
        
        Args:
            image_path: Path to portrait image
            audio_path: Path to audio file
            output_path: Where to save the output video
            options: Additional options (avatar_style, etc.)
        
        Returns:
            dict with video_path, status, and metadata
        """
        if not self.is_available:
            return self._no_api_key_error()
        
        logger.info("🎬 Starting HeyGen video generation...")
        logger.info(f"  Image: {image_path}")
        logger.info(f"  Audio: {audio_path}")
        
        try:
            # Step 1: Upload assets
            image_url = await self._upload_asset(image_path, "image")
            audio_url = await self._upload_asset(audio_path, "audio")
            
            # Step 2: Create video generation request
            video_id = await self._create_video_request(image_url, audio_url, options)
            
            # Step 3: Poll for completion
            result_url = await self._wait_for_completion(video_id)
            
            # Step 4: Download result
            await self._download_video(result_url, output_path)
            
            logger.info("✅ HeyGen video generation successful!")
            
            return {
                "video_path": output_path,
                "status": "success",
                "source": "heygen_api",
                "video_id": video_id
            }
            
        except Exception as e:
            logger.error(f"❌ HeyGen generation failed: {str(e)}")
            return {
                "video_path": None,
                "status": "failed",
                "source": "heygen_api",
                "error": str(e)
            }
    
    async def _upload_asset(self, file_path: str, asset_type: str) -> str:
        """Upload image or audio to HeyGen and return URL"""
        logger.info(f"📤 Uploading {asset_type}: {file_path}")
        
        async with aiohttp.ClientSession() as session:
            # Get upload URL
            async with session.post(
                f"{self.base_url}/assets/upload",
                headers={
                    "X-Api-Key": self.api_key,
                    "Content-Type": "application/json"
                },
                json={"type": asset_type}
            ) as resp:
                if resp.status != 200:
                    error = await resp.text()
                    raise RuntimeError(f"Failed to get upload URL: {error}")
                
                upload_data = await resp.json()
                upload_url = upload_data["data"]["upload_url"]
                asset_id = upload_data["data"]["asset_id"]
            
            # Upload file
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            async with session.put(upload_url, data=file_data) as resp:
                if resp.status not in [200, 201]:
                    raise RuntimeError(f"Failed to upload {asset_type}")
            
            logger.info(f"✅ Uploaded {asset_type}: {asset_id}")
            return asset_id
    
    async def _create_video_request(
        self,
        image_asset_id: str,
        audio_asset_id: str,
        options: Optional[Dict]
    ) -> str:
        """Create video generation request and return video_id"""
        logger.info("🎬 Creating video generation request...")
        
        options = options or {}
        
        payload = {
            "video_inputs": [
                {
                    "character": {
                        "type": "photo_avatar",
                        "photo_id": image_asset_id,
                        "avatar_style": options.get("avatar_style", "normal")
                    },
                    "voice": {
                        "type": "audio",
                        "audio_asset_id": audio_asset_id
                    }
                }
            ],
            "dimension": {
                "width": 1280,
                "height": 720
            },
            "aspect_ratio": options.get("aspect_ratio", "16:9")
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/video/generate",
                headers={
                    "X-Api-Key": self.api_key,
                    "Content-Type": "application/json"
                },
                json=payload
            ) as resp:
                if resp.status != 200:
                    error = await resp.text()
                    raise RuntimeError(f"Failed to create video: {error}")
                
                result = await resp.json()
                video_id = result["data"]["video_id"]
                
                logger.info(f"✅ Video request created: {video_id}")
                return video_id
    
    async def _wait_for_completion(self, video_id: str, timeout: int = 300) -> str:
        """Poll video status until complete or timeout"""
        logger.info(f"⏳ Waiting for video generation (timeout: {timeout}s)...")
        
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            while time.time() - start_time < timeout:
                async with session.get(
                    f"{self.base_url}/video/{video_id}",
                    headers={"X-Api-Key": self.api_key}
                ) as resp:
                    if resp.status != 200:
                        error = await resp.text()
                        raise RuntimeError(f"Failed to check status: {error}")
                    
                    result = await resp.json()
                    status = result["data"]["status"]
                    
                    logger.info(f"  Status: {status}")
                    
                    if status == "completed":
                        video_url = result["data"]["video_url"]
                        logger.info("✅ Video generation complete!")
                        return video_url
                    
                    elif status == "failed":
                        error = result["data"].get("error", "Unknown error")
                        raise RuntimeError(f"Video generation failed: {error}")
                    
                    # Still processing, wait before next poll
                    await asyncio.sleep(5)
        
        raise TimeoutError(f"Video generation timeout after {timeout}s")
    
    async def _download_video(self, url: str, output_path: str):
        """Download video from URL to local path"""
        logger.info(f"📥 Downloading video to {output_path}")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"Failed to download video: HTTP {resp.status}")
                
                with open(output_path, 'wb') as f:
                    while True:
                        chunk = await resp.content.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
        
        logger.info("✅ Video downloaded successfully")
    
    def _no_api_key_error(self) -> Dict:
        """Return error when API key not configured"""
        logger.error("❌ HEYGEN_API_KEY not configured")
        return {
            "video_path": None,
            "status": "failed",
            "source": "heygen_api",
            "error": "API key not configured. Set HEYGEN_API_KEY environment variable.",
            "message": (
                "HeyGen API key required. "
                "Sign up at https://app.heygen.com/ for 10 free credits/month."
            )
        }
    
    async def animate_anime_character(
        self,
        image_path: str,
        audio_path: str,
        output_path: str,
        style: str = "anime"
    ) -> Dict:
        """Generate anime animation (uses same API with style option)"""
        logger.info(f"🎨 Generating Anime animation ({style})")
        return await self.generate_video(
            image_path=image_path,
            audio_path=audio_path,
            output_path=output_path,
            options={"avatar_style": style}
        )


# Global instance
heygen_engine = HeyGenEngine()
