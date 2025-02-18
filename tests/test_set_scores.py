import sys
import pytest
from unittest.mock import patch, MagicMock
from src.snooker_game import SnookerGame
from src.snooker_gui import SnookerGUI
sys.path.append("../")


def create_mock_root():
    """Create a mock root object for the SnookerGUI."""
    return MagicMock()


def test_set_starting_scores_valid_input():
    """Test valid input for set_starting_scores."""
    root = create_mock_root()
    game = SnookerGUI(root)

    with patch('builtins.input', side_effect=["3", "50", "60"]):
        game.game.set_starting_scores(3, 50, 60)

    assert game.game.red_balls == 3
    assert game.game.score_player_1 == 50
    assert game.game.score_player_2 == 60
    assert game.game.available_points == game.game.red_balls * 8 + 27


def test_set_starting_scores_negative_scores():
    """Test negative scores input."""
    root = create_mock_root()
    game = SnookerGUI(root)

    with patch('builtins.input', side_effect=["3", "-10", "20", "3", "50", "60"]):
        game.game.set_starting_scores(3, 50, 60)

    assert game.game.red_balls == 3
    assert game.game.score_player_1 == 50
    assert game.game.score_player_2 == 60
    assert game.game.available_points == game.game.red_balls * 8 + 27


def test_set_starting_scores_total_score_exceeds_147():
    """Test total score exceeding 147."""
    root = create_mock_root()
    game = SnookerGUI(root)

    with patch('builtins.input', side_effect=["3", "100", "50", "3", "50", "60"]):
        game.game.set_starting_scores(3, 50, 60)

    assert game.game.red_balls == 3
    assert game.game.score_player_1 == 50
    assert game.game.score_player_2 == 60
    assert game.game.available_points == game.game.red_balls * 8 + 27


def test_set_starting_scores_invalid_red_balls():
    """Test invalid number of red balls."""
    root = create_mock_root()
    game = SnookerGUI(root)

    # Mock the StartingScoresDialog to simulate invalid input
    with patch('snooker_gui.StartingScoresDialog') as mock_dialog:
        # Mock the show method to return invalid input (20 red balls)
        mock_dialog.return_value.show.return_value = (20, 50, 60)

        # Mock messagebox.showerror to verify the error message
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            # Call the set_starting_scores method
            game.set_starting_scores()

            # Verify that messagebox.showerror was called with the correct arguments
            mock_showerror.assert_called_once_with(
                "Invalid Input", "Number of red balls must be between 0 and 15."
            )


def test_set_starting_scores_non_numeric_input():
    """Test non-numeric input."""
    root = create_mock_root()
    game = SnookerGUI(root)

    with patch('builtins.input', side_effect=["abc", "3", "50", "60"]):
        game.game.set_starting_scores(3, 50, 60)

    assert game.game.red_balls == 3
    assert game.game.score_player_1 == 50
    assert game.game.score_player_2 == 60
    assert game.game.available_points == game.game.red_balls * 8 + 27


if __name__ == "__main__":
    pytest.main()
