# import faust
# import json
# from datetime import datetime
# import logging
# from events import socketio
# import threading

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# faust_app = faust.App(
#     'faust-app',
#     broker='192.168.1.12:9092',
#     web_port=6066
# )

# submit_test_topic = faust_app.topic('submit_test', value_type=bytes)
# update_time_topic = faust_app.topic('update_time', value_type=bytes)
# # log_topic = faust_app.topic('log-topic', value_type=bytes)

# @faust_app.agent(submit_test_topic)
# async def process_submit_test(stream):
#     logger.info('Started process_submit_test agent')
#     async for event in stream:
#         logger.info(f'Received event in submit_test: {event}')
#         try:
#             event_data = json.loads(event.decode('utf-8'))
#             processed_value = {
#                 'table': 'event_based_architecture_test_submission',
#                 'data': {
#                     'test_submission': event_data['test_submission'],
#                     'student_name': event_data['student_name'],
#                     'test_id': event_data['test_id']
#                 }
#             }
#             # await log_topic.send(value=json.dumps(processed_value).encode('utf-8'))
#             socketio.emit('submitted_student_details', processed_value)
#             logger.info('Emitted submitted student details successfully')
#         except Exception as e:
#             logger.error(f'Error processing event in submit_test: {e}')

# @faust_app.agent(update_time_topic)
# async def process_update_time(stream):
#     logger.info('Started process_update_time agent')
#     async for event in stream:
#         logger.info(f'Received event in update_time: {event}')
#         try:
#             event_data = json.loads(event.decode('utf-8'))
#             processed_value = {
#                 'table': 'event_based_architecture_test_details',
#                 'data': {
#                     'test_id': event_data['test_id'],
#                     'test_name': event_data['test_name'],
#                     'start_time': datetime.strptime(event_data['start_time'], '%Y-%m-%dT%H:%M:%S')
#                 }
#             }
#             # await log_topic.send(value=json.dumps(processed_value, default=str).encode('utf-8'))
#             socketio.emit('updated_test_time', processed_value)
#             logger.info('Emitted updated test time successfully')
#         except Exception as e:
#             logger.error(f'Error processing event in update_time: {e}')

