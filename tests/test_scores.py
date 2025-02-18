import sys
import pytest
from unittest.mock import patch, MagicMock
from src.snooker_game import SnookerGame
from src.snooker_gui import SnookerGUI
sys.path.append("../")


def create_mock_root():
    """Create a mock root object for the SnookerGUI."""
    return MagicMock()


def test_update_score():
    """Test updating player scores."""
    root = create_mock_root()
    game = SnookerGUI(root)
    game.game.update_score(5)
    assert game.game.score_player_1 == 5
    game.game.switch_players()
    game.game.update_score(3)
    assert game.game.score_player_2 == 3


def test_calculate_possible_scores_player_1_turn_red_needed_next():
    """Test possible scores when it's Player 1's turn and a red ball is needed next."""
    game = SnookerGame()
    game.player_1_turn = True
    game.red_needed_next = True
    game.score_player_1 = 10
    game.score_player_2 = 20
    game.available_points = 100

    game.calculate_possible_scores()

    assert game.possible_score_player_1 == 110  # 10 + 100
    assert game.possible_score_player_2 == 120  # 20 + 100


def test_calculate_possible_scores_player_1_turn_colored_needed_next():
    """Test possible scores when it's Player 1's turn and a colored ball is needed next."""
    game = SnookerGame()
    game.player_1_turn = True
    game.red_needed_next = False
    game.score_player_1 = 10
    game.score_player_2 = 20
    game.available_points = 100

    game.calculate_possible_scores()

    assert game.possible_score_player_1 == 110  # 10 + 100
    assert game.possible_score_player_2 == 113  # 20 + 100 - 7


def test_calculate_possible_scores_player_2_turn_red_needed_next():
    """Test possible scores when it's Player 2's turn and a red ball is needed next."""
    game = SnookerGame()
    game.player_1_turn = False
    game.red_needed_next = True
    game.score_player_1 = 10
    game.score_player_2 = 20
    game.available_points = 100

    game.calculate_possible_scores()

    assert game.possible_score_player_1 == 110  # 10 + 100
    assert game.possible_score_player_2 == 120  # 20 + 100


def test_calculate_possible_scores_player_2_turn_colored_needed_next():
    """Test possible scores when it's Player 2's turn and a colored ball is needed next."""
    game = SnookerGame()
    game.player_1_turn = False
    game.red_needed_next = False
    game.score_player_1 = 10
    game.score_player_2 = 20
    game.available_points = 100

    game.calculate_possible_scores()

    assert game.possible_score_player_1 == 103  # 10 + 100 - 7
    assert game.possible_score_player_2 == 120  # 20 + 100


def test_calculate_possible_scores_edge_case_zero_available_points():
    """Test possible scores when available_points is 0."""
    game = SnookerGame()
    game.player_1_turn = True
    game.red_needed_next = False
    game.score_player_1 = 10
    game.score_player_2 = 20
    game.available_points = 0

    game.calculate_possible_scores()

    assert game.possible_score_player_1 == 10  # 10 + 0
    assert game.possible_score_player_2 == 13  # 20 + 0 - 7


def test_calculate_possible_scores_edge_case_negative_scores():
    """Test possible scores when scores are negative."""
    game = SnookerGame()
    game.player_1_turn = False
    game.red_needed_next = False
    game.score_player_1 = -10
    game.score_player_2 = -20
    game.available_points = 100

    game.calculate_possible_scores()

    assert game.possible_score_player_1 == 83  # -10 + 100 - 7
    assert game.possible_score_player_2 == 80  # -20 + 100


def test_add_penalty():
    root = create_mock_root()
    game = SnookerGUI(root)

    with patch('builtins.input', side_effect=['4', 'n']):
        game.game.player_1_turn = True
        game.game.add_penalty(4)
        assert game.game.score_player_2 == 4
        assert game.game.player_1_turn is False

    # Input out of range
    with patch('builtins.input', side_effect=['8', '4', 'n']):
        game.game.player_1_turn = False
        game.game.add_penalty(4)
        assert game.game.score_player_1 == 4
        assert game.game.player_1_turn is True

    # Non-numeric input
    with patch('builtins.input', side_effect=['a', '3', 'n']):
        game.game.player_1_turn = True
        game.game.add_penalty(3)
        assert game.game.score_player_2 == 7
        assert game.game.player_1_turn is False

    # Respot balls with 'y'
    with patch('builtins.input', side_effect=['3', 'y']):
        game.game.player_1_turn = False
        game.game.add_penalty(3)
        assert game.game.score_player_1 == 7
        assert game.game.player_1_turn is False

    # Respot balls with 'n'
    with patch('builtins.input', side_effect=['3', 'n']):
        game.game.player_1_turn = True
        game.game.add_penalty(3)
        assert game.game.score_player_2 == 10
        assert game.game.red_needed_next is True


if __name__ == "__main__":
    pytest.main()
