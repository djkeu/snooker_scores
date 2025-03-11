# Snooker Scores


## Description:
Program to display scores of a snooker game.


## Purpose program
Watching a snooker game, it can be pretty confusing when it comes to seeing how many possible points are left for each player to score. This is mainly because it differs if a player misses a red ball or a colored ball: if a colored ball is missed, the next ball to pot must be a red ball. This means that the points of the missed colored ball will no longer be available.

This program is to display how many points are still available for each player throughout the game. This could only be achieved by having the logic follow the games dynamics and rules. As a (desirable) side-effect, the program also shows the current scores and which balls are to be played next. 


## ToDo Section
- ToDo: set_starting_scores
    - Done: prompt for colored ball to play when red ball == 0
    - Done: available: set to (27 - value of colored balls played)
    - ToDo: refactor

- ToDo: get rid of rotating welcome messages, one is enough

- ToDo: repetitive code
    - set_starting_scores
    - red_balls_phase
    - handle_last_colored_ball
    - colored_balls_phase

- ToDo: GUI

```
### Desired output:

$ python claude_snooker_scores.py

                Six times world champion!

q: quit, s: set starting scores, x: switch player, p: penalty, w: early victory

Do you want to enter player names? (y/n) n
What's the value of the shot: s
Enter the number of red balls left: 0
Available colored balls:
2: yellow
3: green
4: brown
5: blue
6: pink
7: black
Enter the value of the next colored ball to play: 3
Enter score for Player 1: 55
Enter score for Player 2: 55

Player 1: score 55, potential score 80
Player 2: score 55, potential score 80
Player 1 must pot a green ball
What's the value of the shot: 3

Player 1: score 58, potential score 80
Player 2: score 55, potential score 77
Player 1 must pot a brown ball
What's the value of the shot: 4

Player 1: score 62, potential score 80
Player 2: score 55, potential score 73
Player 1 must pot a blue ball
What's the value of the shot: 5

Player 1: score 67, potential score 80
Player 2: score 55, potential score 68
Player 1 must pot a pink ball
What's the value of the shot: 6

Player 1: score 73, potential score 80
Player 2: score 55, potential score 62
Player 2 needs snookers!
Player 1 must pot a black ball
What's the value of the shot: 7

Player 1: score 80, potential score 80
Player 2: score 55, potential score 55

Player 1 wins! (with a score of 80 vs 55)
Do you want to play again? (y/n)

```


### Games analyzed
ToDo: Real life tests with videos of snooker games (13 / 100)

        12. Trump vs Bingham 1 | 58 - 72
        13. Trump vs Bingham 2 | 0 - 108

### Conclusions Games analyzed


## File structure

### No GUI

```
snooker_scores/
├── sn_env/
├── tests/
│   ├──  test_game_flow.py
│   ├──  test_game_logic.py
│   ├──  test_input_validation.py
│   ├──  test_score_calculation.py
│   ├──  tst_snooker.py
├── txt/
│   ├──  hotkeys.txt
│   ├──  welcome_messages.txt
├── .gitignore 
├── main.py 
├── pytest.ini 
├── readme.md 
├── snooker_scores.py 

```

### New GUI

```
Note: needs to be updated

snooker_scores/
├── sn_env/
├── tests/
│   ├──  test_game_flow.py
│   ├──  test_game_logic.py
│   ├──  test_input_validation.py
│   ├──  test_score_calculation.py
│   ├──  tst_snooker.py
├── txt/
│   ├──  hotkeys.txt
│   ├──  welcome_messages.txt
├── .gitignore 
├── main.py 
├── pytest.ini 
├── readme.md 
├── snooker_scores.py 

```

### Old GUI

```
Note: obsolete

snooker_scores/ 
├── src/ 
│   ├──  __init__.py
│   ├──  main.py
│   ├──  snooker_game.py
│   ├──  snooker_gui.py
├── tests/
│   ├──  __init__.py
│   ├──  test_conftest.py
│   ├──  test_game_phases.py
│   ├──  test_get_shot.py
│   ├──  test_handle_balls.py
│   ├──  test_initialization.py
│   ├──  test_scores.py
│   ├──  test_set_starting_scores.py
├── .gitignore 
├── pytest.ini 
├── readme.md

```


## Pytest

test_game_flow.py: 

- Test the overall game flow from start to finish.

test_game_logic.py

- Test the main game logic, including handling shots, phases, and score calculations.

test_input_validation.py

- Test input validation, such as handling invalid values and ensuring correct user prompts.

test_score_calculation.py

- Test how scores are updated based on different scenarios.


## Snooker rules
Points are also scored if the opponent makes the following mistakes:
- Do not touch any ball with the cue ball,
- Hitting or pocketing a wrong color ball,
- Pocketing the cue ball,
- Get a ball out of the playing area,
- Use another cue ball than the white ball,
- Push balls.

### De fouten
Als een stoot een fout geeft, dan krijgt uw tegenstander penalty punten:

- 4 punten als de witte (cue) bal werd gepot.
- 7 punten als de tijd om het stoten verstreken is ( 60 seconden/ stoot).
- als de witte bal de verkeerde bal eerst raakt dan de punten van dat kleur. Met een minimum van 4 punten.
- Als de verkeerde bal eerst wordt gepot, dan de punten van dat kleur. Met een minimum van 4 punten.

Dus wanneer een stoot een fout is. Krijgt de tegenstander die strafpunten bij zijn score.
Strafpunten hebben een minimum van 4 punten.
Nadat er een fout werd gemaakt mag de tegenspeler:

- Stoten op de ballen zoals ze liggen.
- Zijn beurt doorgeven, En hem die stoot laten doen. (Zonder terug te keren naar de vorige positie van het spel.).


## Requirements

### Extensions
- Recommended: ToDo Highlights

### Imports main file
- sys
- from random import randint

### Imports test files
- sys
- pytest
- import itertools
- from io import StringIO
- from unittest.mock import patch

- from snooker_scores import SnookerScores


## End notes


## Going further: Do It Yourself Scoreboards
Do you hate how scoreboards on tv suddenly disappear during because some director wants to switch to the face of the player claiming that makes good television? 
