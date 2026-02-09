# Sentinel AI Mobile App (Flet - Recommended)

A cross-platform mobile application built with Python using Flet (Flutter-based framework).

**Why Flet?**
- ✅ Easier to build than Kivy
- ✅ Modern Flutter-based UI
- ✅ One command to build for Android/iOS
- ✅ Hot reload during development
- ✅ Better performance

## Quick Start

### 1. Install Dependencies

```bash
cd sentinel/mobile-flet
pip install -r requirements.txt
```

### 2. Run on Desktop (for testing)

```bash
python main.py
```

### 3. Build for Mobile

#### Android APK

```bash
# Install flet build tools
pip install flet

# Build APK (one command!)
flet build apk
```

The APK will be in `build/apk/` folder.

#### iOS (macOS only)

```bash
flet build ipa
```

## Configuration

### Change Backend URL

Edit `main.py` line 23:

```python
self.api_url = "http://localhost:8000"  # Change this
```

**For mobile devices:**
- Android emulator: `http://10.0.2.2:8000`
- Physical device: Use your computer's IP (e.g., `http://192.168.1.100:8000`)
- Production: `https://your-domain.com`

## Features

- 📱 Native mobile UI with Material Design
- 🎨 Beautiful animations and transitions
- 📁 File picker for images, audio, and video
- 📝 Text analysis with character counter
- 🎯 Real-time results with color-coded risk levels
- 🔄 Easy navigation and reset functionality

## Building for Production

### Android

1. **Build release APK:**
```bash
flet build apk --release
```

2. **Sign the APK** (for Google Play):
```bash
# Generate keystore (first time only)
keytool -genkey -v -keystore my-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-key-alias

# Sign APK
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 -keystore my-release-key.jks build/apk/app-release.apk my-key-alias
```

3. **Upload to Google Play Store**

### iOS

1. **Build IPA:**
```bash
flet build ipa --release
```

2. **Open in Xcode** and configure signing

3. **Upload to App Store Connect**

## Development Tips

### Hot Reload

Run with hot reload for faster development:
```bash
flet run --web
```

Then open in browser at `http://localhost:8550`

### Debug Mode

Add debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Custom Theme

Edit in `main.py`:
```python
self.page.theme_mode = ft.ThemeMode.DARK  # or LIGHT
self.page.theme = ft.Theme(color_scheme_seed=ft.colors.BLUE)
```

## Project Structure

```
mobile-flet/
├── main.py              # Main application
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Troubleshooting

### "flet: command not found"

```bash
pip install --upgrade flet
```

### Build fails

Make sure you have:
- Python 3.8 or higher
- Latest pip: `pip install --upgrade pip`
- Latest flet: `pip install --upgrade flet`

### App crashes on mobile

Check backend URL is accessible from mobile device:
```bash
# Test from mobile browser
http://YOUR_IP:8000/health
```

### File picker not working

Grant storage permissions in Android settings.

## Comparison: Flet vs Kivy

| Feature | Flet | Kivy |
|---------|------|------|
| Build complexity | ⭐⭐⭐⭐⭐ Easy | ⭐⭐⭐ Moderate |
| UI Quality | ⭐⭐⭐⭐⭐ Modern | ⭐⭐⭐⭐ Good |
| Performance | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Good |
| Documentation | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent |
| Build time | Fast | Slow |
| Hot reload | Yes | Limited |

**Recommendation:** Use Flet for easier development and deployment!

## Resources

- Flet Documentation: https://flet.dev/docs/
- Flet Gallery: https://flet.dev/gallery/
- GitHub: https://github.com/flet-dev/flet

## Support

For issues:
1. Check Flet documentation
2. Visit Flet Discord: https://discord.gg/dzWXP8SHG8
3. GitHub Issues: https://github.com/flet-dev/flet/issues
