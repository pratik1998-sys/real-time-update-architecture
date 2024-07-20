from flask_socketio import emit
from common.socketio import socketio
from producers.assessment_producer import send_message
from common.config import ASSESSMENT_TOPIC1, ASSESSMENT_TOPIC2

# @socketio.on('connect')
# def handle_connect(auth):
#     print('assessment module connected')
#     emit_uncommitted_messages()

# @socketio.on('disconnect')
# def handle_connect():
#     print('assessment module disconnected')

@socketio.on('assessment_topic1_event')
def handle_assessment_topic1_event(json):
    try:
        print('messages recieved from assessent module')
        send_message(ASSESSMENT_TOPIC1, json)
    except Exception as e:
        print(f"Failed to send data to Kafka: {e}")

@socketio.on('assessment_topic2_event')
def handle_assessment_topic2_event(json):
    try:
        print('messages recieved from assessent module')
        send_message(ASSESSMENT_TOPIC2, json)
    except Exception as e:
        print(f"Failed to send data to Kafka: {e}")

def emit_uncommitted_messages():
    # Emit uncommitted messages for this module
    pass
