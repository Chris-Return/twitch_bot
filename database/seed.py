from database.session import get_session
from models.Role import Role

def seed_roles():
    with get_session() as session:

        role_count = session.query(Role).count()

        if role_count == 0:
            print("Ajout des rôles par défaut")
            session.add_all([
                Role(name="ADMIN", level=999),
                Role(name="VIP", level=10),
                Role(name="VIEWER", level=1)
            ])