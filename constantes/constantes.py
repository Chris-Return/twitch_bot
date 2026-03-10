from dotenv import load_dotenv
import os

load_dotenv()

TWITCH_IRC_URL = os.getenv("TWITCH_IRC_URL", "irc.chat.twitch.tv")
TWITCH_IRC_PORT = int(os.getenv("TWITCH_IRC_PORT", 6667))

TWITCH_USERNAME = os.getenv("TWITCH_USERNAME")
TWITCH_OAUTH_TOKEN = os.getenv("TWITCH_OAUTH_TOKEN")

CHANNEL_NAME = os.getenv("CHANNEL_NAME")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")