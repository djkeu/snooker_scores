# Snooker Scores


## Description:
Program to display scores of a snooker game.


## Purpose program
Watching a snooker game, it can be pretty confusing when it comes to seeing how many possible points are left for each player to score. This is mainly because it differs if a player misses a red ball or a colored ball: if a colored ball is missed, the next ball to pot must be a red ball. This means that the points of the missed colored ball will no longer be available.

This program is to display how many points are still available for each player throughout the game. This could only be achieved by having the logic follow the games dynamics and rules. As a (desirable) side-effect, the program also shows the current scores and which balls are to be played next. 


## ToDo Section
Note: red_balls_phase, handle_last_colored_ball and colored_balls_phase contain some repetitive code

### Games analysed
ToDo: Real life tests with videos of snooker games (1 / 100)

- Shaun Murphy vs Zhou Jinhao | 2025 World Open | 147 - 0
- Trump vs Long | 2025 World Open Match 1 | 
- Trump vs Long | 2025 World Open Match 2 | 


### Conclusions Games analysed
- FixMe: failing tests for penalties
- Note: Miss of Balls vs Miss of Shot : var/method names?
- ToDo: prompt for restart at end of program
- ToDo: early victory: 'w' could be the key to trigger display_winner
- ToDo: store or show the results in case of early victory

ToDo: GUI


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

- test_game_logic.py - For testing the main game logic, including handling shots, phases, and score calculations.
- test_input_validation.py - For testing input validation, such as handling invalid values and ensuring correct user prompts.
- test_score_calculation.py - For testing how scores are updated based on different scenarios.


### game_flow
test_game_flow.py - For testing the overall game flow from start to finish.

```
$ pytest tests/test_game_flow.py --setup-plan
collected 20 items

```


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
- import sys
- pytest
- import itertools
- from io import StringIO
- from unittest.mock import patch

- from snooker_scores import SnookerScores


## End notes


## Going further: Do It Yourself Scoreboards
Do you hate how scoreboards on tv suddenly disappear during because some director wants to switch to the face of the player claiming that makes good television? 
