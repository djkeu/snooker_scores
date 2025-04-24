from snooker_scores import SnookerScores


def main():
    """Show the snooker scores."""
    scores = SnookerScores()
    scores.set_up_game()
    scores.red_balls_phase()
    scores.display_winner()
    scores.restart_game()


if __name__ == "__main__":
    main()
