# File: 'FN_loadGame.py'

import os.path
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
    * command [pure, whole, type, optional argument]
    * definition [content] (see getDefinition)
    * idx: begin line + breakline (where most errors occurr) + FILE NAME


    additional field: 'metadata'
        * event counter
        # no need for action counter (change the isDone into True if oneshot (not None))
        * next command
        * next action command


overlapping stuff between extractCommand and getDefinition:
    * name
    * type


"""



def loadGame(fileNameList):

    game = {}
    entry = {'command': None, 'content': None, 'indices': None, 'metadata': None}
    entry['metadata'] = {'counter': 0, 'nextCommand': None} # nextActionCmd parallel list of the actions text

    firstScene = None

    if type(fileNameList) == str:
        fileNameList = [fileNameList]

    for fileIdx in range(0, len(fileNameList)):

        fileName = fileNameList[fileIdx]
        fileTranscript = transcribe(fileName)


        # look for the definitions
        defIndices = find(r'\def', fileTranscript)
        firstScene = beginningScene


        for defIdx in defIndices:

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

                    elif captured['type'] != 'actions':
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

    if not firstScene:
        raise Exception('Missing \BEGIN\scene{<scene_name>} from any of the files.')

    return game, firstScene # improve errorList with location of the error in the definition


def transcribe(fileName):

    fileTranscript = []
    try:

        path = os.path.expanduser('~/Dropbox/Python/#textAdventure/pynteractive-fiction/') # change 1/2 HERE
        path = path + fileName

        # transcribe file into list
        with open(path, 'r') as myfile:

            fileTranscript = myfile.readlines()
            return fileTranscript

    except FileNotFoundError as e:
        raise Exception('The specified path is not correct.\n'
                        + path + '\n\n'
                        'Check out:\n'
                        '- the folder path in the definition of the funtion '
                        'transcribe();\n'
                        '- the file name on function call.').with_traceback(e.__traceback__)






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
                    'opt': optionalField}

        return captured


def beginningScene(pattern, fileTranscript): # useless now: the writer must define the startin scene

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
    ((?:\[) (\w+) (?: \]))*                   # group 4?   counter-consequnce/timer (no brackets)
    )

      """, re.VERBOSE)




