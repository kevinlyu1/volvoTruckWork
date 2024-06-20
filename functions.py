# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 21:05:42 2023

@author: a423465
"""
import cantools
import pandas as pd
import os


def diff_sigName(dbc1, dbc2, a):
    print("These two frames have signals that are unique to each one.")
    print("Frames:")
    print("dbc1: " + str(dbc1.get_message_by_frame_id(a).name) + ",\t\t\tdbc2: " + str(dbc2.get_message_by_frame_id(a).name))
    print("Signals:")
    sigList1 = []
    sigList2 = []
    for j in dbc1.get_message_by_frame_id(a).signals:
        sigList1.append(j.name)
    for j in dbc2.get_message_by_frame_id(a).signals:
        sigList2.append(j.name)
    print("dbc1:\t" + str(sigList1[0]) + "  \t\tdbc2:\t" + str(sigList2[0]))
    j=0
    for j in range(min(len(sigList1),len(sigList2))-1):
        print("\t" + str(sigList1[j+1]) + "\t\t\t" + str(sigList2[j+1]))
    if len(sigList1) < len(sigList2):
        for jj in range(j, max(len(sigList1),len(sigList2))-1):
            print("\t\t\t\t\t\t" + str(sigList2[jj+1]))
    else: 
        for jj in range(j, max(len(sigList1),len(sigList2))-1):
            print("\t" + str(sigList1[jj+1]))
    print("Which one should be kept in the merged file? (Answer 1 or 2 for corresponding dbc)")
    ans = 0
    while ans != "1" or ans != "2":
        ans = str(input())
        if ans == "1":
            return 1
        elif ans == "2":
            return 2
        else:
            print("Faulty input!")
            
def clean_file_names(fileName1, fileName2):
    newName = ""
    tempName = ""
    for c in reversed(fileName2):
        if(c=="/"):
            break
        tempName += c
    for i in range(len(tempName)):
        newName = tempName[::-1]
    fileName1 = fileName1.replace('.dbc', '')
    newName = fileName1 + '-' + newName
    
    return newName
            
def main(file1, file2, file3):
    os.chdir(os.path.dirname(os.path.abspath(__file__))) # Set working directory to same as this file

    dbc1 = cantools.database.load_file(file1)
    dbc2 = cantools.database.load_file(file2)

    # Save frames to dataframes:
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    for i in range(int(len(dbc1.messages))):
        df1 = df1._append({"Message": dbc1.messages[i].name, "ID": dbc1.messages[i].frame_id}, ignore_index=True)
    for i in range(int(len(dbc2.messages))):
        df2 = df2._append({"Message": dbc2.messages[i].name, "ID": dbc2.messages[i].frame_id}, ignore_index=True)

    #print(df1)
    #print(df2)

    # Collect all frames that are common or uncommon between dbc's:
    commonFrames_1 = []
    uncommonFrames_1 = []
    commonFrames_2 = []
    uncommonFrames_2 = []
    for i in range(len(df1["ID"])):
        if df1.iloc[i]["ID"] in list(df2["ID"]):
            commonFrames_1.append(int(df1.iloc[i]["ID"]))
        else:
            uncommonFrames_1.append(int(df1.iloc[i]["ID"]))
    for i in range(len(df2["ID"])):
        if df2.iloc[i]["ID"] in list(df1["ID"]):
            commonFrames_2.append(int(df2.iloc[i]["ID"]))
        else:
            uncommonFrames_2.append(int(df2.iloc[i]["ID"]))

    # Check that both common lists are equal:
    commonFrames_1.sort()
    commonFrames_2.sort()
    for i in commonFrames_1:
        if i not in commonFrames_2:
            print("COMMON FRAMES DOES NOT MATCH!!!")
    commonFrames = commonFrames_1
    #print("CommonFrames")
    #print(commonFrames)

    uncommonFrames_1.sort()
    uncommonFrames_2.sort()
    print("uncommonFrames_1: length(" + str(len(uncommonFrames_1)) + ")")
    print(uncommonFrames_1)
    print("uncommonFrames_2: length(" + str(len(uncommonFrames_2)) + ")")
    print(uncommonFrames_2)

    # Separate the common frames with identical signals:
    identical = []
    difference = []
    sameNSignals = []
    diff1 = []
    difference_toKeep1 = []
    difference_toKeep2 = []
    for i in commonFrames:
        #print(i)
        #print(str(len(dbc1.get_message_by_frame_id(i).signals)) + "    " + str(len(dbc2.get_message_by_frame_id(i).signals)))
        if len(dbc1.get_message_by_frame_id(i).signals) == len(dbc2.get_message_by_frame_id(i).signals):
            sameNSignals.append(i)
            counter = 0
            for j in range(len(dbc1.get_message_by_frame_id(i).signals)):
                for k in range(len(dbc2.get_message_by_frame_id(i).signals)):
                    if dbc1.get_message_by_frame_id(i).signals[j].name == dbc2.get_message_by_frame_id(i).signals[k].name:
                        counter += 1
                    #else:
                        #print("dbc1: " + dbc1.get_message_by_frame_id(i).signals[j].name)
            if counter == len(dbc1.get_message_by_frame_id(i).signals):
                identical.append(i)
            else:
                ret = diff_sigName(dbc1, dbc2, i)
                if ret == 1:
                    difference_toKeep1.append(i)
                elif ret == 2:
                    difference_toKeep2.append(i)
                else:
                    diff1.append(i)
        else:
            if len(dbc1.get_message_by_frame_id(i).signals) < len(dbc2.get_message_by_frame_id(i).signals):
                sigList = []
                for j in dbc2.get_message_by_frame_id(i).signals:
                    sigList.append(j.name)
                counter = 0
                for j in dbc1.get_message_by_frame_id(i).signals:
                    if j.name in sigList:
                        counter += 1
                if counter == len(dbc1.get_message_by_frame_id(i).signals):
                    difference_toKeep2.append(i)
                else:
                    #difference_toKeep2.append(i) # if you just want to keep the frame with most signals uncomment this line and comment the rest of the else block
                    ret = diff_sigName(dbc1, dbc2, i)
                    if ret == 1:
                        difference_toKeep1.append(i)
                    elif ret == 2:
                        difference_toKeep2.append(i)
                    else:
                        difference.append(i)

            else:
                sigList = []
                for j in dbc1.get_message_by_frame_id(i).signals:
                    sigList.append(j.name)
                counter = 0
                for j in dbc2.get_message_by_frame_id(i).signals:
                    if j.name in sigList:
                        counter += 1
                if counter == len(dbc2.get_message_by_frame_id(i).signals):
                    difference_toKeep1.append(i)
                else:
                    #difference_toKeep1.append(i) # if you just want to keep the frame with most signals uncomment this line and comment the rest of the else block
                    ret = diff_sigName(dbc1, dbc2, i)
                    if ret == 1:
                        difference_toKeep1.append(i)
                    elif ret == 2:
                        difference_toKeep2.append(i)
                    else:
                        difference.append(i)
            
    print("If the following two lists are empty things are looking good:")
    print(difference)
    print(diff1)

    # look at the differing frames and decide which to keep:
    for i in difference:
        print(str(dbc1.get_message_by_frame_id(i).name))
    print()
    for i in diff1:
        print(str(dbc1.get_message_by_frame_id(i).name))


    #To keep: identical, difference_toKeep1, difference_toKeep2, uncommonFrames_1 & uncommonFrames_2
    dbc3 = dbc1
    removedList = []
    i = len(dbc3.messages) - 1
    while i >= 0: # keep indentical and uncommonFrames_1
        if int(dbc3.messages[i].frame_id) not in identical and int(dbc3.messages[i].frame_id) not in uncommonFrames_1:
            removedList.append(dbc3.messages[i].frame_id)
            dbc3.messages.remove(dbc3.messages[i])
        i -= 1

    for i in difference_toKeep1:
        dbc3.messages.append(dbc1.get_message_by_frame_id(i))
        if i in removedList:
            removedList.remove(i)
    for i in difference_toKeep2:
        dbc3.messages.append(dbc2.get_message_by_frame_id(i))
        if i in removedList:
            removedList.remove(i)
    for i in uncommonFrames_2:
        dbc3.messages.append(dbc2.get_message_by_frame_id(i))
        if i in removedList:
            removedList.remove(i)

    cantools.database.dump_file(dbc3, file3)
    print()
    print("Frames that have been removed from the merge")
    print(removedList)

    # Trouble shooting tips #
    # 1. If you cant open the dbc file after merge, try to switch the order of the input dbc files.
    #    Sometimes the BA_DEF_.. stuff is missing and its brobably because we base dbc3 on the file that doesn't have it.

    return
