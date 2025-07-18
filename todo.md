# ToDo
ToDo file for Snooker Scores. Maintained from 2025-07-14 on.

## FixMe
- [ ] test_game_state.py
    - [ ] test_restart_game_yes() (test hangs)
    - [ ] test_restart_game_invalid_then_valid() (test fails)
- [ ] test_initialization
    - [ ] test_get_player_name_empty() (test hangs)


## ToDo
- [ ] add '0' to txt/hotkeys.txt, displayed from display_startup_message()
- [ ] refactor display_startup_message() : create display_hotkeys()
- [ ] set_up_game(): add call of display_hotkeys()
- [ ] colored_balls_phase: player x missed the y ball:
    - [*] player x failed to pot the y ball
    - [ ] print message @handle_miss: failed to pot
- [ ] store_players_names + get_player_name
    - [ ] refactor
- [ ] todo.md: check Requirements section
- [ ] test_initialization.py:
    - [ ] prompt_for_player_names()
    - [ ] store_players_names()
    - [ ] get_player_name()

## In Progress
- [ ] Live tests with videos of snooker games
    - [*] Live tests 1 - 85
    - [*] 86. Williams vs Zhao: 44 - 47
    - [ ] 87. 

## Done/Fixed
- [*] red ball accidentally potted
    - [*] change else condition in handle_red_ball()
    - [*] test changed else condition in handle_red_ball()
- [*] store_players_names()
    - [*] misleading variable name player_names
    - [*] split store_players_names into prompt function and store function
- [*] main() in snooker_scores.py
    - [*] remove calls of functions
    - [*] print message about running main.py instead of running the module
- [*] test_ball_handling
    - [*] test_handle_red_ball_when_color_needed

## Abandoned
- [ ] GUI
- [ ] explanation on when to use hotkey 'm'
- [ ] replace shot == 0 for missed shot with shot == 'm'
    - [ ] red_balls_phase()
    - [ ] get_shot_value()
    - [ ] handle_miss()
    - [ ] handle_hotkeys()
- [ ] explanation on when to use hotkey 'r'
