import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async

from bot.handlers import month_3
from bot.handlers.conversations_states import MONTH_2, MONTH_3
from bot.models import TelegramUser

logger = logging.getLogger(__name__)


async def block_0(chat_id, context):
    text = (
        "Привет! А вот и я😎 твой Таймпадрес! Уже 2 месяца, как ты с нами! Круто же?"
    )
    button_1 = "Даааа!"
    button_2 = "Конечно🤩"

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
    return MONTH_2[0]


async def block_1(chat_id, context):
    text = "Как настроение?"
    button_1 = "Все прекрасно!"
    button_2 = "Норм"
    button_3 = "Ну, такое"
    button_4 = "Совсем не очень"
    keyboard = ReplyKeyboardMarkup(
        [[button_1, button_2, button_3, button_4]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )
    return MONTH_2[1]


async def get_user_by_chat_id(chat_id):
    return await sync_to_async(TelegramUser.objects.get)(chat_id=chat_id)


async def save_user(user):
    await sync_to_async(user.save)()


async def block_2(chat_id, context):
    response = context.user_data.get('last_response')

    if response in ["Все прекрасно!", "Норм"]:  # Исправлено на проверку вхождения строки
        text = (
            "Я рад, что все хорошо. Столько всего интересного нас ждет! 🌺"
        )
        button = ReplyKeyboardMarkup(
            [[KeyboardButton("Конечно, так и будет!")]],  # Обернуто в список списков
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=button,
            parse_mode="Markdown",
        )
        return MONTH_2[2]
    else:
        text = (
            "Оу, сочувствую тебе! 😕 Если есть сложности или вопросы, ты всегда можешь обратиться за поддержкой "
            "к своему бадди, коллегам или в HR к Юлии. Надеюсь, скоро все наладится! 🤞"
        )
        button = ReplyKeyboardMarkup(
            [[KeyboardButton("Хорошо, спасибо за поддержку!")]],  # Обернуто в список списков
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=button,
            parse_mode="Markdown",
        )
        return MONTH_2[2]


async def block_3(chat_id, context):
    text = (
        "Я слышал, что скоро у тебя встреча с HR. [Ссылка](https://us02web.zoom.us/j/86826507585?pwd=qmo2josZPIVmEJzV8cnrd3FRKlIjl7.1) "
        "в твоем календаре! Приходи в назначенное время 🙂"
    )
    button = ReplyKeyboardMarkup(
        [[KeyboardButton("Спасибо! Буду вовремя!")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=button,
        disable_web_page_preview=True
    )
    return MONTH_2[3]


async def block_4(chat_id, context):
    text = (
        "Супер! Желаю тебе продуктивного дня! До встречи! 😘"
    )
    button = ReplyKeyboardRemove()
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=button,
        parse_mode="Markdown",
    )

