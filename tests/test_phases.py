import sys
import pytest
from unittest.mock import patch, MagicMock
from snooker_gui import SnookerGUI
from snooker_game import SnookerGame
sys.path.append("../")


def create_mock_root():
    """Create a mock root object for the SnookerGUI."""
    return MagicMock()


def test_red_balls_phase():
    """Test the red balls phase."""
    root = create_mock_root()
    game = SnookerGUI(root)
    with patch("builtins.input", side_effect=["1", "2"] * 14 + ["1", "5"]):
        # (14 * 1) + (14 * 2) + 1 + 5 (last blue)
        with patch("builtins.print") as mocked_print:
            game.game.red_balls_phase(1)
            assert game.game.red_balls == 0
            assert game.game.score_player_1 == 48
            assert game.game.available_points == 29
            # 147 - (15) - (98) - 5 (last blue ball)
            mocked_print.assert_any_call(
                "\nNo more red balls left! "
                "Pot a colored ball to start the endgame."
            )


def test_colored_balls_phase():
    """Test the colored balls phase."""
    root = create_mock_root()
    game = SnookerGUI(root)
    game.game.red_balls = 0
    game.game.available_points = 27
    game.game.score_player_1 = 0
    game.game.score_player_2 = 0
    game.game.yellow_ball = 2

    with patch("builtins.input", side_effect=["2", "3", "4", "5", "6", "7"]):
        with patch("builtins.print") as mocked_print:
            game.game.colored_balls_phase(2)
            assert game.game.score_player_1 == 27
            assert game.game.score_player_2 == 0
            assert game.game.available_points == 0
            assert game.game.yellow_ball == 8
            mocked_print.assert_any_call("\nEntering colored balls endgame!\n")
            mocked_print.assert_any_call("Available for endgame: 27")
            mocked_print.assert_any_call("Next ball to pot: yellow (2 points)")
            mocked_print.assert_any_call("Next ball to pot: green (3 points)")
            mocked_print.assert_any_call("Next ball to pot: brown (4 points)")
            mocked_print.assert_any_call("Next ball to pot: blue (5 points)")
            mocked_print.assert_any_call("Next ball to pot: pink (6 points)")
            mocked_print.assert_any_call("Next ball to pot: black (7 points)")
            mocked_print.assert_any_call("\nNo more balls to play!")


if __name__ == "__main__":
    pytest.main()
