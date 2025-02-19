import pytest
from unittest.mock import patch
from snooker_scores import SnookerScores


# Helper function to mock user input
def mock_input(prompt, value):
    return patch('builtins.input', return_value=value)


# Test for initial game setup
def test_initial_game_setup():
    game = SnookerScores()
    
    assert game.score_player_1 == 0
    assert game.score_player_2 == 0
    assert game.available_player_1 == 147
    assert game.available_player_2 == 147
    assert game.red_balls == 15

# Test red ball logic for Player 1
def test_handle_red_ball_player_1():
    game = SnookerScores()

    game.handle_red_ball(1)
    assert game.red_balls == 14
    assert game.available_player_1 == 146
    assert game.available_player_2 == 139
    assert game.score_player_1 == 1

# Test red ball logic for Player 2
def test_handle_red_ball_player_2():
    game = SnookerScores()

    game.switch_players()
    game.handle_red_ball(1)
    assert game.red_balls == 14
    assert game.available_player_2 == 146
    assert game.available_player_1 == 139
    assert game.score_player_2 == 1

def test_handle_color_ball_player_1():
    game = SnookerScores()

    game.handle_red_ball(1)
    game.handle_color_ball(5)
    assert game.score_player_1 == 6
    assert game.available_player_1 == 139

# Test for handling color ball for player 2
def test_handle_color_ball_player_2():
    game = SnookerScores()

    game.switch_players()
    game.handle_red_ball(1)
    game.handle_color_ball(4)
    assert game.score_player_2 == 5
    assert game.available_player_2 == 139

# Test for handling miss
def test_handle_miss():
    game = SnookerScores()
    
    # First, let's pot a red and then miss
    game.handle_red_ball(1)
    game.handle_color_ball(5)
    
    # Now simulate a miss
    game.handle_miss()
    assert game.available_player_1 == 139  # Player 1's available points shouldn't change
    assert game.available_player_2 == 139  # Player 2's available points shouldn't change

# Test for switching players
def test_switch_players():
    game = SnookerScores()
    
    # Test switching players after a shot
    game.switch_players()
    assert game.player_1_turn is False
    
    game.switch_players()
    assert game.player_1_turn is True

# FixMe:
# Test for setting starting scores
def test_set_starting_scores_valid_input():
    # Mocking the input function to simulate user input
    with patch('builtins.input', side_effect=[15, 50, 60]):  # Simulate the user entering 15, 50, and 60 for red balls, player 1 score, and player 2 score
        game = SnookerScores()
        game.set_starting_scores()

    # Assert that the values were set correctly
    assert game.red_balls == 15
    assert game.score_player_1 == 50
    assert game.score_player_2 == 60
    assert game.available_player_1 == 147  # Because red balls * 8 + 27 = 15*8 + 27 = 147
    assert game.available_player_2 == 147

# FixMe:
def test_set_starting_scores_invalid_input():
    # Test when invalid input is provided
    with patch('builtins.input', side_effect=["-1", "15", "50", "60"]):  # First input is invalid, then valid
        game = SnookerScores()
        game.set_starting_scores()

    # Check if the invalid input is handled correctly (red_balls should be 15, as input is reset)
    assert game.red_balls == 15
    assert game.score_player_1 == 50
    assert game.score_player_2 == 60
    
# Test for adding penalty points
def test_add_penalty_valid_input():
    # Mocking the input function to simulate user input
    with patch('builtins.input', side_effect=['5', 'n']):  # Simulating a penalty of 5 points and the response to not respot balls
        game = SnookerScores()
        game.score_player_1 = 50  # Set an initial score for Player 1
        game.score_player_2 = 40  # Set an initial score for Player 2
        game.add_penalty()

    # Check that the penalty was correctly added to Player 2's score (since it's Player 1's turn)
    assert game.score_player_2 == 45  # 40 + 5 penalty
    assert game.score_player_1 == 50  # Player 1's score should not change
    assert game.red_needed_next  # Red ball should be needed next, since no respot occurred

def test_add_penalty_invalid_input():
    # Test when invalid input is provided for penalty (invalid number and invalid respot input)
    with patch('builtins.input', side_effect=["-1", "5", "y"]):  # First input is invalid, then valid
        game = SnookerScores()
        game.score_player_1 = 50
        game.score_player_2 = 40
        game.add_penalty()

    # Assert that the penalty was correctly added after valid input
    assert game.score_player_2 == 45  # Player 2 should have 45 after penalty
    assert game.red_needed_next  # Red ball should be needed next

# Test for displaying the winner
def test_display_winner():
    game = SnookerScores()
    
    # Simulate Player 1 and Player 2 scoring points
    game.score_player_1 = 50
    game.score_player_2 = 40
    
    with patch('builtins.print') as mock_print:
        game.display_winner()
        mock_print.assert_called_with("\nPlayer 1 wins!")  # Check if Player 1 is declared winner

# Test for handling last colored ball
def test_handle_last_colored_ball():
    game = SnookerScores()
    
    # Simulate game reaching the last colored ball
    game.red_balls = 0
    game.available_player_1 = 27
    game.available_player_2 = 27
    
    # Player 1 pots the yellow ball (shot value 2)
    game.switch_players()  # Switch to Player 1
    with mock_input("What's the value of the shot: ", "2"):
        game.handle_last_colored_ball()
    
    # After potted last colored ball, the game should end
    assert game.available_player_1 == 27
    assert game.available_player_2 == 27

# FixMe:
# Test for the game flow
def test_game_flow():
    game = SnookerScores()
    
    # Simulate game flow with mock inputs
    with patch('builtins.input', side_effect=[1, 5, 2, 4, 1, 3, 'q']):
        game.red_balls_phase()  # Begin red ball phase
        game.colored_balls_phase()  # Move to colored balls phase
    
    # Check if the game flow is working, we expect Player 1 and Player 2 scores
    assert game.score_player_1 == 6
    assert game.score_player_2 == 5
