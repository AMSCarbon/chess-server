from app import app
from flask import render_template, request, Response, url_for

import chess
import secrets
from ws_routes import game_cache
import chess.svg

@app.route("/")
def index():
    return render_template("about.html")


# request to play a game
# Bool for whether or not you want random people to be allowed to join?
# Bool for black / white
@app.route("/start")
def init_game():
    raise NotImplementedError()
    return Response(game_id, status=201)


@app.route("/join")
def join_game():
    return "Joining a game"


@app.route("/list-games")
def list_games():
    return str(list(game_cache.keys()))


# get a view of the board
@app.route("/svg")
def svg():
    game_id = request.args.get("game_id")
    if game_id is None:
        return Response("400: The request was missing a game_id parameter", status=400)
    if game_id not in game_cache.games:
        return Response(
            "400: The request contained an invalid game_id parameter", status=400
        )
    return chess.svg.board(game_cache.games.get(game_id).board)


# get a view of the board
@app.route("/watch")
def watch():
    game_id = request.args.get("game_id")
    if game_id is None:
        return Response("400: The request was missing a game_id parameter", status=400)
    if game_id not in game_cache.games:
        return Response(
            "400: The request contained an invalid game_id parameter", status=400
        )
    board_render = chess.svg.board(game_cache.games.get(game_id).board, size=500)
    return render_template("watch.html", render=board_render)


@app.route("/board-state")
def board_state():
    return "A json dict of the boards current state"


@app.route("/valid-moves")
def valid_moves():
    return "A list of moves that the player may make"


# submit their move
@app.route("/submit-move")
def submit_move():
    return "Post the move you want to make"


# know when it's their turn
@app.route("/current-player")
def current_player():
    return "bool whether it's white or black's turn"
