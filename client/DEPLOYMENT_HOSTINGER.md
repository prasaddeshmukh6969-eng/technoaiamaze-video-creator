# 🚀 Hostinger Deployment Instructions

## ✅ Pre-Deployment Checklist

**Build Status:** ✅ Complete  
**Output Directory:** `c:\Users\Shri\Desktop\antigravity Tools\ai video creator\client\out`  
**Backend URL:** `https://technoaiamaze-video-creator.onrender.com`  
**Target Domain:** `ai.technoamaze.in`

---

## 📦 What's Ready to Deploy

The `out/` directory contains:
- ✅ `index.html` - Homepage
- ✅ `_next/` - Next.js static assets (JS, CSS, fonts)
- ✅ `generate/` - Generate page
- ✅ `404.html` - Custom 404 page
- ✅ `.htaccess` - Apache configuration for routing & MIME types

---

## 📤 Step 1: Access Hostinger File Manager

1. **Login to Hostinger**
   - Go to https://hostinger.com
   - Login with your credentials

2. **Navigate to File Manager**
   - Click on **File Manager** in the control panel
   - Or use FTP client (FileZilla, WinSCP, etc.)

3. **Locate Subdomain Directory**
   - Find the directory for `ai.technoamaze.in`
   - Common paths:
     - `/public_html/`
     - `/domains/ai.technoamaze.in/public_html/`
     - `/public_html/ai/`

---

## 🗂️ Step 2: Prepare Directory

**IMPORTANT:** Backup existing files first!

1. **If directory has old files:**
   - Create a backup folder: `public_html_backup_[date]`
   - Move existing files to backup

2. **Clear the directory** OR create fresh subdomain

---

## 📁 Step 3: Upload Files

### Using File Manager:

1. **Open Upload Dialog**
   - Click "Upload" button in File Manager
   - Or drag and drop files

2. **Upload ALL contents from `out/` folder:**
   ```
   ✓ .htaccess
   ✓ index.html
   ✓ 404.html
   ✓ generate/ (folder)
   ✓ _next/ (folder)
   ✓ 404/ (folder)
   ✓ index.txt
   ```

3. **Verify Upload:**
   - Check `.htaccess` is present (may be hidden by default)
   - Enable "Show Hidden Files" if needed
   - Confirm `_next/` folder uploaded completely

### Using FTP:

1. **FTP Credentials:**
   - Host: Your domain or FTP hostname
   - Username: From Hostinger panel
   - Password: From Hostinger panel
   - Port: 21 (or 22 for SFTP)

2. **Connect & Upload:**
   - Connect to server
   - Navigate to subdomain directory
   - Upload entire `out/` folder contents
   - **Do NOT upload the `out/` folder itself, only its contents**

---

## ✓ Step 4: Verify File Structure

After upload, your directory should look like:

```
/public_html/ (or subdomain directory)
├── .htaccess          ← Apache configuration
├── index.html         ← Homepage
├── 404.html           ← 404 page
├── index.txt          ← (optional metadata)
├── _next/             ← Next.js assets
│   ├── static/
│   └── [build-id]/
├── generate/          ← Generate page
│   └── index.html
└── 404/               ← 404 route
    └── index.html
```

---

## 🧪 Step 5: Test Deployment

### 5.1 Homepage Test

1. **Open in browser:**
   ```
   https://ai.technoamaze.in/
   ```

2. **Expected:**
   - ✅ Homepage loads without errors
   - ✅ No blank page
   - ✅ CSS and styling applied
   - ✅ Images/assets load correctly

### 5.2 Browser Console Check

1. **Open Developer Tools** (F12)
2. **Check Console tab:**
   - ✅ No 404 errors for `_next/` files
   - ✅ No MIME type errors
   - ✅ No CORS errors

### 5.3 Navigation Test

1. **Test routing:**
   - Click navigation links
   - Visit `/generate/` directly
   - Check 404 page: `https://ai.technoamaze.in/nonexistent`

