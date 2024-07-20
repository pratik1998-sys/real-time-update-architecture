from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class studentTestSubmission(db.Model):
    __tablename__ = 'event_based_architecture_test_submission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    test_submission = db.Column(db.Integer)
    student_name = db.Column(db.String(100))
    test_id = db.Column(db.Integer)

    def __repr__(self):
        return f'<StudentSubmission {self.student_name}>'

class EventBasedArchitectureTestDetail(db.Model):
    __tablename__ = 'event_based_architecture_test_details'
    test_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    test_name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime)

    def __repr__(self):
        return f'<EventBasedArchitectureTestDetail {self.test_id} {self.start_time}>'
