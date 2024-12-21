"""
Solver which starts with a random first guess, then uses a simple heuristic to select the subsequent guesses
"""

import string
from collections import Counter

import numpy as np

from wordle_solver.agents.base_agent import Agent
from wordle_solver.specs import StepType
from wordle_solver.utils import letter2index, index2letter


# Helper class which contains values of letters for immediate feedback and some useful
# functionality
class Letters:
    def __init__(self, word_length: int = 5):
        self.word_length = word_length
        self.values = np.zeros((26, word_length, 3))
        self.guessed = set()
        self.unguessed = set(string.ascii_uppercase)

    def update(self, guess, answer):
        """
        Updates flags based on guess

        0 - correct position
        1 - wrong position
        2 - not in word
        """
        answer_counts = Counter(answer)

        # As a first pass, we find and mark the letters in the correct positions
        for pos, (letter, target) in enumerate(zip(guess, answer)):
            if letter not in self.guessed:
                self.guessed.add(letter)
                self.unguessed.remove(letter)

            if letter == target:
                i = letter2index(letter)
                self.values[i, pos, 0] = 1.0  # Definitely here
                self.values[i, :, 2] = 0.0  # Definitely in the word
                answer_counts[letter] -= 1  # Use up one instance of the letter

        # Handle correct letters in wrong positions and letters not in words
        for pos, letter in enumerate(guess):
            # Already handled this case
            if letter == answer[pos]:
                continue

            i = letter2index(letter)
            if letter in answer_counts and answer_counts[letter] > 0:
                self.values[i, pos, 0] = 0.0  # Not here
                self.values[i, pos, 1] = 1.0  # In the word but not here
                self.values[i, :, 2] = 0.0  # It's definitely in a position
                answer_counts[letter] -= 1
            elif letter not in answer_counts:
                self.values[i, :, 0] = 0.0  # Not in the word at all
                self.values[i, :, 1] = 0.0  # Not in the word at all
                self.values[i, :, 2] = 1.0  # Definitely not in the word

    @property
    def known_letters(self):
        "Letters which we know appear in the word"
        known_indices = self.values[:, :, 1].sum(1) + self.values[:, :, 0].sum(1) >= 1
        known_letters = [
            index2letter(i)
            for i, letter2index in enumerate(known_indices)
            if letter2index
        ]
        return known_letters

    @property
    def known_not_letters(self):
        "Letters which we know don't appear in the word"
        known_not_indices = self.values[:, :, 2].sum(1) >= 1
        known_not_letters = [
            index2letter(i)
            for i, letter2index in enumerate(known_not_indices)
            if letter2index
        ]
        return known_not_letters

    @property
    def known_letters_and_positions(self):
        "Returns a list with 5 elements with either an empty string or letter in its correct position"
        known_letters = [""] * self.word_length
        known_letters_indices = np.argwhere(self.values[:, :, 0] == 1)

        for i, position in known_letters_indices:
            letter = index2letter(i)
            known_letters[position] = letter
        return known_letters


def has_known_letters(word, known_letters):
    "False if the word doesn't contain a known letter"
    return all(letter in word for letter in known_letters)


def has_known_letters_and_positions(word, known_letters_and_positions):
    "False if a word doesn't contain a known letter in its position"
    return all(
        letter == word[i]
        for i, letter in enumerate(known_letters_and_positions)
        if letter != ""
    )


def has_known_not_letters(word, known_not_letters):
    "True if the word contains a letter known to not be in the answer"
    return any(letter in word for letter in known_not_letters)


def is_possible_word(word, letters):
    return (
        has_known_letters(word, letters.known_letters)
        and has_known_letters_and_positions(word, letters.known_letters_and_positions)
        and not has_known_not_letters(word, letters.known_not_letters)
    )


class RandomAgent(Agent):
    """
    Agent which randomly selects a word from the set of possible words

    Possible words are those which fit the information we've learnt during a game
    """

    def __init__(self, rng=None):
        super().__init__(rng)
        self.letters = None
        self.possible_words = None

    def _set_attrs(self, timestep):
        "Intializes state dependent attributes, if they are not already"
        if self.possible_words is None:
            self.possible_words = timestep.state.words
        if self.letters is None:
            self.letters = Letters(word_length=len(self.possible_words[0]))

    def _reset_attrs(self, timestep):
        "Sets state dependent attributes to initial values"
        self.possible_words = timestep.state.words
        self.letters = Letters(word_length=len(self.possible_words[0]))

    def update(self, timestep, action):
        self._set_attrs(timestep=timestep)

        if timestep.step == StepType.END:
            # We reset the set of possible words
            self._reset_attrs(timestep=timestep)
            return

        self.letters.update(guess=action, answer=timestep.state.answer)

        self.possible_words = [
            word
            for word in self.possible_words
            if is_possible_word(word, self.letters) and word != action
        ]

    def select_action(self, timestep):
        self._set_attrs(timestep=timestep)
        # We select a word from the set of possible words at random
        action = self._rng.choice(self.possible_words)
        return action
