"""
Technoaiamaze - Component Testing Script
Tests each component independently before full integration
"""
import asyncio
import sys
from pathlib import Path
import tempfile

# Setup temp directory
TEMP_DIR = Path(tempfile.gettempdir()) / "technoaiamaze_test"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

print("="*70)
print("TECHNOAIAMAZE COMPONENT TEST SUITE")
print("="*70)
print(f"Temp Directory: {TEMP_DIR}")
print()

# Track results
test_results = {}


async def test_file_permissions():
    """Test 1: File creation and cleanup"""
    print("[TEST 1/4] File Permissions Test")
    print("-" * 70)
    try:
        test_file = TEMP_DIR / "permission_test.txt"
        test_content = "Permission test - Technoaiamaze"
        
        # Write test
        test_file.write_text(test_content)
        print(f"  ✅ Write successful: {test_file}")
        
        # Read test
        if test_file.exists():
            content = test_file.read_text()
            if content == test_content:
                print(f"  ✅ Read successful: {len(content)} bytes")
            else:
                print(f"  ❌ Content mismatch")
                return False
        
        # Cleanup test
        test_file.unlink()
        print(f"  ✅ Cleanup successful")
        
        print("  ✅ RESULT: PASSED")
        return True
        
    except Exception as e:
        print(f"  ❌ ERROR: {type(e).__name__}: {str(e)}")
        print("  ❌ RESULT: FAILED")
        return False
    finally:
        print()


async def test_gpu_availability():
    """Test 2: GPU detection and CUDA availability"""
    print("[TEST 2/4] GPU Availability Test")
    print("-" * 70)
    try:
        import torch
        
        print(f"  📦 PyTorch Version: {torch.__version__}")
        print(f"  📦 CUDA Version (PyTorch): {torch.version.cuda}")
        
        cuda_available = torch.cuda.is_available()
        
        if cuda_available:
            device_name = torch.cuda.get_device_name(0)
            device_count = torch.cuda.device_count()
            print(f"  ✅ CUDA Available: YES")
            print(f"  🎮 GPU Device: {device_name}")
            print(f"  🎮 GPU Count: {device_count}")
            print("  ✅ RESULT: PASSED (GPU Mode)")
        else:
            print(f"  ⚠️  CUDA Available: NO")
            print(f"  💻 Mode: CPU Only")
            print(f"  ⚠️  WARNING: Video generation will be VERY slow")
            print("  ✅ RESULT: PASSED (CPU Mode)")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ PyTorch not installed")
        print(f"  ❌ Run install_gpu_deps.bat first")
        print("  ❌ RESULT: FAILED")
        return False
    except Exception as e:
        print(f"  ❌ ERROR: {type(e).__name__}: {str(e)}")
        print("  ❌ RESULT: FAILED")
        return False
    finally:
        print()


async def test_audio_synthesis():
    """Test 3: Audio generation engine"""
    print("[TEST 3/4] Audio Synthesis Test")
    print("-" * 70)
    try:
        # Import audio synthesizer
        print(f"  📥 Importing audio_synthesizer...")
        sys.path.insert(0, str(Path(__file__).parent))
        from engines.audio_synthesizer import audio_synthesizer
        print(f"  ✅ Import successful")
        
        # Generate audio
        test_text = "Hello, this is a test of the Technoaiamaze audio synthesis engine."
        output_path = str(TEMP_DIR / "test_audio.wav")
        
        print(f"  🎤 Generating audio...")
        print(f"  Text: \"{test_text[:50]}...\"")
        
        result = await audio_synthesizer.synthesize(
            text=test_text,
            output_path=output_path,
            archetype="narrator_male"
        )
        
        # Verify output
        audio_file = Path(result["audio_path"])
        
        if audio_file.exists():
            size = audio_file.stat().st_size
            print(f"  ✅ Audio generated successfully")
            print(f"  📁 Location: {audio_file}")
            print(f"  📏 Size: {size:,} bytes")
            print(f"  ⏱️  Duration: {result['duration']:.2f}s")
            print(f"  🎵 Voice: {result['voice_used']}")
            print(f"  🔧 Engine: {result['engine']}")
            print("  ✅ RESULT: PASSED")
            return True
        else:
            print(f"  ❌ Audio file not created")
            print("  ❌ RESULT: FAILED")
            return False
            
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        print(f"  ❌ Make sure you're running from server directory")
        print("  ❌ RESULT: FAILED")
        return False
    except Exception as e:
        print(f"  ❌ ERROR: {type(e).__name__}: {str(e)}")
        import traceback
        print()
        traceback.print_exc()
        print("  ❌ RESULT: FAILED")
        return False
    finally:
        print()


async def test_animator_import():
    """Test 4: Animator engine import (not full generation)"""
    print("[TEST 4/4] Animator Import Test")
    print("-" * 70)
    try:
        print(f"  📥 Importing animator...")
        sys.path.insert(0, str(Path(__file__).parent))
        from engines.animator import animator
        print(f"  ✅ Import successful")
        
        print(f"  📦 Animator type: {type(animator).__name__}")
        print(f"  📦 Engine: {type(animator.engine).__name__}")
        
        print("  ✅ RESULT: PASSED")
        print("  ℹ️  Note: Full animation test requires image + audio")
        return True
        
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        print("  ❌ RESULT: FAILED")
        return False
    except Exception as e:
        print(f"  ❌ ERROR: {type(e).__name__}: {str(e)}")
        print("  ❌ RESULT: FAILED")
        return False
    finally:
        print()


async def main():
    global test_results
    
    print("Starting component tests...")
    print()
    
    # Run all tests
    test_results["permissions"] = await test_file_permissions()
    test_results["gpu"] = await test_gpu_availability()
    test_results["audio"] = await test_audio_synthesis()
    test_results["animator"] = await test_animator_import()
    
    # Summary
    print("="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed_count = sum(1 for result in test_results.values() if result)
    total_count = len(test_results)
    
    for test_name, passed in test_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name.upper():20s}: {status}")
    
    print()
    print(f"  Results: {passed_count}/{total_count} tests passed")
    print()
    
    if all(test_results.values()):
        print("="*70)
        print("🎉 ALL TESTS PASSED - SYSTEM READY!")
        print("="*70)
        print()
        print("Next steps:")
        print("  1. Run test_full.py for end-to-end video generation test")
        print("  2. Start backend with: python main.py")
        print()
    else:
        print("="*70)
        print("⚠️  SOME TESTS FAILED")
        print("="*70)
        print()
        
        if not test_results["gpu"]:
            print("❌ GPU Test Failed:")
            print("   - Run install_gpu_deps.bat to install PyTorch with CUDA")
            print()
        
        if not test_results["audio"]:
            print("❌ Audio Test Failed:")
            print("   - Check if dependencies are installed: pip install -r requirements.txt")
            print("   - Make sure you're in the server directory")
            print()
        
        print("Review error messages above for details.")
        print()
    
    print(f"Test files location: {TEMP_DIR}")
    print()
    
    return 0 if all(test_results.values()) else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
