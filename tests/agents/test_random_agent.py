"""
Module containing tests for the random agent
"""

from wordle_solver.agents.random_agent import (
    has_known_letters,
    has_known_letters_and_positions,
    has_known_not_letters,
)


def test_has_known_letters():
    assert has_known_letters("hello", ["h", "e", "l", "o"]) == True
    assert has_known_letters("hello", ["x"]) == False
    assert has_known_letters("foo", ["o"]) == True
    assert has_known_letters("bar", ["a", "a"]) == True


def test_has_known_not_letters():
    assert has_known_not_letters("hello", ["h", "e", "l", "o"]) == True
    assert has_known_not_letters("hello", ["x"]) == False
    assert has_known_not_letters("foo", ["o"]) == True
    assert has_known_not_letters("bar", ["a", "a"]) == True
    assert has_known_not_letters("hello", ["a", "e"]) == True


def test_has_known_letters_and_positions():
    assert has_known_letters_and_positions("hello", ["h", "e", "", "", ""]) == True
    assert has_known_letters_and_positions("hello", ["", "", "", "l", ""]) == True
    assert has_known_letters_and_positions("bye", ["a", "", ""]) == False
    assert has_known_letters_and_positions("bye", ["y", "", ""]) == False
