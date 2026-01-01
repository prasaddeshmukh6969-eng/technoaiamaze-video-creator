# 🚀 Deployment Guide

## Overview

Technoaiamaze uses a split architecture:
- **Frontend**: Hostinger (static files)
- **Backend**: Render.com (API server)

**Total Cost**: ₹0/month (free tiers)

---

## 📦 Frontend Deployment (Hostinger)

### **Step 1: Build**
```bash
cd client
npm run build
```

This creates an `out/` folder with optimized static files.

### **Step 2: Upload to Hostinger**

1. Login to **hPanel.hostinger.com**
2. Go to **Files → File Manager**
3. Navigate to `public_html`
4. Delete old files (if any)
5. Upload entire `out/` folder contents
6. Upload `.htaccess` file (rename from `.htaccess-hostinger`)

### **Step 3: Configure Domain**

- Domain: `https://technoamaze.in`
- SSL: Auto-enabled (free)
- DNS: Already configured

### **Step 4: Test**

Visit your domain and verify:
- ✅ Homepage loads
- ✅ Animations work
- ✅ Mobile responsive
- ✅ HTTPS enabled

---

## 🔧 Backend Deployment (Render.com)

### **Step 1: Push to GitHub**

```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

### **Step 2: Create Render Service**

1. Go to **render.com**
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Configure:
   - **Name**: technoaiamaze-api
   - **Root Directory**: `server`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

### **Step 3: Set Environment Variables**

In Render dashboard, add:
```
HEYGEN_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
CORS_ORIGINS=https://technoamaze.in
```

### **Step 4: Deploy**

Render auto-deploys on every GitHub push.

**Backend URL**: `https://technoaiamaze.onrender.com`

---

## 🔗 Connect Frontend to Backend

Update `client/.env.production`:
```
NEXT_PUBLIC_API_URL=https://technoaiamaze.onrender.com
```

Rebuild and redeploy frontend.

---

## ✅ Post-Deployment Checklist

- [ ] Frontend loads at technoamaze.in
- [ ] Backend API responds at /docs endpoint
- [ ] CORS configured correctly
- [ ] Environment variables set
- [ ] SSL certificate active
- [ ] Mobile view works
- [ ] Video generation works end-to-end

---

## 🔄 Update Process

**Frontend Changes**:
```bash
cd client
npm run build
# Upload 'out' folder to Hostinger
```

**Backend Changes**:
```bash
git push origin main
# Render auto-deploys
```

---

## 💰 Cost Monitoring

- **Hostinger**: Already paid (yearly plan)
- **Render**: FREE tier
  - Spins down after 15min inactivity
  - 750 hours/month free
  - Auto-restarts on request

**When to Upgrade**:
- Render free tier usage > 90%
- Need faster cold starts
- More than 100 requests/day

**Paid Plans**:
- Render: $7/month (always-on)
- Hostinger: Already have

---

## 🛡️ Security

- ✅ HTTPS enforced (both frontend & backend)
- ✅ Environment variables (not in code)
- ✅ CORS restricted to your domain
- ✅ API rate limiting (coming soon)

---

## 📊 Monitoring

**Render Dashboard**:
- View logs
- Track deployments
- Monitor uptime

**Hostinger**:
- SSL status
- Traffic analytics
- File manager

---

## 🆘 Troubleshooting

### **Frontend Issues**

**Problem**: Page shows 404
- **Fix**: Check `.htaccess` uploaded correctly

**Problem**: CSS not loading
- **Fix**: Clear browser cache, check MIME types

### **Backend Issues**

**Problem**: API not responding
- **Fix**: Check Render logs, service might be spinning up (30sec wait)

**Problem**: CORS error
- **Fix**: Verify CORS_ORIGINS environment variable

---

## 📞 Support

If deployment fails, check:
1. Render build logs
2. Browser console errors
3. Network tab in DevTools

---

**Deployment takes ~15 minutes total** ⏱️
