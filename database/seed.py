from database.session import get_session
from models.Role import Role
from models.AppUser import AppUser

def seed_roles():
    with get_session() as session:
        # 1. Gestion des Rôles
        if session.query(Role).count() == 0:
            print("Ajout des rôles par défaut", flush=True)
            admin_role = Role(name="ADMIN", level=999)
            co_admin_role = Role(name="CO ADMIN", level= 990)
            vip_role = Role(name="VIP", level=10)
            viewer_assidu_role = Role(name="VIEWER ASSIDU", level=2)
            viewer_role = Role(name="VIEWER", level=1)
            session.add_all([admin_role, co_admin_role, vip_role, viewer_assidu_role, viewer_role])
            session.flush()
        else:
            # Si les rôles existent déjà, on récupère l'objet ADMIN pour la suite
            admin_role = session.query(Role).filter_by(name="ADMIN").first()
            vip_role = session.query(Role).filter_by(name="VIP").first()

        # 2. Gestion des Utilisateurs
        if session.query(AppUser).count() == 0:
            print("Ajout des utilisateurs par défaut")

            session.add_all([
                AppUser(pseudo="ChrisReturn", role=admin_role),
                AppUser(pseudo="ChefSpirite", role=co_admin_role),
                AppUser(pseudo="Zarakaih", role=co_admin_role),
                AppUser(pseudo="minmaj", role=viewer_assidu_role),
                AppUser(pseudo="mewtree1993sh", role=viewer_assidu_role),
                AppUser(pseudo="DawCoeur_", role=viewer_assidu_role),
                AppUser(pseudo="Petonns", role=viewer_assidu_role),
                AppUser(pseudo="maori_2", role=viewer_assidu_role),
                AppUser(pseudo="Luke_MHw", role=viewer_assidu_role),
                AppUser(pseudo="celenoos", role=viewer_assidu_role)
            ])
        
        # Le commit final valide toutes les insertions
        session.commit()