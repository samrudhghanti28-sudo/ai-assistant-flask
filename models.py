from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interface = db.Column(db.String(20), nullable=False)
    task = db.Column(db.String(100), nullable=False)
    creative_type = db.Column(db.String(50), nullable=True)
    user_input = db.Column(db.Text, nullable=False)
    assistant_response = db.Column(db.Text, nullable=True)
    helpful = db.Column(db.String(3), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "interface": self.interface,
            "task": self.task,
            "creative_type": self.creative_type,
            "user_input": self.user_input,
            "assistant_response": self.assistant_response,
            "helpful": self.helpful,
            "timestamp": self.timestamp.isoformat()
        }