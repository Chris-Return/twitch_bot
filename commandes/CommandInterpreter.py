import time

class CommandInterpreter:
    def __init__(self, cooldown: int = 0):
        self.cooldown = cooldown    # temps en secondes
        self.last_used = 0          # timestamp de la dernière exécution
        self.actualTag = ""         # tag pour savoir si la commande sera activée ou non
        self.requiredRole = ""      # Roles requis pour utiliser la commande
        self.activationCommand = "" # Commande permettant d'activer le script

    def can_execute(self):
        return time.time() - self.last_used >= self.cooldown

    def execute(self, username: str, message: str, sock):
        """
        Méthode à override dans les classes filles.
        username: auteur du message
        message: contenu du message
        sock: socket IRC pour envoyer des messages
        """
        raise NotImplementedError