2. **Expected:**
   - ✅ All routes work correctly
   - ✅ No "404 Not Found" for valid pages
   - ✅ Custom 404 page shows for invalid URLs

### 5.4 Backend API Test

1. **Open browser console on deployed site**
2. **Run this command:**
   ```javascript
   fetch('https://technoaiamaze-video-creator.onrender.com/health')
     .then(res => res.json())
     .then(data => console.log('✅ Backend connected:', data))
     .catch(err => console.error('❌ Backend error:', err))
   ```

3. **Expected output:**
   ```json
   {
     "status": "healthy",
     "cuda_available": false,
     "edge_tts": true,
     "coqui_tts": true
   }
   ```

4. **If CORS error appears:**
   - Backend may still be deploying
   - Wait 5 minutes and try again
   - Check CORS update deployed on Render

---

## 🎬 Step 6: End-to-End Video Generation Test

1. **Navigate to Generate Page:**
   ```
   https://ai.technoamaze.in/generate/
   ```

2. **Upload Test Image:**
   - Use any portrait photo
   - Verify file upload works

3. **Enter Test Script:**
   - Type sample text (e.g., "This is a test video")
   - Select voice archetype

4. **Generate Video:**
   - Click generate button
   - Watch for progress updates
   - Wait for completion (mock: ~10 seconds)

5. **Expected Results:**
   - ✅ Upload successful
   - ✅ Job ID received
   - ✅ Progress updates show
   - ✅ Completion message appears
   - ✅ Download link works

---

## 🔧 Troubleshooting

### Issue: Blank Page

**Solution:**
1. Check if `.htaccess` is uploaded
2. Clear browser cache (Ctrl+Shift+Delete)
3. Hard reload (Ctrl+Shift+R)

### Issue: 404 for `_next/` Files

**Solution:**
1. Verify `_next/` folder uploaded completely
2. Check file permissions (should be 644 for files, 755 for folders)
3. Enable "Show Hidden Files" in File Manager
4. Re-upload `_next/` folder

### Issue: CORS Errors

**Solution:**
1. Verify backend is running: `https://technoaiamaze-video-creator.onrender.com/health`
2. Wait 5 minutes for Render deployment to complete
3. Check domain spelling in CORS configuration

### Issue: Routing Not Working

**Solution:**
1. Verify `.htaccess` is in root directory
2. Check Apache `mod_rewrite` is enabled (usually is on Hostinger)
3. Contact Hostinger support if rewrite module disabled

### Issue: HTTPS Redirect Loop

**Solution:**
1. Edit `.htaccess`
2. Comment out HTTPS redirect section temporarily
3. Or adjust HTTPS detection for Hostinger's proxy setup

---

## 📊 Performance Notes

### First Load Expectations:
- **Backend:** May take 50 seconds if cold (free tier spin-up)
- **Frontend:** Instant (served from Hostinger)

### Subsequent Loads:
- **Backend:** Fast (< 1 second)
- **Frontend:** Cached by browser

---

## 🎉 Success Indicators

You'll know deployment succeeded when:
- ✅ Homepage loads at `https://ai.technoamaze.in/`
- ✅ No console errors
- ✅ Navigation works smoothly
- ✅ Backend API responds successfully
- ✅ Video generation flow completes

---

## 📝 Post-Deployment Checklist

- [ ] Homepage loads correctly
- [ ] Generate page accessible
- [ ] Backend API connected
- [ ] Test video generation works
- [ ] Custom 404 page displays
- [ ] HTTPS redirect working
- [ ] Mobile responsive layout verified

---

## 🚨 Need Help?

If you encounter issues:
1. Check browser console for specific errors
2. Verify `.htaccess` uploaded correctly
3. Confirm backend is running
4. Contact me with specific error messages

---

**Deployment Package Location:**
```
c:\Users\Shri\Desktop\antigravity Tools\ai video creator\client\out
```

**Backend API:**
```
https://technoaiamaze-video-creator.onrender.com
```

**Target URL:**
```
https://ai.technoamaze.in
```

---

Good luck! 🍀 The frontend is fully built and ready to go live!
