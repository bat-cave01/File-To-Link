from hydrogram import filters
import asyncio
from secrets import token_hex
from hydrogram.types import Message,InlineKeyboardMarkup, InlineKeyboardButton
from bot import TelegramBot
from bot.config import Telegram, Server
from bot.modules.static import *
from bot.modules.decorators import verify_user

@TelegramBot.on_message(filters.command(['start', 'help']) & filters.private)
@verify_user
async def start_command(_, msg: Message):
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("ℹ️ Help", callback_data="show_help"),
                InlineKeyboardButton("📌 About", callback_data="show_about")
            ]
        ]
    )
    await msg.reply(
        text=WelcomeText % {'first_name': msg.from_user.first_name},
        reply_markup=buttons,
        quote=True
    )

@TelegramBot.on_message(filters.command('privacy') & filters.private)
@verify_user
async def privacy_command(_, msg: Message):
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("✖️ Close", callback_data="close_msg")]]
    )
    await msg.reply(
        text=PrivacyText,
        quote=True,
        disable_web_page_preview=True,
        reply_markup=buttons
    )

@TelegramBot.on_message(filters.command("log") & filters.private & filters.user(Telegram.OWNER_ID))
async def log_command(_, msg: Message):
    try:
        await msg.reply_document("event-log.txt", quote=True)
    except FileNotFoundError:
        await msg.reply("❌ Log file not found.")



@TelegramBot.on_message(filters.command("link"))
async def generate_link(_, msg: Message):
    if not msg.reply_to_message:
        return await msg.reply("❌ You must reply to a file to generate a link.", quote=True)

    replied = msg.reply_to_message
    caption = replied.caption or ""

    # Safe user ID
    user_id = msg.from_user.id if msg.from_user else 0

    # If the file was already processed
    if "||" in caption:
        try:
            content = caption.strip("||")
            secret_code, original_user_id = content.split("/")
            file_id = replied.id
        except Exception:
            return await msg.reply("❌ Unable to extract link information.", quote=True)
    else:
        # If the file was NOT processed, copy to main channel to generate secret_code
        secret_code = token_hex(Telegram.SECRET_CODE_LENGTH)
        file_msg = await replied.copy(
            chat_id=Telegram.CHANNEL_ID,
            caption=f'||{secret_code}/{user_id}||'
        )
        file_id = file_msg.id

    # Generate links
    dl_link = f"{Server.BASE_URL}/dl/{file_id}?code={secret_code}"
    stream_link = ""
    if (replied.document and "video" in replied.document.mime_type) or replied.video:
        stream_link = f"{Server.BASE_URL}/stream/{file_id}?code={secret_code}"

    # Buttons
    buttons = [[InlineKeyboardButton("Download", url=dl_link)]]
    if stream_link:
        buttons[0].append(InlineKeyboardButton("Stream", url=stream_link))
    buttons.append([InlineKeyboardButton("Revoke", callback_data=f"rm_{file_id}_{secret_code}")])

    # Reply with links
    text = MediaLinksText % {"dl_link": dl_link, "stream_link": stream_link, "first_name": (msg.from_user.first_name if msg.from_user else "User")} \
        if stream_link else FileLinksText % {"dl_link": dl_link}

    await msg.reply(text=text, quote=True, reply_markup=InlineKeyboardMarkup(buttons))