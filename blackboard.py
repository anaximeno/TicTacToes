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

    def update(self) -> None:
        pass

    def access(self) -> None:
        pass
