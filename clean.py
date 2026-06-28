from pyrogram import filters

def register_clean_handler(bot):
    @bot.on_message(filters.command("clean") & filters.private)
    async def clean_cmd(client, message):
        await message.reply_text("🧹 Cleaned temporary files.")
        # Add your cleanup logic
