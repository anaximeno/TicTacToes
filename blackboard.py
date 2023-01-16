from pyswip import Prolog

from constants import *

import os

DEBUG: bool = os.getenv('DEBUG') or False

prolog = Prolog()

prolog.consult(RETINENTIA_KNOWLEDGE_SOURCE)
prolog.consult(COMPUTATION_KNOWLEDGE_SOURCE)


def execute_simple_query(q: str) -> dict[str, any] | None:
    try:
        query = prolog.query(query=q)
        result = next(query)
        query.close()
        return result
    except:
        if DEBUG:
            print(f'Got a prolog query exception while executing {q!r}!')
        return None



class Action:
    def __init__(self, col: int, line: int, value: int, height: int) -> None:
        self.height = height
        self.value = value
        self.line = line
        self.col = col


class KnowledgeSource:
    def __init__(self) -> None:
        pass

    def _line_query(self, name: str, line: int = None) -> dict[str, int] | None:
        infix = f'{line}, ' if line is not None else ''
        return execute_simple_query(f"{name}({infix}R, H)")

    def _compute_query(self, name: str, line: int = None) -> dict[str, int] | None:
        infix = f'{line}, ' if line is not None else ''
        return execute_simple_query(f"{name}({infix}L, C, Value)")

    def _compute(self, lines: list[tuple[int, int, int, int]]) -> Action | None:
        for line in lines:
            computation = None

            if line[0] == EnumPositions.V:
                computation = self._compute_query('compute_vert', line[1])
            if line[0] == EnumPositions.H:
                computation = self._compute_query('compute_horiz', line[1])
            if line[0] == EnumPositions.DL:
                computation = self._compute_query('compute_diag_l')
            if line[0] == EnumPositions.DR:
                computation = self._compute_query('compute_diag_r')

            if computation is not None:
                return Action(
                    line=computation['L'],
                    col=computation['C'],
                    value=line[2],
                    height=line[3],
                )
        return None

    def suggest_preventive_action(self) -> Action | None:
        lines = []

        for i in range(3):
            if (vline := self._line_query('praeventionis_rvline', line=i)) is not None:
                lines.append((EnumPositions.V, i, vline['R'], vline['H']))
            if (hline := self._line_query('praeventionis_rhline', line=i)) is not None:
                lines.append((EnumPositions.H, i, hline['R'], hline['H']))

        if (dline_l := self._line_query('praeventionis_rdline_l')) is not None:
            lines.append((EnumPositions.DL, 0, dline_l['R'], dline_l['H']))
        if (dline_r := self._line_query('praeventionis_rdline_r')) is not None:
            lines.append((EnumPositions.DR, 0, dline_r['R'], dline_r['H']))

        lines.sort(key=lambda x: x[3], reverse=True)

        return None if not lines else self._compute(lines)

    def suggest_competitive_action(self) -> Action | None:
        lines = []

        for i in range(3):
            if (vline := self._line_query('quaestum_rvline', line=i)) is not None:
                lines.append((EnumPositions.V, i, vline['R'], vline['H']))
            if (hline := self._line_query('quaestum_rhline', line=i)) is not None:
                lines.append((EnumPositions.H, i, hline['R'], hline['H']))

        if (dline_l := self._line_query('quaestum_rdline_l')) is not None:
            lines.append((EnumPositions.DL, 0, dline_l['R'], dline_l['H']))
        if (dline_r := self._line_query('quaestum_rdline_r')) is not None:
            lines.append((EnumPositions.DR, 0, dline_r['R'], dline_r['H']))

        lines.sort(key=lambda x: x[3], reverse=True)

        return None if not lines else self._compute(lines)


class Controller:
    def __init__(self, board, knowledge_sorce: KnowledgeSource) -> None:
        self.ks = knowledge_sorce
        self.board = board

    def executeKS(self) -> bool:
        preventive = self.ks.suggest_preventive_action()
        competitive = self.ks.suggest_competitive_action()

        action = None

        if preventive and competitive:
            action = preventive if preventive.height > competitive.height else competitive
        elif preventive:
            action = preventive
        elif competitive:
            action = competitive

        if DEBUG:
            if preventive:
                print('* Preventive Suggestion: row = {}, column = {}, height = {}'.format(preventive.line, preventive.col, preventive.height))
            if competitive:
                print('* Competitive Suggestion: row = {}, column = {}, height = {}'.format(competitive.line, competitive.col, competitive.height))
            if action is not None:
                print('=> Acting "%s"' % ["Competitively", "Preventively"][int(action == preventive)])

        if action is not None:
            self.board.update(row=action.line, col=action.col, value=1)
            return True

        return False


class Blackboard:
    def __init__(self, game) -> None:
        self._control = Controller(self, KnowledgeSource())

        self._game = game

        self._data = [[INF, INF, INF],
                      [INF, INF, INF],
                      [INF, INF, INF]]

        self._lines = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]

        self._init_knowledge_memory()

    def _init_knowledge_memory(self) -> None:
        prolog.retractall('o(_, _)')
        prolog.retractall('x(_, _)')

    def update(self, *, row: int, col: int, value: int) -> None:
        if row < len(self._data) and col < len(self._data[row]):
            prolog.assertz(f"{'ox'[value]}({row}, {col})")
            self._data[row][col] = value
            self._game.check_winner()
            if value == 0 and self._game.winner is None and self._control.executeKS():
                self._game.increment_game_steps()

    def access(self, *, row: int = None, col: int = None) -> int | None:
        if row < len(self._data) and col < len(self._data[row]):
            return self._data[row][col]
        return None

    @property
    def data(self) -> list[list[float]]:
        return self._data

    @property
    def lines(self) -> list[list[tuple[int]]]:
        return self._lines
