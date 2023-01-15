from constants import INF


class KnowledgeSource:
    def __init__(self, name: str, path: str, description: str) -> None:
        self._desc = description
        self._name = name
        self._path = path

    @property
    def description(self) -> str:
        return self._desc

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> str:
        return self._path

    def updateBlackboard(self) -> None:
        pass

    def executeCondition(self) -> None:
        pass

    def executeAction(self) -> None:
        pass


class Controller:
    def __init__(self, knowledge_sources: list[KnowledgeSource]) -> None:
        self._ks_list = knowledge_sources

    def selectKnowledgeSource(self) -> None:
        pass

    def configureKnowledgeSource(self) -> None:
        pass

    def executeKnowledgeSource(self) -> None:
        pass


class Blackboard:
    def __init__(self, controller: Controller) -> None:
        self._control = controller
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

    def update(self, *, row: int, col: int, value: int) -> None:
        if row < len(self._data) and col < len(self._data[row]):
            self._data[row][col] = value
            # TODO: notify controller

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
