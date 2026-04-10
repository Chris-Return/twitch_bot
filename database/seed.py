from database.session import get_session
from models.Role import Role
from models.AppUser import AppUser

def seed_roles():
    with get_session() as session:
        # 1. Gestion des Rôles
        if session.query(Role).count() == 0:
            print("Ajout des rôles par défaut", flush=True)
            admin_role = Role(name="ADMIN", level=999)
            vip_role = Role(name="VIP", level=10)
            viewer_role = Role(name="VIEWER", level=1)
            
            session.add_all([admin_role, vip_role, viewer_role])
            # On flush pour que les objets Role reçoivent un ID de la BDD 
            # sans pour autant terminer la transaction tout de suite
            session.flush() 
        else:
            # Si les rôles existent déjà, on récupère l'objet ADMIN pour la suite
            admin_role = session.query(Role).filter_by(name="ADMIN").first()
            vip_role = session.query(Role).filter_by(name="VIP").first()

        # 2. Gestion des Utilisateurs
        if session.query(AppUser).count() == 0:
            print("Ajout des utilisateurs par défaut")

            session.add_all([
                AppUser(pseudo="ChefSpirite", role=admin_role),
                AppUser(pseudo="ChrisReturn", role=admin_role),
                AppUser(pseudo="Zarakaih", role=vip_role),
                AppUser(pseudo="minmaj", role=vip_role)
            ])
        
        # Le commit final valide toutes les insertions
        session.commit()