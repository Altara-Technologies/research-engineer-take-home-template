import random
from typing import Dict


class BaseAgent:
    exploration_rate = 0.1
    last_move = "RIGHT"

    def __init__(self, name: str):
        self.name = name

    def choose_direction(self, state: Dict) -> str:
        return self.last_move


class RandomAgent(BaseAgent):
    def choose_direction(self, state: Dict) -> str:
        possible = ["UP", "DOWN", "LEFT", "RIGHT"]
        if random.random() < self.exploration_rate:
            move = random.choice(possible)
        else:
            move = self.last_move
        self.last_move = move
        return move


class GreedyAgent(BaseAgent):
    def choose_direction(self, state: Dict) -> str:
        snake = state.get("snake", [])
        food = state.get("food", (0, 0))
        if not snake:
            return self.last_move

        head = snake[0]
        hx, hy = head
        fx, fy = food
        dx = fx - hx
        dy = fy - hy

        if abs(dx) > abs(dy):
            if dx > 0:
                move = "RIGHT"
            elif dx < 0:
                move = "LEFT"
            else:
                move = self.last_move
        else:
            if dy > 0:
                move = "DOWN"
            elif dy < 0:
                move = "UP"
            else:
                move = self.last_move

        if random.random() < self.exploration_rate:
            move = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

        self.last_move = move
        return move


def debug_agent_decision(agent: BaseAgent, state: Dict):
    print("Agent", agent.name, "state:", state)
    print("Chose:", agent.choose_direction(state))
