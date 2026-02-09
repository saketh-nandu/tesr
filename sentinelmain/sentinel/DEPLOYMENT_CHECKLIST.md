# 🚀 Sentinel AI - Deployment Checklist

## ✅ Backend Files Verified

All backend files are correct and ready for deployment:

- ✅ `backend/app/main.py` - FastAPI app with CORS
- ✅ `backend/app/models/text_analyzer.py` - Returns `ai_likelihood`
- ✅ `backend/app/models/audio_analyzer.py` - Returns correct fields
- ✅ `backend/app/models/image_analyzer.py` - Returns correct fields
- ✅ `backend/app/models/video_analyzer.py` - Returns correct fields
- ✅ `backend/app/utils/explainer.py` - Generates explanations
- ✅ `backend/app/schemas/responses.py` - Response models
- ✅ `backend/app/api/routes/text.py` - Text analysis endpoint

## 📦 Deploy to Render

### Step 1: Push Code to GitHub (if not already)

```bash
cd sentinel
git add .
git commit -m "Fix backend for mobile app"
git push
```

### Step 2: Deploy on Render

1. Go to https://dashboard.render.com
2. Find your Sentinel AI service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**
4. Wait 5-10 minutes for deployment

### Step 3: Verify Deployment

Test the backend:

```bash
cd sentinel/mobile-flet
py test_backend.py
```

Expected output:
```
✓ Health check: 200 OK
✓ Text analysis: 200 OK
  Verdict: High Risk (or similar)
  Risk Score: 75 (or similar)
```

## 📱 Build Mobile APK

### Step 1: Verify Backend URL

Check `sentinel/mobile-flet/main.py` line 24:

```python
self.api_url = "https://sentinel-ai-3yc8.onrender.com"
```

### Step 2: Build APK

```bash
cd sentinel/mobile-flet
flet build apk
```

Build time: 5-10 minutes

### Step 3: Find APK

Location: `sentinel/mobile-flet/build/apk/app-release.apk`

Size: ~50-80 MB

## 📲 Test APK

### On Android Device:

1. **Enable Unknown Sources:**
   - Settings → Security → Unknown Sources → Enable

2. **Transfer APK:**
   - USB cable, or
   - Google Drive, or
   - Email

3. **Install:**
   - Tap APK file
   - Click "Install"

4. **Test:**
   - Open Sentinel AI app
   - Try text analysis first
   - Then try image/audio/video

## 🐛 Troubleshooting

### Backend Returns 500 Error

**Problem:** Old code on Render

**Solution:**
1. Redeploy on Render (Manual Deploy)
2. Wait for deployment to complete
3. Test with `py test_backend.py`

### APK Build Fails

**Problem:** Missing dependencies

**Solution:**
```bash
pip install --upgrade flet
flet build apk
```

### App Can't Connect to Backend

**Problem:** Wrong URL or backend sleeping

**Solutions:**
1. Check URL in `main.py` (no trailing slash!)
2. Wake up backend by visiting URL in browser
3. Wait 30-60 seconds for free tier to wake up

### File Upload Fails

**Problem:** File too large or wrong format

**Solutions:**
1. Check file size limits:
   - Images: < 50MB
   - Audio: < 30 seconds
   - Video: < 8 seconds
2. Check file formats:
   - Images: JPG, PNG
   - Audio: MP3, WAV, M4A
   - Video: MP4, MOV, WebM

## 📊 Current Status

### Backend
- ✅ Code is correct
- ⏳ Needs redeployment on Render
- 🌐 URL: https://sentinel-ai-3yc8.onrender.com

### Mobile App
- ✅ Code is ready
- ✅ Connected to Render backend
- ⏳ Ready to build APK

## 🎯 Next Steps

1. **Deploy backend to Render** (5-10 min)
2. **Test backend** with `py test_backend.py`
3. **Build APK** with `flet build apk` (5-10 min)
4. **Test APK** on Android device
5. **Share APK** with users!

## 📝 Notes

- **Free Tier:** Render backend sleeps after 15 min inactivity
- **First Request:** Takes 30-60 seconds to wake up
- **APK Size:** ~50-80 MB (includes Python runtime)
- **Permissions:** Internet, Storage (for file picker)

## 🔗 Useful Links

- Render Dashboard: https://dashboard.render.com
- Flet Docs: https://flet.dev/docs/
- Backend URL: https://sentinel-ai-3yc8.onrender.com

---

**Ready to deploy!** Follow the steps above and your mobile app will be live! 🚀
