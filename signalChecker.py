# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:57:40 2024

@author: a423465
"""

import tkinter as tk
from tkinter import filedialog
import pandas as pd
import cantools
import os
import functions


window = tk.Tk()

window.geometry("1010x300")
window.title("Signal Checker")
window.configure(bg = "#787c8a")

tk.Label(window, text="Input Excel Signal File:", width=25).grid(column=0, row=0)
tk.Label(window, text="DBC Folder:", width=25).grid(column=0, row=1)
tk.Label(window, text="Output found signals file:", width=25).grid(column=0, row=2)
tk.Label(window, text="Output not found signals file:", width=25).grid(column=0, row=3)
tk.Label(window, text="Instructions",width=70).grid(column=1, row=4)
tk.Label(window, text="1. Click the grey 'Browse' button to find the xlsx file, which contains all the signal you're interested in.", width=100).grid(column=1, row=5)
tk.Label(window, text="2. Both output entries will auto populate with locations when input file is selected, you can change these if you want.", width=100).grid(column=1, row=6)
tk.Label(window, text="3. Click the grey 'Browse DBC Folder' button to select the folder containing the DBCs you'd like to use to check for signals'.", width=100).grid(column=1, row=7)
tk.Label(window, text="4. Click the blue 'Check Signals' button to create the two output files.", width=100).grid(column=1, row=8)

tk.Label(window, text="NOTE: All file paths are absolute paths.", width=100).grid(column=1,row=10)
tk.Label(window, text="The black screen will tell you if the signal checking was a success or not.",width=100).grid(column=1, row=11)


txt1 = tk.Entry(window, width=70)
txt2 = tk.Entry(window, width=70)
txt3 = tk.Entry(window, width=70)
txt4 = tk.Entry(window, width=70)

txt1.grid(column=1, row=0, padx=2, pady=2)
txt2.grid(column=1, row=1, padx=2, pady=2)
txt3.grid(column=1, row=2, padx=2, pady=2)
txt4.grid(column=1, row=3, padx=2, pady=2)



def clicked():
    excelInputName = txt1.get()
    folderName = txt2.get()
    outputName = txt3.get()
    notFoundSignalName = txt4.get()

    excelFileName = excelInputName
    folderFileName = folderName
    outputFileName = outputName
    notFoundSignalFileName = notFoundSignalName

    try:
        print(outputFileName)
        print(notFoundSignalFileName)
        # Pulling data from excel
        excel_data = pd.read_excel(excelFileName, header=None)

        os.chdir(folderFileName)
        dbcFiles = []
        dbcNames = []
        numOfDbcs = 0
        for file in os.listdir():
            if file.endswith(".dbc"):
                fullFileName = folderFileName + "/" + file
                dbcFiles.append(fullFileName)
                dbcNames.append(file)
                numOfDbcs += 1

        outputData = {key: {} for key in excel_data[0]}
        count = 0
        for file in dbcFiles:
            data_base = cantools.database.load_file(file)
            count += 1
            for message in data_base.messages:
                for signal in message.signals:
                    for key in outputData:
                        similarityResults, newKeyValue = functions.similar_strings(key, signal.name)
                        if similarityResults:
                            outputData[key][dbcNames[count-1]] = newKeyValue
                            break
            for key in outputData:
                if len(outputData[key]) < count:
                    outputData[key][dbcNames[count-1]] = 'No'

        not_found_signals = []
        found_signals = []
        for keys1, internalDict in outputData.items():
            count = 0
            for unused_keys2, value in internalDict.items():
                if value == 'No':
                    count += 1
            if count == len(internalDict):
                not_found_signals.append(keys1)
            else:
                found_signals.append(keys1)

        # Creating excel file
        df = pd.DataFrame(outputData).T
        df.to_excel(outputFileName)
        df = pd.DataFrame(not_found_signals)
        df.to_excel(notFoundSignalFileName)
        print("Signals successfully checked!")

    except Exception as e:
        print(e)
        print("Could not check signals.")

    return

def open_inputName1():
    file = filedialog.askopenfile(mode='r', filetypes=[('Signal List', '*.XLSX')])
    if file:
        txt1.delete(0, tk.END)
        txt1.insert(0, file.name)
        outputName = file.name
        outputName = outputName[:-5]
        outputName = outputName + "_checkedSignals.xlsx"
        txt3.delete(0, tk.END)
        txt3.insert(0, outputName)
        noOutputName = file.name
        noOutputName = noOutputName[:-5]
        noOutputName = noOutputName + "_not_found_signals.xlsx"
        txt4.delete(0, tk.END)
        txt4.insert(0, noOutputName)

def open_inputName2():
    folder = filedialog.askdirectory()
    if folder:
        txt2.insert(0, folder)

def popup_window(popup_title):
    file = filedialog.askopenfile(mode='r', filetypes=[('DBC File', '*.DBC')], title=popup_title)
    print(file.name)
    data_base = cantools.database.load_file(file.name)
    return data_base

btn1 = tk.Button(window, text = "Check Signals", command = clicked, bg = "#0377fc", fg = "white")
btn2 = tk.Button(window, text = "Browse Signal File", command = open_inputName1)
btn3 = tk.Button(window, text = "Browse DBC Folder", command = open_inputName2)

btn1.grid(column=2, row=2)
btn2.grid(column=2, row=0)
btn3.grid(column=2, row=1)

window.mainloop()