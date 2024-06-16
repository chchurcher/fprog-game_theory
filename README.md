# Game Theory Simulation Kit

## Overview

This repository contains a functional programming approach to game theory problems. It includes code for modeling and solving a specific game theory scenarios using Python.

### Description of the Simulated Game

Four players each start with a capital of €10. Each round, players anonymously contribute any amount to a pool collected by the bank. The bank doubles the total amount and distributes it equally among all players. This process is repeated over several rounds. 

Different strategies can be employed by both the bank and players:
- **Bank Strategies**: The bank may vary how it increases the contributions by imposing fees or changing the distribution method.
- **Player Strategies**: Players can choose to contribute different amounts, cooperate with others, or act selfishly to maximize personal gain.

## Repository Structure

- `src/`: Contains the source code for the project.
- `src/game.py`: Handles and executes one simulation of one distinct played game
- `src/player.py`: Player with only the information in his point of view. The player class is inherited to change the strategies.
- `src/setup.py`: Simulates a huge number of games with a certain number of player. Saves and plots the data.
- `src/main.py`: Main execution script.
- `src/`: Contains the source code for the project.
- `test/`: Includes test cases to ensure the correctness of the code.

## Prerequisites

- Python 3.x

## Installation

1. Clone the repository:
   ```sh git clone https://github.com/chchurcher/fprog-game_theory.git```
2. Navigate to the project directory:
   ```cd fprog-game_theory```

## Usage
To run the code, execute the main script in the src directory:
    ```python src/main.py```

## Results
### Duel of Strategies
The simulation results of nine different players competing in games of only two players each can be found [here](/docs/dualOfStrategies.md).
![Boxplot with log values](/docs/dual_of_strategies/duelOfStrategiesBoxplotLog.png)

### Four each Game
The simulation results of seven different players competing in games of four players each can be found [here](/docs/fourEachGame.md).
![Boxplot with log values](/docs/four_each_game/fourEachGameBoxplotLog.png)

### Comparing the above simulations
High cooperative strategies are considered to be risky, because they can lose the most money. However, in the most cases they perform better than every low cooperative strategy. When for example four players compete in a game, different strategies don't perform better than the **AllIn** strategy. Even though low cooperation can minimize the possible lost, it can be said that trust is valued in the longrun.

## License
MIT License

Copyright (c) 2024 Christoph Kircher

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.