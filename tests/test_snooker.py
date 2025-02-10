import unittest
from unittest.mock import patch
from snooker import SnookerScores


# Note: run tests: python -m unittest discover -s tests -p "test_snooker.py"


class TestSnookerScores(unittest.TestCase):

    def test_initial_state(self):
        game = SnookerScores()
        self.assertTrue(game.red_needed_next)
        self.assertTrue(game.player_1_turn)
        self.assertEqual(game.score_player_1, 0)
        self.assertEqual(game.score_player_2, 0)
        self.assertEqual(game.possible_score_player_1, 147)
        self.assertEqual(game.possible_score_player_2, 147)
        self.assertEqual(game.needed_ball, 2)
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
        self.assertEqual(game.red_balls, 14)
        self.assertEqual(game.available, 146)
        self.assertEqual(game.score_player_1, 1)
        self.assertFalse(game.red_needed_next)

    def test_handle_color_ball(self):
        game = SnookerScores()
        game.red_needed_next = False
        game.handle_color_ball(7)
        self.assertEqual(game.available, 140)
        self.assertEqual(game.score_player_1, 7)
        self.assertTrue(game.red_needed_next)

    def test_handle_miss(self):
        game = SnookerScores()
        game.handle_miss()
        self.assertTrue(game.red_needed_next)
        self.assertFalse(game.player_1_turn)

    def test_calculate_possible_scores(self):
        game = SnookerScores()
        game.calculate_possible_scores()
        self.assertEqual(game.possible_score_player_1, 147)
        self.assertEqual(game.possible_score_player_2, 147)

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
            game.switch_players()
            game.display_next_ball()
            mocked_print.assert_any_call("Player 2 must pot a red ball next.")

    def test_play_main_game(self):
        game = SnookerScores()
        # Provide enough inputs to cover the entire main game sequence, including the transition to handle_last_colored_ball
        with patch('builtins.input', side_effect=['1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '2']):
            game.play_main_game()
            self.assertEqual(game.red_balls, 0)

    def test_handle_last_colored_ball(self):
        game = SnookerScores()
        game.red_balls = 0
        with patch('builtins.input', side_effect=['2']):
            game.handle_last_colored_ball()
            self.assertEqual(game.available, 145)

    def test_play_endgame(self):
        game = SnookerScores()
        game.red_balls = 0
        game.available = 27
        with patch('builtins.input', side_effect=['2', '3', '4', '5', '6', '7']):
            game.play_endgame()
            self.assertEqual(game.available, 0)

if __name__ == '__main__':
    unittest.main()
    