import chess
import chess.engine
import random
from local_board import local_board

DEFAULT_PATH = "/usr/local/bin/stockfish"

class ChessBot:
    def __init__(self, random_rate: float = 0.5, stockfish_path:str = DEFAULT_PATH):
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        self.stock_concentration = random_rate

    def make_move(self):
        moves = [str(m) for m in list(local_board.generate_legal_moves())]
        result = self.engine.play(local_board, chess.engine.Limit(time=2.0))
        return result.move.uci() if random.uniform(0.0,1.0) < self.stock_concentration else random.choice(moves)

    def close(self):
        self.engine.close()


