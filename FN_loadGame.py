# File: 'FN_loadGame.py'

import os.path
import re
from FN_getDefinition import getDefinition

# from FN_strFun import str2int
from FN_strFun import find # returns list of indices; (string, stringList, varargin:howMany)


"""
STRUCTURE OF THE TOKENS


- command
    - whole
    - pure
    - type
    - name
    - opt

- content

    [ACTIONS ONLY]
    - [cardinal]
    - [next]
    - [oneshot]

    {REACTIONS ONLY}
    - {gen}
    - {spec}

    - text

- indices
    - begin
    - end
    - fileName

- metadata
    - counter
    - nextCommand

"""



def loadGame(fileNameList,inputPath):
    
    # initialising variables to be returned
    game = {}
    firstScene = None
    
   # obtaining full path to the files
    
    if type(fileNameList) == str:
            fileNameList = [fileNameList]
            
    
    for fileName in fileNameList:

        
        if '~' in inputPath:
            inputPath = os.path.expanduser(inputPath)
            # for inputPath refer to SETUP at the top of the main file
        
        filePath = inputPath + fileName
        
        fileTranscript = transcribe(filePath)


        # look for the definitions
        defIndices = find(r'\def', fileTranscript)

        if not firstScene: # stops looking after the first \BEGIN instance
            firstScene = beginningScene(pattern, fileTranscript)


        for defIdx in defIndices:

            entry = {'command': None, 'content': None, 'indices': None, 'metadata': None}
            entry['metadata'] = {'counter': 0, 'nextCommand': None} # nextActionCmd parallel list of the actions text

            try:


                captured = extractCommand(pattern, fileTranscript, defIdx)
                # breakLine = idx + 1
                definition = getDefinition(defIdx, captured, fileTranscript)




                entry['command'] = captured
                entry['content'] = definition['content']

                entry['indices'] = {'begin': defIdx, 'end': definition['break'], 'fileName': fileName}


#         saving the next command

                try:
                    if r'\ENDGAME' in fileTranscript[definition['break']]:

                        entry['metadata']['nextCommand'] = r'\ENDGAME' # endgame can be in this position OR in the next action command

                    elif captured['type'] != 'actions': # saving new command after "}", absent in actions
                        newCommand = extractCommand(pattern, fileTranscript, definition['break'])
                        entry['metadata']['nextCommand'] = newCommand['pure']

                except TypeError as e:
                    raise Exception('Cannot recognize command on line ' + lineNum(definition['break'])).with_traceback(e.__traceback__)




                key = entry['command']['pure']

                if key not in game:
                    game[key] = entry
                else:
                    doubleIdx = [game[key]['indices']['begin'], defIdx]
                    raise Exception('Double entry on lines ' + lineNum(doubleIdx[0]) + 'and ' + lineNum(doubleIdx[1]))


            except:
                print('Error from the definition on line: ' + lineNum(defIdx))
                raise

                #errorList.append(defIdx)"""

    # after looping through all the files
    if not firstScene:
        raise Exception('Missing \BEGIN\scene{<scene_name>} from any of the files.')

    return game, firstScene # improve errorList with location of the error in the definition


def transcribe(filePath):

    fileTranscript = []
    try:

        # transcribe file into list
        with open(filePath, 'r') as myfile:

            fileTranscript = myfile.readlines()
            return fileTranscript

    except FileNotFoundError as e:
        raise Exception('The specified file appears to be non existent.\n'
                        + filePath + '\n\n'
                        'Check out in the SETUP section of the main file:\n'
                        '- the folder path\n'
                        '- the specified file name(s).').with_traceback(e.__traceback__)






def extractCommand(pattern, fileTranscript, lineIdx): # given pattern, from single line
    line = fileTranscript[lineIdx]
    reOutput = pattern.search(line)

    if reOutput:

        wholeCommand = reOutput.group(0)
        typeCommand = reOutput.group(2)
        nameField = reOutput.group(3)

        if (typeCommand == 'reaction'
            and reOutput.group(4)): # the [1] could be retained in the pure command
            opt = reOutput.group(4)
            notPureCommand = reOutput.group(1)
            pureCommand = notPureCommand.replace(opt,'')
        else:
            pureCommand = reOutput.group(1) # if scene or action


        optionalField = {'whole': reOutput.group(4),
                    'pure': reOutput.group(5)}

        captured = {'whole': wholeCommand,
                    'pure': pureCommand,
                    'type': typeCommand,
                    'name': nameField,
                    'opt': optionalField}

        return captured


def beginningScene(pattern, fileTranscript):

    beginIdx = find(r'\BEGIN', fileTranscript)

    try:
        captured = extractCommand(pattern, fileTranscript, beginIdx[0])
        if captured['type'] == 'scene':
            firstScene = captured['pure']
            return  firstScene

    except:
        pass


def lineNum(idx):
    line = str(idx + 1)
    return line
# %%  Command pattern definition

pattern = re.compile(r""" # raw string for regular expression

    (?: \\def)*                             # group 0: whole match


    (                                       # group 1: scene/actions/reaction command
    (?: \\(scene|actions|reaction) \{)      # group 2: which of the 3?
        (\w+)                               # group 3: name
    (?: \} )
    ((?:\[) (.+) (?: \]))*                   # group 4?   counter-consequnce/timer (no brackets)
    )

      """, re.VERBOSE)



