import secrets
import chess
from typing import Optional, Dict


class GameCacheEntry:
    def __init__(self, token, board, **kwargs):
        self.token = token
        self.board: chess.Board = board
        # white is 1, black is 2
        self.player_1_id = kwargs.get("player_1_id")
        self.player_2_id = None
        self.isPublic = False


class GameCache:
    def __init__(self):
        self.games: Dict[str,GameCacheEntry] = {}

    def get_unique_id(self) -> str:
        game_id = secrets.token_urlsafe(6)
        while game_id in self.games.keys():
            game_id = secrets.token_urlsafe(6)
        return game_id

    def get_game(self, id: str) -> Optional[chess.Board]:
        return self.games.get(id)

    def get_game_data(self, game_id: str):
        board: chess.Board = self.games.get(game_id).board
        return {"game_id": game_id, "legal_moves": [str(m) for m in list(board.generate_legal_moves())]}

    def new_game(self, **kwargs):
        game_id = self.get_unique_id()
        self.games[game_id] = GameCacheEntry(
            game_id, chess.Board(), player_1_id=kwargs.get("player_1_id")
        )
        return game_id

    def set_player_1(self, game_id, player_1_id):
        self.games[game_id].player_1_id = player_1_id

    def set_player_2(self, game_id, player_2_id):
        self.games[game_id].player_2_id = player_2_id

    def get_player_1(self, game_id):
        return self.games[game_id].player_1_id

    def get_player_2(self, game_id):
        return self.games[game_id].player_2_id

    def mark_as_public(self, game_id):
        self.games[game_id].isPublic = True

    def game_joinable(self, game_id):
        return (
            # The game is public and at least one of the users isn't defined.
            self.games[game_id].isPublic
            and not (bool(self.games[game_id].player_1_id) and bool(self.games[game_id].player_2_id))
        )

    def should_end(self, game_id):
        return self.games[game_id].board.is_game_over(claim_draw=True)

    def outcome(self, game_id):
        return self.games[game_id].board.outcome(claim_draw=True)

    def room_available(self):
        # The game is listed as public
        return any([self.game_joinable(game_id) for game_id in self.games.keys()])

    def get_open_game(self) -> Optional[str]:
        # List of joinable games, pick the last element (just cuz). No error checking.
        return [game_id for game_id in self.games.keys() if self.game_joinable(game_id)].pop()

    def push_move(self, game_id, move: str):
        board: chess.Board = self.games[game_id].board
        board.push_uci(move)