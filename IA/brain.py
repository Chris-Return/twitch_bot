import re
import shlex
from commandes.CommandInterpreter import CommandInterpreter
from services.user_service import get_user_level, get_user_role
from services.useraffinity_service import get_user_affinity_context
from constantes import constantes
from .outils.IASendMessage import IASendMessage
from .outils.IASetRoleLevel import IASetRoleLevel
from .outils.IAAddAffinity import IAAddAffinity
from .outils.IAAddLove import IAAddLove
from .outils.IAAddRespect import IAAddRespect
from .outils.IASilence import IASilence
from IA.ConversationHistory import twitch_history
import threading

class IABrain(CommandInterpreter):
    def __init__(self, gemini_bot, cooldown=10):
        super().__init__(cooldown)
        self.minMessagesBeforeTalk = 30
        self.activationCommand = "cheffouhighbot"
        self.gemini_bot = gemini_bot
        self.messageCounter = 0
        self.IAinterpreters = [
            IASendMessage(),
            IASetRoleLevel(),
            IAAddRespect(),   
            IAAddAffinity(),   
            IAAddLove(),
            IASilence(),
        ]

    def execute(self, username, message, twSock):
        user_role_level = get_user_level(username)
        user_role_name = get_user_role(username)

        if user_role_level < constantes.ROLE_LEVEL_VIEWER_ASSIDU:
            return
        
        thread = threading.Thread(
            target=self.execute_async_wrapper, 
            args=(username, message, twSock, user_role_name, user_role_level)
        )
        thread.daemon = True
        thread.start()

    def before_execute(self, twSock):
        self.messageCounter += 1
        if self.messageCounter > self.minMessagesBeforeTalk:
            history_len = twitch_history.get_number_of_context()
            if history_len > self.minMessagesBeforeTalk:
                history_context = twitch_history.get_context()
                twitch_history.clear()
                self.messageCounter = 0
                prompt = (
                    f"Analyse l'historique du chat. Si tu n'as aucune remarque pertinente, choisi le SILENCE"
                    f"Tu peux mentionner directement des utilisateurs.\n"
                    f"Tu peux également attribuer des points aux utilisateurs en fonction de ce qu'ils se disent l'un/l'autre"
                    f"Historique du chat :\n"
                    f"{history_context}\n"
                )

                response = self.gemini_bot.envoyer_message(prompt)
                print(f"Analyse du Contexte de l'IA : {response}", flush=True)
                if not response:
                    return
                
                commands = re.findall(r'\[(\w+)[\s:]+(.*?)\]', response)
                for command_name, command_args in commands:
                    try:
                        clean_args_str = command_args.replace('“', '"').replace('”', '"')
                        args = shlex.split(clean_args_str)
                        
                    except ValueError:
                        args = [command_args.strip('" ')]

                    for interpreter in self.IAinterpreters:
                        if constantes.ROLE_LEVEL_VIP >= interpreter.requiredRoleLevel and command_name == interpreter.activationCommand:
                            try:
                                interpreter.execute(constantes.TWITCH_USERNAME, "", twSock, args)
                            except Exception as e:
                                print(f"Erreur d'exécution dans {command_name}: {e}")
                

        
    def execute_async_wrapper(self, username, message, twSock, user_role_name, user_role_level):
        try:
            history_context = twitch_history.get_context()
            twitch_history.clear()
            relation_context = get_user_affinity_context(username)

            prompt = (
                f"Contexte relationnel avec l'utilisateur {username} :\n"
                f"{relation_context}\n"
                f"Historique du chat :\n"
                f"{history_context}\n"
                f"--- \n"
                f"L'utilisateur {username} dispose du rôle {user_role_name} et vient de dire : {message}."
                f"Réponds-lui en tenant compte du contexte ci-dessus si nécessaire. "
                f"Adresse-toi directement au(x) concerné(s)."
            )

            response = self.gemini_bot.envoyer_message(prompt)
            print(f"Réponse de l'IA : {response}", flush=True)
            if not response:
                return

            commands = re.findall(r'\[(\w+)[\s:]+(.*?)\]', response)
            for command_name, command_args in commands:
                try:
                    clean_args_str = command_args.replace('“', '"').replace('”', '"')
                    args = shlex.split(clean_args_str)
                    
                except ValueError:
                    args = [command_args.strip('" ')]

                for interpreter in self.IAinterpreters:
                    if user_role_level >= interpreter.requiredRoleLevel and command_name == interpreter.activationCommand:
                        try:
                            interpreter.execute(username, message, twSock, args)
                        except Exception as e:
                            print(f"Erreur d'exécution dans {command_name}: {e}")

        except Exception as e:
            print(f"Erreur lors de la récupération de message IABrain : {e}", flush=True)