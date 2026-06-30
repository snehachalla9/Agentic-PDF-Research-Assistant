from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

response = supabase.table("resume_score").select("*").limit(1).execute()

print("✅ Connected to Supabase!")
print(response.data)