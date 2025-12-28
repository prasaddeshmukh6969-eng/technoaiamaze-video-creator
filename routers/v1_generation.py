"""
Antigravity AI - V1 Generation API Routes
Video generation endpoints with FastAPI BackgroundTasks (No Celery/Redis required)
Supports Real-time and Anime avatar modes
"""
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Literal, List, Dict
import uuid
import os
from pathlib import Path
import logging
import cv2
import shutil
import asyncio

# Remove Celery/MinIO imports to avoid dependency errors
# from core.celery_app import celery_app
# from core.storage import storage
from engines import audio_synthesizer, animator, enhancer
from engines.avatar_generator import avatar_generator
from core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Temporary file storage - matches the static mount in main.py
TEMP_DIR = Path("/tmp/antigravity")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Base URL for serving static files (adjust based on your environment)
BASE_URL = "http://localhost:8000/static/generated"

class GenerationRequest(BaseModel):
    """Video generation request"""
    text: str
    archetype: str = "narrator_male"
    pose_intensity: float = 1.0
    language: Optional[str] = None
    enhance: bool = True
    mode: Literal["real", "anime"] = "real"
    style: Optional[str] = "anime"
    avatar_id: Optional[str] = None  # For pre-made avatars


class GenerationStatus(BaseModel):
    """Job status response"""
    job_id: str
    status: Literal["pending", "processing", "completed", "failed"]
    progress: Optional[int] = None
    message: Optional[str] = None
    result_url: Optional[str] = None
    error: Optional[str] = None


async def process_video_generation_task(
    job_id: str,
    image_path: str,
    text: str,
    archetype: str,
    pose_intensity: float,
    language: Optional[str],
    enhance: bool,
    mode: str = "real",
    style: str = "anime"
):
    """
    Background task for video generation (Replaces Celery task)
    """
    processing_marker = TEMP_DIR / f"{job_id}_processing"
    processing_marker.touch()
    
    def update_progress(progress: int):
        """Update progress file"""
        progress_file = TEMP_DIR / f"{job_id}_progress.txt"
        with open(progress_file, "w") as f:
            f.write(str(progress))
    
    try:
        logger.info(f"[{job_id}] Starting video generation (mode={mode})")
        update_progress(10)
        
        # Step 1: Generate audio
        logger.info(f"[{job_id}] Generating audio...")
        audio_path = str(TEMP_DIR / f"{job_id}_audio.wav")
        
        # Run synchronous audio synthesis in thread pool if needed, 
        # but audio_synthesizer.synthesize is async in our mock/wrapper, 
        # checking implementation... actually it might be sync in some versions.
        # Let's assume it's async or wrap it.
        # The previous code treated it as async.
        
        audio_result = await audio_synthesizer.synthesize(
            text=text,
            output_path=audio_path,
            archetype=archetype,
            language=language
        )
        
        logger.info(f"[{job_id}] ✓ Audio generated: {audio_result['duration']:.2f}s")
        update_progress(30)
        
        # Step 2: Animate
        logger.info(f"[{job_id}] Animating portrait...")
        animated_path = str(TEMP_DIR / f"{job_id}_animated.mp4")
        
        await animator.generate_animation(
            image_path=image_path,
            audio_path=audio_result["audio_path"],
            output_path=animated_path,
            pose_intensity=pose_intensity,
            fps=25,
            options={"mode": mode, "style": style}
        )
        
        logger.info(f"[{job_id}] ✓ Animation complete")
        update_progress(80)
        
        # Step 3: Enhance (optional, mostly for real mode)
        final_path = str(TEMP_DIR / f"{job_id}_final.mp4")
        
        if enhance and mode == "real":
            logger.info(f"[{job_id}] Enhancing with GFPGAN...")
            
            async def progress_callback(prog):
                update_progress(80 + int(prog * 0.2))
            
            try:
                await enhancer.enhance_video(
                    video_path=animated_path,
                    output_path=final_path,
                    weight=0.5,
                    progress_callback=progress_callback
                )
                logger.info(f"[{job_id}] ✓ Enhancement complete")
            except Exception as e:
                logger.warning(f"Enhancement failed (skipping): {e}")
                shutil.copy(animated_path, final_path)
        else:
            # Skip enhancement
            shutil.copy(animated_path, final_path)
        
        update_progress(100)
        
        # Cleanup
        if processing_marker.exists():
            processing_marker.unlink()
        
    except Exception as e:
        logger.error(f"[{job_id}] Generation failed: {e}")
        
        # Save error
        error_path = TEMP_DIR / f"{job_id}_error.txt"
        with open(error_path, "w") as f:
            f.write(str(e))
        
        if processing_marker.exists():
            processing_marker.unlink()


