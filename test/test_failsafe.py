import asyncio
import os
import sys
from pathlib import Path
import shutil

# Add server directory to path
sys.path.append(os.path.join(os.getcwd(), "server"))

# Set dummy env vars for Settings validation
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["REDIS_URL"] = "redis://localhost:6379/0"
os.environ["MINIO_ENDPOINT"] = "localhost:9000"
os.environ["MINIO_ACCESS_KEY"] = "minioadmin"
os.environ["MINIO_SECRET_KEY"] = "minioadmin"
os.environ["JWT_SECRET"] = "testsecret"

from routers import v1_generation
from engines import animator

# Mock the animator to simulate failure in real mode
# animator imported from engines is the INSTANCE
original_generate = animator.generate_animation

async def mock_generate_animation(image_path, audio_path, output_path, pose_intensity=1.0, fps=25, options=None):
    options = options or {}
    mode = options.get("mode", "real")
    
    # log_print is not available here, use print
    print(f"Mock Animator called with mode={mode}")
    
    if mode == "real":
        print("Simulating REAL mode FAILURE")
        raise Exception("Simulated LivePortrait Crash")
    
    if mode == "anime":
        print("Simulating ANIME mode SUCCESS")
        # Create a dummy video file
        with open(output_path, "w") as f:
            f.write("dummy video content")
        return {"status": "success", "video_path": output_path}

# Patch the animator instance directly
animator.generate_animation = mock_generate_animation

# Mock audio synthesizer
from engines import audio_synthesizer
async def mock_synthesize(text, output_path, archetype=None, language=None):
    print("Mock Audio Synthesis")
    with open(output_path, "w") as f:
        f.write("dummy audio")
    return {"audio_path": output_path, "duration": 5.0}

audio_synthesizer.synthesize = mock_synthesize

async def test_failsafe():
    log_file = "test_result.log"
    with open(log_file, "w", encoding="utf-8") as log:
        def log_print(*args):
            print(*args)
            print(*args, file=log)
            
        log_print("--- Starting Failsafe Test ---")
        
        # Setup temp dir
        job_id = "test_failsafe_job"
        temp_dir = Path(v1_generation.TEMP_DIR)
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Create dummy input image
        image_path = temp_dir / f"{job_id}_input.jpg"
        with open(image_path, "w") as f:
            f.write("dummy image")
            
        # Run the task
        log_print("Running process_video_generation_task in REAL mode...")
        try:
            await v1_generation.process_video_generation_task(
                job_id=job_id,
                image_path=str(image_path),
                text="Hello world",
                archetype="narrator",
                pose_intensity=1.0,
                language="en",
                enhance=False,
                mode="real" # Request REAL mode
            )
        except Exception as e:
            log_print(f"EXCEPTION in task: {e}")
            import traceback
            traceback.print_exc(file=log)
        
        # Check result
        final_path = temp_dir / f"{job_id}_final.mp4"
        meta_path = temp_dir / f"{job_id}_meta.json"
        
        if final_path.exists():
            log_print("SUCCESS: Final video exists")
        else:
            log_print("FAILURE: Final video missing")
            
        if meta_path.exists():
            import json
            with open(meta_path) as f:
                meta = json.load(f)
            log_print("Metadata: " + json.dumps(meta, indent=2))
            
            if meta.get("fallback_used") is True:
                log_print("SUCCESS: Fallback was triggered")
            else:
                log_print("FAILURE: Fallback NOT triggered")
                
            if meta.get("final_state") == "VIDEO_READY":
                 log_print("SUCCESS: Final state is VIDEO_READY")
            else:
                 log_print("FAILURE: Final state is not VIDEO_READY")
        else:
            log_print("FAILURE: Metadata missing")

if __name__ == "__main__":
    asyncio.run(test_failsafe())
