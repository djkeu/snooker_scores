import sys
import pytest
from unittest.mock import patch, MagicMock
from snooker_gui import SnookerGUI
from snooker_game import SnookerGame
sys.path.append("../")


def create_mock_root():
    """Create a mock root object for the SnookerGUI."""
    return MagicMock()


def test_initial_state():
    """Test the initial state of the SnookerGUI class."""
    root = create_mock_root()
    game = SnookerGUI(root)
    assert game.game.available_points == 147
    assert game.game.red_balls == 15
    assert game.game.red_needed_next is True
    assert game.game.player_1_turn is True
    assert game.game.score_player_1 == 0
    assert game.game.score_player_2 == 0
    assert game.game.possible_score_player_1 == 147
    assert game.game.possible_score_player_2 == 147
    assert game.game.yellow_ball == 2
    assert game.game.colored_balls == {
        2: "yellow",
        3: "green",
        4: "brown",
        5: "blue",
        6: "pink",
        7: "black",
    }
    assert game.game.prompt == "What's the value of the shot: "


def test_initialize_prompt():
    root = create_mock_root()
    game = SnookerGUI(root)

    expected_prompt = "What's the value of the shot: "
    assert game.game.initialize_prompt() == expected_prompt

    expected_prompt = "What's the value of the shot: "
    assert game.game.initialize_prompt() == expected_prompt
