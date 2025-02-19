import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import Toplevel, Label, Entry, Button

from snooker_game import SnookerGame


class StartingScoresDialog(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Set Starting Scores")
        self.parent = parent
        self.result = None

        # Set background color for the dialog
        self.configure(bg="lightgrey")

        # Add input fields
        Label(self, text="Number of red balls left (0-15):", bg="lightgray").grid(row=0, column=0, padx=10, pady=5)
        self.red_balls_entry = Entry(self)
        self.red_balls_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(self, text="Starting score for Player 1:", bg="lightgray").grid(row=1, column=0, padx=10, pady=5)
        self.score_1_entry = Entry(self)
        self.score_1_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(self, text="Starting score for Player 2:", bg="lightgray").grid(row=2, column=0, padx=10, pady=5)
        self.score_2_entry = Entry(self)
        self.score_2_entry.grid(row=2, column=1, padx=10, pady=5)

        # Add submit button
        Button(self, text="Submit", command=self.on_submit, bg="lightgray").grid(row=3, column=0, columnspan=2, pady=10)

        # Center the dialog on the screen
        self.center_dialog()

    def center_dialog(self):
        """Center the dialog on the screen."""
        self.update_idletasks()  # Ensure the window dimensions are up-to-date
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 4) - (height // 2)
        self.geometry(f"+{x}+{y}")

    def on_submit(self):
        """Handle the submit button click."""
        try:
            red_balls = int(self.red_balls_entry.get())
            score_1 = int(self.score_1_entry.get())
            score_2 = int(self.score_2_entry.get())
            self.result = (red_balls, score_1, score_2)
            self.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers.")

    def show(self):
        """Show the dialog and wait for a result."""
        self.wait_window()
        return self.result
    

class SnookerGUI:
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.game = SnookerGame()
        self.setup_gui()

    def setup_gui(self):
        """Setup the GUI components."""
        window_width = 440
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int(screen_height / 5)

        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")  # Set the window size to 400x400 and position it
        self.root.title("Snooker Scores")
        self.root.configure(bg="darkgreen")  # Set the background color of the window

        # Add heading
        self.label_heading = tk.Label(self.root, text="Snooker Scores", fg="white", bg="darkgreen", font=("Helvetica", 20, "bold"))
        self.label_heading.pack(padx=10, pady=10)

        self.label_player_1 = tk.Label(self.root, text="Player 1: score 0, possible score 147")

        self.label_player_1.pack(padx=10, pady=5)

        self.label_player_2 = tk.Label(self.root, text="Player 2: score 0, possible score 147")
        self.label_player_2.pack(padx=10, pady=5)

        self.label_red_balls = tk.Label(self.root, text="15 red balls left")
        self.label_red_balls.pack(padx=10, pady=5)

        self.label_next_ball = tk.Label(self.root, text="Player 1 must pot a red ball")
        self.label_next_ball.pack(padx=10, pady=5)

        self.entry_shot = tk.Entry(self.root)
        self.entry_shot.pack(padx=10, pady=5)

        self.entry_shot.bind("<Return>", lambda event: self.submit_shot())      
        self.button_shot = tk.Button(self.root, text="Submit Shot", command=self.submit_shot)
        self.button_shot.pack(padx=10, pady=5)

        self.button_penalty = tk.Button(self.root, text="Add Penalty", command=self.add_penalty)
        self.button_penalty.pack(padx=10, pady=5)

        self.button_switch = tk.Button(self.root, text="Switch Players", command=self.switch_players)
        self.button_switch.pack(padx=10, pady=5)

        self.button_starting_scores = tk.Button(
            self.root, 
            text="Set starting scores", 
            command=self.set_starting_scores
        )
        self.button_starting_scores.pack(padx=10, pady=5)

        # Bind the Escape key to quit the game
        self.root.bind("<Escape>", lambda event: self.root.quit())

    def submit_shot(self):
        """Handle the shot submission."""
        shot = self.entry_shot.get()  # Get the value from the input field

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
                    elif self.game.available_points > 27:
                        self.game.handle_last_colored_ball(shot)
                    else:
                        self.game.colored_balls_phase(shot)
                    # Update possible scores
                    self.game.calculate_possible_scores()
                    self.update_display()
            except ValueError as e:
                # Debugging: Print a message to verify this block is being executed
                print("Error block executed")
                # Display the error message in a message box
                messagebox.showerror("Invalid Input", "Only numbers between 0 and 7 are valid!")

        # Clear the input field after processing the shot
        self.entry_shot.delete(0, tk.END)
        # Set focus back to the input field
        self.entry_shot.focus_set()

    def set_starting_scores(self):
        """Set starting scores using a custom dialog."""
        dialog = StartingScoresDialog(self.root)
        result = dialog.show()

        if result:
            red_balls, score_1, score_2 = result
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
        self.label_next_ball.config(text=f"{'Player 1' if self.game.player_1_turn else 'Player 2'} must pot a {'red ball' if self.game.red_needed_next else 'colored ball'}")

    def start(self):
        """Start the GUI."""
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = SnookerGUI(root)
    app.start()
