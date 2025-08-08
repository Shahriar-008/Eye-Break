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
        self.interval_minutes = 10  # Default interval in minutes
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
