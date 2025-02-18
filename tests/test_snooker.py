import sys
import pytest
from unittest.mock import patch, MagicMock
from src.snooker_game import SnookerGame
from src.snooker_gui import SnookerGUI
sys.path.append("../")


def create_mock_root():
    """Create a mock root object for the SnookerGUI."""
    return MagicMock()
