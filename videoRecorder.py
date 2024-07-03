import numpy as np
import pyautogui
import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import datetime


resolution = (1920, 1080)
codec = cv2.VideoWriter_fourcc(*"XVID")
fps = 16.0
screen_width, screen_height = pyautogui.size()
window_width = 1020
window_height = 640

out = None
stop = False
previewing = True


def generate_filename():
    date = datetime.datetime.now()
    timestamp = date.strftime("%Y.%m.%d_%H.%M.%S")
    return f"Recording_{timestamp}.avi"
def start_recording():  
    global out, stop, previewing
    stop = False
    previewing = False
    filename = generate_filename()
    out = cv2.VideoWriter(filename, codec, fps, resolution)
    status_label.config(text="recording...")
    record()

def stop_recording():
    global out, stop, previewing
    stop = True
    previewing = True
    if out:
        out.release()
        out = None
    status_label.config(text = "saving video...")
    

def record():
    global out, stop, frame
    if not stop:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        out.write(frame)

        display_frame()
        root.after(16, record)

def preview():
    global previewing, frame
    if previewing:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        status_label.config(text="LIVE")
        display_frame()
        root.after(16, preview)

def display_frame():
    global frame
    size = scaling()
    frame = cv2.resize(frame, (size))
    
    img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  
    img_tk = ImageTk.PhotoImage(image=img_pil)
    video_label.imgtk = img_tk
    video_label.config(image=img_tk)

def scaling():
    scale_width = window_width / screen_width
    scale_height = window_height / screen_height
    scale = min(scale_width, scale_height)

    new_width = int(screen_width * scale)
    new_height = int(screen_height * scale)

    return new_width, new_height


root = tk.Tk()
root.title("Screen Recorder")

root.geometry(f"{window_width}x{window_height + 50}")


start_button = ttk.Button(root, text="Start Recording", command=start_recording)
start_button.pack(pady=10)

stop_button = ttk.Button(root, text="Stop Recording", command=stop_recording)
stop_button.pack(pady=10)

status_label = ttk.Label(root, text="...")
status_label.pack(padx=15)

video_label = ttk.Label(root)
video_label.pack(pady=10)

preview()  

root.mainloop()
