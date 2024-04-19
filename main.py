from ttt import Game
from common import GameStartType

if __name__ == "__main__":
    game = Game(robot_start=GameStartType.RANDOM)
    game.run()
