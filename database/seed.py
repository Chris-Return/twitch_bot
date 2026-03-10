from database import SessionLocal
from models.Role import Role

def seed_roles():
    """Initialise les rôles par défaut si aucun rôle n’existe"""
    session = SessionLocal()
    try:
        # Vérifie si la table Role est vide
        role_count = session.query(Role).count()
        if role_count == 0:
            print("Aucun rôle trouvé, ajout des rôles par défaut...")
            default_roles = [Role(name="ADMIN"), Role(name="VIEWER")]
            session.add_all(default_roles)
            session.commit()
            print("Rôles par défaut ajoutés !")
        else:
            print(f"{role_count} rôle(s) déjà présent(s), aucune action nécessaire.")
    except Exception as e:
        session.rollback()
        print("Erreur lors de l'initialisation des rôles :", e)
    finally:
        session.close()