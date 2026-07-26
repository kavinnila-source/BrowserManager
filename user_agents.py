import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edg/138.0.0.0",
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def format_user_agent(ua):
    if "Firefox/" in ua:
        version = ua.split("Firefox/")[-1].split(".")[0]
        browser = f"Firefox {version}"
    elif "Edg/" in ua:
        version = ua.split("Edg/")[-1].split(".")[0]
        browser = f"Edge {version}"
    elif "Chrome/" in ua:
        version = ua.split("Chrome/")[-1].split(".")[0]
        browser = f"Chrome {version}"
    else:
        browser = "Unknown"

    if "Windows" in ua:
        os_name = "Windows"
    elif "Linux" in ua:
        os_name = "Linux"
    elif "Mac OS X" in ua:
        os_name = "macOS"
    else:
        os_name = "Unknown"

    return f"{browser} ({os_name})"
