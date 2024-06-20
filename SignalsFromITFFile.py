# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 08:56:05 2024

@author: a423465

Description
This file takes an ITF file and pulls all the signal names from it. This ITF file is created by doing a "Copy to file" of a signal group within a storage group in IPEtroink CAETEC plugin.
"""

import tkinter as tk
from tkinter import filedialog

window = tk.Tk()

window.geometry("750x130")
window.title("Signal Extractor")
window.configure(bg = "#787c8a")

tk.Label(window, text="Input ITF file:", width=25).grid(column=0, row=0)
tk.Label(window, text="Output file:", width=25).grid(column=0, row=1)
tk.Label(window, text="1. Click the grey 'Browse' button to find itf file.", width=70).grid(column=1, row=3)
tk.Label(window, text="2. Input and Output entries will auto populate with locations when input file is selected.", width=70).grid(column=1, row=4)
tk.Label(window, text="3. Click 'Extract'.", width=70).grid(column=1, row=5)

txt1 = tk.Entry(window, width=70)
txt2 = tk.Entry(window, width=70)
txt1.grid(column=1, row=0, padx=2, pady=2)
txt2.grid(column=1, row=1, padx=2, pady=2)

def clicked():
    inputName = txt1.get()
    outputName = txt2.get()

    inputFileName = inputName
    outputFileName = outputName
    try:
        print(inputFileName)
        print(outputFileName)
        with open(inputFileName) as fileData:
            for line in fileData.readlines():
                split_data = line.split("</channelName>")

        signal_names = [""] * len(split_data)
        signal_strings = [""] * len(split_data)
        for i in range(len(split_data)):
            signal_strings[i] = split_data[i]
            signal_name = ""
            for c in reversed(split_data[i]):
                character = c
                if(character==">"):
                    signal_names[i]  = signal_name
                    break
                signal_name += character

        for i in range(len(signal_names)):
            signal_names[i] = signal_names[i][::-1]

        outputFile = open(outputFileName, "w")
        for signal in signal_names:
            if not signal:
                continue
            outputFile.write(signal + "\n")
        print("Signals extracted")

    except:
        print("File could not be converted.")

    return

def open_inputName():
    file = filedialog.askopenfile(mode='r', filetypes=[('ITF Files', '*.ITF')])
    if file:
        txt1.delete(0, tk.END)
        txt1.insert(0, file.name)
        outputName = file.name
        outputName = outputName[:-4]
        outputName = outputName + "_signal_list.csv"
        txt2.delete(0, tk.END)
        txt2.insert(0, outputName)

btn1 = tk.Button(window, text = "Extract", command = clicked, bg = "#0377fc", fg = "white")
btn2 = tk.Button(window, text = "Browse", command = open_inputName)
btn1.grid(column=2, row=1)
btn2.grid(column=2, row=0)

window.mainloop()