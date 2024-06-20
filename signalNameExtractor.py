# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 14:10:11 2024

@author: a423465
"""

import cantools
import tkinter as tk
from tkinter import filedialog
import pandas as pd


window = tk.Tk()

window.geometry("800x300")
window.title("Extract Signal Names")
window.configure(bg = "#787c8a")

tk.Label(window, text="DBC file:", width=25).grid(column=0, row=0)
tk.Label(window, text="Output file:", width=25).grid(column=0, row=2)

txt1 = tk.Entry(window, width=70)
txt3 = tk.Entry(window, width=70)

txt1.grid(column=1, row=0, padx=2, pady=2)
txt3.grid(column=1, row=2, padx=2, pady=2)


def clicked():
    dbcInputName = txt1.get()
    outputName = txt3.get()

    dbcFileName = dbcInputName
    outputFileName = outputName
    extractSignals=1
    print(outputFileName)
    try:
        all_data = []
        all_sheet_names = []
        while(extractSignals):
            print(dbcFileName)
            # Pulling data from excel
            dbc_data = cantools.database.load_file(dbcFileName)
            allSignals = []
            for message in dbc_data.messages:
                for signal in message.signals:
                    allSignals.append(signal.name)
            # Creating excel file
            df = pd.DataFrame(allSignals)
            all_data.append(df)

            dbcFileName = dbcFileName[:-4]
            file_name = ''
            counter = 0
            for i in reversed(dbcFileName):
                counter += 1
                if i =='/':
                    break
                file_name = i + file_name
            file_name = file_name[0:30]
            all_sheet_names.append(file_name)

            results = popup_window('Do you want to add a dbc?')
            extractSignals = results[0]
            dbcFileName = results[1]

        writer = pd.ExcelWriter(outputFileName)

        for i in range(len(all_sheet_names)):
            print(all_sheet_names[i])
            df = all_data[i]
            df.to_excel(writer, sheet_name=all_sheet_names[i])

        writer.close()
        print("Signals extracted")

    except Exception as error:
        print("File could not be converted.", error)

    return

def open_inputName1():
    file = filedialog.askopenfile(mode='r', filetypes=[('DBC File', '*.DBC')])
    if file:
        txt1.delete(0, tk.END)
        txt1.insert(0, file.name)
        outputName = file.name
        outputName = outputName[:-5]
        outputName = outputName + "_true_signal_names.xlsx"
        txt3.delete(0, tk.END)
        txt3.insert(0, outputName)

def popup_window(popup_title):
    file = filedialog.askopenfile(mode='r', filetypes=[('DBC File', '*.DBC')], title=popup_title)
    if file is None:
        data_base = []
        continue_flag = 0
    else:
        data_base = file.name
        continue_flag = 1
    return continue_flag, data_base


btn1 = tk.Button(window, text = "Extract", command = clicked, bg = "#0377fc", fg = "white")
btn2 = tk.Button(window, text = "Browse Excel", command = open_inputName1)

btn1.grid(column=2, row=2)
btn2.grid(column=2, row=0)

window.mainloop()