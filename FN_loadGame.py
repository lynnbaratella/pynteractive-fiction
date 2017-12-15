# File: 'FN_loadGame.py'

import re
from FN_getDefinition import getDefinition

# from FN_strFun import str2int
from FN_strFun import find # returns list of indices; (string, stringList, varargin:howMany)


""" # LOADGAME

Look for definitions
extract command.
captured contains:
captured = {'whole': wholeCommand,
                    'pure': pureCommand,
                    'type': typeCommand,
                    'name': nameField,
                    'opt': optionalField,
                    'idx': lineIdx}

NOPE! REWRITE!

what the loadgame dictionary should contain is 

'pure command' (as a dictionary key)
    * command [pure, whole, type, optional argument] + FILE NAME 
    * definition [content] (see getDefinition)
    * idx: begin line + breakline (where most errors occurr)
    
    * next command. if actions (this one is None) look in the 'content' field

    additional field: 'metadata'
        * event counter
        # no need for action counter (change the isDone into True if oneshot (not None))
        * next command
        * next action command


overlapping stuff between extractCommand and getDefinition:
    * name
    * type


"""



def loadGame(fileTranscript):
    
        # look for the definitions
    defIdx = find(r'\def', fileTranscript)
        # init defhistory
    defHistory = {}
    errorList = []
    firstScene = '' 

    for idx in defIdx:

        try:
            captured = extractCommand(pattern, fileTranscript, idx)
            # breakLine = idx + 1
            definition = getDefinition(captured, fileTranscript)
            defHistory = addToDefHistory(captured, definition, defHistory)
        except:
            print(idx)
            errorList.append(idx)


    return defHistory, firstScene, errorList # improve errorList with location of the error in the definition





def extractCommand(pattern, fileTranscript, lineIdx): # given pattern, from single line
    line = fileTranscript[lineIdx]
    reOutput = pattern.search(line)

    if reOutput:

        wholeCommand = reOutput.group(0)
        pureCommand = reOutput.group(1)
        typeCommand = reOutput.group(2)
        nameField = reOutput.group(3)
        optionalField = {'whole': reOutput.group(4),
                    'pure': reOutput.group(5)}

        captured = {'whole': wholeCommand,
                    'pure': pureCommand,
                    'type': typeCommand,
                    'name': nameField,
                    'opt': optionalField,
                    'idx': lineIdx}


        captured['isDef'] = captured['whole'] != captured['pure']

        return captured


# %%  Command pattern definition

pattern = re.compile(r""" # raw string for regular expression

    (?: \\def)*                             # group 0: whole match


    (                                       # group 1: scene/actions/reaction command
    (?: \\(scene|actions|reaction) \{)      # group 2: which of the 3?
        (\w+)                               # group 3: name
    (?: \} )
    ((?:\[) (\w+) (?: \]))*                   # group 4?   counter-consequnce/timer (no brackets)
    )

      """, re.VERBOSE)



def addToDefHistory(captured, definition, defHistory):

    #howManyTimes = 0
    # dictionary containing pure commands pointing at the original definition dictionary
    defHistory.update({captured['pure']: definition}) # not considering the alternative scenes?

    return defHistory

