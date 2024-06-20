# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 21:05:42 2023

@author: a423465
"""

def find_set_index(data, identifier):
    index = data.find(identifier)
    return index

def find_set(data, startIndex):
    in_brackets = 0
    current_substring = ""

    for i in range(startIndex,len(data)):
        if data[i] == "{":
            in_brackets += 1
        elif data[i] == "}" and in_brackets == 1:
            in_brackets -= 1
            return current_substring
        elif data[i] == "}":
            in_brackets -= 1
        elif in_brackets:
            current_substring += data[i]
    return -1

def extract_frames_section(data, startIndex):
    frames = {}
    internal_dictionary = {}
    internal_dictionary.fromkeys(["message_data", "signals"])
    current_message = ""
    current_data = ""
    temp = ""
    tempSignals = []
    tempBitStartPosition = []
    internal_data = {}
    internal_data.fromkeys(["signal","bit_start_position"])
    in_brackets = 0
    in_message_data = 0
    message_data = {}
    message_data.fromkeys(["identifier", "publisher", "length"])

    for i in range(startIndex, len(data)):
        if data[i] == "{" and in_brackets == 0:
            in_brackets += 1
        elif data[i] == "{" and in_brackets == 1:
            message_data["length"] = current_data
            internal_dictionary["message_data"] = message_data
            current_data = ""
            in_message_data = 0
            in_brackets += 1
            message_data = {}
            message_data.fromkeys(["identifier", "publisher", "length"])
        elif data[i] == "}" and in_brackets == 2:
            internal_dictionary["signals"] = internal_data
            frames[current_message] = internal_dictionary
            internal_dictionary = {}
            internal_dictionary.fromkeys(["message_data", "signals"])
            current_message = ""
            internal_data["signal"] = tempSignals
            internal_data["bit_start_position"] = tempBitStartPosition
            internal_data = {}
            internal_data.fromkeys(["signal","bit_start_position"])
            tempSignals = []
            tempBitStartPosition = []
            in_brackets -= 1
        elif data[i]=="}" and in_brackets == 1:
            in_brackets -= 1
            return frames

        elif data[i] == ":" and in_brackets == 1:
            current_message = current_data
            current_data = ""
        elif (data[i].isalnum() or data[i] == "," or data[i] == "_") and in_brackets == 1:
            if data[i] == "," and in_message_data == 0:
                message_data["identifier"] = current_data
                in_message_data += 1
                current_data = ""
            elif data[i] == "," and in_message_data == 1:
                message_data["publisher"] = current_data
                in_message_data += 1
                current_data = ""
            else:
                current_data += data[i]

        elif (data[i].isalnum() or data[i] == "," or data[i] == ";" or data[i] == "_") and in_brackets == 2:
            temp += data[i]
            if data[i] == ",":
                temp = temp.rstrip(temp[-1])
                tempSignals.append(temp)
                temp = ""
            elif data[i] == ";":
                temp = temp.rstrip(temp[-1])
                tempBitStartPosition.append(temp)
                temp = ""
    return -1

def extract_signals_section(data):
    names = []
    lengths = []
    secondNumber = []
    publisher = []
    subscribers = []
    current_data = ""
    is_signal_index = 0

    for i in range(0,len(data)):
        if (data[i].isalnum() or data[i] == "_"):
            current_data += data[i]
        elif data[i] == ":" and is_signal_index == 0:
            names.append(current_data)
            current_data = ""
            is_signal_index += 1
        elif data[i] == "," and is_signal_index == 1:
            lengths.append(current_data)
            current_data = ""
            is_signal_index += 1
        elif data[i] == "," and is_signal_index == 2:
            secondNumber.append(current_data)
            current_data = ""
            is_signal_index += 1
        elif data[i] == "," and is_signal_index == 3:
            publisher.append(current_data)
            current_data = ""
            is_signal_index += 1
        elif data[i] == "," and is_signal_index == 4:
            current_data += ","
        elif data[i] == ";":
            subscribers.append(current_data)
            current_data= ""
            is_signal_index = 0

    internal_data = {}
    for i in range(0,len(names)):
        internal_data_values = {}
        internal_data_values["length"] = lengths[i]
        internal_data_values["secondNumber"] = secondNumber[i]
        internal_data_values["publisher"] = publisher[i]
        internal_data_values["subscribers"] = subscribers[i]
        internal_data[names[i]] = internal_data_values
    return internal_data

def extract_signal_encoding_section(data, startIndex):
    signalEncodings = {}
    current_message = ""
    current_data = ""
    in_brackets = 0

    for i in range(startIndex, len(data)):
        if data[i] == "{" and in_brackets == 0:
            in_brackets += 1
        elif data[i] == "{" and in_brackets == 1:
            in_brackets += 1
        elif data[i] == "}" and in_brackets == 2:
            signalEncodings[current_message] = extract_values(current_data)
            current_message = ""
            current_data = ""
            in_brackets -= 1
        elif data[i] == "}" and in_brackets == 1:
            in_brackets -= 1
            return signalEncodings

        elif (data[i].isalnum() or data[i] == "_") and in_brackets == 1:
            current_message += data[i]
        elif in_brackets == 2:
            current_data += data[i]
    return -1

def extract_signal_representation_section(data, startIndex):
    mapping = {}
    current_data = ""
    key_data = ""
    value_data = ""
    in_brackets = False
    good_data = False
    for i in range(startIndex, len(data)):
        if data[i] == "{":
            in_brackets = True
        elif data[i] == "}":
            in_brackets = False
        elif data[i] == ":":
            value_data = current_data
            current_data = ""
        elif data[i] == ",":
            key_data = current_data
            mapping[key_data] = value_data
            current_data = ""
        elif data[i] == ";":
            key_data = current_data
            current_data = ""
            good_data =True
        elif data[i] == "\n" and good_data:
            mapping[key_data] = value_data
        elif (data[i].isalnum() or data[i] == "_") and in_brackets:
            current_data += data[i]

    return mapping

def extract_values(data):
    #figure out if it's physical or logical values you have to extract
    if data.find("logical_value") > -1:
        output = extract_logical_value(data)
    elif data.find("physical_value") > -1:
        output = extract_physical_value(data)
    else:
        return -1
    return output

def extract_physical_value(data):
    internalData = []
    information = ""
    for c in data:
        if c == "," or c == ";":
            internalData.append(information)
            information = ""
        elif c == " " or c == "\t" or c == "\n":
            continue
        else:
            information += c

    internalDataDict = {
        "value_type" : internalData[0],
        "min" : internalData[1],
        "max" : internalData[2],
        "scale" : internalData[3],
        "offset" : internalData[4],
        "unit" : internalData[5],
        }
    return internalDataDict

def extract_logical_value(data):
    # extract logical values into a dictionary
    internalData = []
    internalDataDict = {}
    information = ""
    for c in data:
        if c == ",":
            information = ""
        elif c == ";":
            internalData.append(information)
            information = ""
        elif c == " " or c == "\t" or c == "\n":
            continue
        else:
            information += c

    for i in range(0,len(internalData)):
        internalDataDict[i] = internalData[i]
    internalDataDict["value_type"] = "logical_value"
    return internalDataDict

def remove_comments(data):
    newData = ""
    previousC = ""
    skipData = False
    for c in data:
        if c == "/" and previousC == "/":
            skipData = True
        elif not skipData:
            newData += c
        elif skipData:
            if c == "\n":
                newData = newData.rstrip(newData[-1])
                newData += c
                skipData = False
            else:
                continue
        previousC = c
    return newData

def decimalToBinary(ip_val):
    binaryString = ""
    if ip_val >= 1:
        binaryString += decimalToBinary(ip_val // 2)
    binaryString += str(ip_val % 2)
    return binaryString

def convert_identifier(ID, CH):
    binary = ""
    tempID = ""
    binary += "1"
    binaryCH = decimalToBinary(CH)
    binaryCH = binaryCH[1:]
    if len(binaryCH) > 4:
        return -1
    elif len(binaryCH) < 4:
        binaryCH = binaryCH.zfill(4)
    binary += binaryCH[0]
    binary += binaryCH[1]
    for i in range(0,5):
        binary += "0"
    binaryID = decimalToBinary(int(ID))
    binaryID = binaryID[1:]
    if len(binaryID) > 6:
        return -1
    elif len(binaryID) < 6:
        binaryID = binaryID.zfill(6)

    binary += binaryID
    binary += binaryCH[2]
    binary += binaryCH[3]
    tempHex = hex(int(binary,2))
    cleanedHex = tempHex[2:]
    tempID += "9BFF"
    tempID += cleanedHex
    newID = int(tempID, 16)
    
    return newID

def write_messsages(file, message, messageDictionary, channel):
    message
    identifier = messageDictionary[message]["message_data"]["identifier"]
    newIdentifier = convert_identifier(identifier, channel-1)
    publisher = messageDictionary[message]["message_data"]["publisher"]
    length = messageDictionary[message]["message_data"]["length"]
    file.write("\nBO_ " + str(newIdentifier) + " " + message + ": " + length + " " + publisher + "\n")
    return file

def write_signals(file, signalName, signalsDictionary, encodingDictionary, message, framesDictionary, representationDictionary):
    try:
        trueSignalName = representationDictionary[signalName]
        mappedSignal = 1
    except:
        trueSignalName = signalName
        mappedSignal = 0
        
    index = framesDictionary[message]["signals"]["signal"].index(signalName)
    bit_start_position = framesDictionary[message]["signals"]["bit_start_position"][index]
    signal_length = signalsDictionary[signalName]["length"]
    if mappedSignal == 1 and encodingDictionary[trueSignalName]["value_type"] == "physical_value":
        scale = encodingDictionary[trueSignalName]["scale"]
        offset = encodingDictionary[trueSignalName]["offset"]
        min_value = str(float(encodingDictionary[trueSignalName]["min"]) + float(offset))
        max_value = str(float(scale) * float(encodingDictionary[trueSignalName]["max"]) + float(offset))
        unit = encodingDictionary[trueSignalName]["unit"]
        receiver = signalsDictionary[signalName]["subscribers"]
    elif mappedSignal == 1 and encodingDictionary[trueSignalName]["value_type"] == "logical_value":
        scale = "1"
        offset = "0"
        min_value = "0"
        max_value = "0"
        unit = "\"\""
        receiver = signalsDictionary[signalName]["subscribers"]
    elif mappedSignal == 0:
        scale = "1"
        offset = "0"
        min_value = "0"
        max_value = "0"
        unit = "\"\""
        receiver = signalsDictionary[signalName]["subscribers"]
    else:
        scale = "N/A"
        offset = "N/A"
        min_value = "N/A"
        max_value = "N/A"
        unit = "N/A"
        receiver = "N/A"
    file.write(" SG_ " + signalName + " : " + bit_start_position + "|" + signal_length + "@1+ (" + scale + "," + offset + ") [" + min_value + "|" + max_value + "] " + unit + " " + receiver + "\n")
    return file

def find_all_nodes(signalsDictionary):
    nodes = ""
    allNodes = []
    for message in signalsDictionary:
        allNodes.append(signalsDictionary[message]["publisher"])
    allNodes = list(set(allNodes)) 
    for i in range(0,len(allNodes)):
        nodes += allNodes[i]
        nodes += " "
    return nodes

def add_new_symbols():
    new_symbols_string = """
    CM_
    BA_DEF_
    BA_
    VAL_
    CAT_DEF_
    CAT_
    FILTER
    BA_DEF_DEF_
    EV_DATA_
    ENVVAR_DATA_
    SGTYPE_
    SGTYPE_VAL_
    BA_DEF_SGTYPE_
    BA_SGTYPE_
    SIG_TYPE_REF_
    VAL_TABLE_
    SIG_GROUP_
    SIG_VALTYPE_
    SIGTYPE_VALTYPE_
    BO_TX_BU_
    BA_DEF_REL_
    BA_REL_
    BA_DEF_DEF_REL_
    BU_SG_REL_
    BU_EV_REL_
    BU_BO_REL_
    """
    return new_symbols_string
