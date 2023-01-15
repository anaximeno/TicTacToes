from random import randint
import sys

from blackboard import *
from constants import *
from pygame.math import Vector2
import pygame as pg


def get_scaled_image(path, res) -> pg.Surface:
    img = pg.image.load(path)
    return pg.transform.smoothscale(img, res)


class Game:
    def __init__(self) -> None:
        pg.init()
        self._tic_tac_toe = TicTacToe(self)
        self.screen = pg.display.set_mode([WIN_SIZE] * 2)
        self.clock = pg.time.Clock()

    def check_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.new_game()

    def new_game(self) -> None:
        self._tic_tac_toe = TicTacToe(self)

    def run(self) -> None:
        while True:
            self._tic_tac_toe.run()
            self.check_events()
            pg.display.update()
            self.clock.tick(60)


class TicTacToe:
    def __init__(self, game: Game) -> None:
        self.game = game
        self._board = Blackboard(
            Controller([
                KnowledgeSource(
                    name='Praeventionis',
                    description='Módulo especializado na prevenção da derrota',
                    path='knowledge/praeventionis.pl',
                ),
                KnowledgeSource(
                    name='Quaestum',
                    description='Módulo especializado em ganhar o jogo',
                    path='knowledge/quaestum.pl',
                ),
            ])
        )
        self.back_img = get_scaled_image(
            path=BOARD_IMG_PATH, res=[WIN_SIZE] * 2,
        )
        self.o_img = get_scaled_image(path=O_IMG_PATH, res=[CELL_SIZE] * 2)
        self.x_img = get_scaled_image(path=X_IMG_PATH, res=[CELL_SIZE] * 2)
        self.player = 0
        self.winner = None
        self.game_steps = 0
        self.winner_line = []

    def check_winner(self) -> None:
        for line in self._board.lines:
            total = sum([self._board.access(row=i, col=j) for i, j in line])
            if total in {0, 3}:
                self.winner = 'XO'[total == 0]
                self.winner_line = [
                    Vector2(line[0][::-1]) * CELL_SIZE + CELL_CENTER,
                    Vector2(line[2][::-1]) * CELL_SIZE + CELL_CENTER,
                ]

    def draw_winner(self) -> None:
        if self.winner is not None:
            pg.draw.line(self.game.screen, 'red', *
                         self.winner_line, CELL_SIZE // 8)

    def run_game_process(self) -> None:
        current_cell = Vector2(pg.mouse.get_pos()) // CELL_SIZE
        col, row = map(int, current_cell)
        left_click = pg.mouse.get_pressed()[0]

        if left_click and self._board.access(row=row, col=col) == INF and self.winner is None:
            self._board.update(row=row, col=col, value=self.player)
            self.player = not self.player
            self.game_steps += 1
            self.check_winner()

    def print_caption(self) -> None:
        if self.winner:
            pg.display.set_caption(f'Player {self.winner!r} Wins! Press "Space" to Restart.')
        elif self.game_steps == 9:
            pg.display.set_caption(f'Game Over! Press "Space" to Restart')
        else:
            pg.display.set_caption(f'Player {"OX"[self.player]!r} Turn!')

    def draw(self) -> None:
        self.game.screen.blit(self.back_img, (0, 0))
        self.draw_objs()
        self.draw_winner()

    def draw_objs(self) -> None:
        for y, row in enumerate(self._board.data):
            for x, obj in enumerate(row):
                if obj != INF:
                    vec = Vector2(x, y) * CELL_SIZE
                    self.game.screen.blit(
                        self.x_img if obj else self.o_img, vec
                    )

    def run(self) -> None:
        self.print_caption()
        self.draw()
        self.run_game_process()
