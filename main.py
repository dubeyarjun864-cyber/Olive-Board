from pyrogram import Client, filters
from config import *
from scraper import extract_mock_data
import os

app = Client("ArjunBotz", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("🔥 **ArjunBotz Premium Extractor Ready!**\\nUse /login to start.")

@app.on_message(filters.command("extract") & filters.user(ADMIN_IDS))
async def extract(client, message):
    url = message.text.split(" ")[1]
    status = await message.reply("⏳ **Processing...**")
    
    # Replace with logic to get stored email/pass
    file = extract_mock_data("YOUR_EMAIL", "YOUR_PASSWORD", url)
    
    caption = "✨ **PREMIUM MOCK EXTRACTED** ✨\\n\\n👤 **By:** [Arjun Dubey](https://t.me/Arjun_Dubey)\\n🤖 **Channel:** [ArjunBotz](https://t.me/ArjunBotz)"
    await message.reply_document(file, caption=caption)
    os.remove(file)
    await status.delete()

app.run()
