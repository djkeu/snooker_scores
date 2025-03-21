import pytest
from unittest.mock import patch
from snooker_scores import SnookerScores


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


# diverse tests
def test_game_flow(capsys):
    game = SnookerScores()
    inputs = generate_inputs([VALID_INPUTS[0], VALID_INPUTS[4], VALID_INPUTS[1], VALID_INPUTS[3], VALID_INPUTS[0], VALID_INPUTS[2], QUIT_INPUT])
    with patch('builtins.input', side_effect=inputs):
        with pytest.raises(SystemExit):
            game.red_balls_phase()
            captured = capsys.readouterr()
            assert "15 red balls left" in captured.out
            game.colored_balls_phase()
            captured = capsys.readouterr()
            assert "Player 1 must pot a yellow ball" in captured.out

def test_multiple_penalties(capsys):
    game = SnookerScores()
    inputs = generate_inputs(
        ["n",
         PENALTY_INPUT, "4", "n",
         PENALTY_INPUT, "5", "y",
         QUIT_INPUT]
    )
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Penalty award of 4 points applied to Player 1." in captured.out
    assert "Penalty award of 5 points applied to Player 1." in captured.out
    assert "Player 1: score 4" in captured.out
    assert "Player 1: score 9" in captured.out
    assert "Switching players..." in captured.out
    assert "Active player: Player 2" in captured.out

def test_switch_players_red_ball_phase(capsys):
    game = SnookerScores()
    inputs = generate_inputs(
        ["n",
         SET_SCORES_INPUT, "15", "0", "0",
         "x",
         QUIT_INPUT]
    )

    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Switching players..." in captured.out


# start_game tests
def test_start_game_full_flow(capsys):
    game = SnookerScores()

    inputs = [
        "n",
        "s",
        "15", "0", "0",
        *[VALID_INPUTS[0], VALID_INPUTS[6]] * 13,
        "0",
        *[VALID_INPUTS[0], VALID_INPUTS[6]] * 2,
        "0",
        *VALID_INPUTS[1:],
        "0",
        "a",
        "n"
    ]

    with patch.object(game, "display_startup_message", return_value=None):
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.exit") as mock_exit:
                mock_exit.side_effect = SystemExit()
                with pytest.raises(SystemExit):
                    game.start_game()

    captured = capsys.readouterr()
    assert "Player 1 wins! (with a score of 131 vs 16)" in captured.out
    assert "Bye!" in captured.out
    assert "15 red balls left" in captured.out
    assert "Player 1 must pot a colored ball next" in captured.out
    assert "Player 1 must pot a yellow ball" in captured.out
    mock_exit.assert_called_once()


def test_start_game_early_exit(capsys):
    game = SnookerScores()
    inputs = generate_inputs(
        ["n",
         QUIT_INPUT]
    )
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "q: quit, s: set starting scores, x: switch player, p: penalty" in captured.out
    assert "Player 1: score 0, potential score 147" not in captured.out
    assert "Player 2: score 0, potential score 147" not in captured.out

def test_start_game_early_exit_red_ball_phase(capsys):
    game = SnookerScores()
    inputs = generate_inputs(["n", SET_SCORES_INPUT, "15", "0", "0", QUIT_INPUT])
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "q: quit, s: set starting scores, x: switch player, p: penalty" in captured.out
    assert "Player 1: score 0, potential score 147" in captured.out
    assert "Player 2: score 0, potential score 147" in captured.out
    assert "15 red balls left" in captured.out

def test_start_game_early_exit_set_starting_scores(capsys):
    game = SnookerScores()
    inputs = generate_inputs("n", [SET_SCORES_INPUT, "q", QUIT_INPUT])
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "q: quit, s: set starting scores, x: switch player, p: penalty" in captured.out
    assert "Ok, back to the game then." in captured.out
    assert "Player 1: score 0, potential score 147" not in captured.out
    assert "Player 2: score 0, potential score 147" not in captured.out

def test_start_game_exceed_max_red_balls_then_early_exit(capsys):
    game = SnookerScores()
    inputs = generate_inputs(
        ["n", SET_SCORES_INPUT, "16", "q", QUIT_INPUT]
    )
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Invalid number of red balls. It must be between 0 and 15." in captured.out
    assert "Player 1: score 0, potential score 147" not in captured.out
    assert "Player 2: score 0, potential score 147" not in captured.out

def test_start_game_invalid_inputs(capsys):
    game = SnookerScores()
    inputs = ["n", "invalid", "invalid", QUIT_INPUT]
    with patch.object(game, "display_startup_message", return_value=None):
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.exit") as mock_exit:
                mock_exit.side_effect = SystemExit()
                with pytest.raises(SystemExit):
                    game.start_game()
    captured = capsys.readouterr()
    assert "Only numbers between 0 and 7 are valid!" in captured.out
    assert "Player 1: score 0, potential score 147" not in captured.out
    assert "Player 2: score 0, potential score 147" not in captured.out

