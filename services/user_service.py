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

def get_user_role(username: str):
    """
    Récupère le nom du rôle d'un utilisateur.
    Retourne le nom du rôle (ex: "VIEWER", "MODO") ou None si l'utilisateur n'existe pas.
    """
    try:
        with get_session() as session:
            # On joint la table AppUser et Role pour avoir le nom du rôle directement
            result = (
                session.query(Role.name)
                .join(AppUser, AppUser.role_id == Role.id)
                .filter(AppUser.pseudo.ilike(username)) # ilike pour ignorer la casse
                .first()
            )
            
            if result:
                return result[0] # result est un tuple (name,)
            return None

    except Exception as e:
        print(f"[DB] Erreur lors de la récupération du rôle de {username} : {e}")
        return None
    
def get_user_level(username: str) -> int:
    """
    Récupère le niveau (level) du rôle d'un utilisateur.
    Retourne l'entier du niveau (ex: 999, 10, 1) ou 0 si l'utilisateur n'existe pas.
    """
    try:
        with get_session() as session:
            result = (
                session.query(Role.level)
                .join(AppUser, AppUser.role_id == Role.id)
                .filter(AppUser.pseudo.ilike(username))
                .first()
            )
            
            return result[0] if result else 0

    except Exception as e:
        print(f"[DB] Erreur lors de la récupération du niveau de {username} : {e}", flush=True)
        return 0

def update_user_role(username: str, role_name: str):
    """
    Change le rôle d'un utilisateur existant.
    Retourne True si le changement est réussi, False sinon.
    """
    try:
        with get_session() as session:
            # 1. On cherche l'utilisateur
            user = session.query(AppUser).filter_by(pseudo=username).first()
            if not user:
                print(f"[DB] Erreur : Utilisateur '{username}' introuvable.")
                return False

            # 2. On cherche le rôle cible
            # On passe le nom en majuscules pour être cohérent avec ton "VIEWER"
            role = session.query(Role).filter_by(name=role_name.upper()).first()
            if not role:
                print(f"[DB] Erreur : Le rôle '{role_name}' n'existe pas en base.")
                return False

            # 3. Mise à jour
            user.role_id = role.id
            # Pas besoin de session.add(user) car l'objet est déjà "attaché" à la session
            
            print(f"[DB] Rôle de {username} mis à jour : {role.name}")
            return True

    except Exception as e:
        print(f"[DB] Erreur lors de la mise à jour du rôle : {e}")
        return False