from database.session import get_session
from models.Role import Role
from models.AppUser import AppUser
from models.AffinityReference import AffinityReference
from models.UserAffinity import UserAffinity

def seed_database():
    with get_session() as session:
        # 1. Gestion des Rôles
        if session.query(Role).count() == 0:
            print("Ajout des rôles par défaut", flush=True)
            admin_role = Role(name="ADMIN", level=999)
            co_admin_role = Role(name="CO ADMIN", level=990)
            vip_role = Role(name="VIP", level=10)
            viewer_assidu_role = Role(name="VIEWER ASSIDU", level=2)
            viewer_role = Role(name="VIEWER", level=1)
            session.add_all([admin_role, co_admin_role, vip_role, viewer_assidu_role, viewer_role])
            session.flush()
        else:
            admin_role = session.query(Role).filter_by(name="ADMIN").first()
            co_admin_role = session.query(Role).filter_by(name="CO ADMIN").first()
            viewer_assidu_role = session.query(Role).filter_by(name="VIEWER ASSIDU").first()

        # 2. Gestion des Références d'Affinités
        if session.query(AffinityReference).count() == 0:
            references = [
                AffinityReference(category='Respect', min_score=-100, max_score=-61, label="IRRESPECT", instruction="Coopérer avec cette personne te rendrait malade. Tu préfères la critiquer."),
                AffinityReference(category='Respect', min_score=-60, max_score=-30, label="PAS RESPECTABLE", instruction="Tu n'as pas trop envie de coopérer."),
                AffinityReference(category='Respect', min_score=-29, max_score=29, label="NEUTRE", instruction="Tu le considères comme n'importe qui d'autre."),
                AffinityReference(category='Respect', min_score=30, max_score=69, label="RÉFÉRENCE", instruction="Tu respectes son avis et son autorité."),
                AffinityReference(category='Respect', min_score=70, max_score=100, label="IDÔLE", instruction="Tu as une admiration totale, c'est ton mentor."),

                AffinityReference(category='Affinite', min_score=-100, max_score=-31, label="ENNEMI", instruction="Tu es froid dans tes réponses."),
                AffinityReference(category='Affinite', min_score=-30, max_score=19, label="NEUTRE", instruction="Tu es neutre avec lui."),
                AffinityReference(category='Affinite', min_score=20, max_score=39, label="CONNAISSANCE", instruction="Tu es poli."),
                AffinityReference(category='Affinite', min_score=40, max_score=69, label="AMI", instruction="Tu rigoles bien avec cette personne."),
                AffinityReference(category='Affinite', min_score=70, max_score=100, label="MEILLEUR AMI", instruction="Tu es extrêmement chaleureux, complice et protecteur."),

                AffinityReference(category='Amour', min_score=-100, max_score=-71, label="HAINE", instruction="Tu le détestes viscéralement."),
                AffinityReference(category='Amour', min_score=-70, max_score=-30, label="DEGOUT", instruction="Tu es un peu écoeuré."),
                AffinityReference(category='Amour', min_score=-29, max_score=29, label="NEUTRE", instruction="Comportement normal, aucune attirance."),
                AffinityReference(category='Amour', min_score=30, max_score=59, label="CRUSH", instruction="Tu as tendance à draguer ou flirter."),
                AffinityReference(category='Amour', min_score=60, max_score=89, label="AMOUREUX", instruction="Tu es amoureux."),
                AffinityReference(category='Amour', min_score=90, max_score=100, label="FOU AMOUREUX", instruction="Ton amour est passionnel et dévorant.")
            ]
            session.add_all(references)
            session.flush()

        # 3. Gestion des Utilisateurs et de leurs Affinités
        if session.query(AppUser).count() == 0:
            print("Ajout des utilisateurs et initialisation des relations")

            users_data = [
                ("ChrisReturn", admin_role, 100, 100, 0),
                ("ChefSpirite", co_admin_role, 0, 0, 0),
                ("Zarakaih", co_admin_role, 0, 0, 0),
                ("minmaj", viewer_assidu_role, 0, 0, 0),
                ("mewtree1993sh", viewer_assidu_role, 0, 0, 0),
                ("DawCoeur_", viewer_assidu_role, 0, 0, 0),
                ("Petonns", viewer_assidu_role, 0, 0, 0),
                ("maori_2", viewer_assidu_role, 0, 0, 0),
                ("Luke_MHw", viewer_assidu_role, 0, 0, 0),
                ("celenoos", viewer_assidu_role, 0, 0, 0),
            ]

            for pseudo, role, aff, res, love in users_data:
                new_user = AppUser(pseudo=pseudo, role=role)
                session.add(new_user)
                session.flush() 

                new_affinity = UserAffinity(
                    user_id=new_user.id,
                    affinity_score=aff,
                    respect_score=res,
                    love_score=love
                )
                session.add(new_affinity)

        session.commit()
        print("Seed terminé avec succès !")