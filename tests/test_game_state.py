import pytest
import sys
from snooker_scores import SnookerScores

"""
def test_restart_game_yes(monkeypatch):
    scores = SnookerScores()
    original_init = scores.__init__
    scores.__init__ = lambda: None
    scores.set_up_game = lambda: None
    scores.main_game = lambda: None
    monkeypatch.setattr('builtins.input', lambda _: "y")
    
    scores.restart_game()
    
    scores.__init__ = original_init
"""

def test_restart_game_no(monkeypatch):
    scores = SnookerScores()
    def mock_exit(_):
        raise SystemExit()
    monkeypatch.setattr('builtins.input', lambda _: "n")
    monkeypatch.setattr(sys, 'exit', mock_exit)
    
    with pytest.raises(SystemExit):
        scores.restart_game()

        
def test_restart_game_invalid_then_valid(monkeypatch):
    scores = SnookerScores()
    original_init = scores.__init__
    scores.__init__ = lambda: None
    scores.set_up_game = lambda: None
    scores.main_game = lambda: None
    inputs = iter(["invalid", "y"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    scores.restart_game()
    
    scores.__init__ = original_init


def test_exit_game(monkeypatch):
    scores = SnookerScores()
    def mock_exit(_):
        raise SystemExit()
    monkeypatch.setattr(sys, 'exit', mock_exit)
    
    with pytest.raises(SystemExit):
        scores.exit_game()


def test_early_victory():
    scores = SnookerScores()
    scores.display_winner = lambda: None
    scores.restart_game = lambda: None
    
    scores.early_victory()


def test_black_ball_phase_miss_then_black(monkeypatch):
    scores = SnookerScores()
    scores.player_1_turn = True
    scores.display_active_player = lambda: None
    scores.winner_black_ball_phase = lambda: None
    inputs = iter(["0", "7"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    scores.black_ball_phase()
    
    assert scores.player_1_turn is False


def test_black_ball_phase_invalid_then_black(monkeypatch):
    scores = SnookerScores()
    scores.player_1_turn = True
    scores.display_active_player = lambda: None
    scores.winner_black_ball_phase = lambda: None
    inputs = iter(["invalid", "9", "7"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    scores.black_ball_phase()
    
    assert scores.player_1_turn is True


def test_display_winner_player_1():
    scores = SnookerScores()
    scores.player_1 = "John"
    scores.player_2 = "Mary"
    scores.score_player_1 = 100
    scores.score_player_2 = 50
    scores.black_ball_phase = lambda: None
    
    scores.display_winner()


def test_display_winner_player_2():
    scores = SnookerScores()
    scores.player_1 = "John"
    scores.player_2 = "Mary"
    scores.score_player_1 = 50
    scores.score_player_2 = 100
    scores.black_ball_phase = lambda: None
    
    scores.display_winner()


def test_display_winner_tie():
    scores = SnookerScores()
    scores.player_1 = "John"
    scores.player_2 = "Mary"
    scores.score_player_1 = 50
    scores.score_player_2 = 50
    scores.black_ball_phase = lambda: None
    
    scores.display_winner()


def test_display_colored_ball_to_play_player1():
    scores = SnookerScores()
    scores.player_1 = "John"
    scores.player_1_turn = True
    scores.yellow_ball = 3
    
    scores.display_colored_ball_to_play()


def test_display_colored_ball_to_play_player2():
    scores = SnookerScores()
    scores.player_2 = "Mary"
    scores.player_1_turn = False
    scores.yellow_ball = 4
    
    scores.display_colored_ball_to_play()


def test_display_break_below_century():
    scores = SnookerScores()
    scores.break_size = 90
    assert scores.century_break is False
    scores.break_size = 99
    assert scores.century_break is False


def test_display_century_break():
    scores = SnookerScores()

    scores.century_break = False
    scores.break_size = 5
    scores.display_century_break()
    assert scores.century_break is False

    scores.century_break = False
    scores.break_size = 95
    scores.display_century_break()
    assert scores.century_break is False

    scores.century_break = False
    scores.break_size = 100
    scores.display_century_break()
    assert scores.century_break is True

    scores.century_break = False
    scores.break_size = 110
    scores.display_century_break()
    assert scores.century_break is True
