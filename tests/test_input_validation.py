import pytest
from unittest.mock import patch
from snooker_scores import SnookerScores

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


# Re-spot input validation
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
        assert game.red_balls == 15

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
        assert game.red_balls == 15
    
def test_set_starting_scores_edge_cases():
    game = SnookerScores()

    with patch("builtins.input", side_effect=["-1", "16", "15", "0", "0"]):
        game.set_starting_scores()
        assert game.red_balls == 15

    with patch("builtins.input", side_effect=["15", "-1", "148", "0", "0"]):
        game.set_starting_scores()
        assert game.score_player_1 == 0
        assert game.score_player_2 == 0

# Starting scores inputs
def test_get_input_starting_scores_valid():
    with patch("builtins.input", side_effect=["10", "10", "10"]):
        game = SnookerScores()
        result = game.collect_starting_scores_inputs()
        assert result == (10, 10, 10)

def test_get_input_starting_scores_invalid_then_valid():
    with patch("builtins.input", side_effect=["invalid", "20", "20", "20"]):
        game = SnookerScores()
        result = game.collect_starting_scores_inputs()
        assert result is None

def test_get_input_starting_scores_edge_cases():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["invalid", "invalid", "5", "5", "5"]):
        result = game.collect_starting_scores_inputs()
        assert result is None

# Starting scores red balls
def test_validate_red_balls_no_reds():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["0", "30", "30", "2"]):
        with patch.object(game, "setup_colored_balls_phase"):
            game.set_starting_scores()
            assert game.red_balls == 0
            assert game.score_player_1 == 30
            assert game.score_player_2 == 30
            assert game.yellow_ball == 2

def test_validate_red_balls_valid_1_red():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["1", "33", "44"]):
        result = game.collect_starting_scores_inputs()
        assert result == (1, 33, 44)

def test_validate_red_balls_valid_2_reds():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["2", "44", "44"]):
        result = game.collect_starting_scores_inputs()
        assert result == (2, 44, 44)

def test_validate_red_balls_invalid_low():
    """Test validate_red_balls with invalid input (too low)."""
    game = SnookerScores()
    with patch("builtins.input", side_effect=["-1", "0", "0"]):
        result = game.collect_starting_scores_inputs()
        assert result is None

def test_validate_red_balls_invalid_high():
    """Test validate_red_balls with invalid input (too high)."""
    game = SnookerScores()
    with patch("builtins.input", side_effect=["16", "0", "0"]):
        result = game.collect_starting_scores_inputs()
        assert result is None

def test_validate_red_balls_edge_cases():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["-1", "0", "0"]):
        result = game.collect_starting_scores_inputs()
        assert result is None

# Starting scores player scores
def test_validate_player_scores_valid():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["0", "50", "60"]):
        result = game.collect_starting_scores_inputs()
        assert result == (0, 50, 60)

def test_validate_player_scores_negative():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["0", "-10", "20"]):
        result = game.collect_starting_scores_inputs()
        assert result is None

def test_validate_player_scores_exceed_maximum_break():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["0", "100", "50"]):
        result = game.collect_starting_scores_inputs()
        assert result is None

def test_validate_player_scores_edge_cases():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["0", "-1", "0"]):
        result = game.collect_starting_scores_inputs()
        assert result is None

# Starting scores minimum scores
def test_validate_min_score_valid():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["5", "30", "35"]):
        result = game.collect_starting_scores_inputs()
        assert result == (5, 30, 35)

def test_validate_min_score_invalid():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["5", "10", "15"]):
        result = game.collect_starting_scores_inputs()
        assert result is None

def test_validate_min_score_edge_cases():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["15", "0", "0"]):
        result = game.collect_starting_scores_inputs()
        assert result == (15, 0, 0)


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
