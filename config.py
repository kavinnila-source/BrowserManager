# ==========================================
# BrowserManager v1.5 Configuration
# ==========================================

# Number of browser windows
NUMBER_OF_WINDOWS = 2

# URLs
URLS = [
    "https://httpbin.org/user-agent",
    "https://example.com",
    "https://news.ycombinator.com",
    "https://www.wikipedia.org",
]

# Browser lifetime (minutes)
MIN_ACTIVE_MINUTES = 10
MAX_ACTIVE_MINUTES = 60

# Restart delay after browser closes (minutes)
RESTART_DELAY_MINUTES = 1

# Delay between launching browsers when Manager starts (seconds)
STARTUP_DELAY_SECONDS = 15

# Window size
MIN_WIDTH = 1000
MAX_WIDTH = 1600

MIN_HEIGHT = 700
MAX_HEIGHT = 900

# Window position
MIN_X = 0
MAX_X = 800

MIN_Y = 0
MAX_Y = 300

# Firefox profiles folder
PROFILE_FOLDER = "profiles"

# ==========================================
# Random Zoom Settings
# ==========================================

# Minimum browser zoom (%)
MIN_ZOOM = 90

# Maximum browser zoom (%)
MAX_ZOOM = 110