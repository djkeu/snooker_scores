# Snooker Scores


## Description:
Program to display scores of a snooker game.


## Purpose program
Watching a snooker game, it can be pretty confusing when it comes to seeing how many possible points are left for each player to score. This is mainly because it differs if a player misses a red ball or a colored ball. For instance, if a colored ball is missed, the next ball to pot must be a red ball. This means that the points of the missed colored ball will no longer be available. Also, if a red ball is potted, the next colored ball won't be available for the other player anymore.

This program is to display how many points are still available for each player throughout the game. This could only be achieved by having the logic follow the games dynamics and rules. As a (desirable) side-effect, the program also shows the current scores, which balls are to be played next and more. 


## ToDo Section
- ToDo: Live tests with videos of snooker games (62 / 100)
    61. Selby vs Higgins: 0 - 72
    62. Trump vs Hawkins: 0 - 82
    63. 

- ToDo: GUI


## Pytest

### All tests updated 10-4-2025
```
$ pytest --collect-only --quiet

tests/test_ball_handling.py::test_handle_red_ball
tests/test_ball_handling.py::test_handle_red_ball_when_color_needed
tests/test_ball_handling.py::test_handle_color_ball
tests/test_ball_handling.py::test_handle_color_ball_when_red_needed
tests/test_ball_handling.py::test_handle_miss
tests/test_ball_handling.py::test_handle_miss_after_color
tests/test_ball_handling.py::test_red_ball_down_basic
tests/test_ball_handling.py::test_red_ball_down_when_no_reds
tests/test_ball_handling.py::test_validate_shot_valid
tests/test_ball_handling.py::test_validate_shot_invalid

tests/test_colored_balls_phase.py::test_colored_balls_phase_correct_ball
tests/test_colored_balls_phase.py::test_colored_balls_phase_wrong_ball
tests/test_colored_balls_phase.py::test_last_colored_ball_phase_miss
tests/test_colored_balls_phase.py::test_last_colored_ball_phase_invalid_ball
tests/test_colored_balls_phase.py::test_last_colored_ball_phase_valid_ball
tests/test_colored_balls_phase.py::test_display_next_ball_red_player1
tests/test_colored_balls_phase.py::test_display_next_ball_color_player2
tests/test_colored_balls_phase.py::test_red_ball_down_no_reds
tests/test_colored_balls_phase.py::test_red_ball_down_last_red_needed
tests/test_colored_balls_phase.py::test_red_ball_down_second_to_last_red_player_1
tests/test_colored_balls_phase.py::test_red_ball_down_second_to_last_red_player_2

tests/test_game_phases.py::test_display_snookers_needed_player_1
tests/test_game_phases.py::test_display_snookers_needed_player_2
tests/test_game_phases.py::test_display_snookers_needed_no_snookers
tests/test_game_phases.py::test_winner_black_ball_phase_player_1
tests/test_game_phases.py::test_winner_black_ball_phase_player_2
tests/test_game_phases.py::test_handle_hotkeys_quit
tests/test_game_phases.py::test_handle_hotkeys_penalty
tests/test_game_phases.py::test_handle_hotkeys_switch
tests/test_game_phases.py::test_handle_hotkeys_set_scores
tests/test_game_phases.py::test_handle_hotkeys_early_victory
tests/test_game_phases.py::test_handle_hotkeys_red_ball_down
tests/test_game_phases.py::test_handle_hotkeys_invalid
tests/test_game_phases.py::test_setup_colored_balls_phase
tests/test_game_phases.py::test_last_colored_ball_phase

tests/test_game_state.py::test_restart_game_yes
tests/test_game_state.py::test_restart_game_no
tests/test_game_state.py::test_restart_game_invalid_then_valid
tests/test_game_state.py::test_exit_game
tests/test_game_state.py::test_early_victory
tests/test_game_state.py::test_black_ball_phase_miss_then_black
tests/test_game_state.py::test_black_ball_phase_invalid_then_black
tests/test_game_state.py::test_display_winner_player_1
tests/test_game_state.py::test_display_winner_player_2
tests/test_game_state.py::test_display_winner_tie
tests/test_game_state.py::test_display_colored_ball_to_play_player1
tests/test_game_state.py::test_display_colored_ball_to_play_player2
tests/test_game_state.py::test_display_break_below_century
tests/test_game_state.py::test_display_century_break

tests/test_initialization.py::test_initialization
tests/test_initialization.py::test_colored_balls_dict
tests/test_initialization.py::test_get_player_name
tests/test_initialization.py::test_get_player_name_empty
tests/test_initialization.py::test_switch_players
tests/test_initialization.py::test_update_score
tests/test_initialization.py::test_calculate_potential_scores

tests/test_input_handling.py::test_store_players_names_yes
tests/test_input_handling.py::test_store_players_names_no
tests/test_input_handling.py::test_store_players_names_invalid_then_valid
tests/test_input_handling.py::test_get_shot_value_valid
tests/test_input_handling.py::test_get_shot_value_invalid_then_valid
tests/test_input_handling.py::test_get_shot_value_hotkey
tests/test_input_handling.py::test_respot_balls_yes
tests/test_input_handling.py::test_respot_balls_no_with_reds
tests/test_input_handling.py::test_respot_balls_no_without_reds
tests/test_input_handling.py::test_respot_balls_invalid_then_valid

tests/test_integration.py::test_basic_game_flow
tests/test_integration.py::test_full_red_phase_simple
tests/test_integration.py::test_break_calculation
tests/test_integration.py::test_potential_scores_calculation
tests/test_integration.py::test_snookers_needed_calculation
tests/test_integration.py::test_combine_penalties_and_scoring
tests/test_integration.py::test_player_switching

tests/test_score_handling.py::test_apply_penalty_player_1
tests/test_score_handling.py::test_apply_penalty_player_2
tests/test_score_handling.py::test_get_penalty_input_valid
tests/test_score_handling.py::test_get_penalty_input_invalid_then_valid
tests/test_score_handling.py::test_get_penalty_input_quit
tests/test_score_handling.py::test_free_ball_player1_valid_input_first_try
tests/test_score_handling.py::test_free_ball_player2_valid_input_first_try
tests/test_score_handling.py::test_free_ball_invalid_then_valid_input
tests/test_score_handling.py::test_free_ball_min_max_values_player1
tests/test_score_handling.py::test_free_ball_min_max_values_player2
tests/test_score_handling.py::test_update_game_state
tests/test_score_handling.py::test_validate_scores_valid
tests/test_score_handling.py::test_validate_scores_total_too_high
tests/test_score_handling.py::test_validate_scores_total_too_low
tests/test_score_handling.py::test_get_player_score_valid
tests/test_score_handling.py::test_get_player_score_negative
tests/test_score_handling.py::test_get_player_score_quit
tests/test_score_handling.py::test_collect_starting_scores_inputs_valid
tests/test_score_handling.py::test_collect_starting_scores_inputs_invalid_red_balls

92 tests collected in 0.03s
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
