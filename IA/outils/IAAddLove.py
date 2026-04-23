from commandes.CommandInterpreter import CommandInterpreter
from constantes import constantes
from models.AppUser import AppUser
from models.UserAffinity import UserAffinity
from database.session import get_session

class IAAddLove(CommandInterpreter):
    def __init__(self):
        super().__init__()
        self.requiredRoleLevel = constantes.ROLE_LEVEL_VIEWER_ASSIDU 
        self.activationCommand = "ADD_LOVE"

    def execute(self, username, message, twSock, args=None):
        if not args or len(args) < 2:
            return

        target_pseudo = args[0].replace("@", "").strip()
        
        try:
            points = int(args[1])
        except ValueError:
            return

        with get_session() as session:
            user_affinity = session.query(UserAffinity).join(AppUser).filter(AppUser.pseudo.ilike(target_pseudo)).first()
            
            if user_affinity:
                new_score = max(-100, min(100, user_affinity.love_score + points))
                user_affinity.love_score = new_score
                session.commit()
                print(f"[DB] Amour mis à jour pour {target_pseudo} : {new_score}")