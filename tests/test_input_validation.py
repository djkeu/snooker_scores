import pytest
from unittest.mock import patch
from snooker_scores import SnookerScores
import itertools

def mock_input(prompt, *values):
    """Helper function to mock the input function."""
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
        with mock_input(snooker_game.shot_prompt, "q"):
            with pytest.raises(SystemExit):
                snooker_game.get_shot_value()
        mock_exit.assert_called_once()

def test_validate_shot_p():
    snooker_game = SnookerScores()
    with patch.object(snooker_game, "add_penalty") as mock_penalty:
        with mock_input(snooker_game.shot_prompt, "p", "1"):
            assert snooker_game.get_shot_value() == 1
        mock_penalty.assert_called_once()

def test_validate_shot_x():
    snooker_game = SnookerScores()
    initial_turn = snooker_game.player_1_turn
    with patch.object(snooker_game, "switch_players", side_effect=snooker_game.switch_players) as mock_switch:
        with mock_input(snooker_game.shot_prompt, "x", "1"):
            assert snooker_game.get_shot_value() == 1
        mock_switch.assert_called_once()
    assert snooker_game.player_1_turn != initial_turn

def test_validate_shot_s():
    snooker_game = SnookerScores()
    snooker_game.first_input = True
    
    # Mock all inputs in sequence
    inputs = ["s", "5", "40", "40", "1"]
    with patch("builtins.input", side_effect=inputs):
        result = snooker_game.get_shot_value()
        assert result == 1


def test_validate_and_return_shot_valid():
    """Test validate_and_return_shot with valid input."""
    game = SnookerScores()
    
    # Test valid inputs
    assert game.validate_and_return_shot("1") == 1
    assert game.validate_and_return_shot("7") == 7
    assert game.validate_and_return_shot("0") == 0

def test_validate_and_return_shot_invalid():
    """Test validate_and_return_shot with invalid input."""
    game = SnookerScores()
    
    # Test invalid inputs
    assert game.validate_and_return_shot("8") is None  # Out of range
    assert game.validate_and_return_shot("-1") is None  # Out of range
    assert game.validate_and_return_shot("abc") is None  # Non-integer
    assert game.validate_and_return_shot("") is None  # Empty input

def test_validate_shot_edge_cases():
    game = SnookerScores()
    assert game.validate_shot("-1") is None
    assert game.validate_shot("8") is None
    assert game.validate_shot("abc") is None
    assert game.validate_shot("") is None


# Handle special inputs
def test_handle_special_input_q():
    snooker_game = SnookerScores()
    with patch("sys.exit") as mock_exit:
        snooker_game.handle_hotkeys("q")
        mock_exit.assert_called_once()

def test_handle_special_input_p():
    snooker_game = SnookerScores()
    with patch.object(snooker_game, 'add_penalty') as mock_add_penalty:
        snooker_game.handle_hotkeys("p")
        mock_add_penalty.assert_called_once()

def test_handle_special_input_x():
    snooker_game = SnookerScores()
    with patch.object(snooker_game, 'switch_players') as mock_switch_players:
        snooker_game.handle_hotkeys("x")
        mock_switch_players.assert_called_once()

def test_handle_special_input_s():
    snooker_game = SnookerScores()
    with patch.object(snooker_game, 'set_starting_scores') as mock_set_starting_scores:
        snooker_game.handle_hotkeys("s")
        mock_set_starting_scores.assert_called_once()

def test_handle_invalid_input(capfd):
    snooker_game = SnookerScores()
    snooker_game.handle_invalid_input()
    captured = capfd.readouterr()
    assert "Only numbers between 0 and 7 are valid!" in captured.out


# Re-spot input validation
def test_get_respot_input_valid():
    with mock_input("Do you want a respot? (y/n) ", "y"):
        game = SnookerScores()
        result = game.get_respot_input()
        assert result == 'y', f"Expected 'y', but got {result}"

    with mock_input("Do you want a respot? (y/n) ", "n"):
        game = SnookerScores()
        result = game.get_respot_input()
        assert result == 'n', f"Expected 'n', but got {result}"

def test_get_respot_input_invalid():
    with mock_input("Re-spot black? (y/n): ", "a"):
        with mock_input("Re-spot black? (y/n): ", "y"):
            game = SnookerScores()
            result = game.get_respot_input()
            assert result == 'y', f"Expected 'y', but got {result}"

def test_get_respot_input_edge_cases():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["invalid", "y"]):
        assert game.get_respot_input() == "y"
    with patch("builtins.input", side_effect=["invalid", "n"]):
        assert game.get_respot_input() == "n"

def test_respot_balls_edge_cases():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["y"]):
        game.respot_balls()
        assert game.red_needed_next is True
    with patch("builtins.input", side_effect=["n"]):
        game.respot_balls()
        assert game.red_needed_next is True


