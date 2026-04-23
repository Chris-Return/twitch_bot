from commandes.CommandInterpreter import CommandInterpreter
from constantes import constantes
from models.AppUser import AppUser
from models.Role import Role
from database.session import get_session

class IASetRoleLevel(CommandInterpreter):
    def __init__(self):
        super().__init__()
        # Seuls les ADMIN peuvent déclencher cet outil via l'IA
        self.requiredRoleLevel = constantes.ROLE_LEVEL_CO_ADMIN 
        self.activationCommand = "SET_PERMISSION_LEVEL"

    def execute(self, username, message, twSock, args=None):
        if not args or len(args) < 2:
            print("Erreur : Arguments insuffisants pour SET_PERMISSION_LEVEL")
            return

        print(f"Arguments : {args}", flush=True)
        target_pseudo = args[0].replace("@", "").strip() # On nettoie le @ si l'IA l'ajoute

        # Sécurité
        if target_pseudo == "ChrisReturn":
            return
        
        new_role_name = args[1].upper().strip()

        with get_session() as session:
            # 1. On cherche l'utilisateur cible
            user = session.query(AppUser).filter(AppUser.pseudo == target_pseudo).first()
            if not user:
                return

            # 2. On cherche le rôle correspondant
            role = session.query(Role).filter(Role.name == new_role_name).first()
            if not role:
                return

            # 3. Mise à jour
            user.role = role
            session.commit()
            
            print(f"Changement de rôle : {target_pseudo} est maintenant {new_role_name}", flush=True)
            twSock.sendMessage(f"Permissions mises à jour : {target_pseudo} est désormais {new_role_name} ! chefsp1Hehe")