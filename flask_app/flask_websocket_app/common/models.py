from common.db import db

class Assessment(db.Model):
    __tablename__ = 'eba_assessments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(100))
    data = db.Column(db.JSON)

    def __repr__(self):
        return f'<Assessment {self.id} {self.topic}>'

class WeeklyChallenge(db.Model):
    __tablename__ = 'eba_weekly_challenges'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(100))
    data = db.Column(db.JSON)

    def __repr__(self):
        return f'<WeeklyChallenge {self.id} {self.topic}>'
