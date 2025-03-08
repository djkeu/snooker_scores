import sys
from random import randint


MAXIMUM_BREAK = 147
END_BREAK = 27


class SnookerScores:
    def __init__(self):
        """Initialize SnookerScores."""
        self.red_balls = 15
        self.player_1 = "Player 1"
        self.player_2 = "Player 2"
        self.score_player_1 = 0
        self.score_player_2 = 0
        self.max_score = MAXIMUM_BREAK
        self.available_player_1 = self.max_score
        self.available_player_2 = self.max_score
        self.potential_score_player_1 = self.max_score
        self.potential_score_player_2 = self.max_score
        self.end_break = END_BREAK
        self.red_needed_next = True
        self.player_1_turn = True
        self.yellow_ball = 2
        self.colored_balls = {
            2: "yellow",
            3: "green",
            4: "brown",
            5: "blue",
            6: "pink",
            7: "black",
        }
        self.first_input = True
        self.shot_prompt = "What's the value of the shot: "


    # Ball handling
    def get_shot_value(self):
        """Get the value of the shot."""
        while True:
            shot = input(self.shot_prompt).strip().lower()

            result = self.handle_special_input(shot)
            if result is not None:
                continue

            valid_shot = self.validate_shot(shot)
            if valid_shot is not None:
                return valid_shot

    def handle_special_input(self, shot):
        """Handle special input."""
        if shot == "q":
            sys.exit()
        elif shot == "p":
            self.add_penalty()
            return "penalty"
        elif shot == "x":
            self.switch_players()
            return "switch"
        elif shot == "s":
            self.set_starting_scores()
            return "scores_set"
        elif shot == "w":
            self.early_victory()
            return "winner"
        else:
            return None

    def validate_and_return_shot(self, shot):
        """Validate the shot and return it."""
        validated_shot = self.validate_shot(shot)
        if validated_shot is not None:
            return int(validated_shot)
        return None

    def validate_shot(self, shot):
        """Validate the shot."""
        try:
            shot = int(shot)
            if shot >= 0 and shot <= 7:
                self.first_input = False
                return shot
        except ValueError:
            pass

        self.handle_invalid_input()
        return None

    def handle_invalid_input(self):
        """Handle invalid input."""
        print("Only numbers between 0 and 7 are valid!")

    def handle_ball(self, shot, is_red_ball):
        """Handle a ball."""
        if is_red_ball:
            self.red_balls -= 1
            if self.player_1_turn:
                self.available_player_1 -= 1
                self.available_player_2 -= 8
            else:
                self.available_player_2 -= 1
                self.available_player_1 -= 8
            self.red_needed_next = False
        else:
            if self.player_1_turn:
                self.available_player_1 -= 7
            else:
                self.available_player_2 -= 7
            self.red_needed_next = True

        self.update_score(shot)

    def handle_red_ball(self, shot):
        """Handle a red ball."""
        if self.red_needed_next:
            self.handle_ball(shot, is_red_ball=True)
        else:
            print("\nYou need to hit a color!")
            self.switch_players()
            self.red_needed_next = True

    def handle_color_ball(self, shot):
        """Handle a color ball."""
        if self.red_needed_next:
            print("\nYou need to hit a red ball first!")
            self.switch_players()
            self.red_needed_next = True
        else:
            self.handle_ball(shot, is_red_ball=False)

    def handle_miss(self):
        """Handle a miss."""
        if not self.red_needed_next:
            self.available_player_1 -= 7
        self.red_needed_next = True
        self.switch_players()

    def switch_players(self):
        """Switch players."""
        print("Switching players...")
        self.player_1_turn = not self.player_1_turn

        self.display_game_state()


    # Score handling
    def set_starting_scores(self):
        """Set the starting scores for the game."""
        while True:
            try:
                self.red_balls = self.get_input_starting_scores(
                    "Enter the number of red balls left: ",
                    self.validate_red_balls
                )
                if self.red_balls is None:
                    return

                score_player_1 = self.get_input_starting_scores(
                    "Enter score for Player 1: ",
                    lambda x: self.validate_player_scores(x, 0)
                )
                if score_player_1 is None:
                    return

                score_player_2 = self.get_input_starting_scores(
                    "Enter score for Player 2: ",
                    lambda x: self.validate_player_scores(score_player_1, x)
                )
                if score_player_2 is None:
                    return

                self.validate_player_scores(score_player_1, score_player_2)
                self.validate_min_score(self.red_balls, score_player_1, score_player_2)

                self.red_needed_next = True
                self.score_player_1 = score_player_1
                self.score_player_2 = score_player_2
                self.available_player_1 = self.red_balls * 8 + self.end_break
                self.available_player_2 = self.red_balls * 8 + self.end_break
 
                self.display_game_state()
                break

            except ValueError as e:
                print(f"Error: {e}. Please try again.")

    def get_input_starting_scores(self, prompt, validation_func):
        """Get and validate input for set_starting_scores."""
        while True:
            try:
                value = input(prompt).strip()
                if value.lower() == "q":
                    return None
                value = int(value)
                validation_func(value)
                return value
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    def validate_red_balls(self, red_balls):
        """Validate that the number of red balls is within the allowed range."""
        if red_balls < 0 or red_balls > 15:
            raise ValueError("Invalid number of red balls. It must be between 0 and 15.")

    def validate_player_scores(self, score_player_1, score_player_2):
        """Validate that the scores are within the allowed range."""
        if score_player_1 < 0 or score_player_2 < 0:
            raise ValueError("Scores must be positive values.")
    
        possible_score = self.max_score - self.end_break - self.red_balls * 8
        if score_player_1 + score_player_2 > possible_score:
            raise ValueError(f"Total score cannot exceed {possible_score}.")

    def validate_min_score(self, red_balls, score_player_1, score_player_2):
        """Validate that the total score is not too low. """
        if red_balls == 15 and score_player_1 == 0 and score_player_2 == 0:
            return
        
        red_balls_played = 15 - red_balls
        min_score = max(0, red_balls_played + (red_balls_played - 1) * 2)
    
        if score_player_1 + score_player_2 < min_score:
            raise ValueError("Total score is too low.")

    def update_score(self, shot):
        """Update the score of the player."""
        if self.player_1_turn:
            self.score_player_1 += shot
        else:
            self.score_player_2 += shot

    def calculate_potential_scores(self):
        """Calculate potential scores for each player."""
        self.potential_score_player_1 = \
            self.score_player_1 + self.available_player_1
        self.potential_score_player_2 = \
            self.score_player_2 + self.available_player_2

    def display_game_state(self):
        """Display the current game state."""
        self.calculate_potential_scores()

        print(f"\n{self.player_1}: score {self.score_player_1}, "
              f"potential score {self.potential_score_player_1}")
        print(f"{self.player_2}: score {self.score_player_2}, "
              f"potential score {self.potential_score_player_2}")

        if self.available_player_1 > self.end_break:
            print(f"{self.red_balls} red balls left")
            self.display_next_ball()

    def display_next_ball(self):
        """Display the next ball to pot."""
        if self.player_1_turn:
            player = "Player 1"
        else:
            player = "Player 2"

        if self.red_needed_next:
            ball = "red ball"
        else:
            ball = "colored ball"

        print(f"{player} must pot a {ball} next")

    def add_penalty(self):
        """Add penalty to the player."""
        penalty = self.get_penalty_input()
        if penalty is None:
            return
        self.apply_penalty(penalty)
        self.switch_players()
        self.respot_balls()

    def get_penalty_input(self):
        """Get input for penalty."""
        while True:
            try:
                penalty = input("Enter the penalty value: ").strip()
                if penalty.lower() == "q":
                    return None
                penalty = int(penalty)
                if penalty < 0:
                    raise ValueError("Penalty must be a non-negative integer.")
                return penalty
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid penalty value.")

    def apply_penalty(self, penalty_value):
        """Apply penalty to the player."""
        if self.player_1_turn:
            print(f"Penalty of {penalty_value} points applied to {self.player_2}.")
            self.score_player_2 += penalty_value
        else:
            print(f"Penalty of {penalty_value} points applied to {self.player_1}.")
            self.score_player_1 += penalty_value

    def get_respot_input(self):
        """Get input for respotting balls."""
        while True:
            respot = input("Do you want a respot? (y/n) ").strip().lower()
            if respot in ['y', 'n']:
                return respot
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    def respot_balls(self):
        """Respot balls if needed."""
        respot = self.get_respot_input()

        if respot == 'y':
            self.switch_players()
        elif self.red_balls > 0:
            self.red_needed_next = True


    # Game phases
    def display_startup_message(self):
        """Display welcome message and hotkeys."""
        with open("txt/welcome_messages.txt") as f:
            for count, line in enumerate(f):
                if count == randint(0, count):
                    welcome_message = line
        print(f"\n\t\t{welcome_message}")

        with open("txt/hotkeys.txt") as f:
            print(f.read())

    def store_players_names(self):
        """Store players names in vars."""
        player_names = input("Do you want to enter player names? (y/n) ").strip().lower()
    
        if player_names == 'y':
            self.player_1 = self.get_player_name()
            self.player_2 = self.get_player_name()
        return

    def get_player_name(self):
        """Get the name of the player."""
        player_name = input("Enter your name: ").strip().capitalize()
        if player_name:
            return player_name


    def red_balls_phase(self):
        """Play the red balls phase of the game."""
        while self.red_balls > 0:
            shot = self.get_shot_value()

            if shot in ["switch", "scores_set", "penalty"]:
                self.display_game_state()
                continue

            if shot == 0:
                self.handle_miss()
            elif shot == 1:
                self.handle_red_ball(shot)
            else:
                self.handle_color_ball(shot)

            self.display_game_state()

        if self.red_balls == 0:
            self.handle_last_colored_ball()
            self.colored_balls_phase()

    def handle_last_colored_ball(self):
        """Handle the last colored ball."""
        print("\nNo more red balls left! ")

        while self.available_player_1 > 0 or self.available_player_2 > 0:
            shot = self.get_shot_value()

            if shot in ["switch", "scores_set", "penalty"]:
                self.display_game_state()
                continue

            if shot < 2 or shot > 7:
                print("\nYou must pot a colored ball!")
            else:
                if self.player_1_turn:
                    self.available_player_1 -= 7
                    self.update_score(shot)
                else:
                    self.available_player_2 -= 7
                    self.update_score(shot)

                self.display_game_state()
                break

        self.available_player_1 = self.end_break
        self.available_player_2 = self.end_break

    def colored_balls_phase(self):
        """Play the colored balls phase of the game."""
        while self.available_player_1 > 0:
            print(
                f"Next ball to pot: "
                f"{self.colored_balls[self.yellow_ball]} "
            )
            shot = self.get_shot_value()

            if shot in ["switch", "scores_set", "penalty"]:
                self.display_game_state()
                continue

            if shot != self.yellow_ball:
                print("Wrong ball!")
                self.switch_players()
            else:
                self.available_player_1 -= self.yellow_ball
                self.available_player_2 -= self.yellow_ball
                self.update_score(shot)
                self.yellow_ball += 1

            self.display_game_state()

    def start_game(self):
        """Start the game."""
        self.display_startup_message()
        self.store_players_names()
        self.red_balls_phase()
        self.colored_balls_phase()
        self.display_winner()
        self.restart_game()

    def display_winner(self):
        """Display winner of the game."""
        winner = ""

        if self.score_player_1 > self.score_player_2:
            winner = self.player_1
        elif self.score_player_1 < self.score_player_2:
            winner = self.player_2

        print(f"\n{winner} wins! (with a score of {max(self.score_player_1, self.score_player_2)} vs {min(self.score_player_1, self.score_player_2)})")

    def early_victory(self):
        """Show winner of an early victory."""
        self.display_winner()
        self.restart_game()

    def restart_game(self):
        """Ask user if they want to play again."""
        restart = input("Do you want to play again? (y/n) ").strip().lower()
        if restart == 'y':
            self.__init__()
            self.start_game()
        else:
            print("Bye!")
            sys.exit()
    
def main():
    scores = SnookerScores()
    scores.start_game()


if __name__ == "__main__":
    main()