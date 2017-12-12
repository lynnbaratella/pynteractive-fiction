# File: 'read.py'

# From the output of getDefinition.py it prints out the text of the game

from time import sleep

# defaultTime = 0.5 # doesn't change the default time for getDefinition

def read(token):
    
    print('\n')
    
    
    if token['type'] == 'scene':

        for idx in range(0, len(token['content']['text'])):
            print(token['content']['text'][idx])
            

    elif token['type'] == 'actions':

        # ONESHOT:
        # when you come back to the action a new instance is created.
        # need to store the data and reaccess it later for making the oneshots work.
        # print('\n')
        for idx in range(0, len(token['content']['text'])):

            print(str(idx+1) + '. ' + token['content']['text'][idx])
            # print only the text until the next command






    elif token['type'] == 'reaction':

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
