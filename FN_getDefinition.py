# File: 'getDefinition.py'

# From a captured \def command it creates a dictionary containing its definition

import re
from strFun import str2num # (string)


def getDefinition(captured, fileTranscript):

    startingPoint = captured['idx']
    token = {'type': None, 'content': None, 'break': None}

    try:
        if captured['type'] == 'scene':


            lineIdx = startingPoint + 1
            text = []


            while lineIdx < len(fileTranscript):

                if '}' in fileTranscript[lineIdx]:
                    breakLine = lineIdx
                    break

                text.append(fileTranscript[lineIdx])
                lineIdx += 1


            token['type'] = 'scene'
            token['content'] = {'text': text}
            token['break'] = breakLine



        elif captured['type'] == 'actions':

            actionEntryPattern = re.compile(r'(?:<<)((?:\[)(.+)(?:\]))* (.+)(\\(scene|actions|reaction)\{(\w*)\})')
            lineIdx = startingPoint + 1
            text = []
            nextCommand = []
            isDone = []


            while lineIdx < len(fileTranscript):

                if ( '}' in fileTranscript[lineIdx]
                   and '<<' not in fileTranscript[lineIdx]):

                    breakLine = lineIdx
                    break

                elif (len(isDone) != len(text) != len(nextCommand)):
                    raise NameError('The two vectors "isDone" and "text" have different length.')

                actionEntry = actionEntryPattern.search(fileTranscript[lineIdx])


                if actionEntry.group(2) == r'\oneshot':
                    isDone.append(False)

                else:
                    isDone.append(None)

                text.append(actionEntry.group(3))
                nextCommand.append(actionEntry.group(4))
                lineIdx += 1


            token['type'] = 'actions'
            token['content'] = {'oneshot': isDone, 'text': text, 'next': nextCommand}
            token['break'] = breakLine





        elif captured['type'] == 'reaction':

            token['type'] = 'reaction'
            # timedReactionPattern = re.compile(r'(?:\+\+)((?:\[)(\d+)(?:\]))* (.+)')
            timedReactionPattern = re.compile(r'(?:\+\+)((?:\[)(\d+\.*\d*)(?:\]))* (.+)')


            try:
                generalTime = captured['opt']['pure']
            except NameError:
                generalTime = '1' # default time in case of failure

            generalTime = str2num(generalTime)
            specificTime = []


            lineIdx = startingPoint + 1 # one line AFTER the definition command
            text = []



            while lineIdx < len(fileTranscript):

                if '}' in fileTranscript[lineIdx]:
                    breakLine = lineIdx
                    break

                elif (len(specificTime) != len(text)):
                    raise NameError('The two vectors "isDone" and "text" have different length.')

                reactionEntry = timedReactionPattern.search(fileTranscript[lineIdx])    # IS IT DED HERE?

                try:
                    specCurrent = str2num(reactionEntry.group(2)) # integer of the specific time
                    specificTime.append(specCurrent)

                except AttributeError:
                    specificTime.append(None)


                try:
                    text.append(reactionEntry.group(3))
                except AttributeError:
                    text.append(fileTranscript[lineIdx]) # if the pattern is not found
                    # ATTENTION: this retains empty lines

                lineIdx += 1


            token['type'] = 'reaction'
            token['content'] = {'gen': generalTime, 'spec': specificTime, 'text': text}
            # when reading the general timing is applied only after the second item of the reaction text
            token['break'] = breakLine



        else:
            raise NameError('Could not identify the type of command or the command does not exist.')

        return token

    except AttributeError:

        raise NameError('Could not capure the definition of "' + captured['pure'] + ' on line ' + str(captured['idx']) + '".')


