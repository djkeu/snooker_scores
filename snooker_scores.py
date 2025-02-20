import sys
from random import randint


class SnookerScores:
    def __init__(self):
        """Initialize the game scores state."""
        self.red_balls = 15
        self.score_player_1 = 0
        self.score_player_2 = 0
        self.maximum_score = 147
        self.available_player_1 = self.maximum_score
        self.available_player_2 = self.maximum_score
        self.possible_score_player_1 = self.maximum_score
        self.possible_score_player_2 = self.maximum_score
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
        """Get the shot value from the user and ensure it's valid."""
        while True:
            shot = input(self.shot_prompt)

            # Handle special input (like "q", "p", "x")
            result = self.handle_special_input(shot)
            if result is not None:
                return result

            # Validate the shot and handle invalid input
            if self.validate_shot(shot):
                return int(shot)
            else:
                self.handle_invalid_input()

    def handle_special_input(self, shot):
        """Handle special inputs (e.g., 'q', 'p', 'x')."""
        if shot == "q":
            sys.exit()  # Quit the game
        elif shot == "p":
            self.add_penalty()  # Apply penalty
        elif shot == "x":
            self.switch_players()  # Switch players
        else:
            return None  # If no special input, return None to fall through to validation

    def handle_invalid_input(self):
        """Handle invalid shot input."""
        print("Only numbers between 0 and 7 are valid!")


    def validate_and_return_shot(self, shot):
        """Validate the shot input and return it as an integer."""
        if self.validate_shot(shot):
            return int(shot)
        print("Only numbers between 0 and 7 are valid!")
        return None  # This ensures the loop will keep asking for input

    def validate_shot(self, shot):
        """Validate the shot value."""
        try:
            shot = int(shot)
            if 0 <= shot <= 7:
                self.first_input = False
                return True
            else:
                raise ValueError
        except ValueError:
            print("\nOnly numbers between 0 and 7 are valid!")
            return False

    def handle_red_ball(self, shot):
        """Handle logic for when a red ball is hit."""
        if self.red_needed_next:
            self.red_balls -= 1

            if self.player_1_turn:
                self.available_player_1 -= 1
                self.available_player_2 -= 8
            else:
                self.available_player_2 -= 1
                self.available_player_1 -= 8
                
            self.red_needed_next = False
            self.update_score(shot)
        else:
            print("\nYou need to hit a color!")
            self.switch_players()
            self.red_needed_next = True

    def handle_color_ball(self, shot):
        """Handle logic for when a color ball is hit."""
        if self.red_needed_next:
            print("\nYou need to hit a red ball first!")
            self.switch_players()
            self.red_needed_next = True
        else:
            color_ball_value = shot
            if self.player_1_turn:
                self.available_player_1 -= 7
            else:
                self.available_player_2 -= 7
            self.red_needed_next = True
            self.update_score(shot)

    def handle_miss(self):
        """Handle logic for when a shot is missed."""
        if not self.red_needed_next:
            self.available_player_1 -= 7
        self.red_needed_next = True
        self.switch_players()

    def switch_players(self):
        self.player_1_turn = not self.player_1_turn

    # Score handling
    def set_starting_scores(self):
        """Set starting scores and the number of red balls left."""
        while True:
            try:
                red_balls = int(input("Enter the number of red balls left: "))
                score_1 = int(input("Enter starting score for Player 1: "))
                score_2 = int(input("Enter starting score for Player 2: "))

                if score_1 < 0 or score_2 < 0:
                    print("\nScores cannot be negative")
                    continue
                elif red_balls < 0 or red_balls > 15:
                    print("\nNumber of red balls must be between 0 and 15.")
                    continue
                elif score_1 + score_2 + (red_balls * 8) > self.maximum_score:
                    print("\nTotal score must be less than 147")
                    continue

                self.score_player_1 = score_1
                self.score_player_2 = score_2
                self.red_balls = red_balls
                self.available_player_1 = (self.red_balls * 8) + 27
                self.available_player_2 = (self.red_balls * 8) + 27
                self.calculate_possible_scores()
                self.display_game_state()
                break
            except ValueError:
                print("Invalid input. Please enter numeric values.")

    def update_score(self, shot):
        """Update the current player's score."""
        if self.player_1_turn:
            self.score_player_1 += shot
        else:
            self.score_player_2 += shot

    def calculate_possible_scores(self):
        """Current score plus remaining available points."""
        self.possible_score_player_1 = \
            self.score_player_1 + self.available_player_1
        self.possible_score_player_2 = \
            self.score_player_2 + self.available_player_2

    def display_game_state(self):
        """Display the current state of the game in the desired format."""
        self.calculate_possible_scores()

        print(f"\nPlayer 1: score {self.score_player_1}, "
              f"possible score {self.possible_score_player_1}")
        print(f"Player 2: score {self.score_player_2}, "
              f"possible score {self.possible_score_player_2}")

        if self.available_player_1 > 27:
            print(f"{self.red_balls} red balls left")
            self.display_next_ball()

    def display_next_ball(self):
        """Display which ball the current player must pot next."""
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
        """Handle penalty input and apply the penalty."""
        penalty_value = self.get_penalty_input()  # Get the penalty input from the player
        self.respot_balls()  # Switch players (not related to penalty)
        self.apply_penalty(penalty_value)  # Apply the penalty to the game

    def get_penalty_input(self):
        """Get the penalty input from the player."""
        while True:
            try:
                penalty = int(input("Enter the penalty value: "))  # Ensure valid input
                if penalty < 0:
                    raise ValueError("Penalty must be a non-negative integer.")
                return penalty
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid penalty value.")

    def apply_penalty(self, penalty_value):
        if self.player_1_turn:
            print(f"Penalty of {penalty_value} points applied to Player 1.")
            self.score_player_1 -= penalty_value
        else:
            print(f"Penalty of {penalty_value} points applied to Player 2.")
            self.score_player_2 -= penalty_value

    def get_respot_input(self):
        """Get and validate the player's choice for respotting balls."""
        while True:
            respot = input("Do you want a respot? (y/n) ").lower()
            if respot in ['y', 'n']:
                return respot
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    def respot_balls(self):
        """Respot the balls after a foul."""
        respot = self.get_respot_input()

        if respot == 'y':
            self.switch_players()
        elif self.red_balls > 0:
            self.red_needed_next = True

    # Game phases
    def display_startup_message(self):
        """Display a startup message + hotkeys."""
        with open("txt/welcome_messages.txt") as f:
            for count, line in enumerate(f):
                if count == randint(0, count):
                    welcome_message = line
        print(f"\n\t\t{welcome_message}")

        with open("txt/hotkeys.txt") as f:
            print(f.read())

    def red_balls_phase(self):
        """Take turns playing reds and colors."""
        while self.red_balls > 0:
            shot = self.get_shot_value()
            print(
                f"Shot value: {shot}, "
                f"Red balls left: {self.red_balls}, "
                f"Available points: {self.available_player_1}")

            if shot == 0:
                self.handle_miss()
            elif shot == 1:
                self.handle_red_ball(shot)
            else:
                self.handle_color_ball(shot)

            self.display_game_state()

        # After all red balls are potted, handle the last colored ball
        if self.red_balls == 0:
            self.handle_last_colored_ball()

    def handle_last_colored_ball(self):
        """Handle last ball before colored balls phase."""
        print("\nNo more red balls left! ")

        while self.available_player_1 > 0 or self.available_player_2 > 0:
            shot = self.get_shot_value()

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

        self.available_player_1 = 27
        self.available_player_2 = 27

    def colored_balls_phase(self):
        """Simulate colored balls phase."""
        while self.available_player_1 > 0:
            print(
                f"Next ball to pot: "
                f"{self.colored_balls[self.yellow_ball]} "
            )
            shot = self.get_shot_value()

            if shot != self.yellow_ball:
                print("Wrong ball!")
                self.switch_players()
            else:
                self.available_player_1 -= self.yellow_ball
                self.available_player_2 -= self.yellow_ball
                self.update_score(shot)
                self.yellow_ball += 1

            self.display_game_state()

    def display_winner(self):
        """Display the winner of the game."""
        if self.score_player_1 > self.score_player_2:
            print("\nPlayer 1 wins!")
        elif self.score_player_1 < self.score_player_2:
            print("\nPlayer 2 wins!")

    def start_game(self):
        """Start the program."""
        self.display_startup_message()
        self.red_balls_phase()
        self.colored_balls_phase()
        self.display_winner()


def main():
    """Show the snooker scores."""
    scores = SnookerScores()
    scores.start_game()


if __name__ == "__main__":
    main()
