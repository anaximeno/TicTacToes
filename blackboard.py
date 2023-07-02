from enum  import Enum
from pyswip import Prolog
from pyswip.prolog import PrologError

from common import debug_log, DebugLevel
from constants import *


prolog = Prolog()

prolog.consult(RETINENTIA_KNOWLEDGE_SOURCE)
prolog.consult(COMPUTATION_KNOWLEDGE_SOURCE)


def execute_simple_query(q: str) -> dict[str, any] | None:
    query = prolog.query(query=q)
    result = None

    try:
        result = next(query)
    except StopIteration:
        debug_log(f'Got no results from query {q!r}', DebugLevel.WARNING)
    except PrologError:
        debug_log(f'Got a prolog query exception while executing {q!r}!', DebugLevel.WARNING)
    finally:
        query.close()

    return result


class Action:
    def __init__(self, col: int, line: int, value: int, weight: int) -> None:
        self.weight = weight
        self.value = value
        self.line = line
        self.col = col


class Position(Enum):
    VERTI = 0
    HORIZ = 1
    DIAG_LEFT = 2
    DIAG_RIGHT = 3


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

            match line[0]:
                case Position.VERTI:
                    computation = self._compute_query(
                        'best_vertical_point_to_play', line[1])
                case Position.HORIZ:
                    computation = self._compute_query(
                        'best_horizontal_point_to_play', line[1])
                case Position.DIAG_LEFT:
                    computation = self._compute_query(
                        'best_left_right_diagonal_point_to_play')
                case Position.DIAG_RIGHT:
                    computation = self._compute_query(
                        'best_right_left_diagonal_point_to_play')

            if computation is not None:
                return Action(
                    line=computation['L'],
                    col=computation['C'],
                    value=line[2] + computation['Value'],
                    weight=line[3] + computation['Value'],
                )
        return None

    def suggest_preventive_action(self) -> Action | None:
        lines = []

        for i in range(3):
            if (vline := self._line_query('o_value_achieved_at_a_vertical_line', line=i)) is not None:
                lines.append((Position.VERTI, i, vline['R'], vline['H']))
            if (hline := self._line_query('o_value_achieved_at_an_horizontal_line', line=i)) is not None:
                lines.append((Position.HORIZ, i, hline['R'], hline['H']))

        if (dline_l := self._line_query('o_value_achieved_at_the_left_right_diagonal')) is not None:
            lines.append((Position.DIAG_LEFT, 0, dline_l['R'], dline_l['H']))
        if (dline_r := self._line_query('o_value_achieved_at_the_right_left_diagonal')) is not None:
            lines.append((Position.DIAG_RIGHT, 0, dline_r['R'], dline_r['H']))

        lines.sort(key=lambda x: x[3], reverse=True)

        return None if not lines else self._compute(lines)

    def suggest_competitive_action(self) -> Action | None:
        lines = []

        for i in range(3):
            if (vline := self._line_query('x_value_achieved_at_a_vertical_line', line=i)) is not None:
                lines.append((Position.VERTI, i, vline['R'], vline['H']))
            if (hline := self._line_query('x_value_achieved_at_an_horizontal_line', line=i)) is not None:
                lines.append((Position.HORIZ, i, hline['R'], hline['H']))

        if (dline_l := self._line_query('x_value_achieved_at_the_left_right_diagonal')) is not None:
            lines.append((Position.DIAG_LEFT, 0, dline_l['R'], dline_l['H']))
        if (dline_r := self._line_query('x_value_achieved_at_the_right_left_diagonal')) is not None:
            lines.append((Position.DIAG_RIGHT, 0, dline_r['R'], dline_r['H']))

        lines.sort(key=lambda x: x[3], reverse=True)

        return None if not lines else self._compute(lines)


class Controller:
    def __init__(self, board, knowledge_source: KnowledgeSource) -> None:
        self.ks = knowledge_source
        self.board = board

    def executeKS(self) -> bool:
        preventive = self.ks.suggest_preventive_action()
        competitive = self.ks.suggest_competitive_action()

        if preventive is not None:
            debug_log('* Preventive Suggestion: row = {}, column = {}, weight = {}'.format(
                preventive.line, preventive.col, preventive.weight), DebugLevel.INFO)

        if competitive is not None:
            debug_log('* Competitive Suggestion: row = {}, column = {}, weight = {}'.format(
                competitive.line, competitive.col, competitive.weight), DebugLevel.INFO)

        action = self._select_action(preventive, competitive)

        if action is not None:
            debug_log('=> Acting "%s"' %
                    ["Competitively", "Preventively"][int(action == preventive)], DebugLevel.INFO)
            self.board.update(row=action.line, col=action.col, value=1)
            return True

        return False

    def _select_action(self, prev: Action | None, comp: Action | None) -> Action | None:
        action = None

        if prev and comp:
            action = prev if prev.weight > comp.weight else comp
        elif prev is not None:
            action = prev
        elif comp is not None:
            action = comp
        else:
            debug_log('=> There are no more suggested actions!', DebugLevel.INFO)

        return action


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
            if value == 0 and self._game.winner is None:
                self._process_robot_step()

    def _process_robot_step(self) -> None:
        if self._control.executeKS():
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
