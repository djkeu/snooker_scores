# Snooker Scores


## Description:
Program to display scores of a snooker game.


## Purpose program
Watching a snooker game, it can be pretty confusing when it comes to seeing how many possible points are left for each player to score. This is mainly because it differs if a player misses a red ball or a colored ball. For instance, if a colored ball is missed, the next ball to pot must be a red ball. This means that the points of the missed colored ball will no longer be available. Also, if a red ball is potted, the next colored ball won't be available for the other player anymore.

This program is to display how many points are still available for each player throughout the game. This could only be achieved by having the logic follow the games dynamics and rules. As a (desirable) side-effect, the program also shows the current scores, which balls are to be played next and more. 


## ToDo Section
- ToDo: Real life tests with videos of snooker games (13 / 100)
    12. Trump vs Bingham 1 | 58 - 72
    13. Trump vs Bingham 2 | 0 - 108
    14. Higgins vs Robertson 1 | 95 - 1
    15. Higgins vs Robertson 2 | 120 - 0
    16. HIggins vs Robertson 3 | 0 - 82
    17. Higgins vs Robertson 4 | 21 - 90

- ToDo: GUI


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
snooker_scores/
├── sn_env/
├── tests/
│   ├──  test_game_flow.py
│   ├──  test_game_logic.py
│   ├──  test_input_validation.py
│   ├──  test_score_calculation.py
├── txt/
│   ├──  hotkeys.txt
├── .gitignore 
├── main.py 
├── pytest.ini 
├── README.md 
├── snooker_scores.py 

```


## Pytest

- test_game_flow.py:
    - Test the overall game flow from start to finish.
- test_game_logic.py
    - Test the main game logic, including handling shots, phases, and score calculations.

- test_input_validation.py
    - Test input validation, such as handling invalid values and ensuring correct user prompts.

- test_score_calculation.py
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

### Imports test files
- sys
- pytest
- import itertools
- from io import StringIO
- from unittest.mock import patch

- from snooker_scores import SnookerScores


## End notes

### Do It Yourself Scoreboards
Do you hate how scoreboards on tv suddenly disappear during because some director wants to switch to the face of the player claiming that makes good television? 
