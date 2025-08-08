
# Eye Blink Reminder

A simple eye blink reminder for Windows, built with Python and Tkinter. This tool helps you maintain eye health by reminding you to blink every 10 minutes with a popup, sound, and notification.

## Features
- Reminds you to blink every 10 minutes (default, not user-settable)
- Popup with blinking ASCII art eyes and sound effect
- Windows notification using `plyer`
- Reminders only appear if your screen is active (not sleeping)
- Can be set to run automatically at Windows startup (see below)

## Requirements
- Python 3.7+
- Windows OS
- Python packages: `tkinter`, `plyer`

## Installation
1. Clone this repository or download the files.
2. (Recommended) Create a virtual environment:
   ```sh
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install plyer
   ```

## Usage
Run the script:
```sh
python demo.py
```
The reminder will appear every 10 minutes automatically.


## Run on Startup (Optional)

### 1. Create or Edit the Batch File (`eye_reminder.bat`)
Example content:
```bat
@echo off
cd /d D:\Programming\PY Code\Eye Break
"D:\Programming\PY Code\Eye Break\.venv\Scripts\python.exe" "D:\Programming\PY Code\Eye Break\demo.py"
```

**How to customize:**
- Change all paths (`D:\Programming\PY Code\Eye Break`) to match the folder where you placed your project.
- If your Python virtual environment is in a different location, update the `.venv\Scripts\python.exe` path accordingly.

### 2. Create or Edit the VBScript (`eye_reminder_launcher.vbs`)
Example content:
```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "D:\Programming\PY Code\Eye Break\eye_reminder.bat" & chr(34), 0
Set WshShell = Nothing
```

**How to customize:**
- Change the path inside `chr(34) & "..." & chr(34)` to the location of your `.bat` file.

### 3. Add to Startup
- Press `Win + R`, type `shell:startup`, and press Enter.
- Copy your `.vbs` file into the Startup folder.

Now, your reminder will run automatically every time you log in to Windows.

## How It Works
- When started, the program runs in the background.
- Every 10 minutes, if your screen is active, a popup with blinking eyes and a sound will remind you to blink, and a Windows notification will appear.
- If your screen is sleeping, the reminder is skipped until the next interval.

## License
MIT License

## Author
Shahriar Hossen
