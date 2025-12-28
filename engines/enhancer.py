"""
Antigravity AI - GFPGAN Enhancement Engine
Face restoration and super-resolution (512px → 1024px+)
Scientific approach: Uses facial priors to hallucinate missing details
"""
try:
    import torch
    from gfpgan import GFPGANer
    GFPGAN_AVAILABLE = True
except ImportError:
    torch = None
    GFPGANer = None
    GFPGAN_AVAILABLE = False

import cv2
import numpy as np
from pathlib import Path
import logging
from typing import Optional

from core.config import settings

logger = logging.getLogger(__name__)


class FaceEnhancer:
    """
    GFPGAN v1.4 wrapper for video enhancement
    
    Why GFPGAN?
    - Raw LivePortrait output is 512px and often blurry
    - GFPGAN uses pre-trained facial priors to reconstruct:
      * Eye details (eyelashes, iris texture)
      * Skin texture (pores, fine wrinkles)
      * Sharp facial features
    - NOT simple upscaling - AI-powered detail hallucination
    """
    
    def __init__(self):
        self.device = "cpu"
        if GFPGAN_AVAILABLE and torch.cuda.is_available():
            self.device = torch.device("cuda")
        
        self.enhancer = None
        logger.info(f"GFPGAN Enhancer initialized (Available: {GFPGAN_AVAILABLE})")
    
    def load_model(self):
        """Load GFPGAN v1.4 model"""
        if not GFPGAN_AVAILABLE:
            return

        if self.enhancer is not None:
            return
        
        try:
            logger.info("Loading GFPGAN v1.4 model...")
            
            weights_path = Path(settings.GFPGAN_WEIGHTS)
            if not weights_path.exists():
                logger.warning(f"GFPGAN weights not found at {weights_path}")
                logger.info("Download from: https://github.com/TencentARC/GFPGAN/releases")
                return
            
            # Initialize GFPGAN
            self.enhancer = GFPGANer(
                model_path=str(weights_path),
                upscale=2,  # 2x upscaling (512px → 1024px)
                arch='clean',
                channel_multiplier=2,
                bg_upsampler=None,  # Don't upscale background (prevents warping)
                device=self.device
            )
            
            logger.info("✓ GFPGAN v1.4 loaded successfully")
            
        except Exception as e:
            logger.error(f"GFPGAN loading failed: {e}")
            self.enhancer = None
    
    def enhance_image(self, image_path: str, output_path: str, weight: float = 0.5) -> dict:
        """
        Enhance a single image
        
        Args:
            image_path: Input image path
            output_path: Output enhanced image path
            weight: Blending weight (0.0 = original, 1.0 = fully enhanced)
        
        Returns:
            dict with enhanced_path, width, height
        """
        self.load_model()
        
        if self.enhancer is None:
            logger.warning("GFPGAN not available, skipping enhancement")
            # Copy original to output
            import shutil
            shutil.copy(image_path, output_path)
            img = cv2.imread(image_path)
            h, w = img.shape[:2]
            return {"enhanced_path": output_path, "width": w, "height": h, "enhanced": False}
        
        # Read image
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        
        # Enhance
        _, _, restored_img = self.enhancer.enhance(
            img,
            has_aligned=False,
            only_center_face=False,
            paste_back=True,
            weight=weight
        )
        
        # Save enhanced image
        cv2.imwrite(output_path, restored_img)
        h, w = restored_img.shape[:2]
        
        logger.info(f"✓ Image enhanced: {w}x{h}")
        
        return {
            "enhanced_path": output_path,
            "width": w,
            "height": h,
            "enhanced": True
        }
    
    async def enhance_video(
        self,
        video_path: str,
        output_path: str,
        weight: float = 0.5,
        progress_callback: Optional[callable] = None
    ) -> dict:
        """
        Enhance video frame-by-frame
        
        Args:
            video_path: Input video path
            output_path: Output enhanced video path
            weight: Enhancement blending weight
            progress_callback: Function to call with progress (0-100)
        
        Returns:
            dict with enhanced_path, frame_count, resolution
        """
        self.load_model()
        
        if self.enhancer is None:
            logger.warning("GFPGAN not available, skipping video enhancement")
            import shutil
            shutil.copy(video_path, output_path)
            return {"enhanced_path": output_path, "enhanced": False}
        
        logger.info(f"Enhancing video: {video_path}")
        
        # Open video
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Read first frame to get dimensions
        ret, first_frame = cap.read()
        if not ret:
            raise ValueError("Failed to read video")
        
        # Enhance first frame to get output dimensions
        _, _, enhanced_first = self.enhancer.enhance(
            first_frame,
            has_aligned=False,
            only_center_face=False,
            paste_back=True,
            weight=weight
        )
        h, w = enhanced_first.shape[:2]
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        temp_output = output_path.replace('.mp4', '_temp.mp4')
        out = cv2.VideoWriter(temp_output, fourcc, fps, (w, h))
        
        # Write enhanced first frame
        out.write(enhanced_first)
        
        # Process remaining frames
        frame_idx = 1
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Enhance frame
            _, _, enhanced_frame = self.enhancer.enhance(
                frame,
                has_aligned=False,
                only_center_face=False,
                paste_back=True,
                weight=weight
            )
            
            out.write(enhanced_frame)
            
            # Progress
            frame_idx += 1
            if frame_idx % 10 == 0:
                progress = int((frame_idx / total_frames) * 100)
                logger.info(f"  Enhanced {frame_idx}/{total_frames} frames ({progress}%)")
                
                if progress_callback:
                    await progress_callback(progress)
        
        cap.release()
        out.release()
        
        # Add audio from original video
        import subprocess
        cmd = [
            'ffmpeg', '-y',
            '-i', temp_output,
            '-i', video_path,
            '-c:v', 'libx264',
            '-c:a', 'copy',
            '-map', '0:v:0',
            '-map', '1:a:0?',
            output_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"✓ Video enhanced: {output_path}")
            
            # Clean up
            Path(temp_output).unlink()
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error: {e.stderr.decode()}")
            raise
        
        return {
            "enhanced_path": output_path,
            "frame_count": total_frames,
            "resolution": f"{w}x{h}",
            "enhanced": True
        }
    
    def clear_gpu_memory(self):
        """Clear GPU memory"""
        if GFPGAN_AVAILABLE and torch.cuda.is_available():
            torch.cuda.empty_cache()
            logger.info("✓ GPU memory cleared")


# Global instance
enhancer = FaceEnhancer()
