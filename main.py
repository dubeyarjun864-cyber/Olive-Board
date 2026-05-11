from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import *
from scraper import run_extraction
import os

app = Client("ArjunBotz", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

user_sessions = {} # {user_id: [email, pass]}

async def check_fjoin(client, user_id):
    try:
        member = await client.get_chat_member(CHANNEL_ID, user_id)
        return member.status not in ["left", "kicked"]
    except: return False

@app.on_message(filters.command("start"))
async def start(client, message):
    if not await check_fjoin(client, message.from_user.id):
        return await message.reply("⚠️ **Join our channel to use this bot!**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join @ArjunBotz 📢", url=CHANNEL_LINK)]]))
    
    await message.reply(f"👋 **Welcome Arjun!**\n\nUse `/login email*password` to begin.\n\nSupport: [Arjun Dubey]({ADMIN_LINK})", disable_web_page_preview=True)

@app.on_message(filters.command("login") & filters.user(ADMIN_IDS))
async def login(client, message):
    try:
        creds = message.text.split(" ", 1)[1]
        user_sessions[message.from_user.id] = creds.split("*")
        await message.reply("✅ **Login Successful!** Now use `/extract` to browse exams.")
    except: await message.reply("❌ Format: `/login email*password`")

@app.on_message(filters.command("extract") & filters.user(ADMIN_IDS))
async def extract_menu(client, message):
    await message.reply("🔍 **Search your exam name:**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("SSC CGL", callback_data="exam_ssccgl")],
            [InlineKeyboardButton("SSC CHSL", callback_data="exam_chsl")]
        ]))

@app.on_callback_query(filters.regex("^exam_"))
async def exam_selected(client, callback_query):
    await callback_query.message.edit("📑 **Select Sectional Type:**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("15 Minute Sectional Timing", callback_data="type_sectional_15")],
            [InlineKeyboardButton("Full Length Mock", callback_data="type_full")]
        ]))

@app.on_callback_query(filters.regex("^type_"))
async def start_fetch(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in user_sessions:
        return await callback_query.answer("❌ Please /login first!", show_alert=True)
    
    await callback_query.message.edit("⏳ **Extracting... Ye thoda samay le sakta hai.**")
    email, password = user_sessions[user_id]
    
    # Example URL based on selection
    file = run_extraction(email, password, "https://www.oliveboard.in/mock-test/", "SSC_CGL")
    
    caption = (
        "✨ **PREMIUM MOCK EXTRACTED** ✨\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Extracted By:** [Arjun Dubey]({ADMIN_LINK})\n"
        f"🤖 **Bot:** [ArjunBotz]({CHANNEL_LINK})\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )
    
    await client.send_document(callback_query.message.chat.id, file, caption=caption)
    os.remove(file)

@app.on_message(filters.command("admin"))
async def admin_cmd(client, message):
    await message.reply(f"👤 **Admin:** [Arjun Dubey]({ADMIN_LINK})\n📢 **Channel:** [ArjunBotz]({CHANNEL_LINK})", disable_web_page_preview=True)

@app.on_message(filters.command("logout"))
async def logout(client, message):
    user_sessions.pop(message.from_user.id, None)
    await message.reply("👋 **Logged out successfully.**")

app.run()
