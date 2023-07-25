import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter
from pytube import YouTube
import os
import requests
from io import BytesIO

def hide_status():
    statusLabel.pack_forget()

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_value_text = str(int(percentage_of_completion))
    progressPercentage.configure(text=progress_value_text + "%")
    progressPercentage.update()
    progressBar.set(float(percentage_of_completion) / 100)

def get_unique_filename(folder, filename, count=1):
    base, ext = os.path.splitext(filename)
    new_filename = f"{base}({count}){ext}"

    if os.path.exists(os.path.join(folder, new_filename)):
        return get_unique_filename(folder, filename, count + 1)
    else:
        return new_filename

def download_video():
    statusLabel.pack_forget()
    resolutionDropdown.pack_forget()
    searchBtn.pack_forget()
    downloadBtn.pack_forget()
    progressPercentage.pack(padx=10, pady=10)
    progressBar.pack(padx=10)

    try:
        ytLink = inputLink.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        video = ytObject.streams.filter(res=resolutionDropdown.get()).first()

        title.configure(text=ytObject.title, text_color="white")
        statusLabel.configure("Downloading...")

        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        desired_filename = f"{ytObject.title}_{selected_resolution.get()}.mp4"

        if os.path.exists(os.path.join("downloads", desired_filename)):
            unique_filename = get_unique_filename("downloads", desired_filename)
            video.download(output_path="downloads", filename=unique_filename)
        else:
            video.download(output_path="downloads", filename=desired_filename)

        url_var.set("")
        statusLabel.configure(text=f"{ytObject.title} is downloaded!", text_color="green")
        title.configure(text="Input a Youtube Link")
        searchBtn.pack(padx=10, pady=10)
        thumbnail_label.pack_forget()
    except:
        statusLabel.configure(text="Download Error!", text_color="red")
        searchBtn.pack(padx=10, pady=10)
        resolutionDropdown.pack(padx=10, pady=10)
        downloadBtn.pack(padx=10, pady=10)

    statusLabel.pack(padx=10, pady=10)
    app.after(3000, hide_status)
    progressPercentage.pack_forget()
    progressBar.pack_forget()
    
    
def search_video():
    try:
        ytLink = inputLink.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        title.configure(text=ytObject.title, text_color="white")
        resolutions = [stream.resolution for stream in ytObject.streams]
        resolutions = set(list(resolutions))
        resolutions = [res for res in resolutions if res is not None]
        resolutions.sort(key=lambda res: int(res[:-1]), reverse=True)

        resolutionDropdown['values'] = ()
        resolutionDropdown['values'] = resolutions

        # for resolution in resolutions:
        #    print(resolution)

        highest_resolution = ytObject.streams.get_highest_resolution().resolution
        resolutionDropdown.set(highest_resolution)

        thumbnail_url = ytObject.thumbnail_url
        response = requests.get(thumbnail_url)
        image = Image.open(BytesIO(response.content))
        image = image.resize((320, 180))
        thumbnail_image = ImageTk.PhotoImage(image)
        thumbnail_label.configure(image=thumbnail_image)
        thumbnail_label.image = thumbnail_image
        
        inputLink.pack_forget()
        searchBtn.pack_forget()
        statusLabel.pack_forget()
        resolutionDropdown.pack_forget()
        downloadBtn.pack_forget()
        thumbnail_label.pack(padx=10, pady=10)
        inputLink.pack(padx=10, pady=10)
        searchBtn.pack(padx=10, pady=10)

        statusLabel.configure(text="Select the desired resolution", text_color="white")
        statusLabel.pack(padx=10, pady=10)
        resolutionDropdown.pack(padx=10, pady=10)
        downloadBtn.pack(padx=10, pady=10)
        
    except:
        statusLabel.configure(text="Please enter a valid link", text_color="white")
        app.after(3000, hide_status)
        downloadBtn.pack_forget()


# system settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# app frame
app = customtkinter.CTk()
app.geometry("720x480") #screen size
app.title("Youtube Video Downloader")

# adding UI elements: access customtkinter to add element to the UI (added to app variable, with the custom text)
title = customtkinter.CTkLabel(app, text="Input a YouTube link", font=("Helvetica", 25))
title.pack(padx=10, pady=10) # add the label element with padding

# image
thumbnail_label = tk.Label(app)

# link input
url_var = customtkinter.StringVar()
inputLink = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
inputLink.pack()

# finished downloading
statusLabel = customtkinter.CTkLabel(app, text="")

# progress percentage
progressPercentage = customtkinter.CTkLabel(app, text="0%")
progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)

def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)

selected_resolution = tk.StringVar() 

# Create the Combobox widget for resolution selection
resolutionDropdown = ttk.Combobox(app, values=(), textvariable=selected_resolution)

# search button
searchBtn = customtkinter.CTkButton(app, text="Search", command=search_video)
searchBtn.pack(padx=10, pady=10)

# download button
downloadBtn = customtkinter.CTkButton(app, text="Download", command=download_video)
# downloadBtn.pack(padx=10, pady=10)

# run app
app.mainloop()