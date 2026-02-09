"""
Configuration file for Sentinel AI Mobile
"""

# Backend API Configuration
# Change this to your backend URL
API_BASE_URL = "http://localhost:8000"

# For Android emulator, use: http://10.0.2.2:8000
# For physical device, use your computer's IP: http://192.168.1.XXX:8000
# For production, use: https://your-domain.com

# File size limits (in MB)
MAX_IMAGE_SIZE = 50
MAX_VIDEO_SIZE = 100
MAX_AUDIO_SIZE = 50

# Supported file formats
SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png']
SUPPORTED_VIDEO_FORMATS = ['.mp4', '.mov', '.webm']
SUPPORTED_AUDIO_FORMATS = ['.mp3', '.wav', '.m4a']

# Text limits
MAX_TEXT_LENGTH = 10000

# Request timeout (seconds)
REQUEST_TIMEOUT = 60

# App theme
THEME_PRIMARY_PALETTE = "Blue"  # Options: Red, Pink, Purple, DeepPurple, Indigo, Blue, LightBlue, Cyan, Teal, Green, LightGreen, Lime, Yellow, Amber, Orange, DeepOrange, Brown, Gray, BlueGray
THEME_STYLE = "Light"  # Options: Light, Dark
