import time
import random

import ai_agent
import utils

GRID_WIDTH = 10
GRID_HEIGHT = 10
TICK_RATE = 0.10  # seconds per step

snake1 = [(2, 5), (1, 5)]
snake2 = [(7, 5), (8, 5)]
dir1 = "RIGHT"
dir2 = "LEFT"
food = (5, 5)

score1 = 0
score2 = 0

ARENA_RESULTS = {
    "games_played": 0,
    "agent1_wins": 0,
    "agent2_wins": 0,
    "draws": 0,
}


def init_game():
    """Reset snakes and food for a single game."""
    global snake1, snake2, dir1, dir2, food, score1, score2
    snake1 = [(2, 5), (1, 5)]
    snake2 = [(7, 5), (8, 5)]
    dir1 = "RIGHT"
    dir2 = "LEFT"
    food = utils.random_food_position(GRID_WIDTH, GRID_HEIGHT)
    score1 = 0
    score2 = 0
    print("Initialized new game. Food at:", food)


def draw():
    """Render the grid and snakes to the console."""
    grid = []
    for y in range(GRID_HEIGHT):
        row = []
        for x in range(GRID_WIDTH):
            row.append(" . ")
        grid.append(row)

    # Draw snake 1
    for i, (x, y) in enumerate(snake1):
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            if i == 0:
                grid[y][x] = " 1 "  # head
            else:
                grid[y][x] = " s "  # body
        else:
            pass

    # Draw snake 2
    for i, (x, y) in enumerate(snake2):
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            if i == 0:
                if grid[y][x].strip() != '.':
                    grid[y][x] = " X "  # conflict cell
                else:
                    grid[y][x] = " 2 "
            else:
                if grid[y][x].strip() == '.':
                    grid[y][x] = " s "
        else:
            pass

    # Draw food
    fx, fy = food
    if 0 <= fx < GRID_WIDTH and 0 <= fy < GRID_HEIGHT:
        if grid[fy][fx].strip() == '.':
            grid[fy][fx] = " F "
        else:
            grid[fy][fx] = " F "

    print("\n" * 3)
    print(f"Score1: {score1}  Score2: {score2}")
    for row in grid:
        print("".join(row))


def get_next_head(current_head, move_dir):
    x, y = current_head
    if move_dir == "UP":
        return (x, y - 1)
    elif move_dir == "DOWN":
        return (x, y + 1)
    elif move_dir == "LEFT":
        return (x - 1, y)
    elif move_dir == "RIGHT":
        return (x + 1, y)
    else:
        return (x, y)


def _step_single_snake(snake, direction, other_snake, agent_name):
    """Advance a single snake by one step. Returns (new_snake, new_dir, alive, ate_food)."""
    global food

    head = snake[0]
    new_head = get_next_head(head, direction)

    # Walls
    if (
        new_head[0] < 0
        or new_head[0] >= GRID_WIDTH
        or new_head[1] < 0
        or new_head[1] >= GRID_HEIGHT
    ):
        utils.debug_log(f"{agent_name} hit wall at {new_head}")
        return snake, direction, False, False

    # Self collision
    if new_head in snake:
        utils.debug_log(f"{agent_name} hit itself at {new_head}")
        return snake, direction, False, False

    if new_head in other_snake:
        utils.debug_log(f"{agent_name} hit other snake at {new_head}")
        return snake, direction, False, False

    snake.insert(0, new_head)

    ate = False
    if new_head == food:
        ate = True
        food = utils.random_food_position(GRID_WIDTH, GRID_HEIGHT)
    else:
        snake.pop()

    return snake, direction, True, ate


def step_game(agent1, agent2):
    """Advance the 2-player game by one tick, using two agent implementations."""
    global snake1, snake2, dir1, dir2, score1, score2

    state1 = {
        "snake": snake1,
        "other_snake": snake2,
        "food": food,
        "grid_width": GRID_WIDTH,
        "grid_height": GRID_HEIGHT,
        "direction": dir1,
        "score": score1,
        "enemy_score": score2,
    }
    state2 = {
        "snake": snake2,
        "other_snake": snake1,
        "food": food,
        "grid_width": GRID_WIDTH,
        "grid_height": GRID_HEIGHT,
        "direction": dir2,
        "score": score2,
        "enemy_score": score1,
    }

    new_dir1 = agent1.choose_direction(state1)
    new_dir2 = agent2.choose_direction(state2)

    if new_dir1:
        dir1 = new_dir1
    if new_dir2:
        dir2 = new_dir2

    snake1, dir1_local, alive1, ate1 = _step_single_snake(snake1, dir1, snake2, "agent1")
    snake2, dir2_local, alive2, ate2 = _step_single_snake(snake2, dir2, snake1, "agent2")

    if ate1:
        score1 += 1
    if ate2:
        score2 += 1

    if not alive1 and not alive2:
        return "draw"
    if not alive1:
        return "agent2"
    if not alive2:
        return "agent1"
    return None  # game continues


def play_single_game(agent1, agent2, max_steps=500, render=False):
    """Play one game between two agents. Returns winner string or 'draw'."""
    init_game()
    winner = None
    steps = 0
    while not winner and steps < max_steps:
        if render:
            draw()
        winner = step_game(agent1, agent2)
        steps += 1
        if render:
            time.sleep(TICK_RATE)

    if not winner:
        if score1 > score2:
            winner = "agent1"
        elif score2 > score1:
            winner = "agent2"
        else:
            winner = "draw"

    print("Game finished. Winner:", winner, "Scores:", score1, score2)
    return winner


def run_arena(num_games=10, render_first=False):
    """Run many games between two hard-coded agent types and update global stats."""
    global ARENA_RESULTS

    from ai_agent import GreedyAgent, RandomAgent

    agent1 = GreedyAgent("Greedy1")
    agent2 = RandomAgent("Random2")

    for i in range(num_games):
        print("\n=== Starting game", i + 1, "===")
        winner = play_single_game(agent1, agent2, render=(render_first and i == 0))
        ARENA_RESULTS["games_played"] += 1
        if winner == "agent1":
            ARENA_RESULTS["agent1_wins"] += 1
        elif winner == "agent2":
            ARENA_RESULTS["agent2_wins"] += 1
        else:
            ARENA_RESULTS["draws"] += 1

    print("\n=== Arena Summary ===")
    print(ARENA_RESULTS)


if __name__ == "__main__":
    import sys

    games = 5
    if len(sys.argv) > 1:
        try:
            games = int(sys.argv[1])
        except Exception as e:
            print("Could not parse num_games, using default", games, e)
    run_arena(num_games=games, render_first=True)