def test_start_game_multiple_invalid_inputs(capsys):
    game = SnookerScores()
    inputs = generate_inputs("n", [INVALID_INPUTS[0], INVALID_INPUTS[1], QUIT_INPUT])
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Only numbers between 0 and 7 are valid!" in captured.out
    assert "Player 1: score 0, potential score 147" not in captured.out
    assert "Player 2: score 0, potential score 147" not in captured.out

def test_start_game_invalid_red_balls_then_early_exit(capsys):
    game = SnookerScores()
    inputs = generate_inputs(
        ["n", SET_SCORES_INPUT, "invalid", "q", QUIT_INPUT]
    )
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Error: invalid literal for int() with base 10: 'invalid'. Please try again." in captured.out
    assert "Player 1: score 0, potential score 147" not in captured.out
    assert "Player 2: score 0, potential score 147" not in captured.out

def test_start_game_invalid_player_scores_then_early_exit(capsys):
    game = SnookerScores()
    inputs = generate_inputs(
        ["n", SET_SCORES_INPUT, "15", "invalid", "q", QUIT_INPUT]
    )
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Error: invalid literal for int() with base 10: 'invalid'. Please try again." in captured.out
    assert "Player 1: score 0, potential score 147" not in captured.out
    assert "Player 2: score 0, potential score 147" not in captured.out

def test_start_game_negative_player_scores_then_early_exit(capsys):
    game = SnookerScores()
    inputs = generate_inputs(
        ["n",
         SET_SCORES_INPUT, "15", "-10", "q", QUIT_INPUT]
    )
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Scores must be positive values." in captured.out
    assert "Player 1: score 0, potential score 147" not in captured.out
    assert "Player 2: score 0, potential score 147" not in captured.out

def test_start_game_penalty(capsys):
    game = SnookerScores()
    inputs = generate_inputs(
        ["n",
         PENALTY_INPUT, PENALTY_VALUES[1], "n",
         QUIT_INPUT]
    )
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Penalty award of 5 points applied to Player 1." in captured.out
    assert "Player 1: score 5" in captured.out
    assert "Player 2: score 0" in captured.out

def test_start_game_penalty_no_respot(capsys):
    game = SnookerScores()
    inputs = generate_inputs(
        ["n",
         PENALTY_INPUT, PENALTY_VALUES[1], "n", QUIT_INPUT]
    )
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Penalty award of 5 points applied to Player 1." in captured.out
    assert "Player 1: score 5" in captured.out
    assert "Player 2: score 0" in captured.out

def test_start_game_penalty_no_respot_edge_case(capsys):
    game = SnookerScores()
    inputs = generate_inputs(
        ["n",
         PENALTY_INPUT, "5", "n", QUIT_INPUT]
    )
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Penalty award of 5 points applied to Player 1." in captured.out
    assert "Player 1: score 5" in captured.out
    assert "Player 2: score 0" in captured.out

def test_start_game_penalty_respot(capsys):
    game = SnookerScores()
    inputs = generate_inputs(
        ["n",
         PENALTY_INPUT, PENALTY_VALUES[1], "y", QUIT_INPUT]
    )
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Penalty award of 5 points applied to Player 1." in captured.out
    assert "Player 1: score 5" in captured.out
    assert "Player 2: score 0" in captured.out
    assert "Switching players..." in captured.out

def test_start_game_penalty_respot_edge_case(capsys):
    game = SnookerScores()
    inputs = generate_inputs(
        ["n",
         PENALTY_INPUT, "5", "y", QUIT_INPUT]
    )
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Penalty award of 5 points applied to Player 1." in captured.out
    assert "Player 1: score 5" in captured.out
    assert "Player 2: score 0" in captured.out
    assert "Switching players..." in captured.out

def test_start_game_set_scores(capsys):
    game = SnookerScores()
    inputs = generate_inputs(
        "n",
        "s",
        [SET_SCORES_INPUT, "15", "0", "0",
        QUIT_INPUT]
    )
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Player 1: score 0, potential score 147" in captured.out
    assert "Player 2: score 0, potential score 147" in captured.out
    assert "15 red balls left" in captured.out

def test_start_game_switch_players(capsys):
    game = SnookerScores()
    inputs = generate_inputs(
        ["n",  # Do not enter player names
         SWITCH_PLAYER_INPUT, QUIT_INPUT]
    )
    with patch("builtins.input", side_effect=inputs):
        with pytest.raises(SystemExit):
            game.start_game()
    captured = capsys.readouterr()
    assert "Switching players..." in captured.out
