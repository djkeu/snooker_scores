import unittest
from unittest.mock import patch
from deep_snooker import SnookerGame

class TestSnookerGame(unittest.TestCase):

    def test_initial_state(self):
        game = SnookerGame()
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
        game = SnookerGame()
        
        # Simulate user input for 'q' to quit
        with patch('builtins.input', side_effect=['q']):
            with self.assertRaises(SystemExit):
                game.get_shot_value()

    def test_get_shot_value_set_starting_scores(self):
        game = SnookerGame()
        
        # Simulate user input for 's' to set starting scores and then provide scores
        with patch('builtins.input', side_effect=['s', '10', '20', '15', 'q']):
            with self.assertRaises(SystemExit):
                game.get_shot_value()
            self.assertFalse(game.first_input)  # Assuming set_starting_scores changes first_input to False

if __name__ == '__main__':
    unittest.main()
