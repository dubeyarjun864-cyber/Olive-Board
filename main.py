from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from scraper import run_extraction
import os

app = Client("ArjunBotz", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

user_sessions = {}

async def check_fjoin(client, user_id):
    try:
        member = await client.get_chat_member(CHANNEL_ID, user_id)
        return member.status not in ["left", "kicked"]
    except: return False

@app.on_message(filters.command("start"))
async def start(client, message):
    if not await check_fjoin(client, message.from_user.id):
        return await message.reply("⚠️ **Join @ArjunBotz to use this bot!**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Channel 📢", url=CHANNEL_LINK)]]))
    await message.reply(f"👋 Welcome! Use `/login email*pass` to start.")

@app.on_message(filters.command("login") & filters.user(ADMIN_IDS))
async def login(client, message):
    try:
        creds = message.text.split(" ", 1)[1]
        user_sessions[message.from_user.id] = creds.split("*")
        await message.reply("✅ **Login Successful!** Now use `/extract`.")
    except: await message.reply("❌ Use: `/login email*pass`.")

@app.on_message(filters.command("extract") & filters.user(ADMIN_IDS))
async def extract_menu(client, message):
    await message.reply("🔍 **Select Exam:**", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("SSC CGL", callback_data="exam_ssccgl")]
    ]))

@app.on_callback_query(filters.regex("^exam_"))
async def fetch(client, cb):
    await cb.message.edit("⏳ **Extracting...**")
    email, password = user_sessions[cb.from_user.id]
    file = run_extraction(email, password, "https://www.oliveboard.in/", "SSC_CGL")
    
    caption = f"✨ **PREMIUM MOCK** ✨\n👤 **By:** [Arjun Dubey]({ADMIN_LINK})\n🤖 **Channel:** [ArjunBotz]({CHANNEL_LINK})"
    await client.send_document(cb.message.chat.id, file, caption=caption)
    os.remove(file)

@app.on_message(filters.command("admin"))
async def admin(client, message):
    await message.reply(f"Contact: [Arjun Dubey]({ADMIN_LINK})")

app.run()
