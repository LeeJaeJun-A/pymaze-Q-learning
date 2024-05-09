# Maze generator and solver
This suite of Python scripts generates random solvable mazes using depth-first search and recursive backtracking algorithms, as inspired by the pseudo code on [Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm). Additionally, it includes a Q-learning algorithm to solve the mazes efficiently. The objective is to navigate from the entry to the exit point in the shortest possible time, avoiding walls and using the ε-greedy strategy for movement without prior knowledge of cell connections.


## Requirement
To install the necessary dependencies, open your terminal, navigate to the MazeGenerator directory, and execute one of the following commands:

`pip install -r requirements.txt`

Or, for direct installation:

`pip install matplotlib`


### Source Layout
* /src/   Contains all the source code modules needed to operate MazeGenerator.
* /examples/  Provides example files that demonstrate how to utilize the library.


### Class Overview
* The`Maze` class. This class provides helper functions to easily manipulate the cells. It can be thought of as being a grid of Cells
* The `Cell` class is used to keep track of walls, and is what makes up the list.
* The `Visualizer` class is responsible for handling the generation, display, and saving of animations and grid images. It can be interacted with directly, or controlled thought the `MazeManager` class.
* The `Solve` class. All solution methods are derived from this class. 
* The `MazeManager` class acts as the glue, bridging the `Visualizer`, `Maze`, and `Solve` classes together.


#### How to run my assignment

Ensure you are in the project's root directory. 

To execute the Q-learning algorithm, use the following command:

`python -m examples.solve_Q_learning`

Upon execution, you will be prompted to enter values for episodes, learning rate, discount factor, and exploration rate.

- Recommended Settings:
Episodes:
Learning Rate:
Discount Factor:
Exploration Rate:


#### Visualization

Observe the Q-learning process and results through MP4 files in the project folder. Outcomes are also depicted in 
PNG files, providing a clear visual representation of the final paths.