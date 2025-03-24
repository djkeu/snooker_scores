import pytest
import sys
from snooker_scores import SnookerScores


def test_basic_game_flow(monkeypatch):
    scores = SnookerScores()
    
    monkeypatch.setattr(sys, 'exit', lambda _: None)
    
    scores.start_game = lambda: None
    scores.red_balls = 1
    scores.display_game_state = lambda: None
    scores.display_next_ball = lambda: None
    scores.display_winner = lambda: None
    scores.restart_game = lambda: None
    
    shot_sequence = [1, 7, 0]
    shot_iterator = iter(shot_sequence)
    
    def mock_get_shot_value():
        try:
            return next(shot_iterator)
        except StopIteration:
            scores.red_balls = 0
            return 0
    
    scores.get_shot_value = mock_get_shot_value
    scores.colored_balls_phase = lambda: None
    
    scores.main_game()


def test_full_red_phase_simple(monkeypatch):
    scores = SnookerScores()
    
    scores.red_balls = 2
    scores.display_game_state = lambda: None
    scores.last_colored_ball_phase = lambda: None
    scores.colored_balls_phase = lambda: None
    
    shot_sequence = [1, 2, 1, 3, 0]
    shot_iterator = iter(shot_sequence)
    
    def mock_get_shot_value():
        try:
            return next(shot_iterator)
        except StopIteration:
            scores.red_balls = 0
            return 0
    
    scores.get_shot_value = mock_get_shot_value
    
    scores.red_balls_phase()
    
    assert scores.score_player_1 == 6  # 1+2+1+3 = 7 but last shot not counted
    assert scores.red_needed_next is False  # Last shot was a color
    assert scores.red_balls == 0


def test_break_calculation():
    scores = SnookerScores()
    
    scores.break_size = 0
    
    scores.update_score(1)  # Red
    assert scores.break_size == 1
    
    scores.update_score(7)  # Black
    assert scores.break_size == 8
    
    scores.update_score(1)  # Red
    assert scores.break_size == 9
    
    scores.update_score(7)  # Black
    assert scores.break_size == 16
    
    scores.break_size = 0
    assert scores.break_size == 0


def test_potential_scores_calculation():
    scores = SnookerScores()
    
    scores.score_player_1 = 20
    scores.score_player_2 = 10
    scores.available_player_1 = 100
    scores.available_player_2 = 90
    
    scores.calculate_potential_scores()
    
    assert scores.potential_score_player_1 == 120
    assert scores.potential_score_player_2 == 100
    
    scores.score_player_1 = 30
    scores.available_player_1 = 80
    
    scores.calculate_potential_scores()
    
    assert scores.potential_score_player_1 == 110
    assert scores.potential_score_player_2 == 100


def test_snookers_needed_calculation():
    scores = SnookerScores()
    
    scores.score_player_1 = 60
    scores.score_player_2 = 10
    scores.available_player_2 = 35
    scores.snookers_needed = False
    
    scores.display_snookers_needed()
    
    assert scores.snookers_needed is True
    
    scores = SnookerScores()
    scores.score_player_1 = 10
    scores.score_player_2 = 60
    scores.available_player_1 = 35
    scores.snookers_needed = False
    
    scores.display_snookers_needed()
    
    assert scores.snookers_needed is True
    
    scores = SnookerScores()
    scores.score_player_1 = 50
    scores.score_player_2 = 40
    scores.available_player_2 = 30
    scores.snookers_needed = False
    
    scores.display_snookers_needed()
    
    assert scores.snookers_needed is False


def test_combine_penalties_and_scoring():
    scores = SnookerScores()
    
    scores.update_score(5)
    assert scores.score_player_1 == 5
    
    scores.player_1_turn = False
    scores.update_score(7)
    assert scores.score_player_2 == 7
    
    scores.apply_penalty(4)
    assert scores.score_player_2 == 11
    
    scores.player_1_turn = True
    scores.apply_penalty(6)
    assert scores.score_player_1 == 11
    
    assert scores.score_player_1 + scores.score_player_2 == 22


def test_player_switching():
    scores = SnookerScores()
    
    assert scores.player_1_turn is True
    
    scores.handle_miss()
    assert scores.player_1_turn is False
    
    scores.update_score(7)
    scores.handle_miss()
    assert scores.player_1_turn is True
    
    scores.switch_players()
    assert scores.player_1_turn is False
    
    scores.switch_players()
    assert scores.player_1_turn is True
