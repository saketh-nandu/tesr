# Sentinel AI Mobile App (Python)

A cross-platform mobile application built with Python using Kivy/KivyMD framework.

## Features

- ✅ Works on Android and iOS
- ✅ Native Python code
- ✅ Material Design UI
- ✅ File picker for images, audio, and video
- ✅ Text analysis
- ✅ Real-time results display

## Prerequisites

### For Development (Desktop Testing)

```bash
pip install -r requirements.txt
```

### For Android Build

1. Install Buildozer:
```bash
pip install buildozer
```

2. Install Android dependencies (Linux/WSL):
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

### For iOS Build (macOS only)

```bash
pip install kivy-ios
```

## Running the App

### Desktop Testing

```bash
cd sentinel/mobile
python main.py
```

### Build for Android

```bash
cd sentinel/mobile

# Initialize buildozer (first time only)
buildozer init

# Build APK
buildozer -v android debug

# Build and deploy to connected device
buildozer android debug deploy run
```

The APK will be in `bin/` folder.

### Build for iOS (macOS only)

```bash
cd sentinel/mobile

# Build iOS app
toolchain build kivy
toolchain build kivymd
toolchain create SentinelAI .

# Open in Xcode
open SentinelAI-ios/SentinelAI.xcodeproj
```

## Configuration

### Backend URL

Edit `main.py` and change the API URL:

```python
api_url = "http://your-backend-url:8000"
```

For Android testing with local backend:
- Use `http://10.0.2.2:8000` (Android emulator)
- Use your computer's IP address for physical device (e.g., `http://192.168.1.100:8000`)

## Project Structure

```
mobile/
├── main.py              # Main application code
├── requirements.txt     # Python dependencies
├── buildozer.spec      # Android/iOS build configuration
└── README.md           # This file
```

## Screens

1. **Home Screen**
   - Tabs for Text, Image, Audio, Video
   - File picker for media files
   - Text input for text analysis
   - Check button to analyze

2. **Result Screen**
   - Risk score display
   - Verdict badge (Safe/Possibly AI/High Risk)
   - Detailed explanations
   - Action recommendations
   - Back button

## Customization

### Theme Colors

Edit in `main.py`:

```python
self.theme_cls.primary_palette = "Blue"  # Change to: Red, Green, Purple, etc.
self.theme_cls.theme_style = "Light"     # Change to: "Dark"
```

### Permissions

Edit `buildozer.spec`:

```ini
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,CAMERA,RECORD_AUDIO
```

## Troubleshooting

### "Module not found" errors

```bash
pip install --upgrade kivy kivymd
```

### Buildozer fails on Windows

Use WSL (Windows Subsystem for Linux) or a Linux VM for Android builds.

### App crashes on startup

Check logs:
```bash
buildozer android logcat
```

### File picker not working

Make sure permissions are granted in Android settings.

## Distribution

### Android

1. Build release APK:
```bash
buildozer android release
```

2. Sign the APK with your keystore

3. Upload to Google Play Store

### iOS

1. Build in Xcode
2. Archive and upload to App Store Connect

## Notes

- The app requires an active internet connection to communicate with the backend
- Make sure your backend API is accessible from mobile devices
- For production, use HTTPS for secure communication
- Test thoroughly on both Android and iOS devices

## Support

For issues or questions, refer to:
- Kivy Documentation: https://kivy.org/doc/stable/
- KivyMD Documentation: https://kivymd.readthedocs.io/
- Buildozer Documentation: https://buildozer.readthedocs.io/
