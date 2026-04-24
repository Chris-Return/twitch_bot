import os
import sys
import io
import random
from dotenv import load_dotenv
from google import genai
import time

class GeminiManager:
    def __init__(self, preprompt_filename="preprompt.md"):
        load_dotenv()
        
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Erreur : La clé API 'GEMINI_API_KEY' est manquante.")

        self.client = genai.Client(api_key=self.api_key)
        self.model_id = "gemini-3.1-flash-lite-preview"
        
        current_dir = os.path.dirname(__file__)
        self.preprompt_path = os.path.join(current_dir, preprompt_filename)
        
        # Initialisation de la session avec le socle commun
        self.chat_session = self._initialiser_session()

    def _charger_preprompt(self):
        """Charge les règles de base (TOS, personnalité générale)."""
        try:
            with open(self.preprompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "Tu es un bot Twitch. Sois bref et respecte les TOS."

    def _initialiser_session(self):
        return self.client.chats.create(
            model=self.model_id,
            config={
                "system_instruction": self._charger_preprompt(),
                "temperature": 0.8,
            }
        )

    def envoyer_message(self, message_utilisateur, fallback=True):
        """
        Tente d'envoyer un message jusqu'à 5 fois avec un délai croissant.
        """
        max_retries = 5
        base_delay = 1  # Attente de départ en secondes
        
        phrases_secours = [
            "Je prends une pause café, reviens plus tard. Kappa",
            "Mon cerveau est en train de fondre, réessaie dans une minute.",
            "Trop de messages, je ne vous écoute plus ! ResidentSleeper",
            "L'IA est momentanément partie en vacances. LUL",
            "Erreur 404 : Mon envie de répondre a disparu.",
            "Je réfléchis... Enfin, j'essaie. Repose ta question plus tard !"
        ]

        for attempt in range(max_retries):
            try:
                response = self.chat_session.send_message(message_utilisateur)
                return response.text
                
            except Exception as e:
                delay = min(base_delay * (2 ** attempt), 10)
                
                print(f"DEBUG - Essai {attempt + 1}/{max_retries} échoué : {e}", flush=True)
                
                if attempt < max_retries - 1:
                    time.sleep(delay)
                else:
                    # Si c'est le dernier essai et que ça échoue encore
                    return random.choice(phrases_secours) if fallback else None
        
    def lister_modeles_gemini():
        # Chargement de la clé API
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            print("Erreur : La clé GEMINI_API_KEY est manquante dans le fichier .env")
            return

        # Initialisation du client
        client = genai.Client(api_key=api_key)

        print(f"{'NOM DU MODÈLE':<40} | {'VERSIONS/CAPACITÉS'}")
        print("-" * 70)

        try:
            # Récupération de la liste des modèles
            # On itère sur les modèles disponibles pour ton compte
            for model in client.models.list():
                print(f"{model.name:<40} | {model.display_name}")
                
        except Exception as e:
            print(f"Erreur lors de la récupération des modèles : {e}")

    if __name__ == "__main__":
        lister_modeles_gemini()