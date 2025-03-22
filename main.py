from snooker_scores import SnookerScores


def main():
    """Show the snooker scores."""
    scores = SnookerScores()
    scores.start_game()
    scores.main_game()


if __name__ == "__main__":
    main()
