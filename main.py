import sys

import numpy as np
import pygame

pygame.init()

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(WHITE)


class Game:
    def __init__(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))

    def draw_lines(self):
        # Draw board lines in black
        for i in range(1, BOARD_ROWS):
            pygame.draw.line(
                screen,
                BLACK,
                (0, SQUARE_SIZE * i),
                (WIDTH, SQUARE_SIZE * i),
                LINE_WIDTH,
            )
            pygame.draw.line(
                screen,
                BLACK,
                (SQUARE_SIZE * i, 0),
                (SQUARE_SIZE * i, HEIGHT),
                LINE_WIDTH,
            )

    def draw_figures(self):
        # Draw circles in red and crosses in green
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.board[row][col] == 1:
                    pygame.draw.circle(
                        screen,
                        RED,
                        (
                            int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                            int(row * SQUARE_SIZE + SQUARE_SIZE // 2),
                        ),
                        CIRCLE_RADIUS,
                        CIRCLE_WIDTH,
                    )
                elif self.board[row][col] == 2:
                    pygame.draw.line(
                        screen,
                        GREEN,
                        (
                            col * SQUARE_SIZE + SQUARE_SIZE // 4,
                            row * SQUARE_SIZE + SQUARE_SIZE // 4,
                        ),
                        (
                            col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                            row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                        ),
                        CROSS_WIDTH,
                    )
                    pygame.draw.line(
                        screen,
                        GREEN,
                        (
                            col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                            row * SQUARE_SIZE + SQUARE_SIZE // 4,
                        ),
                        (
                            col * SQUARE_SIZE + SQUARE_SIZE // 4,
                            row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                        ),
                        CROSS_WIDTH,
                    )

    def mark_square(self, row, col, player):
        self.board[row][col] = player

    def available_square(self, row, col):
        return self.board[row][col] == 0

    def is_board_full(self):
        return not any(0 in row for row in self.board)

    def check_win(self, player):
        for col in range(BOARD_COLS):
            if (
                self.board[0][col] == player
                and self.board[1][col] == player
                and self.board[2][col] == player
            ):
                return True
        for row in range(BOARD_ROWS):
            if (
                self.board[row][0] == player
                and self.board[row][1] == player
                and self.board[row][2] == player
            ):
                return True
        if (
            self.board[0][0] == player
            and self.board[1][1] == player
            and self.board[2][2] == player
        ):
            return True
        if (
            self.board[0][2] == player
            and self.board[1][1] == player
            and self.board[2][0] == player
        ):
            return True
        return False

    def minimax(self, depth, is_maximizing):
        if self.check_win(2):
            return 1
        if self.check_win(1):
            return -1
        if self.is_board_full():
            return 0

        if is_maximizing:
            best_score = float("-inf")
            for row in range(BOARD_ROWS):
                for col in range(BOARD_COLS):
                    if self.available_square(row, col):
                        self.mark_square(row, col, 2)
                        score = self.minimax(depth + 1, False)
                        self.board[row][col] = 0
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = float("inf")
            for row in range(BOARD_ROWS):
                for col in range(BOARD_COLS):
                    if self.available_square(row, col):
                        self.mark_square(row, col, 1)
                        score = self.minimax(depth + 1, True)
                        self.board[row][col] = 0
                        best_score = min(best_score, score)
            return best_score

    def get_best_move(self):
        best_score = float("-inf")
        move = (-1, -1)
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.available_square(row, col):
                    self.mark_square(row, col, 2)
                    score = self.minimax(0, False)
                    self.board[row][col] = 0
                    if score > best_score:
                        best_score = score
                        move = (row, col)
        return move


game = Game()
game.draw_lines()

player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX, mouseY = event.pos
            mouseX //= SQUARE_SIZE
            mouseY //= SQUARE_SIZE

            if game.available_square(mouseY, mouseX):
                game.mark_square(mouseY, mouseX, player)
                if game.check_win(player):
                    game_over = True
                player = 2 if player == 1 else 1

            if not game_over and player == 2:
                move = game.get_best_move()
                if move != (-1, -1):
                    game.mark_square(move[0], move[1], 2)
                    if game.check_win(2):
                        game_over = True
                player = 1

            if not game_over and game.is_board_full():
                game_over = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            game.__init__()
            game_over = False
            player = 1

    game.draw_figures()
    pygame.display.update()
