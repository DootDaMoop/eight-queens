import random

# Print Chess Board
def printBoard(board):
    for row in board:
        for val in row:
            print(val, end=" ")
        print()

# Random Start State
def randStartState(board):
    for col in range(8):
        row = random.randint(0,7)
        board[row][col] = 1

# Calculates the conflicts of the current board
def calcConflicts(board):
    conflicts = 0
    length = len(board)

    # Checks Row Conflicts
    for i in range(length):
        numQueens = sum(board[i])
        if numQueens > 1:
            conflicts += numQueens - 1
    
    # Checks Column Conflicts
    #for j in range(length):
        #numQueens = sum([board[i][j] for i in range(length)])
        #if numQueens > 1:
            #conflicts += numQueens - 1
    
    # Diagonal Conflicts
    for i in range(length):
        for j in range(length):
            if board[i][j] == 1:
                # Positive Slope
                k = 1
                while (i+k < length) and (j+k < length):
                    if board[i+k][j+k] == 1:
                        conflicts += 1
                    k += 1

                # Negative Slope
                k = 1
                while (i+k < length) and (j-k >= 0):
                    if board[i+k][j-k] == 1:
                        conflicts += 1
                    k += 1

    return conflicts

# Neighbor States
def neighborStates(board):
    neighbors = []
    length = len(board)

    # Col of Queen
    for i in range(length):
        for j in range(length):
            if board[j][i] == 1:
                # Move queen around board
                for k in range(length):
                    if k != i:
                        state = [row[:] for row in board]
                        state[j][i] = 0
                        state[k][i] = 1
                        neighbors.append(state)
    return neighbors


# Main
numRestarts = 0
numStateChanges = 0

# Chess Board (as a matrix)
board = [[0 for i in range(8)] for j in range(8)]

print("Starting State:")
randStartState(board)

while True:
    # Evaluate current state conflicts
    conflicts = calcConflicts(board)
    #Solution Found with Statistics
    if conflicts == 0:
        printBoard(board)
        print("\u001b[33mSolution Found!")
        print("Number of State Changes: "+str(numStateChanges))
        print("Number of Restarts: "+str(numRestarts)+"\u001b[0m")
        break

    # Generate Neighbor States for each Queen
    neighbors = neighborStates(board)

    # Check for best (lowest) heuristic value from each state
    bestState = None
    heuristicVal = conflicts
    for state in neighbors:
        neighborHeu = calcConflicts(state)
        if neighborHeu < heuristicVal:
            bestState = state
            heuristicVal = neighborHeu

    # Best State (Move with lowest Heuristic Value)
    if bestState is not None:
        board = bestState
        numStateChanges += 1
        printBoard(board)
        print("\u001b[34mNeighbor State found with lower heuristic val: "+str(heuristicVal)+"\nSetting new current state.\u001b[0m\n")
        continue

    # Restart (No better heuristic value was found)
    print("\u001b[31mNo better Heuristic Value was found\nRestarting\n\u001b[0m")
    numRestarts += 1
    randStartState(board)