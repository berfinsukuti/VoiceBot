import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *


import sqlite3 as sql

window = tk.Tk()

window.geometry("800x500")
window.title("Giriş Sayfası")

labelg = tk.Label(window, text = "GİRİŞ SAYFASI", font = "Times 16", fg = "black")
labelg.place(x = 350, y = 10)

labelemail = tk.Label(window, text = "E-Mail: ", font = "Times 12", fg = "black")
labelemail.place(x=30, y=60)

labelparola = tk.Label(window, text = "Parola: ", font = "Times 12", fg = "black")
labelparola.place(x=30, y=120)

entry_email =tk.Entry(window, width=50)
entry_email.insert(string="@gmail.com", index =0)
entry_email.place(x = 120, y = 60)

entry_parola =tk.Entry(window, width=50)
entry_parola.insert(string="", index =0)
entry_parola.place(x = 120, y = 125)

girisyap = tk.Button(window, text = "Giriş Yap", fg = "black")
girisyap.place(x = 120, y = 200)


window.mainloop()