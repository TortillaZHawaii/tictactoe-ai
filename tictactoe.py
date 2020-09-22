# Author: Dawid Wysocki
# Tic Tac Toe
# Players 'X' vs 'O'
# 'X' always starts 'O' follows
# ' ' mean empty space in board

import random


class Board:
    def __init__(self):
        # Generate an empty board
        self.b = [[' ' for _ in range(3)] for _ in range(3)]

    def __getitem__(self, i, j):
        return self.b[i][j]

    def __setitem__(self, i, j, value):
        self.b[i][j] = value

    def copy(self):
        a = Board()
        a.game_setup(self.save())
        return a

    def save(self):
        save_str = ""
        for i in range(3):
            for j in range(3):
                save_str += self.b[i][j]
        return save_str

    # Checks whose turn is it
    def whose_turn(self):
        num = 0
        for i in range(3):
            for j in range(3):
                if self.b[i][j] == 'X':
                    num += 1
                elif self.b[i][j] == 'O':
                    num -= 1

        if num > 0:
            return 'O'
        return 'X'

    # Returns one of four possible state
    def game_status(self):
        # Checks if we have a winner -> "X wins" or "O wins"
        for i in range(3):
            # Rows
            if self.b[i][0] == self.b[i][1] == self.b[i][2] != ' ':
                return self.b[i][0] + " wins"
            # Columns
            if self.b[0][i] == self.b[1][i] == self.b[2][i] != ' ':
                return self.b[0][i] + " wins"

        # Diagonals
        if self.b[0][0] == self.b[1][1] == self.b[2][2] != ' ':
            return self.b[1][1] + " wins"
        if self.b[0][2] == self.b[1][1] == self.b[2][0] != ' ':
            return self.b[1][1] + " wins"

        # Checks if there are no empty cells -> "Game not finished"
        for i in range(3):
            for j in range(3):
                if self.b[i][j] == ' ':
                    break
            else:
                continue

            return "Game not finished"

        # Else -> "Draw"
        return "Draw"

    # Checks if cell is occupied
    def is_occupied(self, coords):
        return self.b[coords[0]][coords[1]] != ' '

    # Checks if cell is clear
    def is_blank(self, coords):
        return self.b[coords[0]][coords[1]] == ' '

    # Two in a row
    def two_in_row(self, symbol):

        # Rows
        for i in range(3):
            blank = None
            n_attack = 0
            for j in range(3):
                if self.b[i][j] == symbol:
                    n_attack += 1
                elif self.b[i][j] == ' ':
                    blank = [i, j]

            if n_attack == 2 and blank is not None:
                return blank

        # Columns
        for j in range(3):
            blank = None
            n_attack = 0
            for i in range(3):
                if self.b[i][j] == symbol:
                    n_attack += 1
                elif self.b[i][j] == ' ':
                    blank = [i, j]

            if n_attack == 2 and blank is not None:
                return blank

        # Diagonals
        blank = None
        n_attack = 0
        for i in range(3):
            if self.b[i][i] == symbol:
                n_attack += 1
            elif self.b[i][i] == ' ':
                blank = [i, i]

        if n_attack == 2 and blank is not None:
            return blank

        blank = None
        n_attack = 0
        for i in range(3):
            if self.b[i][2 - i] == symbol:
                n_attack += 1
            elif self.b[i][2 - i] == ' ':
                blank = [i, 2 - i]

        if n_attack == 2 and blank is not None:
            return blank

        return None

    # Change state of the one cell
    def change_state(self, coords):
        self.b[coords[0]][coords[1]] = self.whose_turn()

    # Fill the board with game state from string
    def game_setup(self, start_str):
        start_str = start_str.replace('_', ' ')
        self.b = [[start_str[i * 3 + j] for j in range(3)] for i in range(3)]

    # Prints the board with pretty format
    def __str__(self):
        fancy_board = '---------\n'
        for i in range(3):
            fancy_board += '| '
            for j in range(3):
                fancy_board += self.b[i][j] + ' '
            fancy_board += '|\n'
        fancy_board += '---------'
        return fancy_board


board = Board()

# Types of players
players_list = ("user", "easy", "medium", "hard")


