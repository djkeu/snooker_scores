import pytest
from unittest.mock import patch
from snooker import SnookerScores


def test_initial_state():
    """Test the initial state of the SnookerScores class."""
    game = SnookerScores()
    assert game.available_points == 147
    assert game.red_balls == 15
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
    assert game.prompt == "What's the value of the shot: (enter 'q' to quit, 's' to set starting scores) "

# Ball handling
def test_initialize_prompt():
    snooker_scores = SnookerScores()
    
    expected_prompt = "What's the value of the shot: (enter 'q' to quit, 's' to set starting scores) "
    assert snooker_scores.initialize_prompt() == expected_prompt
    
    snooker_scores.first_input = False
    expected_prompt = "What's the value of the shot: (enter 'q' to quit) "
    assert snooker_scores.initialize_prompt() == expected_prompt


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


def test_get_shot_value_invalid():
    """Test entering an invalid shot value."""
    game = SnookerScores()
    with patch("builtins.input", side_effect=["8", "q"]):
        with patch("builtins.print") as mocked_print:
            with pytest.raises(SystemExit):
                game.get_shot_value()
            mocked_print.assert_any_call(
                "\nYou can't score 8 points with one shot!"
            )


def test_get_shot_value_non_numeric():
    """Test entering a non-numeric shot value."""
    game = SnookerScores()
    with patch("builtins.input", side_effect=["abc", "q"]):
        with patch("builtins.print") as mocked_print:
            with pytest.raises(SystemExit):
                game.get_shot_value()
            mocked_print.assert_any_call(
                "\nOnly numbers between 0 and 7 are valid!"
            )


def test_handle_red_ball():
    """Test handling a red ball."""
    game = SnookerScores()
    game.handle_red_ball(1)
    assert game.score_player_1 == 1
    assert game.red_balls == 14
    assert game.red_needed_next is False


def test_handle_red_ball_reduces_available_points():
    """Test that handle_red_ball reduces available points correctly."""
    game = SnookerScores()
    game.handle_red_ball(1)
    assert game.available_points == 146


def test_handle_color_ball():
    """Test handling a colored ball."""
    game = SnookerScores()
    game.red_needed_next = False
    game.handle_color_ball(2)
    assert game.score_player_1 == 2
    assert game.red_needed_next is True


def test_handle_color_ball_reduces_available_points():
    """Test that handle_color_ball reduces available points correctly."""
    game = SnookerScores()
    game.red_balls = 13
    game.available_points = 138  # 147 - 1 - 7 - 1
    game.red_needed_next = False
    game.handle_color_ball(3)  # green ball
    assert game.available_points == 131  # 138 - 7


def test_handle_miss():
    """Test handling a missed shot."""
    game = SnookerScores()
    game.handle_miss()
    assert game.red_needed_next is True
    assert game.player_1_turn is False


def test_add_penalty():
    snooker_scores = SnookerScores()

    # Test valid penalty input
    with patch('builtins.input', side_effect=['4', 'n']):
        snooker_scores.player_1_turn = True
        snooker_scores.add_penalty()
        assert snooker_scores.score_player_2 == 4
        assert snooker_scores.player_1_turn == False

    # Test invalid penalty input (out of range)
    with patch('builtins.input', side_effect=['8', '4', 'n']):
        snooker_scores.player_1_turn = False
        snooker_scores.add_penalty()
        assert snooker_scores.score_player_1 == 4
        assert snooker_scores.player_1_turn == True

    # Test invalid penalty input (non-numeric)
    with patch('builtins.input', side_effect=['a', '3', 'n']):
        snooker_scores.player_1_turn = True
        snooker_scores.add_penalty()
        assert snooker_scores.score_player_2 == 7
        assert snooker_scores.player_1_turn == False

    # Test respot balls with 'y' input
    with patch('builtins.input', side_effect=['3', 'y']):
        snooker_scores.player_1_turn = False
        snooker_scores.add_penalty()
        assert snooker_scores.score_player_1 == 7
        assert snooker_scores.player_1_turn == False
    # Test respot balls with 'n' input
    with patch('builtins.input', side_effect=['3', 'n']):
        snooker_scores.player_1_turn = True
        snooker_scores.add_penalty()
        assert snooker_scores.score_player_2 == 10
        assert snooker_scores.red_needed_next == True


# Score handling
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

def test_calculate_possible_scores():
    """Test calculating possible scores."""
    game = SnookerScores()
    game.score_player_1 = 10
    game.score_player_2 = 20
    game.available_points = 117
    game.calculate_possible_scores()
    assert game.possible_score_player_1 == 127
    assert game.possible_score_player_2 == 137

def test_set_starting_scores_valid():
    """Test setting valid starting scores."""
    game = SnookerScores()
    with patch("builtins.input", side_effect=["10", "20", "15"]):
        game.set_starting_scores()
        assert game.score_player_1 == 20
        assert game.score_player_2 == 15
        assert game.red_balls == 10
        assert game.available_points == 112

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


# Game phases
def test_red_balls_phase():
    """Test the red balls phase."""
    game = SnookerScores()
    with patch("builtins.input", side_effect=["1", "2"] * 14 + ["1", "5"]):
        # (14 * 1) + (14 * 2), 1 + 5 (last blue)
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
    game = SnookerScores()
    game.red_balls = 0
    game.available_points = 27
    game.score_player_1 = 0
    game.score_player_2 = 0
    game.color_needed = 2

    with patch("builtins.input", side_effect=["2", "3", "4", "5", "6", "7"]):
        with patch("builtins.print") as mocked_print:
            game.colored_balls_phase()
            assert game.score_player_1 == 27  # Player 1 pots all colored balls
            assert game.score_player_2 == 0
            assert game.available_points == 0
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
