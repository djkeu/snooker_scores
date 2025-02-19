import pytest
from unittest.mock import patch
from snooker_scores import SnookerScores


def mock_input(prompt, value):
    return patch('builtins.input', return_value=value)


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


def test_set_starting_scores_valid_input():
    with patch('builtins.input', side_effect=[16, 50, 60, 2, 50, 60]):
        game = SnookerScores()
        game.set_starting_scores()

    assert game.red_balls == 2
    assert game.score_player_1 == 50
    assert game.score_player_2 == 60
    assert game.available_player_1 == 43
    assert game.available_player_2 == 43

def test_set_starting_scores_invalid_input():
    with patch('builtins.input', side_effect=["15", "50", "60", "2", "50", "60"]):  
        game = SnookerScores()
        game.set_starting_scores()

    assert game.red_balls == 2
    assert game.score_player_1 == 50
    assert game.score_player_2 == 60
    assert game.available_player_1 == 43
    assert game.available_player_2 == 43
    
def test_add_penalty_valid_input():
    with patch('builtins.input', side_effect=['5', 'n']):
        game = SnookerScores()
        game.score_player_1 = 50
        game.score_player_2 = 40
        game.add_penalty()

    assert game.score_player_2 == 45
    assert game.score_player_1 == 50
    assert game.red_needed_next

def test_add_penalty_invalid_input():
    with patch('builtins.input', side_effect=["-1", "5", "y"]):
        game = SnookerScores()
        game.score_player_1 = 50
        game.score_player_2 = 40
        game.add_penalty()

    assert game.score_player_2 == 45
    assert game.red_needed_next


def test_display_winner():
    game = SnookerScores()
    
    game.score_player_1 = 50
    game.score_player_2 = 40
    
    with patch('builtins.print') as mock_print:
        game.display_winner()
        mock_print.assert_called_with("\nPlayer 1 wins!")

def test_game_flow():
    game = SnookerScores()
    
    with patch('builtins.input', side_effect=[1, 5, 2, 4, 1, 3, 'q']):
        with pytest.raises(SystemExit):
            game.red_balls_phase()
            game.colored_balls_phase()  # Note: this phase is not reached
