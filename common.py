from enum  import Enum

import os


DEBUG_LEVEL: int | None = int(os.getenv('DEBUG')) if os.getenv('DEBUG') else None


class GameStartType(Enum):
    PLAYER = 0
    AGENT = 1
    RANDOM = 2


class DebugLevel(Enum):
    NONE = 0
    INFO = 1
    WARNING = 2
    ERROR = 3


def debug_log(msg: str, level: DebugLevel) -> bool:
    if DEBUG_LEVEL is not None and level.value <= DEBUG_LEVEL:
        print(msg)
        return True
    return False
