import tkinter as tk
from time import sleep
from tkinter.filedialog import askopenfilename

from neural_network.neural_network import *

FORM = tk.Tk()
FORM.title(TITLE)
FORM.geometry("380x200")
FORM.config(bg="#ffdb8f")

neural_net = NeuralNetwork()
filename=None

def create_out_path(filename:str):
    words = filename.split('.')
    string = "".join(words[:len(words)-1])
    return f'{string}_output.avi'

def link(*args):
    neural_net.OpenVideo('assets/demo.mp4')
def link2(*args):
    global filename
    filename = askopenfilename(filetypes=filetypes)
    if filename != "":
        button3['state'] = tk.NORMAL
        button4['state'] = tk.NORMAL
def link3(*args):
    if filename is not None:
        neural_net.OpenVideo(filename)
def link4(*args):
    label.config(text="Video Processing...")
    FORM.update()
    if filename is not None:
        neural_net.SaveVideo(filename, create_out_path(filename))
    label.config(text="Processing completed successfully")
    FORM.update()
    sleep(2)
    label.config(text="")
    FORM.update()
button = tk.Button(
    FORM,
    command=link,
    padx=20,
    pady=20,
    text="Open demo video",
    bd=0,
    bg="#00bfff",
    underline=0,
    cursor="hand2",
)  # Инициализация кнопки
button.grid(column=0, row=1, padx=20, pady=20)
button2 = tk.Button(
    FORM,
    command=link2,
    padx=20,
    pady=20,
    text="Open file",
    bd=0,
    bg="#00bfff",
    underline=0,
    cursor="hand2",
)  # Инициализация кнопки
button2.grid(column=1, row=0, padx=20, pady=20)
button3 = tk.Button(
    FORM,
    command=link3,
    padx=20,
    pady=20,
    text="Watch video",
    bd=0,
    bg="#00bfff",
    underline=0,
    cursor="hand2",
    state=tk.DISABLED
)  # Инициализация кнопки
button3.grid(column=1, row=1, padx=20, pady=20)
button4 = tk.Button(
    FORM,
    command=link4,
    padx=20,
    pady=20,
    text="Save processed video",
    bd=0,
    bg="#00bfff",
    underline=0,
    cursor="hand2",
    state=tk.DISABLED
)  # Инициализация кнопки
button4.grid(column=0, row=0, padx=20, pady=20)
label = tk.Label(text="", bg="#ffdb8f")
label.place(x=40, y=85)
filetypes = [
            ("Video File1", "*.mp4"),
            ("Video File2", "*.avi")
            ]


def focus_inb(event):
    event.widget.configure(fg="#000")
    event.widget.configure(bg="#fff")


def focus_outb(event):
    event.widget.configure(bg="#00bfff")
    event.widget.configure(fg="#000")


button.bind("<Enter>", focus_inb)
button.bind("<Leave>", focus_outb)
button2.bind("<Enter>", focus_inb)
button2.bind("<Leave>", focus_outb)
button3.bind("<Enter>", focus_inb)
button3.bind("<Leave>", focus_outb)
button4.bind("<Enter>", focus_inb)
button4.bind("<Leave>", focus_outb)

FORM.mainloop()