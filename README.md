# Technoaiamaze - AI Video Creator

Professional anime-style marketing video platform optimized for the Indian market.

## 🌟 Features

- 17 Indian languages with smart code-mixing
- AI-powered script generation
- Professional voice synthesis
- Duration control (30s - 5min)
- Brand asset management
- Full-screen optimized UI

## 🚀 Quick Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

## 📦 Tech Stack

**Frontend:** Next.js 14, React, TypeScript, Tailwind CSS, Framer Motion  
**Backend:** FastAPI, Edge-TTS, Python 3.11+  
**Storage:** MinIO (optional), Local filesystem  
**Queue:** Redis (for production video generation)

## 🔧 Environment Variables

### Backend (.env)
```env
REDIS_URL=redis://localhost:6379
USE_EDGE_TTS=true
USE_COQUI_TTS=false
```

### Frontend (.env.production)
```env
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

## 📖 Documentation

- [Deployment Guide](DEPLOYMENT.md)
- [User Guide](docs/user_guide.md)
- [API Documentation](docs/api.md)

## 🎯 Local Development

```bash
# Backend
cd server
pip install -r requirements.txt
python -m uvicorn mock_server:app --reload --port 8000

# Frontend
cd client
npm install
npm run dev
```

## 📄 License

Proprietary - Technoaiamaze

## 🤝 Support

For issues and questions, please contact support.

---

Made with ❤️ for the Indian Market
