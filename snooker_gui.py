import tkinter as tk
from tkinter import messagebox, simpledialog
from snooker_game import SnookerGame


class SnookerGUI:
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.game = SnookerGame()
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

        self.button_starting_scores = tk.Button(
            self.root, 
            text="Set starting scores", 
            command=self.set_starting_scores
        )
        self.button_starting_scores.pack()

    def submit_shot(self):
        """Handle the shot submission."""
        shot = self.entry_shot.get()
        if shot == "q":
            self.root.quit()
        elif shot == "s":
            self.set_starting_scores()
        elif shot == "p":
            self.add_penalty()
        elif shot == "x":
            self.switch_players()
        else:
            try:
                shot = int(shot)
                if self.game.validate_shot(shot):
                    if self.game.red_balls > 0:
                        self.game.red_balls_phase(shot)
                    else:
                        self.game.handle_last_colored_ball(shot)
                    self.update_display()
            except ValueError as e:
                messagebox.showerror("Invalid Input", str(e))

    def set_starting_scores(self):
        """Set starting scores using a dialog."""
        red_balls = simpledialog.askinteger("Input", "Enter the number of red balls left:", minvalue=0, maxvalue=15)
        score_1 = simpledialog.askinteger("Input", "Enter starting score for Player 1:", minvalue=0)
        score_2 = simpledialog.askinteger("Input", "Enter starting score for Player 2:", minvalue=0)

        if red_balls is not None and score_1 is not None and score_2 is not None:
            try:
                self.game.set_starting_scores(red_balls, score_1, score_2)
                self.update_display()
            except ValueError as e:
                messagebox.showerror("Invalid Input", str(e))

    def add_penalty(self):
        """Add a penalty using a dialog."""
        penalty = simpledialog.askinteger("Input", "Enter the penalty value:", minvalue=0, maxvalue=7)
        if penalty is not None:
            try:
                self.game.add_penalty(penalty)
                self.update_display()
            except ValueError as e:
                messagebox.showerror("Invalid Input", str(e))

    def switch_players(self):
        """Switch players."""
        self.game.switch_players()
        self.update_display()

    def update_display(self):
        """Update the display with the current game state."""
        self.label_player_1.config(text=f"Player 1: score {self.game.score_player_1}, possible score {self.game.possible_score_player_1}")
        self.label_player_2.config(text=f"Player 2: score {self.game.score_player_2}, possible score {self.game.possible_score_player_2}")
        self.label_red_balls.config(text=f"{self.game.red_balls} red balls left")
        self.label_next_ball.config(text=f"{'Player 1' if self.game.player_1_turn else 'Player 2'} must pot a {'red ball' if self.game.red_needed_next else 'colored ball'} next")

    def start(self):
        """Start the GUI."""
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = SnookerGUI(root)
    app.start()
