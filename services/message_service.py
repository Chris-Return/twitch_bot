from database.session import get_session
from models.AppUser import AppUser
from models.ChatMessage import ChatMessage
from sqlalchemy import desc
from sqlalchemy import func

def save_twitch_message(username, content, skip_user_check=False):
    with get_session() as db:
        user_id = None
        
        if not skip_user_check:
            user = db.query(AppUser).filter(AppUser.pseudo == username).first()
            if not user:
                user = AppUser(pseudo=username, role_id=1)
                db.add(user)
                db.flush() 
            user_id = user.id
        else:
            user = db.query(AppUser).filter(AppUser.pseudo == username).first()
            user_id = user.id

        # Insertion du message
        new_msg = ChatMessage(content=content, user_id=user_id)
        db.add(new_msg)

def get_last_messages_from_db(pseudo, limit=40):
    """Récupère les X derniers messages d'un utilisateur spécifique."""
    with get_session() as db:
        messages = (
            db.query(ChatMessage.content)
            .join(AppUser)
            .filter(func.lower(AppUser.pseudo) == pseudo.lower())
            .order_by(desc(ChatMessage.created_at))
            .limit(limit)
            .all()
        )

        return [m.content for m in messages]