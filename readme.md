# Snooker Scores
##### Description:
Program to display scores of a snooker game.

##### Note: 
The filename differs from the name of the program: snooker.py vs Snooker Scores. For practical purposes this will remain the case for the time being.


### Purpose program
Watching a snooker game, it can be pretty confusing when it comes to seeing how many possible points are left for each player to score. This is mainly because it differs if a player misses a red ball or a colored ball: if a colored ball is missed, the next ball to pot must be a red ball. This means that the lost colored ball will no longer be available.

This program was/is being written to display how many points are still available throughout the game. This could only be achieved by having the logic follow the games dynamics and rules. As a (desirable) side-effect, the program also shows the current scores and which balls are to be played next. 


### ToDo Section
- ToDo: add more info to readme.md
- ToDo: add penalty prompt
- ToDo: prompt if players switch after penalty
- ToDo: assign key to switch_players
- ToDo: snookers needed stage
- ToDo: penalties for misses
- ToDo: possibility for sitting player to put ball back after miss
- ToDo: lose game after three misses
- ToDo: random startup messages
- ToDo: GUI


### Snooker rules
Points are also scored if the opponent makes the following mistakes:
- Do not touch any ball with the cue ball,
- Hitting or pocketing a wrong color ball,
- Pocketing the cue ball,
- Get a ball out of the playing area,
- Use another cue ball than the white ball,
- Push balls.

#### De fouten
Als een stoot een fout geeft, dan krijgt uw tegenstander penalty punten:

- 4 punten als de witte (cue) bal werd gepot.
- 7 punten als de tijd om het stoten verstreken is ( 60 seconden/ stoot).
- als de witte bal de verkeerde bal eerst raakt dan de punten van dat kleur. Met een minimum van 4 punten.
- Als de verkeerde bal eerst wordt gepot, dan de punten van dat kleur. Met een minimum van 4 punten.

Dus wanneer een stoot een fout is. Krijgt de tegenstander die strafpunten bij zijn score.
Strafpunten hebben een minimum van 4 punten.
Nadat er een fout werd gemaakt mag de tegenspeler:

- Stoten op de ballen zoals ze liggen.
- Zijn beurt doorgeven, En hem die stoot laten doen. (Zonder terug te keren naar de vorige positie van het spel.).




### Requirements

#### Imports
- sys

#### Testing
- pytest
