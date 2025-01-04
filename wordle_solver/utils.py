import string
import enum
from typing import Optional


class BackgroundColor(str, enum.Enum):
    YELLOW = "43m"
    GREEN = "42m"
    GREY = "47m"
    BLACK = "40m"


class TextColor(str, enum.Enum):
    RED = "91"
    GREEN = "92"
    WHITE = "97"


def format_text(
    text,
    text_colour_code=TextColor.WHITE.value,
    background_color_code=BackgroundColor.BLACK.value,
):
    return f"\033[{text_colour_code};{background_color_code} {text} \033[0m"


def render_guess(
    guess: str,
    answer: str,
    n_guesses: int,
    max_guesses: int,
    n_possibilities: Optional[int] = None,
):
    "Colour codes the guess wrt the answer"
    # text_colour = "97" if n_guesses <= 5 else "91"
    text_color = TextColor.WHITE if n_guesses <= max_guesses else TextColor.RED

    output = format_text("{} :".format(n_guesses), text_colour_code=text_color)
    matched_indices = set()
    for i, letter in enumerate(guess):
        # Guessed letter in answer in correct position
        if letter == answer[i]:
            output += format_text(
                letter,
                text_colour_code=text_color,
                background_color_code=BackgroundColor.GREEN,
            )
        # Guessed letter in answer, incorrect position
        elif letter in answer and answer.index(letter) not in matched_indices:
            output += format_text(
                letter,
                text_colour_code=text_color,
                background_color_code=BackgroundColor.YELLOW,
            )
            matched_indices.add(answer.index(letter))
        # Letter not in answer
        else:
            output += format_text(
                letter,
                text_colour_code=text_color,
                background_color_code=BackgroundColor.GREY,
            )

    output += f" {n_possibilities}" if n_possibilities is not None else ""
    return output


def letter2index(letter: str):
    assert len(letter) == 1
    assert letter in string.ascii_uppercase
    return ord(letter) - ord("A")


def index2letter(ind: int):
    assert 0 <= ind <= 25
    return chr(ord("A") + ind)