# Starting scores validation
def test_set_starting_scores_valid_input():
    inputs = ["5", "15", "15"]
    with patch("builtins.input", side_effect=inputs):
        game = SnookerScores()
        game.set_starting_scores()
        assert game.red_balls == 5
        assert game.score_player_1 == 15
        assert game.score_player_2 == 15

def test_set_starting_scores_invalid_score():
    with mock_input(
        "Enter the number of red balls left: ", "5",
        "Enter score for Player 1: ", "30",
        "Enter score for Player 2: ", "20"
    ):
        game = SnookerScores()
        game.set_starting_scores()
        assert game.red_balls == 5
        assert game.score_player_1 == 30
        assert game.score_player_2 == 20


def test_set_starting_scores_invalid_red_balls():
    """Test set_starting_scores with invalid red ball inputs."""
    with mock_input(
        "Enter the number of red balls left: ", "20", "-15", "15",
        "Enter score for Player 1: ", "0",
        "Enter score for Player 2: ", "0"
    ):
        game = SnookerScores()
        game.set_starting_scores()
        assert game.red_balls == 15

def test_set_starting_scores_invalid_total_score():
    with mock_input(
        "Enter the number of red balls left: ", "5",
        "Enter score for Player 1: ", "30",
        "Enter score for Player 2: ", "20"
    ):
        game = SnookerScores()
        game.set_starting_scores()
        assert game.red_balls == 5
        assert game.score_player_1 == 30
        assert game.score_player_2 == 20
    
def test_set_starting_scores_edge_cases():
    game = SnookerScores()

    with patch("builtins.input", side_effect=["-1", "16", "15", "0", "0"]):
        game.set_starting_scores()
        assert game.red_balls == 15

    with patch("builtins.input", side_effect=["15", "-1", "148", "0", "0"]):
        game.set_starting_scores()
        assert game.score_player_1 == 0
        assert game.score_player_2 == 0


def test_get_input_starting_scores_valid():
    with mock_input("Enter a number: ", "10"):
        game = SnookerScores()
        result = game.get_input_starting_scores("Enter a number: ", lambda x: None)
        assert result == 10

def test_get_input_starting_scores_invalid_then_valid():
    with mock_input("Enter a number: ", "invalid", "20"):
        game = SnookerScores()
        result = game.get_input_starting_scores("Enter a number: ", lambda x: None)
        assert result == 20

def test_get_input_starting_scores_edge_cases():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["invalid", "invalid", "5"]):
        result = game.get_input_starting_scores("Enter a number: ", lambda x: int(x))
    assert result == 5


def test_validate_red_balls_valid():
    """Test validate_red_balls with valid input."""
    game = SnookerScores()
    
    game.validate_red_balls(0)
    game.validate_red_balls(10)
    game.validate_red_balls(15)

def test_validate_red_balls_invalid_low():
    """Test validate_red_balls with invalid input (too low)."""
    game = SnookerScores()
    
    with pytest.raises(ValueError, match="Invalid number of red balls. It must be between 0 and 15."):
        game.validate_red_balls(-1)

def test_validate_red_balls_invalid_high():
    """Test validate_red_balls with invalid input (too high)."""
    game = SnookerScores()
    
    with pytest.raises(ValueError, match="Invalid number of red balls. It must be between 0 and 15."):
        game.validate_red_balls(16)

def test_validate_red_balls_edge_cases():
    game = SnookerScores()
    with pytest.raises(ValueError):
        game.validate_red_balls(-1)
    with pytest.raises(ValueError):
        game.validate_red_balls(16)
    game.validate_red_balls(0)
    game.validate_red_balls(15)


def test_validate_player_scores_valid():
    """Test validate_player_scores with valid input."""
    game = SnookerScores()
    game.red_balls = 0
    game.end_break = 0
    game.validate_player_scores(50, 60)
    game.validate_player_scores(0, 0)
    game.validate_player_scores(147, 0)

def test_validate_player_scores_negative():
    """Test validate_player_scores with negative scores."""
    game = SnookerScores()
    
    with pytest.raises(ValueError, match="Scores must be positive values."):
        game.validate_player_scores(-10, 20)
    with pytest.raises(ValueError, match="Scores must be positive values."):
        game.validate_player_scores(10, -20)
    with pytest.raises(ValueError, match="Scores must be positive values."):
        game.validate_player_scores(-10, -20)

def test_validate_player_scores_exceed_maximum_break():
    """Test validate_player_scores with scores exceeding the maximum break."""
    game = SnookerScores()
    game.red_balls = 0
    game.end_break = 0
    
    with pytest.raises(ValueError, match="Total score cannot exceed 147."):
        game.validate_player_scores(100, 50)
    with pytest.raises(ValueError, match="Total score cannot exceed 147."):
        game.validate_player_scores(148, 0)
    with pytest.raises(ValueError, match="Total score cannot exceed 147."):
        game.validate_player_scores(0, 148)

