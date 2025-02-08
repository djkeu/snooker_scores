import sys


class SnookerScores:
    def __init__(self):
        """Initialize the game state."""
        self.available = 147
        self.red_balls = 15
        self.red_needed_next = True
        self.player_1_turn = True
        self.score_player_1 = 0
        self.score_player_2 = 0
        self.possible_score_player_1 = 147
        self.possible_score_player_2 = 147
        self.needed_ball = 2  # For the endgame, starts with yellow ball
        self.colored_balls = {
            2: "yellow",
            3: "green",
            4: "brown",
            5: "blue",
            6: "pink",
            7: "black",
        }
        self.first_input = True  # Initialize first_input here

    def get_shot_value(self):
        """Prompt the user for the shot value and handle input validation."""
        while True:
            if self.first_input:
                shot = input("What's the value of the shot: (enter 'q' to quit, 's' to set starting scores) ")
            else:
                shot = input("What's the value of the shot: (enter 'q' to quit) ")

            if shot == "q":
                sys.exit("Bye!")
            elif shot == "s" and self.first_input:
                self.set_starting_scores()
                continue  # Return to the input prompt after setting scores

            try:
                shot = int(shot)
                if 0 <= shot <= 7:
                    self.first_input = False  # Set first_input to False after the first valid input
                    return shot
                else:
                    print(f"\nYou can't score {shot} points with one shot!")
            except ValueError:
                print("\nOnly numbers between 0 and 7 are valid!")
                self.display_game_state()


    def set_starting_scores(self):
        """Set starting scores for both players and the number of red balls left."""
        if not self.red_needed_next:
            print("Starting scores can only be set when a red ball is needed next.")
            return

        try:
            score_1 = int(input("Enter starting score for Player 1: "))
            score_2 = int(input("Enter starting score for Player 2: "))
            red_balls = int(input("Enter the number of red balls left: "))

            if score_1 < 0 or score_2 < 0 or red_balls < 0 or red_balls > 15:
                print("Invalid input. Scores cannot be negative, and red balls must be between 0 and 15.")
                return

            self.score_player_1 = score_1
            self.score_player_2 = score_2
            self.red_balls = red_balls
            # Note:
            self.available -= (score_1 + score_2)
            self.calculate_possible_scores()
            print(f"Starting scores set: Player 1 = {self.score_player_1}, Player 2 = {self.score_player_2}")
            print(f"Red balls left: {self.red_balls}")
        except ValueError:
            print("Invalid input. Please enter numeric values.")


    def update_score(self, shot):
        """Update the current player's score."""
        if self.player_1_turn:
            self.score_player_1 += shot
        else:
            self.score_player_2 += shot


    def switch_players(self):
        """Switch turns between players."""
        self.player_1_turn = not self.player_1_turn


    def handle_red_ball(self, shot):
        """Handle logic for when a red ball is hit."""
        if self.red_needed_next:
            self.available -= 1
            self.red_balls -= 1
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
            self.available -= 7
            self.red_needed_next = True
            self.update_score(shot)


    def handle_miss(self):
        """Handle logic for when a shot is missed."""
        if not self.red_needed_next:
            # Player missed a color ball
            self.available -= 7
        self.red_needed_next = True
        self.switch_players()


    def calculate_possible_scores(self):
        """
        Calculate the possible scores for both players.
        Which is their current score plus the remaining available points
        """
        self.possible_score_player_1 = self.score_player_1 + self.available
        self.possible_score_player_2 = self.score_player_2 + self.available


    def display_game_state(self):
        """Display the current state of the game in the desired format."""
        self.calculate_possible_scores()

        print(f"\nScore player 1: {self.score_player_1}")
        print(f"Possible score player 1: {self.possible_score_player_1}")
        print(f"Score player 2: {self.score_player_2}")
        print(f"Possible score player 2: {self.possible_score_player_2}")
        print(f"Red balls left: {self.red_balls}")

        self.display_next_ball()


    def display_next_ball(self):
        """Display which ball the current player must pot next."""
        if self.red_needed_next:
            if self.player_1_turn:
                print("Player 1 must pot a red ball next.")
            else:
                print("Player 2 must pot a red ball next.")
        else:
            if self.player_1_turn:
                print("Player 1 must pot a colored ball next.")
            else:
                print("Player 2 must pot a colored ball next.")


    def play_main_game(self):
        """Simulate the main phase of the snooker game."""
        print("This is snooker at its best!")
        while self.red_balls > 0 and self.available >= 27 + 7:
            shot = self.get_shot_value()

            if shot == 0:
                self.handle_miss()
            elif shot == 1:
                self.handle_red_ball(shot)
            else:
                self.handle_color_ball(shot)

            self.display_game_state()

        if self.red_balls == 0:
            self.handle_last_colored_ball()


    def handle_last_colored_ball(self):
        """Handle the last colored ball before starting the endgame."""
        print("\nNo more red balls left! Pot the last colored ball to start the endgame.")
        while self.available > 27:
            shot = self.get_shot_value()

            if shot < 2 or shot > 7:
                print("\nYou must pot a colored ball!")
            else:
                self.available -= shot
                self.update_score(shot)
                self.display_game_state()
                break


    def play_endgame(self):
        """Simulate the endgame phase of the snooker game."""
        print("\nEntering colored balls endgame!\n")
        self.available = 27
        print(f"Available for endgame: {self.available}")

        while self.available > 0:
            print(f"Next ball to pot: {self.colored_balls[self.needed_ball]} ({self.needed_ball} points)")
            shot = self.get_shot_value()

            if shot != self.needed_ball:
                print("Wrong ball!")
                self.switch_players()
            else:
                self.available -= self.needed_ball
                self.update_score(shot)
                self.needed_ball += 1

            self.display_game_state()

        print("\nNo more balls to play!")


    def play(self):
        """Run the snooker game."""
        self.play_main_game()
        self.play_endgame()
