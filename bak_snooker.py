import sys


def main():
    """Calulate and display info about snooker scores."""
    snooker()


def keep_score(shot, player, score):
    """Keep the scores."""
    if player == True:
        score += shot


def snooker():
    """Calculate the available score."""
    print("This is snooker at its best!")
    available = 147
    red_needed_next = 1
    red_balls = 15
    
    player_1 = True
    player_2 = False

    score_player_1 = 0
    score_player_2 = 0

    playing = True
    while playing and available >= (27 + 7) and red_balls >= 0:
        try:
            shot = int(input("What's the value of the shot: "))

            if shot < 0 or shot > 7:
                print(f"\nYou can't score {shot} points with one shot!")
            elif shot >= 2 and shot <= 7 and red_needed_next == 0:
                available -= 7
                red_needed_next = 1
                if player_1:
                    score_player_1 += shot
                else:
                    score_player_2 += shot
            elif shot >= 2 and shot <=7 and red_needed_next == 1:
                print("\nYou need to hit a red ball first!")
                player_1 = not player_1
                player_2 = not player_2
            elif shot == 1 and red_needed_next == 0:
                print("\nYou need to hit a color!")
                player_1 = not player_1
                player_2 = not player_2
                red_needed_next = 1
            elif shot == 1:
                available -= 1
                red_needed_next = 0
                red_balls -= 1

                if player_1:
                    score_player_1 += shot
                else:
                    score_player_2 += shot
            elif shot == 0 and red_needed_next == 0:
                available -= 7
                red_needed_next = 1
            elif shot == 0:
                available -= 7
                red_needed_next = 1

                player_1 = not player_1
                player_2 = not player_2

            print(f"\nAvailable: {available}")
            print(f"Score player 1: {score_player_1}")
            print(f"Score player 2: {score_player_2}")
            print(f"Red balls left: {red_balls}")   

        except ValueError:
            print("\nOnly numbers between 0 and 7 are valid!")
            sys.exit("Quitting")

    
    print("\nEntering colored balls endgame!\n")
    needed_ball = 2

    while available > 0:
        try:
            shot = int(input("What's the value of the shot: "))

            if shot != needed_ball:
                print(f"Wrong ball!")
            elif shot == needed_ball:
                available -= needed_ball
                needed_ball += 1

            print(f"Available: {available}")        
            print(f"Score player 1: {score_player_1}")
            print(f"Score player 2: {score_player_2}")

        except ValueError:
            print("\nOnly numbers between 0 and 7 are valid!")
            sys.exit("Quitting")
            break

    print("\nNo more balls to play!")


if __name__ == "__main__":
    main()


### ToDo Section ###
"""
- Done: highest possible score: 147
- Done: check if color can be played
- Done: number of red balls
- Done: colored balls endgame
- Done: a red ball can't be followed by another red ball
- Done: active vs sitting player

- ToDo: show possible scores for each player
- ToDo: penalties for misses

- FixMe: refactor things a little bit?
"""


### Snooker rules ###
"""
Snooker game is played on pocket tables with sets of 22 balls of 52mm diameter. The balls include:

    A white cue ball
    15 red balls with 1 point value
    1 yellow ball with 2 points value
    1 green ball with 3 points value
    1 brown ball with 4 points value
    1 blue ball with 5 points value
    1 pink ball with 6 points value
    1 black ball with 7 points value

Each player can play as long as he scores points. Only the white cue ball can be played directly by the player. The goal is to score as many points as possible with the red and colored balls.

The game consists in two phases:

Player must first pocket a red ball,

Then he can take another shot for any other color ball.

When a color is pocketed it is replaced on the playing area. Another red ball is then played, then a color ball, etc.

When the last red ball and the next color have been played, the second phase begins. In this phase, all colors must be pocketed in the correct order (increasing points value).

Each time a ball is pocketed the player gets as many points as the balls value.

Points are also scored if the opponent makes the following mistakes:

    Do not touch any ball with the cue ball,
    Hitting or pocketing a wrong color ball,
    Pocketing the cue ball,
    Get a ball out of the playing area,
    Use another cue ball than the white ball,
    Push balls.

Yes, it is mandatory to aim a color ball after pocketing a red ball because it's a rule and if you hit on red again then it's a foul counted and (minimum 4 points is given to your opponent and maximum it would be a 7 points) so you have to opt for the color after potting red, you have varieties of option to choose ( yellow is of 2 points, green is of 3 points, brown is of 4 points, blue is of 5 points, pink is of 6 points and black is of 7 points) so you can go for this all options and you can only win by having more no.of points on your board.

"""
