import json
import tkinter as tk
from tkinter import LEFT, TOP, W, Button, Label, Toplevel
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter.font import Font
import os.path
from pathlib import Path
from neural_network.neural_network import *


FORM = tk.Tk()
FORM.title(TITLE)
FORM.geometry("570x350")
FORM.config(bg="#CFDBDA")
FORM.resizable(width=0, height=0)


neural_net = NeuralNetwork()
filename = None
fontt = Font(family="Segoe UI Symbol", size=16)


def create_out_path(filename: str):
    words = filename.split(".")
    string = "".join(words[: len(words) - 1])
    return f"{string}_output{Path(filename).suffix}"


def cut_filename(filename: str):
    res = filename.split("/")
    return "/".join(res[len(res) - 2 :])


def link2(*args):
    global filename
    filename = askopenfilename(filetypes=filetypes)
    if filename != "":
        button3["state"] = tk.NORMAL
        button4["state"] = tk.NORMAL
        labelopfile.config(text=cut_filename(filename))
        label.config(text="")
        FORM.update()


def link3(*args):
    if filename is not None:
        s = neural_net.OpenVideo(filename)
        words = filename.split(".")
        string = "".join(words[: len(words) - 1])
        fs = f"{string}_watch.json"
        with open(fs, "w", encoding="utf8") as f:
            json.dump(s, f, indent=4)


def save(f):
    label.place(x=195, y=265)
    label.config(text="Video Processing...")
    FORM.update()
    neural_net.SaveVideo(filename, f)
    label.place(x=135, y=265)
    label.config(text="Processing completed successfully")
    FORM.update()


def link4(*args):
    if filename is not None:
        f = create_out_path(filename)
        if os.path.exists(f):
            createPopUp(
                f,
                "Saving videos",
                f"A file named {f} exists \nOverwrite the file?",
            )
        else:
            save(f)


def createPopUp(f, t, m):
    answer = Toplevel(FORM)
    fontAns = Font(family="Segoe UI Symbol", size=10)
    answer.title(t)
    answer.config(bg="#CFDBDA")
    answer.geometry("400x200")
    answer.resizable(width=0, height=0)
    answer.grab_set()
    # Yes/No
    def yesbut():
        answer.destroy()
        save(f)

    def nobut():
        answer.destroy()
                
    def savebut():
        pth=filedialog.asksaveasfilename(filetypes=filetypes)
        if pth:
            answer.destroy()
            if not Path(pth).suffix:
                pth+=Path(filename).suffix
            save(pth)

    label = Label(
        answer,
        wraplength=300,
        justify=LEFT,
        font=fontAns,
        bg="#CFDBDA",
        text=m,
    )
    label.pack(pady=30, side=TOP)
    b1 = Button(
        answer,
        text="Yes",
        font=fontAns,
        command=yesbut,
        width=12,
        bd=0,
        pady=5,
        bg="#8AAAA5",
        underline=0,
        cursor="hand2",
    )
    b2 = Button(
        answer,
        text="No",
        font=fontAns,
        command=nobut,
        width=12,
        pady=5,
        bd=0,
        bg="#8AAAA5",
        underline=0,
        cursor="hand2",
    )
    b3 = Button(
        answer,
        text="Choose path",
        font=fontAns,
        command=savebut,
        width=12,
        pady=5,
        bd=0,
        bg="#8AAAA5",
        underline=0,
        cursor="hand2",
    )
    b1.place(x=30,y=150)
    b2.place(x=280,y=150)
    b3.place(x=155, y=150)


# button.grid(column=0, row=3, pady=4, padx=25)
button2 = Button(
    FORM,
    command=link2,
    padx=17,
    pady=3,
    text="Open file",
    bd=0,
    bg="#8AAAA5",
    underline=0,
    cursor="hand2",
    font=fontt,
)  # Инициализация кнопки
# button2.grid(column=0, row=0, pady=4, padx=25)
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
    font=fontt,
)  # Инициализация кнопки
# button3.grid(column=0, row=2, pady=4, padx=25)
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
    font=fontt,
)  # Инициализация кнопки
# button4.grid(column=0, row=1, pady=4, padx=25)
label = tk.Label(text="", bg="#CFDBDA", fg="#708479")
label.place(x=195, y=265)
labelopfile = tk.Label(text="", bg="#CFDBDA", fg="#708479")
labelopfile.place(x=170, y=85)
labelmainname = tk.Label(text="Detect medical mask on people", bg="#CFDBDA")

label.config(font=fontt)
labelopfile.config(font=fontt)
labelmainname.config(font=("Segoe UI Semibold", 20))

labelmainname.pack(pady=15, anchor=W, padx=25)
button2.pack(pady=5, anchor=W, padx=25)
button3.pack(pady=5, anchor=W, padx=25)
button4.pack(pady=5, anchor=W, padx=25)

filetypes = [("Video File1", "*.mp4"), ("Video File2", "*.avi")]


def focus_inb(event):
    event.widget.configure(fg="#000")
    event.widget.configure(bg="#fff")


def focus_outb(event):
    event.widget.configure(bg="#8AAAA5")
    event.widget.configure(fg="#000")


button2.bind("<Enter>", focus_inb)
button2.bind("<Leave>", focus_outb)
button3.bind("<Enter>", focus_inb)
button3.bind("<Leave>", focus_outb)
button4.bind("<Enter>", focus_inb)
button4.bind("<Leave>", focus_outb)

FORM.mainloop()
