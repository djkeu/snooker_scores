import pytest
from snooker_scores import SnookerScores


def test_initialization():
    scores = SnookerScores()
    assert scores.red_balls == 15
    assert scores.player_1 == "Player 1"
    assert scores.player_2 == "Player 2"
    assert scores.score_player_1 == 0
    assert scores.score_player_2 == 0
    assert scores.max_score == 147
    assert scores.end_break == 27
    assert scores.available_player_1 == scores.max_score
    assert scores.available_player_2 == scores.max_score
    assert scores.potential_score_player_1 == scores.max_score
    assert scores.potential_score_player_2 == scores.max_score
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


def test_get_player_name_empty(monkeypatch):
    scores = SnookerScores()
    monkeypatch.setattr('builtins.input', lambda _: "")
    assert scores.get_player_name() is None


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
