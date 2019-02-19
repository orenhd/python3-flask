from flask_socketio import emit

from main import socketio

namespace = '/paint-socket'


@socketio.on('submit', namespace=namespace)
def handle_submit(doodle_data):
    emit('publish', doodle_data)
