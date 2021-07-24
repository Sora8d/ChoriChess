from stockfish import Stockfish
from config import Config
#param = {
#    "Write Debug Log": "false",
#    "Contempt": 0,
#    "Min Split Depth": 0,
#    "Threads": 1,
#    "Ponder": "false",
#    "Hash": 16,
#    "MultiPV": 1,
#    "Skill Level": 20,
#    "Move Overhead": 30,
#    "Minimum Thinking Time": 20,
#    "Slow Mover": 80,
#    "UCI_Chess960": "false",
#}

class Bridge_Stock_Chess():
    def __init__(self, stockfish_path=Config.STOCKFISH):
        self.stockfish= Stockfish(stockfish_path)

    def update_board(self, input):
        self.stockfish.make_moves_from_current_position([input])

    def move(self):
        b_move = self.stockfish.get_best_move_time(500)
        return b_move

    def import_fen(self, fen_position):
        self.stockfish.set_fen_position(fen_position)
        print(self.stockfish.get_fen_position())