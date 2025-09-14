from hydrogram import Client, enums
from hydrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Union, Callable
from functools import wraps
from bot.config import Telegram
from bot.modules.static import *

def verify_user(func: Callable):

    @wraps(func)
    async def decorator(client: Client, update: Union[Message, CallbackQuery]):
        user_id = str(update.from_user.id if update.from_user else update.chat.id)

        # ✅ Step 1: Check allowed users
        if Telegram.ALLOWED_USER_IDS and user_id not in Telegram.ALLOWED_USER_IDS:
            if isinstance(update, CallbackQuery):
                return await update.answer(UserNotInAllowedList, show_alert=True)
            elif isinstance(update, Message):
                return await update.reply(
                    text=UserNotInAllowedList,
                    quote=True,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton('Deploy Own', url='')]]
                    )
                )
            return

        # ✅ Step 2: Force subscription check
        try:
            member = await client.get_chat_member(Telegram.FORCE_CHANNEL_ID, int(user_id))
            if member.status == enums.ChatMemberStatus.BANNED:
                if isinstance(update, CallbackQuery):
                    return await update.answer("🚫 You are banned from using this bot.", show_alert=True)
                elif isinstance(update, Message):
                    return await update.reply("🚫 You are banned from using this bot.")
                return
        except Exception:
            # Not a participant
            join_button = InlineKeyboardMarkup(
                [[InlineKeyboardButton("📢 Join Channel", url=Telegram.FORCE_CHANNEL_LINK)]]
            )
            if isinstance(update, CallbackQuery):
                await update.message.reply("⚠️ You must join our channel to use this bot.", reply_markup=join_button)
                return await update.answer()  # dismiss loading spinner
            elif isinstance(update, Message):
                return await update.reply("⚠️ You must join our channel to use this bot.", reply_markup=join_button)
            return

        # ✅ Step 3: Run original handler
        return await func(client, update)

    return decorator
