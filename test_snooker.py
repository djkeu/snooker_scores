import pytest
from unittest.mock import patch
from snooker_gui import SnookerGUI
from snooker_game import SnookerGame


def test_initial_state():
    """Test the initial state of the SnookerGUI class."""
    game = SnookerGUI()
    assert game.available_points == 147
    assert game.red_balls == 15
    assert game.red_needed_next is True
    assert game.player_1_turn is True
    assert game.score_player_1 == 0
    assert game.score_player_2 == 0
    assert game.possible_score_player_1 == 147
    assert game.possible_score_player_2 == 147
    assert game.yellow_ball == 2
    assert game.colored_balls == {
        2: "yellow",
        3: "green",
        4: "brown",
        5: "blue",
        6: "pink",
        7: "black",
    }
    assert game.first_input is True
    assert game.prompt == "What's the value of the shot: (enter 'q' to quit, 's' to set starting scores) "

# Ball handling
def test_initialize_prompt():
    snooker_scores = SnookerGUI()

    expected_prompt = "What's the value of the shot: (enter 'q' to quit, 's' to set starting scores) "
    assert snooker_scores.initialize_prompt() == expected_prompt

    snooker_scores.first_input = False
    expected_prompt = "What's the value of the shot: (enter 'q' to quit) "
    assert snooker_scores.initialize_prompt() == expected_prompt

def test_get_shot_value_quit():
    """Test quitting the game using 'q'."""
    game = SnookerGUI()
    with patch("builtins.input", side_effect=["q"]):
        with pytest.raises(SystemExit):
            game.get_shot_value()

def test_get_shot_value_set_starting_scores():
    """Test setting starting scores using 's'."""
    game = SnookerGUI()
    with patch("builtins.input", side_effect=["s", "10", "20", "15", "q"]):
        with pytest.raises(SystemExit):
            game.get_shot_value()
        assert game.first_input is False

def test_get_shot_value_invalid():
    """Test entering an invalid shot value."""
    game = SnookerGUI()
    with patch("builtins.input", side_effect=["8", "q"]):
        with patch("builtins.print") as mocked_print:
            with pytest.raises(SystemExit):
                game.get_shot_value()
            mocked_print.assert_any_call(
                "\nOnly numbers between 0 and 7 are valid!"
            )

def test_get_shot_value_non_numeric():
    """Test entering a non-numeric shot value."""
    game = SnookerGUI()
    with patch("builtins.input", side_effect=["abc", "q"]):
        with patch("builtins.print") as mocked_print:
            with pytest.raises(SystemExit):
                game.get_shot_value()
            mocked_print.assert_any_call(
                "\nOnly numbers between 0 and 7 are valid!"
            )

def test_handle_red_ball():
    """Test handling a red ball."""
    game = SnookerGUI()
    game.handle_red_ball(1)
    assert game.score_player_1 == 1
    assert game.red_balls == 14
    assert game.red_needed_next is False

def test_handle_red_ball_reduces_available_points():
    """Test that handle_red_ball reduces available points correctly."""
    game = SnookerGUI()
    game.handle_red_ball(1)
    assert game.available_points == 146

def test_handle_color_ball():
    """Test handling a colored ball."""
    game = SnookerGUI()
    game.red_needed_next = False
    game.handle_color_ball(2)
    assert game.score_player_1 == 2
    assert game.red_needed_next is True

def test_handle_color_ball_reduces_available_points():
    """Test that handle_color_ball reduces available points correctly."""
    game = SnookerGUI()
    game.red_balls = 13
    game.available_points = 138  # 147 - 1 - 7 - 1
    game.red_needed_next = False
    game.handle_color_ball(3)  # green ball
    assert game.available_points == 131  # 138 - 7

def test_handle_miss():
    """Test handling a missed shot."""
    game = SnookerGUI()
    game.handle_miss()
    assert game.red_needed_next is True
    assert game.player_1_turn is False


# Score handling
def test_update_score():
    """Test updating player scores."""
    game = SnookerGUI()
    game.update_score(5)
    assert game.score_player_1 == 5
    game.switch_players()
    game.update_score(3)
    assert game.score_player_2 == 3

def test_switch_players():
    """Test switching turns between players."""
    game = SnookerGUI()
    assert game.player_1_turn is True
    game.switch_players()
    assert game.player_1_turn is False
    game.switch_players()
    assert game.player_1_turn is True

def test_calculate_possible_scores():
    """Test calculating possible scores."""
    game = SnookerGUI()
    game.score_player_1 = 10
    game.score_player_2 = 20
    game.available_points = 117
    game.calculate_possible_scores()
    assert game.possible_score_player_1 == 127
    assert game.possible_score_player_2 == 137

