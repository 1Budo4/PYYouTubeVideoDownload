import tkinter
import customtkinter
from pytube import YouTube
from PIL import ImageTk
from urllib.request import urlopen
import threading

dir = 'C:\\Users\\Marko\\Desktop'

def chgDir():
    global dir
    dir = customtkinter.filedialog.askdirectory()
    print(dir)

def getThumb():
    try:
        ytLink = link.get()
        thumbCode = ytLink[ytLink.find('=')+1:]
        thumbLink = 'https://i.ytimg.com/vi/' + thumbCode + '/hqdefault.jpg?sqp=-oaymwEnCOADEI4CSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIHBACGAYgATgB&rs=AOn4CLDqosrCb7K5VMjMb2jX0AP5akSuRw'
        data = urlopen(thumbLink)
        thumbnail = ImageTk.PhotoImage(data=data.read())
        thumbnailImage.configure(image=thumbnail)
    except:
        print('THUMBNAIL CANT LOAD')
    
def startDownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution()
        title.configure(text=ytObject.title, text_color="white")
        finishLabel.configure(text="")  
        video.download(dir)
        finishLabel.configure(text="DOWNLOADED!", text_color='green')
    except:
        finishLabel.configure(text="DOWNLOAD ERROR!", text_color='red')

def downloadBtn():
    threading.Thread(target=getThumb).start()
    threading.Thread(target=startDownload).start()

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percetage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percetage_of_completion))
    pPercentage.configure(text=per + '%')
    pPercentage.update()
    progressBar.set(float(percetage_of_completion) / 100)

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("800x580")
app.title("Youtube Downloader")
app.iconbitmap('ytdl.ico')

title = customtkinter.CTkLabel(app, text="Insert a youtube link")
title.pack(padx=10, pady=10)

url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=30, textvariable=url_var)
link.pack()

finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)

thumbnailImage = customtkinter.CTkLabel(app, text='', width=480, height=270,)
thumbnailImage.pack()

download = customtkinter.CTkButton(app, text="Download", command=downloadBtn)
download.pack(padx=10, pady=10)

directory = customtkinter.CTkButton(app, text="Change Directory", command=chgDir)
directory.pack(padx=10, pady=10)

app.mainloop()