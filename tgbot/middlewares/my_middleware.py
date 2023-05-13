from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
import logging

class MyMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, *args):
        logging.info(f"Update BB={update}")

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, data:dict):
        await call.answer()
        logging.info(f"Callback_data={call.data}")