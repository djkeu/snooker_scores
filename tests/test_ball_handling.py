import pytest
from snooker_scores import SnookerScores


def test_handle_red_ball():
    scores = SnookerScores()
    initial_red_balls = scores.red_balls
    
    scores._handle_red_ball(1)
    
    assert scores.red_balls == initial_red_balls - 1
    assert scores.red_needed_next is False
    assert scores.score_player_1 == 1
    assert scores.break_size == 1
    assert scores.available_player_1 == scores.MAX_BREAK - 1
    assert scores.available_player_2 == scores.MAX_BREAK - 8


def test_handle_red_ball_when_color_needed():
    scores = SnookerScores()
    scores.red_needed_next = False
    initial_red_balls = scores.red_balls - 1
    initial_player_turn = scores.player_1_turn

    scores._handle_red_ball(1)

    assert scores.red_balls == initial_red_balls
    assert scores.red_needed_next is True
    assert scores.player_1_turn != initial_player_turn


def test_handle_color_ball():
    scores = SnookerScores()
    scores.red_needed_next = False
    
    scores.handle_color_ball(5)
    
    assert scores.red_needed_next is True
    assert scores.score_player_1 == 5
    assert scores.break_size == 5
    assert scores.available_player_1 == scores.MAX_BREAK - 7


def test_handle_color_ball_when_red_needed():
    scores = SnookerScores()
    scores.red_needed_next = True
    initial_player_turn = scores.player_1_turn
    
    scores.handle_color_ball(5)
    
    assert scores.red_needed_next is True
    assert scores.score_player_1 == 0
    assert scores.break_size == 0
    assert scores.player_1_turn != initial_player_turn


def test_handle_miss():
    scores = SnookerScores()
    scores.break_size = 10
    scores.red_needed_next = True
    initial_player_turn = scores.player_1_turn
    
    scores.handle_miss()
    
    assert scores.break_size == 0
    assert scores.player_1_turn != initial_player_turn
    assert scores.red_needed_next is True


def test_handle_miss_after_color():
    scores = SnookerScores()
    scores.break_size = 10
    scores.red_needed_next = False
    scores.available_player_1 = 100
    initial_player_turn = scores.player_1_turn
    
    scores.handle_miss()
    
    assert scores.break_size == 0
    assert scores.player_1_turn != initial_player_turn
    assert scores.available_player_1 == 100 - 7


def test_red_ball_down_basic():
    scores = SnookerScores()
    initial_red_balls = scores.red_balls
    scores.red_needed_next = True

    scores.red_ball_down()

    assert scores.red_balls == initial_red_balls - 2
    assert scores.player_1_turn is True


def test_red_ball_down_when_no_reds():
    scores = SnookerScores()
    scores.red_balls = 0
    
    scores.red_ball_down()
    
    assert scores.red_balls == 0
    assert scores.player_1_turn is True
    

def test_validate_shot_valid():
    scores = SnookerScores()
    
    assert scores._validate_shot("3") == 3
    assert scores._validate_shot("0") == 0
    assert scores._validate_shot("7") == 7
    assert scores.first_input is False


def test_validate_shot_invalid():
    scores = SnookerScores()
    
    assert scores._validate_shot("8") is None
    assert scores._validate_shot("-1") is None
    assert scores._validate_shot("abc") is None
    assert scores.first_input is True
