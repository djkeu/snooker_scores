import pytest
from snooker_scores import SnookerScores


def test_apply_penalty_player_1():
    scores = SnookerScores()
    scores.player_1_turn = True
    initial_score = scores.score_player_1
    
    scores.apply_penalty(4)
    
    assert scores.score_player_1 == initial_score + 4
    assert scores.score_player_2 == 0


def test_apply_penalty_player_2():
    scores = SnookerScores()
    scores.player_1_turn = False
    initial_score = scores.score_player_2
    
    scores.apply_penalty(7)
    
    assert scores.score_player_2 == initial_score + 7
    assert scores.score_player_1 == 0


def test_get_penalty_input_valid(monkeypatch):
    scores = SnookerScores()
    monkeypatch.setattr('builtins.input', lambda _: "4")
    
    result = scores.get_penalty_input()
    
    assert result == 4


def test_get_penalty_input_invalid_then_valid(monkeypatch):
    scores = SnookerScores()
    inputs = iter(["-1", "abc", "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    with pytest.raises(StopIteration):
        scores.get_penalty_input()


def test_get_penalty_input_quit(monkeypatch):
    scores = SnookerScores()
    monkeypatch.setattr('builtins.input', lambda _: "q")
    
    result = scores.get_penalty_input()
    
    assert result is None


def test_update_game_state():
    scores = SnookerScores()
    
    scores.update_game_state(10, 20, 30)
    
    assert scores.red_balls == 10
    assert scores.score_player_1 == 20
    assert scores.score_player_2 == 30
    assert scores.red_needed_next is True
    assert scores.yellow_ball == 2
    assert scores.available_player_1 == 10 * 8 + scores.end_break
    assert scores.available_player_2 == 10 * 8 + scores.end_break


def test_validate_scores_valid():
    scores = SnookerScores()
    
    assert scores.validate_scores(10, 20, 30) is True


def test_validate_scores_total_too_high():
    scores = SnookerScores()
    possible_score = scores.max_score - scores.end_break - 10 * 8
    
    assert scores.validate_scores(10, possible_score, 1) is False


def test_validate_scores_total_too_low():
    scores = SnookerScores()
    
    assert scores.validate_scores(10, 0, 0) is False


def test_get_player_score_valid(monkeypatch):
    scores = SnookerScores()
    monkeypatch.setattr('builtins.input', lambda _: "42")
    
    result = scores.get_player_score("Test Player")
    
    assert result == 42


def test_get_player_score_negative(monkeypatch):
    scores = SnookerScores()
    monkeypatch.setattr('builtins.input', lambda _: "-5")
    
    result = scores.get_player_score("Test Player")
    
    assert result is None


def test_get_player_score_quit(monkeypatch):
    scores = SnookerScores()
    monkeypatch.setattr('builtins.input', lambda _: "q")
    
    result = scores.get_player_score("Test Player")
    
    assert result is None


def test_collect_starting_scores_inputs_valid(monkeypatch):
    scores = SnookerScores()
    inputs = iter(["10", "20", "30"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    result = scores.collect_starting_scores_inputs()
    
    assert result == (10, 20, 30)


def test_collect_starting_scores_inputs_invalid_red_balls(monkeypatch):
    scores = SnookerScores()
    monkeypatch.setattr('builtins.input', lambda _: "20")
    
    result = scores.collect_starting_scores_inputs()
    
    assert result is None
