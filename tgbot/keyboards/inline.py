from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

divisions = ['Flyweight', 'Bantamweight', 'Featherweight',
             'Lightweight', 'Welterweight', 'Middleweight',
             'Light Heavyweight', 'Heavyweight', "Women's Strawweight",
             "Women's Flyweight", "Women's Bantamweight", "Women's Featherweight", ]

divisions_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(division, callback_data="division:" + division), ] for division in divisions
    ]
)

fighter_callback = CallbackData("fighter", "division", "to_fighter")
def fighter_keyboard_constractor(division, current_rank, next_rank, prev_rank):
    keyboard = InlineKeyboardMarkup(
        row_width=3,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Показать списком",
                    callback_data=fighter_callback.new(division=division,
                                                       to_fighter="list")

                )],
                [
                    InlineKeyboardButton(
                        text="⬅️",
                        callback_data=fighter_callback.new(division=division,
                                                           to_fighter=prev_rank),
                    ),
                    InlineKeyboardButton(
                        text=f"{current_rank}",
                        callback_data=fighter_callback.new(division=division,
                                                           to_fighter="all_ranks"),
                    ),
                    InlineKeyboardButton(
                        text="➡️",
                        callback_data=fighter_callback.new(division=division,
                                                           to_fighter=next_rank),
                    ),
                ]
        ]
    )
    return keyboard

