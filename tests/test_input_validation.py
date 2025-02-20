import pytest
from unittest.mock import patch
from snooker_scores import SnookerScores


@pytest.fixture
def snooker_game():
    return SnookerScores()

def test_validate_shot_valid(snooker_game):
    assert snooker_game.validate_shot("0") is True
    assert snooker_game.validate_shot("7") is True

def test_validate_shot_invalid(snooker_game):
    assert snooker_game.validate_shot("-1") is False
    assert snooker_game.validate_shot("8") is False
    assert snooker_game.validate_shot("100") is False
    assert snooker_game.validate_shot("abc") is False
    assert snooker_game.validate_shot("!") is False
    assert snooker_game.validate_shot("") is False

@patch("sys.exit")
def test_validate_shot_quit(mock_exit, snooker_game):
    # Mock user input with "q" to trigger quitting
    with patch("builtins.input", return_value="q"):
        mock_exit.side_effect = SystemExit  # Ensure SystemExit is raised from sys.exit()
        with pytest.raises(SystemExit):  # Expecting a SystemExit to be raised
            snooker_game.get_shot_value()

def test_validate_shot_s(snooker_game):
    snooker_game.first_input = True
    with patch("builtins.input", side_effect=["s", "1"]):
        assert snooker_game.get_shot_value() == 1
    assert snooker_game.first_input is False

def test_validate_shot_p(snooker_game):
    with patch.object(snooker_game, "add_penalty") as mock_penalty:
        with patch("builtins.input", side_effect=["p", "1"]):
            assert snooker_game.get_shot_value() == 1
        mock_penalty.assert_called_once()

def test_validate_shot_x(snooker_game):
    initial_turn = snooker_game.player_1_turn
    with patch.object(snooker_game, "switch_players", side_effect=snooker_game.switch_players) as mock_switch:
        with patch("builtins.input", side_effect=["x", "1"]):
            assert snooker_game.get_shot_value() == 1
        mock_switch.assert_called_once()
    assert snooker_game.player_1_turn != initial_turn  # Ensure player turn changed
