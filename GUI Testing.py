# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 14:58:38 2023

@author: a423465
"""

import functions
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showinfo

window = tk.Tk()

window.geometry("600x200")
window.title("LDF2DBC Converter")
window.configure(bg = "#787c8a")

tk.Label(window, text="Input LDF file:").grid(column=0, row=0)
tk.Label(window, text="Output file:").grid(column=0, row=1)
tk.Label(window, text="Channel number 1-16 (CH):").grid(column=0, row=2)

txt1 = tk.Entry(window, width = 50)
txt2 = tk.Entry(window, width = 50)
txt3 = tk.Entry(window, width = 50)
txt1.grid(column = 1, row = 0)
txt2.grid(column = 1, row = 1)
txt3.grid(column = 1, row = 2)

def clicked():
    inputName = txt1.get()
    outputName = txt2.get()
    channel = txt3.get()

    inputFileName = "./" + inputName + ".ldf"
    outputFileName = "./" + outputName + "_LIN" + channel + ".dbc"
    print(inputFileName)
    print(outputFileName)

    return

def open_inputName():
    file = filedialog.askopenfile(mode='r', filetypes=[('LDF Files', '*.ldf')])
    if file:
        print(file.name)
        txt1.delete(0, tk.END)
        txt1.insert(0, file.name)

btn1 = tk.Button(window, text = "convert", command = clicked, bg = "#0377fc", fg = "white")
btn1.grid(column = 1, row = 3)

btn2 = tk.Button(window, text = "Browse", command = open_inputName)
btn2.grid(column=2, row=0)

window.mainloop()
