import sys
from random import randint
import tkinter as tk
from tkinter import messagebox, simpledialog


class SnookerScores:
    def __init__(self, root):
        """Initialize the game scores state and GUI."""
        self.root = root
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

        self.setup_gui()

    def setup_gui(self):
        """Setup the GUI components."""
        self.root.title("Snooker Scores")

        self.label_player_1 = tk.Label(self.root, text="Player 1: score 0, possible score 147")
        self.label_player_1.pack()

        self.label_player_2 = tk.Label(self.root, text="Player 2: score 0, possible score 147")
        self.label_player_2.pack()

        self.label_red_balls = tk.Label(self.root, text="15 red balls left")
        self.label_red_balls.pack()

        self.label_next_ball = tk.Label(self.root, text="Player 1 must pot a red ball next")
        self.label_next_ball.pack()

        self.entry_shot = tk.Entry(self.root)
        self.entry_shot.pack()

        self.button_shot = tk.Button(self.root, text="Submit Shot", command=self.submit_shot)
        self.button_shot.pack()

        self.button_penalty = tk.Button(self.root, text="Add Penalty", command=self.add_penalty)
        self.button_penalty.pack()

        self.button_switch = tk.Button(self.root, text="Switch Players", command=self.switch_players)
        self.button_switch.pack()

    def submit_shot(self):
        """Handle the shot submission."""
        shot = self.entry_shot.get()
        if shot == "q":
            sys.exit("Bye!")
        elif shot == "s" and self.first_input:
            self.set_starting_scores()
            self.first_input = False
            return
        elif shot == 'p':
            self.add_penalty()
            return
        elif shot == 'x':
            self.switch_players()
            return

        if self.validate_shot(shot):
            self.first_input = False
            shot = int(shot)
            if shot == 0:
                self.handle_miss()
            elif shot == 1:
                self.handle_red_ball(shot)
            else:
                self.handle_color_ball(shot)
            self.display_game_state()

    def validate_shot(self, shot):
        """Validate the shot value."""
        try:
            shot = int(shot)
            if 0 <= shot <= 7:
                return True
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Only numbers between 0 and 7 are valid!")
            return False

    def handle_red_ball(self, shot):
        """Handle logic for when a red ball is hit."""
        if self.red_needed_next:
            self.available_points -= 1
            self.red_balls -= 1
            self.red_needed_next = False
            self.update_score(shot)
        else:
            messagebox.showinfo("Invalid Shot", "You need to hit a color!")
            self.switch_players()
            self.red_needed_next = True

    def handle_color_ball(self, shot):
        """Handle logic for when a color ball is hit."""
        if self.red_needed_next:
            messagebox.showinfo("Invalid Shot", "You need to hit a red ball first!")
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
        self.display_game_state()

    def set_starting_scores(self):
        """Set starting scores and the number of red balls left."""
        # This method can be expanded to include a dialog for setting starting scores
        pass

    def update_score(self, shot):
        """Update the current player's score."""
        if self.player_1_turn:
            self.score_player_1 += shot
        else:
            self.score_player_2 += shot

    def calculate_possible_scores(self):
        """Current score plus remaining available points."""
        self.possible_score_player_1 = self.score_player_1 + self.available_points
        self.possible_score_player_2 = self.score_player_2 + self.available_points

    def display_game_state(self):
        """Display the current state of the game in the desired format."""
        self.calculate_possible_scores()

        self.label_player_1.config(text=f"Player 1: score {self.score_player_1}, possible score {self.possible_score_player_1}")
        self.label_player_2.config(text=f"Player 2: score {self.score_player_2}, possible score {self.possible_score_player_2}")

        if self.available_points > 27:
            self.label_red_balls.config(text=f"{self.red_balls} red balls left")
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

        self.label_next_ball.config(text=f"{player} must pot a {ball} next")

    def add_penalty(self):
        """Add points to the other player's score."""
        penalty = simpledialog.askinteger("Penalty", "Enter the penalty value:", minvalue=0, maxvalue=7)
        if penalty is not None:
            if self.player_1_turn:
                self.score_player_2 += penalty
            else:
                self.score_player_1 += penalty

            self.switch_players()
            self.respot_balls()

    def respot_balls(self):
        """Respot the balls after a foul."""
        respot = messagebox.askyesno("Respot", "Do you want a respot?")
        if respot:
            self.switch_players()
        elif self.red_balls > 0:
            self.red_needed_next = True

    def start_game(self):
        """Start the program."""
        self.display_game_state()

def main():
    """Show the snooker scores."""
    root = tk.Tk()
    app = SnookerScores(root)
    root.mainloop()

if __name__ == "__main__":
    main()
