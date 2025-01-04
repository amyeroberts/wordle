# Wordle Solver

Simple wordle solver that uses basic heuristics to guess the wordle word.

To run, select choose a script and run with the python command e.g. `python play_human.py`

Available scripts:
* `play_random.py`: plays wordle using an agent which randomly picks a word based on the remaining compatible words
* `play_human.py`: you play wordle, takes a terminal input from a user

You can control the behaviour through simple command line options:
* `--n-games`: the number of games to run, default 5
* `--seed-env:` the random seed used by the agent. If -1 then a random integer between 0-9999 is chosen. Default 1000
* `--seed-agent:` the random seed used by the enviroment. If -1 then a random integer between 0-9999 is chosen. Default 2000
* `--max-guesses`: the number of guesses to allow the agent to try, default 5
* `--word-length`: the length of words to guess, default 5
* `--show/--no-show`: whether to log the anwer to the terminal. Only available for `play_human.py`
