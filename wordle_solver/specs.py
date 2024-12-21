import enum


class StepType(enum.Enum):
    START = 0
    STEP = 1
    END = 2


class Reward(enum.Enum):
    WIN = 1
    DRAW = 0
    LOSE = -1
