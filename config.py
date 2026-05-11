import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
# Admin IDs ko comma se separate karein .env mein: 12345,67890
ADMIN_IDS = [int(i.strip()) for i in os.getenv("ADMIN_IDS", "").split(",") if i.strip()]
CHANNEL_ID = os.getenv("CHANNEL_ID", "@ArjunBotz")
ADMIN_USERNAME = "@Arjun_Dubey"
