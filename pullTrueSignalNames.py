# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:57:40 2024

@author: a423465
"""

import tkinter as tk
from tkinter import filedialog, Toplevel, simpledialog
import pandas as pd
import cantools
import sys
import numpy as np

window = tk.Tk()

window.geometry("800x300")
window.title("Pull True Signal Names")
window.configure(bg = "#787c8a")

tk.Label(window, text="Input Excel file:", width=25).grid(column=0, row=0)
# tk.Label(window, text="Input DBC file:", width=25).grid(column=0, row=1)
tk.Label(window, text="Output file:", width=25).grid(column=0, row=2)
tk.Label(window, text="1. Click the grey 'Browse' button to find itf file.", width=70).grid(column=1, row=3)
tk.Label(window, text="2. Input and Output entries will auto populate with locations when input file is selected.", width=70).grid(column=1, row=4)
tk.Label(window, text="3. Click 'Extract'.", width=70).grid(column=1, row=5)

txt1 = tk.Entry(window, width=70)
# txt2 = tk.Entry(window, width=70)
txt3 = tk.Entry(window, width=70)
# txt4 = tk.Entry(pick_dbc_window, width=70)

txt1.grid(column=1, row=0, padx=2, pady=2)
# txt2.grid(column=1, row=1, padx=2, pady=2)
txt3.grid(column=1, row=2, padx=2, pady=2)



def clicked():
    excelInputName = txt1.get()
    # dbcInputName = txt2.get()
    outputName = txt3.get()

    excelFileName = excelInputName
    # dbcFileName = dbcInputName
    outputFileName = outputName
    try:
        print(excelFileName)
        print(outputFileName)
        # Pulling data from excel
        excel_data = pd.read_excel(excelFileName, header=None)
        # print(excel_data)
        # print(excel_data[0])
        # print(excel_data[1])
        print('-----------------')
        can_networks = set(excel_data[0])
        dbcs = dict.fromkeys(can_networks)
        i = 0
        for network in can_networks:
            print(network)
            data_base = popup_window('Pick DBC for ' + network)
            dbcs[network] = data_base
            i += 1

        w = 2
        h = int(excel_data.size/2)
        newDataSet = [[0 for i in range(w)] for j in range(h)]
        for i in range(0, h):
            newDataSet[i][0] = excel_data.values[i][1]
            newDataSet[i][1] = excel_data.values[i][1]
            current_dbc = excel_data.values[i][0]
            skip_flag = 0
            for message in dbcs[current_dbc].messages:
                for signal in message.signals:
                    if newDataSet[i][0] in signal.name:
                        newDataSet[i][1] = signal.name
                        skip_flag = 1
                        break
                if skip_flag == 1:
                    break

        # Creating excel file
        df = pd.DataFrame(newDataSet)
        df.to_excel(excel_writer = outputFileName)
        print("Signals extracted")

    except:
        print("File could not be converted.")

    return

def open_inputName1():
    file = filedialog.askopenfile(mode='r', filetypes=[('Excel File', '*.XLSX')])
    if file:
        txt1.delete(0, tk.END)
        txt1.insert(0, file.name)
        outputName = file.name
        outputName = outputName[:-5]
        outputName = outputName + "_true_signal_names.xlsx"
        txt3.delete(0, tk.END)
        txt3.insert(0, outputName)

# def open_inputName2():
#     file = filedialog.askopenfile(mode='r', filetypes=[('DBC File', '*.DBC')])
#     if file:
#         txt2.delete(0, tk.END)
#         txt2.insert(0, file.name)

def popup_window(popup_title):
    file = filedialog.askopenfile(mode='r', filetypes=[('DBC File', '*.DBC')], title=popup_title)
    print(file.name)
    data_base = cantools.database.load_file(file.name)
    return data_base



#     return

# def get_dbc():
#     file = filedialog.askopenfile(mode='r', filetypes=[('DBC File', '*.DBC')])
#     if file:
#         txt4.delete(0, tk.END)
#         txt4.insert(0, file.name)

btn1 = tk.Button(window, text = "Extract", command = clicked, bg = "#0377fc", fg = "white")
btn2 = tk.Button(window, text = "Browse Excel", command = open_inputName1)
# btn3 = tk.Button(window, text = "Browse DBC", command = open_inputName2)
# btn4 = tk.Button(pick_dbc_window, text = "Submit DBC", command = get_dbc, bg = "#0377fc", fg = "white")

btn1.grid(column=2, row=2)
btn2.grid(column=2, row=0)
# btn3.grid(column=2, row=1)

window.mainloop()