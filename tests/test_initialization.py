import pytest
from snooker_scores import SnookerScores


def test_initialization():
    scores = SnookerScores()
    assert scores.red_balls == 15
    assert scores.player_1 == "Player 1"
    assert scores.player_2 == "Player 2"
    assert scores.score_player_1 == 0
    assert scores.score_player_2 == 0
    assert scores.max_break == 147
    assert scores.end_break == 27
    assert scores.available_player_1 == scores.max_break
    assert scores.available_player_2 == scores.max_break
    assert scores.potential_score_player_1 == scores.max_break
    assert scores.potential_score_player_2 == scores.max_break
    assert scores.break_size == 0
    assert scores.red_needed_next is True
    assert scores.player_1_turn is True
    assert scores.snookers_needed is False
    assert scores.yellow_ball == 2
    assert scores.first_input is True


def test_colored_balls_dict():
    scores = SnookerScores()
    expected_colored_balls = {
        2: "yellow",
        3: "green",
        4: "brown",
        5: "blue",
        6: "pink",
        7: "black",
    }
    assert scores.colored_balls == expected_colored_balls


def test_get_player_name(monkeypatch):
    scores = SnookerScores()
    monkeypatch.setattr('builtins.input', lambda _: "John Doe")
    assert scores.get_player_name() == "John Doe"


def test_get_player_name_empty_then_valid(monkeypatch):
    scores = SnookerScores()
    # Mock input to return empty string first, then valid name
    inputs = iter(["", "John Doe"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    # Mock print to avoid output during test
    monkeypatch.setattr('builtins.print', lambda *args: None)
    assert scores.get_player_name() == "John Doe"


def test_get_player_name_strips_and_titles(monkeypatch):
    scores = SnookerScores()
    monkeypatch.setattr('builtins.input', lambda _: "  john doe  ")
    assert scores.get_player_name() == "John Doe"


def test_prompt_for_player_names_yes(monkeypatch):
    scores = SnookerScores()
    monkeypatch.setattr('builtins.input', lambda _: "y")
    assert scores.prompt_for_player_names() == True


def test_prompt_for_player_names_no(monkeypatch):
    scores = SnookerScores()
    monkeypatch.setattr('builtins.input', lambda _: "n")
    assert scores.prompt_for_player_names() == False


def test_prompt_for_player_names_invalid_then_yes(monkeypatch):
    scores = SnookerScores()
    inputs = iter(["invalid", "y"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    # Mock print to avoid output during test
    monkeypatch.setattr('builtins.print', lambda *args: None)
    assert scores.prompt_for_player_names() == True


def test_store_players_names_with_custom_names(monkeypatch):
    scores = SnookerScores()
    
    # Mock the methods that store_players_names calls
    scores.prompt_for_player_names = lambda: True
    scores.get_player_name = lambda: "Test Player"
    scores.display_active_player = lambda: None
    
    scores.store_players_names()
    
    # Both players should be set to "Test Player" since get_player_name returns the same value
    assert scores.player_1 == "Test Player"
    assert scores.player_2 == "Test Player"


def test_store_players_names_without_custom_names(monkeypatch):
    scores = SnookerScores()
    
    # Store original values
    original_player_1 = scores.player_1
    original_player_2 = scores.player_2
    
    # Mock prompt_for_player_names to return False
    scores.prompt_for_player_names = lambda: False
    scores.display_active_player = lambda: None
    
    scores.store_players_names()
    
    # Players should remain unchanged
    assert scores.player_1 == original_player_1
    assert scores.player_2 == original_player_2


def test_switch_players():
    scores = SnookerScores()
    assert scores.player_1_turn is True
    
    scores.switch_players()
    assert scores.player_1_turn is False
    
    scores.switch_players()
    assert scores.player_1_turn is True


def test_update_score():
    scores = SnookerScores()
    
    scores.update_score(7)
    assert scores.score_player_1 == 7
    assert scores.score_player_2 == 0
    assert scores.break_size == 7
    
    scores.player_1_turn = False
    scores.update_score(5)
    assert scores.score_player_1 == 7
    assert scores.score_player_2 == 5
    assert scores.break_size == 12


def test_calculate_potential_scores():
    scores = SnookerScores()
    scores.score_player_1 = 30
    scores.score_player_2 = 20
    scores.available_player_1 = 100
    scores.available_player_2 = 90
    
    scores.calculate_potential_scores()
    
    assert scores.potential_score_player_1 == 130
    assert scores.potential_score_player_2 == 110
