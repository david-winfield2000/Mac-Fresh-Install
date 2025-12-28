#!/usr/bin/env python3
import subprocess
from concurrent.futures import ThreadPoolExecutor
import os

# -----------------------------
# Map brew cask names to app names
# -----------------------------
apps = {
    "firefox": "Firefox.app",
    "visual-studio-code": "Visual Studio Code.app",
    "alt-tab": "AltTab.app",
    "linearmouse": "LinearMouse.app",
    "maccy": "Maccy.app",
    "rectangle": "Rectangle.app",
    "mac-mouse-fix": "Mac Mouse Fix.app",
    "docker": "Docker.app",
    "ghostty": "Ghostty.app",
}


def install_app(cask, app_name):
    app_path = f"/Applications/{app_name}"
    if os.path.exists(app_path):
        print(f"✅ {app_name} already exists, skipping.")
        return
    print(f"Installing {cask}...")
    try:
        subprocess.run(["brew", "install", "--cask", cask], check=True)
    except subprocess.CalledProcessError:
        print(f"⚠️ Failed to install {cask}, continuing...")


try:
    subprocess.run(["brew", "--version"], check=True, stdout=subprocess.DEVNULL)
    print("Homebrew already installed")
except subprocess.CalledProcessError:
    print("Installing Homebrew...")
    subprocess.run(
        [
            "/bin/bash",
            "-c",
            "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)",
        ],
        check=True,
    )

with ThreadPoolExecutor(max_workers=len(apps)) as executor:
    for cask, app_name in apps.items():
        executor.submit(install_app, cask, app_name)

try:
    subprocess.run(["git", "--version"], check=True, stdout=subprocess.DEVNULL)
    print("Git is installed, configuring username and email...")
    subprocess.run(
        ["git", "config", "--global", "user.name", "davidwinfield2000"], check=True
    )
    subprocess.run(
        ["git", "config", "--global", "user.email", "david.winfield2000@gmail.com"],
        check=True,
    )
    print("✅ Git configured successfully")
except subprocess.CalledProcessError:
    print("⚠️ Git is not installed or failed to configure")

print("=== All apps installed (or skipped if already present) ===")
