"""
Antigravity AI - Simple Mock Backend
Simplified version for testing without heavy AI dependencies
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Literal
import uuid
import time
import asyncio
from pathlib import Path
import io
import subprocess

app = FastAPI(
    title="Technoaiamaze - AI Video Creator",
    version="1.0.0",
    description="AI-powered talking head video generation"
)

# CORS Configuration - Allow multiple frontend origins
# This supports local development, Vercel, Hostinger, and custom domains
import os
import re

# Define allowed origins
allowed_origins = [
    "http://localhost:3000",                                    # Local development
    "https://localhost:3000",                                   # Local HTTPS
    "https://technoaiamaze-video-creator.vercel.app",          # Vercel main domain
    "https://ai.technoamaze.in",                               # Hostinger custom domain
    "https://technoamaze.in",                                  # Main domain
]

# Allow all Vercel preview deployments (e.g., technoaiamaze-video-creator-*.vercel.app)
def check_origin(origin: str) -> bool:
    """Check if origin is allowed"""
    if origin in allowed_origins:
        return True
    
    # Allow any Vercel deployment
    if re.match(r"https://technoaiamaze-video-creator.*\.vercel\.app", origin):
        return True
    
    # Allow any localhost port for development
    if re.match(r"http://localhost:\d+", origin):
        return True
    
    return False

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://(technoaiamaze-video-creator.*\.vercel\.app|ai\.technoamaze\.in|technoamaze\.in)|http://localhost:\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job storage
jobs = {}

class JobStatus(BaseModel):
    job_id: str
    status: Literal["pending", "processing", "completed", "failed"]
    progress: Optional[int] = None
    message: Optional[str] = None
    result_url: Optional[str] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    return {
        "app": "Antigravity AI - Mock Backend",
        "version": "1.0.0",
        "status": "operational",
        "message": "⚠️ This is a mock backend. Install full dependencies for real video generation."
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "cuda_available": False,
        "edge_tts": True,
        "mode": "mock"
    }


@app.post("/api/v1/generate")
async def create_generation_job(
    image: UploadFile = File(...),
    text: str = Form(...),
    archetype: str = Form("narrator_male"),
    pose_intensity: float = Form(1.0),
    language: Optional[str] = Form(None),
    enhance: bool = Form(True)
) -> JSONResponse:
    """Submit mock video generation job"""
    
    job_id = str(uuid.uuid4())
    
    # Store job
    jobs[job_id] = {
        "status": "pending",
        "progress": 0,
        "message": "Job queued...",
        "created_at": time.time(),
        "user_email": current_user['email']
    }
    
    # Start mock processing in background
    asyncio.create_task(mock_process_job(job_id))
    
    return JSONResponse({
        "job_id": job_id,
        "status": "pending",
        "message": "Video generation queued (MOCK MODE)"
    })


async def mock_process_job(job_id: str):
    """Simulate video generation process and create placeholder video"""
    
    # Simulate processing stages
    stages = [
        (10, "Generating audio..."),
        (30, "Audio complete, starting animation..."),
        (50, "Animating portrait..."),
        (70, "Animation complete..."),
        (90, "Enhancing with GFPGAN..."),
        (100, "Complete!")
    ]
    
    jobs[job_id]["status"] = "processing"
    
    for progress, message in stages:
        await asyncio.sleep(2)  # 2 seconds per stage
        jobs[job_id]["progress"] = progress
        jobs[job_id]["message"] = message
    
    # Create placeholder video file
    video_path = create_placeholder_video(job_id)
    jobs[job_id]["video_path"] = str(video_path)
    
    # Mark as completed
    jobs[job_id]["status"] = "completed"
    jobs[job_id]["result_url"] = f"http://localhost:8000/api/v1/download/{job_id}"
    jobs[job_id]["message"] = "Video generation complete! (MOCK - Placeholder video created)"


def create_placeholder_video(job_id: str) -> Path:
    """Create a proper placeholder video file using PIL"""
    output_dir = Path("temp_videos")
    output_dir.mkdir(exist_ok=True)
    
    video_path = output_dir / f"{job_id}.mp4"
    
    try:
        # Try ffmpeg first (best quality)
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi',
            '-i', 'color=c=purple:s=640x480:d=5',
            '-vf', f"drawtext=text='Antigravity AI Mock Video':fontsize=30:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2,drawtext=text='Job ID\\: {job_id[:8]}':fontsize=20:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2+50",
            '-c:v', 'libx264',
            '-t', '5',
            '-pix_fmt', 'yuv420p',
            str(video_path)
        ]
        subprocess.run(cmd, capture_output=True, timeout=10, check=True)
        return video_path
    except:
        pass
    
    try:
        # Fallback: Use PIL to create a video
        from PIL import Image, ImageDraw, ImageFont
        import struct
        
        # Create a purple image with text
        width, height = 640, 480
        frames = []
        
        for i in range(30):  # 30 frames = ~1 second at 30fps
            img = Image.new('RGB', (width, height), color=(128, 0, 128))  # Purple
            draw = ImageDraw.Draw(img)
            
            # Add text
            try:
                font_title = ImageFont.truetype("arial.ttf", 40)
                font_small = ImageFont.truetype("arial.ttf", 24)
            except:
                font_title = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Draw title
            title = "Technoaiamaze"
            title_bbox = draw.textbbox((0, 0), title, font=font_title)
            title_width = title_bbox[2] - title_bbox[0]
            draw.text(((width - title_width) / 2, height / 2 - 50), title, fill=(255, 255, 255), font=font_title)
            
            # Draw subtitle
            subtitle = "Mock Video Generated"
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_small)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            draw.text(((width - subtitle_width) / 2, height / 2 + 20), subtitle, fill=(200, 200, 200), font=font_small)
            
            # Draw job ID
            job_text = f"Job: {job_id[:8]}"
            job_bbox = draw.textbbox((0, 0), job_text, font=font_small)
            job_width = job_bbox[2] - job_bbox[0]
            draw.text(((width - job_width) / 2, height / 2 + 60), job_text, fill=(180, 180, 180), font=font_small)
            
            frames.append(img)
        
        # Save as animated GIF first (then convert if needed)
        gif_path = output_dir / f"{job_id}.gif"
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0
        )
        
        # If we got here, return the GIF (browsers can play it)
        return gif_path
        
    except Exception as e:
        print(f"PIL fallback failed: {e}")
        pass
    
    # Last resort: Create a static image as PNG
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        img = Image.new('RGB', (640, 480), color=(128, 0, 128))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except:
            font = ImageFont.load_default()
        
        text = "Antigravity AI\nMock Video"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text(((640 - text_width) / 2, 200), text, fill=(255, 255, 255), font=font)
        
        png_path = output_dir / f"{job_id}.png"
        img.save(png_path)
        return png_path
        
    except:
        # Absolute last resort: Return a text file explaining the situation
        txt_path = output_dir / f"{job_id}.txt"
        with open(txt_path, 'w') as f:
            f.write(f"Antigravity AI Mock Video\n")
            f.write(f"Job ID: {job_id}\n\n")
            f.write(f"This is a placeholder because video generation libraries are not available.\n")
            f.write(f"Install ffmpeg or PIL (Pillow) for better mock videos.\n")
        return txt_path


@app.get("/api/v1/status/{job_id}")
async def get_job_status(job_id: str) -> JobStatus:
    """Get job status"""
    
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")
    
    job_data = jobs[job_id]
    
    return JobStatus(
        job_id=job_id,
        status=job_data["status"],
        progress=job_data.get("progress"),
        message=job_data.get("message"),
        result_url=job_data.get("result_url")
    )


@app.get("/api/v1/download/{job_id}")
async def download_video(job_id: str):
    """Download generated video file"""
    
    # Check if job exists in memory
    if job_id in jobs:
        job_data = jobs[job_id]
        
        if job_data["status"] != "completed":
            raise HTTPException(400, "Video not ready yet")
        
        video_path = job_data.get("video_path")
    else:
        # Job not in memory (server restarted), check disk directly
        video_path = None
        output_dir = Path("temp_videos")
        
        # Check for different file extensions
        for ext in ['.gif', '.mp4', '.png', '.txt']:
            potential_path = output_dir / f"{job_id}{ext}"
            if potential_path.exists():
                video_path = str(potential_path)
                break
    
    if not video_path or not Path(video_path).exists():
        raise HTTPException(404, "Video file not found")
    
    # Determine media type based on extension
    ext = Path(video_path).suffix.lower()
    media_types = {
        '.mp4': 'video/mp4',
        '.gif': 'image/gif',
        '.png': 'image/png',
        '.txt': 'text/plain'
    }
    media_type = media_types.get(ext, 'application/octet-stream')
    
    return FileResponse(
        video_path,
        media_type=media_type,
        filename=f"antigravity_video_{job_id[:8]}{ext}",
        headers={
            "Content-Disposition": f'attachment; filename="antigravity_video_{job_id[:8]}{ext}"'
        }
    )


@app.post("/api/v1/preview/keypoints")
async def preview_keypoints(image: UploadFile = File(...)) -> JSONResponse:
    """Mock keypoint preview"""
    
    return JSONResponse({
        "keypoints_count": 478,
        "confidence": 0.95,
        "face_bbox": [100, 100, 400, 500],
        "visualization_url": "https://via.placeholder.com/512x512/667eea/ffffff?text=Keypoints+Detected"
    })


@app.get("/api/v1/voices")
async def list_voices() -> JSONResponse:
    """List available voices"""
    
    return JSONResponse({
        "voices": [
            {
                "engine": "edge-tts",
                "voice": "en-US-AriaNeural",
                "category": "English (US)",
                "quality": "premium-equivalent"
            },
            {
                "engine": "edge-tts",
                "voice": "en-US-GuyNeural",
                "category": "English (US)",
                "quality": "premium-equivalent"
            }
        ],
        "archetypes": [
            "philosopher",
            "storyteller",
            "innovator",
            "narrator_male",
            "narrator_female",
            "indian_english"
        ]
    })




@app.get("/api/v1/voices/preview/{voice}")
async def preview_voice(voice: str):
    """Generate voice preview audio using edge-tts"""
    try:
        import edge_tts
        import tempfile
        import os
        
        # Create sample text for preview
        sample_text = "Hello! This is a preview of the selected voice for your video."
        
        # Create a temporary file for the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_path = temp_file.name
        
        # Generate TTS audio
        communicate = edge_tts.Communicate(sample_text, voice)
        await communicate.save(temp_path)
        
        # Return the audio file
        return FileResponse(
            temp_path,
            media_type='audio/mpeg',
            filename=f'preview_{voice}.mp3',
            background=None  # Don't delete file immediately
        )
    except ImportError:
        # Fallback if edge-tts not available
        raise HTTPException(
            status_code=501,
            detail="Voice preview requires edge-tts. Install with: pip install edge-tts"
        )
    except Exception as e:
        raise HTTPException(500, f"Voice preview failed: {str(e)}")


@app.post("/api/v1/avatars/generate")
async def generate_avatar(
    prompt: str = Form(...),
    style: str = Form("realistic")
) -> JSONResponse:
    """Mock avatar generation endpoint"""
    
    # Generate a unique job ID
    job_id = str(uuid.uuid4())
    
    # Use a free placeholder avatar service
    # DiceBear provides free avatar generation
    placeholder_url = f"https://api.dicebear.com/7.x/avataaars/png?seed={job_id}&size=512"
    
    return JSONResponse({
        "job_id": job_id,
        "status": "completed",
        "url": placeholder_url,
        "message": f"Generated mock avatar with style: {style}. Upload your own image for best results."
    })


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Antigravity AI Mock Backend...")
    print("⚠️  This is a MOCK server for testing the UI")
    print("📦 Install full dependencies for real video generation")
    print("")
    uvicorn.run(app, host="0.0.0.0", port=8000)
