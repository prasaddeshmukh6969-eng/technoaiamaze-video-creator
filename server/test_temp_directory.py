"""
Technoaiamaze - Temp Directory Verification Test
Tests Windows temp directory creation and file permissions
"""
import tempfile
from pathlib import Path
import sys

print("="*60)
print("TECHNOAIAMAZE TEMP DIRECTORY VERIFICATION")
print("="*60)
print()

try:
    # Test 1: Get temp directory
    print("[TEST 1/4] Getting Windows temp directory...")
    base_temp = tempfile.gettempdir()
    print(f"  ✅ Base Temp: {base_temp}")
    print()
    
    # Test 2: Create project temp directory
    print("[TEST 2/4] Creating project temp directory...")
    temp_dir = Path(base_temp) / "technoaiamaze"
    print(f"  Target: {temp_dir}")
    
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    if temp_dir.exists():
        print(f"  ✅ Directory created successfully")
    else:
        print(f"  ❌ Directory creation failed")
        sys.exit(1)
    print()
    
    # Test 3: Test write permissions
    print("[TEST 3/4] Testing write permissions...")
    test_file = temp_dir / "permission_test.txt"
    test_content = "Hello from Technoaiamaze!\nWindows compatibility test."
    
    test_file.write_text(test_content)
    
    if test_file.exists():
        size = test_file.stat().st_size
        print(f"  ✅ Write successful")
        print(f"  📁 File: {test_file}")
        print(f"  📏 Size: {size} bytes")
    else:
        print(f"  ❌ Write failed")
        sys.exit(1)
    print()
    
    # Test 4: Test read permissions
    print("[TEST 4/4] Testing read permissions...")
    read_content = test_file.read_text()
    
    if read_content == test_content:
        print(f"  ✅ Read successful")
        print(f"  Content matches: {len(read_content)} characters")
    else:
        print(f"  ❌ Read failed or content mismatch")
        sys.exit(1)
    print()
    
    # Cleanup
    print("[CLEANUP] Removing test file...")
    test_file.unlink()
    print(f"  ✅ Cleanup successful")
    print()
    
    # Summary
    print("="*60)
    print("🎉 ALL TESTS PASSED!")
    print("="*60)
    print()
    print("✅ Windows temp directory is accessible")
    print("✅ File read/write permissions work")
    print("✅ Path handling is correct")
    print()
    print(f"Your temp directory: {temp_dir}")
    print()
    print("You can proceed to install GPU dependencies.")
    print()
    
except Exception as e:
    print()
    print("="*60)
    print("❌ TEST FAILED")
    print("="*60)
    print(f"Error: {type(e).__name__}")
    print(f"Message: {str(e)}")
    print()
    import traceback
    traceback.print_exc()
    sys.exit(1)
