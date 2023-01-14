from .constants import *
from random import randint
from pygame.math import Vector2
import pygame as pg
import sys


def get_scaled_image(path, res) -> pg.Surface:
    img = pg.image.load(path)
    return pg.transform.smoothscale(img, res)


class Game:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode([WIN_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.tic_tac_toe = TicTacToe(self)

    def check_events(seld) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def run(self) -> None:
        while True:
            self.tic_tac_toe.run()
            self.check_events()
            pg.display.update()
            self.clock.tick(60)


class TicTacToe:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.back_img = get_scaled_image(path=BOARD_IMG_PATH, res=[WIN_SIZE] * 2)
        self.o_img = get_scaled_image(path=O_IMG_PATH, res=[CELL_SIZE] * 2)
        self.x_img = get_scaled_image(path=X_IMG_PATH, res=[CELL_SIZE] * 2)

        self.game_array = [[INF, INF, INF],
                           [INF, INF, INF],
                           [INF, INF, INF]]

        self.line_indices_array = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]

        self.player = randint(0, 1)
        self.winner = None
        self.game_steps = 0
        self.winner_line = []

    def check_winner(self) -> None:
        for lines_indices in self.line_indices_array:
            sum_line = sum([self.game_array[i][j] for i, j in lines_indices])
            if sum_line in {0, 3}:
                self.winner = 'XO'[sum_line == 0]
                self.winner_line = [
                    Vector2(lines_indices[0][::-1]) * CELL_SIZE + CELL_CENTER,
                    Vector2(lines_indices[2][::-1]) * CELL_SIZE + CELL_CENTER,
                ]

    def draw_winner(self) -> None:
        if self.winner is not None:
            pg.draw.line(self.game.screen, 'red', *self.winner_line, CELL_SIZE // 8)

    def run_game_process(self) -> None:
        current_cell = Vector2(pg.mouse.get_pos()) // CELL_SIZE
        col, row = map(int, current_cell)
        left_click = pg.mouse.get_pressed()[0]

        if left_click and self.game_array[row][col] == INF and self.winner is None:
            self.game_array[row][col] = self.player
            self.player = not self.player
            self.game_steps += 1
            self.check_winner()

    def print_caption(self) -> None:
        pg.display.set_caption(f'Player {"OX"[self.player]!r} turn!')

    def draw(self) -> None:
        self.game.screen.blit(self.back_img, (0, 0))
        self.draw_objs()
        self.draw_winner()

    def draw_objs(self) -> None:
        for y, row in enumerate(self.game_array):
            for x, obj in enumerate(row):
                if obj != INF:
                    vec = Vector2(x, y) * CELL_SIZE
                    self.game.screen.blit(
                        self.x_img if obj else self.o_img, vec)

    def run(self) -> None:
        self.print_caption()
        self.draw()
        self.run_game_process()
