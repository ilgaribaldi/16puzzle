import utils
import time


def run_algo(start, goal):
    start_time = time.time()

    # Initialize OPEN, CLOSE
    OPEN = [
        {
            "id": 0,
            "state": start,
            "depth": 0,
            "cost": utils.get_manhattan_distance(start, goal),
            "direction_array": ["-"],
            "lineage": []
        }
    ]
    CLOSED = []

    X = OPEN[0]
    counter = 1
    while X["state"] != goal and counter < 20000:
        # Remove X from OPEN
        OPEN.pop(0)

        # Compute children states
        children = utils.generate_children(X, goal)

        # Update OPEN, CLOSE
        OPEN, CLOSE = utils.update_OPEN_CLOSE(children, OPEN, CLOSED)

        # Arrange OPEN based on min cost
        OPEN = sorted(OPEN, key=lambda d: d["cost"])

        # Add X to CLOSED
        CLOSED.append(X)

        # DEFINE X for next iteration
        X = OPEN[0]

        # Display iteration
        print("Iteration: ", counter)
        counter += 1

    # Print objective
    utils.print_sol(X, start, goal)

    print(time.time() - start_time)

    # For statistics
    if X["state"] == goal:
        return True
    else:
        return False


if __name__ == '__main__':
    # Load the text file
    with open("Datos.txt", "r") as f:
        data = f.read().splitlines()

    # Split the data into individual values
    data = [list(map(int, row.split(","))) for row in data]

    # Split the matrix into two arrays of arrays
    start_state = data[:4]
    goal_state = data[4:]

    run_algo(start_state, goal_state)






