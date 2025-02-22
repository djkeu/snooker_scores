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

def test_start_game_early_exit(capsys):
    game = SnookerScores()
    with patch("builtins.input", side_effect=["q"]):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "q: quit, s: set starting scores, x: switch player, p: penalty" in captured.out

def test_start_game_penalty(capsys):
    game = SnookerScores()
    with patch("builtins.input", side_effect=["p", "5", "n", "q"]):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Penalty of 5 points applied to Player 1." in captured.out

def test_start_game_switch_players(capsys):
    game = SnookerScores()
    with patch("builtins.input", side_effect=["x", "q"]):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Switching players..." in captured.out

def test_start_game_set_scores(capsys):
    game = SnookerScores()
    with patch("builtins.input", side_effect=["s", "15", "0", "0", "q"]):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Player 1: score 0, potential score 147" in captured.out
    assert "Player 2: score 0, potential score 147" in captured.out
    assert "15 red balls left" in captured.out

def test_start_game_invalid_inputs(capsys):
    game = SnookerScores()
    with patch("builtins.input", side_effect=["invalid", "q"]):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Only numbers between 0 and 7 are valid!" in captured.out

def test_start_game_multiple_invalid_inputs(capsys):
    game = SnookerScores()
    with patch("builtins.input", side_effect=["invalid", "invalid", "q"]):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Only numbers between 0 and 7 are valid!" in captured.out

def test_start_game_penalty_respot(capsys):
    game = SnookerScores()
    with patch("builtins.input", side_effect=["p", "5", "y", "q"]):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Penalty of 5 points applied to Player 1." in captured.out
    assert "Switching players..." in captured.out

def test_start_game_penalty_no_respot(capsys):
    game = SnookerScores()
    with patch("builtins.input", side_effect=["p", "5", "n", "q"]):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Penalty of 5 points applied to Player 1." in captured.out


def test_game_flow():
    game = SnookerScores()
    
    with patch('builtins.input', side_effect=[1, 5, 2, 4, 1, 3, 'q']):
        with pytest.raises(SystemExit):
            game.red_balls_phase()
            game.colored_balls_phase()  # Note: this phase is not reached
