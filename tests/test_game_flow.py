import pytest
from unittest.mock import patch
from snooker_scores import SnookerScores
from io import StringIO
import sys


def mock_input(prompt, value):
    return patch('builtins.input', return_value=value)


def test_start_game(capsys):
    game = SnookerScores()

    inputs = [
        "15", "0", "0",
        *(["1", "7"] * 13), "0",
        *(["1", "7"] * 2), "0",
        "2", "3", "4", "5", "6", "7", "0",
    ]

    with patch.object(game, "display_startup_message", return_value=None):
        with patch("builtins.input", side_effect=inputs):
            game.start_game()

    captured = capsys.readouterr()
    output = captured.out

    assert "Player 1 must pot a red ball next" in output
    assert "Player 1 must pot a colored ball next" in output
    assert "Player 2 must pot a red ball next" in output
    assert "Player 2 must pot a colored ball next" in output
    assert "Next ball to pot: yellow" in output
    assert "Next ball to pot: black" in output
    assert "wins with a score of" in output

def test_game_flow():
    game = SnookerScores()
    
    with patch('builtins.input', side_effect=[1, 5, 2, 4, 1, 3, 'q']):
        with pytest.raises(SystemExit):
            game.red_balls_phase()
            game.colored_balls_phase()  # Note: this phase is not reached
