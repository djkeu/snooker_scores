# Snooker Scores

## Description:
Snooker Scores displays the scores of a snooker game. The user enters which balls are potted and more, following a game in real time.

## Purpose program
Watching a snooker game, it can be pretty confusing when it comes to seeing how many possible points are left for each player to score. This is mainly because it differs if a player misses a red ball or a colored ball. For instance, if a colored ball is missed, the next ball to pot must be a red ball. This means that the points of the missed colored ball will no longer be available. Also, if a red ball is potted, the next colored ball won't be available for the other player anymore.

This program is to display how many points are still available for each player throughout the game. This could only be achieved by having the logic follow the games dynamics and rules. As a side-effect, the program also shows the current scores, which balls are to be played next and more. Although it was not the original intent of the program, I consider it to be desirable.

## File structure

```
snooker_scores/
├── .venv/
├── tests/
│   ├──  test_ball_handling.py
│   ├──  test_colored_balls_phase.py
│   ├──  test_game_phases.py
│   ├──  test_game_state.py
│   ├──  test_initialization.py
│   ├──  test_input_handling.py
│   ├──  test_integration.py
│   ├──  test_score_handling.py
├── txt/
│   ├──  hotkeys.txt
├── .gitignore 
├── changelog.md 
├── pytest.ini 
├── readme.md 
├── snooker_scores.py 
├── todo.md 

```
