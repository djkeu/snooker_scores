import pytest
from unittest.mock import patch
from snooker_scores import SnookerScores
from io import StringIO
import sys


VALID_INPUTS = ["1", "2", "3", "4", "5", "6", "7"]
INVALID_INPUTS = ["invalid", "-1", "8"]
PENALTY_VALUES = ["4", "5", "6", "7"]
QUIT_INPUT = "q"
SET_SCORES_INPUT = "s"
SWITCH_PLAYER_INPUT = "x"
PENALTY_INPUT = "p"


def mock_input(prompt, value):
    return patch('builtins.input', return_value=value)

def generate_inputs(*sequences):
    return [str(item) for sequence in sequences for item in sequence]


def test_start_game_full_flow(capsys):
    game = SnookerScores()

    inputs = generate_inputs(
        ["15", "0", "0"],  # Starting scores
        [VALID_INPUTS[0], VALID_INPUTS[6]] * 13,  # Red and colored ball phase (13 reds)
        ["0"],  # End of red ball phase
        [VALID_INPUTS[0], VALID_INPUTS[6]] * 2,  # Final colored balls (2 reds left)
        ["0"],  # End of game
        VALID_INPUTS[1:] + ["0"]  # Colored ball phase
    )

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
    assert "15 red balls left" in output
    assert "0 red balls left" in output
    assert "Player 1: score" in output
    assert "Player 2: score" in output

def test_start_game_early_exit(capsys):
    game = SnookerScores()
    inputs = generate_inputs([QUIT_INPUT])
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "q: quit, s: set starting scores, x: switch player, p: penalty" in captured.out

def test_start_game_penalty(capsys):
    game = SnookerScores()
    inputs = generate_inputs([PENALTY_INPUT, PENALTY_VALUES[1], "n", QUIT_INPUT])
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Penalty of 5 points applied to Player 1." in captured.out

def test_start_game_switch_players(capsys):
    game = SnookerScores()
    inputs = generate_inputs([SWITCH_PLAYER_INPUT, QUIT_INPUT])
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Switching players..." in captured.out

def test_start_game_set_scores(capsys):
    game = SnookerScores()
    inputs = generate_inputs([SET_SCORES_INPUT, "15", "0", "0", QUIT_INPUT])
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Player 1: score 0, potential score 147" in captured.out
    assert "Player 2: score 0, potential score 147" in captured.out
    assert "15 red balls left" in captured.out

def test_start_game_invalid_inputs(capsys):
    game = SnookerScores()
    inputs = generate_inputs([INVALID_INPUTS[0], QUIT_INPUT])
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Only numbers between 0 and 7 are valid!" in captured.out

def test_start_game_multiple_invalid_inputs(capsys):
    game = SnookerScores()
    inputs = generate_inputs([INVALID_INPUTS[0], INVALID_INPUTS[1], QUIT_INPUT])
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Only numbers between 0 and 7 are valid!" in captured.out

def test_start_game_penalty_respot(capsys):
    game = SnookerScores()
    inputs = generate_inputs([PENALTY_INPUT, PENALTY_VALUES[1], "y", QUIT_INPUT])
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Penalty of 5 points applied to Player 1." in captured.out
    assert "Switching players..." in captured.out

def test_start_game_penalty_no_respot(capsys):
    game = SnookerScores()
    inputs = generate_inputs([PENALTY_INPUT, PENALTY_VALUES[1], "n", QUIT_INPUT])
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Penalty of 5 points applied to Player 1." in captured.out


def test_game_flow():
    game = SnookerScores()
    inputs = generate_inputs([VALID_INPUTS[0], VALID_INPUTS[4], VALID_INPUTS[1], VALID_INPUTS[3], VALID_INPUTS[0], VALID_INPUTS[2], QUIT_INPUT])
    with patch('builtins.input', side_effect=inputs):
        with pytest.raises(SystemExit):
            game.red_balls_phase()
            game.colored_balls_phase()
