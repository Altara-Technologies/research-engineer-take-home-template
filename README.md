# AI Snake Arena

This repository contains a tiny Python project that powers a simple "AI Snake Arena." 

The starter code is intentionally messy. Your task is to:
1. Refactor the code and make it feel like something you would actually want to build on. This includes cleaning up the architecture, fixing bugs, improving the agent interface, and making the codebase more maintainable and extensible.
2. Implement at least one new AI agent strategy that demonstrates more sophisticated decision-making than the existing `RandomAgent` and `GreedyAgent`. Your agent should be well-integrated with the refactored codebase and show thoughtful game-playing logic. We encourage you to be creative with your agent strategies.
3. Write a short write-up describing the following. We're looking to better understand from this write-up how you reason about and evaluate systems at scale.
    1. How would you evaluate this system?
    2. If you grew this system into something more realistic or scalable down the road, how would you think about architecting and scaling?
    3. What are some more complex things you would try, given more time?


## Game Overview

This is a competitive two-player Snake game where AI agents control snakes on a 10x10 grid. The game rules are:

- **Objective**: Each snake tries to eat food to grow longer and score points while avoiding death.
- **Movement**: On each turn, each snake moves one cell in one of four directions (UP, DOWN, LEFT, RIGHT).
- **Food**: When a snake's head reaches a food cell, the snake grows by one segment, its score increases by 1, and new food spawns at a random location.
- **Death Conditions**: A snake dies if it:
  - Hits a wall (moves outside the grid boundaries)
  - Hits its own body
  - Hits the other snake's body
- **Game End**: The game ends when:
  - One snake dies (the other wins)
  - Both snakes die on the same turn (draw)
  - Maximum steps (500) are reached (snake with higher score wins, or draw if tied)
- **Starting Positions**: Snake 1 starts at positions (2,5) and (1,5) moving right. Snake 2 starts at (7,5) and (8,5) moving left.

## Getting Started

To run the starter code:

```python game.py [num_games]```

## Submission

When you're done, send back your refactored code and short write-up as a zip file. Do NOT share your code as a public Github repo.

If you have any questions, feel free to reach out.
