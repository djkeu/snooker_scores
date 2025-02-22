import pytest
from unittest.mock import patch
from snooker_scores import SnookerScores
import itertools

def mock_input(prompt, *values):
    if len(values) == 1:
        return patch('builtins.input', return_value=values[0])
    else:
        return patch('builtins.input', side_effect=values)


# Shot validation tests
def test_validate_shot_valid():
    snooker_game = SnookerScores()
    assert snooker_game.validate_shot("0") == 0
    assert snooker_game.validate_shot("7") == 7

def test_validate_shot_invalid():
    snooker_game = SnookerScores()
    assert snooker_game.validate_shot("-1") is None
    assert snooker_game.validate_shot("8") is None
    assert snooker_game.validate_shot("100") is None
    assert snooker_game.validate_shot("abc") is None
    assert snooker_game.validate_shot("!") is None
    assert snooker_game.validate_shot("") is None

def test_validate_shot_quit():
    snooker_game = SnookerScores()
    with patch("sys.exit", side_effect=SystemExit) as mock_exit:
        with mock_input("Enter shot value: ", "q"):
            with pytest.raises(SystemExit):
                snooker_game.get_shot_value()
        mock_exit.assert_called_once()

def test_validate_shot_p():
    snooker_game = SnookerScores()
    with patch.object(snooker_game, "add_penalty") as mock_penalty:
        with mock_input("Enter shot value: ", "p", "1"):  # Mock input sequence
            assert snooker_game.get_shot_value() == 1
        mock_penalty.assert_called_once()

def test_validate_shot_x():
    snooker_game = SnookerScores()
    initial_turn = snooker_game.player_1_turn
    with patch.object(snooker_game, "switch_players", side_effect=snooker_game.switch_players) as mock_switch:
        with mock_input("Enter shot value: ", "x", "1"):  # Mock input sequence
            assert snooker_game.get_shot_value() == 1
        mock_switch.assert_called_once()
    assert snooker_game.player_1_turn != initial_turn

def test_validate_shot_s():
    snooker_game = SnookerScores()
    snooker_game.first_input = True
    with mock_input("Enter shot value: ", "s"):
        with mock_input("Enter red balls: ", "5"):
            with mock_input("Enter player 1 score: ", "40"):
                with mock_input("Enter player 2 score: ", "40"):
                    with mock_input("Enter shot value: ", "1"):
                        snooker_game.get_shot_value()


# Handle special inputs
def test_handle_special_input_q():
    snooker_game = SnookerScores()
    with patch("sys.exit") as mock_exit:
        snooker_game.handle_special_input("q")
        mock_exit.assert_called_once()

def test_handle_special_input_p():
    snooker_game = SnookerScores()
    with patch.object(snooker_game, 'add_penalty') as mock_add_penalty:
        snooker_game.handle_special_input("p")
        mock_add_penalty.assert_called_once()

def test_handle_special_input_x():
    snooker_game = SnookerScores()
    with patch.object(snooker_game, 'switch_players') as mock_switch_players:
        snooker_game.handle_special_input("x")
        mock_switch_players.assert_called_once()

def test_handle_special_input_s():
    snooker_game = SnookerScores()
    with patch.object(snooker_game, 'set_starting_scores') as mock_set_starting_scores:
        snooker_game.handle_special_input("s")
        mock_set_starting_scores.assert_called_once()

def test_handle_invalid_input(capfd):
    snooker_game = SnookerScores()
    snooker_game.handle_invalid_input()
    captured = capfd.readouterr()
    assert "Only numbers between 0 and 7 are valid!" in captured.out


# Re-spot input validation
def test_get_respot_input_valid():
    with mock_input("Re-spot black? (y/n): ", "y"):
        game = SnookerScores()
        result = game.get_respot_input()
        assert result == 'y', f"Expected 'y', but got {result}"

    with mock_input("Re-spot black? (y/n): ", "n"):
        game = SnookerScores()
        result = game.get_respot_input()
        assert result == 'n', f"Expected 'n', but got {result}"

def test_get_respot_input_invalid():
    with mock_input("Re-spot black? (y/n): ", "a"):
        with mock_input("Re-spot black? (y/n): ", "y"):
            game = SnookerScores()
            result = game.get_respot_input()
            assert result == 'y', f"Expected 'y', but got {result}"


# Starting scores validation
def test_set_starting_scores_valid_input():
    with mock_input("Enter red balls: ", "5"):
        with mock_input("Enter player 1 score: ", "15"):
            with mock_input("Enter player 2 score: ", "15"):
                game = SnookerScores()
                game.set_starting_scores()

def test_set_starting_scores_invalid_score():
    # Provide invalid inputs followed by valid inputs to allow the method to retry
    with mock_input(
        "Enter the number of red balls left: ", "5", "5", "5",  # Invalid inputs
        "Enter score for Player 1: ", "5", "5", "5",            # Invalid inputs
        "Enter score for Player 2: ", "5", "5", "5"             # Invalid inputs
    ):
        game = SnookerScores()
        with pytest.raises(ValueError):
            game.set_starting_scores()

def test_set_starting_scores_invalid_red_balls():
    # Provide only invalid inputs for red balls
    with mock_input(
        "Enter the number of red balls left: ", "20", "20", "20"  # Invalid inputs for red balls
    ):
        game = SnookerScores()
        with pytest.raises(ValueError):
            game.set_starting_scores()

