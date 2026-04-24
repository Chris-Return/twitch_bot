
class ConversationHistory:
    """
    Classe gérant l'historique de la conversation.
    Utilise le pattern Singleton pour garantir une seule instance globale.
    """
    _instance = None

    def __new__(cls, max_length=50):
        if cls._instance is None:
            cls._instance = super(ConversationHistory, cls).__new__(cls)
            # Initialisation des attributs
            cls._instance.history = []
            cls._instance.max_length = max_length
        return cls._instance

    def add_message(self, user, message):
        """Ajoute un message formaté à la liste."""
        formatted_entry = f"{user}: {message}"
        self.history.append(formatted_entry)

        # On garde seulement les 'max_length' derniers messages
        if len(self.history) > self.max_length:
            self.history.pop(0)

    def get_context(self):
        """Retourne l'historique sous forme d'une seule chaîne de caractères."""
        return "\n".join(self.history)
    
    def get_number_of_context(self):
        return self.history.__len__()

    def clear(self):
        """Efface l'historique."""
        self.history = []

# Instance globale prête à l'emploi
twitch_history = ConversationHistory(max_length=20)