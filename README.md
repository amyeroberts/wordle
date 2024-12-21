# Wordle Solver

Simple wordle solver that uses basic heuristics to guess the wordle word.

To run: `python play.py`

You can control the behaviour through simple command line options:

* `--n-games`: the number of games to run, default 5
* `--seed-env:` the random seed used by the agent, default 1000
* `--seed-agent:` the random seed used by the enviroment, default 1000
* `--max-guesses`: the number of guesses to allow the agent to try, default 5
* `--word-length`: the length of words to guess, default 5
