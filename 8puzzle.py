import numpy as np
import math
import timeit

INF = float("inf")

class State():
    def __init__(self, state: np.ndarray):
        self.state = state

    def __hash__(self) -> int:
        return hash(self.state.tobytes())
    
    def __eq__(self, other) -> bool:
        return self.__hash__() == other.__hash__()

    def get_possible_states(self):
        #get the coordinates of the empty tile
        y,x = np.where(self.state == 0)

        x=int(x)
        y=int(y)

        #check if any of the direction is over the board limit
        left = (x+1,y,"left") if x+1 < len(self.state) else 0
        right = (x-1,y,"right") if x-1 >= 0 else 0
        down = (x,y-1,"down") if y-1 >= 0 else 0
        up = (x,y+1,"up") if y+1 < len(self.state) else 0

        possible_states = []
        for direction in (right,left,up,down):
            if direction != 0:
                new_state = np.copy(self.state)
                new_state[direction[1]][direction[0]], new_state[y][x] = new_state[y][x], new_state[direction[1]][direction[0]]
                possible_states.append((State(new_state), direction[2]))

        return possible_states


def IDA(initial_state: State, goal_state: State):
    #get initial threshold
    bound = manhattan_heuristic(initial_state.state, goal_state.state)

    #path.append(initial_state)
    path = list()
    path.append(initial_state)

    directions = list()

    while True:
        result = search(0,bound,goal_state,path,directions)
        if result == True:
            return (True, directions)
        if result == INF:
            return (False, None)
        bound = result

def search(g: int,bound: int, goal_state: State,path,directions):
    current_state = path[-1]
    f = g + manhattan_heuristic(current_state.state,goal_state.state)
    if f > bound:
        return f
    if np.array_equal(current_state.state,goal_state.state):
        return True
    
    min = INF

    for (possible_state, direction) in current_state.get_possible_states():
        if possible_state not in path:
            directions.append(direction)
            path.append(possible_state)
            result = search(g+1,bound, goal_state,path,directions)
            if result == True:
                return True
            if result < min:
                min = result
            path.pop()
            directions.pop()
    return min

def manhattan_heuristic(current_state: np.ndarray, goal_state: np.ndarray):
    number_of_elements = len(current_state) ** 2
    distance = sum([manhattan_distance(np.where(current_state == num), np.where(goal_state == num)) for num in range(1, number_of_elements)])

    return distance


def manhattan_distance(current_position, goal_position):
    distance = abs(current_position[0] - goal_position[0]) + abs(current_position[1] - goal_position[1])

    return distance[0]

def is_solvable_board(board: np.ndarray):
    inv_count = 0
    is_solvable = False
    flat_board = board.flatten()

    for i in range(0, len(flat_board)):
        for j in range(i+1, len(flat_board)):
            if flat_board[j] != 0 and flat_board[i] != 0 and flat_board[i]>flat_board[j]:
                inv_count+=1

    if (len(board)%2) == 0:
        y, x = np.where(board == 0)
        y= int(y)
        inv_count +=y
        is_solvable = (inv_count%2) == 1
    else:
        is_solvable = (inv_count%2) == 0

    return is_solvable

if __name__ == "__main__":
    #get number of elements
    element_count = int(input())
    #get 0 index
    zero_index = int(input())

    #get row and column size
    row_count = int(math.sqrt(element_count+1))

    if zero_index == -1:
        zero_index = element_count

    initial_board = list()

    #populate the initial board
    while len(initial_board) <= element_count:
        input_line = input()
        elements = input_line.split()
        initial_board.extend([int(element) for element in elements ])

    start = timeit.default_timer()
    #index of the current element
    index = 0
    #number to be added
    number = 1
    goal_board = list()

    #populate goal board
    while index <= element_count:
        if index == zero_index:
            goal_board.append(0)
        else:
            goal_board.append(number)
            number += 1
        index += 1

    #convert from list to numpy array
    initial_board = np.array(initial_board)
    goal_board = np.array(goal_board)

    #convert from 1d array to 2d array
    initial_board = initial_board.reshape((row_count,row_count))
    goal_board = goal_board.reshape((row_count, row_count))

    #initialize states
    initial_state = State(initial_board)
    goal_state = State(goal_board)

    is_solvable = is_solvable_board(initial_board)

    end = 0.0

    if is_solvable:
        is_found, directions = IDA(initial_state,goal_state)
        end = timeit.default_timer()
        print(len(directions))
        print(*directions, sep="\n")
    else:
        end = timeit.default_timer()
        print(-1)

    print("Time: {} seconds".format(round(end-start,2)))