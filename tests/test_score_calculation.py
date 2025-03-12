import pytest
from unittest.mock import patch
from snooker_scores import SnookerScores


def mock_input(prompt, value):
    return patch('builtins.input', return_value=value)


def test_apply_penalty():
    game = SnookerScores()
    game.score_player_1 = 50
    game.score_player_2 = 40

    game.apply_penalty(5)
    assert game.score_player_1 == 55
    assert game.score_player_2 == 40

    game.switch_players()
    game.apply_penalty(5)
   
    assert game.score_player_1 == 55
    assert game.score_player_2 == 45

def test_apply_penalty_edge_cases():
    game = SnookerScores()
    game.player_1_turn = True
    game.apply_penalty(5)
    assert game.score_player_1 == 5
    assert game.score_player_2 == 0
    game.player_1_turn = False
    game.apply_penalty(3)
    assert game.score_player_1 == 5
    assert game.score_player_2 == 3


def test_add_penalty_valid():
    with patch('builtins.input', side_effect=['5', 'n']):
        game = SnookerScores()
        game.score_player_1 = 50
        game.score_player_2 = 40

        game.add_penalty()
    
    assert game.score_player_1 == 55
    assert game.score_player_2 == 40

def test_add_penalty_invalid():
    with patch('builtins.input', side_effect=['-1', '5', 'y']):
        game = SnookerScores()
        game.score_player_1 = 50
        game.score_player_2 = 40

        game.add_penalty()

    assert game.score_player_1 == 55
    assert game.score_player_2 == 40

def test_add_penalty_edge_cases_2():
    game = SnookerScores()
    with patch("builtins.input", side_effect=["-1", "5", "n"]):
        game.add_penalty()
    assert game.score_player_1 == 5
    assert game.score_player_2 == 0


def test_update_score_edge_cases():
    game = SnookerScores()
    game.player_1_turn = True
    game.update_score(5)
    assert game.score_player_1 == 5
    game.player_1_turn = False
    game.update_score(3)
    assert game.score_player_2 == 3


def test_calculate_potential_scores_edge_cases():
    game = SnookerScores()
    game.score_player_1 = 10
    game.score_player_2 = 20
    game.available_player_1 = 30
    game.available_player_2 = 40
    game.calculate_potential_scores()
    assert game.potential_score_player_1 == 40
    assert game.potential_score_player_2 == 60