def test_set_starting_scores_invalid_total_score():
    # Provide invalid inputs for total score, followed by valid inputs for red balls and scores
    with mock_input(
        "Enter the number of red balls left: ", "5", "5", "5",      # Valid inputs for red balls
        "Enter score for Player 1: ", "150", "150", "150",         # Invalid inputs for Player 1
        "Enter score for Player 2: ", "150", "150", "150"          # Invalid inputs for Player 2
    ):
        game = SnookerScores()
        with pytest.raises(ValueError):
            game.set_starting_scores()

def test_get_valid_input_valid():
    """Test get_valid_input with valid input."""
    with mock_input("Enter a number: ", "10"):
        game = SnookerScores()
        result = game.get_valid_input(
            "Enter a number: ",
            lambda x: None,  # No validation
            "Invalid input."
        )
        assert result == 10

def test_get_valid_input_invalid_then_valid():
    """Test get_valid_input with invalid input followed by valid input."""
    with mock_input("Enter a number: ", "invalid", "20"):
        game = SnookerScores()
        result = game.get_valid_input(
            "Enter a number: ",
            lambda x: None,  # No validation
            "Invalid input."
        )
        assert result == 20

def test_get_valid_input_exhaust_retries():
    """Test get_valid_input exhausting retries with invalid input."""
    with mock_input("Enter a number: ", "invalid", "invalid", "invalid"):
        game = SnookerScores()
        with pytest.raises(ValueError, match="Invalid input."):
            game.get_valid_input(
                "Enter a number: ",
                lambda x: None,  # No validation
                "Invalid input.",
                max_retries=3
            )

def test_validate_red_balls_valid():
    """Test validate_red_balls with valid input."""
    game = SnookerScores()
    
    # Test valid inputs
    game.validate_red_balls(0)   # Minimum valid value
    game.validate_red_balls(10)  # Middle valid value
    game.validate_red_balls(15)  # Maximum valid value

def test_validate_red_balls_invalid_low():
    """Test validate_red_balls with invalid input (too low)."""
    game = SnookerScores()
    
    # Test invalid input (too low)
    with pytest.raises(ValueError, match="Invalid number of red balls. It must be between 0 and 15."):
        game.validate_red_balls(-1)

def test_validate_red_balls_invalid_high():
    """Test validate_red_balls with invalid input (too high)."""
    game = SnookerScores()
    
    # Test invalid input (too high)
    with pytest.raises(ValueError, match="Invalid number of red balls. It must be between 0 and 15."):
        game.validate_red_balls(16)

def test_validate_player_scores_valid():
    """Test validate_player_scores with valid input."""
    game = SnookerScores()
    
    # Test valid inputs
    game.validate_player_scores(50, 60)  # Valid scores
    game.validate_player_scores(0, 0)    # Edge case: minimum valid scores
    game.validate_player_scores(147, 0)  # Edge case: maximum valid total score

def test_validate_player_scores_negative():
    """Test validate_player_scores with negative scores."""
    game = SnookerScores()
    
    # Test invalid input (negative scores)
    with pytest.raises(ValueError, match="Scores must be positive values."):
        game.validate_player_scores(-10, 20)  # Player 1 score is negative
    with pytest.raises(ValueError, match="Scores must be positive values."):
        game.validate_player_scores(10, -20)  # Player 2 score is negative
    with pytest.raises(ValueError, match="Scores must be positive values."):
        game.validate_player_scores(-10, -20)  # Both scores are negative

def test_validate_player_scores_exceed_maximum_break():
    """Test validate_player_scores with scores exceeding the maximum break."""
    game = SnookerScores()
    
    # Test invalid input (total score exceeds maximum break)
    with pytest.raises(ValueError, match="Total score cannot exceed 147."):
        game.validate_player_scores(100, 50)  # Total score is 150
    with pytest.raises(ValueError, match="Total score cannot exceed 147."):
        game.validate_player_scores(148, 0)   # Total score is 148
    with pytest.raises(ValueError, match="Total score cannot exceed 147."):
        game.validate_player_scores(0, 148)   # Total score is 148

def test_validate_minimum_score_valid():
    """Test validate_minimum_score with valid input."""
    game = SnookerScores()
    
    # Test valid inputs
    game.validate_minimum_score(5, 50, 60)  # Total score (110) exceeds minimum
    game.validate_minimum_score(0, 147, 0)  # Edge case: maximum score with 0 red balls
    game.validate_minimum_score(15, 0, 0)   # Edge case: minimum score with 15 red balls

def test_validate_minimum_score_invalid():
    """Test validate_minimum_score with invalid input (total score too low)."""
    game = SnookerScores()
    
    # Test invalid input (total score too low)
    with pytest.raises(ValueError, match="Total score is too low."):
        game.validate_minimum_score(5, 10, 15)  # Total score (25) is below minimum (expected minimum: 28)
    with pytest.raises(ValueError, match="Total score is too low."):
        game.validate_minimum_score(10, 5, 7)  # Total score (12) is below minimum (expected minimum: 13)
    with pytest.raises(ValueError, match="Total score is too low."):
        game.validate_minimum_score(14, 0, 0)   # Total score (0) is below minimum (expected minimum: 0)

# Penalty input validation
def test_get_penalty_input_valid():
    with mock_input("Enter penalty value: ", "5"):
        game = SnookerScores()
        penalty = game.get_penalty_input()
        assert penalty == 5

def test_get_penalty_input_invalid():
    with mock_input("Enter penalty value: ", "-1"):
        with mock_input("Enter penalty value: ", "3"):
            game = SnookerScores()
            penalty = game.get_penalty_input()
            assert penalty == 3
