"""
Agent which takes human input in the games
"""

from wordle_solver.agents.base_agent import Agent
from wordle_solver.specs import StepType


def _is_right_len(guess, answer):
    return len(guess) == len(answer)


def _is_vocab_word(guess, words):
    return guess in words


class HumanAgent(Agent):
    """
    Agent which takes in an input from a human for a wordle guess
    """

    def __init__(self, rng=None):
        super().__init__(rng)

    def update(self, timestep, action):
        pass

    def _is_valid_action(self, action, timestep):
        return _is_right_len(
            guess=action, answer=timestep.state.answer
        ) & _is_vocab_word(guess=action, words=timestep.state.words)

    def select_action(self, timestep):
        action = input("Guess: ").upper()

        while not self._is_valid_action(action, timestep):
            if not _is_right_len(action, timestep.state.answer):
                action = input(
                    f"Wrong number of letters, got {len(action)} expected {len(timestep.state.answer)}: "
                ).upper()
            elif not _is_vocab_word(action, timestep.state.words):
                action = input(f"{action} is not a valid word. Try again: ").upper()

        return action