@router.post("/generate")
async def create_generation_job(
    background_tasks: BackgroundTasks,
    image: Optional[UploadFile] = File(None, description="Portrait image (required for real mode)"),
    text: str = Form(..., description="Text script to synthesize"),
    archetype: str = Form("narrator_male", description="Voice archetype"),
    pose_intensity: float = Form(1.0, description="Head movement intensity (0.0-1.5)"),
    language: Optional[str] = Form(None, description="Language code (auto-detect if None)"),
    enhance: bool = Form(True, description="Enable GFPGAN enhancement"),
    mode: str = Form("real", description="Mode: 'real' or 'anime'"),
    style: str = Form("anime", description="Anime style: 'anime', 'cartoon', '3d'"),
    avatar_id: Optional[str] = Form(None, description="Pre-made avatar ID (for anime mode)")
) -> JSONResponse:
    """
    Submit video generation job
    """
    job_id = str(uuid.uuid4())
    logger.info(f"New generation job: {job_id} (mode={mode})")
    
    try:
        image_path = None
        
        # Handle Image Input
        if mode == "real":
            if not image:
                raise HTTPException(400, "Image file required for Real mode")
            
            # Save uploaded image
            image_path = TEMP_DIR / f"{job_id}_input.jpg"
            with open(image_path, "wb") as f:
                f.write(await image.read())
                
        elif mode == "anime":
            if image:
                # User uploaded custom anime image
                image_path = TEMP_DIR / f"{job_id}_input.jpg"
                with open(image_path, "wb") as f:
                    f.write(await image.read())
            elif avatar_id:
                # Use pre-made avatar
                gallery_path = avatar_generator.get_avatar_path(avatar_id)
                if not gallery_path:
                    raise HTTPException(400, f"Avatar ID not found: {avatar_id}")
                
                # Copy to temp
                image_path = TEMP_DIR / f"{job_id}_input.png"
                shutil.copy(gallery_path, image_path)
            else:
                raise HTTPException(400, "For Anime mode, provide image OR avatar_id")
        
        # Validate image exists
        if not image_path or not os.path.exists(image_path):
            raise HTTPException(400, "Failed to process input image")
            
        # Submit Background Task (No Celery)
        background_tasks.add_task(
            process_video_generation_task,
            job_id=job_id,
            image_path=str(image_path),
            text=text,
            archetype=archetype,
            pose_intensity=pose_intensity,
            language=language,
            enhance=enhance,
            mode=mode,
            style=style
        )
        
        return JSONResponse({
            "job_id": job_id,
            "status": "pending",
            "message": "Video generation queued"
        })
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Job submission failed: {e}")
        raise HTTPException(500, str(e))


@router.get("/status/{job_id}")
async def get_job_status(job_id: str) -> GenerationStatus:
    """
    Poll job status
    """
    result_path = TEMP_DIR / f"{job_id}_final.mp4"
    error_path = TEMP_DIR / f"{job_id}_error.txt"
    
    if error_path.exists():
        with open(error_path) as f:
            error = f.read()
        return GenerationStatus(
            job_id=job_id,
            status="failed",
            error=error
        )
    
    if result_path.exists():
        # Return local URL instead of MinIO presigned URL
        result_url = f"{BASE_URL}/{job_id}_final.mp4"
        
        return GenerationStatus(
            job_id=job_id,
            status="completed",
            result_url=result_url,
            message="Video generation complete"
        )
    
    # Check if processing
    processing_marker = TEMP_DIR / f"{job_id}_processing"
    if processing_marker.exists():
        # Read progress if available
        progress_file = TEMP_DIR / f"{job_id}_progress.txt"
        progress = 0
        if progress_file.exists():
            with open(progress_file) as f:
                try:
                    progress = int(f.read().strip())
                except:
                    progress = 0
        
        return GenerationStatus(
            job_id=job_id,
            status="processing",
            progress=progress,
            message="Generating video..."
        )
    
    return GenerationStatus(
        job_id=job_id,
        status="pending",
        message="Waiting in queue..."
    )


@router.get("/avatars")
async def list_avatars(
    category: Optional[str] = None,
    style: Optional[str] = None
) -> JSONResponse:
    """List pre-made anime avatars"""
    avatars = await avatar_generator.get_avatar_gallery(category=category, style=style)
    return JSONResponse({"avatars": avatars})


@router.post("/avatars/generate")
async def generate_custom_avatar(
    prompt: str = Form(..., description="Character description"),
    style: str = Form("anime", description="Style: anime, cartoon, 3d")
) -> JSONResponse:
    """Generate custom anime avatar from text"""
    try:
        job_id = str(uuid.uuid4())
        output_path = TEMP_DIR / f"{job_id}_avatar.png"
        
        result = await avatar_generator.generate_anime_avatar(
            prompt=prompt,
            output_path=str(output_path),
            style=style
        )
        
        # Return local URL
        url = f"{BASE_URL}/{job_id}_avatar.png"
        
        return JSONResponse({
            "avatar_url": url,
            "job_id": job_id,
            "metadata": result
        })
        
    except Exception as e:
        logger.error(f"Avatar generation failed: {e}")
        raise HTTPException(500, str(e))


@router.get("/voices")
async def list_voices() -> JSONResponse:
    """
    List available high-quality voices
    """
    voices = audio_synthesizer.get_available_voices()
    
    return JSONResponse({
        "voices": voices,
        "archetypes": list(settings.VOICE_ARCHETYPES.keys())
    })
