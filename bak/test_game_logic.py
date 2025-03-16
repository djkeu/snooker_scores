import pytest
from unittest.mock import patch
from snooker_scores import SnookerScores


def mock_input(prompt, value):
    return patch('builtins.input', return_value=value)


# Initial game setup
def test_initial_game_setup():
    game = SnookerScores()

    assert game.score_player_1 == 0
    assert game.score_player_2 == 0
    assert game.available_player_1 == 147
    assert game.available_player_2 == 147
    assert game.red_balls == 15


def test_switch_players():
    game = SnookerScores()

    game.switch_players()
    assert game.player_1_turn is False

    game.switch_players()
    assert game.player_1_turn is True

def test_switch_players_edge_cases():
    game = SnookerScores()
    game.player_1_turn = True
    game.switch_players()
    assert game.player_1_turn is False
    game.switch_players()
    assert game.player_1_turn is True

def test_display_game_state_edge_cases(capsys):
    game = SnookerScores()
    game.score_player_1 = 10
    game.score_player_2 = 20
    game.available_player_1 = 30
    game.available_player_2 = 40
    game.red_balls = 5
    game.player_1_turn = True
    game.red_needed_next = True
    game.display_game_state()
    captured = capsys.readouterr()
    assert "Player 1: score 10, potential score 40" in captured.out
    assert "Player 2: score 20, potential score 60" in captured.out
    assert "5 red balls left" in captured.out
    assert "Player 1 must pot a red ball next" in captured.out

def test_display_next_ball_edge_cases(capsys):
    game = SnookerScores()
    game.player_1_turn = True
    game.red_needed_next = True
    game.display_next_ball()
    captured = capsys.readouterr()
    assert "Player 1 must pot a red ball next" in captured.out
    game.player_1_turn = False
    game.red_needed_next = False
    game.display_next_ball()
    captured = capsys.readouterr()
    assert "Player 2 must pot a colored ball next" in captured.out


# Handling red ball shots
def test_handle_ball_edge_cases():
    game = SnookerScores()
    game.red_balls = 1
    game.handle_ball(1, is_red_ball=True)
    assert game.red_balls == 0
    game.handle_ball(1, is_red_ball=True)
    assert game.red_balls == -1

def test_handle_ball_red():
    """Test the handle_ball method when a red ball is potted."""
    game = SnookerScores()
    
    assert game.red_balls == 15
    assert game.score_player_1 == 0
    assert game.score_player_2 == 0
    assert game.red_needed_next == True

    game.handle_ball(1, is_red_ball=True)
    
    assert game.red_balls == 14
    assert game.score_player_1 == 1
    assert game.red_needed_next == False

    game.switch_players()
    game.handle_ball(1, is_red_ball=True)
    
    assert game.red_balls == 13
    assert game.score_player_2 == 1
    assert game.red_needed_next == False

def test_handle_red_ball_player_1():
    game = SnookerScores()

    game.handle_red_ball(1)
    assert game.red_balls == 14
    assert game.available_player_1 == 146
    assert game.available_player_2 == 139
    assert game.score_player_1 == 1

def test_handle_red_ball_player_2():
    game = SnookerScores()

    game.switch_players()
    game.handle_red_ball(1)
    assert game.red_balls == 14
    assert game.available_player_2 == 146
    assert game.available_player_1 == 139
    assert game.score_player_2 == 1

def test_display_next_ball_red_player_1(capsys):
    """Test display_next_ball when Player 1 needs to pot a red ball."""
    game = SnookerScores()
    game.player_1_turn = True
    game.red_needed_next = True

    game.display_next_ball()

    captured = capsys.readouterr()
    assert "Player 1 must pot a red ball next" in captured.out


# Handling colored ball shots
def test_handle_ball_color():
    """Test the handle_ball method when a colored ball is potted."""
    game = SnookerScores()
    
    assert game.red_balls == 15
    assert game.score_player_1 == 0
    assert game.score_player_2 == 0
    assert game.red_needed_next == True

    game.handle_ball(1, is_red_ball=True)
    game.handle_ball(7, is_red_ball=False)
    
    assert game.red_balls == 14
    assert game.score_player_1 == 8
    assert game.red_needed_next == True

