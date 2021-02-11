from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title("mp3 player")
root.geometry('600x400')

pygame.mixer.init()

def slide(x):
    global time_
    time_ = int(slider.get())
    tt = time.strftime("%M:%S",time.gmtime(time_))
    slider_label.config(text=f"{tt} of {converted_song_length}")
    current_song = song_box.curselection()
    current_song = current_song[0]

    song_name = song_list[current_song]
    pygame.mixer.music.load(song_name)
    pygame.mixer.music.play(loops=0,start=time_)

def add_song():
    global song_list
    file_ = filedialog.askopenfilenames(title="choose a song", filetypes=(('mp3 files', '*.mp3'),))
    song_list = []
    for files in file_:
        song_list.append(files)
        file_name = files.split('/')
        song = (file_name[len(file_name)-1])
        song_box.insert(END, song)

def status():
    current_time = int(pygame.mixer.music.get_pos() / 1000) 

    convert = time.strftime("%M:%S",time.gmtime(current_time))
    te = int(slider.get()) + 1
    print(f"current position: {current_time} and pos: {te}")
        

    current_song = song_box.curselection()
    current_song = current_song[0]

    song_name = song_list[current_song]

    song_mut = MP3(song_name)

    global song_time, converted_song_length
    song_time = song_mut.info.length
    converted_song_length = time.strftime("%M:%S", time.gmtime(song_time))

    if te == current_time:
        status_bar.config(text=f"{convert} of {converted_song_length}")
        slider.config(value=int(current_time))
    if int(song_time) == te:
        slider.config(value=0)
        forward()
    else:
        elapsed = time.strftime("%M:%S", time.gmtime(te))
        status_bar.config(text=f"{elapsed} of {converted_song_length}")
        slider.config(value=int(te))
        

    status_bar.after(1000,status)

def play():
    song = song_box.get(ACTIVE)
    for i in song_list:
        if song in i:
            pygame.mixer.music.load(i)
            pygame.mixer.music.play(loops=0)
            status()
            slider_position = song_time
            slider.config(to=slider_position, value=0)


global paused
paused = False
def pause(is_paused):
    global paused
    paused = is_paused

    if is_paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

def stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    status_bar.config(text="")
    slider.config(value=0)

def forward():
    next_ = song_box.curselection()
    next_ = next_[0]+1

    next_song = song_list[next_]
    pygame.mixer.music.load(next_song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0, END)
    song_box.activate(next_)
    song_box.selection_set(next_,last=None)

    status_bar.config(text="")
    slider.config(value=0)

def backward():
    previous = song_box.curselection()
    previous = previous[0]-1

    previous_song = song_list[previous]
    pygame.mixer.music.load(previous_song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0, END)
    song_box.activate(previous)
    song_box.selection_set(previous, last=None)

    status_bar.config(text="")
    slider.config(value=0)
        
song_box = Listbox(root, bg="grey", fg="black", width=80, selectbackground="black", selectforeground="white")
song_box.pack(pady=30)

pause_btn = PhotoImage(file="images/pause1.png")
play_btn = PhotoImage(file="images/play1.png")
stop_btn = PhotoImage(file="images/st1.png")
forward_btn = PhotoImage(file="images/fd1.png")
backward_btn = PhotoImage(file="images/bk1.png")

control_frame = Frame(root)
control_frame.pack()

pa_btn = Button(control_frame, image=pause_btn, borderwidth=0, command=lambda: pause(paused))
pl_btn = Button(control_frame, image=play_btn, borderwidth=0, command=play)
st_btn = Button(control_frame, image=stop_btn, borderwidth=0, command=stop)
fd_btn = Button(control_frame, image=forward_btn, borderwidth=0, command=forward)
bd_btn = Button(control_frame, image=backward_btn, borderwidth=0, command=backward)

pl_btn.grid(row=0, column=0, padx=25)
pa_btn.grid(row=0, column=1, padx=25)
st_btn.grid(row=0, column=2, padx=25)
bd_btn.grid(row=0, column=3, padx=25)
fd_btn.grid(row=0, column=4, padx=25)

my_menu = Menu(root)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="add songs", command=add_song)

status_bar = Label(root, text="", bd=1, anchor=E)
status_bar.pack(side=BOTTOM,fill=X)

slider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, command=slide,value=0)
slider.pack(fill=X, side=BOTTOM)

slider_label = Label(root,text="")
slider_label.pack(pady=20, side=BOTTOM)

root.mainloop()