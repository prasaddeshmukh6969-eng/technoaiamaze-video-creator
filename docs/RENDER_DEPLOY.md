# 🚀 Deploy Backend to Render - Quick Guide

## ⏱️ Time Required: 20 minutes

---

## 📋 **Prerequisites**

✅ GitHub account (you have this)
✅ Code pushed to GitHub (done!)
✅ Render.com account (free)

---

## 🎯 **Step 1: Create Render Account** (2 min)

1. Go to: **https://render.com**
2. Click **"Get Started"**
3. Sign up with **GitHub** (easiest!)
4. Authorize Render to access your repos

---

## 🎯 **Step 2: Create Web Service** (3 min)

1. Click **"New +"** → **"Web Service"**
2. Connect your repository
3. Select: **`ai video creator`** repo
4. Click **"Connect"**

---

## 🎯 **Step 3: Configure Service** (5 min)

**Basic Settings**:
- **Name**: `technoaiamaze-api`
- **Region**: `Singapore` (closest to India)
- **Branch**: `master`
- **Root Directory**: `server`
- **Runtime**: `Python 3`

**Build Settings**:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Instance Type**:
- Select: **Free** (₹0/month)

---

## 🎯 **Step 4: Environment Variables** (5 min)

Click **"Advanced"** → **"Add Environment Variable"**

Add these (one by one):

```
CORS_ORIGINS=https://technoamaze.in
PYTHON_VERSION=3.10.0
```

*Note: We'll add API keys later when you're ready to enable video generation*

---

## 🎯 **Step 5: Deploy!** (5 min)

1. Click **"Create Web Service"**
2. Wait for build (3-5 minutes)
3. Watch logs for success ✅

**Your backend will be at**:
```
https://technoaiamaze-api.onrender.com
```

---

## 🎯 **Step 6: Update Frontend** (5 min)

Update your frontend to connect to Render backend:

**File**: `client/.env.production`
```
NEXT_PUBLIC_API_URL=https://technoaiamaze-api.onrender.com
```

Then rebuild & redeploy frontend!

---

## ✅ **Verify It Works**

Visit: `https://technoaiamaze-api.onrender.com/docs`

You should see **FastAPI documentation** page! 🎉

---

## 🔍 **Troubleshooting**

**Build Failed?**
- Check `requirements.txt` exists in `server/` folder
- Verify Python version compatibility

**Service Won't Start?**
- Check logs in Render dashboard
- Verify `main.py` has correct FastAPI app

**CORS Errors?**
- Check `CORS_ORIGINS` environment variable
- Should match your frontend domain exactly

---

## 💰 **Cost Reminder**

**Render Free Tier**:
- ✅ FREE forever
- ✅ 750 hours/month
- ⚠️ Spins down after 15 min inactivity
- ⚠️ 30 sec cold start

**Upgrade Later** (when profitable):
- $7/month = always on
- Better performance
- No cold starts

---

**Ready to start? Let me walk you through each step!** 🚀
