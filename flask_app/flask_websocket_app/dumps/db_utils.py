from flask_websocket_app.dumps.models import studentTestSubmission, EventBasedArchitectureTestDetail, db
from flask_websocket_app.dumps.events import uncommitted_messages
from threading import Lock

commit_lock = Lock()

def commit_to_database(app,buffer):
    print(buffer)
    with commit_lock:
        try:
           with app.app_context():      
              for obj in buffer:
                  if isinstance(obj, studentTestSubmission):
                      print('adding student details for test submission')
                      db.session.add(obj)                   
                  elif isinstance(obj, EventBasedArchitectureTestDetail):
                      print('updating examination timing')
                      existing_test_detail = EventBasedArchitectureTestDetail.query.get(obj.test_id)
                      if existing_test_detail:
                          existing_test_detail.start_time = obj.start_time
                          db.session.add(existing_test_detail)
                      else:
                          print('test not available')
              
              db.session.commit()
              print('DB updated successfully')

              for topic in uncommitted_messages:
                  uncommitted_messages[topic].clear()

              buffer.clear()

        except Exception as e:
            with app.app_context():
                db.session.rollback()
                print(f"Error inserting into MySQL: {e}")
