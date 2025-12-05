# CS2520-Snake-Final-Project

This project is an extended version of the classic Snake game built with Python and Pygame. The snake moves on a grid, eats food to grow, and the playable area expands over time. Random spikes are added as extra hazards, and the game keeps track of scores across runs and displays the top high scores on the game over screen.

---

## Requirements

- Python 3.x  
- [Pygame](https://www.pygame.org/)  
- The pixel font file `EXEPixelPerfect.ttf` placed in the `resources/` folder (used for score and title text).

Install Pygame with:

```bash
pip install pygame
```

---

## How to Run

From the project directory (where SnakeClass.py is located), run:
```bash
python SnakeClass.py
```
This will open the game window and show the start menu. 

---

## Controls

- W / A / S / D: Move Up / Left / Down / Right
- SPACE:
  - From start menu: begin the game
  - From game over screen: play again
- Q: Quit from the game over screen
