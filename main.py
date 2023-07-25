import tkinter as tk
import customtkinter
from pytube import YouTube
import os

def hide_status():
    finishLabel.pack_forget()

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_value_text = str(int(percentage_of_completion))
    progressPercentage.configure(text=progress_value_text + "%")
    progressPercentage.update()
    progressBar.set(float(percentage_of_completion) / 100)

def download_video():
    downloadBtn.pack_forget()
    progressPercentage.pack(padx=10, pady=10)
    progressBar.pack(padx=10)

    try:
        ytLink = inputLink.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution()

        title.configure(text=ytObject.title, text_color="white")
        finishLabel.configure(text="Input a YouTube link")

        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        video.download(output_path="downloads", filename=ytObject.title + ".mp4")

        url_var.set("")
        finishLabel.configure(text=f"{ytObject.title} is downloaded!", text_color="green")
    except:
        finishLabel.configure(text="Download Error!", text_color="red")

    finishLabel.pack(padx=10, pady=10)
    app.after(3000, hide_status)
    title.configure(text="Input a Youtube Link")
    progressPercentage.pack_forget()
    progressBar.pack_forget()
    downloadBtn.pack(padx=10, pady=10)
    

# system settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# app frame
app = customtkinter.CTk()
app.geometry("720x480") #screen size
app.title("Youtube Video Downloader")

# adding UI elements: access customtkinter to add element to the UI (added to app variable, with the custom text)
title = customtkinter.CTkLabel(app, text="Input a YouTube link", font=("Helvetica", 20))
title.pack(padx=10, pady=10) # add the label element with padding

# link input
url_var = customtkinter.StringVar()
inputLink = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
inputLink.pack()

# finished downloading
finishLabel = customtkinter.CTkLabel(app, text="")

# progress percentage
progressPercentage = customtkinter.CTkLabel(app, text="0%")
progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)

# download button
downloadBtn = customtkinter.CTkButton(app, text="Download", command=download_video)
downloadBtn.pack(padx=10, pady=10)

# run app
app.mainloop()