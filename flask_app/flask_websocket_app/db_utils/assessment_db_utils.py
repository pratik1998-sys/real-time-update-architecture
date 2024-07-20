from common.models import Assessment, db
from threading import Lock

commit_lock = Lock()

def commit_to_database(app, buffer):
    with commit_lock:
        try:
            with app.app_context():
                for message in buffer:
                    assessment = Assessment(
                        topic=message.get('topic'),
                        data=message.get('data')
                    )
                    db.session.add(assessment)
                db.session.commit()
                print(buffer)
                buffer.clear()
        except Exception as e:
            with app.app_context():
                db.session.rollback()
                print(f"Error inserting into MySQL: {e}")
