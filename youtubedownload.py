from pytube import YouTube
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def download_video(url, file_path, format_choice, progress_bar):
    try:
        yt = YouTube(url)

        # Update progress bar function to be called whenever a chunk is downloaded
        def progress_function(stream, chunk, bytes_remaining):
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percentage_of_completion = bytes_downloaded / total_size * 100
            progress_bar['value'] = percentage_of_completion
            root.update_idletasks()

        yt.register_on_progress_callback(progress_function)

        if format_choice == 'MP4':
            streams = yt.streams.filter(progressive=True, file_extension="mp4")
            chosen_stream = streams.get_highest_resolution()
        elif format_choice == 'MP3':
            streams = yt.streams.filter(only_audio=True)
            chosen_stream = streams.get_audio_only()

        chosen_stream.download(output_path=file_path)
        messagebox.showinfo("Success", f"Download completed successfully as {format_choice}!")

    except Exception as ex:
        messagebox.showerror("Error", str(ex))

def start_file_dialog():
    folder = filedialog.askdirectory()
    if folder:
        return folder
    return None

def on_download():
    video_url = url_entry.get()
    format_choice = format_var.get()
    if not video_url.strip():
        messagebox.showerror("Error", "Please enter a valid YouTube URL")
        return
    
    save_directory = start_file_dialog()
    if save_directory:
        download_video(video_url, save_directory, format_choice, progress_bar)
    else:
        messagebox.showerror("Error", "Please provide a valid saving location.")

# Setting up the main window
root = tk.Tk()
root.title("YouTube MP4 and MP3 Downloader")

# Calculate position to center the window
window_width = 800
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Creating widgets
url_label = ttk.Label(root, text="Enter YouTube URL:")
url_label.pack(pady=(20, 5))

url_entry = ttk.Entry(root, width=60)
url_entry.pack(pady=(0, 10))

format_label = ttk.Label(root, text="Select format:")
format_label.pack(pady=(10, 0))

format_var = tk.StringVar()
format_var.set("MP4")
format_options = ttk.Combobox(root, textvariable=format_var, values=['MP4', 'MP3'])
format_options.pack(pady=(0, 20))

download_button = ttk.Button(root, text="Download", command=on_download)
download_button.pack(pady=(0, 10))

progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
progress_bar.pack()

# Start the GUI
root.mainloop()
