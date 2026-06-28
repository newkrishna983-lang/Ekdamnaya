from pyrogram import filters
from pyrogram.types import Message
from db import db

async def add_user_cmd(client, message: Message):
    if not db.is_admin(message.from_user.id):
        await message.reply_text("❌ You are not an admin.")
        return
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("❌ Use: /add user_id [username]")
        return
    try:
        user_id = int(args[1])
        username = args[2] if len(args) > 2 else None
        db.add_user(user_id, username)
        await message.reply_text(f"✅ User {user_id} added.")
    except ValueError:
        await message.reply_text("❌ Invalid user ID.")

async def remove_user_cmd(client, message: Message):
    if not db.is_admin(message.from_user.id):
        await message.reply_text("❌ You are not an admin.")
        return
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("❌ Use: /remove user_id")
        return
    try:
        user_id = int(args[1])
        db.remove_user(user_id)
        await message.reply_text(f"✅ User {user_id} removed.")
    except ValueError:
        await message.reply_text("❌ Invalid user ID.")

async def list_users_cmd(client, message: Message):
    if not db.is_admin(message.from_user.id):
        await message.reply_text("❌ You are not an admin.")
        return
    users = db.list_users()
    if not users:
        await message.reply_text("📋 No authorized users.")
    else:
        text = "**Authorized Users:**\n"
        for uid, uname in users:
            text += f"- {uid} ({uname or 'no username'})\n"
        await message.reply_text(text)

async def my_plan_cmd(client, message: Message):
    # Simple plan info (you can extend)
    await message.reply_text("📋 Your plan: Premium (unlimited downloads)")
