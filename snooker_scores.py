import sys


class SnookerScores:
    def __init__(self):
        """Initialize SnookerScores."""
        self.red_balls = 15
        self.player_1 = "Player 1"
        self.player_2 = "Player 2"
        self.score_player_1 = 0
        self.score_player_2 = 0
        self.max_score = 147
        self.end_break = 27
        self.available_player_1 = self.max_score
        self.available_player_2 = self.max_score
        self.potential_score_player_1 = self.max_score
        self.potential_score_player_2 = self.max_score
        self.break_size = 0
        self.red_needed_next = True
        self.player_1_turn = True
        self.snookers_needed = False
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


    # Game phases 1: start the game
    def start_game(self):
        """Start the game."""
        self.display_startup_message()
        self.store_players_names()
        self.red_balls_phase()
        self.colored_balls_phase()
        self.display_winner()
        self.restart_game()

    def display_startup_message(self):
        """Display welcome message and hotkeys."""
        print(f"\t\tSnooker at its best!")

        with open("txt/hotkeys.txt") as f:
            print(f.read())

    def store_players_names(self):
        """Store players names in vars."""
        while True:
            player_names = input("Do you want to enter player names? (y/n) ").strip().lower()
            if player_names in ['y', 'n']:
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        if player_names == 'y':
            self.player_1 = self.get_player_name()
            self.player_2 = self.get_player_name()
        return

    def get_player_name(self):
        """Get the name of the player."""
        player_name = input("Enter player name: ").strip().title()
        if player_name:
            return player_name


    # Game phases 2: run of the balls
    def red_balls_phase(self):
        """Play the red balls phase of the game."""
        while self.red_balls > 0:
            shot = self.get_shot_value()

            if shot in [
                "switch",
                "scores_set",
                "penalty",
                "red_ball_down"
            ]:
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
            self.last_colored_ball_phase()
            self.colored_balls_phase()

    def last_colored_ball_phase(self):
        """Handle the last colored ball."""
        while self.available_player_1 > 0 or self.available_player_2 > 0:
            shot = self.get_shot_value()

            if shot in ["switch", "scores_set", "penalty"]:
                self.display_game_state()
                continue

            if shot == 0 and self.red_balls == 0:
                self.handle_miss()
                self.colored_balls_phase()
            elif shot < 2 or shot > 7:
                if self.player_1_turn:
                    print(f"\n{self.player_1} must pot a colored ball!")
                else:
                    print(f"\n{self.player_2} must pot a colored ball!")
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
            if self.player_1_turn:
                print(
                    f"{self.player_1} must pot a "
                    f"{self.colored_balls[self.yellow_ball]} ball"
                )
            else:
                print(
                    f"{self.player_2} must pot a "
                    f"{self.colored_balls[self.yellow_ball]} ball"
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
            if self.yellow_ball > 7:
                self.display_winner()
                self.restart_game()
                return

    def black_ball_phase(self):
        print("\n\tBlack ball phase!")
        self.display_active_player()
        
        while True:
            shot = input("Enter 0 for miss, 7 for black: ")
            if shot == "q":
                sys.exit()
            elif shot not in ["0", "7"]:
                print("0 or 7 please")
            elif int(shot) == 0:
                self.switch_players()
            elif int(shot) == 7:
                self.winner_black_ball_phase()
                break

    def winner_black_ball_phase(self):
        if self.player_1_turn:
            self.score_player_1 += 7
        else:
            self.score_player_2 += 7


    # Game phases 3: end the game
    def early_victory(self):
        """Show winner of an early victory."""
        self.display_winner()
        self.restart_game()

    def display_winner(self):
        """Display winner of the game."""
        winner = ""

        if self.score_player_1 == self.score_player_2:
            self.black_ball_phase()

        if self.score_player_1 > self.score_player_2:
            winner = self.player_1
        elif self.score_player_1 < self.score_player_2:
            winner = self.player_2

        print(
            f"\n{winner} wins! "
            f"(with a score of {max(self.score_player_1, self.score_player_2)}"
            f" vs {min(self.score_player_1, self.score_player_2)})")

    def restart_game(self):
        """Ask user if they want to play again."""
        while True:
            restart = input("Do you want to play again? (y/n) ").strip().lower()
            if restart in ['y', 'n']:
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        if restart == 'y':
            self.__init__()
            self.start_game()
        else:
            print("Bye!")
            sys.exit()


    # Set starting scores
    def set_starting_scores(self):
        """Set the starting scores for the game."""
        if not self.player_1_turn:
            self.switch_players()

        inputs = self.collect_starting_scores_inputs()
        if not inputs:
            print("Ok, back to the game then.")
            return

        red_balls, score_player_1, score_player_2 = inputs
        self.update_game_state(red_balls, score_player_1, score_player_2)

        if red_balls == 0:
            self.setup_colored_balls_phase()

        self.display_game_state()

    def collect_starting_scores_inputs(self):
        """Collect and validate all inputs for game setup."""
        try:
            red_balls_input = input(
                "Enter the number of red balls left: "
            ).strip()
            if red_balls_input.lower() == "q" or red_balls_input == "":
                return None

            red_balls = int(red_balls_input)
            if red_balls < 0 or red_balls > 15:
                print(
                    "Invalid number of red balls. "
                    "It must be between 0 and 15."
                )
                return None

            score_player_1 = self.get_player_score(self.player_1)
            if score_player_1 is None:
                return None

            score_player_2 = self.get_player_score(self.player_2)
            if score_player_2 is None:
                return None

            if not self.validate_scores(
                red_balls, score_player_1, score_player_2
            ):
                return None

            return red_balls, score_player_1, score_player_2

        except ValueError as e:
            print(f"Error: {e}. Please try again.")
            return None

    def get_player_score(self, player_name):
        """Get and validate a player's score."""
        score_input = input(f"Enter score for {player_name}: ").strip()
        if score_input.lower() == "q" or score_input == "":
            return None

        score = int(score_input)
        if score < 0:
            print("Scores must be positive values.")
            return None

        return score

    def validate_scores(self, red_balls, score_player_1, score_player_2):
        """Validate that the combined scores make sense for the game state."""
        possible_score = self.max_score - self.end_break - red_balls * 8
        if score_player_1 + score_player_2 > possible_score:
            print(f"Total score cannot exceed {possible_score}.")
            return False

        if red_balls != 15 or score_player_1 != 0 or score_player_2 != 0:
            red_balls_played = 15 - red_balls
            min_score = max(0, red_balls_played + (red_balls_played - 1) * 2)
            if score_player_1 + score_player_2 < min_score:
                print("Total score is too low.")
                return False

        return True

    def update_game_state(self, red_balls, score_player_1, score_player_2):
        """Update the game state with new values."""
        self.red_balls = red_balls
        self.red_needed_next = True
        self.yellow_ball = 2
        self.score_player_1 = score_player_1
        self.score_player_2 = score_player_2
        self.available_player_1 = red_balls * 8 + self.end_break
        self.available_player_2 = red_balls * 8 + self.end_break
        self.display_game_state()
        if self.red_balls > 0:
            self.red_balls_phase()

    def setup_colored_balls_phase(self):
        """Setup for the colored balls phase."""
        self.red_needed_next = False

        while True:
            try:
                colored_ball_input = int(input("Which colored ball is the first to play: "))
                if 2 <= colored_ball_input <= 7:
                    break
                else:
                    print("A number between 2 and 7 please")
            except ValueError:
                print("A number between 2 and 7 please")

        self.yellow_ball = colored_ball_input
        balls_played = sum(range(2, self.yellow_ball))
        self.available_player_1 -= balls_played
        self.available_player_2 -= balls_played
        self.colored_balls_phase()


    # Shot handling
    def get_shot_value(self):
        """Get the value of the shot."""
        while True:
            shot = input(self.shot_prompt).strip().lower()

            result = self.handle_hotkeys(shot)
            if result is not None:
                continue

            valid_shot = self.validate_shot(shot)
            if valid_shot is not None:
                return valid_shot

    def handle_hotkeys(self, shot):
        """Handle hotkeys."""
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
        elif shot == "r":
            self.red_ball_down()
            return "red_ball_down"
        else:
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

        print("Only numbers between 0 and 7 are valid!")
        return None


    # Ball handling
    def handle_red_ball(self, shot):
        """Handle a red ball."""
        if self.red_needed_next:
            self.handle_ball(shot, is_red_ball=True)
        else:
            print("\nYou need to hit a color!")
            self.switch_players()

    def handle_color_ball(self, shot):
        """Handle a color ball."""
        if self.red_needed_next:
            print("\nYou need to hit a red ball first!")
            self.switch_players()
        else:
            self.handle_ball(shot, is_red_ball=False)

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

    def display_next_ball(self):
        """Display the next ball to pot."""
        if self.player_1_turn:
            player = self.player_1
        else:
            player = self.player_2

        if self.red_needed_next:
            ball = "red ball"
        else:
            ball = "colored ball"

        print(f"{player} must pot a {ball} next")


    # Score handling
    def update_score(self, shot):
        """Update the score of the player."""
        if self.player_1_turn:
            self.score_player_1 += shot
        else:
            self.score_player_2 += shot

        self.break_size += shot

    def calculate_potential_scores(self):
        """Calculate potential scores for each player."""
        self.potential_score_player_1 = \
            self.score_player_1 + self.available_player_1
        self.potential_score_player_2 = \
            self.score_player_2 + self.available_player_2

    def display_game_state(self):
        """Display the current game state."""
        self.calculate_potential_scores()

        print(
            f"\t{self.player_1}: score {self.score_player_1}, "
            f"potential score {self.potential_score_player_1}"
        )
        print(
            f"\t{self.player_2}: score {self.score_player_2}, "
            f"potential score {self.potential_score_player_2}"
        )

        self.display_break_size()
        self.red_balls_left()
        self.display_snookers_needed()

    def red_balls_left(self):
        """Display the number of red balls left."""
        if self.player_1_turn and self.available_player_1 > self.end_break:
            print(f"{self.red_balls} red balls left")
            self.display_next_ball()
        elif not self.player_1_turn and self.available_player_2 > self.end_break:
            print(f"{self.red_balls} red balls left")
            self.display_next_ball()

    def display_snookers_needed(self):
        """Display the number of snookers needed."""
        if (
            self.snookers_needed is False and
            self.score_player_1 > self.score_player_2 + self.available_player_2
        ):
            print(f"{self.player_2} needs snookers!")
            self.snookers_needed = True
        elif (
            self.snookers_needed is False and
            self.score_player_2 > self.score_player_1 + self.available_player_1
        ):
            print(f"{self.player_1} needs snookers!")
            self.snookers_needed = True

    def display_active_player(self):
        if self.player_1_turn:
            active_player = self.player_1
        else:
            active_player = self.player_2

        print(f"Active player: {active_player}")

    def display_break_size(self):
        """Display the size of the current break ."""
        print(f"Break: {self.break_size}")
        

    # Handle missed balls
    def handle_miss(self):
        """Handle a miss."""
        if not self.red_needed_next:
            self.available_player_1 -= 7
        
        self.break_size = 0
        self.switch_players()
        self.display_next_ball()

    def red_ball_down(self):
        self.red_balls -= 1
        self.available_player_1 -= 8
        self.available_player_2 -= 8
        print("\tRed ball down!")

        self.red_needed_next is True
        self.switch_players()
        self.display_game_state()

    def switch_players(self):
        """Switch players."""
        print("Switching players...")
        self.player_1_turn = not self.player_1_turn
        self.display_active_player()

        if self.red_balls > 0:
            self.red_needed_next = True


    # Handle penalties
    def add_penalty(self):
        """Add penalty to the player."""
        penalty = self.get_penalty_input()
        if penalty is None:
            return
        self.apply_penalty(penalty)
        # self.switch_players()
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
                print(
                    f"Invalid input: {e}. Please enter a valid penalty value."
                )

    def apply_penalty(self, penalty_value):
        """Apply penalty to the player."""
        if self.player_1_turn:
            print(
                f"Penalty award of {penalty_value} "
                f"points applied to {self.player_1}."
            )
            self.score_player_1 += penalty_value
        else:
            print(
                f"Penalty of {penalty_value} "
                f"points applied to {self.player_2}."
            )
            self.score_player_2 += penalty_value

    def respot_balls(self):
        """Respot balls if needed."""
        while True:
            respot = input("Do you want a respot? (y/n) ").strip().lower()
            if respot in ['y', 'n']:
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        self.display_active_player()

        if respot == 'y':
            self.switch_players()
        elif self.red_balls > 0:
            self.red_needed_next = True


def main():
    scores = SnookerScores()
    scores.start_game()


if __name__ == "__main__":
    main()
