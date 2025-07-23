# Snooker Scores

## Description:
Snooker Scores displays the scores of a snooker game. The user enters which balls are potted and more, following a game in real time.

## Purpose program
Watching a snooker game, it can be pretty confusing when it comes to seeing how many possible points are left for each player to score. This is mainly because it differs if a player misses a red ball or a colored ball. For instance, if a colored ball is missed, the next ball to pot must be a red ball. This means that the points of the missed colored ball will no longer be available. Also, if a red ball is potted, the next colored ball won't be available for the other player anymore.

This program is to display how many points are still available for each player throughout the game. This could only be achieved by having the logic follow the games dynamics and rules. As a side-effect, the program also shows the current scores, which balls are to be played next and more. Although it was not the original intent of the program, I consider it to be desirable.

## Hotkeys

Hotkeys:
q: quit
s: set starting scores
x: switch player
w: early victory
r: red ball down
p: penalty
f: free ball
0: missed ball

## File structure

    snooker_scores/
    ├── .venv/
    ├── tests/
        ├──  test_ball_handling.py
        ├──  test_colored_balls_phase.py
        ├──  test_game_phases.py
        ├──  test_game_state.py
        ├──  test_initialization.py
        ├──  test_input_handling.py
        ├──  test_integration.py
        └──  test_score_handling.py
    ├── txt/
        ├──  hotkeys.txt
        └──  startup_message.txt
    ├── .gitignore 
    ├── changelog.md 
    ├── pytest.ini 
    ├── readme.md 
    ├── snooker_scores.py 
    └── todo.md

## Pytest

    $ pytest --collect-only --quiet
    
    test_ball_handling.py::test_handle_red_ball
    test_ball_handling.py::test_handle_red_ball_when_color_needed
    test_ball_handling.py::test_handle_color_ball
    test_ball_handling.py::test_handle_color_ball_when_red_needed
    test_ball_handling.py::test_handle_miss
    test_ball_handling.py::test_handle_miss_after_color
    test_ball_handling.py::test_red_ball_down_basic
    test_ball_handling.py::test_red_ball_down_when_no_reds
    test_ball_handling.py::test_validate_shot_valid
    test_ball_handling.py::test_validate_shot_invalid
    
    test_colored_balls_phase.py::test_colored_balls_phase_correct_ball
    test_colored_balls_phase.py::test_colored_balls_phase_wrong_ball
    test_colored_balls_phase.py::test_last_colored_ball_phase_miss
    test_colored_balls_phase.py::test_last_colored_ball_phase_invalid_ball
    test_colored_balls_phase.py::test_last_colored_ball_phase_valid_ball
    test_colored_balls_phase.py::test_display_next_ball_red_player1
    test_colored_balls_phase.py::test_display_next_ball_color_player2
    test_colored_balls_phase.py::test_red_ball_down_no_reds
    test_colored_balls_phase.py::test_red_ball_down_last_red_needed
    test_colored_balls_phase.py::test_red_ball_down_second_to_last_red_player_1
    test_colored_balls_phase.py::test_red_ball_down_second_to_last_red_player_2
    
    test_game_phases.py::test_display_snookers_needed_player_1
    test_game_phases.py::test_display_snookers_needed_player_2
    test_game_phases.py::test_display_snookers_needed_no_snookers
    test_game_phases.py::test_winner_black_ball_phase_player_1
    test_game_phases.py::test_winner_black_ball_phase_player_2
    test_game_phases.py::test_handle_hotkeys_quit
    test_game_phases.py::test_handle_hotkeys_penalty
    test_game_phases.py::test_handle_hotkeys_switch
    test_game_phases.py::test_handle_hotkeys_set_scores
    test_game_phases.py::test_handle_hotkeys_early_victory
    test_game_phases.py::test_handle_hotkeys_red_ball_down
    test_game_phases.py::test_handle_hotkeys_invalid
    test_game_phases.py::test_setup_colored_balls_phase
    test_game_phases.py::test_last_colored_ball_phase
    
    test_game_state.py::test_restart_game_yes
    test_game_state.py::test_restart_game_no
    test_game_state.py::test_restart_game_invalid_then_yes
    test_game_state.py::test_exit_game
    test_game_state.py::test_early_victory
    test_game_state.py::test_black_ball_phase_miss_then_black
    test_game_state.py::test_black_ball_phase_invalid_then_black
    test_game_state.py::test_display_winner_player_1
    test_game_state.py::test_display_winner_player_2
    test_game_state.py::test_display_winner_tie
    test_game_state.py::test_display_colored_ball_to_play_player1
    test_game_state.py::test_display_colored_ball_to_play_player2
    test_game_state.py::test_display_break_below_century
    test_game_state.py::test_display_century_break
    
    test_initialization.py::test_initialization
    test_initialization.py::test_colored_balls_dict
    test_initialization.py::test_get_player_name
    test_initialization.py::test_get_player_name_empty_then_valid
    test_initialization.py::test_get_player_name_strips_and_titles
    test_initialization.py::test_prompt_for_player_names_yes
    test_initialization.py::test_prompt_for_player_names_no
    test_initialization.py::test_prompt_for_player_names_invalid_then_yes
    test_initialization.py::test_store_players_names_with_custom_names
    test_initialization.py::test_store_players_names_without_custom_names
    test_initialization.py::test_switch_players
    test_initialization.py::test_update_score
    test_initialization.py::test_calculate_potential_scores
    
    test_input_handling.py::test_store_players_names_yes
    test_input_handling.py::test_store_players_names_no
    test_input_handling.py::test_store_players_names_invalid_then_valid
    test_input_handling.py::test_get_shot_value_valid
    test_input_handling.py::test_get_shot_value_invalid_then_valid
    test_input_handling.py::test_get_shot_value_hotkey
    test_input_handling.py::test_respot_balls_yes
    test_input_handling.py::test_respot_balls_no_with_reds
    test_input_handling.py::test_respot_balls_no_without_reds
    test_input_handling.py::test_respot_balls_invalid_then_valid
    
    test_integration.py::test_basic_game_flow
    test_integration.py::test_full_red_phase_simple
    test_integration.py::test_break_calculation
    test_integration.py::test_potential_scores_calculation
    test_integration.py::test_snookers_needed_calculation
    test_integration.py::test_combine_penalties_and_scoring
    test_integration.py::test_player_switching
    
    test_score_handling.py::test_apply_penalty_player_1
    test_score_handling.py::test_apply_penalty_player_2
    test_score_handling.py::test_get_penalty_input_valid
    test_score_handling.py::test_get_penalty_input_invalid_then_valid
    test_score_handling.py::test_get_penalty_input_quit
    test_score_handling.py::test_free_ball_player_1_red_balls_phase
    test_score_handling.py::test_free_ball_player_2_red_balls_phase
    test_score_handling.py::test_free_ball_player_1_colored_balls_phase
    test_score_handling.py::test_free_ball_player_2_colored_balls_phase
    test_score_handling.py::test_update_game_state
    test_score_handling.py::test_validate_scores_valid
    test_score_handling.py::test_validate_scores_total_too_high
    test_score_handling.py::test_validate_scores_total_too_low
    test_score_handling.py::test_get_player_score_valid
    test_score_handling.py::test_get_player_score_negative
    test_score_handling.py::test_get_player_score_quit
    test_score_handling.py::test_collect_starting_scores_inputs_valid
    test_score_handling.py::test_collect_starting_scores_inputs_invalid_red_balls

    97 tests collected in 0.03s
