WIN_SIZE = 600

CELL_SIZE = WIN_SIZE // 3
CELL_CENTER = (CELL_SIZE // 2, CELL_SIZE // 2)

BOARD_IMG_PATH = "assets/board.png"
X_IMG_PATH = "assets/x.png"
O_IMG_PATH = "assets/o.png"

INF = float('inf')

COMPUTATION_KNOWLEDGE_SOURCE = "knowledge/computatio.pl"
RETINENTIA_KNOWLEDGE_SOURCE = "knowledge/retinentia.pl"
VALOREM_KNOWLEDGE_SOURCE = "knowledge/valorem.pl"


class EnumPositions: V, H, DL, DR = range(4)
