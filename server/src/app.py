from flask import Flask
import socketio

#Move this
from game_cache import GameCache
game_cache = GameCache()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = socketio.Server(logger=False, async_mode=None)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)


