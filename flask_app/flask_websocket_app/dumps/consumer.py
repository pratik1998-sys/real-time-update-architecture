import threading
import time
import random
import json
from kafka import KafkaConsumer
from flask_socketio import emit
from flask_websocket_app.dumps.config import KAFKA_BROKER_URL, TOPIC, TOPIC1, TOPIC2
from flask_websocket_app.dumps.models import studentTestSubmission, EventBasedArchitectureTestDetail, db
from db_utils import commit_to_database
from flask_websocket_app.dumps.events import socketio, uncommitted_messages
from datetime import datetime


consumer = None
consumer_thread = None
running = True
commit_lock = threading.Lock()

consumer = KafkaConsumer(
    TOPIC, TOPIC1, TOPIC2,
    bootstrap_servers=KAFKA_BROKER_URL,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda m: json.loads(m.decode('ascii'))
)


def consume_messages(app,buffer):
    BATCH_SIZE = 50
    BATCH_INTERVAL = 5
    
    last_commit_time = time.time()

    with app.app_context(): 
        for message in consumer:
            try:
                message_value = message.value  
            except Exception as e:
                continue

            if message.topic == 'submit_test':
                socketio.emit('submitted_student_details', message_value)
                print('emit submitted student details successfully')
                uncommitted_messages[TOPIC1].append(message_value)
                new_submission = studentTestSubmission(
                    id=message_value['id'],
                    student_name=message_value['name'],
                    test_submission=random.randint(0, 1),
                    test_id=message_value['test_id']
                )
                buffer.append(new_submission)
            elif message.topic == 'update_time':
                socketio.emit('updated_test_time', message_value)
                print('emitted update test timing successfully')
                uncommitted_messages[TOPIC2].append(message_value)
                updated_test_details = EventBasedArchitectureTestDetail(
                    test_id=message_value['test_id'],
                    start_time=message_value['updated_time']
                )
                buffer.append(updated_test_details)
                
            if len(buffer) >= BATCH_SIZE or (time.time() - last_commit_time) >= BATCH_INTERVAL:
                commit_to_database(app,buffer)
                last_commit_time = time.time()

    if buffer:
        commit_to_database(app,buffer)

def start_consumer(app,buffer):
    thread = threading.Thread(target=consume_messages,args=(app,buffer))
    thread.daemon = True
    thread.start()

def periodic_commit(app, buffer, interval=5):
    while running:
        time.sleep(interval)
        with commit_lock:
            if buffer:
              commit_to_database(app,buffer)

def start_periodic_commit(app, buffer, interval=5):
    periodic_thread = threading.Thread(target=periodic_commit, args=(app, buffer, interval))
    periodic_thread.daemon = True
    periodic_thread.start()
