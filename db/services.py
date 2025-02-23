from typing import Optional, List
from sqlalchemy.orm import Session
from .models import User, Conversation, Message

def get_or_create_user(db: Session, telegram_id: int, username: Optional[str] = None,
                      first_name: Optional[str] = None, last_name: Optional[str] = None) -> User:
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def create_conversation(db: Session, user: User, title: Optional[str] = None) -> Conversation:
    conversation = Conversation(user_id=user.id, title=title)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def add_message(db: Session, conversation_id: int, role: str, content: str) -> Message:
    message = Message(conversation_id=conversation_id, role=role, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_conversation_messages(db: Session, conversation_id: int) -> List[dict]:
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()
    return [{'role': msg.role, 'content': msg.content} for msg in messages]

def get_user_conversations(db: Session, user_id: int) -> List[Conversation]:
    return db.query(Conversation).filter(Conversation.user_id == user_id).all()

def get_all_users(db: Session) -> List[User]:
    return db.query(User).all()