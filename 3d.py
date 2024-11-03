import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy.editor import VideoFileClip
import os

# Define the maximum file size (2GB)
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024
output_file = "3d_movie.mp4"

def process_video(file_path, progress_var):
    global output_file
    # Load video
    video = VideoFileClip(file_path)
    fps = video.fps
    width, height = video.size
    total_frames = int(video.fps * video.duration)
    
    # Define OpenCV video writer for saving the output
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Iterate through frames and update progress
    for i, frame in enumerate(video.iter_frames(fps=fps)):
        # Create a stereoscopic effect by shifting the red and cyan channels
        left_frame = np.copy(frame)
        right_frame = np.copy(frame)

        # Shift red channel for left eye and cyan for right eye
        left_frame[:, :, 1:] = 0  # Remove green and blue for left frame
        right_frame[:, :, 0] = 0  # Remove red for right frame

        # Shift frames slightly to simulate depth
        left_shifted = np.zeros_like(left_frame)
        right_shifted = np.zeros_like(right_frame)

        left_shifted[:, :-10, :] = left_frame[:, 10:, :]  # Shift left frame right
        right_shifted[:, 10:, :] = right_frame[:, :-10, :]  # Shift right frame left

        # Merge both frames
        stereo_frame = cv2.addWeighted(left_shifted, 0.5, right_shifted, 0.5, 0)

        # Write processed frame to the output video
        out.write(stereo_frame)

        # Update the progress bar
        progress_var.set((i + 1) / total_frames * 100)
        root.update_idletasks()

    # Release the video writer
    out.release()
    return output_file

def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("MP4 files", "*.mp4")], title="Select a .mp4 file"
    )
    if not file_path:
        return

    # Check file size
    if os.path.getsize(file_path) > MAX_FILE_SIZE:
        messagebox.showerror("File Too Large", "File must be 2GB or less.")
        return

    # Process the video
    messagebox.showinfo("Processing", "Please wait while we process the video.")
    output_path = process_video(file_path, progress_var)
    messagebox.showinfo("Completed", f"3D movie saved as {output_path}")

    # Enable download button
    download_button.config(state="normal")

def download_file():
    save_path = filedialog.asksaveasfilename(
        defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")], title="Save 3D movie as"
    )
    if save_path:
        os.rename(output_file, save_path)
        messagebox.showinfo("Download Complete", f"3D movie downloaded to {save_path}")

# GUI setup
root = tk.Tk()
root.title("Sidhaant's MP4 File to 3D Video Converter")  # Updated title
root.geometry("400x300")

label = tk.Label(root, text="Upload a .mp4 file to convert it to 3D", font=("Arial", 14))
label.pack(pady=20)

upload_button = tk.Button(root, text="Upload .mp4", command=open_file, font=("Arial", 12))
upload_button.pack(pady=10)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=10, fill=tk.X, padx=20)

# Download button, initially disabled until processing is complete
download_button = tk.Button(root, text="Download 3D Movie", command=download_file, font=("Arial", 12), state="disabled")
download_button.pack(pady=10)

root.mainloop()
