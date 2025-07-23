import pytest
from snooker_scores import SnookerScores


def test_store_players_names_yes(monkeypatch):
    scores = SnookerScores()
    inputs = iter(["y", "John", "Mary"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    scores.display_active_player = lambda: None
    
    scores._store_players_names()
    
    assert scores.player_1 == "John"
    assert scores.player_2 == "Mary"


def test_store_players_names_no(monkeypatch):
    scores = SnookerScores()
    monkeypatch.setattr('builtins.input', lambda _: "n")
    
    scores._store_players_names()
    
    assert scores.player_1 == "Player 1"
    assert scores.player_2 == "Player 2"


def test_store_players_names_invalid_then_valid(monkeypatch):
    scores = SnookerScores()
    inputs = iter(["invalid", "y", "John", "Mary"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    scores.display_active_player = lambda: None
    
    scores._store_players_names()
    
    assert scores.player_1 == "John"
    assert scores.player_2 == "Mary"


def test_get_shot_value_valid(monkeypatch):
    scores = SnookerScores()
    monkeypatch.setattr('builtins.input', lambda _: "5")
    
    result = scores._get_shot_value()
    
    assert result == 5
    assert scores.first_input is False


def test_get_shot_value_invalid_then_valid(monkeypatch):
    scores = SnookerScores()
    inputs = iter(["invalid", "8", "5"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    result = scores._get_shot_value()
    
    assert result == 5
    assert scores.first_input is False


def test_get_shot_value_hotkey(monkeypatch):
    scores = SnookerScores()
    scores.switch_players = lambda: None
    inputs = iter(["x", "5"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    result = scores._get_shot_value()
    
    assert result == 5


def test_respot_balls_yes(monkeypatch):
    scores = SnookerScores()
    scores.player_1_turn = True
    inputs = iter(["y"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    scores.display_active_player = lambda: None
    
    scores.respot_balls()
    
    assert scores.player_1_turn is False


def test_respot_balls_no_with_reds(monkeypatch):
    scores = SnookerScores()
    scores.red_balls = 5
    inputs = iter(["n"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    scores.display_active_player = lambda: None
    
    scores.respot_balls()
    
    assert scores.red_needed_next is True


def test_respot_balls_no_without_reds(monkeypatch):
    scores = SnookerScores()
    scores.red_balls = 0
    inputs = iter(["n"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    scores.display_active_player = lambda: None
    
    scores.respot_balls()
    
    assert scores.red_needed_next is False


def test_respot_balls_invalid_then_valid(monkeypatch):
    scores = SnookerScores()
    inputs = iter(["invalid", "y"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    scores.display_active_player = lambda: None
    
    scores.respot_balls()
    
    assert scores.player_1_turn is False
