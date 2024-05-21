import random
import math

def check_if_valid(board):
    valid_move = False
    val = None
    while not valid_move:
        square = input(f"Please enter your move location (0-8): ")
        try:
            val = int(square)
            if val not in available_moves(board):
                raise ValueError
            valid_move = True
        except:
            print("Please input a valid location")
    return val

def print_board(board):

    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print("| " + " | ".join(row) + " |")

def board_nums():

    number_board = [[str(i) for i in range(j*3, (j+1) * 3)] for j in range(3)]
    
    for row in number_board:
        print('| ' + ' | '.join(row) + ' |')

def available_moves(board):
    return [i for i, spot in enumerate(board) if spot == ' ']

def winner(board, letter, square):

    row_index = square // 3
    row = board[row_index * 3:(row_index +1) * 3]
    if all([spot == letter for spot in row]):
        return True
    
    col_index = square % 3
    col = [board[col_index +i*3] for i in range(3)]
    if all([spot == letter for spot in col]):
        return True
    
    if square % 2 == 0:
        diagonal1 = [board[i] for i in [0, 4, 8]]
        if all([spot == letter for spot in diagonal1]):
            return True
        diagonal2 = [board[i] for i in [2, 4, 6]]
        if all([spot == letter for spot in diagonal2]):
            return True
    
    return False

def empty_moves(board):

    return ' ' in board

def cheatingComputer(board, player, square):
    CheckAvailableMoves = available_moves(board)
    if len(available_moves(board)) == 9:
        move = random.choice(CheckAvailableMoves)
    else:
        move = minimax(board, player, square)
    return move

def check_move(board, player, square):
    
    board[square] = player
    return square
    
def computer_player(board):

    CheckAvailableMoves = available_moves(board)
    move = random.choice(CheckAvailableMoves)
    return move

def minimax(board, player,  square):

    max_player = player
    other_player = 'O' if max_player == 'X' else 'X'

    if winner(board, player, square) == other_player:
        return -1
    elif not empty_moves(board):
        return 0

    if player == max_player:
        best_score = -math.inf
    else:
        best_score = math.inf

    for move in available_moves(board):
        make_move = check_move(board, player, move)
        sim_move = minimax(board, other_player, make_move) # simulate the move made
        board[move] = ' ' # undo the move
        sim_move = move
    
        if player == max_player:
            if sim_move > best_score:
                best_score = sim_move
        else:
            if sim_move < best_score:
                best_score = sim_move
    return best_score

    
def play():
    board = [' 'for _ in range(9)]
    player_1 = 'X'
    player_2 = 'O'
    computer = 'O'
    board_nums()
    print('Would you like to play against a computer player or another player ? ')
    versus = input('if you would to play against computer player, press c, if against another player press p: ')
    while ' ' in board:
        

        if versus.lower() == 'p':

            if player_1:
                print('Player 1 turn')
                print(f"Available moves{available_moves(board)} for player 1")
                print_board(board)
                letter = player_1
                square = check_if_valid(board)
                board[square] = player_1
                print(available_moves(board))
                print(f"Player 1 moves to square {square}")

                if winner(board, letter, square) == True:
                    print('Player 1 has won the game!')  
                    print_board(board) 
                    break

            if player_2:
                print(f'Player 2 move')
                print(f"Available moves{available_moves(board)} for player 2")
                print_board(board)
                letter = player_2
                square = check_if_valid(board)
                board[square] = player_2
                print(f"Player 1 moves to square {square}")

                if winner(board, letter, square) == True:
                    print_board(board)
                    print('Congratulations! player2 you have won!')
                    break
            
        else:
            while ' ' in board:
                if player_1:
                    print('Player 1 turn')
                    print(f"Available moves{available_moves(board)} for player 1")
                    print_board(board)
                    letter = player_1
                    square = check_if_valid(board)
                    board[square] = player_1
                    print(available_moves(board))
                    print(f"Player 1 moves to square {square}")

                    if winner(board, letter, square) == True:
                        print_board(board)
                        print('Congratulations! player1 you have won!')
                        break
                
                if computer:
                    print('Computer turn')
                    letter = computer
                    square = cheatingComputer(board, computer, square)
                    board[square] = computer
                    print(f'computer player moves to {square}')
                    print_board(board)

                    if winner(board, letter, square) == True:
                        print_board(board)
                        print('Computer player has won the game!')
                        break
            break                
if __name__ == '__main__':
    
    play()
