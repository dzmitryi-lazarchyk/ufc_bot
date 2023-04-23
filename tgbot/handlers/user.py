
import aiogram.utils.exceptions
from aiogram import Dispatcher, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMedia

from tgbot.keyboards.inline import divisions_keyboard, fighter_keyboard_constractor, fighter_callback
from tgbot.models.custom_models import Fighters


async def user_start(message: Message):
    await message.reply(message.chat.id)


async def rankings(msg: Message):
    # rankings = await get_rankings()
    # # await msg.answer("\n".join(rankings))
    await msg.answer(text="Выберите вес👇", reply_markup=divisions_keyboard)


async def divisions(call: CallbackQuery):
    _, division = call.data.split(":")
    if division == "back":
        await call.message.edit_text("Выберите вес👇")
        await call.message.edit_reply_markup(divisions_keyboard)
    else:
        division_fighters = await Fighters.get_division_fighters(division=division)
        text = f"<i>Вес:{division}\n\n</i>" \
               f"<b>{division_fighters[0].rank}. {division_fighters[0].name}</b>\n" + \
               "\n".join([f"{fighter.rank}. {fighter.name}" for fighter in division_fighters[1:]])
        keyboard = InlineKeyboardMarkup(
            row_width=2,
            inline_keyboard=[
                [InlineKeyboardButton(text="Страница бойца", callback_data=f"fighter:{division}:by_one")],
                [InlineKeyboardButton(text="⬅️Сменить вес", callback_data=f"division:back")],
            ]
        )
        try:
            await call.message.edit_text(text=text)
            await call.message.edit_reply_markup(reply_markup=keyboard)
        except aiogram.utils.exceptions.BadRequest:
            await call.message.answer(text=text,
                                      reply_markup=keyboard)


async def fighter(call: CallbackQuery):
    bot = Bot.get_current()
    msg = call.message
    chat_id = call.message.chat.id

    _, division, rank = call.data.split(":")

    if rank == "list":
        await call.message.delete()
        call.data = f"division:{division}"
        await divisions(call)
        return
    elif rank == "by_one":
        await call.message.delete()
        rank = "Champion"
        fighter: Fighters = await Fighters.get_division_fighter(division=division, rank=rank)
        next_rank, prev_rank = await Fighters.get_next_previous(fighter.division, fighter.rank)
        keyboard = fighter_keyboard_constractor(division, rank, next_rank, prev_rank)

        await bot.send_photo(chat_id=chat_id,
                             photo=fighter.image,
                             caption=fighter,
                             reply_markup=keyboard)
    elif rank == "all_ranks":
        ranks = await Fighters.get_all_ranks(division=division)
        keyboard = InlineKeyboardMarkup(row_width=4)
        keyboard.row(
            InlineKeyboardButton(
                text=ranks[0],
                callback_data=fighter_callback.new(division=division,
                                                   to_fighter=ranks[0])
            )
        )
        if len(ranks) > 1:
            ranks = ranks[1:]
            for _ in range(0, len(ranks), 4):
                if len(ranks) > 3:
                    buttons = [InlineKeyboardButton(
                        text=rank,
                        callback_data=fighter_callback.new(division=division,
                                                           to_fighter=rank)
                    ) for rank in ranks[:4]]
                    ranks = ranks[4:]
                    keyboard.row(*buttons)
                else:
                    buttons = [InlineKeyboardButton(
                        text=rank,
                        callback_data=fighter_callback.new(division=division,
                                                           to_fighter=rank)
                    ) for rank in ranks]
                    keyboard.row(*buttons)
                    break
        await msg.edit_reply_markup(reply_markup=keyboard)
    else:
        fighter: Fighters = await Fighters.get_division_fighter(division=division, rank=rank)
        next_rank, prev_rank = await Fighters.get_next_previous(fighter.division, fighter.rank)
        keyboard = fighter_keyboard_constractor(division, rank, next_rank, prev_rank)
        media = InputMedia(type='photo', media=fighter.image)

        await msg.edit_media(media=media)

        await msg.edit_caption(caption=fighter,
                               reply_markup=keyboard)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(rankings, commands=["rankings"], state="*")
    dp.register_callback_query_handler(divisions,
                                       lambda callback_querry: callback_querry.data.startswith('division'),
                                       state="*")
    dp.register_callback_query_handler(fighter,
                                       lambda callback_querry: callback_querry.data.startswith('fighter'),
                                       state="*")
