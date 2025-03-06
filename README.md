# 2048 Game with AI Mode

This is a Python implementation of the popular "2048" game with an added AI mode using basic decision-making algorithms. The game features manual controls for the player and an option to enable AI that automatically makes moves.

## Features

- **Game Mechanics:**
  - Move tiles left, right, up, or down.
  - Merge tiles of the same value.
  - New tiles appear on the grid after each move.

- **AI Mode:**
  - Toggle AI mode with the `AI MODE` button or the spacebar (`SPACE` key).
  - AI will automatically make moves every 300 milliseconds.
  
- **Game Over/Win:**
  - The game ends when there are no more moves available.
  - The game is won when the 2048 tile is reached.

- **Animations:**
  - Smooth animations for tile movements and merges.
  - The scale of the newly created tiles adjusts based on their animation progress.

## Installation

### Requirements

- Python 3.x
- Pygame (for the graphical interface)

### Installing Pygame

If you don't have Pygame installed, you can install it using `pip`:

```bash
pip install pygame
How to Run
Clone this repository to your local machine:

bash
Copy
Edit
git clone https://github.com/1akin1/2048-ai-expectimax.git
Navigate into the project directory:

bash
Copy
Edit
cd 2048-ai-game
Run the game:

bash
Copy
Edit
python main.py
Use the arrow keys to play manually, or press the spacebar to toggle AI mode.

Key Bindings
Arrow Keys:
Up, Down, Left, Right: Move tiles in the corresponding direction.
Spacebar: Toggle AI mode (AI will start making moves automatically).
R: Reset the game.
Mouse: Click the "AI MODE" button to toggle the AI mode on/off.

Game Development & AI
The AI uses a simple evaluation function that looks at:
The number of empty cells.
The maximum tile value on the grid.
The grid’s monotonicity (arrangement of tiles in a non-decreasing order).
The game grid is implemented as a 4x4 matrix with integer values, and the player interacts with it through keyboard inputs.

Contributing
Feel free to fork this project and contribute by making pull requests. Contributions can be in the form of bug fixes, new features, optimizations, or improvements to the AI.

by 1akin1
