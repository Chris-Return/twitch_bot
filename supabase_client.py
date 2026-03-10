from supabase import create_client, Client
from constantes import constantes

supabase: Client = create_client(constantes.SUPABASE_URL, constantes.SUPABASE_SERVICE_ROLE_KEY)