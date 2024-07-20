from tkinter import simpledialog
from pynput import keyboard
import tkinter as tk
import PIL.Image
import pyautogui
import pyperclip
import threading
import pystray
import os

if not os.path.isfile('config'):
    old_substring = '-'
    new_substring = ','
else:
    with open('config','r') as conf:
        old_substring, new_substring = [l.strip() for l in conf.readlines()]

class DualInputDialog(simpledialog.Dialog):
    def __init__(self, parent, title):
        self.old_substring = None
        self.new_substring = None
        super().__init__(parent, title)
    
    def body(self, master):
        tk.Label(master, text="String you want to replace:").grid(row=0)
        tk.Label(master, text="Change with:").grid(row=1)

        self.old_substring_entry = tk.Entry(master)
        self.new_substring_entry = tk.Entry(master)

        self.old_substring_entry.grid(row=0, column=1)
        self.new_substring_entry.grid(row=1, column=1)
        
        return self.old_substring_entry

    def apply(self):
        self.old_substring = self.old_substring_entry.get()
        self.new_substring = self.new_substring_entry.get()

        with open('config','w') as conf:
            conf.writelines([self.old_substring+'\n', self.new_substring])


def on_activate():
    try:
        pyautogui.sleep(0.5)
        pyautogui.hotkey('ctrl', 'c')
        text = pyperclip.paste()
        modified_text = text.replace(old_substring, new_substring)
        pyperclip.copy(modified_text)
        pyautogui.hotkey('ctrl', 'v')
        print(f"Modified text: {modified_text}")

    except Exception as e:
        print(f"Error: {e}")


def run(*arg):
    def for_canonical(f):
        return lambda k: f(l.canonical(k))
    
    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<alt>+,'), on_activate)

    with keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release)) as l:
        l.join()


def on_clicked(icon, item):
    if str(item) == "Exit":
        icon.visible = False
        icon.stop()
        os._exit(0)

def get_input():
    root = tk.Tk()
    root.withdraw()
    global old_substring
    global new_substring
    dialog = DualInputDialog(root, "Input")
    old_substring, new_substring = dialog.old_substring, dialog.new_substring
    root.destroy()

def background_task():
    image = PIL.Image.open("icon.png")


    icon = pystray.Icon("Clipboard Replacer", image, menu=pystray.Menu(
        pystray.MenuItem('Change Replacement', lambda *args: threading.Thread(target=get_input).start()),
        pystray.MenuItem("Exit", on_clicked)
    ))

    icon.run_detached()
    run()
    

if __name__ == "__main__":
    background_task()