import random

import pygame as pg

from pygame.math import Vector2 as vec2
from pygame.display import set_caption
from common import GameStartType

from blackboard import *
from constants import *


def get_scaled_image(path, res) -> pg.Surface:
    return pg.transform.smoothscale(pg.image.load(path), res)


class Game:
    def __init__(self, robot_start: GameStartType) -> None:
        pg.init()
        self.robot_start = robot_start
        self._tic_tac_toe = TicTacToe(self, robot_start=robot_start)
        self.screen = pg.display.set_mode([WIN_SIZE] * 2)
        self.clock = pg.time.Clock()

    def check_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit(0)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.new_game()

    def new_game(self) -> None:
        self._tic_tac_toe = TicTacToe(self, robot_start=self.robot_start)

    def run(self) -> None:
        while True:
            self._tic_tac_toe.run()
            self.check_events()
            pg.display.update()
            self.clock.tick(60)


class TicTacToe:
    def __init__(self, game: Game, robot_start: GameStartType) -> None:
        self.game = game
        self.robot_start = robot_start
        self._board = Blackboard(self)
        self.back_img = get_scaled_image(path=BOARD_IMG_PATH, res=[WIN_SIZE] * 2)
        self.o_img = get_scaled_image(path=O_IMG_PATH, res=[CELL_SIZE] * 2)
        self.x_img = get_scaled_image(path=X_IMG_PATH, res=[CELL_SIZE] * 2)
        self._players = ['robot', 'user']
        self.winner = None
        self.winner_line = []
        self.game_steps = 0
        self.ply = 0
        self._game_start()

    def _game_start(self):
        start_by = self.robot_start

        if start_by == GameStartType.RANDOM:
            start_by = random.choice([
                GameStartType.PLAYER,
                GameStartType.AGENT,
            ])

        if start_by == GameStartType.AGENT:
            debug_log("Starting By: Agent Player", level=DebugLevel.INFO)
            row = random.randint(0, 2)
            col = random.randint(0, 2)
            self._board.update(
                row=row,
                col=col,
                value=1,
            )
        else:
            debug_log("Starting By: User Player", level=DebugLevel.INFO)

    def check_winner(self) -> None:
        for line in self._board.lines:
            total = sum([self._board.access(row=i, col=j) for i, j in line])
            if total in {0, 3}:
                self.winner = self._players[total == 0]
                self.winner_line = [
                    vec2(line[0][::-1]) * CELL_SIZE + CELL_CENTER,
                    vec2(line[2][::-1]) * CELL_SIZE + CELL_CENTER,
                ]

    def draw_winner(self) -> None:
        if self.winner is not None:
            pg.draw.line(self.game.screen, 'yellow',
                         *self.winner_line, CELL_SIZE // 8)

    def increment_game_steps(self) -> None:
        self.game_steps += 1

    def run_game_process(self) -> None:
        current_cell = vec2(pg.mouse.get_pos()) // CELL_SIZE
        col, row = map(int, current_cell)
        left_click = pg.mouse.get_pressed()[0]

        if left_click and self._board.access(row=row, col=col) == INF and self.winner is None:
            self._board.update(row=row, col=col, value=self.ply)
            self._board.run_agent()
            self.increment_game_steps()
            self.check_winner()

    def print_caption(self) -> None:
        if self.winner:
            self.set_caption(
                f'The {self.winner} player is the winner!'
                ' Press "Space" to Restart.'
            )
        elif self.game_steps == 9:
            self.set_caption(f'Game Over! Press "Space" to Restart')
        else:
            self.set_caption(f'Your Turn!')

    def set_caption(self, caption: str) -> None:
        set_caption(caption)

    def draw(self) -> None:
        self.game.screen.blit(self.back_img, (0, 0))
        self.draw_objs()
        self.draw_winner()

    def draw_objs(self) -> None:
        for y, row in enumerate(self._board.data):
            for x, obj in enumerate(row):
                if obj != INF:
                    vec = vec2(x, y) * CELL_SIZE
                    self.game.screen.blit(
                        self.x_img if obj else self.o_img, vec
                    )

    def run(self) -> None:
        self.print_caption()
        self.draw()
        self.run_game_process()
