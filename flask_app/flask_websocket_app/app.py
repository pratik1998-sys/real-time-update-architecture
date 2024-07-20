import eventlet
eventlet.monkey_patch()

from flask import Flask
from common.socketio import socketio
from common.config import SQLALCHEMY_DATABASE_URI
from common.db import db
from consumers.assessment_consumer import start_consumer as start_assessment_consumer
from consumers.weeklyChallenge_consumer import start_consumer as start_weekly_challenge_consumer
import signal
from db_utils.assessment_db_utils import commit_to_database as commit_assessment_to_database
from db_utils.weeklyChallenge_db_utils import commit_to_database as commit_weekly_challenge_to_database

# Import event handlers to register them
import websocketEvent.weeklyChallenge_events
import websocketEvent.assessment_events



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db.init_app(app)
socketio.init_app(app, cors_allowed_origins="*")

# Global buffers to store uncommitted messages
assessment_buffer = []
weekly_challenge_buffer = []

@app.route('/')
def index():
    return "WebSocket server is running"

@socketio.on('connect')
def handle_connect():
    print('websocket connection established')

@socketio.on('disconnect')
def handle_disconnect():
    print('websocket disconnect')

def graceful_shutdown(signum, frame):
    global assessment_buffer, weekly_challenge_buffer, app
    if assessment_buffer:        
        commit_assessment_to_database(app, assessment_buffer)
    if weekly_challenge_buffer:        
        commit_weekly_challenge_to_database(app, weekly_challenge_buffer)
    print("Graceful shutdown completed")
    socketio.stop()

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)
    start_assessment_consumer(app, assessment_buffer)
    start_weekly_challenge_consumer(app, weekly_challenge_buffer)
    socketio.run(app, debug=True)
