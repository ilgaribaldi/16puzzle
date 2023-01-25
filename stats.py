import random
import utils
import main

random.seed(8)

goal = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
start = utils.generate_matrix()

total_puzzles = 0
solutions_found = 0
for i in range(50):
    if utils.is_solvable(start, goal):
        total_puzzles += 1
        if main.run_algo(start, goal):
            solutions_found += 1
print(f'ratio of solutions fount to total number of puzzles: {solutions_found/total_puzzles}')
