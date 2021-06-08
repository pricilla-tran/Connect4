import numpy as np
import pygame
import sys
import math

# Board Colour
BLUE = (0, 0, 255)
# Gap Colour
BLACK = (0, 0, 0)
# Counter Colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

# Creating Board
def create_board():
    # makes matrix of all zeros
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# Function for when a counter is dropped
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Check if it is a valid location of the piece being dropped by using the printed board and the columns
def is_valid_location(board, col):
    # return board the row is 5, and column, if it is 0 it can be dropped
    # if not the column is full
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Print Board so the orientation has the pieces at the bottom
# because numpy uses the top left corner as the first index
def print_board(board):
    print(np.flip(board, 0))

# LOGIC FOR THE WIN!
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def draw_board(board):
    # Drawing The Board
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)


    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # Player 1 Pieces
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            # Player 2 Pieces
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

# prints the board matrix
board = create_board()
print_board(board)
# this is so the game keeps going until someone wins
game_over = False
turn = 0

# Start Game
pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

# Font of Label/Text
myfont = pygame.font.SysFont("monospace", 75)

# During the game before anyone wins
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Follows Mouse Motion
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

        # When player decides a place to drop the piece
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            # Ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                # if valid drop zone
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    # drop the piece/counter
                    drop_piece(board, row, col, 1)

                    # If player 1 wins
                    if winning_move(board, 1):
                        # first value is the message, second is axis, third is text colour
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        # Put label on the screen
                        # First is the text, second is the coordinates of where the text is displayed
                        screen.blit(label, (40, 10))
                        game_over = True


            # # Ask for Player 2 Input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 wins!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)
            draw_board(board)

            # Alternating between the two playesr for whose turn it is
            turn += 1
            turn = turn % 2

            if game_over:
                # Waits 3000 milliseconds to shut the game after the win
                pygame.time.wait(3000)