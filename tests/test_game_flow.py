import pytest
from unittest.mock import patch
from snooker_scores import SnookerScores


def mock_input(prompt, value):
    return patch('builtins.input', return_value=value)


def test_game_flow():
    game = SnookerScores()
    
    with patch('builtins.input', side_effect=[1, 5, 2, 4, 1, 3, 'q']):
        with pytest.raises(SystemExit):
            game.red_balls_phase()
            game.colored_balls_phase()  # Note: this phase is not reached
