from tkinter import *
from tkinter import messagebox as mb
from pytube import YouTube
from pytube.cli import on_progress
from tkinter import ttk
import os,threading
import time

root = Tk()
root.title('Youtube Video Downloader')
root.geometry('700x300')
root.resizable(0, 0)
root.config(bg='Coral')
my_progress=ttk.Progressbar(root,orient=HORIZONTAL,length=400,mode="determinate")
my_progress.place(relx=0.25, rely=0.6)

def get():
    global yt,my_progress,dropdown,clicked
    yt_link = str(link_strvar.get())
    try:
        yt = YouTube(yt_link)
    except:
        mb.showinfo("ERROR","Connection Error")
    clicked=StringVar()
    if click=="GET VIDEO":
        resolution= [stream.resolution for stream in yt.streams.filter(file_extension="mp4",progressive=True).all()]
        print(resolution)
        clicked.set("Select Resolution")
        dropdown=OptionMenu(root,clicked,*resolution)
        dropdown.place(relx=0.5,rely=0.49)

def on_progress(stream, chunk, bytes_remaining):
  global inc,my_progress
  total_size = stream.filesize
  bytes_downloaded = total_size - bytes_remaining
  percentage_of_completion = bytes_downloaded / total_size * 100
  inc=int(percentage_of_completion)
  print(inc)
  my_progress["value"]+=inc-my_progress["value"]
  root.update_idletasks()
  time.sleep(0.5)
  if my_progress["value"]==100:
    mb.showinfo("Youtube Downloader","Downloaded Successfully")

def downloader():
    global my_prodress
    save_path = dir_strvar.get()
    file=yt.streams.filter(res=clicked.get()).first()
    size=file.filesize
    yt.register_on_progress_callback(on_progress)  
    yt.streams.filter(res=clicked.get()).first().download(save_path)
    
def reset():
    link_strvar.set('')
    dir_strvar.set('')
    my_progress["value"]=0

def about():
    mb.showinfo('About','This program is created by: Kartikey Shah')

def thread(b):
  global click
  click=b
  thread=threading.Thread(target=get)
  thread.start()



Label(root, text='Youtube Video Downloader', font=("Comic Sans MS", 15), bg='Coral').place(relx=0.25, rely=0.0)

Label(root, text='Enter the Youtube link:', font=("Times New Roman", 13), bg='Coral').place(relx=0.05, rely=0.2)

link_strvar = StringVar()
link_entry = Entry(root, width=50, textvariable=link_strvar)
link_entry.place(relx=0.5, rely=0.2)


Label(root, text='Enter the save location:', font=("Times New Roman", 13), bg='Coral').place(relx=0.05, rely=0.4)

dir_strvar = StringVar()
dir_entry = Entry(root, width=50, textvariable=dir_strvar)
dir_entry.place(relx=0.5, rely=0.4)

button1=Button(root,text="Resolutions:",font=("Arial Bold",10),bg="#c2dcf0",command=lambda b="GET VIDEO":thread(b)).place(relx=0.25, rely=0.49)


download_btn = Button(root, text='Download', font=7, bg='Aquamarine',command=downloader).place(relx=0.3, rely=0.75)

reset_btn = Button(root, text='Reset', font=7, bg='Aquamarine',command=reset).place(relx=0.5, rely=0.75)

about_btn = Button(root, text='About', font=7, bg='Aquamarine', command=about, height=1, width=6)
about_btn.place(relx=0.65, rely=0.75)

root.update()
root.mainloop()
