import tkinter as tk
import random

AI = True
HUMAN = False

AI_MARK = 'X'
HUMAN_MARK = 'O'

game_board = " " * 9

def is_win(board, player):
    for (x, y, z) in ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)):
        if board[x] == board[y] == board[z]:
            if board[x] == player:
                return True
    return False

def is_end(board):
    return is_win(board, AI_MARK) or is_win(board, HUMAN_MARK) or ' ' not in board

def find_empty(board):
    empty = []
    for i in range(0, 9):
        if board[i] == " ":
            empty.append(i)
    return tuple(empty)

def is_valid(x):
    return x in find_empty(game_board)

def place(x, player):
    if is_valid(x):
        global game_board
        game_board = game_board[:x] + player + game_board[x+1:]
        return True
    return False

def evaluate(board):
    if is_win(board, AI_MARK):
        score = 1
    elif is_win(board, HUMAN_MARK):
        score = -1
    else:
        score = 0
    return score

def minimax(board, depth, is_maximizing):
    if is_win(board, AI_MARK):
        return 1
    elif is_win(board, HUMAN_MARK):
        return -1
    elif ' ' not in board:
        return 0

    if is_maximizing:
        max_eval = -float("inf")
        for i in range(9):
            if board[i] == ' ':
                board = board[:i] + AI_MARK + board[i+1:]
                eval = minimax(board, depth + 1, False)
                board = board[:i] + ' ' + board[i+1:]
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for i in range(9):
            if board[i] == ' ':
                board = board[:i] + HUMAN_MARK + board[i+1:]
                eval = minimax(board, depth + 1, True)
                board = board[:i] + ' ' + board[i+1:]
                min_eval = min(min_eval, eval)
        return min_eval

def best_move(board):
    best_score = -float("inf")
    best_move = -1
    for i in range(9):
        if board[i] == ' ':
            board = board[:i] + AI_MARK + board[i+1:]
            move_score = minimax(board, 0, False)
            board = board[:i] + ' ' + board[i+1:]
            if move_score > best_score:
                best_score = move_score
                best_move = i
    return best_move

def draw_board():
    for i in range(9):
        text = game_board[i] if game_board[i] != ' ' else ''
        button = tk.Button(root, text=text, width=8, height=3, font=('Helvetica', 24), command=lambda i=i: make_move(i))
        if text == AI_MARK:
            button.config(bg='black', fg='white')
        elif text == HUMAN_MARK:
            button.config(bg='white', fg='black')
        button.grid(row=i//3, column=i%3)

def make_move(position):
    if is_valid(position) and not is_end(game_board):
        place(position, HUMAN_MARK)
        draw_board()
        if not is_end(game_board):
            ai_position = best_move(game_board)
            place(ai_position, AI_MARK)
            draw_board()
        if is_end(game_board):
            result = "Tie" if not is_win(game_board, AI_MARK) and not is_win(game_board, HUMAN_MARK) else "AI" if is_win(game_board, AI_MARK) else "Human"
            winner_label.config(text=result)
            play_again_button.config(state=tk.NORMAL)

def play_again():
    global game_board
    game_board = " " * 9
    winner_label.config(text='')
    play_again_button.config(state=tk.DISABLED)
    draw_board()

def close_game():
    root.destroy()

root = tk.Tk()
root.title("Unbeatable Tic Tac Toe")

winner_label = tk.Label(root, text='', font=('Helvetica', 20))
winner_label.grid(row=3, columnspan=3)

draw_board()

play_again_button = tk.Button(root, text="Play Again", command=play_again, state=tk.DISABLED)
play_again_button.grid(row=4, column=0, columnspan=2, pady=10)

close_button = tk.Button(root, text="Close", command=close_game)
close_button.grid(row=4, column=2, columnspan=1, pady=10)

root.mainloop()