# Translate from coordinate system used by user to used by program
def coordinates(i, j):
    return [3 - j, i - 1]


# Virtual class to create different players
class Player:
    name = None

    def make_move(self):
        pass


# Checks if user coordinates are valid
def is_valid(user_coords):
    if len(user_coords) != 2:
        return False
    for i in user_coords:
        if i > 3 or i < 1:
            return False
    return True


# "user" player
class User(Player):
    name = "user"

    # Player's move. Asks for coordinates and changes the cell
    def make_move(self):
        coords = self.ask_for_coordinates()
        board.change_state(coords)

    # Asks for coordinates and checks them
    def ask_for_coordinates(self):

        while True:
            coords_str = input('Enter the coordinates: > ')

            if len(coords_str) != 3:
                print("You should enter numbers!")
                continue

            if coords_str[0].isdigit() and coords_str[1] == ' ' and coords_str[2].isdigit():
                user_coords = [int(coords_str[0]), int(coords_str[2])]

                if is_valid(user_coords):
                    coords = coordinates(user_coords[0], user_coords[1])
                    if board.is_occupied(coords):
                        print("This cell is occupied! Choose another one!")
                        continue

                    # valid move
                    return coords

                else:
                    print("Coordinates should be from 1 to 3!")

            else:
                print("You should enter numbers!")


# Make random move in a free space
def random_move():
    while True:
        coords = [random.randint(0, 2), random.randint(0, 2)]
        if not board.is_occupied(coords):
            board.change_state(coords)
            break


# "easy" player
class Easy(Player):
    name = "easy"

    # Easy difficulty move. Just random
    def make_move(self):
        random_move()
        print(f"Making move level \"{self.name}\"")


# "medium" player
class Medium(Easy):
    name = "medium"

    # Medium difficulty move. Block and attack at if two are in row, else make random moves
    def make_move(self):
        attack = board.whose_turn()
        defend = "X"
        if attack == "X":
            defend = "O"

        if board.two_in_row(attack) is not None:  # Winning
            board.change_state(board.two_in_row(attack))
        elif board.two_in_row(defend) is not None:  # Defending from losing
            board.change_state(board.two_in_row(defend))
        else:
            random_move()

        print(f"Making move level \"{self.name}\"")


# "hard" player
# Uses minimax algorithm to always win or draw
class Hard(Player):
    name = "hard"
    typ = None
    en_typ = None

    def score(self, b: Board):
        if b.game_status() == self.typ + " wins":
            return 10
        if b.game_status() == self.en_typ + " wins":
            return -10
        if b.game_status() == "draw":
            return 0

        score = 0
        for i in range(3):
            for j in range(3):
                if b.is_blank([i, j]):
                    b2 = b.copy()
                    b2.change_state([i, j])
                    score += self.score(b2)
        return score

    def make_move(self):
        if self.typ is None:
            self.typ = board.whose_turn()
            self.en_typ = 'X' if self.typ == 'O' else 'O'

        move = None
        maks = -1000000
        for i in range(3):
            for j in range(3):
                if board.is_blank([i, j]):
                    b2 = board.copy()
                    b2.change_state([i, j])
                    score = self.score(b2)
                    if score > maks:
                        maks = score
                        move = [i, j]

        if move is None:
            random_move()
        else:
            board.change_state(move)
        print(f"Making move level \"{self.name}\"")


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
                    player_1 = create_player(commands[1])
                    player_2 = create_player(commands[2])
                    play(player_1, player_2)
                else:
                    print("Bad parameters!")
            else:
                print("Bad parameters!")
        else:
            print("Bad parameters!")


# Creates a player from name
def create_player(player_name):
    if player_name == "user":
        return User()
    elif player_name == "easy":
        return Easy()
    elif player_name == "medium":
        return Medium()
    elif player_name == "hard":
        return Hard()


# Select players p1 (X) and p2 (O), and setup the game for them
def play(p1: Player, p2: Player):
    board.game_setup("_________")
    print(board)

    while board.game_status() == "Game not finished":
        # P1's turn
        p1.make_move()
        print(board)
        if board.game_status() != "Game not finished":
            break
        # P2's turn
        p2.make_move()
        print(board)

    print(board.game_status())


menu()
