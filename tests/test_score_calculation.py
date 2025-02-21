import pytest
from unittest.mock import patch
from snooker_scores import SnookerScores


def mock_input(prompt, value):
    return patch('builtins.input', return_value=value)


def test_apply_penalty():
    game = SnookerScores()
    game.score_player_1 = 50
    game.score_player_2 = 40
    game.apply_penalty(5)
    
    # Verify the penalty was applied correctly
    assert game.score_player_1 == 45  # Player 1 is penalized
    assert game.score_player_2 == 40  # Player 2's score should remain the same

def test_add_penalty_valid():
    with patch('builtins.input', side_effect=['5', 'n']):  # Simulating valid penalty input and no respot
        game = SnookerScores()
        game.score_player_1 = 50
        game.score_player_2 = 40
        game.add_penalty()
    
    # Ensure the correct penalty was applied to player 1
    assert game.score_player_1 == 45  # Player 1 is penalized by 5

def test_add_penalty_invalid():
    with patch('builtins.input', side_effect=['-1', '5', 'y']):  # Simulating invalid penalty input, followed by valid input
        game = SnookerScores()
        game.score_player_1 = 50
        game.score_player_2 = 40
        game.add_penalty()

    # Ensure the penalty was correctly applied
    assert game.score_player_2 == 35  # Player 2 is penalized by 5
