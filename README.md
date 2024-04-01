# ABOYNE
Aboyne is a board game for Windowsthat aims to move the pieces to achieve victory or stop the opponent from advancing by protecting the pieces themselves.

## Game modes
###Human vs. Human Mode:
Two people play against each other, alternating turns. This mode is ideal for players who want to compete directly with friends.

###Human vs. Computer Mode:
The player can choose whether they want to play first or second.
There is the option to select the difficulty of the bot, adjustable to best suit the player's skill level.
You can choose the size of the board, with options of 3x3, 4x4, or 5x5, allowing you to vary the complexity and length of the game

###Computer vs. Computer Mode:
In this mode, two bots play against each other, ideal for strategy analysis. You can select the size of the board with options of 3x3, 4x4, or 5x5.

## Bot Difficulty
###The First mode
Easy is made by using a minimax with a deph of 2 scaling minimax was an issue because of the high branching factor.
###The Second mode 
Medium is made using a Montecarlo Tree search with expected 100 number of simulations it will also timeout if it takes to long.
###The Third mode
Hard is made using a Montecarlo Tree search with expected 200 number of simulations as the previous one it will timeout.

##How to Compile
Make sure you are in the AboyneGame folder then, to Run the code just type on the console 
```$python main.py```
Once you are runing the game just select the game mode like any regular game and play.