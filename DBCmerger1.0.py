"""
Merges two .dbc-files. Easy!

Works with Python3.11!

If you cant open the dbc file after merge, try to switch the order of the input dbc files.

Questions? Ask Andreas!
"""

import functions
import tkinter as tk
from tkinter import filedialog

window = tk.Tk()

window.geometry("750x250")
window.title("DBC Merger")
window.configure(bg = "#787c8a")

tk.Label(window, text="First DBC file:", width=25).grid(column=0, row=0)
tk.Label(window, text="Second DBC file:", width=25).grid(column=0, row=1)
tk.Label(window, text="Output file (must be full path):", width=25).grid(column=0, row=2)
tk.Label(window, text="1. Click the grey 'Browse1' button to find the first file.", width=70).grid(column=1, row=3)
tk.Label(window, text="2. Click the grey 'Browse2' button to find the second file.", width=70).grid(column=1, row=4)
tk.Label(window, text="3. Output will auto populate if no location is given.", width=70).grid(column=1, row=5)
tk.Label(window, text="The location will be the folder where the first DBC was pulled from.", width=70).grid(column=1, row=6)
tk.Label(window, text="4. Click blue 'Merge'", width=70).grid(column=1, row=7)

txt1 = tk.Entry(window, width=70)
txt2 = tk.Entry(window, width=70)
txt3 = tk.Entry(window, width=70)
txt1.grid(column=1, row=0, padx=2, pady=2)
txt2.grid(column=1, row=1, padx=2, pady=2)
txt3.grid(column=1, row=2, padx=2, pady=2)

def clicked():
    inputName1 = txt1.get()
    inputName2 = txt2.get()
    if not txt3.get():
        tempName = functions.clean_file_names(inputName1, inputName2)
        txt3.insert(0, tempName)
        outputName = txt3.get()
    else:
        outputName = txt3.get()
    
    inputFileName1 = inputName1
    inputFileName2 = inputName2
    outputFileName = outputName
    
    try:
        print(inputFileName1)
        print(inputFileName2)
        print(outputFileName)
        functions.main(inputFileName1, inputFileName2, outputFileName)
        print("File merged")
    
    except:
        print("File could not be merged.")

    return

def open_inputName1():
    file = filedialog.askopenfile(mode='r', filetypes=[('DBC Files', '*.dbc')])
    if file:
        txt1.delete(0, tk.END)
        txt1.insert(0, file.name)
        
def open_inputName2():
    file = filedialog.askopenfile(mode='r', filetypes=[('DBC Files', '*.dbc')])
    if file:
        txt2.delete(0, tk.END)
        txt2.insert(0, file.name)


btn1 = tk.Button(window, text = "Convert", command = clicked, bg = "#0377fc", fg = "white")
btn2 = tk.Button(window, text = "Browse1", command = open_inputName1)
btn3 = tk.Button(window, text = "Browse2", command = open_inputName2)
btn1.grid(column=2, row=2)
btn2.grid(column=2, row=0)
btn3.grid(column=2, row=1)

window.mainloop()
