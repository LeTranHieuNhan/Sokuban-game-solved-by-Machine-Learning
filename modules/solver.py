# Solver for sokuban game using following search strategies:
# - Breadth-first search
# - Depth-first search
# - A* search
# - Uniform-cost search
# - Greedy search
# - Custom strategy (Best First Search with custom_score)
# The solver class has the following methods:
# - solve(): solve the game
# """


import time
from collections import deque
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
        queue = deque([(self.initial_state, [])])

        count_expanded = 0
        count_move_states = 0

        while queue:
            current_state, path = queue.popleft()
            count_expanded += 1

            if current_state.check_solved():
                print("Expanded Node:", str(count_expanded))
                print("Generated states: ", str(count_move_states))
                print("Number of moves: ", len(path))
                print(path)
                return path

            visited.add(tuple(map(tuple, current_state.map)))  # hashing

            for direction in ['U', 'D', 'L', 'R']:
                temp_state = current_state.move('M')
                next_state = temp_state.move(direction)
                
                next_map_tuple = tuple(map(tuple, next_state.map))
                if next_map_tuple not in visited:
                    queue.append((next_state, path + [direction]))
                    visited.add(next_map_tuple)
                    count_move_states += 1

        return None

    def dfs(self):
        count_expanded = 0
        count_move_states = 0
        visited = set()
        queue = [(self.initial_state, [])]

        while queue:
            current_state, path = queue.pop()
            count_expanded += 1

            if current_state.check_solved():
                print("Expanded Node:", str(count_expanded))
                print("Generated states: ", str(count_move_states))
                print("Number of moves: ", len(path))
                print(path)
                return path

            visited.add(tuple(map(tuple, current_state.map)))  # hashing

            for direction in ['U', 'D', 'L', 'R']:
                temp_state = current_state.move('M')
                next_state = temp_state.move(direction)

                if tuple(map(tuple, next_state.map)) not in visited:
                    queue.append((next_state, path + [direction]))
                    visited.add(tuple(map(tuple, next_state.map)))
                    count_move_states += 1

        return None


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
                print("Generated states: ", str(count_move_states))
                print("Number of moves: ", len(path))
                print(path)
                return path  # Return the path if the goal is reached

            visited.add(tuple(map(tuple, current_state.map))) # hasing

            for direction in ['U', 'D', 'L', 'R']:
                temp_state = current_state.move('M')
                next_state = temp_state.move(direction)
                
                # Check if the next state is not visited
                if tuple(map(tuple, next_state.map)) not in visited:

                    # Use a tuple (total cost, GameState, path) to ensure correct comparison
                    priority_queue.put((next_state.get_total_cost(), next_state, path + [direction]))
                    count_move_states += 1

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
                print("Generated states: ", str(count_move_states))
                print("Number of moves: ", len(path))
                print(path)
                return path
            
            visited.add(tuple(map(tuple, current_state.map))) # hasing
            
            for direction in ['U', 'D', 'L', 'R']:
                temp_state = current_state.move('M')
                next_state = temp_state.move(direction)
                
                if tuple(map(tuple, next_state.map)) not in visited:
                    priority_queue.put((next_state.get_current_cost(), next_state, path + [direction]))
                    count_move_states += 1

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
                print("Generated states: ", str(count_move_states))
                print("Number of moves: ", len(path))
                print(path)
                return path
            visited.add(tuple(map(tuple, current_state.map))) # hasing
            
            for direction in ['U','D','L','R']:
                temp_state = current_state.move('M')
                next_state = temp_state.move(direction)
                
                if tuple(map(tuple, next_state.map)) not in visited:
                    priority_queue.put((next_state.get_heuristic(), next_state, path + [direction]))
                    count_move_states += 1
        return None


    # Best Frist Search
    def custom(self):
        visited = set()
        priority_queue = PriorityQueue()

        # include (custom_score, GameState, path)
        priority_queue.put((self.custom_score(self.initial_state), self.initial_state, []))

        count_expanded = 0
        count_move_states = 0
        while not priority_queue.empty():
            _, current_state, path = priority_queue.get()
            count_expanded += 1

            if current_state.check_solved():
                print("Expanded Node:", str(count_expanded))
                print("Generated states: ", str(count_move_states))
                print("Number of moves: ", len(path))
                print(path)
                return path

            visited.add(tuple(map(tuple, current_state.map)))  # hasing

            for direction in ['U', 'D', 'L', 'R']:
                temp_state = current_state.move('M')
                next_state = temp_state.move(direction)

                if tuple(map(tuple, next_state.map)) not in visited:
                    priority_queue.put((self.custom_score(next_state), next_state, path + [direction]))
                    count_move_states += 1

        return None

    def custom_score(self, state):
        current_cost = state.get_current_cost()
        
        # Calculate the number of boxes in target positions
        boxes_in_target = 0
        for box in state.boxes:
            if state.is_target(box):
                boxes_in_target += 1

        # Calculate the Manhattan distance from the player to the closest box
        player_position = state.find_player()
        
        closest_box_distance = float('inf')  # positive infinity for comparison
        for box in state.boxes:
            distance = abs(player_position[0] - box[0]) + abs(player_position[1] - box[1])
            closest_box_distance = min(closest_box_distance, distance)

        
        # Combine the factors to form the custom score
        custom_score = current_cost + 2 * boxes_in_target - closest_box_distance
        
        return custom_score


    def get_solution(self):
        return self.solution