def test_handle_color_ball_player_1():
    game = SnookerScores()

    game.handle_red_ball(1)
    game.handle_color_ball(5)
    assert game.score_player_1 == 6
    assert game.available_player_1 == 139

def test_handle_color_ball_player_2():
    game = SnookerScores()

    game.switch_players()
    game.handle_red_ball(1)
    game.handle_color_ball(4)
    assert game.score_player_2 == 5
    assert game.available_player_2 == 139


# Handling other game events
def test_handle_miss():
    game = SnookerScores()

    game.handle_red_ball(1)
    game.handle_color_ball(5)

    game.handle_miss()
    assert game.available_player_1 == 139
    assert game.available_player_2 == 139

def test_red_balls_phase_edge_cases(capsys):
    """Test edge cases in the red balls phase."""
    game = SnookerScores()
    game.red_balls = 1
    game.player_1_turn = True
    with patch("builtins.input", side_effect=["1", "7", "0", "2", "3", "4", "5", "6", "7", "0", "n"],):
        with pytest.raises(SystemExit):
            game.red_balls_phase()
    captured = capsys.readouterr()
    assert "Player 1: score 1, potential score 147" in captured.out
    assert "Player 2: score 0, potential score 139" in captured.out
    assert "0 red balls left" in captured.out

def test_handle_last_colored_ball():
    game = SnookerScores()

    game.red_balls = 0
    game.available_player_1 = 27
    game.available_player_2 = 27

    game.switch_players()
    with mock_input("What's the value of the shot: ", "2"):
        game.last_colored_ball_phase()

    assert game.available_player_1 == 27
    assert game.available_player_2 == 27
    assert game.red_needed_next == True

def test_handle_last_colored_ball_edge_cases(capsys):
    game = SnookerScores()
    game.red_balls = 0
    game.available_player_1 = 27
    game.available_player_2 = 27
    game.player_1_turn = True
    with patch("builtins.input", side_effect=["2"]):
        game.last_colored_ball_phase()
    captured = capsys.readouterr()
    assert "Player 1: score 2, potential score 22" in captured.out
    assert "Player 2: score 0, potential score 27" in captured.out


def test_colored_balls_phase(capsys):
    game = SnookerScores()
    game.player_1_turn = True
    game.available_player_1 = 2
    game.yellow_ball = 2

    def mock_get_shot_value():
        return 2

    game.get_shot_value = mock_get_shot_value
    game.colored_balls_phase()
    captured = capsys.readouterr()

    assert "Player 1 must pot a yellow ball" in captured.out

def test_colored_balls_phase_basic():
    game = SnookerScores()
    game.available_player_1 = 2
    game.yellow_ball = 2
    with patch("builtins.input", side_effect=["2"]):
        game.colored_balls_phase()
    assert game.available_player_1 == 0

def test_colored_balls_phase_edge_cases(capsys):
    """Test edge cases in the colored balls phase."""
    game = SnookerScores()
    game.available_player_1 = 27
    game.yellow_ball = 2
    game.player_1_turn = True
    with patch("builtins.input", side_effect=["2", "3", "4", "5", "6", "7", "0", "n"]):
        with pytest.raises(SystemExit):
            game.colored_balls_phase()
    captured = capsys.readouterr()
    assert "Player 1 must pot a yellow ball" in captured.out
    assert "Player 1: score 2, potential score 27" in captured.out
    assert "Player 1: score 27, potential score 27" in captured.out
    assert "Player 1 wins!" in captured.out

# Game conclusion
def test_display_winner():
    game = SnookerScores()

    game.score_player_1 = 50
    game.score_player_2 = 40

    with patch('builtins.print') as mock_print:
        game.display_winner()
        mock_print.assert_called_with(
            "\nPlayer 1 wins! (with a score of 50 vs 40)"
        )
