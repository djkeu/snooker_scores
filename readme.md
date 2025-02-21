# Snooker Scores


## Description:
Program to display scores of a snooker game.


## Purpose program
Watching a snooker game, it can be pretty confusing when it comes to seeing how many possible points are left for each player to score. This is mainly because it differs if a player misses a red ball or a colored ball: if a colored ball is missed, the next ball to pot must be a red ball. This means that the points of the missed colored ball will no longer be available.

This program is to display how many points are still available for each player throughout the game. This could only be achieved by having the logic follow the games dynamics and rules. As a (desirable) side-effect, the program also shows the current scores and which balls are to be played next. 


## ToDo Section
- FixMe: hardcoded minimum score in set_starting_scores
- ToDo: elaborate on welcome message
- ToDo: refactor red_balls_phase, handle_last_colored_ball, colored_balls_phase
- ToDo: refactor display_winner
- ToDo: move hardcode values to __init__ Note: or hardcode 147 and 27 in the code

- ToDo: real life test with video of snooker game

- ToDo:
4. Combine Score Calculation Logic

update_score and calculate_possible_scores could potentially be combined since they both deal with adjusting scores. If they are meant to do different things, you could rename them to clarify their roles.

- ToDo:
5. display_game_state and display_next_ball

You may find it more efficient to combine the logic for displaying the game state and the next ball in one method, as they both deal with showing the game progress.

- ToDo:
6. Improve respot_balls to Avoid Duplication

Currently, the respot_balls method calls get_respot_input and handles its result. Since the input is already validated in get_respot_input, respot_balls could be streamlined.

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

- test_game_logic.py – For testing the main game logic, including handling shots, phases, and score calculations.
- test_input_validation.py – For testing input validation, such as handling invalid values and ensuring correct user prompts.
- test_score_calculation.py – For testing how scores are updated based on different scenarios.
- test_game_flow.py – For testing the overall game flow from start to finish.


```
$ pytest --setup-plan

collected 32 items

tests\test_game_flow.py
        tests/test_game_flow.py::test_game_flow
tests\test_game_logic.py
        tests/test_game_logic.py::test_initial_game_setup
        tests/test_game_logic.py::test_switch_players
        tests/test_game_logic.py::test_handle_red_ball_player_1
        tests/test_game_logic.py::test_handle_red_ball_player_2
        tests/test_game_logic.py::test_handle_color_ball_player_1
        tests/test_game_logic.py::test_handle_color_ball_player_2
        tests/test_game_logic.py::test_handle_miss
        tests/test_game_logic.py::test_handle_last_colored_ball
        tests/test_game_logic.py::test_display_winner
tests\test_input_validation.py
        tests/test_input_validation.py::test_validate_shot_valid
        tests/test_input_validation.py::test_validate_shot_invalid
        tests/test_input_validation.py::test_validate_shot_quit
        tests/test_input_validation.py::test_validate_shot_p
        tests/test_input_validation.py::test_validate_shot_x
        tests/test_input_validation.py::test_validate_shot_s
        tests/test_input_validation.py::test_handle_special_input_q
        tests/test_input_validation.py::test_handle_special_input_p
        tests/test_input_validation.py::test_handle_special_input_x
        tests/test_input_validation.py::test_handle_special_input_s
        SETUP    F capfd
        tests/test_input_validation.py::test_handle_invalid_input (fixtures used: capfd, request)
        TEARDOWN F capfd
        tests/test_input_validation.py::test_get_respot_input_valid
        tests/test_input_validation.py::test_get_respot_input_invalid
        tests/test_input_validation.py::test_set_starting_scores_valid_input
        tests/test_input_validation.py::test_set_starting_scores_invalid_score
        tests/test_input_validation.py::test_set_starting_scores_invalid_red_balls
        tests/test_input_validation.py::test_set_starting_scores_invalid_total_score
        tests/test_input_validation.py::test_get_penalty_input_valid
        tests/test_input_validation.py::test_get_penalty_input_invalid
tests\test_score_calculation.py
        tests/test_score_calculation.py::test_apply_penalty
        tests/test_score_calculation.py::test_add_penalty_valid
        tests/test_score_calculation.py::test_add_penalty_invalid
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

### Imports
- sys

### Testing
- pytest
