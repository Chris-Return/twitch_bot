from models.UserAffinity import UserAffinity
from models.AffinityReference import AffinityReference
from sqlalchemy import and_
from database.session import get_session
from models.AppUser import AppUser

def get_user_affinity_context(username: str) -> str:
    """
    Récupère les libellés et instructions pour les 3 catégories (Affinité, Respect, Amour).
    Retourne un bloc de texte formaté pour le prompt de l'IA.
    """
    try:
        with get_session() as session:
            # 1. On récupère les scores de l'utilisateur
            user_affinity = (
                session.query(UserAffinity)
                .join(AppUser)
                .filter(AppUser.pseudo.ilike(username))
                .first()
            )

            if not user_affinity:
                return "Tu ne connais pas encore bien cet utilisateur. Sois neutre."

            # 2. On récupère les références correspondantes aux 3 scores
            # On cherche les lignes où le score est entre min et max pour chaque catégorie
            categories = [
                ('Affinite', user_affinity.affinity_score),
                ('Respect', user_affinity.respect_score),
                ('Amour', user_affinity.love_score)
            ]
            
            summary = []
            for cat_name, score in categories:
                ref = session.query(AffinityReference).filter(
                    and_(
                        AffinityReference.category == cat_name,
                        AffinityReference.min_score <= score,
                        AffinityReference.max_score >= score
                    )
                ).first()
                
                if ref:
                    summary.append(f"- {cat_name.capitalize()} [{ref.label}] : {ref.instruction}")

            return "\n".join(summary)

    except Exception as e:
        print(f"[DB] Erreur affinity context pour {username} : {e}")
        return "Erreur lors de la récupération de la relation. Sois neutre."