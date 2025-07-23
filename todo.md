# ToDo
ToDo file for Snooker Scores. Maintained from 2025-07-14 on.

## FixMe

## ToDo
- [ ] add leading underscores to helper methods in SnookerScores
    - [*] _display_startup_message
    - [*] _display_hotkeys
    - [*] _store_players_names
    - [*] _prompt_for_player_names
    - [*] _get_players_name

    - [*] _red_balls_phase
    - [*] _last_colored_ball
    - [*] _colored_balls_phase

    - [*] _get_shot_value
    - [*] _validate_shot

    - [*] _handle_red_ball
    - [*] _handle_color_ball
    - [*] _handle_ball
    - [*] _display_next_ball


    - [ ] identify remaining helper functions

- [ ] pytest
    - [ ] add test for run_of_the_balls()
    - [ ] check test for _red_balls_phase()
    - [ ] check test for _last_colored_ball_phase()
    - [ ] check test for _colored_balls_phase()
- [*] display startup message
    - [*] get message from txt/startup_messages.txt
    - [*] display random message
    - [ ] add messages to txt/startup_messages.txt

## In Progress
- [ ] Live tests with videos of snooker games
    - [*] Live tests 1 - 85
    - [*] 86. Williams vs Zhao: 44 - 47
    - [ ] 87. 

## Done
- [*] store_players_names()
    - [*] misleading variable name player_names
    - [*] split store_players_names into prompt function and store function
- [*] colored_balls_phase: player x missed the y ball:
    - [*] player x failed to pot the y ball
- [*] store_players_names + get_player_name
    - [*] refactor
- [*] add '0' to txt/hotkeys.txt, displayed from display_startup_message()
- [*] refactor display_startup_message() : create display_hotkeys()
- [*] set_up_game(): add call of display_hotkeys()
- [*] test_initialization.py:
    - [*] prompt_for_player_names()
    - [*] store_players_names()
    - [*] get_player_name()
- [*] start program from snooker_scores.py, remove main.py
- [*] COLORED_BALLS
    - [*] Check if dictionary self.colored_balls is used anywhere
        - [*] colored_balls_phase()
        - [*] display_colored_ball_to_play()
    - [*] rename self.colored_balls to COLORS
- [*] readme.md
    - [*] check Requirements section
    - [*] remove obsolete/abundant sections
- [*] rename variable self.yellow_ball:
    - [ ] first_color
    - [ ] end_game_color
    - [ ] dedicated_color
    - [*] color_in_line
- [ ] mention hotkeys in docstrings in applicable functions
    - [*] exit_game: q
    - [*] add_penalty: p
    - [*] switch_players: x
    - [*] set_starting_scores: s
    - [*] early_victory: w
    - [*] red_ball_down: r
    - [*] handle_free_ball: f
- [*] create run_of_the_balls method to hold the helper methods below
- [*] call run_of_the_balls instead of red_balls_phase in
    - [*] update_game_state
    - [*] main()

## Fixed
- [*] red ball accidentally potted
    - [*] change else condition in handle_red_ball()
    - [*] test changed else condition in handle_red_ball()
- [*] test_ball_handling
    - [*] test_handle_red_ball_when_color_needed
- [*] test_game_state.py
    - [*] test_restart_game_yes() (test hangs)
    - [*] test_restart_game_invalid_then_valid() (test fails)
- [*] test_initialization.py
    - [*] test_get_player_name_empty() (test hangs)

## Abandoned
- [ ] GUI
- [ ] explanation on when to use hotkey 'm'
- [ ] replace shot == 0 for missed shot with shot == 'm'
    - [ ] red_balls_phase()
    - [ ] get_shot_value()
    - [ ] handle_miss()
    - [ ] handle_hotkeys()
- [ ] explanation on when to use hotkey 'r'
- [*] main() in snooker_scores.py
    - [*] remove calls of functions
    - [*] print message about running main.py instead of running the module
