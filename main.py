import tkinter as tk
from time import sleep
from tkinter import W
from tkinter.filedialog import askopenfilename
from tkinter.font import Font

from neural_network.neural_network import *

FORM = tk.Tk()
FORM.title(TITLE)
FORM.geometry("570x420")
FORM.config(bg="#CFDBDA")

neural_net = NeuralNetwork()
filename=None
fontt = Font(family='Segoe UI Symbol', size=16)
def create_out_path(filename:str):
    words = filename.split('.')
    string = "".join(words[:len(words)-1])
    return f'{string}_output.avi'

def cut_filename(filename:str):
    res = filename.split('/')
    return "/".join(res[len(res)-2:])

def link(*args):
    neural_net.OpenVideo('assets/demo.mp4')
def link2(*args):
    global filename
    filename = askopenfilename(filetypes=filetypes)
    if filename != "":
        button3['state'] = tk.NORMAL
        button4['state'] = tk.NORMAL
        labelopfile.config(text=cut_filename(filename))
def link3(*args):
    if filename is not None:
        neural_net.OpenVideo(filename)
def link4(*args):
    label.place(x=195, y=265)
    label.config(text="Video Processing...")
    FORM.update()
    if filename is not None:
        neural_net.SaveVideo(filename, create_out_path(filename))
    label.place(x=135, y=265)
    label.config(text="Processing completed successfully")
    FORM.update()
    sleep(2)
    label.config(text="")
    FORM.update()
button = tk.Button(
    FORM,
    command=link,
    padx=175,
    pady=3,
    text="Open demo video",
    bd=0,
    bg="#8AAAA5",
    underline=0,
    cursor="hand2",
    font=fontt
)  # Инициализация кнопки
#button.grid(column=0, row=3, pady=4, padx=25)
button2 = tk.Button(
    FORM,
    command=link2,
    padx=17,
    pady=3,
    text="Open file",
    bd=0,
    bg="#8AAAA5",
    underline=0,
    cursor="hand2",
    font=fontt
)  # Инициализация кнопки
#button2.grid(column=0, row=0, pady=4, padx=25)
button3 = tk.Button(
    FORM,
    command=link3,
    padx=197,
    pady=3,
    text="Watch video",
    bd=0,
    bg="#8AAAA5",
    underline=0,
    cursor="hand2",
    state=tk.DISABLED,
    font=fontt
)  # Инициализация кнопки
#button3.grid(column=0, row=2, pady=4, padx=25)
button4 = tk.Button(
    FORM,
    command=link4,
    padx=155,
    pady=3,
    text="Save processed video",
    bd=0,
    bg="#8AAAA5",
    underline=0,
    cursor="hand2",
    state=tk.DISABLED,
    font=fontt
)  # Инициализация кнопки
#button4.grid(column=0, row=1, pady=4, padx=25)
label = tk.Label(text="", bg="#CFDBDA", fg="#708479")
label.place(x=195, y=265)
labelopfile = tk.Label(text="", bg="#CFDBDA", fg="#708479")
labelopfile.place(x=170, y=85)
labelmainname = tk.Label(text="Detect medical mask on people", bg="#CFDBDA")

label.config(font=fontt)
labelopfile.config(font=fontt)
labelmainname.config(font=('Segoe UI Semibold', 20))

labelmainname.pack(pady=15, anchor=W, padx=25)
button2.pack(pady=5, anchor=W, padx=25)
button3.pack(pady=5, anchor=W, padx=25)
button4.pack(pady=5, anchor=W, padx=25)
button.pack(pady=50, anchor=W, padx=25)

filetypes = [
            ("Video File1", "*.mp4"),
            ("Video File2", "*.avi")
            ]


def focus_inb(event):
    event.widget.configure(fg="#000")
    event.widget.configure(bg="#fff")


def focus_outb(event):
    event.widget.configure(bg="#8AAAA5")
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