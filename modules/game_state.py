"""
Sokuban game state class
The state of the game consists the map which is a 2D array of characters. There are 6 types of characters:
- ' ': empty space
- '#': wall
- '$': box
- '.': target
- '@': player
- '+': player on target
- '*': box on target
The game state class keeps track of the map.
The game state also keeps track of the player and box positions, and whether the game is solved or not.
The game state class has the following methods:
- find_player(): find the player in the map and return its position
- find_boxes(): find all the boxes in the map and return their positions
- find_targets(): find all the targets in the map and return their positions  
- generate_next_state(direction): generate the next game state by moving the player to the given direction
- check_solved(): check if the game is solved
"""

import time
import copy

class GameState:
    def __init__(self, map, current_cost=0):
        self.map = map
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.player = self.find_player()
        self.boxes = self.find_boxes()
        self.targets = self.find_targets()
        self.is_solved = self.check_solved()
        self.current_cost = current_cost

    def __lt__(self, other):
        return self.map < other.map
    # ------------------------------------------------------------------------------------------------------------------
    # The following methods are used to find the player, boxes, and targets in the map
    # The positions are tuples (row, column)
    # ------------------------------------------------------------------------------------------------------------------
    
    def find_player(self):
        """Find the player in the map and return its position"""
        # TODO: implement this method
        for row in range(self.height):
            for column in range(self.width):
                if self.map[row][column] in ('@', '+'):
                    return (row, column)
                

    def find_boxes(self):
        """Find all the boxes in the map and return their positions"""
        boxes = []
        
        for row in range(self.height):
            for column in range(self.width):
                if self.map[row][column] in ('$', '*'):
                    boxes.append((row, column))
                    
        return boxes

    def find_targets(self):
        """Find all the targets in the map and return their positions"""
        targets = []
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j] in ('.', '*') or self.map[i][j] in ('+', '*'):
                    targets.append((i, j))
        return targets

    # ------------------------------------------------------------------------------------------------------------------
    # The following methods are used to check if a position is a wall, box, target, or empty space
    # The position is a tuple (row, column)
    # ------------------------------------------------------------------------------------------------------------------

    def is_wall(self, position):
        """Check if the given position is a wall"""
        check = False
        row, column = position
        if self.map[row][column] == "#":
            check = True
        
        return check
        

    def is_box(self, position):
        """Check if the given position is a box
            Note: the box can be on "$" or "*" (box on target)
        """
        check = False
        row, column = position
        if self.map[row][column] in ('$', '*'):
            check = True
        
        return check

    def is_target(self, position):
        """Check if the given position is a target
            Note: the target can be "." or "*" (box on target)
        """
        check = False
        row, column = position
        if self.map[row][column] in ('.', '*') or self.map[row][column] in ('+', '*'):
            check = True
        
        return check

    def is_empty(self, position):
        """Check if the given position is empty"""
        check = False
        row, column = position
        if self.map[row][column] == ' ':
            check = True
        
        return check

    # ------------------------------------------------------------------------------------------------------------------
    # The following methods get heuristics for the game state (for informed search strategies)
    # ------------------------------------------------------------------------------------------------------------------

    def get_heuristic(self):
        """Get the heuristic for the game state
            Note: the heuristic is the sum of the distances from all the boxes to their nearest targets
        """
        heuristic = 0
        min_distance = float("inf") # positive infintie for comparision
        
        for box in self.boxes:
            box_row, box_col = box # Box position
            
            for target in self.targets:
                target_row, target_col = target # target position
                
                move_row = abs(target_row - box_row) # row distance
                move_col = abs(target_col - box_col) # col distance
                
                distance = move_row + move_col
                
                # check if current distance is greater than min distance
                if distance < min_distance:
                    min_distance = distance
                    
            heuristic += min_distance          
        return heuristic

    def get_total_cost(self):
        """Get the cost for the game state
            Note: the cost is the number of moves from the initial state to the current state + the heuristic
        """
        return self.get_current_cost() + self.get_heuristic()

    def get_current_cost(self):
        """Get the current cost for the game state
            Note: the current cost is the number of moves from the initial state to the current state
        """
        return self.current_cost

    # ------------------------------------------------------------------------------------------------------------------
    # The following methods are used to generate the next game state and check if the game is solved
    # ------------------------------------------------------------------------------------------------------------------
    
    def move(self, direction):
        """Generate the next game state by moving the player to the given direction. 
            The rules are as follows:
            - The player can move to an empty space
            - The player can move to a target
            - The player can push a box to an empty space (the box moves to the empty space, the player moves to the box's previous position)
            - The player can push a box to a target (the box moves to the target, the player moves to the box's previous position)
            - The player cannot move to a wall
            - The player cannot push a box to a wall
            - The player cannot push two boxes at the same time
        """
        p_row, p_col = self.player  # player current position
        p_new_row, p_new_col = p_row, p_col
        if direction == 'U':
            p_new_row -= 1
        elif direction == 'D':
            p_new_row += 1
        elif direction == 'L':
            p_new_col -= 1
        elif direction == 'R':
            p_new_col += 1
        elif direction == 'M':
            return GameState(self.map, self.current_cost)

        new_map = copy.deepcopy(self.map)
        player_new_pos = (p_new_row, p_new_col)  # player new position
        
        # If player position is inside the map    
        if 0 < p_row < (self.width - 1) or 0 < p_col < (self.height - 1):
            # If player meets wall then return
            if self.is_wall(player_new_pos):
                return self

            # If player goes into goal direction
            if self.is_target(player_new_pos):
                new_map[p_new_row][p_new_col] = '+'
                new_map[p_row][p_col] = ' '

            # If player goes into box position
            if self.is_box(player_new_pos):
                # box position
                b_row, b_col = player_new_pos
                b_new_row, b_new_col = b_row, b_col
                if direction == 'U':
                    b_new_row -= 1
                elif direction == 'D':
                    b_new_row += 1
                elif direction == 'L':
                    b_new_col -= 1
                elif direction == 'R':
                    b_new_col += 1
                elif direction == 'M':
                    return GameState(self.map, self.current_cost)
                box_new_pos = (b_new_row, b_new_col)  # box position
                


                # If box meets wall or meets another box then return
                if self.is_wall(box_new_pos) or self.is_box(box_new_pos):
                    return self
                # TODO If box goes into goal
                if self.is_target(box_new_pos):
                    new_map[b_new_row][b_new_col] = '*'
                    new_map[b_row][b_col] = '@'
                    new_map[p_row][p_col] = ' '
                # TODO If box goes out of goal
                    # previous box position in target
                elif self.is_target(player_new_pos):
                    new_map[b_new_row][b_new_col] = '$'
                    new_map[b_row][b_col] = '+'
                    new_map[p_row][p_col] = ' '   
                # Update map, player will go into box, and box will go into another direction
                else:
                    new_map[b_row][b_col] = new_map[p_row][p_col]
                    new_map[p_row][p_col] = ' '
                    new_map[b_new_row][b_new_col] = '$'

            # If the previous path is the goal path
            if not self.is_target(player_new_pos):
                if self.is_target(self.player):
                    new_map[p_row][p_col] = '.'
                else:
                    new_map[p_row][p_col] = ' '
                new_map[p_new_row][p_new_col] = '@'
        else:
            return self

        # Update map                
        self.map = copy.deepcopy(new_map)

        # TODO: implement this method
        return GameState(self.map, self.current_cost + 1)

        # Update map                
        self.map = copy.deepcopy(new_map)

        # TODO: implement this method
        return GameState(self.map, self.current_cost + 1)

    def check_solved(self):
        """Check if the game is solved"""
        total_boxes = len(self.boxes)
        count = 0 
        
        for box in self.boxes:
            if self.is_target(box):
                count += 1
        
        if total_boxes == count:
            return True
