# Changelog
Changelog for Snooker Scores

---

## [1.0.2] - 2025-07-20
### Removed
- main.py
### Changed
- run program from snooker_scores.py instead of main.py
- refactor display_startup_message()
- snooker_scores.py: move functions to appropriate sections
- update tests
- create new tests for the new/refactored functions in snooker_scores.py
- uppercase consts in __init__

---

## [1.0.1] - 2025-07-16
### Fixed
- miscaculation of remaining red balls when a red ball is accidentally potted instead of a colored ball in handle_red_ball()
- adjust test_handle_red_ball_when_color_needed() in test_ball_handling.py
### Changed
- comment out hanging test_restart_game_yes() in test_game_state.py
- refactor store_players_names() for clarity

---

## [1.0.0] - 2025-07-14
### Added
- create todo.md to hold todo's, fixme's and history
- create changelog.md to hold version information
### Changed
- add version number
- move todo section from readme.md to todo.md

---
