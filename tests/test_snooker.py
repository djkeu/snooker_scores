# Note: run tests: python -m unittest discover -s tests -p "test_snooker.py"

import unittest
from unittest.mock import patch
from snooker import SnookerScores

class TestSnookerScores(unittest.TestCase):

    def test_initial_state(self):
        game = SnookerScores()
        self.assertTrue(game.red_needed_next)
        self.assertTrue(game.player_1_turn)
        self.assertEqual(game.score_player_1, 0)
        self.assertEqual(game.score_player_2, 0)
        self.assertEqual(game.possible_score_player_1, 147)
        self.assertEqual(game.possible_score_player_2, 147)
        self.assertEqual(game.color_needed, 2)
        self.assertEqual(game.colored_balls, {
            2: "yellow",
            3: "green",
            4: "brown",
            5: "blue",
            6: "pink",
            7: "black",
        })
        self.assertTrue(game.first_input)

    def test_get_shot_value_quit(self):
        game = SnookerScores()
        
        # Simulate user input for 'q' to quit
        with patch('builtins.input', side_effect=['q']):
            with self.assertRaises(SystemExit):
                game.get_shot_value()

    def test_get_shot_value_set_starting_scores(self):
        game = SnookerScores()
        
        # Simulate user input for 's' to set starting scores and then provide scores
        with patch('builtins.input', side_effect=['s', '10', '20', '15', 'q']):
            with self.assertRaises(SystemExit):
                game.get_shot_value()
            self.assertFalse(game.first_input)  # Assuming set_starting_scores changes first_input to False

    def test_update_score(self):
        game = SnookerScores()
        game.update_score(5)
        self.assertEqual(game.score_player_1, 5)
        game.switch_players()
        game.update_score(3)
        self.assertEqual(game.score_player_2, 3)

    def test_switch_players(self):
        game = SnookerScores()
        self.assertTrue(game.player_1_turn)
        game.switch_players()
        self.assertFalse(game.player_1_turn)
        game.switch_players()
        self.assertTrue(game.player_1_turn)

    def test_handle_red_ball(self):
        game = SnookerScores()
        game.handle_red_ball(1)
        self.assertEqual(game.score_player_1, 1)
        self.assertEqual(game.red_balls, 14)
        self.assertFalse(game.red_needed_next)

    def test_handle_color_ball(self):
        game = SnookerScores()
        game.red_needed_next = False
        game.handle_color_ball(2)
        self.assertEqual(game.score_player_1, 2)
        self.assertTrue(game.red_needed_next)

    def test_handle_miss(self):
        game = SnookerScores()
        game.handle_miss()
        self.assertTrue(game.red_needed_next)
        self.assertFalse(game.player_1_turn)

    def test_calculate_possible_scores(self):
        game = SnookerScores()
        game.score_player_1 = 10
        game.score_player_2 = 20
        game.calculate_possible_scores()
        self.assertEqual(game.possible_score_player_1, 157)
        self.assertEqual(game.possible_score_player_2, 167)

    def test_display_game_state(self):
        game = SnookerScores()
        with patch('builtins.print') as mocked_print:
            game.display_game_state()
            mocked_print.assert_any_call("\nScore player 1: 0")
            mocked_print.assert_any_call("Possible score player 1: 147")
            mocked_print.assert_any_call("Score player 2: 0")
            mocked_print.assert_any_call("Possible score player 2: 147")
            mocked_print.assert_any_call("Red balls left: 15")

    def test_display_next_ball(self):
        game = SnookerScores()
        with patch('builtins.print') as mocked_print:
            game.display_next_ball()
            mocked_print.assert_any_call("Player 1 must pot a red ball next.")

    def test_set_starting_scores(self):
        game = SnookerScores()
        
        # Test valid input
        with patch('builtins.input', side_effect=['10', '20', '15']):
            game.set_starting_scores()
            self.assertEqual(game.score_player_1, 20)
            self.assertEqual(game.score_player_2, 15)
            self.assertEqual(game.red_balls, 10)
            self.assertEqual(game.available, 112)  # 147 - (20 + 15)
        
        # Test invalid input: negative scores
        with patch('builtins.input', side_effect=['10', '-20', '15']):
            with patch('builtins.print') as mocked_print:
                game.set_starting_scores()
                mocked_print.assert_any_call(
                    "Invalid input. Scores cannot be negative, and red balls must be between 0 and 15."
                )
        
        # Test invalid input: red balls out of range
        with patch('builtins.input', side_effect=['16', '20', '15']):
            with patch('builtins.print') as mocked_print:
                game.set_starting_scores()
                mocked_print.assert_any_call(
                    "Invalid input. Scores cannot be negative, and red balls must be between 0 and 15."
                )
        
        # Test invalid input: non-numeric values
        with patch('builtins.input', side_effect=['ten', '20', '15']):
            with patch('builtins.print') as mocked_print:
                game.set_starting_scores()
                mocked_print.assert_any_call("Invalid input. Please enter numeric values.")

    def test_red_balls_phase(self):
        game = SnookerScores()
        
        # Simulate user input for 15 red balls being potted
        with patch('builtins.input', side_effect=['1'] * 15):
            with patch('builtins.print') as mocked_print:
                game.red_balls_phase()
                self.assertEqual(game.red_balls, 0)
                self.assertEqual(game.score_player_1, 15)
                self.assertEqual(game.available, 132)  # 147 - 15 red balls
                mocked_print.assert_any_call("\nNo more red balls left! Pot the last colored ball to start the endgame.")

    def test_colored_balls_phase(self):
        game = SnookerScores()
        game.red_balls = 0
        game.available = 27
        with patch('builtins.input', side_effect=['2', '3', '4', '5', '6', '7']):
            game.colored_balls_phase()
            self.assertEqual(game.score_player_1, 27)
            self.assertEqual(game.available, 0)

if __name__ == '__main__':
    unittest.main()
