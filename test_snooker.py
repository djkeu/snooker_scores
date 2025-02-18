import sys
import pytest
from unittest.mock import patch, MagicMock
from snooker_gui import SnookerGUI
from snooker_game import SnookerGame
sys.path.append("../")


def create_mock_root():
    """Create a mock root object for the SnookerGUI."""
    return MagicMock()
