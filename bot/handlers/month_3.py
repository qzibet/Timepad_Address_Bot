import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async

from bot.handlers.conversations_states import MONTH_3
from bot.models import TelegramUser

logger = logging.getLogger(__name__)


async def block_0(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "И снова рад тебя приветствовать! 😊  Вот и подошел к концу твой испытательный срок! 🙌"
    )
    button_1 = "Наконец-то!!🤩"
    button_2 = "Ого!Уже? 😅"
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
    return MONTH_3[0]


async def block_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Да! Поздравляю тебя! 🎉 \n\n"
        "Скоро у тебя будет *встреча с HR и твоим руководителем,* на которой вы обсудите, "
        "как прошли твои первые три месяца работы. \n\n"
        "Жди от них приглашение🤓"
    )
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("Понятно, жду 😎")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await update.message.reply_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )
    return MONTH_3[1]


async def block_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "А пока ты ждешь встречу, заполни, пожалуйста анкету "
        "[👉🏼обратной связи👈🏼](https://docs.google.com/forms/d/e/1FAIpQLSf1X3GgiJ2x8-x-XXVearUhGp5tTYkX-_bI7hQX7OBCOzh4Qg/viewform) "
        "и поделись своими впечатлениями о работе у нас! \n\n"
        "Как заполнишь, жми кнопку \"Сделано ✅\""
    )
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("Сделано ✅")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await update.message.reply_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )
    return MONTH_3[2]


async def block_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Супер! \n\n"
        "Ты всегда можешь возвращаться ко мне и смотреть информацию в *Базе знаний* 📖 \n\n"
        "Я желаю тебе интересных проектов и классных тусовок в Timepad! 🥰 Пока-пока!"
    )
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("И это все? 🥺")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await update.message.reply_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )
    return MONTH_3[3]


async def block_4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Да! *Мы поздравляем тебя с успешным завершением испытательного срока и желаем крутых карьерных побед!*"
        "А еще хотим напомнить, что ты можешь рекомендовать нас своим друзьям и наоборот, чтобы они тоже стали "
        "часть нашей крутой команды *#TimepadTeam* 🥰"
    )
    button = ReplyKeyboardRemove()
    await update.message.reply_photo(
        photo="https://disk.yandex.ru/i/X2npIWZ9NConJQ",
        caption=text,
        reply_markup=button,
        parse_mode="Markdown",
    )
