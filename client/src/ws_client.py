import os
import sys

import socketio

from local_board import local_board
from chess_bot import ChessBot

uri = "ws://localhost:5000"
sio = socketio.Client()
bot = ChessBot(float(sys.argv[1]))

@sio.event
def connect():
    print("I'm connected!")
    print('my connection id is', sio.sid)
    print("Requesting join...")
    sio.emit('join', {'public_game': True, 'join_ok': True}, callback=join_return)
    return

@sio.event
def disconnect():
    print("Disconnected")
    bot.close()

@sio.event
def game_connect(data):
    print(f"Got game data {data}")

@sio.event
def request_move(data):
    print(f"Got request to make a move")
    previous_move = data.get("opponent_move")
    if previous_move:
        local_board.push_uci(previous_move)
    move = bot.make_move()
    local_board.push_uci(move)
    print(f"playing {move}")
    data["move"] = move
    sio.emit("submit_move", data)

@sio.event
def game_over(outcome):
    print("Game over")
    if outcome == "tie":
        print(outcome)
    else:
        print("white" if outcome else "black")

@sio.event
def join_return(game_id, game_ready):
    print(f"Watch at: http://localhost:5000/watch?game_id={game_id}")
    game_id = game_id
    if game_ready:
        sio.emit("start_game", {"game_id": game_id})


sio.connect(uri)
sio.wait()

