"""
Wordle Environment
"""

from dataclasses import dataclass
from typing import List

import numpy as np
from wordle_solver.specs import StepType, Reward


@dataclass
class State:
    words: list
    answer: str
    n_guesses: int


@dataclass
class TimeStep:
    state: State
    reward: Reward
    step: StepType = StepType.START


class Environment:
    def __init__(self, words: List[str], max_guesses: int = 5, rng=None) -> None:
        self._rng = rng if rng is not None else np.random.RandomState(0)
        self.words = words
        self.answer = self._rng.choice(self.words)
        self.max_guesses = max_guesses
        self.n_guesses = 0

    def state(self) -> State:
        """
        Returns the current state of the environment
        """
        return State(
            words=self.words,
            answer=self.answer,
            n_guesses=self.n_guesses,
        )

    def step(self, action: str) -> TimeStep:
        """
        Based on the action, returns a new timestep with a new state,
        """
        self.n_guesses += 1

        if action == self.answer:
            return TimeStep(
                state=self.state(),
                step=StepType.END,
                reward=Reward.WIN,
            )

        # We've selected an invalid word or we've run out of guesses
        if self.n_guesses >= self.max_guesses or action not in self.words:
            return TimeStep(
                state=self.state(),
                step=StepType.END,
                reward=Reward.LOSE,
            )

        # Otherwise we can take another guess
        return TimeStep(
            state=self.state(),
            step=StepType.STEP,
            reward=Reward.DRAW,
        )

    def reset(self) -> TimeStep:
        """
        Returns a freshly initialised Environment and returns a new
        timestep for the start of a new play session.
        """
        # self.letters = Letters(word_length=self.letters.word_length)
        self.answer = self._rng.choice(self.words).upper()
        self.n_guesses = 0

        return TimeStep(
            state=self.state(),
            step=StepType.START,
            reward=Reward.DRAW,
        )
