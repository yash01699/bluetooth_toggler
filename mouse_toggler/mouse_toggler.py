#!/usr/bin/env python3

from datetime import datetime
import subprocess
import os
import traceback

MOUSE_MAC = "YOUR-MOUSE-MAC-ID"
BLUEUTIL_PATH = "YOUR-FILE-PATH"


def is_connected(mac_address: str) -> bool:
    """Returns True if the device is connected, False otherwise."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        result = subprocess.run(
            [BLUEUTIL_PATH, "--is-connected", mac_address],
            capture_output=True,
            text=True,
            timeout=10
        )
        print(f"[{timestamp}] blueutil exit code: {result.returncode}")
        print(f"[{timestamp}] blueutil stdout: {result.stdout}")
        if result.stderr:
            print(f"[{timestamp}] blueutil stderr: {result.stderr}")
        return result.stdout.strip() == "1"
    except Exception as e:
        print(f"[{timestamp}] ERROR in is_connected: {e}")
        print(traceback.format_exc())
        return False


def set_natural_scrolling(enabled: bool):
    """Sets the global natural scrolling preference."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        value = "true" if enabled else "false"
        result = subprocess.run(
            ["defaults", "write", "-g", "com.apple.swipescrolldirection", "-bool", value],
            capture_output=True,
            text=True,
            timeout=10
        )
        print(f"[{timestamp}] defaults write exit code: {result.returncode}")
    except Exception as e:
        print(f"[{timestamp}] ERROR in set_natural_scrolling: {e}")
        print(traceback.format_exc())

def get_natural_scrolling():
    """Read the current natural scrolling setting."""
    try:
        result = subprocess.run(
            ["defaults", "read", "-g", "com.apple.swipescrolldirection"],
            capture_output=True,
            text=True,
            timeout=10
        )
        # Returns "1" for true, "0" for false
        return result.stdout.strip() == "1"
    except subprocess.CalledProcessError:
        # Key doesn't exist, return default (usually true on macOS)
        return True
    except Exception as e:
        print(f"ERROR reading natural scrolling: {e}")
        return None


def main():
    print("=== Script started ===")
    try:
        print(f"BLUEUTIL_PATH: {BLUEUTIL_PATH}")
        print(f"BLUEUTIL exists: {os.path.exists(BLUEUTIL_PATH)}")
        
        connected = is_connected(MOUSE_MAC)
        print(f"Mouse connected: {connected}")

        natural_Scrolling = get_natural_scrolling()
        print(f"Current natural scrolling setting: {natural_Scrolling}")

        if connected and natural_Scrolling == True:
            print("Setting bluetooth settings for natural scrolling to false")
            set_natural_scrolling(False)
            print("Mouse connected. Natural scrolling disabled.")

        elif not connected and natural_Scrolling == False:
            print("Setting bluetooth settings for natural scrolling to true")
            set_natural_scrolling(True)
            print("Mouse disconnected. Natural scrolling enabled.")
            
        print("=== Script completed successfully ===")

    except Exception as e:
        print(f"FATAL ERROR: {e}")
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
