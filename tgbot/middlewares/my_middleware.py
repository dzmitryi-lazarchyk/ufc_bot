from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
import logging

from tgbot.models.custom_models import Users


class MyMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, *args):
        logging.info(f"Update BB={update}")

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, data:dict):
        await call.answer()
        logging.info(f"Callback_data={call.data}")


class ACLMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update:types.Update, data:dict):
        print(update)
        if update.my_chat_member:
            user_id = update.my_chat_member.from_user.id
            user_name = update.my_chat_member.from_user.full_name
            if update.my_chat_member.new_chat_member.status == "member":
                await Users.create(id=user_id, name=user_name, )
            elif update.my_chat_member.new_chat_member.status == "kicked":
                await Users.delete.where(Users.id == user_id).gino.status()
