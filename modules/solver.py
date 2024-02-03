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

import time
from collections import deque
from queue import Queue
from queue import PriorityQueue


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

        # Each element in the queue is a tuple (GameState, path)
        queue.put((self.initial_state, []))

        while not queue.empty():
            current_state, path = queue.get()
            visited.add(tuple(map(tuple, current_state.map)))  # Convert map to tuple for hashing
            
            for direction in ['U', 'D', 'L', 'R']:
                temp_state = current_state.move('M')
                next_state = temp_state.move(direction)
                
                if next_state.check_solved():
                    return path + [direction]
                
                # Check if the next state is not visited
                if tuple(map(tuple, next_state.map)) not in visited:
                    queue.put((next_state, path + [direction]))

        return None  # Return None if no solution is found

    def dfs(self):
        visited = set()
        stack = []

        #Each element in the stack is a tuple (GameState, path, visited)
        stack.append((self.initial_state, [], visited))

        while stack:
            current_state, path, visited = stack.pop() # pop 

            if current_state.check_solved():
                return path  # Return the path if the goal is reached

            visited.add(tuple(map(tuple, current_state.map)))  # Convert map to tuple for hashing

            for direction in reversed(['U', 'D', 'L', 'R']):
                temp_state = current_state.move('M')
                next_state = temp_state.move(direction)

                # Check if the next state is not visited
                if tuple(map(tuple, next_state.map)) not in visited:
                    stack.append((next_state, path + [direction], visited))
                    # stack (right, left)

        return None  # Return None if no solution is found


    def astar(self):
        visited = set()
        priority_queue = PriorityQueue()

        # Include (total cost, GameState, path)
        priority_queue.put((self.initial_state.get_total_cost(), self.initial_state, []))
        
        while not priority_queue.empty():
            _, current_state, path = priority_queue.get()

            # Check if the current state is solved
            if current_state.check_solved():
                return path  # Return the path if the goal is reached

            visited.add(tuple(map(tuple, current_state.map)))

            for direction in ['U', 'D', 'L', 'R']:
                temp_state = current_state.move('M')
                next_state = temp_state.move(direction)

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
        while not priority_queue.empty():
            _, current_state, path = priority_queue.get()
            if current_state.check_solved():
                return path
            visited.add(tuple(map(tuple, current_state.map)))
            for direction in ['U', 'D', 'L', 'R']:
                temp_state = current_state.move('M')
                next_state = temp_state.move(direction)

                if tuple(map(tuple, next_state.map)) not in visited:
                    priority_queue.put((next_state.get_current_cost(), next_state, path + [direction]))

        return None

    def greedy(self):
        visited = set()
        priority_queue = PriorityQueue()

        # include (heuristic, GameState, path)
        priority_queue.put((self.initial_state.get_heuristic(), self.initial_state, []))
        while not priority_queue.empty():
            _, current_state, path = priority_queue.get()
            if current_state.check_solved():
                return path
            visited.add(tuple(map(tuple, current_state.map)))
            for direction in ['U','D','L','R']:
                temp_state = current_state.move('M')
                next_state = temp_state.move(direction)

                if tuple(map(tuple, next_state.map)) not in visited:
                    priority_queue.put((next_state.get_heuristic(), next_state, path + [direction]))
        return None

    def custom(self):
        return ['U', 'U',]

    def get_solution(self):
        return self.solution
