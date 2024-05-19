import random
import time
# creating the sudoku board
board = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
]

# printing the sudoku board
def board_print(board):
    # printing the row horizontal line
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("-----------------------")
        # printing the col divinding line for every 3 numbers
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(' | ', end="")
            # checking if on last spot so we can repeat
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

# Finding empty locations on board
def find_empty(board):
    # finding the row
    for row in range(len(board)):
        #finding the col
        for col in range(len(board[0])):
            if board[row][col] == 0:
                return (row, col)
    
    return None

def check_if_won(board, number, position):
    # checking each row in each column for matching numbers
    for row in range(len(board[0])):
        if board[position[0]][row] == number and position[1] != row:
            return False
    
    # checking each column in each row for matching numbers
    for col in range(len(board)):
        if board[col][position[1]] == number and position[0] != col:
            return False
        
    # check a 3x3 box for matching numbers
    box_x = position[1] // 3
    box_y = position[0] // 3

    for boxY in range(box_y * 3, box_y * 3 + 3):
        for boxX in range(box_x * 3, box_x * 3 + 3):
            if board[boxY][boxX] == number and (boxY, boxX) != position:    
                return False
    
    return True

def random_location_on_board(board):
    empty_space = [(i, j) for i in range(9) for j in range(9) if board[i][j] == 0]
    if not empty_space:
        return None
    else:
        random_space = random.choice(empty_space)
    return random_space

def random_digit(board, difficulty):
    count = 0
    while count < difficulty:
        row, col = random_location_on_board(board)
        digit = random.randint(1, 9)
        board[row][col] = digit
        if check_if_won(board, digit, (row, col)) == True:
            pass
        count += 1
    
def solved(board):
    print(board)
    check_if_empty = find_empty(board)
    if not check_if_empty:
        return True
    else:
        row, col = check_if_empty

    for i in range(1, 10):
        if check_if_won(board, i, (row, col)):
            board[row][col] = i

            if solved(board):
                return True

            board[row][col] = 0
    
    return False
def diff(difficulty=None):
    
    if difficulty.lower() == 'e':
        amount = random.randint(35, 45)
    elif difficulty.lower() == 'm':
        amount = random.randint(30, 35)
    else:
        amount = random.randint(25, 30)
    
    return amount

def new_board(board):

    for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] != 0:
                    board[i][j] = 0
    return None

def game(board):
    difficulty_message = print('Please select difficulty: "e" for easy, "m" for medium, "h" for hard')
    difficulty_input = input(": ")
    board_print(board)
    difficulty = diff(difficulty_input)
    random_digit(board, difficulty)
    print('-----------------------')
    board_print(board)
    count = 0
    while not solved(board) and count < 100:
        new_board(board)
        random_digit(board, difficulty)
        count += 1
    print("-------------------------")
    board_print(board)
    
game(board)
