"""
Script for running to simple wordle solver.
"""

import logging

import click
import numpy as np

from wordle_solver.environment import Environment, StepType, Reward, TimeStep
from wordle_solver.agents import HumanAgent
from wordle_solver.utils import render_guess


logging.basicConfig(level=logging.INFO, format="%(message)s")


SEED_ENV = 1000
SEED_AGENT = 2000
N_EPISODES = 5
MAX_GUESSES = 5
WORD_LENGTH = 5


@click.command()
@click.option("--show/--no-show", default=False)
@click.option(
    "--seed-env",
    default=SEED_ENV,
    help="Seed for the environment. If -1 then a random integer between 0-9999 is chosen",
)
@click.option(
    "--seed-agent",
    default=SEED_AGENT,
    help="Seed for the agent. If -1 then a random integer between 0-9999 is chosen",
)
@click.option("--n-games", default=N_EPISODES, help="Number of games to run")
@click.option("--max-guesses", default=MAX_GUESSES, help="Number of guesses to allow")
@click.option("--word-length", default=WORD_LENGTH, help="Length of words to guess")
def run(show, seed_env, seed_agent, n_games, max_guesses, word_length):
    seed_env = seed_env if seed_env != -1 else np.random.randint(low=0, high=9999)
    seed_agent = seed_agent if seed_agent != -1 else np.random.randint(low=0, high=9999)
    _RNG_ENV = np.random.RandomState(seed_env)
    _RNG_AGENT = np.random.RandomState(seed_agent)
    logging.info(f"Seed environment: {seed_env}, seed agent: {seed_agent}")

    # Get set of possible 5 letter words
    with open("./all_words.txt") as f:
        words = f.read().splitlines()
        words = [word.upper() for word in words if len(word) == word_length]

    # Initialize the environment
    environment = Environment(words=words, rng=_RNG_ENV, max_guesses=max_guesses)

    # Initialize the agent
    agent = HumanAgent(rng=_RNG_AGENT)

    for n in range(n_games):
        logging.info(f"\nGame {n + 1}/{n_games}")
        log = "\n     "
        if show:
            log += "".join(f"\033[40m {x} \033[0m" for x in environment.answer)
            logging.info(log)
        else:
            log += "         "

        # Initial timestep
        timestep = TimeStep(
            state=environment.state(), step=StepType.START, reward=Reward.DRAW
        )

        while True:
            state = environment.state()

            action = agent.select_action(timestep=timestep)

            # Update the environment
            timestep = environment.step(action)

            # Print current state and guesses
            log += "\n" + render_guess(
                guess=action,
                answer=state.answer,
                n_guesses=state.n_guesses,
                max_guesses=max_guesses,
            )
            logging.info(log)

            # Update the agent's values
            agent.update(timestep=timestep, action=action)

            if timestep.step == StepType.END:
                if timestep.reward == Reward.WIN:
                    logging.info("You win!")
                elif timestep.reward == Reward.LOSE:
                    logging.info(
                        f"You lose - better luck next time! Answer {timestep.state.answer}"
                    )
                break

        environment.reset()


if __name__ == "__main__":
    run()
