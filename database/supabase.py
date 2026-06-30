from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Read credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Validate credentials
if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is missing.")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY is missing.")

# Create Supabase client
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

print("✅ Supabase Connected Successfully!")