import sys

# Read the existing mock_server.py
with open('mock_server.py', 'r') as f:
    lines = f.readlines()

# Find the line with "if __name__"
insert_index = None
for i, line in enumerate(lines):
    if 'if __name__ == "__main__":' in line:
        insert_index = i
        break

if insert_index is None:
    print("ERROR: Could not find main block")
    sys.exit(1)

# New endpoints to add
new_endpoints = '''
@app.get("/api/v1/voices/preview/{voice}")
async def preview_voice(voice: str):
    """Generate voice preview audio - Mock endpoint"""
    # Not implemented in mock mode
    raise HTTPException(
        status_code=501,
        detail="Voice preview not available in mock mode. Please use generate page directly."
    )


@app.post("/api/v1/avatars/generate")
async def generate_avatar(
    prompt: str = Form(...),
    style: str = Form("realistic")
) -> JSONResponse:
    """Mock avatar generation endpoint"""
    
    job_id = str(uuid.uuid4())
    
    # Use a free placeholder service
    placeholder_url = f"https://api.dicebear.com/7.x/avataaars/png?seed={job_id}&size=512"
    
    return JSONResponse({
        "job_id": job_id,
        "status": "completed",
        "url": placeholder_url,
        "message": f"Generated mock avatar with style: {style}"
    })


'''

# Insert the new endpoints before the main block
new_lines = lines[:insert_index] + [new_endpoints] + lines[insert_index:]

# Write back
with open('mock_server.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Successfully added missing endpoints to mock_server.py")
