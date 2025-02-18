# Snooker Scores

## Description:
Program to display scores of a snooker game.

## Purpose program
Watching a snooker game, it can be pretty confusing when it comes to seeing how many possible points are left for each player to score. This is mainly because it differs if a player misses a red ball or a colored ball: if a colored ball is missed, the next ball to pot must be a red ball. This means that the points of the missed colored ball will no longer be available.

This program is to display how many points are still available for each player throughout the game. This could only be achieved by having the logic follow the games dynamics and rules. As a (desirable) side-effect, the program also shows the current scores and which balls are to be played next. 

## ToDo Section
- ToDo: working test suite
- FixMe: test_calculate_possible_scores - assert 130 == 137
- FixMe: test_add_penalty - assert True is False
- FixMe: test_red_balls_phase - assert 14 == 0
- FixMe: test_colored_balls_phase - assert 2 == 27


## File structure

snooker_scores/
|-  src/
|   |-  __init__.py
|   |-  main.py  
|   |-  snooker_game.py
|   |-  snooker_gui.py
|-  tests/
|   |-  __init__.py
|   |-  conftest.py
|   |-  test_game_phases.py
|   |-  test_get_shot.py
|   |-  test_handle_balls.py
|   |-  test_inititialization.py
|   |-  test_scores.py
|   |-  test_set_scores.py
|   .gitgnore
|   pytest.ini
|   readme.md


## Pytest
$ pytest --setup-plan
========================================================================== test session starts ===========================================================================
platform win32 -- Python 3.12.4, pytest-8.3.4, pluggy-1.5.0
rootdir: E:\Gebruiker\Dev\snooker_scores
configfile: pytest.ini
collected 26 items

tests\test_get_shot.py 
        tests/test_get_shot.py::test_get_shot_value_quit
        tests/test_get_shot.py::test_get_shot_value_invalid
        tests/test_get_shot.py::test_get_shot_value_non_numeric
tests\test_handle_balls.py 
        tests/test_handle_balls.py::test_handle_red_ball
        tests/test_handle_balls.py::test_handle_red_ball_reduces_available_points
        tests/test_handle_balls.py::test_handle_color_ball
        tests/test_handle_balls.py::test_handle_color_ball_reduces_available_points
        tests/test_handle_balls.py::test_handle_miss
tests\test_init.py 
        tests/test_init.py::test_initial_state
        tests/test_init.py::test_initialize_prompt
        tests/test_init.py::test_switch_players
tests\test_phases.py 
        tests/test_phases.py::test_red_balls_phase
        tests/test_phases.py::test_colored_balls_phase
tests\test_scores.py 
        tests/test_scores.py::test_update_score
        tests/test_scores.py::test_calculate_possible_scores_player_1_turn_red_needed_next
        tests/test_scores.py::test_calculate_possible_scores_player_1_turn_colored_needed_next
        tests/test_scores.py::test_calculate_possible_scores_player_2_turn_red_needed_next
        tests/test_scores.py::test_calculate_possible_scores_player_2_turn_colored_needed_next
        tests/test_scores.py::test_calculate_possible_scores_edge_case_zero_available_points
        tests/test_scores.py::test_calculate_possible_scores_edge_case_negative_scores
        tests/test_scores.py::test_add_penalty
tests\test_set_scores.py 
        tests/test_set_scores.py::test_set_starting_scores_valid_input
        tests/test_set_scores.py::test_set_starting_scores_negative_scores
        tests/test_set_scores.py::test_set_starting_scores_total_score_exceeds_147
        tests/test_set_scores.py::test_set_starting_scores_invalid_red_balls
        tests/test_set_scores.py::test_set_starting_scores_non_numeric_input


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
