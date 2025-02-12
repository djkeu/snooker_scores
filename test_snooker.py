import pytest
from unittest.mock import patch
from snooker import SnookerScores


def test_initial_state():
    """Test the initial state of the SnookerScores class."""
    game = SnookerScores()
    assert game.red_needed_next is True
    assert game.player_1_turn is True
    assert game.score_player_1 == 0
    assert game.score_player_2 == 0
    assert game.possible_score_player_1 == 147
    assert game.possible_score_player_2 == 147
    assert game.color_needed == 2
    assert game.colored_balls == {
        2: "yellow",
        3: "green",
        4: "brown",
        5: "blue",
        6: "pink",
        7: "black",
    }
    assert game.first_input is True


def test_get_shot_value_quit():
    """Test quitting the game using 'q'."""
    game = SnookerScores()
    with patch("builtins.input", side_effect=["q"]):
        with pytest.raises(SystemExit):
            game.get_shot_value()


def test_get_shot_value_set_starting_scores():
    """Test setting starting scores using 's'."""
    game = SnookerScores()
    with patch("builtins.input", side_effect=["s", "10", "20", "15", "q"]):
        with pytest.raises(SystemExit):
            game.get_shot_value()
        assert game.first_input is False


def test_update_score():
    """Test updating player scores."""
    game = SnookerScores()
    game.update_score(5)
    assert game.score_player_1 == 5
    game.switch_players()
    game.update_score(3)
    assert game.score_player_2 == 3


def test_switch_players():
    """Test switching turns between players."""
    game = SnookerScores()
    assert game.player_1_turn is True
    game.switch_players()
    assert game.player_1_turn is False
    game.switch_players()
    assert game.player_1_turn is True


def test_handle_red_ball():
    """Test handling a red ball."""
    game = SnookerScores()
    game.handle_red_ball(1)
    assert game.score_player_1 == 1
    assert game.red_balls == 14
    assert game.red_needed_next is False


def test_handle_red_ball_reduces_available():
    """Test that handle_red_ball reduces available points correctly."""
    game = SnookerScores()
    game.handle_red_ball(1)
    assert game.available == 146  # 147 - 1


def test_handle_color_ball():
    """Test handling a colored ball."""
    game = SnookerScores()
    game.red_needed_next = False
    game.handle_color_ball(2)
    assert game.score_player_1 == 2
    assert game.red_needed_next is True


def test_handle_color_ball_reduces_available():
    """Test that handle_color_ball reduces available points correctly."""
    game = SnookerScores()
    game.red_needed_next = False  # Simulate that a red ball was just potted
    game.handle_color_ball(2)
    assert game.available == 140  # 147 - 7


def test_handle_miss():
    """Test handling a missed shot."""
    game = SnookerScores()
    game.handle_miss()
    assert game.red_needed_next is True
    assert game.player_1_turn is False


def test_calculate_possible_scores():
    """Test calculating possible scores."""
    game = SnookerScores()
    game.score_player_1 = 10
    game.score_player_2 = 20
    game.calculate_possible_scores()
    assert game.possible_score_player_1 == 157
    assert game.possible_score_player_2 == 167


def test_set_starting_scores_valid():
    """Test setting valid starting scores."""
    game = SnookerScores()
    with patch("builtins.input", side_effect=["10", "20", "15"]):
        game.set_starting_scores()
        assert game.score_player_1 == 20
        assert game.score_player_2 == 15
        assert game.red_balls == 10
        assert game.available == 112  # 147 - (20 + 15)


def test_set_starting_scores_invalid():
    """Test setting invalid starting scores."""
    game = SnookerScores()
    with patch("builtins.input", side_effect=["16", "20", "15"]):
        with patch("builtins.print") as mocked_print:
            game.set_starting_scores()
            mocked_print.assert_called_with(
                "Invalid input. "
                "Scores cannot be negative, "
                "and red balls must be between 0 and 15."
            )


def test_red_balls_phase():
    """Test the red balls phase."""
    game = SnookerScores()
    with patch("builtins.input", side_effect=["1", "2"] * 14 + ["1", "5"]):
        # (14 * 1) + (14 * 2), 1 + 5 (last blue)
        with patch("builtins.print") as mocked_print:
            game.red_balls_phase()
            assert game.red_balls == 0
            assert game.score_player_1 == 48
            # (15 * 1) + (14 * 2) + 5 (last blue ball)
            assert game.available == 29
            # 147 - (15 * 1) - (14 * 7) - 5 (last blue ball)
            mocked_print.assert_any_call(
                "\nNo more red balls left! "
                "Pot a colored ball to start the endgame."
            )


def test_colored_balls_phase():
    """Test the colored balls phase."""
    game = SnookerScores()
    game.red_balls = 0
    game.available = 27
    game.score_player_1 = 0  # Reset player scores
    game.score_player_2 = 0  # Reset player scores
    game.color_needed = 2  # Start with the yellow ball

    with patch("builtins.input", side_effect=["2", "3", "4", "5", "6", "7"]):
        with patch("builtins.print") as mocked_print:
            game.colored_balls_phase()
            assert game.score_player_1 == 27  # Player 1 pots all colored balls
            assert game.score_player_2 == 0   # Player 2 does not score
            assert game.available == 0        # All points have been potted
            assert game.color_needed == 8
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
