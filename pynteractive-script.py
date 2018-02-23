
from time import sleep

from FN_read import narrate
from FN_strFun import str2int
from FN_loadGame import loadGame


# %% FILES SETUP

# you can either replace the user with ~ or use the full path
inputPath = '~/Dropbox/Python/#textAdventure/pynteractive-fiction/'

fileNameList = ['test_fiction.txt'] # if more than one: ['one.txt','two.txt']


 # %% Functions


def promptAction(message,maxNum):

    userInput = input(message)

    if userInput == 'exit':
        quitGame()

    userInput = str2int(userInput)

    # the non-int cases are handled by str2int()
    while (userInput < 1
           or userInput > maxNum):
        print('[Number out of range: try again]')
        userInput = input(message)
        userInput = str2int(userInput)

    return userInput




def gameStart():

    userInput = input('Ready to start? Press ENTER to begin or type "exit" to leave the game:\n')

    if userInput == 'exit':
        quitGame()


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


def quitGame():
    raise KeyboardInterrupt('The game was interrupted by the user')

def endScreen():
    sleep(5)
    print('Thank you for playing! \nIf you wish to play again you can run the script by pressing F5')

# %% Start game





[game, firstScene] = loadGame(fileNameList,inputPath)

# ready to start?
gameStart()

# begin with first available _defined_ scene
nextEntry = firstScene


while nextEntry != r'\ENDGAME':

    token = game[nextEntry]

    narrate(token)

    # check if the current token is an action
    if token['command']['type'] == 'actions':
        cardinal = token['content']['cardinal']

        nChoices = len([i for i in cardinal if i])
        whichAction = promptAction('\n>> ',nChoices)

        indexAction = cardinal.index(whichAction)
        if token['content']['oneshot'][indexAction] is False: # if oneshot action still to be done

            token['content']['oneshot'][indexAction] = True # markes it done
            cardinal[indexAction] = None # removes the corresponding number from the possible actions

            # update the numbers representing the actions
            idx = 0
            while idx < (len(cardinal)-(indexAction + 1)):
                cardinal[indexAction + idx + 1] = whichAction + idx
                idx = idx + 1


        nextEntry = token['content']['next'][indexAction] # go to the next command according to the chosen action
    else:
        nextEntry = token['metadata']['nextCommand'] # if it's not an action go directly to the next command


print('\n[THE END]\n[*credits*]')

# %% NOTES:

"""
# todo:

* easier game setup (no need to define path?)
* remove the extra newlines/tabs: if isEmpty: don't add. Possible option (debugging might be harder)
* IF NO SUBSEQUENT COMMAND RESUME FROM LAST ACTION (warning message)


report double begin_index (+ filename if they differ) in these cases:
* warning if same name in different trype of entry
* error if same command is repeated


"""
