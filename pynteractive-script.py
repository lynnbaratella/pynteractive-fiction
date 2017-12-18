import re
import os.path

from time import sleep


from FN_read import read
from FN_getDefinition import getDefinition

from FN_strFun import str2int
from FN_strFun import find # returns list of indices; (string, stringList, varargin:howMany)


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


 # %% Functions


def transcribe(fileName):

    fileTranscript = []
    try:
        # SET FOLDER PATH
        path = os.path.expanduser('~/Downloads/pynteractive-fiction-master/') # change 1/2 HERE
        # path = '/Users/<username>/Downloads/pynteractive-fiction-master/' # or use this one
        if path[-1] != '/':
            path = path + '/'
           
        path = path + fileName

        # transcribe file into list
        with open(path, 'r') as myfile:

            fileTranscript = myfile.readlines()
            return fileTranscript

    except FileNotFoundError as e:
        raise Exception('The specified path is not correct.\n'
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
                    'opt': optionalField,
                    'idx': lineIdx}


        captured['isDef'] = captured['whole'] != captured['pure']

        return captured




def beginningScene(pattern, fileTranscript):

    lineIdx = 0

    while lineIdx < len(fileTranscript):

        captured = extractCommand(pattern, fileTranscript, lineIdx)

        if (captured# exists
          and captured['isDef']
          and captured['type'] == 'scene'):


            return  captured

        lineIdx += 1




def promptAction(message,maxNum):

    userInput = input(message)

    if ('exit' in userInput
        or 'quit' in userInput):
        endGame()

    userInput = str2int(userInput)

    while (type(userInput) != int
           or userInput < 1
           or userInput > maxNum):

        userInput = input(message)
        userInput = str2int(userInput)

    return userInput



def addToDefHistory(captured, definition, defHistory):

    #howManyTimes = 0
    defHistory.update({captured['pure']: definition})

    return defHistory



def gameStart():

    userInput = input('Ready to start? Press ENTER to begin or type "exit" to leave the game:\n')

    if userInput == 'exit':
        endGame()


    while (userInput != ''
           and userInput != ' '
           and userInput != '    '):

        userInput = input('Press ENTER to begin or type "exit" to leave the game:\n')
    sleep(0.5)
    print('the game is starting...')
    sleep(0.5)
    print('enjoy!')
    print('--------------------------------')
    sleep(1)


def endGame():
    raise KeyboardInterrupt('The game was interrupted by the user')


# %% Transcription

fileTranscript = transcribe('test_fiction.txt') # change 2/2 HERE

# ready to start?
gameStart()

# begin with first available _defined_ scene
captured = beginningScene(pattern, fileTranscript)


# read until break
definition = getDefinition(captured, fileTranscript)
read(definition)

# initializing def history
defHistory = {}
defHistory = addToDefHistory(captured, definition, defHistory)

# return breakline
breakLine = definition['break']


# %% game loop

lineIdx = breakLine
timeoutCounter = 0

while breakLine < len(fileTranscript):

    # extract the command from the current line
    captured = extractCommand(pattern, fileTranscript, breakLine)

    try:

        if captured['isDef']: # is it the definition of the command?

            definition = getDefinition(captured, fileTranscript) ###
            defHistory = addToDefHistory(captured, definition, defHistory)

            read(definition)

            if definition['type'] == 'actions':
                nChoices = len(definition['content']['next'])
                whichAction = promptAction('\n',nChoices)

                # converting to indexing
                whichAction -= 1

                # subtracting the negative index from original breakline
                breakLine = definition['break'] - (nChoices - whichAction)


            else:
                breakLine = definition['break']

                if '\ENDGAME' in fileTranscript[breakLine]:
                    raise Exception('Thank you for playing.')


        else: # it's the next event: look for its definition


            lineIdx  = find(('\\def'+captured['pure']), fileTranscript, 1) # loop through the list and check for string in line

            try:
                # use as breakline the first occurrence of the definition (in case of multiple instances)
                breakLine = lineIdx[0]


            except IndexError as e:
                raise Exception('Command definition not found').with_traceback(e.__traceback__)




    except TypeError as e:
        raise Exception('Error from the command on line ' + str(breakLine) + '.').with_traceback(e.__traceback__)


# %% NOTES:

"""
# todo:

* completely load the game at game start + accurate error reporting for command definitions
* make \oneshot actions actually work
* easier game setup (no need to define path?)

* remove the extra newlines/tabs: if isEmpty: don't add. Possible option (debugging might be harder)
* IF NO SUBSEQUENT COMMAND RESUME FROM LAST ACTION (warning message)



# game steps:
1. begin with first available _defined_ scene
2. read() text until closing bracket line
3. capture command on that same line
4. look for \def\command{}


"""
