from app import game_cache, sio
from flask_socketio import emit, send
from time import sleep


@sio.on("ping")
def handle_my_custom_event(json):
    emit("pong", json)


@sio.on("game_connect")
def game_connect(data):
    game_id = game_cache.new_game()
    game_data = game_cache.get_game_details(game_id)
    print(f"returning: {data}")
    sleep(3)
    emit("game_connect", data)

@sio.event
def connection(sid, data):
    print(f"Connection from {sid}")

@sio.event
def join(sid, data):
    print(sid)
    print(f"Connection from {sid}")
    # Is the user ok with joining an open game, and is there one available?
    game_ready = False
    if bool(data.get("join_ok")) and game_cache.room_available():
        room_id = game_cache.get_open_game()
        game_cache.set_player_2(room_id, sid)
        print(f"Joined room: {room_id}")
        game_ready = True
    # They've specified a room they want to join
    elif bool(data.get("room")):
        print("Request to join specific room not implemented yet")
        raise NotImplementedError()
    # They want to make a new room.
    else:
        room_id = game_cache.new_game(player_1_id=sid)
        if bool(data.get('public_game')):
            game_cache.mark_as_public(room_id)
        game_cache.set_player_1(room_id, sid)
        print(f"New game, id: {room_id}")
    sio.enter_room(sid, str(room_id))
    return str(room_id), game_ready


@sio.event
def start_game(sid, data):
    game_id = data.get("game_id")
    game_data = game_cache.get_game_data(game_id)
    sio.emit("request_move", game_data, room=game_id, skip_sid=sid)


@sio.event
def submit_move(sid, data):
    game_id = data.get("game_id")
    move = data.get("move")
    game_cache.push_move(game_id, move)
    game_data = game_cache.get_game_data(game_id)
    game_data["opponent_move"] = move
    if game_cache.should_end(game_id):
        winner = game_cache.outcome(game_id).winner
        winner = winner if winner is not None else "tie"
        print(f">>> {winner}")
        sio.emit("game_over", winner, room=game_id)
        sio.sleep(1)
        sio.disconnect(game_cache.get_player_1(game_id))
        sio.disconnect(game_cache.get_player_2(game_id))
    else:
        sio.emit("request_move", game_data, room=game_id, skip_sid=sid)