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
def test_handle_ball_red():
    """Test the handle_ball method when a red ball is potted."""
    game = SnookerScores()
    
    # Initial state
    assert game.red_balls == 15
    assert game.score_player_1 == 0
    assert game.score_player_2 == 0
    assert game.red_needed_next == True

    # Player 1 pots a red ball
    game.handle_ball(1, is_red_ball=True)
    
    # Verify state after potting a red ball
    assert game.red_balls == 14  # One red ball removed
    assert game.score_player_1 == 1  # Player 1 gains 1 point
    assert game.red_needed_next == False  # Next shot must be a colored ball

    # Player 2 pots a red ball
    game.switch_players()
    game.handle_ball(1, is_red_ball=True)
    
    # Verify state after Player 2 pots a red ball
    assert game.red_balls == 13  # Another red ball removed
    assert game.score_player_2 == 1  # Player 2 gains 1 point
    assert game.red_needed_next == False  # Next shot must be a colored ball

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
def test_handle_ball_color():
    """Test the handle_ball method when a colored ball is potted."""
    game = SnookerScores()
    
    # Initial state
    assert game.red_balls == 15
    assert game.score_player_1 == 0
    assert game.score_player_2 == 0
    assert game.red_needed_next == True

    # Player 1 pots a red ball first (required before potting a color)
    game.handle_ball(1, is_red_ball=True)
    
    # Player 1 pots a colored ball (e.g., black ball, value 7)
    game.handle_ball(7, is_red_ball=False)
    
    # Verify state after potting a colored ball
    assert game.red_balls == 14  # Red ball count remains the same
    assert game.score_player_1 == 8  # Player 1 gains 1 (red) + 7 (black)
    assert game.red_needed_next == True  # Next shot must be a red ball

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
        mock_print.assert_called_with(
            "\nPlayer 1 wins with a score of 50!"
        )
