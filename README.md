# Snooker Scores


## Description:
Program to display scores of a snooker game.


## Purpose program
Watching a snooker game, it can be pretty confusing when it comes to seeing how many possible points are left for each player to score. This is mainly because it differs if a player misses a red ball or a colored ball. For instance, if a colored ball is missed, the next ball to pot must be a red ball. This means that the points of the missed colored ball will no longer be available. Also, if a red ball is potted, the next colored ball won't be available for the other player anymore.

This program is to display how many points are still available for each player throughout the game. This could only be achieved by having the logic follow the games dynamics and rules. As a (desirable) side-effect, the program also shows the current scores, which balls are to be played next and more. 


## ToDo Section
- ToDo: refactor display_colored_ball_to_play

- ToDo: pytest
    - Note: do live tests after a test phase is marked Done:
    - Done: test_game_flow.py:
    - Done: test_game_logic.py
    - ToDo: test_input_validation.py
    - ToDo: test_score_calculation.py

- ToDo: Live tests with videos of snooker games (37 / 100)
    33. Trump vs Peifan: 65 - 56
    34. Williams vs Wilson: 5 - 75
    35. Wilson vs Robertson: 116 - 6
    36. Wilson vs Robertson: 106 - 13
    37. Wilson vs Robertson: 70 - 2
    38. Wilson vs Robertson:
        https://www.youtube.com/watch?v=hAw1cb7G4j8&t=1847s
        41:00

- ToDo: GUI


## Pytest

### Commands to show only failed tests:
    - $ pytest -v --tb=no --no-header --no-summary | grep FAILED | awk '{print $1}'
    - $ pytest --lf --collect-only -q

### Files
- test_game_flow.py:
    - Test the overall game flow from start to finish.

- test_game_logic.py
    - Test the main game logic, including handling shots, phases, and score calculations.

- test_input_validation.py
    - Test input validation, such as handling invalid values and ensuring correct user prompts.

- test_score_calculation.py
    - Test how scores are updated based on different scenarios.

