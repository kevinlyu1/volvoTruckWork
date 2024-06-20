# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: a423465
"""

import functions
import tkinter as tk
from tkinter import filedialog

window = tk.Tk()

window.geometry("750x165")
window.title("LDF2DBC Converter")
window.configure(bg = "#787c8a")

tk.Label(window, text="Input LDF file:", width=25).grid(column=0, row=0)
tk.Label(window, text="Output file:", width=25).grid(column=0, row=1)
tk.Label(window, text="Channel number 1-16 (CH):", width=25).grid(column=0, row=2)
tk.Label(window, text="1. Click the grey 'Browse' button to find ldf file.", width=70).grid(column=1, row=3)
tk.Label(window, text="2. Input and Output entries will auto populate with locations when input file is selected.", width=70).grid(column=1, row=4)
tk.Label(window, text="3. Add a channel number 1-16 for the LIN channel.", width=70).grid(column=1, row=5)
tk.Label(window, text="4. Click blue 'Convert'", width=70).grid(column=1, row=6)

txt1 = tk.Entry(window, width=70)
txt2 = tk.Entry(window, width=70)
txt3 = tk.Entry(window, width=70)
txt1.grid(column=1, row=0, padx=2, pady=2)
txt2.grid(column=1, row=1, padx=2, pady=2)
txt3.grid(column=1, row=2, padx=2, pady=2)

def clicked():
    inputName = txt1.get()
    outputName = txt2.get()
    channel = txt3.get()

    inputFileName = inputName
    outputFileName = outputName
    
    try:
        channel = int(channel)
        if channel < 1 or channel > 16:
            fileName = "File could not be converted. Channel number is invalid."
            print(fileName)
            return
        else:
            outputFileName = outputFileName.replace("<ch>", str(channel))
            print(inputFileName)
            print(outputFileName)

        inputFile = open(inputFileName, "r")
        fileContent = inputFile.read()
        newFileContent = functions.remove_comments(fileContent)
        signalsIndex = functions.find_set_index(newFileContent, "Signals")
        signalSection = functions.find_set(newFileContent, signalsIndex)
        signals = functions.extract_signals_section(signalSection)
        framesIndex = functions.find_set_index(newFileContent, "Frames")
        frames = functions.extract_frames_section(newFileContent, framesIndex)
        signalEncodingTypesIndex = functions.find_set_index(newFileContent, "Signal_encoding_types")
        signalEncodingTypes = functions.extract_signal_encoding_section(newFileContent, signalEncodingTypesIndex)
        signalRepresentationIndex = functions.find_set_index(newFileContent, "Signal_representation")
        signalRepresentation = functions.extract_signal_representation_section(newFileContent, signalRepresentationIndex)
        inputFile.close()

        outputFile = open(outputFileName, "w")
        outputFile.write("\nVERSION \"\"\n")
        outputFile.write("\nNS_: " + functions.add_new_symbols() + "\n") 
        outputFile.write("\nBS_: 500000 : 0,0\n") # Defines the baud rate of the DBC
        outputFile.write("\nBU_: " + functions.find_all_nodes(signals) + "\n")

        for message in frames:
            functions.write_messsages(outputFile, message, frames, channel)
            currentMessageSignals = frames[message]["signals"]["signal"]
            for signalName in currentMessageSignals:
                functions.write_signals(outputFile, signalName, signals, signalEncodingTypes, message, frames, signalRepresentation)
        outputFile.close()
        print("File converted")

    except:
        print("File could not be converted.")

    return

def open_inputName():
    file = filedialog.askopenfile(mode='r', filetypes=[('LDF Files', '*.ldf')])
    if file:
        txt1.delete(0, tk.END)
        txt1.insert(0, file.name)
        outputName = file.name
        outputName = outputName[:-4]
        outputName = outputName + "_LIN<ch>.dbc"
        txt2.delete(0, tk.END)
        txt2.insert(0, outputName)

btn1 = tk.Button(window, text = "Convert", command = clicked, bg = "#0377fc", fg = "white")
btn2 = tk.Button(window, text = "Browse", command = open_inputName)
btn1.grid(column=2, row=2)
btn2.grid(column=2, row=0)

window.mainloop()
