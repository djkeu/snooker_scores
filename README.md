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
- ToDo: prompt for restart at end of program
- ToDo: display_winner: display score of loser as well
- ToDo: early victory: 'w' could be the key to trigger display_winner
- ToDo: quitting (q): display scores
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

### Game flow
- test_game_flow.py

For testing the overall game flow from start to finish.

```
$ pytest tests/test_game_flow.py --setup-plan -q

        tests/test_game_flow.py::test_game_flow
        SETUP    F capsys
        tests/test_game_flow.py::test_start_game_full_flow (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_flow.py::test_start_game_early_exit (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_flow.py::test_start_game_penalty (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_flow.py::test_start_game_switch_players (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_flow.py::test_start_game_set_scores (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_flow.py::test_start_game_invalid_inputs (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_flow.py::test_start_game_multiple_invalid_inputs (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_flow.py::test_start_game_penalty_respot (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_flow.py::test_start_game_penalty_no_respot (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_flow.py::test_start_game_early_exit_set_starting_scores (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_flow.py::test_start_game_invalid_red_balls_then_early_exit (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_flow.py::test_start_game_invalid_player_scores_then_early_exit (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_flow.py::test_start_game_negative_player_scores_then_early_exit (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_flow.py::test_start_game_exceed_max_red_balls_then_early_exit (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_flow.py::test_start_game_early_exit_red_ball_phase (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_flow.py::test_start_game_penalty_respot_edge_case (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_flow.py::test_start_game_penalty_no_respot_edge_case (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_flow.py::test_multiple_penalties (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_flow.py::test_switch_players_red_ball_phase (fixtures used: capsys, request)
        TEARDOWN F capsys
```

### Game logic
- test_game_logic.py

For testing the main game logic, including handling shots, phases, and score calculations.

```
$ pytest tests/test_game_logic.py --setup-plan -q

        tests/test_game_logic.py::test_initial_game_setup
        tests/test_game_logic.py::test_switch_players
        tests/test_game_logic.py::test_switch_players_edge_cases
        SETUP    F capsys
        tests/test_game_logic.py::test_display_game_state_edge_cases (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_logic.py::test_display_next_ball_edge_cases (fixtures used: capsys, request)
        TEARDOWN F capsys
        tests/test_game_logic.py::test_handle_ball_edge_cases
        tests/test_game_logic.py::test_handle_ball_red
        tests/test_game_logic.py::test_handle_red_ball_player_1
        tests/test_game_logic.py::test_handle_red_ball_player_2
        SETUP    F capsys
        tests/test_game_logic.py::test_display_next_ball_red_player_1 (fixtures used: capsys, request)
        TEARDOWN F capsys
        tests/test_game_logic.py::test_handle_ball_color
        tests/test_game_logic.py::test_handle_color_ball_player_1
        tests/test_game_logic.py::test_handle_color_ball_player_2
        tests/test_game_logic.py::test_handle_miss
        SETUP    F capsys
        tests/test_game_logic.py::test_red_balls_phase_edge_cases (fixtures used: capsys, request)
        TEARDOWN F capsys
        tests/test_game_logic.py::test_handle_last_colored_ball
        SETUP    F capsys
        tests/test_game_logic.py::test_handle_last_colored_ball_edge_cases (fixtures used: capsys, request)
        TEARDOWN F capsys
        SETUP    F capsys
        tests/test_game_logic.py::test_colored_balls_phase (fixtures used: capsys, request)
        TEARDOWN F capsys
        tests/test_game_logic.py::test_colored_balls_phase_basic
        SETUP    F capsys
        tests/test_game_logic.py::test_colored_balls_phase_edge_cases (fixtures used: capsys, request)
        TEARDOWN F capsys
        tests/test_game_logic.py::test_display_winner
```

### Input validation
- test_input_validation.py

For testing input validation, such as handling invalid values and ensuring correct user prompts.

