import random

def print_board(board):
    for i in range(3):
        print(" | ".join(board[i]))
        if i < 2:
            print("---------") 
def check_winner(board):
    for row in board:
        if row.count(row[0]) == 3 and row[0] != " ":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None

def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "] 

def ai_move(board, ai_symbol, user_symbol):
    empty_cells = get_empty_cells(board)
    if not empty_cells:
        return None  

    for i, j in empty_cells:
        board[i][j] = ai_symbol
        if check_winner(board) == ai_symbol:
            return (i, j)
        board[i][j] = " "  

    for i, j in empty_cells:
        board[i][j] = user_symbol
        if check_winner(board) == user_symbol:
            board[i][j] = ai_symbol
            return (i, j)
        board[i][j] = " "  

    return random.choice(empty_cells)

def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]

    while True:
        user_symbol = input("Do you want to be X or O? ").strip().upper()
        if user_symbol in ["X", "O"]:
            break
        print("Invalid choice! Please choose X or O.")

    ai_symbol = "O" if user_symbol == "X" else "X"
    current_player = "X"  

    while True:
        print_board(board)

        if not get_empty_cells(board):  
            print("It's a draw!")
            break

        if current_player == user_symbol:
            try:
                row, col = map(int, input("Enter your move (row and column, 1-3): ").split())
                row, col = row - 1, col - 1  
                if (row, col) not in get_empty_cells(board):
                    print("Invalid move! Cell already occupied. Try again.")
                    continue
            except ValueError:
                print("Invalid input! Enter row and column as two numbers (1-3).")
                continue
        else:
            move = ai_move(board, ai_symbol, user_symbol)
            if move is None:
                print("It's a draw!")
                break
            row, col = move
            print(f"AI chooses: {row+1} {col+1}")  

        board[row][col] = current_player
        winner = check_winner(board)
        if winner:
            print_board(board)
            if winner == user_symbol:
                print("You win!")
            else:
                print("AI wins!")
            break

        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    tic_tac_toe()
