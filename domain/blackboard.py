class Controller:
    def __init__(self) -> None:
        pass

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

class KnowledgeSource:
    def __init__(self) -> None:
        pass

    def updateBlackboard(self) -> None:
        pass

    def executeCondition(self) -> None:
        pass

    def executeAction(self) -> None:
        pass
