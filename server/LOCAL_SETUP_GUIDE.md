# Local GPU Testing Configuration

## Environment Variables

Copy this content to your `.env` file in the `server` directory:

```env
# Edge-TTS (Free, Premium Quality)
USE_EDGE_TTS=true
USE_COQUI_TTS=false

# Database (Required by config.py, even if not used)
DATABASE_URL=sqlite:///./test.db
REDIS_URL=redis://localhost:6379
JWT_SECRET=test-secret-for-local-dev-only

# MinIO (Optional for local testing)
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# GPU Configuration
CUDA_VISIBLE_DEVICES=0
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# Hugging Face (Optional - for LivePortrait Space access)
# Get free token from: https://huggingface.co/settings/tokens
# HF_TOKEN=your_token_here

# GFPGAN Weights (Skip for quick test)
GFPGAN_WEIGHTS=./weights/GFPGANv1.4.pth

# LivePortrait Weights (Not needed - uses HF Space API)
LIVEPORTRAIT_WEIGHTS=./weights/liveportrait

# CORS - Add localhost for testing
CORS_ORIGINS=http://localhost:3000,https://ai.technoamaze.in
```

## Setup Steps

1. Copy the above content to `server/.env`
2. Run `setup_local.bat` to install dependencies and start the server
3. The server will use Hugging Face Spaces for LivePortrait animation (free)
4. Without GFPGAN weights, enhancement will be skipped (still works)
