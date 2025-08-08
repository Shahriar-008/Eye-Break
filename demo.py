import tkinter as tk
from tkinter import Label
import threading
import time
from plyer import notification
import winsound
import os
import ctypes

class EyeReminder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window
        self.interval_file = "interval.txt"
        self.interval_minutes = self.load_interval()
        self.reminder_thread = None
        self.show_interval_gui()

    def load_interval(self):
        if os.path.exists(self.interval_file):
            try:
                with open(self.interval_file, 'r') as f:
                    val = int(f.read().strip())
                    if val > 0:
                        return val
            except Exception:
                pass
        return 10  # Default interval

    def save_interval(self, val):
        try:
            with open(self.interval_file, 'w') as f:
                f.write(str(val))
        except Exception:
            pass

    def show_interval_gui(self):
        self.interval_win = tk.Toplevel()
        self.interval_win.title("Set Reminder Interval")
        self.interval_win.geometry("300x150")
        self.interval_win.attributes('-topmost', True)
        label = tk.Label(self.interval_win, text="Set interval (minutes):", font=("Arial", 12))
        label.pack(pady=10)
        self.interval_var = tk.StringVar(value=str(self.interval_minutes))
        entry = tk.Entry(self.interval_win, textvariable=self.interval_var, font=("Arial", 12), justify='center')
        entry.pack(pady=5)
        set_btn = tk.Button(self.interval_win, text="Start Reminder", font=("Arial", 12), command=self.start_reminder)
        set_btn.pack(pady=10)
        entry.focus()
        self.interval_win.protocol("WM_DELETE_WINDOW", self.on_close_interval_win)

    def on_close_interval_win(self):
        self.root.destroy()

    def start_reminder(self):
        try:
            val = int(self.interval_var.get())
            if val <= 0:
                raise ValueError
            self.interval_minutes = val
            self.save_interval(val)
        except ValueError:
            tk.messagebox.showerror("Invalid Input", "Please enter a positive integer for minutes.")
            return
        self.interval_win.destroy()
        self.root.deiconify()
        self.reminder_thread = threading.Thread(target=self.show_reminder_loop, daemon=True)
        self.reminder_thread.start()
        self.root.mainloop()

    def show_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Eye Break!")
        
        # Set window to appear in the center of screen
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        window_width = 300
        window_height = 200
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        popup.geometry(f'{window_width}x{window_height}+{x}+{y}')
        popup.lift()  # Bring window to front
        popup.attributes('-topmost', True)  # Keep window on top
        
        # Eye ASCII art frames for blinking
        open_eyes = """
        .-========-.
       / 👁️  👁️  \\
      /     👃     \\
      |     👄     |
       \\         /
        '-....-'
        """
        closed_eyes = """
        .-========-.
       /  -   -   \\
      /     👃     \\
      |     👄     |
       \\         /
        '-....-'
        """
        eye_label = Label(popup, text=open_eyes, font=('Courier', 14))
        eye_label.pack(pady=20)
        
        message = Label(popup, text="Time to blink!\nTake a 20-second break", font=('Arial', 12))
        message.pack(pady=10)
        
        # Close button
        close_button = tk.Button(popup, text="OK", command=popup.destroy)
        close_button.pack(pady=10)
        
        # Blinking animation
        def blink(count=0):
            if count < 6:  # 3 blinks (open/close)
                eye_label.config(text=closed_eyes if count % 2 else open_eyes)
                # Play a short beep for each blink (frequency=1200Hz, duration=80ms)
                winsound.Beep(1200, 80)
                popup.after(300, lambda: blink(count + 1))
            else:
                eye_label.config(text=open_eyes)
        blink()
        
        # Auto close after 5 seconds
        popup.after(5000, popup.destroy)
    
    def is_screen_on(self):
        user32 = ctypes.windll.user32
        # 0x0073 = SPI_GETPOWEROFFACTIVE, 0x11 = SC_MONITORPOWER
        # SendMessageW returns 1 if monitor is on, 2 if off
        HWND_BROADCAST = 0xFFFF
        WM_SYSCOMMAND = 0x0112
        SC_MONITORPOWER = 0xF170
        # 1 = low power, 2 = shut off
        # We'll use GetForegroundWindow as a proxy for activity
        # If the monitor is off, GetForegroundWindow returns 0
        return user32.GetForegroundWindow() != 0

    def show_reminder_loop(self):
        while True:
            if self.is_screen_on():
                self.root.after(0, self.show_popup)
                notification.notify(
                    title="Eye Break Reminder",
                    message="Time to take a break and blink your eyes!",
                    timeout=3
                )
            time.sleep(self.interval_minutes * 60)  # Wait for user-set interval
    
    def start(self):
        self.reminder_thread.start()
        self.root.mainloop()

if __name__ == "__main__":
    reminder = EyeReminder()
