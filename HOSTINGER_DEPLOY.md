# 🌐 Deploy to Hostinger - Complete Guide

## ✅ **Cost: ₹0 (Using your existing Hostinger hosting)**

---

## 📦 **Step 1: Build the Frontend**

### **On Your Computer:**

```bash
# Navigate to client folder
cd "C:\Users\Shri\Desktop\antigravity Tools\ai video creator\client"

# Install dependencies (if not already done)
npm install

# Build for production
npm run build

# This creates an 'out' folder with static files
```

---

## 📁 **Step 2: Prepare Files for Upload**

After `npm run build`, you'll have an `out` folder containing:
```
out/
├── _next/
├── index.html
├── generate.html
├── demo-placeholder.svg
└── ...other files
```

**These are the files you'll upload to Hostinger!**

---

## 🌍 **Step 3: Upload to Hostinger**

### **Option A: File Manager (Easiest)**

1. **Login to Hostinger**
   - Go to: hpanel.hostinger.com
   - Navigate to your domain

2. **Open File Manager**
   - Click "Files" → "File Manager"
   - Navigate to `public_html` folder

3. **Clear Old Files** (if any)
   - Delete everything in `public_html`
   - Keep `.htaccess` if it exists

4. **Upload New Files**
   - Click "Upload"
   - Select ALL files from your `out` folder
   - Wait for upload to complete ✅

### **Option B: FTP (Faster for large files)**

1. **Get FTP Credentials**
   - Hostinger → Files → FTP Accounts
   - Note: Host, Username, Password

2. **Use FileZilla** (free FTP client)
   - Download from: filezilla-project.org
   - Connect using credentials
   - Upload entire `out` folder contents to `public_html`

---

## ⚙️ **Step 4: Configure .htaccess**

**Create/Update `.htaccess` file in `public_html`:**

```apache
# Enable HTTPS redirect
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Handle Next.js routing
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ /index.html [L]

# MIME types for Next.js
AddType application/javascript .js
AddType text/css .css
AddType image/svg+xml .svg
AddType application/json .json

# Enable gzip compression
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/css application/javascript
</IfModule>

# Cache static files
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType text/css "access plus 1 year"
</IfModule>
```

Upload this `.htaccess` file to `public_html` folder.

---

## 🔗 **Step 5: Update API URL**

**In your Next.js app, update the backend URL:**

File: `client/components/studio/Studio.tsx`

```typescript
// Change this line:
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// To your Render backend URL:
const API_URL = 'https://your-backend.onrender.com';
```

**Or create `.env.production` file:**

```bash
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

Then rebuild: `npm run build`

---

## ✅ **Step 6: Test Your Live Site**

1. **Visit Your Domain**
   - https://yourdomain.com (or technoamaze.in)

2. **Check Everything Works**
   - ✅ Homepage loads
   - ✅ Animations work
   - ✅ "Start Creating" button works
   - ✅ Mobile responsive

3. **Test Backend Connection**
   - Try generating a video
   - Should connect to Render backend

---

## 🛡️ **Common Issues & Fixes**

### **Issue 1: Page shows 404**
**Fix**: Check `.htaccess` is uploaded correctly

### **Issue 2: CSS/JS not loading**
**Fix**: 
- Clear browser cache
- Check MIME types in `.htaccess`
- Verify `_next` folder uploaded

### **Issue 3: "API connection failed"**
**Fix**:
- Verify Render backend is running
- Check API_URL in code
- Enable CORS on Render backend

---

## 🚀 **After Successful Deploy**

Your site will be live at:
- **Frontend**: https://technoamaze.in (Hostinger)
- **Backend**: https://your-app.onrender.com (Render)

**Cost Breakdown**:
- Hostinger: Already paid ✅
- Render: FREE tier ✅
- Domain: Already have ✅
- **Total NEW costs: ₹0** 🎉

---

## 📊 **What to Do After Launch**

1. **Share the link** with 10 friends
2. **Post on social media** (LinkedIn, Facebook)
3. **Track signups** (we'll add analytics next)
4. **Get feedback**
5. **First customer within 7 days!** 🎯

---

## 🔄 **How to Update Site Later**

Whenever you make changes:

```bash
# 1. Make code changes
# 2. Build again
npm run build

# 3. Upload new 'out' folder to Hostinger
# Done! ✅
```

**Updates take 2-5 minutes!**

---

## 💡 **Pro Tips**

1. **Subdomain Setup** (Optional)
   - Create: `ai.technoamaze.in`
   - Point to same `public_html`
   - Better branding!

2. **SSL Certificate**
   - Should be auto-enabled on Hostinger
   - If not: Hostinger → SSL → Enable

3. **Backup**
   - Download your `out` folder
   - Keep local copy
   - Hostinger also has auto-backups

---

## ✅ **Ready to Deploy?**

Just run these 3 commands:

```bash
cd client
npm run build
# Then upload 'out' folder to Hostinger!
```

**Time needed: 10-15 minutes** ⏱️
**Difficulty: Easy** ✅
**Cost: FREE** 💰
