import sys


class SnookerScores:
    def __init__(self):
        """Initialize the game scores state."""
        self.red_balls = 15
        self.available_points = (self.red_balls * 8) + 27
        self.red_needed_next = True
        self.player_1_turn = True
        self.score_player_1 = 0
        self.score_player_2 = 0
        self.possible_score_player_1 = self.available_points
        self.possible_score_player_2 = self.available_points
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
        self.prompt = self.initialize_prompt()

    # Ball handling
    def initialize_prompt(self):
        """Initialize the prompt message."""
        prompt = "What's the value of the shot: (enter 'q' to quit"
        if self.first_input:
            prompt += ", 's' to set starting scores"
        prompt += ") "
        return prompt

    def get_shot_value(self):
        """Prompt user for the shot value and handle input validation."""
        while True:
            shot = input(self.prompt)

            if shot == "q":
                sys.exit("Bye!")
            elif shot == "s" and self.first_input:
                self.set_starting_scores()
                self.first_input = False
                continue
            elif shot == 'p':
                self.add_penalty()
            elif shot == 'x':
                self.switch_players()

            if self.validate_shot(shot):
                self.first_input = False
                return int(shot)

    def validate_shot(self, shot):
        """Validate the shot value."""
        try:
            shot = int(shot)
            if 0 <= shot <= 7:
                self.first_input = False
                self.prompt = self.initialize_prompt()
                return True
            else:
                raise ValueError
        except ValueError:
            print("\nOnly numbers between 0 and 7 are valid!")
            # self.display_game_state()
            return False

    def handle_red_ball(self, shot):
        """Handle logic for when a red ball is hit."""
        if self.red_needed_next:
            self.available_points -= 1
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
            self.available_points -= 7
            self.red_needed_next = True
            self.update_score(shot)

    def handle_miss(self):
        """Handle logic for when a shot is missed."""
        if not self.red_needed_next:
            self.available_points -= 7
        self.red_needed_next = True
        self.switch_players()

    def switch_players(self):
        """Switch turns between players."""
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
                elif score_1 + score_2 + (red_balls * 8) > self.available_points:
                    print("\nTotal score must be less than 147")
                    continue

                self.score_player_1 = score_1
                self.score_player_2 = score_2
                self.red_balls = red_balls
                self.available_points = (self.red_balls * 8) + 27
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
            self.score_player_1 + self.available_points
        self.possible_score_player_2 = \
            self.score_player_2 + self.available_points

    def display_game_state(self):
        """Display the current state of the game in the desired format."""
        self.calculate_possible_scores()

        print(f"\nPlayer 1: score {self.score_player_1}, "
              f"possible score {self.possible_score_player_1}")
        print(f"Player 2: score {self.score_player_2}, "
              f"possible score {self.possible_score_player_2}")
        print(f"{self.red_balls} red balls left")

        self.display_next_ball()

    def display_next_ball(self):
        """Display which ball the current player must pot next."""
        # Note: prints possibly abundant, leave for now
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

    def add_penalty(self):
        """Add points to the other player's score."""
        while True:
            penalty = input("Enter the penalty value: ")

            try:
                penalty = int(penalty)
                if 0 <= penalty <= 7:
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Penalty must be between 0 and 7")

        if self.player_1_turn:
            self.score_player_2 += penalty
        else:
            self.score_player_1 += penalty

        self.switch_players()
        self.respot_balls()

    def respot_balls(self):
        """Respot the balls after a foul."""
        while True:
            respot = input("Do you want a respot? (y/n) ").lower()
            if respot in ['y', 'n']:
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        if respot == 'y':
            self.switch_players()
        elif self.red_balls > 0:
            self.red_needed_next = True

    # Game phases
    def display_startup_message(self):
        """Display a random startup message."""
        print("This is snooker at its best!")
        # Todo: random startup message

    def red_balls_phase(self):
        while self.red_balls > 0:
            shot = self.get_shot_value()
            print(
                f"Shot value: {shot}, "
                f"Red balls left: {self.red_balls}, "
                f"Available points: {self.available_points}")

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
        print(
            "\nNo more red balls left! "
            "Pot a colored ball to start the endgame."
        )

        while self.available_points > 0:
            shot = self.get_shot_value()

            if shot < 2 or shot > 7:
                print("\nYou must pot a colored ball!")
            else:
                self.available_points -= shot
                self.update_score(shot)
                self.display_game_state()
                break

    def colored_balls_phase(self):
        """Simulate the colored balls phase."""
        print("\nEntering colored balls endgame!\n")
        self.available_points = 27
        print(f"Available for endgame: {self.available_points}")

        while self.available_points > 0:
            print(
                f"Next ball to pot: "
                f"{self.colored_balls[self.yellow_ball]} "
                f"({self.yellow_ball} points)"
            )
            shot = self.get_shot_value()

            if shot != self.yellow_ball:
                print("Wrong ball!")
                self.switch_players()
            else:
                self.available_points -= self.yellow_ball
                self.update_score(shot)
                self.yellow_ball += 1

            self.display_game_state()

        print("\nNo more balls to play!")

    def start_game(self):
        """Start the program."""
        self.display_startup_message()
        self.red_balls_phase()
        self.colored_balls_phase()
