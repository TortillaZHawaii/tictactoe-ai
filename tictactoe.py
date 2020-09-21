# Author: Dawid Wysocki
# Tic Tac Toe
# Players 'X' vs 'O'
# 'X' always starts 'O' follows
# ' ' mean empty space in board

import random


# Generate empty board
board = [[' ' for _ in range(3)] for _ in range(3)]

# Types of players
players_list = ("user", "easy")


# Checks whose turn is it
def whose_turn():
    num = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                num += 1
            elif board[i][j] == 'O':
                num -= 1

    if num > 0:
        return 'O'
    return 'X'


# Translate from coordinate system used by user to used by program
def coordinates(i, j):
    return [3 - j, i - 1]


# Returns one of four possible state
def game_status():
    # Checks if we have a winner -> "X wins" or "O wins"
    for i in range(3):
        # Rows
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0] + " wins"
        # Columns
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i] + " wins"

    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[1][1] + " wins"
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[1][1] + " wins"

    # Checks if there are no empty cells -> "Game not finished"
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                break
        else:
            continue

        return "Game not finished"

    # Else -> "Draw"
    return "Draw"


# Checks if user coordinates are valid
def is_valid(user_coords):
    if len(user_coords) != 2:
        return False
    for i in user_coords:
        if i > 3 or i < 1:
            return False
    return True


# Checks if cell is occupied
def is_occupied(coords):
    global board
    return board[coords[0]][coords[1]] != ' '


# Change state of the one cell
def change_state(coords):
    global board
    board[coords[0]][coords[1]] = whose_turn()


# Fill the board with game state from string
def game_setup(start_str):
    global board
    start_str = start_str.replace('_', ' ')
    board = [[start_str[i * 3 + j] for j in range(3)] for i in range(3)]


# Prints the board with pretty format
def print_board():
    print('---------')
    for i in range(3):
        print('|', end=' ')
        for j in range(3):
            print(board[i][j], end=' ')
        print('|')
    print('---------')


# Asks for coordinates and checks them
def ask_for_coordinates():

    while True:
        coords_str = input('Enter the coordinates: > ')

        if len(coords_str) != 3:
            print("You should enter numbers!")
            continue

        if coords_str[0].isdigit() and coords_str[1] == ' ' and coords_str[2].isdigit():
            user_coords = [int(coords_str[0]), int(coords_str[2])]

            if is_valid(user_coords):
                coords = coordinates(user_coords[0], user_coords[1])
                if is_occupied(coords):
                    print("This cell is occupied! Choose another one!")
                    continue

                # valid move
                return coords

            else:
                print("Coordinates should be from 1 to 3!")

        else:
            print("You should enter numbers!")


# Player's move. Asks for coordinates and changes the cell
def players_move():
    coords = ask_for_coordinates()
    change_state(coords)


# Easy difficulty move. Just random
def easy_move():
    while True:
        coords = [random.randint(0, 2), random.randint(0, 2)]
        if not is_occupied(coords):
            print("Making move level \"easy\"")
            change_state(coords)
            return


# Main menu
def menu():
    while True:
        command = input("Input command: > ")
        commands = command.split()
        if command == "exit":
            break
        elif len(commands) == 3:
            if commands[0] == "start":
                if commands[1] in players_list and commands[2] in players_list:
                    play(commands[1], commands[2])
                else:
                    print("Bad parameters!")
        else:
            print("Bad parameters!")


# Take a turn
def take_turn(player):
    if player == "user":
        players_move()
    elif player == "easy":
        easy_move()
    print_board()


# Select players p1 (X) and p2 (O), and setup the game for them
def play(p1, p2):
    game_setup("_________")
    print_board()

    while game_status() == "Game not finished":
        # P1's turn
        take_turn(p1)
        if game_status() != "Game not finished":
            break
        # P2's turn
        take_turn(p2)

    print(game_status())


def stage1():
    game_setup(str(input('Enter cells: > ')))
    print_board()
    coords = ask_for_coordinates()
    change_state(coords)
    print_board()
    print(game_status())


def stage2():
    game_setup("_________")
    print_board()

    while game_status() == "Game not finished":
        # Player's turn
        players_move()
        print_board()
        if game_status() != "Game not finished":
            break
        # AI's move
        easy_move()
        print_board()

    print(game_status())


def stage3():
    menu()


stage3()
