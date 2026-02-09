[app]

# Application title
title = Sentinel AI

# Package name
package.name = sentinelai

# Package domain (needed for android/ios)
package.domain = org.sentinelai

# Source code directory
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas

# Application versioning
version = 1.0.0

# Application requirements
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests,pillow,plyer

# Supported orientations
orientation = portrait

# Android specific
[app:android]
# Android API to use
android.api = 33

# Minimum API required
android.minapi = 21

# Android SDK version to use
android.sdk = 33

# Android NDK version to use
android.ndk = 25b

# Android permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,CAMERA,RECORD_AUDIO

# Android app theme
android.apptheme = "@android:style/Theme.NoTitleBar"

# iOS specific
[app:ios]
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

[buildozer]
# Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Display warning if buildozer is run as root
warn_on_root = 1
