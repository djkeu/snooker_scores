import sys
import pytest
from unittest.mock import patch, MagicMock
from snooker_gui import SnookerGUI
from snooker_game import SnookerGame
sys.path.append("../")


def create_mock_root():
    """Create a mock root object for the SnookerGUI."""
    return MagicMock()


def test_get_shot_value_quit():
    """Test quitting the game using 'q'."""
    root = create_mock_root()
    game = SnookerGUI(root)
    with patch.object(game.root, 'quit') as mock_quit:
        game.entry_shot.get = MagicMock(return_value="q")
        game.submit_shot()
        mock_quit.assert_called_once()


def test_get_shot_value_invalid():
    """Test entering an invalid shot value."""
    root = create_mock_root()
    game = SnookerGUI(root)

    # Mock the entry widget to simulate invalid input
    with patch.object(game.entry_shot, 'get', return_value="8"):
        # Mock messagebox.showerror to verify the error message
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            # Call the submit_shot method
            game.submit_shot()

            # Verify that messagebox.showerror was called with the correct arguments
            mock_showerror.assert_called_once_with(
                "Invalid Input", "Only numbers between 0 and 7 are valid!"
            )


def test_get_shot_value_non_numeric():
    """Test entering a non-numeric shot value."""
    root = create_mock_root()
    game = SnookerGUI(root)

    # Mock the entry widget to simulate non-numeric input
    with patch.object(game.entry_shot, 'get', return_value="abc"):
        # Mock messagebox.showerror to verify the error message
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            # Call the submit_shot method
            game.submit_shot()

            # Verify that messagebox.showerror was called with the correct arguments
            mock_showerror.assert_called_once_with(
                "Invalid Input", "Only numbers between 0 and 7 are valid!"
            )
