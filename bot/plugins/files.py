from hydrogram import filters
from hydrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from secrets import token_hex
from bot import TelegramBot
from bot.config import Telegram, Server
from bot.modules.decorators import verify_user
from bot.modules.static import *

@TelegramBot.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.video_note
        | filters.audio
        | filters.voice
        | filters.photo
    )
)
@verify_user
async def handle_user_file(_, msg: Message):
    """
    Handles user file uploads, stores them in the private channel,
    and generates Cloudflare-proxied streaming/download links.
    """
    sender_id = msg.from_user.id
    secret_code = token_hex(Telegram.SECRET_CODE_LENGTH)

    # Copy the user's file to your channel (acts as your private storage)
    file = await msg.copy(
        chat_id=Telegram.CHANNEL_ID,
        caption=f'||{secret_code}/{sender_id}||'
    )

    file_id = file.id

    # --- Base URL (use Cloudflare proxied domain if available) ---
    # Example: BASE_URL=https://files.yourdomain.com (set in .env)
    base_url = getattr(Server, "CF_BASE_URL", None) or Server.BASE_URL

    # --- Generate Cloudflare-optimized download/stream URLs ---
    dl_link = f'{base_url}/dl/{file_id}?code={secret_code}'
    stream_link = f'{base_url}/stream/{file_id}?code={secret_code}'

    # --- Inline keyboard buttons ---
    if (msg.document and msg.document.mime_type and 'video' in msg.document.mime_type) or msg.video:
        # For videos — show stream + download buttons
        await msg.reply(
            text=MediaLinksText % {'dl_link': dl_link, 'stream_link': stream_link},
            quote=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('📥 Download', url=dl_link),
                        InlineKeyboardButton('▶️ Stream', url=stream_link)
                    ],
                    [
                        InlineKeyboardButton('❌ Revoke', callback_data=f'rm_{file_id}_{secret_code}')
                    ]
                ]
            )
        )
    else:
        # For other file types — only download link
        await msg.reply(
            text=FileLinksText % {'dl_link': dl_link},
            quote=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('📥 Download', url=dl_link)
                    ],
                    [
                        InlineKeyboardButton('❌ Revoke', callback_data=f'rm_{file_id}_{secret_code}')
                    ]
                ]
            )
        )
