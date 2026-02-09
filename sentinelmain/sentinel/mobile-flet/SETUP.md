# Quick Setup Guide - Connect Mobile App to Render Backend

## ✅ You Already Have Backend on Render!

Perfect! Your mobile app will connect to your existing Render backend.

## 🚀 Setup Steps:

### Step 1: Get Your Render URL

Your Render backend URL looks like:
```
https://your-app-name.onrender.com
```

Example: `https://sentinel-ai-xyz.onrender.com`

### Step 2: Update Mobile App

Open `main.py` and change line 23:

```python
self.api_url = "https://your-app-name.onrender.com"
```

**Replace `your-app-name` with your actual Render app name!**

### Step 3: Test on Desktop First

```bash
cd sentinel/mobile-flet
pip install -r requirements.txt
python main.py
```

Try analyzing some text to make sure it connects to your Render backend.

### Step 4: Build Mobile App

Once testing works, build the APK:

```bash
pip install flet
flet build apk
```

The APK will be in `build/apk/` folder.

## 🔍 Troubleshooting:

### Error: "Connection refused" or "Cannot connect"

**Check 1:** Is your Render backend running?
- Go to your Render dashboard
- Make sure the service is "Live" (not sleeping)

**Check 2:** Test backend URL in browser:
```
https://your-app-name.onrender.com/health
```

Should return: `{"status": "healthy"}`

**Check 3:** CORS settings

Your backend needs to allow mobile app requests. Check `sentinel/backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins (good for mobile)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Error: "SSL Certificate" issues

If you get SSL errors, temporarily use HTTP (not recommended for production):

```python
self.api_url = "http://your-app-name.onrender.com"
```

But Render should provide HTTPS by default.

### Render Free Tier Sleeps

⚠️ **Important:** Render free tier sleeps after 15 minutes of inactivity.

**Solutions:**

1. **Accept the delay** (first request takes 30-60 seconds to wake up)

2. **Keep it awake** with a ping service:
   - Use https://uptimerobot.com (free)
   - Ping your backend every 10 minutes

3. **Upgrade to paid tier** ($7/month - no sleep)

4. **Add loading message** in mobile app:
```python
# In main.py, add this message
"If this is the first request, it may take 30-60 seconds (free tier waking up)..."
```

## 📱 Distribution:

### Share APK Directly

1. Build APK: `flet build apk`
2. Find APK: `build/apk/app-release.apk`
3. Share via:
   - Google Drive
   - Dropbox
   - Email
   - WhatsApp

Users need to:
1. Enable "Install from Unknown Sources" in Android settings
2. Download and install APK

### Publish to Google Play Store (Optional)

1. Create Google Play Developer account ($25 one-time)
2. Build signed APK
3. Upload to Play Store
4. Wait for review (1-3 days)

## 🎯 Complete Example:

If your Render URL is: `https://sentinel-backend-abc123.onrender.com`

Then in `main.py`:
```python
self.api_url = "https://sentinel-backend-abc123.onrender.com"
```

That's it! The mobile app will now use your Render backend.

## 📊 Architecture:

```
┌─────────────────────┐
│   User's Phone      │
│   (Mobile App)      │
└──────────┬──────────┘
           │
           │ HTTPS
           │
           ▼
┌─────────────────────┐
│   Render Cloud      │
│   (Your Backend)    │
│   - FastAPI         │
│   - Redis           │
│   - Celery          │
└─────────────────────┘
```

## ✅ Checklist:

- [ ] Backend is deployed on Render
- [ ] Backend URL is accessible (test in browser)
- [ ] Updated `main.py` with Render URL
- [ ] Tested on desktop (`python main.py`)
- [ ] Built APK (`flet build apk`)
- [ ] Tested APK on Android device
- [ ] Shared APK with users

## 🆘 Need Help?

**Backend not working?**
- Check Render logs
- Make sure all environment variables are set
- Verify Docker containers are running

**Mobile app not connecting?**
- Double-check URL (no trailing slash!)
- Test URL in browser first
- Check phone has internet connection

**Want to add features?**
- Edit `main.py`
- Test with `python main.py`
- Rebuild APK

---

**You're all set!** Your mobile app will work with your existing Render backend. No need to change anything on the backend side! 🎉
