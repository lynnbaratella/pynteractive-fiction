#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File: "strFun.py"

Gathers useful string functions, also from "cryptFunctions.py"
"""

def inputError(type):
    print('ERROR: the input must be ' + type + '.')


# Asks the user to input a string
def promptString(message):

    userInput = input(message)

    while type(userInput) != str:
        inputError('string')
        userInput = input(message)

    return userInput

# outputs a boolean: whether the string represents a float or not
def isFloat(val):
    try:
        float(val)
        boolFloat = ('.' in val) # is there a . inside the number? So is it float?
        return boolFloat

    except ValueError:
        return False

def str2num(string):
    try:
        stringConvertedFloat = float(string)
        stringConvertedInt = int(stringConvertedFloat)

        if isFloat(string):
            return stringConvertedFloat
        else:
            return stringConvertedInt

    except ValueError:
        inputError('string representing an integer value')
    except TypeError:
        return None

# Converts a string into the integer number it represents
#   if float, truncates with warning

def str2int(string):
    try:
        stringConvertedFloat = float(string)
        stringConvertedInt = int(stringConvertedFloat)

        if isFloat(string):
            print('WARNING: your input may have been truncated to an integer value')

        return stringConvertedInt

    except ValueError:
        inputError('a string representing an integer value')
    except TypeError:
        return None

def find(string, stringList, *args): # returns a list of indices. you can specify the number you need

    if (args
        and type(args[0]) == int):

        howMany = args[0]
        getAll = False
    else:
        getAll = True

    lineIdx = 0
    indicesList = []
    nFound = 0

    while (lineIdx < len(stringList)
          and (getAll
               or nFound < howMany)):

        if string in stringList[lineIdx]:

            indicesList.append(lineIdx)
            nFound += 1
        lineIdx += 1
    return indicesList
