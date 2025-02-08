from snooker import SnookerGame
# from deep_snooker import SnookerGame


def main():
    """Run the snooker game."""
    game = SnookerGame()
    game.play()


if __name__ == "__main__":
    main()



# ## ToDo Section ## #
"""
- ToDo: assign key 'p'/'f' to snookers/penalties/fouls
- ToDo: snookers needed stage
- ToDo: penalties for misses
- ToDo: possibility for putting ball back after miss
- ToDo: lose game after three misses
"""


# ## Snooker rules ## #
"""
Points are also scored if the opponent makes the following mistakes:
    Do not touch any ball with the cue ball,
    Hitting or pocketing a wrong color ball,
    Pocketing the cue ball,
    Get a ball out of the playing area,
    Use another cue ball than the white ball,
    Push balls.
"""
