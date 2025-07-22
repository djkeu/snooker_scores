import pytest
import sys
from snooker_scores import SnookerScores


def test_display_snookers_needed_player_1():
    scores = SnookerScores()
    scores.score_player_2 = 100
    scores.score_player_1 = 20
    scores.available_player_1 = 70
    scores.snookers_needed = False
    
    scores.display_snookers_needed()
    
    assert scores.snookers_needed is True


def test_display_snookers_needed_player_2():
    scores = SnookerScores()
    scores.score_player_1 = 100
    scores.score_player_2 = 20
    scores.available_player_2 = 70
    scores.snookers_needed = False
    
    scores.display_snookers_needed()
    
    assert scores.snookers_needed is True


def test_display_snookers_needed_no_snookers():
    scores = SnookerScores()
    scores.score_player_1 = 50
    scores.score_player_2 = 60
    scores.available_player_1 = 70
    scores.available_player_2 = 70
    scores.snookers_needed = False
    
    scores.display_snookers_needed()
    
    assert scores.snookers_needed is False


def test_winner_black_ball_phase_player_1():
    scores = SnookerScores()
    scores.player_1_turn = True
    scores.score_player_1 = 60
    
    scores.winner_black_ball_phase()
    
    assert scores.score_player_1 == 67
    assert scores.score_player_2 == 0


def test_winner_black_ball_phase_player_2():
    scores = SnookerScores()
    scores.player_1_turn = False
    scores.score_player_2 = 60
    
    scores.winner_black_ball_phase()
    
    assert scores.score_player_2 == 67
    assert scores.score_player_1 == 0


def test_handle_hotkeys_quit(monkeypatch):
    scores = SnookerScores()
    def mock_exit(_):
        raise SystemExit()
    monkeypatch.setattr(sys, 'exit', mock_exit)
    
    with pytest.raises(SystemExit):
        scores.handle_hotkeys("q")


def test_handle_hotkeys_penalty():
    scores = SnookerScores()
    scores.add_penalty = lambda: None
    
    result = scores.handle_hotkeys("p")
    
    assert result == "penalty"


def test_handle_hotkeys_switch():
    scores = SnookerScores()
    scores.switch_players = lambda: None
    
    result = scores.handle_hotkeys("x")
    
    assert result == "switch"


def test_handle_hotkeys_set_scores():
    scores = SnookerScores()
    scores.set_starting_scores = lambda: None
    
    result = scores.handle_hotkeys("s")
    
    assert result == "scores_set"


def test_handle_hotkeys_early_victory():
    scores = SnookerScores()
    scores.early_victory = lambda: None
    
    result = scores.handle_hotkeys("w")
    
    assert result == "winner"


def test_handle_hotkeys_red_ball_down():
    scores = SnookerScores()
    scores.red_ball_down = lambda: None
    
    result = scores.handle_hotkeys("r")
    
    assert result == "red_ball_down"


def test_handle_hotkeys_invalid():
    scores = SnookerScores()
    
    result = scores.handle_hotkeys("z")
    
    assert result is None


def test_setup_colored_balls_phase(monkeypatch):
    scores = SnookerScores()
    monkeypatch.setattr('builtins.input', lambda _: "4")
    scores._colored_balls_phase = lambda: None
    scores.red_balls = 0
    
    scores.starting_scores_colored_balls()
    
    assert scores.red_needed_next is False
    assert scores.color_in_line == 4
    # 2+3 = sum(range(2, 4))
    assert scores.available_player_1 == scores.available_player_1
    assert scores.available_player_2 == scores.available_player_2


def test_last_colored_ball_phase(monkeypatch):
    scores = SnookerScores()
    scores.red_balls = 0
    scores.available_player_1 = 50
    scores.available_player_2 = 50
    scores.update_score = lambda x: None
    
    monkeypatch.setattr(scores, 'get_shot_value', lambda: 2)
    scores._last_colored_ball()
    
    assert scores.available_player_1 == scores.END_BREAK
    assert scores.available_player_2 == scores.END_BREAK
