import sys
import pytest
from unittest.mock import patch, MagicMock
from src.snooker_game import SnookerGame
from src.snooker_gui import SnookerGUI
sys.path.append("../")


def create_mock_root():
    """Create a mock root object for the SnookerGUI."""
    return MagicMock()


def test_handle_red_ball():
    """Test handling a red ball."""
    root = create_mock_root()
    game = SnookerGUI(root)
    game.game.handle_red_ball(1)
    assert game.game.score_player_1 == 1
    assert game.game.red_balls == 14
    assert game.game.red_needed_next is False


def test_handle_red_ball_reduces_available_points():
    """Test that handle_red_ball reduces available points correctly."""
    root = create_mock_root()
    game = SnookerGUI(root)
    game.game.handle_red_ball(1)
    assert game.game.available_points == 146


def test_handle_color_ball():
    """Test handling a colored ball."""
    root = create_mock_root()
    game = SnookerGUI(root)
    game.game.red_needed_next = False
    game.game.handle_color_ball(2)
    assert game.game.score_player_1 == 2
    assert game.game.red_needed_next is True


def test_handle_color_ball_reduces_available_points():
    """Test that handle_color_ball reduces available points correctly."""
    root = create_mock_root()
    game = SnookerGUI(root)
    game.game.red_balls = 13
    game.game.available_points = 138  # 147 - 1 - 7 - 1
    game.game.red_needed_next = False
    game.game.handle_color_ball(3)  # green ball
    assert game.game.available_points == 131  # 138 - 7


def test_handle_miss():
    """Test handling a missed shot."""
    root = create_mock_root()
    game = SnookerGUI(root)
    game.game.handle_miss()
    assert game.game.red_needed_next is True
    assert game.game.player_1_turn is False


if __name__ == "__main__":
    pytest.main()
