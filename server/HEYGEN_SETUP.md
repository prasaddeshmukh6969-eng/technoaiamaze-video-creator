# HeyGen API Integration - Quick Setup Guide

## 🎯 What Changed

We've integrated **HeyGen API** as your primary video generation engine, with LivePortrait as automatic fallback.

**Benefits:**
- ✅ **10 free videos/month** (HeyGen free tier)
- ✅ **Reliable** (no more mock videos)
- ✅ **Production-ready** quality
- ✅ **Automatic fallback** to LivePortrait if HeyGen quota exhausted

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Get HeyGen API Key (FREE)

1. Go to https://app.heygen.com/
2. Sign up (free account)
3. Navigate to **API** section
4. Generate your API key
5. **Free tier**: 10 API credits/month (= 10 short videos)

### Step 2: Configure Environment

Add to your `.env` file:

```bash
# HeyGen API Configuration
HEYGEN_API_KEY=your_api_key_here

# Animation Engine Selection
# Options: "heygen" (recommended), "liveportrait" (free but unreliable)
ANIMATION_ENGINE=heygen
```

### Step 3: Install Dependencies

```bash
cd server
pip install aiohttp
```

### Step 4: Test It

```bash
python main.py
```

Visit http://localhost:8000/health - should show HeyGen engine status

---

## 💰 Pricing Tiers

| Plan | Cost | Credits | Videos/Month |
|------|------|---------|--------------|
| **Free** | $0 | 10 | ~10 short videos |
| **Pro** | $99/mo | 100 | ~100 videos |
| **Scale** | $330/mo | 660 | ~660 videos |

**1 credit = 1 minute of video generation**

---

## 🔄 Engine Fallback System

The system now supports **automatic fallback**:

1. **Primary**: HeyGen API (if API key configured)
2. **Fallback**: LivePortrait/HuggingFace (if HeyGen fails or quota exceeded)
3. **Result**: You always get a video (or clear error message)

---

## ⚙️ Configuration Options

### Use HeyGen Only (Recommended for Production)

```bash
ANIMATION_ENGINE=heygen
HEYGEN_API_KEY=your_key_here
```

### Use LivePortrait Only (Free but Unreliable)

```bash
ANIMATION_ENGINE=liveportrait
# No API key needed, but expect failures
```

### Hybrid (Best of Both)

```bash
ANIMATION_ENGINE=heygen
HEYGEN_API_KEY=your_key_here
# Automatically falls back to LivePortrait if HeyGen unavailable
```

---

## 📊 Monitoring Usage

Check your HeyGen dashboard to track:
- Credits used
- Credits remaining
- Video generation history

**Free tier quota resets monthly!**

---

## 🐛 Troubleshooting

### "API key not configured" Error

**Solution**: Add `HEYGEN_API_KEY` to `.env` file

### "Failed to upload asset" Error

**Solution**: Check your API key is valid and has credits remaining

### "Quota exceeded" Error

**Solution**: System automatically falls back to LivePortrait, or upgrade plan

### Still Getting Mock Videos?

**Check:**
1. `HEYGEN_API_KEY` is set in `.env`
2. `.env` file is in `server/` directory
3. Restart the server after adding API key

---

## 🎓 What Was Changed

### New Files:
- `server/engines/heygen_wrapper.py` - HeyGen API integration

### Modified Files:
- `server/core/config.py` - Added HEYGEN_API_KEY and ANIMATION_ENGINE
- `server/engines/animator.py` - Multi-engine support with fallback

### Unchanged:
- ✅ Frontend (works exactly the same)
- ✅ API endpoints (no changes needed)
- ✅ Audio generation (still using Edge-TTS)
- ✅ User experience (seamless upgrade)

---

## 🎉 Expected Results

**Before (with mock server):**
- Static placeholder videos
- No real animation

**After (with HeyGen):**
- Real talking head animation
- Lip-sync with audio
- Professional quality
- 10 free videos/month to test

---

## 📈 Next Steps

1. **Test with free tier** (10 videos)
2. **Get real users** to validate
3. **If successful** → upgrade to Pro ($99/month for 100 videos)
4. **If high volume** → consider building DIY solution

---

## ❓ Questions?

**Q: Can I still use LivePortrait?**  
A: Yes! Set `ANIMATION_ENGINE=liveportrait` in `.env`

**Q: What if I run out of free credits?**  
A: System automatically falls back to LivePortrait (unreliable) or you can upgrade

**Q: Can I build my own later?**  
A: Absolutely! Use HeyGen to validate, build DIY when profitable

**Q: Is my API key secure?**  
A: Yes, stored in `.env` which is gitignored. Never commit API keys to GitHub.

---

**Ready to generate real videos? Add your API key and restart the server!** 🚀