def test_validate_player_scores_edge_cases():
    game = SnookerScores()
    game.red_balls = 0
    game.end_break = 0
    
    with pytest.raises(ValueError):
        game.validate_player_scores(-1, 0)
    with pytest.raises(ValueError):
        game.validate_player_scores(0, -1)
    with pytest.raises(ValueError):
        game.validate_player_scores(148, 0)
    with pytest.raises(ValueError):
        game.validate_player_scores(0, 148)
    game.validate_player_scores(0, 0)
    game.validate_player_scores(147, 0)
    game.validate_player_scores(0, 147)


def test_validate_min_score_valid():
    """Test validate_min_score with valid input."""
    game = SnookerScores()
    
    game.validate_min_score(5, 50, 60)
    game.validate_min_score(0, 147, 0)
    game.validate_min_score(15, 0, 0)

def test_validate_min_score_invalid():
    """Test validate_min_score with invalid input (total score too low)."""
    game = SnookerScores()
    
    with pytest.raises(ValueError, match="Total score is too low."):
        game.validate_min_score(5, 10, 15)
    with pytest.raises(ValueError, match="Total score is too low."):
        game.validate_min_score(10, 5, 7)
    with pytest.raises(ValueError, match="Total score is too low."):
        game.validate_min_score(14, 0, 0)

def test_validate_min_score_edge_cases():
    game = SnookerScores()
    game.validate_min_score(15, 0, 0)
    game.validate_min_score(14, 1, 0)
    game.validate_min_score(14, 1, 1)
    game.validate_min_score(14, 3, 0)


# Penalty input validation
def test_get_penalty_input_valid():
    with mock_input("Enter the penalty value: ", "5"):
        game = SnookerScores()
        penalty = game.get_penalty_input()
        assert penalty == 5

def test_get_penalty_input_invalid():
    with mock_input("Enter penalty value: ", "-1"):
        with mock_input("Enter penalty value: ", "3"):
            game = SnookerScores()
            penalty = game.get_penalty_input()
            assert penalty == 3

def test_get_penalty_input_edge_cases():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["invalid", "-1", "5"]):
        assert game.get_penalty_input() == 5

def test_get_penalty_input_early_exit():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["q"]):
        penalty = game.get_penalty_input()
        assert penalty is None

def test_get_penalty_input_invalid_then_early_exit():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["invalid", "q"]):
        penalty = game.get_penalty_input()
        assert penalty is None

def test_get_penalty_input_negative_then_early_exit():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["-1", "q"]):
        penalty = game.get_penalty_input()
        assert penalty is None


# Players names input validation
def test_store_players_names_no():
    game = SnookerScores()
    inputs = ["n"]
    with mock_input("Do you want to enter player names? (y/n) ", *inputs):
        game.store_players_names()
    assert game.player_1 == "Player 1"
    assert game.player_2 == "Player 2"

def test_store_players_names_yes():
    game = SnookerScores()
    inputs = ["y", "Alice", "Bob"]
    with mock_input("Do you want to enter player names? (y/n) ", *inputs):
        game.store_players_names()
    assert game.player_1 == "Alice"
    assert game.player_2 == "Bob"

def test_get_player_name_empty():
    game = SnookerScores()
    with mock_input("Enter your name: ", ""):
        name = game.get_player_name()
    assert name is None

def test_get_player_name_valid():
    game = SnookerScores()
    with mock_input("Enter your name: ", "Alice"):
        name = game.get_player_name()
    assert name == "Alice"

def test_get_player_name_capitalized():
    game = SnookerScores()
    with mock_input("Enter your name: ", "alice"):
        name = game.get_player_name()
    assert name == "Alice"

def test_get_player_name_whitespace():
    game = SnookerScores()
    with mock_input("Enter your name: ", "  Alice  "):
        name = game.get_player_name()
    assert name == "Alice"

def test_get_player_name_special_characters():
    game = SnookerScores()
    with mock_input("Enter your name: ", "Alice123!"):
        name = game.get_player_name()
    assert name == "Alice123!"

def test_get_player_name_multiple_words():
    game = SnookerScores()
    with mock_input("Enter your name: ", "Alice Smith"):
        name = game.get_player_name()
    assert name == "Alice Smith"

def test_get_player_name_all_lowercase():
    game = SnookerScores()
    with mock_input("Enter your name: ", "alice smith"):
        name = game.get_player_name()
    assert name == "Alice Smith"

def test_get_player_name_all_uppercase():
    game = SnookerScores()
    with mock_input("Enter your name: ", "ALICE SMITH"):
        name = game.get_player_name()
    assert name == "Alice Smith"

def test_get_player_name_mixed_case():
    game = SnookerScores()
    with mock_input("Enter your name: ", "aLiCe sMiTh"):
        name = game.get_player_name()
    assert name == "Alice Smith"
