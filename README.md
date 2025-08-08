# Eye Blink Reminder

A customizable eye blink reminder for Windows, built with Python and Tkinter. This tool helps you maintain eye health by reminding you to blink at user-defined intervals with a popup, sound, and notification. The interval is persistent and can be changed via a simple GUI.

## Features
- Set your own reminder interval (in minutes) via a GUI
- Interval is saved and persists between runs
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
- Set your desired interval in the GUI and click "Start Reminder".
- The interval will be saved for future runs.

## Run on Startup (Optional)
1. Create a batch file `eye_reminder.bat`:
   ```bat
   @echo off
   cd /d D:\Programming\PY Code\Eye Break
   "D:\Programming\PY Code\Eye Break\.venv\Scripts\python.exe" "D:\Programming\PY Code\Eye Break\demo.py"
   ```
2. (Recommended) Create a VBScript `eye_reminder_launcher.vbs` to run silently:
   ```vbscript
   Set WshShell = CreateObject("WScript.Shell")
   WshShell.Run chr(34) & "D:\Programming\PY Code\Eye Break\eye_reminder.bat" & chr(34), 0
   Set WshShell = Nothing
   ```
3. Place the `.vbs` file in your Windows Startup folder (`Win + R`, type `shell:startup`).

## How It Works
- When started, a GUI lets you set the interval (in minutes).
- The interval is saved to `interval.txt` and loaded automatically on next run.
- Every interval, if your screen is active, a popup with blinking eyes and a sound will remind you to blink, and a Windows notification will appear.
- If your screen is sleeping, the reminder is skipped until the next interval.

## License
MIT License

## Author
Shahriar Hossen
