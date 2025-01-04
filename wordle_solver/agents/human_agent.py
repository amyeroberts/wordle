"""
Agent which takes human input in the games
"""

from wordle_solver.agents.base_agent import Agent
from wordle_solver.specs import StepType


class HumanAgent(Agent):
    """
    Agent which takes in an input from a human for a wordle guess
    """

    def __init__(self, rng=None):
        super().__init__(rng)

    def update(self, timestep, action):
        pass

    def _validate_len(self, action, timestep):
        expected_len = len(timestep.state.answer)
        if len(action) != expected_len:
            raise ValueError(
                f"Expected answer of length {expected_len}, got {len(action)}"
            )

    def select_action(self, timestep):
        action = input("Guess: ").upper()
        self._validate_len(action, timestep=timestep)

        while action not in timestep.state.words:
            self._validate_len(action, timestep=timestep)
            action = input(f"{action} is not a valid word. Try again: ").upper()

        return action
