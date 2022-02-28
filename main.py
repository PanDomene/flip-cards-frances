from tkinter import *
import random
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
ES = "Español"
FR = "Francés"
data = None

try:
    data = pd.read_csv("data/por_aprender.csv")
except FileNotFoundError:
    data = pd.read_csv("data/palabras_frances.csv")
finally:
    por_aprender = pd.DataFrame()
    frances = data.Frances.to_list()
    frances_juego_actual = data.Frances.to_list()
    espanol = data.Español.to_list()
    espanol_juego_actual = data.Español.to_list()

palabra_fr = ""
palabra_es = ""
flip_timer = None
# ----------------------------------- CARD FLIP --------------------------------#


def start():
    global palabra_fr, palabra_es, flip_timer
    window.after_cancel(flip_timer)
    palabra_fr = random.choice(frances_juego_actual)
    palabra_es = espanol_juego_actual[frances_juego_actual.index(palabra_fr)]
    canvas.itemconfig(card, image=FRONT_CARD)
    canvas.itemconfig(title, text=FR, fill="black")
    canvas.itemconfig(word, text=palabra_fr.title(), fill="black")
    flip_timer = window.after(5000, flip)


def flip():
    canvas.itemconfig(card, image=BACK_CARD)
    canvas.itemconfig(title, text=ES, fill="white")
    canvas.itemconfig(word, text=palabra_es.title(), fill="white")


# ------------------------------------ BUTTONS---------------------------------#

def know():
    frances_juego_actual.remove(palabra_fr)
    espanol_juego_actual.remove(palabra_es)
    return start()


def dont_know():
    return start()


def eliminate_word():
    global por_aprender, frances, espanol
    frances.remove(palabra_fr)
    espanol.remove(palabra_es)
    las_que_quedan = {"Frances": frances, "Español": espanol}
    por_aprender = pd.DataFrame(las_que_quedan)
    por_aprender.to_csv("data/por_aprender.csv", index=False)
    know()

# ------------------------------------ UI SETUP --------------------------------#


window = Tk()
window.title("Flash Cards")
window.config(bg=BACKGROUND_COLOR, width=900, height=900, padx=50, pady=50)

flip_timer = window.after(3000, flip)
FRONT_CARD = PhotoImage(file="images/card_front.png")
BACK_CARD = PhotoImage(file="images/card_back.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card = canvas.create_image(400, 263, image=FRONT_CARD)
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=3)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=know)
right_button.grid(row=1, column=1)
wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=dont_know)
wrong_button.grid(row=1, column=0)
elim_button = Button(text="Quitar\nPalabra", command=eliminate_word)
elim_button.grid(row=1, column=2)

start()

window.mainloop()
