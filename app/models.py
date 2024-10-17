import base64
import enum
import uuid
from app import db

class Document(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(120), index=True)
    path = db.Column(db.String(120), index=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'path': self.path,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f'<Document {self.title}>'
    
class Conversations(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(120), index=True)
    title = db.Column(db.String(120), index=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f'<Conversations {self.title}>'
    
class Sender(enum.Enum):
    USER = 'user'
    BOT = 'bot'
    
class Messages(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation = db.relationship('Conversations', backref=db.backref('messages', lazy=True))
    conversation_id = db.Column(db.String(36), db.ForeignKey('conversations.id', ondelete="CASCADE"), index=True)
    message = db.Column(db.Text)
    sender = db.Column(db.Enum(Sender))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'message': self.message,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f'<Messages {self.message}>'