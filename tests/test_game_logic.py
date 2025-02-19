import pytest
from unittest.mock import patch
from snooker_scores import SnookerScores

# Helper function to mock user input
def mock_input(prompt, value):
    return patch('builtins.input', return_value=value)

# Test for initial game setup
def test_initial_game_setup():
    game = SnookerScores()
    
    # Test if the starting scores and available points are set correctly
    assert game.score_player_1 == 0
    assert game.score_player_2 == 0
    assert game.available_player_1 == 147
    assert game.available_player_2 == 147
    assert game.red_balls == 15

# Test for handling red ball
def test_handle_red_ball():
    game = SnookerScores()
    
    # Test red ball logic for Player 1
    game.handle_red_ball(1)  # Player 1 pots a red ball
    assert game.red_balls == 14
    assert game.available_player_1 == 146
    assert game.available_player_2 == 139
    assert game.score_player_1 == 1
    
    # Test red ball logic for Player 2
    game.switch_players()  # Switch to Player 2
    game.handle_red_ball(1)  # Player 2 pots a red ball
    assert game.red_balls == 13
    assert game.available_player_1 == 138
    assert game.available_player_2 == 138
    assert game.score_player_2 == 1

# Test for handling color ball
def test_handle_color_ball():
    game = SnookerScores()
    
    # First handle red ball for Player 1
    game.handle_red_ball(1)
    
    # Now Player 1 pots a blue ball (shot value 5)
    game.handle_color_ball(5)
    assert game.score_player_1 == 6  # 1 (red) + 5 (blue)
    assert game.available_player_1 == 141  # 146 - 7 (blue)
    
    # Test Player 2 pots a color ball
    game.switch_players()  # Switch to Player 2
    game.handle_red_ball(1)  # Player 2 pots a red ball
    game.handle_color_ball(4)  # Player 2 pots a brown ball (shot value 4)
    assert game.score_player_2 == 5  # 1 (red) + 4 (brown)
    assert game.available_player_2 == 134  # 138 - 4 (brown)

# Test for handling miss
def test_handle_miss():
    game = SnookerScores()
    
    # First, let's pot a red and then miss
    game.handle_red_ball(1)
    game.handle_color_ball(5)
    
    # Now simulate a miss
    game.handle_miss()
    assert game.available_player_1 == 141  # Player 1's available points shouldn't change
    assert game.available_player_2 == 139  # Player 2's available points shouldn't change

# Test for switching players
def test_switch_players():
    game = SnookerScores()
    
    # Test switching players after a shot
    game.switch_players()
    assert game.player_1_turn is False
    
    game.switch_players()
    assert game.player_1_turn is True

# Test for setting starting scores
def test_set_starting_scores():
    game = SnookerScores()
    
    # Mock user input for starting scores
    with mock_input("Enter the number of red balls left: ", "15"), \
         mock_input("Enter starting score for Player 1: ", "10"), \
         mock_input("Enter starting score for Player 2: ", "15"):
        
        game.set_starting_scores()
        
    assert game.score_player_1 == 10
    assert game.score_player_2 == 15
    assert game.red_balls == 15
    assert game.available_player_1 == 147
    assert game.available_player_2 == 147

# Test for adding penalty points
def test_add_penalty():
    game = SnookerScores()
    
    # Simulate Player 1 committing a foul and adding penalty to Player 2
    with mock_input("Enter the penalty value: ", "4"):
        game.add_penalty()
    
    assert game.score_player_2 == 4  # Player 2 gets 4 points as a penalty

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
