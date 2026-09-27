# bluetooth_toggler

I had to keep manually toggling settings in my macbook everytime I connected to my bluetooth mouse, so I wrote a script for it that automatically toggles my settings for me if my bluetooth mouse is connected and disables this settings whenever its not. It runs every 15 seconds using the apple launch agent (but you can customise it however you want).

-----------*****************************-----------

Automatically toggle macOS natural scrolling based on Bluetooth mouse connection state. 

When your Bluetooth mouse connects, natural scrolling is disabled (traditional scroll direction). When it disconnects, natural scrolling is re-enabled for trackpad use.

## Features

✨ **Automatic detection** - Detects when your Bluetooth mouse connects/disconnects  
✨ **Smart toggling** - Only changes settings when mouse state actually changes  
✨ **Low battery impact** - Efficient polling every 15 seconds  
✨ **Background service** - Runs silently as a macOS LaunchAgent  
✨ **Easy installation** - Simple setup with one command  

## Requirements

- macOS (10.12+)
- Python 3
- Homebrew (for `blueutil`)

## Installation

### 1. Install dependencies

```bash
brew install blueutil
```

### 2. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/bluetooth_toggler.git
cd bluetooth_toggler
```

Or download and place in a convenient location:
```bash
mkdir -p /usr/local/opt/mouse_toggler
# Copy mouse_toggler.py here
```

### 3. Find your Bluetooth mouse MAC address

```bash
blueutil --paired
```

Look for your mouse in the output. Example:
```
address: d5-39-51-c9-12-7b, name: "Logitech MX Master 3"
```

### 4. Update the script

Edit `mouse_toggler.py` and update the `MOUSE_MAC` variable:

```python
MOUSE_MAC = "d5-39-51-c9-12-7b"  # Replace with your mouse's MAC address
```

### 5. Install the LaunchAgent

```bash
# Copy the plist to your LaunchAgents directory
cp com.user.togglescrolling.plist ~/Library/LaunchAgents/

# Load it
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.user.togglescrolling.plist

# Verify it's running
launchctl print gui/$(id -u)/com.user.togglescrolling | grep "state\|last exit"
```

You should see `state = spawn scheduled` and `last exit code = 0`.

## How It Works

The LaunchAgent runs the Python script every **15 seconds**: #you can customise it based on your preference in the plist script

1. Checks if your Bluetooth mouse is connected via `blueutil --is-connected`
2. Compares current state to last known state
3. **If state changed:**
   - Mouse connected → Disable natural scrolling (traditional scroll)
   - Mouse disconnected → Enable natural scrolling (trackpad-friendly)

## Configuration

### Change polling interval

Edit `com.user.togglescrolling.plist` and change `StartInterval`:

```xml
<key>StartInterval</key>
<integer>15</integer>  <!-- Run every 15 seconds (lower = more battery, higher = slower detection) -->
```

### View logs

```bash
# View normal output
tail -f /tmp/mouse_toggler_stdout.log

# View errors
tail -f /tmp/mouse_toggler_stderr.log
```

### Multiple mice

To support multiple Bluetooth mice, add them to a list:

```python
MOUSE_MACS = [
    "d5-39-51-c9-12-7b",  # Mouse 1
    "a1-23-45-67-89-bc",  # Mouse 2
]

def is_any_connected():
    for mac in MOUSE_MACS:
        if is_connected(mac):
            return True
    return False
```

## Uninstallation

```bash
# Stop the LaunchAgent
launchctl bootout gui/$(id -u)/com.user.togglescrolling

# Remove the plist
rm ~/Library/LaunchAgents/com.user.togglescrolling.plist

# (Optional) Remove the script
rm -rf /usr/local/opt/mouse_toggler
```

## Troubleshooting

### Script not running

Check if LaunchAgent is loaded:
```bash
launchctl print gui/$(id -u)/com.user.togglescrolling
```

If `state = not running`, reload it:
```bash
launchctl bootout gui/$(id -u)/com.user.togglescrolling
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.user.togglescrolling.plist
```

### Permission denied errors

Remove quarantine attribute:
```bash
xattr -d com.apple.quarantine mouse_toggler.py
```

### Check script manually

```bash
python3 mouse_toggler.py
```

Then check logs:
```bash
cat /tmp/mouse_toggler_stdout.log
cat /tmp/mouse_toggler_stderr.log
```

### Wrong MAC address

Verify your mouse MAC:
```bash
blueutil --paired | grep -i "your mouse name"
```

## Battery Impact

- **At 15-second intervals:** Negligible (~1-2% impact)
- **At 5-second intervals:** Noticeable (~5-10% impact)
- Script only modifies settings when state *changes*, minimizing overhead

## How to find this in System Settings

Your natural scrolling setting is located at:
```
System Settings → Trackpad → Scrolling → Natural scrolling
```

This script automates toggling that setting.

## Advanced: Clean up logs automatically

Create `/usr/local/opt/mouse_toggler/com.user.togglescrolling-cleanup.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.togglescrolling-cleanup</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>truncate -s 0 /tmp/mouse_toggler_stdout.log /tmp/mouse_toggler_stderr.log 2>/dev/null</string>
    </array>
    <key>StartInterval</key>
    <integer>30</integer>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

Then load it:
```bash
launchctl bootstrap gui/$(id -u) /usr/local/opt/mouse_toggler/com.user.togglescrolling-cleanup.plist
```

## License

MIT

## Contributing

Feel free to submit issues and PRs!

---

**Questions?** Open an issue on GitHub or check the logs in `/tmp/mouse_toggler_stdout.log`
