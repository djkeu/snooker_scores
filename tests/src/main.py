import tkinter as tk
from snooker_gui import SnookerGUI


def main():
    """Start the Snooker GUI."""
    root = tk.Tk()
    app = SnookerGUI(root)
    app.start()


if __name__ == "__main__":
    main()
