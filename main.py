import tkinter as tk
from tkinter import LEFT
from neural_network.neural_network import *

FORM = tk.Tk()
FORM.geometry("500x300")
FORM.config(bg="#ffdb8f")

neural_net = NeuralNetwork()


def link():
    neural_net.OpenFromWebCamera()


button = tk.Button(
    FORM,
    command=link,
    padx=20,
    pady=20,
    text="Вебкамера",
    bd=0,
    bg="#00bfff",
    underline=0,
    cursor="hand2",
)  # Инициализация кнопки
button.pack(side=LEFT, expand=1)


# choices available with user.
def check(*args):
    neural_net.OpenVideo(videos.get(variable.get()))


videos = {
    "Лондон": "assets/videos/2.mp4",
    "Нью-Йорк": "assets/videos/3.mp4",
    "Санкт-Петербург": "assets/videos/4.mp4",
}

variable = tk.StringVar(value="Выбрать камеру")
variable.set("Выбрать камеру")
variable.trace_add("write", check)

#  creating widget
dropdown = tk.OptionMenu(FORM, variable, *videos)
dropdown.configure(width=20, height=3, bd=0, bg="#00bfff", underline=0, cursor="hand2")
# positioning widget
dropdown.pack(side=LEFT, expand=1)


def focus_inb(e=None):
    button.configure(fg="#000")
    button.configure(bg="#fff")


def focus_outb(e=None):
    button.configure(bg="#00bfff")
    button.configure(fg="#000")


button.bind("<Enter>", focus_inb)
button.bind("<Leave>", focus_outb)


FORM.mainloop()
