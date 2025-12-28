"""
Technoaiamaze - Anime Avatar Generator
Generate custom anime avatars OR use pre-made gallery
100% FREE via Hugging Face Spaces
"""
import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, List
from gradio_client import Client
import json
import random

logger = logging.getLogger(__name__)

from core.config import settings


class AvatarGenerator:
    """
    Anime/Cartoon Avatar Generation System
    
    Two modes:
    1. Pre-made Gallery: Instant selection from curated avatars
    2. AI-Generated: Custom avatars from text prompts via HF Spaces
    
    100% FREE using Hugging Face Spaces with Stable Diffusion
    """
    
    def __init__(
        self,
        gallery_dir: str = "assets/avatars",
        sd_space_url: str = "stabilityai/stable-diffusion"
    ):
        """
        Initialize avatar generator
        
        Args:
            gallery_dir: Directory containing pre-made avatars
            sd_space_url: HF Space for Stable Diffusion anime model
        """
        self.gallery_dir = Path(gallery_dir)
        self.sd_space_url = sd_space_url
        self.client = None
        
        # Create gallery directory if it doesn't exist
        self.gallery_dir.mkdir(parents=True, exist_ok=True)
        
        # Load avatar catalog
        self._load_avatar_catalog()
        
        logger.info(f"Avatar Generator initialized")
        logger.info(f"  Gallery: {self.gallery_dir}")
        logger.info(f"  SD Space: {sd_space_url}")
    
    def _load_avatar_catalog(self):
        """Load catalog of pre-made avatars"""
        catalog_path = self.gallery_dir / "catalog.json"
        
        if catalog_path.exists():
            with open(catalog_path) as f:
                self.catalog = json.load(f)
            logger.info(f"✓ Loaded {len(self.catalog)} avatars from gallery")
        else:
            # Create default catalog structure
            self.catalog = self._create_default_catalog()
            self._save_catalog()
    
    def _create_default_catalog(self) -> List[Dict]:
        """
        Create default avatar catalog structure
        
        Returns:
            List of avatar metadata dicts
        """
        # This will be populated when you add actual avatar images
        default_avatars = [
            {
                "id": "avatar_001",
                "name": "Professional Male",
                "category": "professional",
                "gender": "male",
                "style": "anime",
                "description": "Business professional with suit",
                "filename": "professional_male_001.png",
                "tags": ["business", "formal", "suit"]
            },
            {
                "id": "avatar_002",
                "name": "Casual Female",
                "category": "casual",
                "gender": "female",
                "style": "anime",
                "description": "Friendly casual style",
                "filename": "casual_female_001.png",
                "tags": ["casual", "friendly", "modern"]
            },
            # Add more as you create/collect avatars
        ]
        
        logger.info("Created default avatar catalog (placeholder)")
        return default_avatars
    
    def _save_catalog(self):
        """Save catalog to JSON"""
        catalog_path = self.gallery_dir / "catalog.json"
        with open(catalog_path, 'w') as f:
            json.dump(self.catalog, f, indent=2)
    
    async def get_avatar_gallery(
        self,
        category: Optional[str] = None,
        gender: Optional[str] = None,
        style: Optional[str] = None
    ) -> List[Dict]:
        """
        Get filtered list of pre-made avatars
        
        Args:
            category: Filter by category (professional, casual, fantasy, etc.)
            gender: Filter by gender (male, female, neutral)
            style: Filter by style (anime, cartoon, 3d)
        
        Returns:
            List of avatar metadata dicts
        """
        filtered = self.catalog
        
        if category:
            filtered = [a for a in filtered if a.get("category") == category]
        
        if gender:
            filtered = [a for a in filtered if a.get("gender") == gender]
        
        if style:
            filtered = [a for a in filtered if a.get("style") == style]
        
        logger.info(f"Gallery query: {len(filtered)} avatars (category={category}, gender={gender}, style={style})")
        
        return filtered
    
    def get_avatar_path(self, avatar_id: str) -> Optional[str]:
        """
        Get file path for avatar by ID
        
        Args:
            avatar_id: Avatar identifier
        
        Returns:
            Full path to avatar image or None if not found
        """
        avatar = next((a for a in self.catalog if a["id"] == avatar_id), None)
        
        if avatar:
            avatar_path = self.gallery_dir / avatar["filename"]
            if avatar_path.exists():
                return str(avatar_path)
            else:
                logger.warning(f"Avatar file not found: {avatar_path}")
        
        return None
    


    async def generate_anime_avatar(
        self,
        prompt: str,
        output_path: str,
        style: str = "anime",
        negative_prompt: Optional[str] = None
    ) -> Dict:
        """
        Generate custom anime avatar from text prompt
        Uses FREE Hugging Face Space with Stable Diffusion
        
        Args:
            prompt: Text description of character
            output_path: Where to save generated image
            style: Style preset (anime, cartoon, 3d, realistic)
            negative_prompt: What to avoid in generation
        
        Returns:
            dict with image_path, prompt, metadata
        """
        logger.info(f"Generating {style} avatar from prompt: {prompt}")
        
        # Initialize HF client if needed
        if self.client is None:
            try:
                if settings.HF_TOKEN:
                    self.client = Client(self.sd_space_url, hf_token=settings.HF_TOKEN)
                else:
                    self.client = Client(self.sd_space_url)
                logger.info(f"✓ Connected to SD Space: {self.sd_space_url}")
            except Exception as e:
                logger.error(f"Failed to connect to HF Space: {e}")
                raise RuntimeError("Anime generation service unavailable")
        
        # Style-specific prompt enhancements
        style_prompts = {
            "anime": "anime style, high quality, detailed, portrait, ",
            "cartoon": "cartoon style, vibrant colors, simple shapes, ",
            "3d": "3d render, pixar style, smooth, detailed, ",
            "realistic": "photorealistic, high detail, professional photo, "
        }
        
        enhanced_prompt = style_prompts.get(style, "") + prompt
        
        # Default negative prompt
        if negative_prompt is None:
            negative_prompt = "low quality, blurry, distorted, bad anatomy, ugly, malformed"
        
        try:
            # Call Stable Diffusion API
            # Note: Adjust parameters based on actual HF Space interface
            result = self.client.predict(
                prompt=enhanced_prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=30,  # Quality vs speed tradeoff
                guidance_scale=7.5,      # How closely to follow prompt
                width=512,
                height=512,
                api_name="/predict"
            )
            
            # Download generated image
            if isinstance(result, str):
                image_url = result
            elif isinstance(result, (list, tuple)) and len(result) > 0:
                image_url = result[0]
            else:
                raise ValueError(f"Unexpected result format: {result}")
            
            # Save image
            await self._download_image(image_url, output_path)
            
            logger.info(f"✓ Avatar generated: {output_path}")
            
            return {
                "image_path": output_path,
                "prompt": enhanced_prompt,
                "style": style,
                "status": "success",
                "source": "ai_generated"
            }
        
        except Exception as e:
            logger.error(f"Avatar generation failed: {e}")
            raise RuntimeError(f"Failed to generate avatar: {str(e)}")
    
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
    
    def get_random_avatar(self, category: Optional[str] = None) -> Optional[str]:
        """
        Get random avatar from gallery
        
        Args:
            category: Optional category filter
        
        Returns:
            Path to random avatar image
        """
        avatars = self.catalog
        
        if category:
            avatars = [a for a in avatars if a.get("category") == category]
        
        if avatars:
            avatar = random.choice(avatars)
            return self.get_avatar_path(avatar["id"])
        
        return None
    
    def add_avatar_to_gallery(
        self,
        image_path: str,
        metadata: Dict
    ) -> str:
        """
        Add new avatar to gallery
        
        Args:
            image_path: Path to avatar image
            metadata: Avatar metadata (name, category, etc.)
        
        Returns:
            Avatar ID
        """
        import shutil
        
        # Generate avatar ID
        avatar_id = f"avatar_{len(self.catalog) + 1:03d}"
        filename = f"{avatar_id}.png"
        
        # Copy image to gallery
        dest_path = self.gallery_dir / filename
        shutil.copy(image_path, dest_path)
        
        # Add to catalog
        avatar_data = {
            "id": avatar_id,
            "filename": filename,
            **metadata
        }
        self.catalog.append(avatar_data)
        self._save_catalog()
        
        logger.info(f"✓ Added avatar to gallery: {avatar_id}")
        
        return avatar_id


# Global instance
avatar_generator = AvatarGenerator()
