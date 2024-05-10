import random
import numpy as np

maximum_steps = 1000 # Maximum number of steps per episode
exploration_decay = 0.995  # Rate of decay for exploration
minimum_exploration_rate = 0.05  # Minimum exploration rate

# Function to get the reward for the current state
def get_reward(current_state, next_state, maze):
    # Penalty for hitting a wall
    if maze.grid[current_state[0]][current_state[1]].is_walls_between(maze.grid[next_state[0]][next_state[1]]):
        reward = -1
    elif next_state == maze.exit_coor: # Reward for reaching the exit
        reward = 100
    else:
        reward = -0.1 # Penalty for moving to a cell
    return reward

# Function to get the valid actions that do not allow escape from the maze for the current state.
def valid_action(current_state, maze):
    actions = []

    if current_state[0] != 0:
        actions.append(0) # up
    if current_state[0] != maze.num_rows - 1:
        actions.append(1) # down
    if current_state[1] != 0:
        actions.append(2) # left
    if current_state[1] != maze.num_cols - 1:
        actions.append(3) # right

    return actions

# Update state based on action taken
def take_action(current_state, action):
    if action == 0: # up
        return (current_state[0] - 1, current_state[1])
    elif action == 1: # down
        return (current_state[0] + 1, current_state[1])
    elif action == 2: # left
        return (current_state[0], current_state[1] - 1)
    elif action == 3: # right
        return (current_state[0], current_state[1] + 1)

# Select the valid action with the highest Q-value for the current state
def select_best_action(current_state, q_table, valid_actions):
    max_q_value = -float('inf')
    best_actions = []

    for action in valid_actions:
        q_value = q_table[current_state[0], current_state[1], action] # Q(s, a)
        if q_value > max_q_value:
            max_q_value = q_value
            best_actions = [action]
        elif q_value == max_q_value:
            best_actions.append(action)
    return random.choice(best_actions)

def q_learning(maze, episodes_num, learning_rate, discount_factor, exploration_rate):
    """
    Implements the Q-learning algorithm to find the optimal policy for navigating a maze.

    Parameters:
        maze (Maze): The maze object which includes properties like grid, entry and exit coordinates.
        episodes_num (int): The number of episodes over which the agent will learn.
        learning_rate (float): The step size to update the Q-value, often denoted as alpha (α).
        discount_factor (float): The discount factor for future rewards, often denoted as gamma (γ).
        exploration_rate (float): The initial rate of exploration, determining how often to choose a random action.
    
    Description:
        This function initializes a Q-table with dimensions based on the maze size and possible actions per state.
        For each episode, it selects actions using an ε-greedy strategy, updates the Q-values based on the received rewards,
        and adjusts the exploration rate to ensure a balance between exploration and exploitation. The Q-learning update 
        rule is applied to adjust Q-values towards better estimates of the expected future rewards.

    Returns:
        The updated Q-table after all episodes, which can be used to infer the optimal policy by selecting 
        the action with the highest Q-value at each state.
    """
    q_table = np.zeros((maze.num_rows, maze.num_cols, 4)) # Initialize Q-table with zeros
    first_hit = episodes_num
    for episode in range(episodes_num): # Loop over episodes
        current_state = maze.entry_coor # Initialize the current state
        for step in range(maximum_steps): # Loop over steps
            # Apply ε-greedy strategy
            valid_actions = valid_action(current_state, maze)
            if random.uniform(0, 1) < exploration_rate:
                action = random.choice(valid_actions)
            else:
                action = select_best_action(current_state, q_table, valid_actions)

            next_state = take_action(current_state, action)
            reward = get_reward(current_state, next_state, maze) # R(s, a)

            if reward == -1: # Stay in the same place if hit a wall
                next_state = current_state

            q_now = q_table[current_state[0], current_state[1], action] # Q(s, a)
            next_valid_actions = valid_action(next_state, maze) # Q(s′,a′)
            
            max_next_q_value = -float('inf')
            for next_action in next_valid_actions:
                next_q_value = q_table[next_state[0], next_state[1], next_action]
                if next_q_value > max_next_q_value:
                    max_next_q_value = next_q_value # maxQ(s′,a′)

            # Q-learning formula: Q(s, a) = Q(s, a) + α * (R(s, a) + γ * maxQ(s′,a′) - Q(s, a))
            q_table[current_state[0], current_state[1], action] = q_now + learning_rate * (reward + discount_factor * max_next_q_value - q_now)

            current_state = next_state # Move to the next state
            
            if next_state == maze.exit_coor: # If the agent reaches the exit, terminate the episode
                if first_hit > episode:
                    first_hit = episode
                break

        exploration_rate = max(minimum_exploration_rate, exploration_rate * exploration_decay) # Decay the exploration rate to reduce exploration over time
    print(first_hit)
    return q_table

def q_learning_path(maze, q_table):
    """
    Determines the optimal path through the maze using the learned Q-table.

    Parameters:
        maze (Maze): The maze object which contains properties like grid, entry and exit coordinates.
        q_table (numpy.ndarray): The Q-table obtained from the q_learning function, which contains Q-values for each state-action pair.
    
    Description:
        This function uses the Q-table to navigate from the entry to the exit of the maze. It selects the best action at each state
        according to the highest Q-value, simulating the path an agent would take under a policy derived from the Q-table.
        It stops when the exit is reached or the maximum number of steps is exceeded, ensuring the function terminates.

    Returns:
        tuple: A tuple containing two elements:
            found_path (list): The sequence of states (coordinates) representing the path from entry to exit.
            found_cost (int): The number of steps taken to reach the exit, serving as a cost or length of the path.
    """
    current_state = maze.entry_coor # Start at the entry point of the maze
    found_path = [current_state] # Initialize the path with the starting position

    for _ in range(maximum_steps):
        if current_state == maze.exit_coor:  # Stop if the exit is reached
            break
        
        # Determine the best valid action to take at the current state
        valid_actions = valid_action(current_state, maze)
        best_action = select_best_action(current_state, q_table, valid_actions)
        # Move to the next state based on the best action
        next_state = take_action(current_state, best_action)
        # Add the new state to the path
        found_path.append(next_state)
        # Update the current state to the new state
        current_state = next_state

    found_cost = len(found_path)

    return [found_path, found_cost]
