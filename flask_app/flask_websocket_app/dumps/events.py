from flask_socketio import SocketIO, emit
from flask import request
from flask_websocket_app.dumps.producer import producer
import random
from flask_websocket_app.dumps.config import TOPIC1, TOPIC2

socketio = SocketIO()

uncommitted_messages = {
    TOPIC1: [],
    TOPIC2: []
}

@socketio.on('connect')
def handle_connect(auth):
    print(uncommitted_messages)
    for topic, messages in uncommitted_messages.items():
        for message in messages:
            if topic == 'submit_test':
                emit('submitted_student_details', message)
            elif topic == 'update_time':
                emit('updated_test_time', message)

@socketio.on('disconnect')
def handle_disconnect():
    pass

@socketio.on('submit_test')
def handle_submit_test(json):
    try:  
        producer.send(TOPIC1, json)
        print(json)
    except Exception as e:
        print(f"Failed to send data to Kafka: {e}")

@socketio.on('update_time')
def handle_update_time(json):
    try:  
        producer.send(TOPIC2, json)
        print(json)
    except Exception as e:
        print(f"Failed to send data to Kafka: {e}")

@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"])
    print(request.event["args"])
