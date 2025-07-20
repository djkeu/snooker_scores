import pytest
from snooker_scores import SnookerScores


def test_colored_balls_phase_correct_ball(monkeypatch):
    scores = SnookerScores()
    scores.available_player_1 = 2
    scores.player_1_turn = True
    scores.yellow_ball = 2
    scores.display_colored_ball_to_play = lambda : None
    scores.display_game_state = lambda: None
    scores.display_winner = lambda: None
    scores.restart_game = lambda: None

    def mock_get_shot_value():
        return scores.yellow_ball

    scores.get_shot_value = mock_get_shot_value

    scores.colored_balls_phase()


def test_colored_balls_phase_wrong_ball(monkeypatch):
    scores = SnookerScores()
    scores.available_player_1 = 27
    scores.player_1_turn = True
    scores.yellow_ball = 2
    scores.display_colored_ball_to_play = lambda : None
    scores.display_game_state = lambda: None

    def mock_get_shot_value():
        scores.available_player_1 = 0
        return 3

    scores.get_shot_value = mock_get_shot_value

    scores.colored_balls_phase()

    assert scores.break_size == 0
    assert scores.player_1_turn is False


def test_last_colored_ball_phase_miss(monkeypatch):
    scores = SnookerScores()
    scores.red_balls = 0
    scores.available_player_1 = 20
    scores.available_player_2 = 20
    scores.player_1_turn = True
    scores.display_game_state = lambda: None

    def mock_get_shot_value():
        scores.available_player_1 = 0
        scores.available_player_2 = 0
        return 0

    scores.get_shot_value = mock_get_shot_value
    scores.colored_balls_phase = lambda: None

    scores.last_colored_ball_phase()

    assert scores.player_1_turn is False


def test_last_colored_ball_phase_invalid_ball(monkeypatch):
    scores = SnookerScores()
    scores.red_balls = 0
    scores.available_player_1 = 20
    scores.available_player_2 = 20
    scores.player_1_turn = True

    inputs = [1, 0]
    input_iterator = iter(inputs)

    def mock_get_shot_value():
        try:
            return next(input_iterator)
        except StopIteration:
            scores.available_player_1 = 0
            scores.available_player_2 = 0
            return 0

    scores.get_shot_value = mock_get_shot_value
    scores.handle_miss = lambda: None
    scores.colored_balls_phase = lambda: None

    scores.last_colored_ball_phase()


def test_last_colored_ball_phase_valid_ball(monkeypatch):
    scores = SnookerScores()
    scores.red_balls = 0
    scores.available_player_1 = 20
    scores.available_player_2 = 20
    scores.player_1_turn = True
    scores.update_score = lambda x: None
    scores.display_game_state = lambda: None

    def mock_get_shot_value():
        return 3

    scores.get_shot_value = mock_get_shot_value

    scores.last_colored_ball_phase()

    assert scores.available_player_1 == scores.END_BREAK
    assert scores.available_player_2 == scores.END_BREAK


def test_display_next_ball_red_player1():
    scores = SnookerScores()
    scores.player_1 = "John"
    scores.player_1_turn = True
    scores.red_needed_next = True

    scores.display_next_ball()


def test_display_next_ball_color_player2():
    scores = SnookerScores()
    scores.player_2 = "Mary"
    scores.player_1_turn = False
    scores.red_needed_next = False

    scores.display_next_ball()


def test_red_ball_down_no_reds():
    scores = SnookerScores()
    scores.red_balls = 0

    scores.red_ball_down()

    assert scores.red_balls == 0


def test_red_ball_down_last_red_needed():
    scores = SnookerScores()
    scores.red_balls = 1
    scores.red_needed_next = True

    scores.red_ball_down()

    assert scores.red_balls == 1


def test_red_ball_down_second_to_last_red_player_1():
    scores = SnookerScores()
    scores.player_1_turn = True
    scores.red_balls = 2
    scores.red_needed_next = True
    scores.display_game_state = lambda: None
    scores.switch_players = lambda: None
    scores.colored_balls_phase = lambda: None

    scores.red_ball_down()

    assert scores.red_balls == max(0, scores.red_balls)
    assert scores.available_player_1 == scores.MAX_BREAK - 8
    assert scores.available_player_2 == scores.MAX_BREAK - 16


def test_red_ball_down_second_to_last_red_player_2():
    scores = SnookerScores()
    scores.player_1_turn = False
    scores.red_balls = 2
    scores.red_needed_next = True
    scores.display_game_state = lambda: None
    scores.switch_players = lambda: None
    scores.colored_balls_phase = lambda: None

    scores.red_ball_down()

    assert scores.red_balls == max(0, scores.red_balls)
    assert scores.available_player_1 == scores.MAX_BREAK - 16
    assert scores.available_player_2 == scores.MAX_BREAK - 8
