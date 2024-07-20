from flask_socketio import emit, SocketIO
import time

socketio = SocketIO()

# Function to send messages with acknowledgment
# def send_to_client(event, data, timeout=2):
#     ack_received = False

#     def ack():
#         nonlocal ack_received
#         ack_received = True

#     socketio.emit(event, data, callback=ack)

#     # Wait for acknowledgment
#     start_time = time.time()
#     while not ack_received and (time.time() - start_time) < timeout:
#         socketio.sleep(0.1)

#     if not ack_received:
#         print(f"Acknowledgment not received for event {event}, resending...")
#         socketio.emit(event, data, callback=ack)
