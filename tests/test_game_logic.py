import pytest
from unittest.mock import patch
from snooker_scores import SnookerScores


def mock_input(prompt, value):
    return patch('builtins.input', return_value=value)

# Game initialization and player switching
def test_initial_game_setup():
    game = SnookerScores()
    
    assert game.score_player_1 == 0
    assert game.score_player_2 == 0
    assert game.available_player_1 == 147
    assert game.available_player_2 == 147
    assert game.red_balls == 15

def test_switch_players():
    game = SnookerScores()
    
    game.switch_players()
    assert game.player_1_turn is False
    
    game.switch_players()
    assert game.player_1_turn is True

# Handling red ball shots
def test_handle_red_ball_player_1():
    game = SnookerScores()

    game.handle_red_ball(1)
    assert game.red_balls == 14
    assert game.available_player_1 == 146
    assert game.available_player_2 == 139
    assert game.score_player_1 == 1

def test_handle_red_ball_player_2():
    game = SnookerScores()

    game.switch_players()
    game.handle_red_ball(1)
    assert game.red_balls == 14
    assert game.available_player_2 == 146
    assert game.available_player_1 == 139
    assert game.score_player_2 == 1

# Handling colored ball shots
def test_handle_color_ball_player_1():
    game = SnookerScores()

    game.handle_red_ball(1)
    game.handle_color_ball(5)
    assert game.score_player_1 == 6
    assert game.available_player_1 == 139

def test_handle_color_ball_player_2():
    game = SnookerScores()

    game.switch_players()
    game.handle_red_ball(1)
    game.handle_color_ball(4)
    assert game.score_player_2 == 5
    assert game.available_player_2 == 139

# Handling other game events
def test_handle_miss():
    game = SnookerScores()
    
    game.handle_red_ball(1)
    game.handle_color_ball(5)
    
    game.handle_miss()
    assert game.available_player_1 == 139
    assert game.available_player_2 == 139

def test_handle_last_colored_ball():
    game = SnookerScores()
    
    game.red_balls = 0
    game.available_player_1 = 27
    game.available_player_2 = 27
    
    game.switch_players()
    with mock_input("What's the value of the shot: ", "2"):
        game.handle_last_colored_ball()
    
    assert game.available_player_1 == 27
    assert game.available_player_2 == 27

# Game conclusion
def test_display_winner():
    game = SnookerScores()
    
    game.score_player_1 = 50
    game.score_player_2 = 40
    
    with patch('builtins.print') as mock_print:
        game.display_winner()
        mock_print.assert_called_with("\nPlayer 1 wins!")
