from sqlalchemy.orm import close_all_sessions

def shutdown_bot(twSock=None):
    """
    Ferme le socket Twitch et toutes les sessions SQLite.
    Peut prendre None si le bot n'était pas encore connecté.
    """
    print("Fermeture du socket Twitch et des sessions SQLite...", flush=True)
    
    if twSock:
        try:
            twSock.close()
            print("Socket Twitch fermé correctement", flush=True)
        except Exception as e:
            print("Erreur fermeture socket :", e, flush=True)
    
    try:
        close_all_sessions()
        print("SQLite fermé correctement", flush=True)
    except Exception as e:
        print("Erreur fermeture sessions SQLite :", e, flush=True)
    
    print("Bot arrêté avec succès", flush=True)