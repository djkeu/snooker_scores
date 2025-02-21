import pytest
from unittest.mock import patch
from snooker_scores import SnookerScores


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
    with mock_input("Enter red balls: ", "5"):
        with mock_input("Enter player 1 score: ", "5"):
            with mock_input("Enter player 2 score: ", "5"):
                game = SnookerScores()
                with pytest.raises(ValueError):
                    game.set_starting_scores()


def test_set_starting_scores_invalid_red_balls():
    with mock_input("Enter red balls: ", "20"):
        with mock_input("Enter player 1 score: ", "10"):
            with mock_input("Enter player 2 score: ", "10"):
                game = SnookerScores()
                with pytest.raises(ValueError):
                    game.set_starting_scores()


def test_set_starting_scores_invalid_total_score():
    with mock_input("Enter red balls: ", "5"):
        with mock_input("Enter player 1 score: ", "150"):
            with mock_input("Enter player 2 score: ", "150"):
                game = SnookerScores()
                with pytest.raises(ValueError):
                    game.set_starting_scores()


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
