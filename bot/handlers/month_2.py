import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async

from bot.handlers import month_3
from bot.handlers.conversations_states import MONTH_2, MONTH_3
from bot.models import TelegramUser

logger = logging.getLogger(__name__)


async def block_0(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    await update.message.reply_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )
    return MONTH_2[0]


async def block_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.message.text
    print(response)
    chat_id = update.effective_chat.id
    user = await get_user_by_chat_id(chat_id)
    user.mood_second_month = response
    await save_user(user)
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
    await update.message.reply_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )
    return MONTH_2[1]


async def get_user_by_chat_id(chat_id):
    return await sync_to_async(TelegramUser.objects.get)(chat_id=chat_id)


async def save_user(user):
    await sync_to_async(user.save)()


async def block_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.message.text


    if response in ["Все прекрасно!", "Норм"]:  # Исправлено на проверку вхождения строки
        text = (
            "Я рад, что все хорошо. Столько всего интересного нас ждет! 🌺"
        )
        button = ReplyKeyboardMarkup(
            [[KeyboardButton("Конечно, так и будет!")]],  # Обернуто в список списков
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await update.message.reply_text(
            text=text,
            reply_markup=button,
            parse_mode="Markdown",
        )
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
        await update.message.reply_text(
            text=text,
            reply_markup=button,
            parse_mode="Markdown",
        )
        return MONTH_2[2]


async def block_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Я слышал, что скоро у тебя встреча с HR. [Ссылка](https://us02web.zoom.us/j/86826507585?pwd=qmo2josZPIVmEJzV8cnrd3FRKlIjl7.1) "
        "в твоем календаре! Приходи в назначенное время 🙂"
    )
    button = ReplyKeyboardMarkup(
        [[KeyboardButton("Спасибо! Буду вовремя!")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=button,
        disable_web_page_preview=True
    )
    return MONTH_2[3]


async def block_4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Супер! Желаю тебе продуктивного дня! До встречи! 😘"
    )
    button = ReplyKeyboardRemove()
    await update.message.reply_text(
        text=text,
        reply_markup=button,
        parse_mode="Markdown",
    )
    await month_3.block_0(update, context)
    return MONTH_3[0]
