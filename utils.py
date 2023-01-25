import copy
import random


def generate_matrix():
    matrix = [[0 for _ in range(4)] for _ in range(4)]
    numbers = list(range(16))
    random.shuffle(numbers)
    for i in range(4):
        for j in range(4):
            matrix[i][j] = numbers[i*4 + j]
    return matrix


def is_solvable(start, goal):
    inversions = 0
    flat_start = [num for sublist in start for num in sublist]
    flat_goal = [num for sublist in goal for num in sublist]
    for i in range(len(flat_start)):
        if flat_start[i] != 0:
            for j in range(i+1, len(flat_start)):
                if flat_start[j] != 0 and flat_start[i] > flat_start[j]:
                    inversions += 1
    for i in range(len(flat_goal)):
        if flat_goal[i] != 0:
            for j in range(i+1, len(flat_goal)):
                if flat_goal[j] != 0 and flat_goal[i] > flat_goal[j]:
                    inversions -= 1
    if inversions % 2 == 0:
        return True
    else:
        return False


def find_empty_tile(state):
    empty_tile_i = 0
    empty_tile_j = 0
    for idx, row in enumerate(state):
        if 0 in row:
            empty_tile_i = idx
            empty_tile_j = row.index(0)
    empty_tile = (empty_tile_i, empty_tile_j)
    return empty_tile


def get_adjacent_indices(i, j):
    adjacent_indices = []
    if i > 0:
        adjacent_indices.append((i - 1, j))
    if i + 1 < 4:
        adjacent_indices.append((i + 1, j))
    if j > 0:
        adjacent_indices.append((i, j - 1))
    if j + 1 < 4:
        adjacent_indices.append((i, j + 1))
    return adjacent_indices


def get_direction(empty_tile, adjacent_cell):
    if empty_tile[0] == adjacent_cell[0]:
        if empty_tile[1] < adjacent_cell[1]:
            return "R"
        else:
            return "L"
    elif empty_tile[0] < adjacent_cell[0]:
        return "D"
    else:
        return "U"


# heuristic 1
def get_wrong_tiles(state, objective):
    wrong_positions = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] != objective[i][j] and state[i][j] != 0:
                wrong_positions += 1
    return wrong_positions


# heuristic 2
def get_manhattan_distance(state, goal):
    # Initialize the distance variable
    distance = 0

    # Iterate through the elements of the state
    for i in range(len(state)):
        for j in range(len(state[i])):
            # Find the position of the current tile in the goal
            for k in range(len(goal)):
                for l in range(len(goal[k])):
                    if goal[k][l] == state[i][j]:
                        if goal[k][l] != 0:
                            goal_i, goal_j = k, l
                            # Add the Manhattan distance to the distance variable
                            distance += abs(goal_i - i) + abs(goal_j - j)
    return distance


def generate_children(X, objective):
    # Find empty tile and its adjacent cells
    empty_tile = find_empty_tile(X["state"])
    adjacent_cells = get_adjacent_indices(empty_tile[0], empty_tile[1])

    # Compute children with results from above
    children_states = []
    for i, adjacent_cell in enumerate(adjacent_cells):
        child_state = copy.deepcopy(X["state"])
        child_state[adjacent_cell[0]][adjacent_cell[1]] = 0
        child_state[empty_tile[0]][empty_tile[1]] = X["state"][adjacent_cell[0]][adjacent_cell[1]]
        direction = get_direction(empty_tile, adjacent_cell)
        depth = X["depth"] + 1
        heuristic = get_manhattan_distance(child_state, objective)

        if i == 1:
            ID = X["depth"] + 0.1
        elif i == 2:
            ID = X["depth"] + 0.2
        elif i == 3:
            ID = X["depth"] + 0.3
        else:
            ID = X["depth"] + 0.4

        child_data = {
            "id": ID,
            "state": child_state,
            "depth": depth,
            "cost": heuristic + depth,
            "direction_array": X["direction_array"] + [direction],
            "lineage": X["lineage"] + [ID]
        }

        children_states.append(child_data)

    return children_states


def update_OPEN_CLOSE(children, OPEN, CLOSED):
    # Add children to OPEN or CLOSED
    for child in children:
        # --------------------------------- CASE 1 --------------------------------- #
        if child["state"] not in [x["state"] for x in OPEN] and child["state"] not in [x["state"] for x in CLOSED]:
            OPEN.append(child)
        '''
        # --------------------------------- CASE 2 --------------------------------- #
        elif child["state"] in [x["state"] for x in OPEN]:
            for i, x in enumerate(OPEN):
                if x["state"] == child["state"] and x["cost"] > child["cost"]:
                    OPEN[i] = child
                    OPEN = [obj for obj in OPEN if x["id"] not in obj["lineage"]]
                    break
        # --------------------------------- CASE 3 --------------------------------- #
        elif child["state"] in [x["state"] for x in CLOSED]:
            for i, x in enumerate(CLOSED):
                if x["state"] == child["state"] and x["cost"] > child["cost"]:
                    del CLOSED[i]
                    break
            OPEN.append(child)
        # -------------------------------------------------------------------------- #
        '''
    return OPEN, CLOSED


def print_sol(X, initial_state, objective):
    print('-------------Objective------------')
    print('\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in objective]))
    print('----------------------------------')

    # Print state
    print('----------Initial State-----------')
    print('\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in initial_state]))
    print('----------------------------------')

    print('-------------Solution-------------')
    print("\n")
    print(X["direction_array"][1:])
    print("\n")
    print('----------------------------------')
