from aiogram import Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from tgbot.models.quick_commands import get_rankings, get_ranks


divisions =['Flyweight','Bantamweight', 'Featherweight',
           'Lightweight', 'Welterweight',  'Middleweight',
           'Light Heavyweight', 'Heavyweight', "Women's Strawweight",
           "Women's Flyweight", "Women's Bantamweight", "Women's Featherweight", ]

async def user_start(message: Message):
    await message.reply(message.chat.id)


async def rankings(msg:Message):
    # rankings = await get_rankings()
    # # await msg.answer("\n".join(rankings))
    keyboard = [[InlineKeyboardButton(division, callback_data="division:"+division), ] for division in divisions]
    await msg.answer(text="Выберите вес👇",reply_markup=InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=keyboard
    ))

async def division(call:CallbackQuery):
    _, division = call.data
    await call.message.edit_text()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(rankings, commands=["rankings"], state="*")
    dp.register_callback_query_handler(division,
                                       lambda callback_querry: callback_querry.data.startswith('division'),
                                       state="*")
