# Pynteractive Fiction

## The syntax

A simple LaTeX-y syntax for writing short interactive fictions.

Three types of entry: 
* `\scene`: the main descriptions can be written here 
* `\actions`: a set of possibilities the player has to choose from 
* `\reaction`: what happens (mostly) after an action has been chosen. They can be timed (`++ ` symbol), either by specifying an optional parameter for the whole entry or for a single line only.

### example
A short working example of the content of the text file
```
\def\scene{whereItBegins}{
This is where it begins.
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

### da rules
- Every entry has to be preceded by `\def`
- every entry needs a name (first field) and a description (second mandatory field)
- mind the closing brace on newline
- after that closing brace in the entries `\scene` and `\reaction` you'll need to specify to the program where to look next (the next command, *without* specifying `\def`)
- in the case of `\actions` entry you'll need a `<< ` for every line of text; the next command can be specified right after every line of text
- with `\reaction` entries you can specify in squared brackets, right after the name, the time in seconds that every `++ ` line will wait before being displayed. As an alternative you can specify that number in squared brackets after the double plus symbol (`++[2] `) 
- to end the game (you might want to) you can simply use `\ENDGAME` as the next command (yes, in Caps: you're screaming to the computer).
- see "How to make it work" for what concerns the script setup

## The script
* written on Python 3.6
* dictionary-based
* informative errors

### setup
1. the game has to be written in a text file in the same folder as the script
2. in the file "pynteractive.py", where the function `transcribe()` is called change the file name
3. in the same file, where the function `transcribe()` is defined adjust the path of the folder containing the script 
4. if you're having trouble with the two previous operations just use ctrl+F or cmd+F and look for the two instances of "here".
5. run the script, follow the instructions and enjoy the game

### how it works
Main game steps:
1. begin with first available _defined_ scene
2. `read()` text until closing bracket line
3. capture command on that same line
4. look for `\def\<command>{}`
5. start over with #2

## Work In Progress
1. **Loading the whole game in advance:** Currently the entries are loaded during the game, something that might lead to errors while playing if entries are missing or the syntax is incorrect. I'm working in order to load the whole game beforehand, so the in-game behavior will be completely predictable.
2. **Oneshot actions**: `<<[\oneshot] you do something` makes the action disappear when you come back to the same action menu.
3. **Simplified setup**

## Limitations
This is my *first* proper Python project; let me save you some time. 

Look somewhere else if:
* you need to write long and complex storylines: with this syntax errors are easy to miss (WIP #1 might partially solve the problem)
* you're feeling lazy: impossibility to use placeholders (e.g. in order to write a single reaction where one word changes according to the chosen actions): you might need to manually write multiple similar entries


