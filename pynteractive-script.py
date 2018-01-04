

from time import sleep


from FN_read import read
from FN_getDefinition import getDefinition

from FN_strFun import str2int
from FN_strFun import find # returns list of indices; (string, stringList, varargin:howMany)

from FN_loadGame import loadGame

# %% Files

fileNameList = ['test_fiction.txt'] # HERE


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


[game, firstScene] = loadGame(fileNameList)

# ready to start?
gameStart()

# begin with first available _defined_ scene
currentEntry = firstScene


while True:
    token = game[currentEntry]
    read(token)





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
