import sys              # Used to cleanly exit the program.
import pygame           # Used for creating the game window and handling events.
import numpy as np      # Used for handling the game board as a 2D array.

pygame.init()         # Initialize all imported pygame modules.

# Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Proportions and Sizes
WIDTH = 400
HEIGHT = 400
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

screen = pygame.display.set_mode((WIDTH, HEIGHT))   # Create the game window
pygame.display.set_caption('Tic-Tac-Toe AI')        # Set the window title
screen.fill(BLACK)                                  # Fill the screen with black color

board = np.zeros((BOARD_ROWS, BOARD_COLS))         # Initialize the game board as a 2D array of zeros

def draw_lines(color=WHITE):            # Draws the grid lines of the board
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

def draw_figure(color=WHITE):        # Draws circles and crosses depending on the board state
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                                   int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, color,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 CROSS_WIDTH)

def mark_square(row, col, player):   # Marks a square for a player (1 or 2)
    board[row][col] = player

def available_square(row, col):        # Checks if a square is available (not already marked)
    return board[row][col] == 0

def is_board_full(check_board=board):   # Checks if the board is full (no available squares)
    return not np.any(check_board == 0)

def check_win(player, check_board=board):  # Checks if a player has won the game
    for col in range(BOARD_COLS):
        if all(check_board[:, col] == player):
            return True
    for row in range(BOARD_ROWS):
        if all(check_board[row, :] == player):
            return True
    if all(np.diag(check_board) == player):
        return True
    if all(np.diag(np.fliplr(check_board)) == player):
        return True
    return False

def minimax(minimax_board, depth, is_maximizing):   # Minimax algorithm to find the best move for the AI
    if check_win(2, minimax_board):
        return 10 - depth
    elif check_win(1, minimax_board):
        return depth - 10
    elif is_board_full(minimax_board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

def best_move():      # Finds the best move for the AI using the minimax algorithm
    best_score = -float('inf')
    move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    return move

def restart_game():     # Resets the game board and screen for a new game
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

draw_lines()

player = 1
game_over = False
ai_turn = False

while True:   # Main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == 1:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE

            if available_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)
                if check_win(player):
                    game_over = True
                else:
                    player = 2
                    ai_turn = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart_game()
            game_over = False
            player = 1
            ai_turn = False

    if ai_turn and not game_over:
        move = best_move()
        if move:
            mark_square(move[0], move[1], 2)
            if check_win(2):
                game_over = True
            else:
                player = 1
        ai_turn = False

    draw_figure()

    if game_over:
        if check_win(1):
            draw_lines(color=GREEN)
        elif check_win(2):
            draw_lines(color=RED)
        else:
            draw_lines(color=GRAY)

    pygame.display.update()