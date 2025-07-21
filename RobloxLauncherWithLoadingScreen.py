import tkinter as tk
from tkinter import ttk
import threading
import time
import os
import ctypes
import sys
import psutil
from PIL import Image, ImageTk

def find_roblox_player():
    possible_paths = [
        os.path.join(os.environ['LOCALAPPDATA'], 'Roblox', 'Versions'),
        os.path.join(os.environ.get('ProgramFiles(x86)', ''), 'Roblox', 'Versions'),
        os.path.join(os.environ.get('ProgramFiles', ''), 'Roblox', 'Versions'),
    ]
    for base_path in possible_paths:
        if os.path.exists(base_path):
            for root, dirs, files in os.walk(base_path):
                if 'RobloxPlayerBeta.exe' in files:
                    exe_path = os.path.join(root, 'RobloxPlayerBeta.exe')
                    os.startfile(exe_path)
                    return True
    ctypes.windll.user32.MessageBoxW(
        0,
        "RobloxPlayerBeta.exe not found.\nPlease make sure Roblox is installed.",
        "Error",
        0x10
    )
    return False

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def show_splash():
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash_width = 300
    splash_height = 220
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x = int((screen_width / 2) - (splash_width / 2))
    y = int((screen_height / 2) - (splash_height / 2))
    splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")
    splash.configure(bg="white")

    try:
        logo_img = Image.open(resource_path("logo.png"))
        logo_img = logo_img.resize((100, 100), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(splash, image=logo_photo, bg="white")
        logo_label.image = logo_photo
        logo_label.pack(pady=(30, 10))
    except Exception:
        logo_label = tk.Label(splash, text="", bg="white")
        logo_label.pack(pady=(30, 10))

    splash_label = tk.Label(splash, text="G7 Technologies", font=("Segoe UI", 16), bg="white")
    splash_label.pack(pady=(0, 20))

    splash.after(1800, splash.destroy)  # Show splash for 1.8 seconds
    splash.update()
    return splash

def launch_with_loading():
    def task():
        print("Task: Updating label to 'Looking for Roblox...'")
        label.config(text="Looking for Roblox...")
        root.update_idletasks()
        print("Task: Searching for RobloxPlayerBeta.exe")
        found = find_roblox_player()
        if found:
            print("Task: Updating label to 'Launching Roblox...'")
            label.config(text="Launching Roblox...")
            root.update_idletasks()
            print("Task: Waiting for user feedback (1.5s)")
            time.sleep(2.0)
        print("Task: Quitting loading screen")
        root.quit()
    threading.Thread(target=task, daemon=True).start()

root = tk.Tk()
root.withdraw()  # Hide main window during splash

# Show splash screen
splash = show_splash()
splash.wait_window()

root.deiconify()
root.overrideredirect(True)

try:
    root.iconbitmap(resource_path("g7logo.ico"))
except Exception:
    pass

window_width = 350
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

root.resizable(False, False)
root.configure(bg="white")

try:
    logo_img = Image.open(resource_path("logo.png"))
    logo_img = logo_img.resize((80, 80), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(root, image=logo_photo, bg="white")
    logo_label.image = logo_photo
    logo_label.pack(pady=(15, 5))
except Exception:
    pass

label = tk.Label(root, text="Launching Roblox...", font=("Segoe UI", 14), bg="white")
label.pack(pady=10)

progress = ttk.Progressbar(root, mode='indeterminate', length=250)
progress.pack(pady=10)
progress.start(10)


launch_with_loading()
root.mainloop()