def test_set_starting_scores_valid_input():
    """Test valid input for set_starting_scores."""
    game = SnookerGUI()

    with patch('builtins.input', side_effect=["3", "50", "60"]):
        game.set_starting_scores()

    assert game.red_balls == 3
    assert game.score_player_1 == 50
    assert game.score_player_2 == 60
    assert game.available_points == game.red_balls * 8 + 27

def test_set_starting_scores_negative_scores():
    """Test negative scores input."""
    game = SnookerGUI()

    with patch('builtins.input', side_effect=["3", "-10", "20", "3", "50", "60"]):
        game.set_starting_scores()

    assert game.red_balls == 3
    assert game.score_player_1 == 50
    assert game.score_player_2 == 60
    assert game.available_points == game.red_balls * 8 + 27

def test_set_starting_scores_total_score_exceeds_147():
    """Test total score exceeding 147."""
    game = SnookerGUI()

    with patch('builtins.input', side_effect=["3", "100", "50", "3", "50", "60"]):
        game.set_starting_scores()

    assert game.red_balls == 3
    assert game.score_player_1 == 50
    assert game.score_player_2 == 60
    assert game.available_points == game.red_balls * 8 + 27

def test_set_starting_scores_invalid_red_balls():
    """Test invalid number of red balls."""
    game = SnookerGUI()

    with patch('builtins.input', side_effect=["20", "3", "50", "3", "50", "60"]):
        with patch('builtins.print') as mocked_print:
            game.set_starting_scores()

    mocked_print.assert_any_call("\nNumber of red balls must be between 0 and 15.")
    assert game.red_balls == 3
    assert game.score_player_1 == 50
    assert game.score_player_2 == 60
    assert game.available_points == game.red_balls * 8 + 27

def test_set_starting_scores_non_numeric_input():
    """Test non-numeric input."""
    game = SnookerGUI()

    with patch('builtins.input', side_effect=["abc", "3", "50", "60"]):
        game.set_starting_scores()

    assert game.red_balls == 3
    assert game.score_player_1 == 50
    assert game.score_player_2 == 60
    assert game.available_points == game.red_balls * 8 + 27

def test_add_penalty():
    snooker_scores = SnookerGUI()

    with patch('builtins.input', side_effect=['4', 'n']):
        snooker_scores.player_1_turn = True
        snooker_scores.add_penalty()
        assert snooker_scores.score_player_2 == 4
        assert snooker_scores.player_1_turn is False

    # Input out of range
    with patch('builtins.input', side_effect=['8', '4', 'n']):
        snooker_scores.player_1_turn = False
        snooker_scores.add_penalty()
        assert snooker_scores.score_player_1 == 4
        assert snooker_scores.player_1_turn is True

    # Non-numeric input)
    with patch('builtins.input', side_effect=['a', '3', 'n']):
        snooker_scores.player_1_turn = True
        snooker_scores.add_penalty()
        assert snooker_scores.score_player_2 == 7
        assert snooker_scores.player_1_turn is False

    # Respot balls with 'y'
    with patch('builtins.input', side_effect=['3', 'y']):
        snooker_scores.player_1_turn = False
        snooker_scores.add_penalty()
        assert snooker_scores.score_player_1 == 7
        assert snooker_scores.player_1_turn is False

    # Respot balls with 'n'
    with patch('builtins.input', side_effect=['3', 'n']):
        snooker_scores.player_1_turn = True
        snooker_scores.add_penalty()
        assert snooker_scores.score_player_2 == 10
        assert snooker_scores.red_needed_next is True


# Game phases
def test_red_balls_phase():
    """Test the red balls phase."""
    game = SnookerGUI()
    with patch("builtins.input", side_effect=["1", "2"] * 14 + ["1", "5"]):
        # (14 * 1) + (14 * 2) + 1 + 5 (last blue)
        with patch("builtins.print") as mocked_print:
            game.red_balls_phase()
            assert game.red_balls == 0
            assert game.score_player_1 == 48
            assert game.available_points == 29
            # 147 - (15) - (98) - 5 (last blue ball)
            mocked_print.assert_any_call(
                "\nNo more red balls left! "
                "Pot a colored ball to start the endgame."
            )

def test_colored_balls_phase():
    """Test the colored balls phase."""
    game = SnookerGUI()
    game.red_balls = 0
    game.available_points = 27
    game.score_player_1 = 0
    game.score_player_2 = 0
    game.yellow_ball = 2

    with patch("builtins.input", side_effect=["2", "3", "4", "5", "6", "7"]):
        with patch("builtins.print") as mocked_print:
            game.colored_balls_phase()
            assert game.score_player_1 == 27
            assert game.score_player_2 == 0
            assert game.available_points == 0
            assert game.yellow_ball == 8
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
