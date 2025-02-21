import pytest
from unittest.mock import patch
from snooker_scores import SnookerScores


def mock_input(prompt, value):
    return patch('builtins.input', return_value=value)


def test_apply_penalty():
    game = SnookerScores()
    game.score_player_1 = 50
    game.score_player_2 = 40

    game.switch_players()  # After a missed or wrong ball
    game.apply_penalty(5)
    
    assert game.score_player_1 == 50
    assert game.score_player_2 == 45

def test_add_penalty_valid():
    with patch('builtins.input', side_effect=['5', 'n']):
        game = SnookerScores()
        game.score_player_1 = 50
        game.score_player_2 = 40

        game.switch_players()  # After a missed or wrong ball
        game.add_penalty()
    
    assert game.score_player_1 == 50

def test_add_penalty_invalid():
    with patch('builtins.input', side_effect=['-1', '5', 'y']):
        game = SnookerScores()
        game.score_player_1 = 50
        game.score_player_2 = 40

        game.switch_players()  # After a missed or wrong ball
        game.add_penalty()

    assert game.score_player_2 == 45
