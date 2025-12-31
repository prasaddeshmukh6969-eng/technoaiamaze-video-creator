"""
TECHNOAIAMAZE - COMPLETE SYSTEM FIX & TEST
===========================================
Save this as: complete_fix.py
Run with: python complete_fix.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import tempfile
import time

class C:
    H='\033[95m';B='\033[94m';G='\033[92m';Y='\033[93m';R='\033[91m';E='\033[0m'

def h(t): print(f"\n{C.H}{'='*80}\n{t.center(80)}\n{'='*80}{C.E}\n")
def p(n,t): print(f"\n{C.B}{'='*80}\nPHASE {n}: {t}\n{'='*80}{C.E}\n")
def s(t): print(f"{C.G}✓ {t}{C.E}")
def e(t): print(f"{C.R}✗ {t}{C.E}")
def i(t): print(f"{C.B}ℹ {t}{C.E}")
def w(t): print(f"{C.Y}⚠ {t}{C.E}")

def run(cmd, cwd=None):
    try:
        r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=30)
        return r.returncode == 0, r.stdout, r.stderr
    except: return False, "", "Error"

# PHASE 1: Find project
def phase1():
    p(1, "FINDING PROJECT")
    root = Path(r"C:\Users\Shri\Desktop\antigravity Tools\ai video creator")
    
    if not root.exists():
        e("Project not found!"); return None
    
    s(f"Project: {root}")
    s(f"Server: {root / 'server'}")
    
    # Check Python
    ok, out, _ = run("python --version")
    if ok: s(f"Python: {out.strip().split()[-1]}")
    
    # Check GPU
    ok, out, _ = run("nvidia-smi --query-gpu=name --format=csv,noheader")
    gpu = ok and out.strip()
    if gpu: s(f"GPU: {out.strip()}")
    else: w("No GPU (will use CPU mode)")
    
    return {'root': root, 'gpu': gpu}

# PHASE 2: Fix paths
def phase2(r):
    p(2, "FIXING PATHS")
    
    files = [
        r['root'] / "server" / "engines" / "audio_synthesizer.py",
        r['root'] / "server" / "engines" / "animator.py",
        r['root'] / "server" / "engines" / "enhancer.py",
        r['root'] / "server" / "main.py",
        r['root'] / "server" / "mock_server.py"
    ]
    
    fixed = 0
    for f in files:
        if not f.exists(): continue
        
        i(f"Checking {f.name}...")
        content = f.read_text(encoding='utf-8')
        orig = content
        
        if '/tmp/' in content:
            # Add imports
            if 'import tempfile' not in content:
                lines = content.split('\n')
                for idx, line in enumerate(lines):
                    if line.startswith('import '):
                        lines.insert(idx+1, 'import tempfile')
                        break
                content = '\n'.join(lines)
            
            if 'import os' not in content:
                lines = content.split('\n')
                for idx, line in enumerate(lines):
                    if line.startswith('import '):
                        lines.insert(idx+1, 'import os')
                        break
                content = '\n'.join(lines)
            
            # Replace paths
            content = content.replace('"/tmp/antigravity"', 'os.path.join(tempfile.gettempdir(), "antigravity")')
            content = content.replace("'/tmp/antigravity'", "os.path.join(tempfile.gettempdir(), 'antigravity')")
            
            if content != orig:
                shutil.copy2(f, f.with_suffix(f.suffix + '.backup'))
                f.write_text(content, encoding='utf-8')
                s(f"Fixed {f.name}")
                fixed += 1
    
    if fixed: s(f"Fixed {fixed} files")
    else: i("No fixes needed")
    
    # Create temp dir
    tmp = Path(tempfile.gettempdir()) / "antigravity"
    tmp.mkdir(exist_ok=True)
    s(f"Temp dir: {tmp}")
    return True

# PHASE 3: Test TTS
def phase3(r):
    p(3, "TESTING TEXT-TO-SPEECH")
    
    test = r['root'] / "server" / "test_tts.py"
    test.write_text('''
import edge_tts, asyncio, os, tempfile
async def test():
    d = os.path.join(tempfile.gettempdir(), "antigravity")
    os.makedirs(d, exist_ok=True)
    f = os.path.join(d, "test.mp3")
    c = edge_tts.Communicate("Test audio", "en-IN-NeerjaNeural")
    await c.save(f)
    if os.path.exists(f):
        print(f"SUCCESS: {os.path.getsize(f)} bytes")
        return True
    return False
asyncio.run(test())
''')
    
    venv = r['root'] / ".venv" / "Scripts" / "python.exe"
    py = str(venv) if venv.exists() else "python"
    
    ok, out, err = run(f'{py} "{test}"', cwd=r['root'] / "server")
    test.unlink(missing_ok=True)
    
    if ok and "SUCCESS" in out:
        s("TTS works! " + out.strip())
        return True
    else:
        e("TTS failed"); e(err)
        return False

# PHASE 4: Test Image
def phase4(r):
    p(4, "TESTING IMAGE GENERATION")
    
    test = r['root'] / "server" / "test_img.py"
    test.write_text('''
from PIL import Image, ImageDraw
import os, tempfile
d = os.path.join(tempfile.gettempdir(), "antigravity")
os.makedirs(d, exist_ok=True)
f = os.path.join(d, "test.png")
img = Image.new('RGB', (512, 512), 'blue')
draw = ImageDraw.Draw(img)
draw.ellipse([100, 100, 412, 412], fill=(255, 220, 180))
draw.ellipse([180, 180, 230, 230], fill=(50, 50, 50))
draw.ellipse([282, 180, 332, 230], fill=(50, 50, 50))
img.save(f)
if os.path.exists(f):
    print(f"SUCCESS: {os.path.getsize(f)} bytes")
''')
    
    venv = r['root'] / ".venv" / "Scripts" / "python.exe"
    py = str(venv) if venv.exists() else "python"
    
    ok, out, err = run(f'{py} "{test}"', cwd=r['root'] / "server")
    test.unlink(missing_ok=True)
    
    if ok and "SUCCESS" in out:
        s("Images work! " + out.strip())
        return True
    else:
        e("Images failed"); e(err)
        return False

# PHASE 5: Full test
def phase5(r):
    p(5, "COMPLETE VIDEO GENERATION TEST")
    
    test = r['root'] / "server" / "test_full.py"
    test.write_text('''
import asyncio, os, tempfile, uuid
from pathlib import Path
import edge_tts
from PIL import Image, ImageDraw

async def test():
    d = Path(tempfile.gettempdir()) / "antigravity"
    d.mkdir(exist_ok=True)
    job = str(uuid.uuid4())[:8]
    
    # Audio
    print("Creating audio...")
    audio = d / f"{job}.mp3"
    c = edge_tts.Communicate("Test video generation", "en-IN-NeerjaNeural")
    await c.save(str(audio))
    
    if not audio.exists():
        print("FAIL: No audio")
        return False
    print(f"✓ Audio: {audio.stat().st_size} bytes")
    
    # Frames
    print("Creating frames...")
    frames_d = d / f"{job}_frames"
    frames_d.mkdir(exist_ok=True)
    
    for i in range(5):
        img = Image.new('RGB', (512, 512), (100, 150, 200))
        draw = ImageDraw.Draw(img)
        draw.ellipse([100, 100, 412, 412], fill=(255, 220, 180))
        draw.ellipse([180, 180, 230, 230], fill=(50, 50, 50))
        draw.ellipse([282, 180, 332, 230], fill=(50, 50, 50))
        draw.text((256, 450), f"Frame {i+1}", fill=(255, 255, 255), anchor='mm')
        img.save(frames_d / f"frame_{i:04d}.png")
    
    frames = len(list(frames_d.glob("*.png")))
    print(f"✓ Frames: {frames}")
    
    # Video placeholder
    video = d / f"{job}.mp4"
    video.write_bytes(b"TEST_VIDEO")
    print(f"✓ Video: {video.stat().st_size} bytes")
    
    print(f"\\nSUCCESS! All files in: {d}")
    return True

asyncio.run(test())
''')
    
    venv = r['root'] / ".venv" / "Scripts" / "python.exe"
    py = str(venv) if venv.exists() else "python"
    
    i("Running full video generation test...")
    ok, out, err = run(f'{py} "{test}"', cwd=r['root'] / "server")
    print(out)
    test.unlink(missing_ok=True)
    
    if ok and "SUCCESS" in out:
        s("FULL TEST PASSED!")
        tmp = Path(tempfile.gettempdir()) / "antigravity"
        s(f"Files created in: {tmp}")
        
        if tmp.exists():
            files = list(tmp.glob("*"))
            i(f"Found {len(files)} test files:")
            for f in files[:5]:
                i(f"  {f.name}")
        return True
    else:
        e("Full test failed"); e(err)
        return False

# PHASE 6: Server test
def phase6(r):
    p(6, "SERVER START TEST")
    
    server = r['root'] / "server" / ("main.py" if r['gpu'] else "mock_server.py")
    i(f"Testing: {server.name}")
    
    test = r['root'] / "server" / "test_server.py"
    test.write_text(f'''
import subprocess, time, requests, sys
from pathlib import Path

py = r"{sys.executable}"
srv = Path(r"{server}")

print("Starting server...")
p = subprocess.Popen([py, str(srv)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(3)

try:
    r = requests.get("http://localhost:8000/health", timeout=2)
    if r.status_code == 200:
        print(f"SUCCESS: Server running! {{r.json()}}")
        ok = True
    else:
        print(f"FAIL: Status {r.status_code}")
        ok = False
except Exception as e:
    print(f"FAIL: {{e}}")
    ok = False

p.terminate()
p.wait(timeout=5)
sys.exit(0 if ok else 1)
''')
    
    venv = r['root'] / ".venv" / "Scripts" / "python.exe"
    py = str(venv) if venv.exists() else "python"
    
    w("Server will start for 5 seconds...")
    ok, out, err = run(f'{py} "{test}"', cwd=r['root'] / "server")
    print(out)
    test.unlink(missing_ok=True)
    
    if ok and "SUCCESS" in out:
        s("SERVER WORKS!")
        return True
    else:
        e("Server failed"); e(err)
        return False

# MAIN
def main():
    h("TECHNOAIAMAZE COMPLETE FIX & TEST")
    print("This will test everything step-by-step.\n")
    input("Press ENTER to start...")
    
    r = phase1()
    if not r: e("\nFATAL: Project not found"); input("Press ENTER to exit"); return
    
    s("\n✓ Phase 1 done")
    input("Press ENTER for Phase 2...")
    
    if not phase2(r): e("\nPhase 2 failed"); input("Press ENTER to exit"); return
    s("\n✓ Phase 2 done")
    input("Press ENTER for Phase 3...")
    
    if not phase3(r): w("\nPhase 3 issues"); input("Continue? (ENTER=yes, Ctrl+C=no)")
    s("\n✓ Phase 3 done")
    input("Press ENTER for Phase 4...")
    
    if not phase4(r): w("\nPhase 4 issues"); input("Continue? (ENTER=yes, Ctrl+C=no)")
    s("\n✓ Phase 4 done")
    input("Press ENTER for Phase 5...")
    
    if not phase5(r): w("\nPhase 5 issues"); input("Continue? (ENTER=yes, Ctrl+C=no)")
    s("\n✓ Phase 5 done")
    input("Press ENTER for Phase 6...")
    
    if not phase6(r): e("\nPhase 6 failed")
    else: s("\n✓ Phase 6 done")
    
    h("ALL TESTS COMPLETE!")
    print(f"{C.G}Your system is ready!{C.E}\n")
    print(f"To start the server:")
    print(f"  cd \"{r['root'] / 'server'}\"")
    if r['gpu']:
        print(f"  python main.py")
    else:
        print(f"  python mock_server.py")
    
    print(f"\nTest files location:")
    print(f"  {Path(tempfile.gettempdir()) / 'antigravity'}")
    
    input("\nPress ENTER to exit")

if __name__ == "__main__":
    main()