import pytest
from unittest.mock import patch, MagicMock
from snooker_gui import SnookerGUI
from snooker_game import SnookerGame


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
