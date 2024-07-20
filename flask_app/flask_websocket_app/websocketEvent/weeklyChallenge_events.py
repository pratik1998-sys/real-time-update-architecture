from flask_socketio import emit
from common.socketio import socketio
from producers.weeklyChallenge_producer import send_message
from common.config import WEEKLY_CHALLENGE_TOPIC1, WEEKLY_CHALLENGE_TOPIC2


@socketio.on('weekly_challenge_topic1_event')
def handle_weekly_challenge_topic1_event(json):
    try:
        print('messages recieved from weeklyChallange module')
        send_message(WEEKLY_CHALLENGE_TOPIC1, json)
    except Exception as e:
        print(f"Failed to send data to Kafka: {e}")

@socketio.on('weekly_challenge_topic2_event')
def handle_weekly_challenge_topic2_event(json):
    try:
        print('messages recieved from weeklyChallange module')
        send_message(WEEKLY_CHALLENGE_TOPIC2, json)
    except Exception as e:
        print(f"Failed to send data to Kafka: {e}")

def emit_uncommitted_messages():
    # Emit uncommitted messages for this module
    pass
