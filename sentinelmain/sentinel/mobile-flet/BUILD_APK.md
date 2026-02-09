# 📱 Build Android APK - Simple Guide

## ✅ Your System Status

- ✅ Flutter is installed
- ✅ Android SDK is installed
- ⚠️ Git not in PATH (optional)
- ⚠️ Visual Studio not needed for Android

## 🚀 Build APK (Simple Method)

### Option 1: Build Now (Recommended)

```bash
cd sentinel/mobile-flet
flet build apk --verbose
```

**Build time:** 5-10 minutes first time, 2-3 minutes after

**Output:** `build/apk/app-release.apk`

### Option 2: Build with Custom Name

```bash
flet build apk --project "SentinelAI" --org "com.sentinelai"
```

### Option 3: Build for Testing (Faster)

```bash
flet build apk --debug
```

## 📦 After Build

### Find Your APK

```
sentinel/mobile-flet/build/apk/app-release.apk
```

### APK Size

~50-80 MB (includes Python runtime + dependencies)

### Share APK

**Method 1: USB Transfer**
```bash
# Connect phone via USB
# Copy APK to phone's Download folder
```

**Method 2: Cloud**
- Upload to Google Drive
- Share link with users

**Method 3: Direct Install**
```bash
# If phone is connected via USB
adb install build/apk/app-release.apk
```

## 🔧 If Build Fails

### Error: "Flutter not found"

```bash
# Add Flutter to PATH
# Or use full path:
C:\path\to\flutter\bin\flutter doctor
```

### Error: "Android SDK not found"

```bash
# Flutter will show the path needed
flutter doctor --android-licenses
```

### Error: "Build failed"

```bash
# Clean and rebuild
flet build apk --clean
```

## 📱 Install on Android

### Step 1: Enable Unknown Sources

1. Open **Settings**
2. Go to **Security** or **Privacy**
3. Enable **Install from Unknown Sources**
4. Or enable for specific app (Chrome, Files, etc.)

### Step 2: Install APK

1. Transfer APK to phone
2. Open APK file
3. Tap **Install**
4. Wait for installation
5. Tap **Open**

### Step 3: Grant Permissions

When app asks:
- ✅ Allow **Internet** (required)
- ✅ Allow **Storage** (for file picker)

## 🧪 Test the App

### Test 1: Text Analysis

1. Open app
2. Go to **Text** tab
3. Enter: "You won $1000! Click here now!"
4. Tap **Check**
5. Wait 30-60 seconds (first request wakes up backend)
6. Should show: High Risk

### Test 2: Image Analysis

1. Go to **Image** tab
2. Tap **Choose File**
3. Select any image
4. Tap **Check**
5. Should show analysis result

## 🐛 Common Issues

### "Server error: 500"

**Cause:** Backend needs redeployment

**Fix:**
1. Go to Render dashboard
2. Click "Manual Deploy"
3. Wait 5-10 minutes
4. Try app again

### "Cannot connect to server"

**Cause:** Backend is sleeping (free tier)

**Fix:**
1. Open browser
2. Visit: https://sentinel-ai-3yc8.onrender.com/health
3. Wait 30-60 seconds
4. Try app again

### "File picker not working"

**Cause:** Storage permission not granted

**Fix:**
1. Go to phone Settings
2. Apps → Sentinel AI
3. Permissions → Storage → Allow

## 📊 Build Output

After successful build, you'll see:

```
✓ Built build/apk/app-release.apk (XX.X MB)
```

## 🎯 Quick Commands

```bash
# Build APK
flet build apk

# Build with verbose output
flet build apk --verbose

# Clean build
flet build apk --clean

# Build debug version (faster)
flet build apk --debug

# Check Flutter setup
flutter doctor
```

## 📝 Notes

- **First build:** Takes 5-10 minutes (downloads dependencies)
- **Subsequent builds:** 2-3 minutes
- **APK size:** ~50-80 MB (normal for Python apps)
- **Min Android:** API 21 (Android 5.0)
- **Target Android:** API 33 (Android 13)

## ✅ Checklist

Before building:
- [ ] Backend deployed on Render
- [ ] Backend URL correct in `main.py`
- [ ] Tested backend with `py test_backend.py`
- [ ] Flutter installed
- [ ] Android SDK installed

After building:
- [ ] APK file exists in `build/apk/`
- [ ] APK size is reasonable (~50-80 MB)
- [ ] Tested on Android device
- [ ] All features work

---

**Ready to build!** Just run `flet build apk` and wait 5-10 minutes! 🚀
