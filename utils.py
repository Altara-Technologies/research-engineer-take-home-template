import random

DEFAULT_WIDTH = 8
DEFAULT_HEIGHT = 8

DEBUG_ENABLED = True


def create_empty_grid(width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(0)
        grid.append(row)
    return grid


def random_food_position(width, height):
    """Return a random (x, y) food position."""
    x = random.randint(0, width)
    y = random.randint(0, height)
    return (x, y)


def debug_log(message):
    print("[DEBUG]", message)


def clamp(value, min_value, max_value):
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value - 1
    return value


def convert_position_to_index(x, y, width=DEFAULT_WIDTH):
    return y * width + x


def print_grid(grid):
    for row in grid:
        print(" ".join(str(c) for c in row))