```
$ pytest tests/test_input_validation.py --setup-plan -q

        tests/test_input_validation.py::test_validate_shot_valid
        tests/test_input_validation.py::test_validate_shot_invalid
        tests/test_input_validation.py::test_validate_shot_quit
        tests/test_input_validation.py::test_validate_shot_p
        tests/test_input_validation.py::test_validate_shot_x
        tests/test_input_validation.py::test_validate_shot_s
        tests/test_input_validation.py::test_validate_and_return_shot_valid
        tests/test_input_validation.py::test_validate_and_return_shot_invalid
        tests/test_input_validation.py::test_validate_shot_edge_cases
        tests/test_input_validation.py::test_handle_special_input_q
        tests/test_input_validation.py::test_handle_special_input_p
        tests/test_input_validation.py::test_handle_special_input_x
        tests/test_input_validation.py::test_handle_special_input_s
        SETUP    F capfd
        tests/test_input_validation.py::test_handle_invalid_input (fixtures used: capfd, request)
        TEARDOWN F capfd
        tests/test_input_validation.py::test_get_respot_input_valid
        tests/test_input_validation.py::test_get_respot_input_invalid
        tests/test_input_validation.py::test_get_respot_input_edge_cases
        tests/test_input_validation.py::test_respot_balls_edge_cases
        tests/test_input_validation.py::test_set_starting_scores_valid_input
        tests/test_input_validation.py::test_set_starting_scores_invalid_score
        tests/test_input_validation.py::test_set_starting_scores_invalid_red_balls
        tests/test_input_validation.py::test_set_starting_scores_invalid_total_score
        tests/test_input_validation.py::test_set_starting_scores_edge_cases
        tests/test_input_validation.py::test_get_input_starting_scores_valid
        tests/test_input_validation.py::test_get_input_starting_scores_invalid_then_valid
        tests/test_input_validation.py::test_get_input_starting_scores_exhaust_retries
        tests/test_input_validation.py::test_get_input_starting_scores_edge_cases
        tests/test_input_validation.py::test_validate_red_balls_valid
        tests/test_input_validation.py::test_validate_red_balls_invalid_low
        tests/test_input_validation.py::test_validate_red_balls_invalid_high
        tests/test_input_validation.py::test_validate_red_balls_edge_cases
        tests/test_input_validation.py::test_validate_player_scores_valid
        tests/test_input_validation.py::test_validate_player_scores_negative
        tests/test_input_validation.py::test_validate_player_scores_exceed_maximum_break
        tests/test_input_validation.py::test_validate_player_scores_edge_cases
        tests/test_input_validation.py::test_validate_minimum_score_valid
        tests/test_input_validation.py::test_validate_minimum_score_invalid
        tests/test_input_validation.py::test_validate_minimum_score_edge_cases
        tests/test_input_validation.py::test_get_penalty_input_valid
        tests/test_input_validation.py::test_get_penalty_input_invalid
        tests/test_input_validation.py::test_get_penalty_input_edge_cases
        tests/test_input_validation.py::test_get_penalty_input_early_exit
        tests/test_input_validation.py::test_get_penalty_input_invalid_then_early_exit
        tests/test_input_validation.py::test_get_penalty_input_negative_then_early_exit
```

### Score calculation
- test_score_calculation.py

For testing how scores are updated based on different scenarios.

```
$ pytest tests/test_score_calculation.py --setup-plan -q

        tests/test_score_calculation.py::test_apply_penalty
        tests/test_score_calculation.py::test_apply_penalty_edge_cases
        tests/test_score_calculation.py::test_add_penalty_valid
        tests/test_score_calculation.py::test_add_penalty_invalid
        tests/test_score_calculation.py::test_add_penalty_edge_cases_2
        tests/test_score_calculation.py::test_update_score_edge_cases
        tests/test_score_calculation.py::test_calculate_potential_scores_edge_cases
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
