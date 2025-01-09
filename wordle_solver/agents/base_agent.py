"""
Class and utilities which define an agent which solves wordle
"""

import numpy as np


class Agent:
    def __init__(self, rng=None):
        self._rng = rng if rng is not None else np.random.RandomState(0)

    def select_action(self, state):
        raise NotImplementedError

    def update(self, state, action, reward):
        raise NotImplementedError
