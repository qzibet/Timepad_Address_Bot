import logging
import os

from asgiref.sync import sync_to_async
from django.conf import settings
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from bot.handlers import month_2
from bot.handlers.conversations_states import MONTH_1, MONTH_2
from bot.models import TelegramUser

logger = logging.getLogger(__name__)
MONTH_SECRET_PASSWORD = os.getenv("MONTH_SECRET_PASSWORD")


async def get_user_by_chat_id(chat_id):
    return await sync_to_async(TelegramUser.objects.get)(chat_id=chat_id)


async def save_user(user):
    await sync_to_async(user.save)()


async def block_0(chat_id, context):
    text = (
        "Привет!  Это  Таймпадрес, твой давний друг! Давно мы с тобой не общались. "
        "Хочу узнать, как у тебя дела 😉"
    )
    button_1 = "Привет-привет!"
    button_2 = "О, какая встреча!"

    keyboard = ReplyKeyboardMarkup(
        [[button_1, button_2]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )
    return MONTH_1[0]


async def block_1(chat_id, context):
    text = (
        "Заполни, пожалуйста, короткую [анкету](https://docs.google.com/forms/d/e/1FAIpQLScEQfKbumuqSd_3DeR1WDtQJUt5fYvUQEnGFJWgqXLmm9MLyQ/viewform) о том, как "
        "проходит твой адаптационный период.(ТЫК на слово \"анкета\") \n\n"
        "В конце опроса ты получишь *кодовое слово,* которое нужно будет написать мне, чтобы получить таймпадики! \n\n"
        "А я скоро напишу тебе снова, до связи! 🤓"
    )
    keyboard = ReplyKeyboardMarkup(
        [["Анкета готова!"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )
    return MONTH_1[1]


async def block_2(chat_id, context):
    text = "Супер! Напиши кодовое слово😉"
    button = ReplyKeyboardRemove()

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=button
    )

    context.user_data['awaiting_password'] = True
    return MONTH_1[2]


async def block_3(chat_id, context):
    if context.user_data.get('awaiting_password', False):
        password = context.user_data.get('last_response')
        print(password)

        if password == MONTH_SECRET_PASSWORD:
            photo_url = os.path.join(settings.MEDIA_ROOT, "10sticker.webp")
            text = "Лови *10 таймпадиков!* И успехов в адаптации! 🍀"
            await context.bot.send_sticker(
                sticker=open(photo_url, 'rb'),
                chat_id=chat_id
            )
            user = await get_user_by_chat_id(chat_id)
            user.timepad += 10
            await save_user(user)
            await context.bot.send_message(
                chat_id=chat_id, text=text, parse_mode="Markdown"
            )
        else:
            await context.bot.send_message(chat_id=chat_id, text="Пароль неверный 😓 попробуй ещё раз!")
