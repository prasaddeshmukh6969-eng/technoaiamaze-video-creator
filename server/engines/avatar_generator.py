"""
Technoaiamaze - Production-Grade Avatar Generator with Failover
100% guaranteed success regardless of HF Space availability
"""
import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, List
from gradio_client import Client
import json
import random
import time
from PIL import Image
import io

logger = logging.getLogger(__name__)

from core.config import settings


class AvatarGenerationCircuitBreaker:
    """Circuit breaker for HF Space to prevent cascading failures"""
    
    def __init__(self, failure_threshold=3, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = 0
        self.is_open = False
    
    def record_success(self):
        """Reset on success"""
        self.failure_count = 0
        self.is_open = False
    
    def record_failure(self):
        """Track failures and open circuit if needed"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.is_open = True
            logger.warning(f"🔴 Circuit breaker OPEN - HF Space marked as unavailable")
    
    def can_attempt(self) -> bool:
        """Check if we should attempt HF call"""
        if not self.is_open:
            return True
        
        # Auto-reset after timeout
        if time.time() - self.last_failure_time > self.timeout:
            logger.info("🔄 Circuit breaker auto-reset - retrying HF Space")
            self.is_open = False
            self.failure_count = 0
            return True
        
        return False


class AvatarGenerator:
    """
    Production-Grade Avatar Generation with Multi-Layer Failover
    
    Failure Resistance Strategy:
    1. Try LivePortrait/SD (if circuit allows)
    2. Fallback to placeholder avatar
    3. NEVER block video generation
    """
    
    def __init__(
        self,
        gallery_dir: str = "assets/avatars",
        sd_space_url: str = "stabilityai/stable-diffusion"
    ):
        self.gallery_dir = Path(gallery_dir)
        self.sd_space_url = sd_space_url
        self.client = None
        self.circuit_breaker = AvatarGenerationCircuitBreaker()
        
        # Create gallery directory
        self.gallery_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure placeholder exists
        self._ensure_placeholder_avatar()
        
        # Load avatar catalog
        self._load_avatar_catalog()
        
        logger.info(f"🎨 Avatar Generator initialized (PRODUCTION MODE)")
        logger.info(f"  Gallery: {self.gallery_dir}")
        logger.info(f"  Circuit breaker: ENABLED")
    
    def _ensure_placeholder_avatar(self):
        """Create placeholder avatar if none exists"""
        placeholder_path = self.gallery_dir / "placeholder.png"
        
        if not placeholder_path.exists():
            # Create simple colored placeholder
            from PIL import Image, ImageDraw, ImageFont
            
            img = Image.new('RGB', (512, 512), color=(100, 100, 200))
            draw = ImageDraw.Draw(img)
            
            # Draw simple avatar shape
            draw.ellipse([128, 128, 384, 384], fill=(150, 150, 255))
            draw.ellipse([200, 200, 312, 280], fill=(200, 200, 255))  # Face
            
            img.save(placeholder_path)
            logger.info(f"✓ Created placeholder avatar: {placeholder_path}")
    
    def _load_avatar_catalog(self):
        """Load catalog of pre-made avatars"""
        catalog_path = self.gallery_dir / "catalog.json"
        
        if catalog_path.exists():
            with open(catalog_path) as f:
                self.catalog = json.load(f)
        else:
            self.catalog = []
            self._save_catalog()
    
    def _save_catalog(self):
        """Save catalog to JSON"""
        catalog_path = self.gallery_dir / "catalog.json"
        with open(catalog_path, 'w') as f:
            json.dump(self.catalog, f, indent=2)
    
    async def generate_anime_avatar(
        self,
        prompt: str,
        output_path: str,
        style: str = "anime",
        negative_prompt: Optional[str] = None,
        timeout: int = 30
    ) -> Dict:
        """
        Generate avatar with GUARANTEED fallback
        
        Returns ALWAYS, never throws blocking errors
        """
        logger.info(f"🎨 Avatar generation requested: {prompt[:50]}...")
        
        # Check circuit breaker
        if not self.circuit_breaker.can_attempt():
            logger.warning("⚡ Circuit breaker OPEN - skipping HF Space, using placeholder")
            return await self._use_placeholder_avatar(output_path, "circuit_open")
        
        try:
            # Try HF generation with timeout
            logger.info(f"Attempting HF Space generation (timeout: {timeout}s)...")
            
            result = await asyncio.wait_for(
                self._attempt_hf_generation(prompt, output_path, style, negative_prompt),
                timeout=timeout
            )
            
            # Success!
            self.circuit_breaker.record_success()
            logger.info(f"✅ HF generation successful")
            return result
            
        except asyncio.TimeoutError:
            logger.error(f"⏱️ HF generation timeout after {timeout}s")
            self.circuit_breaker.record_failure()
            return await self._use_placeholder_avatar(output_path, "timeout")
            
        except Exception as e:
            logger.error(f"❌ HF generation failed: {type(e).__name__}: {str(e)}")
            self.circuit_breaker.record_failure()
            return await self._use_placeholder_avatar(output_path, "error")
    
    async def _attempt_hf_generation(
        self,
        prompt: str,
        output_path: str,
        style: str,
        negative_prompt: Optional[str]
    ) -> Dict:
        """Actual HF Space call - can fail"""
        
        # Initialize client if needed
        if self.client is None:
            if settings.HF_TOKEN:
                self.client = Client(self.sd_space_url, hf_token=settings.HF_TOKEN)
            else:
                self.client = Client(self.sd_space_url)
        
        # Style-specific prompts
        style_prompts = {
            "anime": "anime style, high quality, detailed, portrait, ",
            "cartoon": "cartoon style, vibrant colors, ",
            "3d": "3d render, smooth, ",
            "realistic": "photorealistic, "
        }
        
        enhanced_prompt = style_prompts.get(style, "") + prompt
        
        if negative_prompt is None:
            negative_prompt = "low quality, blurry, distorted"
        
        # Call SD API
        result = self.client.predict(
            prompt=enhanced_prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=20,  # Reduced for speed
            guidance_scale=7.5,
            width=512,
            height=512,
            api_name="/predict"
        )
        
        # Handle result
        if isinstance(result, str):
            image_url = result
        elif isinstance(result, (list, tuple)) and len(result) > 0:
            image_url = result[0]
        else:
            raise ValueError(f"Unexpected result: {result}")
        
        # Download
        await self._download_image(image_url, output_path)
        
        return {
            "image_path": output_path,
            "prompt": enhanced_prompt,
            "style": style,
            "status": "success",
            "source": "ai_generated"
        }
    
    async def _use_placeholder_avatar(
        self,
        output_path: str,
        reason: str
    ) -> Dict:
        """
        GUARANTEED fallback - always succeeds
        """
        import shutil
        
        placeholder_path = self.gallery_dir / "placeholder.png"
        
        logger.info(f"🔄 Using placeholder avatar (reason: {reason})")
        logger.info(f"  Source: {placeholder_path}")
        logger.info(f"  Destination: {output_path}")
        
        # Copy placeholder
        shutil.copy(str(placeholder_path), output_path)
        
        logger.info(f"✅ Placeholder avatar ready - GUARANTEED SUCCESS")
        
        return {
            "image_path": output_path,
            "prompt": "placeholder",
            "style": "placeholder",
            "status": "success_fallback",
            "source": "placeholder",
            "fallback_reason": reason
        }
    
    async def _download_image(self, url: str, output_path: str):
        """Download image from URL"""
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(output_path, 'wb') as f:
                        f.write(await response.read())
                else:
                    raise RuntimeError(f"Download failed: HTTP {response.status}")
    
    def get_random_avatar(self) -> Optional[str]:
        """Get random avatar or placeholder"""
        if self.catalog:
            avatar = random.choice(self.catalog)
            path = self.gallery_dir / avatar["filename"]
            if path.exists():
                return str(path)
        
        # Fallback to placeholder
        return str(self.gallery_dir / "placeholder.png")


# Global instance
avatar_generator = AvatarGenerator()
