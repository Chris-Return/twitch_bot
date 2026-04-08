import os
import sys
import io
import random
from dotenv import load_dotenv
from google import genai

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
        Envoie le message à l'IA. Si l'IA est indisponible, 
        renvoie une phrase de secours aléatoire.
        """
        # Liste de phrases de secours (style "banter" Twitch)
        phrases_secours = [
            "Je prends une pause café, reviens plus tard. Kappa",
            "Mon cerveau est en train de fondre, réessaie dans une minute.",
            "Trop de messages, je ne vous écoute plus ! ResidentSleeper",
            "L'IA est momentanément partie en vacances. LUL",
            "Erreur 404 : Mon envie de répondre a disparu.",
            "Je réfléchis... Enfin, j'essaie. Repose ta question plus tard !"
        ]

        try:
            response = self.chat_session.send_message(message_utilisateur)
            return response.text
            
        except Exception as e:
            print(f"DEBUG - Erreur API Gemini : {e}", flush=True) 
            return random.choice(phrases_secours) if fallback else None