# File: 'read.py'

# From the output of getDefinition.py it prints out the text of the game

from time import sleep

# defaultTime = 0.5 # doesn't change the default time for getDefinition

def read(token):

    print('\n')





    if token['command']['type'] == 'scene':

        for idx in range(0, len(token['content']['text'])):
            print(token['content']['text'][idx]) # time separation for printing scene paragraphs?





    elif token['command']['type'] == 'actions':

        # ONESHOT?


        if anyTrue(token['content']['oneshot']):
            # the numbers on the list of options change

            oneshot = token['content']['oneshot']
            text = token['content']['text']
            options = [[],[]]
            for idx in range(0, len(text)):
                if oneshot[idx] != True: # (False or None)
                    options[0].append(oneshot[idx])
                    options[1].append(text[idx])
            print()
        for idx in range(0, len(token['content']['text'])):

            print(str(idx+1) + '. ' + token['content']['text'][idx])
            # print only the text until the next command






    elif token['command']['type'] == 'reaction':

        for idx in range(0, len(token['content']['text'])):

            # the timing is applied only after the second item of the reaction text
            if idx != 0:
                try: # if spec time is present
                    sleep(token['content']['spec'][idx])

                except: # more specific
                    sleep(token['content']['gen'])

            print(token['content']['text'][idx])

            # AFTER PRINTING TIME MANAGEMENT
            try:
                if not (token['content']['spec'][idx+1]): # no specific time for the following item

                    try: # sleep again for the current  spec or gen time
                        sleep(token['content']['spec'][idx])

                    except TypeError:
                        sleep(token['content']['gen'])
            except IndexError: # last item of the list

                # sleep nevertheless

                try:
                        sleep(token['content']['spec'][idx])
                except TypeError:
                        sleep(token['content']['gen'])



def anyTrue(listName):


    for idx in range(0, len(listName)):
        if listName[idx] is True:
            return True
    return False