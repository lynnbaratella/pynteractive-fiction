

from time import sleep


from FN_read import read
from FN_getDefinition import getDefinition

from FN_strFun import str2int
from FN_strFun import find # returns list of indices; (string, stringList, varargin:howMany)



 # %% Functions







def promptAction(message,maxNum):

    userInput = input(message)

    if userInput == 'exit':
        endGame()

    userInput = str2int(userInput)

    while (type(userInput) != int
           or userInput < 1
           or userInput > maxNum):

        userInput = input(message)
        userInput = str2int(userInput)

    return userInput




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



# %% Start game


loadGame(fileTranscript)

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

* transcription of multiple files (list of filenames as a single input)

report double begin_index (+ filename if they differ) in these cases:
* warning if same name in different trype of entry
* error if same command is repeated

# game steps:
1. begin with first available _defined_ scene
2. read() text until closing bracket line
3. capture command on that same line
4. look for \def\command{}


"""
