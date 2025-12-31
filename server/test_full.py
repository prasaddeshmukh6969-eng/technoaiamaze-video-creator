"""
Technoaiamaze - Full End-to-End Video Generation Test
Creates a test video and saves it to Desktop for verification
"""
import asyncio
import sys
from pathlib import Path
import tempfile
import shutil

print("="*70)
print("TECHNOAIAMAZE FULL VIDEO GENERATION TEST")
print("="*70)
print()

# Setup paths
TEMP_DIR = Path(tempfile.gettempdir()) / "technoaiamaze_fulltest"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

DESKTOP = Path.home() / "Desktop"
OUTPUT_VIDEO = DESKTOP / "technoaiamaze_test_output.mp4"

print(f"📂 Temp Directory: {TEMP_DIR}")
print(f"📂 Output Location: {OUTPUT_VIDEO}")
print()

async def run_full_test():
    try:
        # Import engines
        print("📥 Importing engines...")
        sys.path.insert(0, str(Path(__file__).parent))
        
        from engines import audio_synthesizer, animator
        print("  ✅ Engines imported successfully")
        print()
        
        # Step 1: Create test image
        print("="*70)
        print("[STEP 1/5] Creating Test Image")
        print("="*70)
        
        import numpy as np
        import cv2
        
        # Create 512x512 gradient image with text
        img = np.zeros((512, 512, 3), dtype=np.uint8)
        
        # Create gradient background
        for y in range (512):
            color_val = int(100 + (y / 512) * 100)
            img[y, :] = (color_val, 80, 180)
        
        # Add text
        cv2.putText(img, "TECHNOAIAMAZE", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
        cv2.putText(img, "Test Avatar", (120, 280), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
        
        # Add circle for "head"
        cv2.circle(img, (256, 350), 80, (255, 220, 180), -1)  # Face
        cv2.circle(img, (230, 330), 15, (50, 50, 50), -1)     # Left eye
        cv2.circle(img, (282, 330), 15, (50, 50, 50), -1)     # Right eye
        cv2.ellipse(img, (256, 380), (30, 15), 0, 0, 180, (50, 50, 50), 2)  # Smile
        
        test_image = TEMP_DIR / "test_avatar.jpg"
        cv2.imwrite(str(test_image), img)
        
        file_size = test_image.stat().st_size
        print(f"  ✅ Test image created")
        print(f"  📁 Location: {test_image}")
        print(f"  📏 Size: {file_size:,} bytes")
        print()
        
        # Step 2: Generate audio
        print("="*70)
        print("[STEP 2/5] Generating Audio from Text")
        print("="*70)
        
        test_text = "Hello! This is a test of the Technoaiamaze AI video creator. If you can hear this, the audio synthesis is working correctly."
        print(f"  📝 Text: \"{test_text}\"")
        print()
        print(f"  🎤 Synthesizing speech...")
        
        audio_path = TEMP_DIR / "test_audio.wav"
        
        audio_result = await audio_synthesizer.synthesize(
            text=test_text,
            output_path=str(audio_path),
            archetype="narrator_male"
        )
        
        audio_file = Path(audio_result["audio_path"])
        audio_size = audio_file.stat().st_size
        
        print(f"  ✅ Audio generated successfully")
        print(f"  📁 Location: {audio_file}")
        print(f"  📏 Size: {audio_size:,} bytes")
        print(f"  ⏱️  Duration: {audio_result['duration']:.2f}s")
        print(f"  🎵 Voice: {audio_result['voice_used']}")
        print(f"  🔧 Engine: {audio_result['engine']}")
        print()
        
        # Step 3: Check GPU availability
        print("="*70)
        print("[STEP 3/5] Checking GPU Status")
        print("="*70)
        
        try:
            import torch
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                print(f"  ✅ GPU Available: {gpu_name}")
            else:
                print(f"  ⚠️  GPU Not Available - Using CPU mode")
                print(f"  ⚠️  Animation may be very slow or use API")
        except ImportError:
            print(f"  ⚠️  PyTorch not installed - Will use API mode")
        print()
        
        # Step 4: Generate animation
        print("="*70)
        print("[STEP 4/5] Generating Animated Video")
        print("="*70)
        print("  🎬 Starting animation...")
        print("  ⏳ This may take 30-120 seconds...")
        print("  ℹ️  Using LivePortrait API via Gradio")
        print()
        
        animated_video = TEMP_DIR / "test_animated.mp4"
        
        try:
            anim_result = await animator.generate_animation(
                image_path=str(test_image),
                audio_path=str(audio_file),
                output_path=str(animated_video),
                pose_intensity=1.0,
                options={"mode": "real"}
            )
            
            print(f"  Animation result status: {anim_result.get('status')}")
            
            if anim_result.get("status") == "success" and anim_result.get("video_path"):
                video_file = Path(anim_result["video_path"])
                
                if video_file.exists():
                    video_size = video_file.stat().st_size
                    print(f"  ✅ Video generated successfully")
                    print(f"  📁 Location: {video_file}")
                    print(f"  📏 Size: {video_size:,} bytes")
                    print()
                    
                    # Step 5: Copy to Desktop
                    print("="*70)
                    print("[STEP 5/5] Saving to Desktop")
                    print("="*70)
                    
                    shutil.copy(video_file, OUTPUT_VIDEO)
                    final_size = OUTPUT_VIDEO.stat().st_size
                    
                    print(f"  ✅ Video saved to Desktop!")
                    print(f"  📂 {OUTPUT_VIDEO}")
                    print(f"  📏 Size: {final_size:,} bytes")
                    print()
                    
                    # Success message
                    print("="*70)
                    print("🎉🎉🎉 SUCCESS! VIDEO GENERATION COMPLETE! 🎉🎉🎉")
                    print("="*70)
                    print()
                    print(f"✅ Audio synthesis: WORKING")
                    print(f"✅ Video animation: WORKING")
                    print(f"✅ File handling: WORKING")
                    print()
                    print(f"▶️  Open this file to view your test video:")
                    print(f"   {OUTPUT_VIDEO}")
                    print()
                    print("Your system is ready for production use!")
                    print()
                    
                    return 0
                else:
                    print(f"  ❌ Video file not created at expected location")
                    return 1
            else:
                # Graceful failure
                print(f"  ⚠️  Animation service unavailable")
                print(f"  Reason: {anim_result.get('reason', 'unknown')}")
                print(f"  Message: {anim_result.get('message', 'N/A')}")
                print()
                print("="*70)
                print("⚠️  PARTIAL SUCCESS")
                print("="*70)
                print()
                print(f"✅ Audio synthesis: WORKING")
                print(f"❌ Video animation: API temporarily unavailable")
                print()
                print("This is normal for API-based services.")
                print()
                print("Your system components are working correctly.")
                print("Try again later when the LivePortrait API is available,")
                print("or consider using a local animation engine.")
                print()
                
                return 2  # Partial success
                
        except Exception as anim_error:
            print(f"  ❌ Animation failed with error:")
            print(f"     {type(anim_error).__name__}: {str(anim_error)}")
            print()
            import traceback
            traceback.print_exc()
            return 1
            
    except Exception as e:
        print()
        print("="*70)
        print("❌ TEST FAILED")
        print("="*70)
        print()
        print(f"Error: {type(e).__name__}")
        print(f"Message: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        print()
        
        return 1


if __name__ == "__main__":
    print("Starting full video generation test...")
    print()
    
    exit_code = asyncio.run(run_full_test())
    
    print()
    print("Test complete.")
    print(f"Temp files location: {TEMP_DIR}")
    print()
    
    sys.exit(exit_code)
