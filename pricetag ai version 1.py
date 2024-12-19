import base64
import requests
from openai import OpenAI
from PIL import Image
import cv2
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
from ttkthemes import ThemedTk
import pandas as pd

# Initialize OpenAI client
client = OpenAI(api_key="im not telling you my api key")

# Excel file setup
output_file = "analysis_results.xlsx"
def initialize_excel():
    if not os.path.exists(output_file):
        df = pd.DataFrame(columns=["Item", "Condition", "Price", "Special Info"])
        df.to_excel(output_file, index=False)

initialize_excel()

# Function to capture an image using OpenCV
def capture_image(selected_camera, save_path="captured_image.jpg"):
    cam = cv2.VideoCapture(selected_camera)
    if not cam.isOpened():
        messagebox.showerror("Error", "Camera could not be opened!")
        return None

    print("Press 's' to save the image and 'q' to quit preview.")
    while True:
        ret, frame = cam.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture frame.")
            break

        cv2.imshow("Camera Preview", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            cv2.imwrite(save_path, frame)
            print(f"Image saved to {save_path}")
            break
        elif key == ord('q'):
            print("Preview exited.")
            break

    cam.release()
    cv2.destroyAllWindows()
    return save_path if os.path.exists(save_path) else None

# Function to encode the image in base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Function to analyze image using OpenAI's API
def analyze_image(image_path):
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Analyze the object in this image."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "You are an assistant trained to analyze images and provide concise details in four words: (1) the object in the image, (2) the object's condition (brand new to worn out), (3) the suitable price for the object to be sold in a charity store (cheaper than market price), and (4) identify if there is something special about the item (usually 'none')."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    },
                ],
            }
        ],
    )
    return response.choices[0].message.content

# Function to record response in Excel
def record_to_excel(item, condition, price, special_info):
    df = pd.read_excel(output_file)
    new_entry = pd.DataFrame({"Item": [item], "Condition": [condition], "Price": [price], "Special Info": [special_info]})
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_excel(output_file, index=False)

# UI Application class
def start_ui():
    def update_camera_list():
        camera_options.clear()
        for i in range(5):
            cam = cv2.VideoCapture(i)
            if cam.isOpened():
                camera_options.append(f"Camera {i}")
                cam.release()

    def capture_and_analyze():
        selected_camera = camera_listbox.current()
        if selected_camera == -1:
            messagebox.showerror("Error", "Please select a camera!")
            return

        image_path = capture_image(selected_camera)
        if not image_path:
            return

        print("Analyzing image...")
        analysis = analyze_image(image_path)
        print("Analysis Result:")
        print(analysis)

        # Parse and record the response
        try:
            phrases = analysis.split('\n')
            item, condition, price, special_info = phrases[0], phrases[1], phrases[2], phrases[3]
            record_to_excel(item, condition, price, special_info)
            result_label["text"] = f"Analysis Recorded:\n{item}, {condition}, {price}, {special_info}"
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse analysis: {e}")

    def quit_program():
        root.quit()
        root.destroy()

    root = ThemedTk(theme="equilux")
    root.title("Image Analysis Tool")
    root.geometry("500x400")
    root.configure(bg="#2E2E2E")

    # Custom Font
    custom_font = Font(family="Helvetica", size=12, weight="bold")

    # UI Elements
    tk.Label(root, text="Select Camera:", font=custom_font, bg="#2E2E2E", fg="white").pack(pady=10)

    camera_options = []
    update_camera_list()

    camera_listbox = ttk.Combobox(root, values=camera_options, state="readonly")
    camera_listbox.pack(pady=10)

    capture_button = tk.Button(root, text="Take Photo", font=custom_font, command=capture_and_analyze, bg="#4CAF50", fg="white", relief="groove", bd=2)
    capture_button.pack(pady=10)

    quit_button = tk.Button(root, text="Quit", font=custom_font, command=quit_program, bg="#f44336", fg="white", relief="groove", bd=2)
    quit_button.pack(pady=10)

    result_label = tk.Label(root, text="", font=custom_font, bg="#2E2E2E", fg="white", wraplength=450, justify="left")
    result_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    start_ui()