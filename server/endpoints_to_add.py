

@app.get("/api/v1/voices/preview/{voice}")
async def preview_voice(voice: str):
    """Generate voice preview audio - Mock implementation"""
    # In a real implementation, this would use edge-tts to generate a preview
    # For mock mode, we'll return a 501 Not Implemented status
    raise HTTPException(
        status_code=501,
        detail="Voice preview not available in mock mode. Please select a voice and generate your video to hear it."
    )


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
