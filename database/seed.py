from database import SessionLocal
from models.Role import Role
from supabase_client import supabase

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

def seed_roles_api():
    # Vérifie si la table "Role" est vide
    response = supabase.table("roles").select("*").execute()
    roles = response.data

    if not roles:
        print("Aucun rôle trouvé, ajout des rôles par défaut...")
        default_roles = [{"name": "ADMIN"}, {"name": "VIEWER"}]
        supabase.table("roles").insert(default_roles).execute()
        print("Rôles par défaut ajoutés !")
    else:
        print(f"{len(roles)} rôle(s) déjà présent(s), aucune action nécessaire.")