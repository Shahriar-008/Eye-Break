import tkinter as tk
from tkinter import Label
import threading
import time
from plyer import notification
import winsound
import ctypes

class EyeReminder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window
        self.interval_minutes = 10  # Fixed interval in minutes
        self.reminder_thread = threading.Thread(target=self.show_reminder_loop, daemon=True)
        self.reminder_thread.start()
        self.root.mainloop()

    def show_popup(self):
        # Create popup
        popup = tk.Toplevel(self.root)
        popup.title("Eye Break!")

        # Center popup
        sw, sh = popup.winfo_screenwidth(), popup.winfo_screenheight()
        ww, wh = 320, 220
        x, y = (sw - ww) // 2, (sh - wh) // 2
        popup.geometry(f"{ww}x{wh}+{x}+{y}")
        popup.lift()
        popup.attributes('-topmost', True)

        bg = popup.cget('bg')

        # Canvas-based blinking eyes
        canvas = tk.Canvas(popup, width=300, height=130, bg=bg, highlightthickness=0)
        canvas.pack(pady=(12, 6))

        msg = tk.Label(popup, text="Time to blink!\nTake a short eye break", font=('Arial', 12))
        msg.pack(pady=(0, 6))

        btn = tk.Button(popup, text="OK", command=popup.destroy)
        btn.pack(pady=6)

        def draw_eye(cx, cy, r=40):
            # Circular eye bounds
            x1, y1, x2, y2 = cx - r, cy - r, cx + r, cy + r

            # Outer eye ring and sclera
            canvas.create_oval(x1, y1, x2, y2, outline='#1f2937', width=2)
            canvas.create_oval(x1+2, y1+2, x2-2, y2-2, fill='white', outline='')

            # Iris gradient (concentric circles)
            iris_layers = []
            colors = ['#0ea5e9', '#22b0ee', '#38bdf8', '#60ccfb', '#93defe']
            ir = int(r * 0.48)
            for i, col in enumerate(reversed(colors)):
                rr = int(ir * (1 - i * 0.18))
                iris_layers.append(canvas.create_oval(cx-rr, cy-rr, cx+rr, cy+rr, fill=col, outline=''))

            # Dark iris ring
            canvas.create_oval(cx-ir, cy-ir, cx+ir, cy+ir, outline='#0f172a', width=1)

            # Pupil
            pr = int(ir * 0.45)
            pupil = canvas.create_oval(cx-pr, cy-pr, cx+pr, cy+pr, fill='#0b1020', outline='')

            # Specular highlight
            hl = canvas.create_oval(cx-pr+3, cy-pr+3, cx-pr+9, cy-pr+9, fill='#e2e8f0', outline='')

            # Curved eyelids using arcs (chords), animated by resizing bbox
            pad = 2
            top_lid = canvas.create_arc(x1-pad, y1-pad, x2+pad, y1, start=0, extent=180, style='chord', fill=bg, outline=bg)
            bot_lid = canvas.create_arc(x1-pad, y2, x2+pad, y2+pad, start=180, extent=180, style='chord', fill=bg, outline=bg)

            # A few subtle eyelashes
            lash_len = 10
            for dx in (-r*0.5, -r*0.2, r*0.2, r*0.5):
                canvas.create_line(cx+dx, y1-2, cx+dx-3, y1-2-lash_len, fill='#1f2937', width=2, capstyle='round')

            movables = iris_layers + [pupil, hl]
            return {'bounds': (x1, y1, x2, y2), 'top': top_lid, 'bottom': bot_lid, 'movables': movables}

        left = draw_eye(110, 65, r=42)
        right = draw_eye(190, 65, r=42)

        def drift(eye, t):
            import math
            x1, y1, x2, y2 = eye['bounds']
            cx, cy = (x1+x2)/2, (y1+y2)/2
            r = 3
            dx = r * math.cos(t/10.0)
            dy = r * math.sin(t/12.0)
            # Move all circular iris layers, pupil and highlight together
            # Compute current center from the first movable
            if not eye['movables']:
                return
            ix1, iy1, ix2, iy2 = canvas.coords(eye['movables'][0])
            icx, icy = (ix1+ix2)/2, (iy1+iy2)/2
            ox, oy = (cx+dx)-icx, (cy+dy)-icy
            for item in eye['movables']:
                canvas.move(item, ox, oy)

        state = {'t': 0}
        def idle():
            if not popup.winfo_exists():
                return
            state['t'] += 1
            drift(left, state['t'])
            drift(right, state['t'])
            popup.after(90, idle)

        def set_lids(eye, frac):
            # frac: 0 open, 1 closed
            x1, y1, x2, y2 = eye['bounds']
            h = (y2 - y1)
            # Top lid: grow its bbox downward to cover upper half
            ty2 = y1 + h * frac
            canvas.coords(eye['top'], x1-2, y1-2, x2+2, ty2)
            # Bottom lid: grow its bbox upward to cover lower half
            by1 = y2 - h * frac
            canvas.coords(eye['bottom'], x1-2, by1, x2+2, y2+2)

        def blink_once(cb=None):
            frames, dur = 10, 18
            def close_step(i=0):
                if not popup.winfo_exists():
                    return
                f = min(1.0, i/frames)
                set_lids(left, f)
                set_lids(right, f)
                if i < frames:
                    popup.after(dur, lambda: close_step(i+1))
                else:
                    popup.after(80, open_step)
            def open_step(i=0):
                if not popup.winfo_exists():
                    return
                f = max(0.0, 1 - i/frames)
                set_lids(left, f)
                set_lids(right, f)
                if i < frames:
                    popup.after(dur, lambda: open_step(i+1))
                else:
                    if cb:
                        cb()
            try:
                winsound.Beep(1200, 60)
            except Exception:
                pass
            close_step()

        def blink_loop(n=3):
            def next_blink(k):
                if k <= 0 or not popup.winfo_exists():
                    return
                blink_once(lambda: popup.after(180, lambda: next_blink(k-1)))
            next_blink(n)

        idle()
        blink_loop(3)
        popup.after(5000, popup.destroy)
    
    def is_screen_on(self):
        # More robust: use GetDevicePowerState to check monitor power
        import ctypes.wintypes
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        # Get the handle to the monitor (primary monitor)
        hMonitor = user32.MonitorFromWindow(user32.GetDesktopWindow(), 1)  # MONITOR_DEFAULTTOPRIMARY = 1
        # Get the device name
        class MONITORINFOEXW(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.wintypes.DWORD),
                ("rcMonitor", ctypes.wintypes.RECT),
                ("rcWork", ctypes.wintypes.RECT),
                ("dwFlags", ctypes.wintypes.DWORD),
                ("szDevice", ctypes.c_wchar * 32)
            ]
        info = MONITORINFOEXW()
        info.cbSize = ctypes.sizeof(MONITORINFOEXW)
        if not user32.GetMonitorInfoW(hMonitor, ctypes.byref(info)):
            return True  # Assume on if can't get info
        # Open a handle to the device
        hDev = kernel32.CreateFileW(
            r"\\.\\" + info.szDevice,
            0,
            0,
            None,
            3,  # OPEN_EXISTING
            0,
            None
        )
        if hDev == -1:
            return True  # Assume on if can't open device
        # Query power state
        powerState = ctypes.wintypes.BOOL()
        ret = kernel32.DeviceIoControl(
            hDev,
            0x294414,  # IOCTL_VIDEO_QUERY_DISPLAY_POWER_STATE
            None,
            0,
            ctypes.byref(powerState),
            ctypes.sizeof(powerState),
            ctypes.byref(ctypes.wintypes.DWORD()),
            None
        )
        kernel32.CloseHandle(hDev)
        if not ret:
            return True  # Assume on if can't query
        # powerState == 1 means on, 4 means off
        return powerState.value == 1

    def show_reminder_loop(self):
        while True:
            if self.is_screen_on():
                self.root.after(0, self.show_popup)
                notification.notify(
                    title="Eye Break Reminder",
                    message="Time to take a break and blink your eyes!",
                    timeout=3
                )
            time.sleep(self.interval_minutes * 60)  # Wait for fixed interval
    
    def start(self):
        self.reminder_thread.start()
        self.root.mainloop()

if __name__ == "__main__":
    reminder = EyeReminder()
