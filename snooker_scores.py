import sys


class SnookerScores:
    def __init__(self):
        """Initialize SnookerScores."""
        self.red_balls = 15
        self.player_1 = "Player 1"
        self.player_2 = "Player 2"
        self.player_1_turn = True
        self.active_player = self.player_1
        self.score_player_1 = 0
        self.score_player_2 = 0
        self.MAX_BREAK = 147
        self.available_player_1 = self.MAX_BREAK
        self.available_player_2 = self.MAX_BREAK
        self.potential_score_player_1 = self.MAX_BREAK
        self.potential_score_player_2 = self.MAX_BREAK
        self.END_BREAK = 27
        self.break_size = 0
        self.century_break = False
        self.red_needed_next = True
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
        self.shot_prompt = "\nWhat's the value of the shot: "

    # Game phases 1: set up the game

    def set_up_game(self):
        """Show and get information before starting the game."""
        self.display_startup_message()
        self.display_hotkeys()
        self.store_players_names()

    def display_startup_message(self):
        """Display welcome message and hotkeys."""
        print(f"\t\tSnooker at its best!")

    def display_hotkeys(self):
        """Display hotkeys."""
        with open("txt/hotkeys.txt") as f:
            print(f.read())

    def store_players_names(self):
        """Store players names."""
        if self.prompt_for_player_names():
            self.player_1 = self.get_player_name()
            self.player_2 = self.get_player_name()
            self.display_active_player()

    def prompt_for_player_names(self):
        """Ask user if they want to enter custom player names."""
        while True:
            response = input(
                "Do you want to enter player names? (y/n) "
            ).strip().lower()

            if response in ['y', 'n']:
                return response == 'y'
            print("Invalid input. Please enter 'y' or 'n'.")

    def get_player_name(self):
        """Get and return the name of a player."""
        while True:
            player_name = input("Enter player name: ").strip().title()
            if player_name:
                return player_name
            print("Please enter the player name")

    # Game phases 2: run of the balls

    def red_balls_phase(self):
        """Play the red balls phase of the game."""
        while self.red_balls > 0:
            shot = self.get_shot_value()

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

            if shot == 0 and self.red_balls == 0:
                self.handle_miss()
                self.colored_balls_phase()
                continue

            if shot < 2 or shot > 7:
                self.active_player = (
                    self.player_1 if self.player_1_turn else self.player_2
                )
                print(f"\n{self.active_player} must play a colored ball!")
                continue

            if self.player_1_turn:
                self.available_player_1 -= 7
            else:
                self.available_player_2 -= 7

            self.update_score(shot)
            self.display_game_state()
            break

        self.available_player_1 = self.END_BREAK
        self.available_player_2 = self.END_BREAK

    def colored_balls_phase(self):
        """Play the colored balls phase of the game."""
        while self.available_player_1 > 0:
            self.active_player = (
                self.player_1 if self.player_1_turn else self.player_2
            )

            self.display_colored_ball_to_play()
            shot = self.get_shot_value()

            if shot != self.yellow_ball:
                print(
                    f"{self.active_player} failed to pot the "
                    f"{self.colored_balls[self.yellow_ball]} ball!"
                )
                self.break_size = 0
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
            self.exit_game()
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
        elif shot == "f":
            self.handle_free_ball()
            return "free_ball"
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
            self.red_balls -= 1
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
            self.active_player = self.player_1
        else:
            self.active_player = self.player_2

        if self.red_needed_next:
            ball = "red ball"
        else:
            ball = "colored ball"

        print(f"{self.active_player} must play a {ball} next")

    def display_colored_ball_to_play(self):
        """Display which colored ball should be played next."""
        print(
            f"{self.active_player} must play the "
            f"{self.colored_balls[self.yellow_ball]} ball"
        )

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
        self.display_break_size()
        self.display_century_break()

        print(
            f"\t{self.player_1}: score {self.score_player_1}, "
            f"potential score {self.potential_score_player_1}"
        )
        print(
            f"\t{self.player_2}: score {self.score_player_2}, "
            f"potential score {self.potential_score_player_2}"
        )

        self.display_snookers_needed()
        self.red_balls_left()

    def red_balls_left(self):
        """Display the number of red balls left."""
        if (
            self.player_1_turn and self.available_player_1 > self.END_BREAK
        ):
            print(f"{self.red_balls} red balls left")
            self.display_next_ball()
        elif (
            not self.player_1_turn and self.available_player_2 > self.END_BREAK
        ):
            print(f"{self.red_balls} red balls left")
            self.display_next_ball()

    def display_snookers_needed(self):
        """Display if snookers are needed."""
        while self.snookers_needed is False:
            if (
                self.score_player_1 > self.score_player_2 + self.available_player_2  # noqa: W501
            ):
                print(f"{self.player_2} needs snookers!")
                self.snookers_needed = True
            elif (
                self.score_player_2 > self.score_player_1 + self.available_player_1  # noqa: W501
            ):
                print(f"{self.player_1} needs snookers!")
                self.snookers_needed = True
            break

    def display_active_player(self):
        """Display the name of the active player."""
        if self.player_1_turn:
            self.active_player = self.player_1
        else:
            self.active_player = self.player_2

        print(f"Active player: {self.active_player}")

    def display_break_size(self):
        """Display the size of the current break ."""
        if self.break_size > 0:
            print(f"Break: {self.break_size}")

    def display_century_break(self):
        """Signal if a player has made a century break."""
        if self.century_break is False and self.break_size >= 100:
            print("Century break!")
            self.century_break = True

    # Handle missed balls
    def handle_miss(self):
        """Handle a miss."""
        if not self.red_needed_next:
            if self.player_1_turn:
                self.available_player_1 -= 7
            else:
                self.available_player_2 -= 7

        self.break_size = 0
        self.switch_players()
        # self.display_next_ball()

    def red_ball_down(self):
        """Handle an accidentally potted red ball."""
        no_reds_available = "No reds available to accidentally pot!"

        if self.red_balls == 0:
            print(no_reds_available)
            return
        elif self.red_needed_next and self.red_balls == 1:
            print(no_reds_available)
            return

        print("\tRed ball down!")
        self.break_size = 0

        if self.red_needed_next and self.red_balls >= 2:
            self.red_balls = max(0, self.red_balls - 2)

            if self.player_1_turn:
                self.available_player_1 -= 8
                self.available_player_2 -= 16
            else:
                self.available_player_1 -= 16
                self.available_player_2 -= 8

            self.red_needed_next = False
            self.display_game_state()
            if self.red_balls == 0:
                self.colored_balls_phase()
            return

        self.red_balls = max(0, self.red_balls - 1)
        if self.player_1_turn:
            self.available_player_1 -= 15
            self.available_player_2 -= 8
        else:
            self.available_player_1 -= 8
            self.available_player_2 -= 15

        self.switch_players()
        self.display_game_state()

        if self.red_balls == 0:
            self.colored_balls_phase()

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
        self.display_game_state()
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

        if respot == 'y':
            self.switch_players()
        elif self.red_balls > 0:
            self.red_needed_next = True
        else:
            self.red_needed_next = False

    def handle_free_ball(self):
        """In case a player gets to play a 'free ball'."""
        print("\tFree ball!")
        if self.red_balls > 0:
            free_ball = 1
        else:
            free_ball = self.yellow_ball

        if self.player_1_turn:
            self.score_player_1 += free_ball
        else:
            self.score_player_2 += free_ball

        self.display_free_ball(free_ball)

    def display_free_ball(self, free_ball):
        """Display which player gets the points of the free ball."""
        if self.player_1_turn:
            self.active_player = self.player_1
        else:
            self.active_player = self.player_2

        if free_ball == 1:
            print(f"{free_ball} point for {self.active_player}")
        else:
            print(f"{free_ball} points for {self.active_player}")

        # FixMe: Refactor
        if self.red_balls > 0:
            self.display_next_ball()
        else:
            self.display_colored_ball_to_play()

    # Set starting scores
    def set_starting_scores(self):
        """Set scores for an ongoing game."""
        if not self.player_1_turn:
            self.switch_players()

        inputs = self.get_starting_scores()
        if not inputs:
            print("Ok, back to the game then.")
            return

        self.break_size = 0
        self.snookers_needed = False
        red_balls, score_player_1, score_player_2 = inputs
        self.update_game_state(red_balls, score_player_1, score_player_2)

        if red_balls == 0:
            self.setup_colored_balls_phase()

        self.display_game_state()

    def get_starting_scores(self):
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
        possible_score = self.MAX_BREAK - self.END_BREAK - red_balls * 8
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
        self.break_size = 0
        self.snookers_needed = False
        self.warn_incorrect_break_size()

        self.score_player_1 = score_player_1
        self.score_player_2 = score_player_2
        self.available_player_1 = red_balls * 8 + self.END_BREAK
        self.available_player_2 = red_balls * 8 + self.END_BREAK
        self.display_game_state()
        if self.red_balls > 0:
            self.red_balls_phase()

    def warn_incorrect_break_size(self):
        """Warn about incorrect break size."""
        print(
            "Warning: displayed break size does not match actual break size. "
        )

    def setup_colored_balls_phase(self):
        """Setup for the colored balls phase."""
        self.red_needed_next = False
        while True:
            colored_ball_input = input(
                "Which colored ball is the first to play: "
            ).strip()

            if colored_ball_input.lower() == "q":
                self.exit_game()

            try:
                colored_ball_input = int(colored_ball_input)
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

    def black_ball_phase(self):
        """Respot black ball after a tie."""
        print("\n\tBlack ball phase!")
        self.display_active_player()

        while True:
            shot = input("Enter 0 for miss, 7 for black: ")
            if shot == "q":
                self.exit_game()
            elif shot not in ["0", "7"]:
                print("0 or 7 please")
            elif int(shot) == 0:
                self.switch_players()
            elif int(shot) == 7:
                self.winner_black_ball_phase()
                break

    def winner_black_ball_phase(self):
        """Apply points to the winner of the black ball phase."""
        if self.player_1_turn:
            self.score_player_1 += 7
        else:
            self.score_player_2 += 7

    def restart_game(self):
        """Ask user if they want to play again."""
        while True:
            restart = input(
                "Do you want to play again? (y/n) "
            ).strip().lower()

            if restart in ['y', 'n']:
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        if restart == 'y':
            self.__init__()
            self.set_up_game()
            self.red_balls_phase()
            self.display_winner()
            # self.restart_game()
        else:
            self.exit_game()

    def exit_game(self):
        """Exit the game."""
        print("Bye!")
        sys.exit(0)


def main():
    """Show the snooker scores."""
    scores = SnookerScores()
    scores.set_up_game()
    scores.red_balls_phase()
    scores.display_winner()
    scores.restart_game()


if __name__ == "__main__":
    main()
