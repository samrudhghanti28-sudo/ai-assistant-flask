from models import db, Feedback
from flask import current_app
import os

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///feedback.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

def append_feedback(data):
    feedback = Feedback(
        interface=data.get('interface', 'web'),
        task=data.get('task'),
        creative_type=data.get('creative_type'),
        user_input=data.get('user_input', ''),
        assistant_response=data.get('assistant_response', ''),
        helpful=data.get('helpful', 'no')
    )
    db.session.add(feedback)
    db.session.commit()
    return feedback

def read_all_feedback(limit=50):
    return [f.to_dict() for f in Feedback.query.order_by(Feedback.timestamp.desc()).limit(limit).all()]
