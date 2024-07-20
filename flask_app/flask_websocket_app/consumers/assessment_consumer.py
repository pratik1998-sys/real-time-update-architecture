import threading
import time
import json
from kafka import KafkaConsumer
from common.config import KAFKA_BROKER_URL, ASSESSMENT_TOPIC1, ASSESSMENT_TOPIC2
from db_utils.assessment_db_utils import commit_to_database
from common.socketio import socketio

consumer = KafkaConsumer(
    ASSESSMENT_TOPIC1, ASSESSMENT_TOPIC2,
    bootstrap_servers=KAFKA_BROKER_URL,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='assessment-group',
    value_deserializer=lambda m: json.loads(m.decode('ascii'))
)

def consume_messages(app, buffer):
    BATCH_SIZE = 10
    BATCH_INTERVAL = 5
    last_commit_time = time.time()

    with app.app_context():
        for message in consumer:
            try:
                message_value = message.value
            except Exception as e:
                print(f"Error decoding message: {e}")
                continue
            
            print(f"Received message: {message}")
            if message.topic == ASSESSMENT_TOPIC1:
                socketio.emit('assessment_topic1_event_back', message_value)
                print(f"Emitted to 'assessment_topic1_event': {message_value}")
                buffer.append(message_value)
            elif message.topic == ASSESSMENT_TOPIC2:
                socketio.emit('assessment_topic2_event_back', message_value)
                print(f"Emitted to 'assessment_topic2_event': {message_value}")
                buffer.append(message_value)

            if len(buffer) >= BATCH_SIZE or (time.time() - last_commit_time) >= BATCH_INTERVAL:
                commit_to_database(app, buffer)
                last_commit_time = time.time()

        if buffer:
            commit_to_database(app, buffer)

def start_consumer(app, buffer):
    thread = threading.Thread(target=consume_messages, args=(app, buffer))
    thread.daemon = True
    thread.start()
