# Pynteractive Fiction

## The syntax

A simple LaTeX-y syntax for writing short interactive fictions.
Three types of entry: 
* `\scene`: the main descriptions can be written here 
* `\actions`: a set of possibilities the player has to choose from 
* `\reaction`: what happens (mostly) after an action has been chosen. They can be timed (`++ ` symbol), either by specifying an optional parameter for the whole entry or for a single line only.

### DA RULES
- Every entry has to be preceded by `\def`
- every entry needs a name (first field) and a description (second mandatory field)
- mind the closing brace on newline
- after that closing brace in the entries `\scene` and `\reaction` you'll need to specify to the program where to look next (the next command, *without* specifying `\def`)
- in the case of `\actions` entry you'll need a `<< ` for every line of text; the next command can be specified right after every line of text
- with `\reaction` entries you can specify in squared brackets, right after the name, the time in seconds that every `++ ` line will wait before being displayed. As an alternative you can specify that number in squared brackets after the double plus symbol (`++[2] `) 
- One of the files has to contain `\BEGIN\<whichEntry>{<entryName>}`
- to end the game (you might want to) you can simply use `\ENDGAME` as the next command (yes, in Caps: you're screaming to the computer).
- see "How to make it work" for what concerns the script setup

### Example
A short working example of the content of the text file
```
\BEGIN\scene{somewhere}

\def\scene{somewhere}{
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
}\actions{actionsName}


\def\actions{actionsName}{
<< Do something \reaction{something}
<< Go to some place \scene{somePlace}
}

\def\reaction{something}[1]{
You do something.
++ Bad consequences
++ happening after 1 second as specified
++ or
++[3] even a different time.
} \actions{actionsName}

\def\scene{somePlace}{
You win. Happy feelings.
}\ENDGAME
```

## The script
* written on Python 3.6
* dictionary-based
* informative errors

### Setup
1. the game has to be written in one or more text files in the same folder as the script
2. in the file "pynteractive.py" specify the path to the folder (you can use the ~ shortcut)
3. in the same file, specify one or more file names
4. run the script, follow the instructions and enjoy the game

## Work In Progress
* **Even simpler setup**

## Limitations
This is my *first* proper Python project; let me save you some time. 

Look somewhere else if:
* you need to write long and complex storylines: it's hard to lose track of what happens with this syntax
* you're feeling lazy: impossibility to use placeholders (e.g. in order to write a single reaction where one word changes according to the chosen actions): you might need to manually write multiple similar entries


