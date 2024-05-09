from __future__ import absolute_import
from src.maze_manager import MazeManager

if __name__ == "__main__":

    # Create the manager
    manager = MazeManager()

    # Add a 20x20 maze to the manager
    maze = manager.add_maze(20, 20)

    # Save mp4 file and png
    # manager.set_filename("Q_learning")

    # Solve the maze using the Q_learning algorithm
    manager.solve_maze(maze.id, "Q_learning")

    # Show how the maze was solved
    manager.show_solution_animation(maze.id)
    
    # Display the maze with the solution overlaid
    manager.show_solution(maze.id)
