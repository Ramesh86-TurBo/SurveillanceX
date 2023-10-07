# Import necessary libraries
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import threading
import requests
import torch
from pathlib import Path
from ultralytics import YOLO
import sqlite3
from datetime import datetime

# Check for GPU availability
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Initialize the YOLO model
models_dir = Path('models')
models_dir.mkdir(exist_ok=True)
SEG_MODEL_NAME = "yolov8n-seg"
seg_model = YOLO(models_dir / f'{SEG_MODEL_NAME}.pt').to(device)

# Define stream URLs
STREAM_URLS = [
    "http://192.168.12.12:8080/shot.jpg",
    "http://your-second-stream-url.com",
    "http://your-third-stream-url.com",
    "http://your-fourth-stream-url.com",
]

# Initialize the default stream URL
STREAM_URL = STREAM_URLS[0]

# Create a SQLite database connection and cursor
conn = sqlite3.connect("detection_log.db")
cursor = conn.cursor()

# Create a table to store detection results if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS detection_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    detection INTEGER,
                    time TEXT,
                    stream INTEGER
                )''')

# Commit the changes and close the database connection
conn.commit()
conn.close()

# Create a Tkinter window
root = tk.Tk()
root.title("People Counter GUI")

# Function to get a frame from the video stream
def get_frame_from_stream(url: str) -> np.ndarray:
    response = requests.get(url)
    if response.status_code == 200:
        frame = np.asarray(bytearray(response.content), dtype=np.uint8)
        return cv2.imdecode(frame, cv2.IMREAD_COLOR)
    else:
        return None

# Function to start the video feed
def start_video_feed():
    global is_video_playing
    if not is_video_playing:
        is_video_playing = True
        video_thread = threading.Thread(target=process_video_feed)
        video_thread.start()

# Function to stop the video feed
def stop_video_feed():
    global is_video_playing
    is_video_playing = False

# Function to process the video feed
def process_video_feed():
    while is_video_playing:
        frame = get_frame_from_stream(STREAM_URL)
        if frame is not None:
            frame = cv2.resize(frame, (640, 640))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_tensor = torch.from_numpy(frame / 255.0).permute(2, 0, 1).unsqueeze(0).to(device)
            res = seg_model(frame_tensor)
            box_multi_list = []
            centr_pt_cur_fr = []
            result = res[0]
            classes = np.array(result.boxes.cls.cpu(), dtype="int")
            confidence = np.array(result.boxes.conf.cpu())
            bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")

            idx = []
            for i in range(0, len(classes)):
                if classes[i] == 0:
                    idx.append(i)

            bbox = []
            for i in idx:
                temp = bboxes[i]
                bbox.append(temp)
                box_multi_list = [arr.tolist() for arr in bbox]

            for box in box_multi_list:
                (x, y, x2, y2) = box
                cv2.rectangle(frame, (x, y), (x2, y2), (255, 255, 0), 1)
                cx = int((x+x2)/2)
                cy = int((y+y2)/2)
                centr_pt_cur_fr.append((cx, cy))
                cv2.circle(frame, (cx, cy), 5, (255, 255, 0), -3)

            head_count = len(centr_pt_cur_fr)
            count_var = head_count

            text = f'Head Count: {head_count}'
            cv2.putText(frame, text, (15, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)

            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = cv2.resize(frame, (640, 480))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(image=frame)
            video_label.config(image=frame)
            video_label.image = frame

            # Log the detection result to the database including the selected stream option
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            selected_stream = STREAM_URLS.index(STREAM_URL) + 1  # Assuming stream options start from 1
            conn = sqlite3.connect("detection_log.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO detection_log (detection, time, stream) VALUES (?, ?, ?)", (head_count, current_time, selected_stream))
            conn.commit()
            conn.close()
   
        else:
            print("Failed to retrieve frame from the stream.")
            break

# Function to handle window close event
def on_closing():
    global is_video_playing
    if is_video_playing:
        stop_video_feed()
    root.destroy()

# Bind the window close event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Define stream selection options
options = ["Stream 1", "Stream 2", "Stream 3", "Stream 4"]

# Function to handle stream selection from the dropdown menu
def dropdown_selected(event):
    global STREAM_URL
    selected_option = dropdown_var.get()
    if selected_option == "Stream 1":
        STREAM_URL = STREAM_URLS[0]
    elif selected_option == "Stream 2":
        STREAM_URL = STREAM_URLS[1]
    elif selected_option == "Stream 3":
        STREAM_URL = STREAM_URLS[2]
    elif selected_option == "Stream 4":
        STREAM_URL = STREAM_URLS[3]
    stop_video_feed()
    start_video_feed()

# Create the main GUI window
main_frame = ttk.Frame(root, padding=10)
main_frame.grid(column=0, row=0, sticky=(tk.W, tk.N, tk.E, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Configure GUI styles
style = ttk.Style()
style.configure("Professional.TButton", foreground="white", background="#007acc", padding=(10, 5))

# Create a dropdown menu for stream selection
dropdown_var = tk.StringVar()
dropdown = ttk.Combobox(main_frame, textvariable=dropdown_var, values=options)
dropdown.set(options[0])
dropdown.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
dropdown.bind("<<ComboboxSelected>>", dropdown_selected)

# Create a button to start the video feed
button_start = ttk.Button(main_frame, text="Start Video", command=start_video_feed, style="Black.TButton")
button_start.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)

# Create a button to stop the video feed
button_stop = ttk.Button(main_frame, text="Stop Video", command=stop_video_feed, style="Black.TButton" )
button_stop.grid(column=1, row=1, padx=5, pady=5, sticky=tk.W)

# Create a label to display the video stream
video_label = ttk.Label(main_frame)
video_label.grid(column=2, row=0, rowspan=5, padx=10, pady=10, sticky=(tk.N, tk.W, tk.E, tk.S))

# Initialize a global variable to manage the video feed state
is_video_playing = False

# Main event loop
root.mainloop()
