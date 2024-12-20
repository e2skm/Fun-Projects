# Tic-Tac-Toe - Fun project11

# Define a function to print the board
def print_board(board):
    for row in board:
        print('|'.join(row))
        print('-'*5)

## Define a function to check winnner (and return the winner if there is one)
def check_winner(board):
    ### Create a for loop to check win veritcally(rows, ie like this -)
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]
    ### Create another for loop to check Horizontally(columns, i.e like so |)
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]
    ### Create an if statement to check for right diagonal win(like this \)
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    ### Create an if statement to check for left diagonal win(like this /)
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    ### Also return a result when there is no winner
    return None

## Define the game's main function
def tic_tac_toe():
    ### Create Board variable
    board = [[' ' for _ in range(3)]for _ in range(3)] 
    ### Create P1 variable X
    player = 'X'
    ### Take Turns for P1 and P2 for the nine cells on the board
    for turn in range(9):
        #### Create the current board (Showing all the populated and empty cells)
        print_board(board)
        #### Display whose turn it is 
        print(f"Player {player}'s turn")
        #### Get Player input (Which cell they would like to populate)
        row, col = map(int, input("Enter row and column (0-2) separated by space: ").split())
        #### Check whether that cell is empty (or already populated)
        if board[row][col] == ' ':
            ##### Assign the player to the spot when cell is empty
            board[row][col] = player
            ##### Check if player won after populating them to their desired cell
            winner = check_winner(board)
            ##### Display the Winner
            if winner:
                print_board
                print(f"Player {player} won")
                return 
            player = 'O' if player == 'X' else 'X'
        #### Show error message when cell is already populated
        else:
            print('Cell is occupied! Try again')
    ### If all cells are populated and the is no winner show the board and draw result       
    print_board(board)
    print('It is a draw')

tic_tac_toe()
                