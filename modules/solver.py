# Solver for sokuban game using following search strategies:
# - Breadth-first search
# - Depth-first search
# - A* search
# - Uniform-cost search
# - Greedy search
# - Custom strategy
# The solver class has the following methods:
# - solve(): solve the game
# """

# Extra function: dfs_recursive

import time
from collections import deque
from queue import Queue
from queue import PriorityQueue
import random


class Solver(object):
    
    def __init__(self, initial_state, strategy):
        self.initial_state = initial_state
        self.strategy = strategy
        self.solution = None
        self.time = None

    def solve(self):
        start_time = time.time()
        if self.strategy == 'bfs':
            self.solution = self.bfs()
        elif self.strategy == 'dfs':
            self.solution = self.dfs()
        elif self.strategy == 'astar':
            self.solution = self.astar()
        elif self.strategy == 'ucs':
            self.solution = self.ucs()
        elif self.strategy == 'greedy':
            self.solution = self.greedy()
        elif self.strategy == 'custom':
            self.solution = self.custom()
        else:
            raise Exception('Invalid strategy')
        self.time = time.time() - start_time
    

    def bfs(self):
        visited = set()
        queue = Queue()

        # include (total cost, GameState, path)
        queue.put((self.initial_state, []))

        count_expanded = 0
        count_move_states = 0
        while not queue.empty():
            current_state, path = queue.get()
            count_expanded += 1
            visited.add(tuple(map(tuple, current_state.map)))  # hasing
            
            for direction in ['U', 'D', 'L', 'R']:
                # move('M'): Update all attributes of the current state to temp_state
                temp_state = current_state.move('M')
                next_state = temp_state.move(direction)
                count_move_states += 1
                
                if next_state.check_solved():
                    print("Expanded Node:", str(count_expanded))
                    print("All states: ", str(count_move_states))
                    print("Number of moves: ", len(path + [direction]))
                    print(path + [direction])
                    return path + [direction]
                
                # Check if the next state is not visited
                if tuple(map(tuple, next_state.map)) not in visited:
                    queue.put((next_state, path + [direction]))

        return None  

    def dfs_recursive(self, current_state, path, count_expanded, count_move_states, visited):
        if current_state.check_solved():
            print("Expanded Node:", str(count_expanded))
            print("All states: ", str(count_move_states))
            print("Number of moves: ", len(path))
            print(path)
            return path  

        count_expanded += 1
        visited.add(tuple(map(tuple, current_state.map)))  # hashing

        for direction in ['U', 'D', 'L', 'R']: 
            temp_state = current_state.move('M')
            next_state = temp_state.move(direction)
            count_move_states += 1
            
            # Check if the next state is not visited
            if tuple(map(tuple, next_state.map)) not in visited:
                result = self.dfs_recursive(next_state, path + [direction], count_expanded, count_move_states, visited)
                if result is not None:
                    return result

        return None  

    def dfs(self):
        count_expanded = 0
        count_move_states = 0
        visited = set()
        return self.dfs_recursive(self.initial_state, [], count_expanded, count_move_states, visited)




    def astar(self):
        visited = set()
        priority_queue = PriorityQueue()

        # include (total cost, GameState, path)
        priority_queue.put((self.initial_state.get_total_cost(), self.initial_state, []))
        
        count_expanded = 0
        count_move_states = 0
        while not priority_queue.empty():
            _, current_state, path = priority_queue.get()
            count_expanded += 1
            
            # Check if the current state is solved
            if current_state.check_solved():
                print("Expanded Node:", str(count_expanded))
                print("All states: ", str(count_move_states))
                print("Number of moves: ", len(path))
                print(path)
                return path  # Return the path if the goal is reached

            visited.add(tuple(map(tuple, current_state.map))) # hasing

            for direction in ['U', 'D', 'L', 'R']:
                temp_state = current_state.move('M')
                next_state = temp_state.move(direction)
                count_move_states += 1
                
                # Check if the next state is not visited
                if tuple(map(tuple, next_state.map)) not in visited:

                    # Use a tuple (total cost, GameState, path) to ensure correct comparison
                    priority_queue.put((next_state.get_total_cost(), next_state, path + [direction]))

        return None  # Return None if no solution is found

    def ucs(self):
        visited = set()
        priority_queue = PriorityQueue()
        #include (current cost, GameState, path)
        
        priority_queue.put((self.initial_state.get_current_cost(), self.initial_state, []))
        
        count_expanded = 0
        count_move_states = 0
        while not priority_queue.empty():
            _, current_state, path = priority_queue.get()
            count_expanded += 1
            
            if current_state.check_solved():
                print("Expanded Node:", str(count_expanded))
                print("All states: ", str(count_move_states))
                print("Number of moves: ", len(path))
                print(path)
                return path
            
            visited.add(tuple(map(tuple, current_state.map))) # hasing
            
            for direction in ['U', 'D', 'L', 'R']:
                temp_state = current_state.move('M')
                next_state = temp_state.move(direction)
                count_move_states += 1
                
                if tuple(map(tuple, next_state.map)) not in visited:
                    priority_queue.put((next_state.get_current_cost(), next_state, path + [direction]))

        return None

    def greedy(self):
        visited = set()
        priority_queue = PriorityQueue()

        # include (heuristic, GameState, path)
        priority_queue.put((self.initial_state.get_heuristic(), self.initial_state, []))
        
        count_expanded = 0
        count_move_states = 0
        while not priority_queue.empty():
            _, current_state, path = priority_queue.get()
            count_expanded += 1
            
            if current_state.check_solved():
                print("Expanded Node:", str(count_expanded))
                print("All states: ", str(count_move_states))
                print("Number of moves: ", len(path))
                print(path)
                return path
            visited.add(tuple(map(tuple, current_state.map))) # hasing
            
            for direction in ['U','D','L','R']:
                temp_state = current_state.move('M')
                next_state = temp_state.move(direction)
                count_move_states += 1
                
                if tuple(map(tuple, next_state.map)) not in visited:
                    priority_queue.put((next_state.get_heuristic(), next_state, path + [direction]))
        return None

    def custom(self):
        path = []

        while not self.initial_state.check_solved():
            # Randomly choose a direction (U, D, L, R)
            direction = random.choice(['U', 'D', 'L', 'R'])
            
            # Move in the chosen direction
            next_state = self.initial_state.move(direction)
            
            # Check if the move is valid (i.e., the state has changed)
            if next_state != self.initial_state:
                # Append the chosen direction to the path
                path.append(direction)
            
            # Update the initial state for the next iteration
            self.initial_state = next_state

        return path

    def get_solution(self):
        return self.solution
