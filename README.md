# Artificial Inteligence 1º Project
To Run the code just type on the console 
```$python main.py```
Once you are runing the game just select the game mode like any regular game and play.
## Game modes
There are three game modes Human vs Human, Human vs Computer and Computer vs Computer. On the Human vs computer mode you can select whether to start first or second, you can select the dificulty of the Bot playing either on the Human vs Computer and Computer vs Computer, at last you can chose the board size between 3x3,4x4 and 5x5.

## Bot Difficulty
The First mode Easy is made by using a minimax with a deph of 2 scaling minimax was an issue because of the high branching factor.
The Second mode Medium is made using a Montecarlo Tree search with expected 100 number of simulations it will also timeout if it takes to long.
The Third mode Hard is made using a Montecarlo Tree search with expected 200 number of simulations as the previous one it will timeout.
