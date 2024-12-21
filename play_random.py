"""
Script for running to simple wordle solver.
"""

import logging

import click
import numpy as np

from wordle_solver.environment import Environment, StepType, Reward, TimeStep
from wordle_solver.agents.random_agent import RandomAgent
from wordle_solver.utils import render_guess


logging.basicConfig(level=logging.INFO, format="%(message)s")


SEED_ENV = 1000
SEED_AGENT = 2000
N_EPISODES = 5
MAX_GUESSES = 5
WORD_LENGTH = 5


@click.command()
@click.option("--seed-env", default=SEED_ENV)
@click.option("--seed-agent", default=SEED_AGENT)
@click.option("--n-games", default=N_EPISODES, help="Number of games to run")
@click.option("--max-guesses", default=MAX_GUESSES, help="Number of guesses to allow")
@click.option("--word-length", default=WORD_LENGTH, help="Length of words to guess")
def run(seed_env, seed_agent, n_games, max_guesses, word_length):
    _RNG_ENV = np.random.RandomState(seed_env)
    _RNG_AGENT = np.random.RandomState(seed_agent)

    # Get set of possible 5 letter words
    with open("./all_words.txt") as f:
        words = f.read().splitlines()
        words = [word.upper() for word in words if len(word) == word_length]

    # Initialize the environment
    environment = Environment(words=words, rng=_RNG_ENV, max_guesses=max_guesses)

    # Initialize the agent
    agent = RandomAgent(rng=_RNG_AGENT)

    for _ in range(n_games):
        logging.info(
            "\n     "
            + "".join(f"\033[40m {x} \033[0m" for x in environment.answer)
            + " No. possibilities"
        )

        # Initial timestep
        timestep = TimeStep(
            state=environment.state(), step=StepType.START, reward=Reward.DRAW
        )

        while timestep.step != StepType.END:
            state = environment.state()

            action = agent.select_action(timestep=timestep)  # state=state)

            # Update the environment
            timestep = environment.step(action)

            # Print current state and guesses
            logging.info(
                render_guess(
                    action,
                    answer=state.answer,
                    n_guesses=state.n_guesses,
                    n_possibilities=len(agent.possible_words),
                )
            )

            # Update the agent's values
            agent.update(timestep=timestep, action=action)

        # Reset the environment
        environment.reset()


if __name__ == "__main__":
    run()
