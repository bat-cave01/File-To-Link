from hydrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from hydrogram import filters
from bot import TelegramBot
from bot.modules.decorators import verify_user
from bot.modules.static import *
from bot.modules.telegram import get_message

# ✅ Only catches rm_* queries
@TelegramBot.on_callback_query(filters.regex("^rm_"))
@verify_user
async def manage_callback(bot, q: CallbackQuery):
    sq = q.data.split('_')

    if len(sq) != 3:
        return await q.answer(InvalidQueryText, show_alert=True)

    message = await get_message(int(sq[1]))

    if not message:
        return await q.answer(MessageNotExist, show_alert=True)
    
    sc = message.caption.split('/')

    if q.from_user.id != int(sc[1]) or sq[2] != sc[0]:
        return await q.answer(InvalidQueryText, show_alert=True)
    
    await message.delete()
    await q.answer(LinkRevokedText, show_alert=True)


# ✅ Help button
@TelegramBot.on_callback_query(filters.regex("^show_help$"))
async def help_callback(_, q: CallbackQuery):
    await q.message.edit_text(
        text=HelpText,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]]
        )
    )

# ✅ About button
@TelegramBot.on_callback_query(filters.regex("^show_about$"))
async def about_callback(_, q: CallbackQuery):
    await q.message.edit_text(
        text=AboutText,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]]
        )
    )

# ✅ Back button
@TelegramBot.on_callback_query(filters.regex("^back_to_start$"))
async def back_callback(_, q: CallbackQuery):
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("ℹ️ Help", callback_data="show_help"),
                InlineKeyboardButton("📌 About", callback_data="show_about")
            ]
        ]
    )
    await q.message.edit_text(
        text=WelcomeText % {'first_name': q.from_user.first_name},
        reply_markup=buttons
    )


# ✅ Handler for the close button
@TelegramBot.on_callback_query(filters.regex("^close_msg$"))
async def close_button(_, q):
    try:
        await q.message.delete()
    except:
        await q.answer("❌ Can't delete this message.", show_alert=True)