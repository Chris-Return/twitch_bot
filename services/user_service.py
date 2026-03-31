from database.session import get_session
from models.AppUser import AppUser
from models.Role import Role
from sqlalchemy.exc import IntegrityError

DEFAULT_ROLE_NAME = "VIEWER"

def get_or_create_user(username: str):
    try:
        with get_session() as session:
            user = session.query(AppUser).filter_by(pseudo=username).first()
            if user:
                return

            role = session.query(Role).filter_by(name=DEFAULT_ROLE_NAME).first()

            if not role:
                role = Role(name=DEFAULT_ROLE_NAME)
                session.add(role)
                session.flush()

            new_user = AppUser(pseudo=username, role_id=role.id)
            session.add(new_user)

            print(f"[DB] Nouvel utilisateur créé : {username}")

    except IntegrityError:
        # utilisateur créé entre temps → OK
        print(f"[DB] User déjà créé (race condition) : {username}")