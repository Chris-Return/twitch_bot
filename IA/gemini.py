import os
import sys
import io
from dotenv import load_dotenv
from google import genai

class GeminiManager:
    def __init__(self, preprompt_filename="preprompt.md"):
        load_dotenv()
        
        # Configuration de l'encodage pour la console
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Erreur : La clé API 'GEMINI_API_KEY' est manquante.")

        self.client = genai.Client(api_key=self.api_key)
        self.model_id = "gemini-3.1-flash-lite-preview"
        
        # Chemin dynamique vers le preprompt dans le dossier IA
        current_dir = os.path.dirname(__file__)
        self.preprompt_path = os.path.join(current_dir, preprompt_filename)
        
        # Initialisation de la session avec le contexte Twitch
        self.chat_session = self._initialiser_session()

    def _charger_preprompt(self):
        """Récupère les règles de conduite et le style de réponse (piques Twitch)."""
        try:
            with open(self.preprompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            # Fallback si le fichier est absent : on définit un comportement par défaut
            return (
                "Tu es un bot Twitch humoristique. Tu dois générer des petites piques "
                "ironiques mais toujours respectueuses et conformes aux règles de Twitch."
            )

    def _initialiser_session(self):
        """
        Crée la session de chat. Le preprompt est injecté ici en tant qu'instruction 
        système, l'IA s'en souviendra durant toute la durée de l'objet.
        """
        instructions = self._charger_preprompt()
        
        return self.client.chats.create(
            model=self.model_id,
            config={
                "system_instruction": instructions,
                "temperature": 0.8, # Un peu plus élevé pour favoriser l'humour/créativité
            }
        )

    def envoyer_message(self, message_utilisateur):
        """
        Prend un message (ex: issu de la BDD) et retourne la pique de l'IA.
        """
        try:
            # Envoi simple du texte sans gestion d'image
            response = self.chat_session.send_message(message_utilisateur)
            return response.text
        except Exception as e:
            return f"Erreur lors de la génération de la pique : {e}"

# --- TEST RAPIDE ---
if __name__ == "__main__":
    bot = GeminiManager()
    # Simulation d'un message Twitch récupéré
    test_msg = "On peut farmer des rires de bébés"
    print(f"User: {test_msg}")
    print(f"Bot: {bot.envoyer_message(test_msg)}")