### All tests updated 17-3-2025
```
$ pytest --collect-only --quiet
tests/test_game_flow.py::test_game_flow
tests/test_game_flow.py::test_multiple_penalties
tests/test_game_flow.py::test_switch_players_red_ball_phase
tests/test_game_flow.py::test_start_game_full_flow
tests/test_game_flow.py::test_start_game_early_exit
tests/test_game_flow.py::test_start_game_early_exit_red_ball_phase
tests/test_game_flow.py::test_start_game_early_exit_set_starting_scores
tests/test_game_flow.py::test_start_game_exceed_max_red_balls_then_early_exit
tests/test_game_flow.py::test_start_game_invalid_inputs
tests/test_game_flow.py::test_start_game_multiple_invalid_inputs
tests/test_game_flow.py::test_start_game_invalid_red_balls_then_early_exit
tests/test_game_flow.py::test_start_game_invalid_player_scores_then_early_exit
tests/test_game_flow.py::test_start_game_negative_player_scores_then_early_exit
tests/test_game_flow.py::test_start_game_penalty
tests/test_game_flow.py::test_start_game_penalty_no_respot
tests/test_game_flow.py::test_start_game_penalty_no_respot_edge_case
tests/test_game_flow.py::test_start_game_penalty_respot
tests/test_game_flow.py::test_start_game_penalty_respot_edge_case
tests/test_game_flow.py::test_start_game_set_scores
tests/test_game_flow.py::test_start_game_switch_players
tests/test_game_logic.py::test_initial_game_setup
tests/test_game_logic.py::test_switch_players
tests/test_game_logic.py::test_switch_players_edge_cases
tests/test_game_logic.py::test_display_game_state_edge_cases
tests/test_game_logic.py::test_display_next_ball_edge_cases
tests/test_game_logic.py::test_handle_ball_edge_cases
tests/test_game_logic.py::test_handle_ball_red
tests/test_game_logic.py::test_handle_red_ball_player_1
tests/test_game_logic.py::test_handle_red_ball_player_2
tests/test_game_logic.py::test_display_next_ball_red_player_1
tests/test_game_logic.py::test_handle_ball_color
tests/test_game_logic.py::test_handle_color_ball_player_1
tests/test_game_logic.py::test_handle_color_ball_player_2
tests/test_game_logic.py::test_handle_miss
tests/test_game_logic.py::test_red_balls_phase_edge_cases
tests/test_game_logic.py::test_handle_last_colored_ball
tests/test_game_logic.py::test_handle_last_colored_ball_edge_cases
tests/test_game_logic.py::test_colored_balls_phase
tests/test_game_logic.py::test_colored_balls_phase_basic
tests/test_game_logic.py::test_colored_balls_phase_edge_cases
tests/test_game_logic.py::test_display_winner
tests/test_input_validation.py::test_validate_shot_valid
tests/test_input_validation.py::test_validate_shot_invalid
tests/test_input_validation.py::test_validate_shot_quit
tests/test_input_validation.py::test_validate_shot_p
tests/test_input_validation.py::test_validate_shot_x
tests/test_input_validation.py::test_validate_shot_s
tests/test_input_validation.py::test_validate_shot_edge_cases
tests/test_input_validation.py::test_handle_special_input_q
tests/test_input_validation.py::test_handle_special_input_p
tests/test_input_validation.py::test_handle_special_input_x
tests/test_input_validation.py::test_handle_special_input_s
tests/test_input_validation.py::test_respot_balls_edge_cases
tests/test_input_validation.py::test_set_starting_scores_valid_input
tests/test_input_validation.py::test_set_starting_scores_invalid_score
tests/test_input_validation.py::test_set_starting_scores_invalid_red_balls
tests/test_input_validation.py::test_set_starting_scores_invalid_total_score
tests/test_input_validation.py::test_set_starting_scores_edge_cases
tests/test_input_validation.py::test_get_input_starting_scores_valid
tests/test_input_validation.py::test_get_input_starting_scores_invalid_then_valid
tests/test_input_validation.py::test_get_input_starting_scores_edge_cases
tests/test_input_validation.py::test_validate_red_balls_no_reds
tests/test_input_validation.py::test_validate_red_balls_valid_1_red
tests/test_input_validation.py::test_validate_red_balls_valid_2_reds
tests/test_input_validation.py::test_validate_red_balls_invalid_low
tests/test_input_validation.py::test_validate_red_balls_invalid_high
tests/test_input_validation.py::test_validate_red_balls_edge_cases
tests/test_input_validation.py::test_validate_player_scores_valid
tests/test_input_validation.py::test_validate_player_scores_negative
tests/test_input_validation.py::test_validate_player_scores_exceed_maximum_break
tests/test_input_validation.py::test_validate_player_scores_edge_cases
tests/test_input_validation.py::test_validate_min_score_valid
tests/test_input_validation.py::test_validate_min_score_invalid
tests/test_input_validation.py::test_validate_min_score_edge_cases
tests/test_input_validation.py::test_get_penalty_input_valid
tests/test_input_validation.py::test_get_penalty_input_invalid
tests/test_input_validation.py::test_get_penalty_input_edge_cases
tests/test_input_validation.py::test_get_penalty_input_early_exit
tests/test_input_validation.py::test_get_penalty_input_invalid_then_early_exit
tests/test_input_validation.py::test_get_penalty_input_negative_then_early_exit
tests/test_input_validation.py::test_store_players_names_no
tests/test_input_validation.py::test_store_players_names_yes
tests/test_input_validation.py::test_get_player_name_empty
tests/test_input_validation.py::test_get_player_name_valid
tests/test_input_validation.py::test_get_player_name_capitalized
tests/test_input_validation.py::test_get_player_name_whitespace
tests/test_input_validation.py::test_get_player_name_special_characters
tests/test_input_validation.py::test_get_player_name_multiple_words
tests/test_input_validation.py::test_get_player_name_all_lowercase
tests/test_input_validation.py::test_get_player_name_all_uppercase
tests/test_input_validation.py::test_get_player_name_mixed_case
tests/test_score_calculation.py::test_apply_penalty
tests/test_score_calculation.py::test_apply_penalty_edge_cases
tests/test_score_calculation.py::test_add_penalty_valid
tests/test_score_calculation.py::test_add_penalty_invalid
tests/test_score_calculation.py::test_add_penalty_edge_cases_2
tests/test_score_calculation.py::test_update_score_edge_cases
tests/test_score_calculation.py::test_calculate_potential_scores_edge_cases
```


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
