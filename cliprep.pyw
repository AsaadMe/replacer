from tkinter import simpledialog
from pynput import keyboard
import tkinter as tk
import PIL.Image
import pyautogui
import pyperclip
import threading
import pystray
import os

replace_with = ','
def on_activate():
    try:
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.sleep(0.1)
        text = pyperclip.paste()
        modified_text = text.replace(' ', replace_with)
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
    if str(item) =="DO":
        print("DID")
    elif str(item) == "Exit":
        icon.visible = False
        icon.stop()
        os._exit(0)

def get_input():
    root = tk.Tk()
    root.withdraw()
    global replace_with
    user_input = simpledialog.askstring("Input", f"Change char \"{replace_with}\" with:")
    replace_with = user_input
    root.destroy()

def background_task():
    image = PIL.Image.open("icon.png")


    icon = pystray.Icon("Clipboard Replacer", image, menu=pystray.Menu(
        pystray.MenuItem('Replace with?', lambda *args: threading.Thread(target=get_input).start()),
        pystray.MenuItem("Exit", on_clicked)
    ))

    icon.run_detached()
    run()
    

if __name__ == "__main__":
    background_task()