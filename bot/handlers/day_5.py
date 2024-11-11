from io import BytesIO

from asgiref.sync import sync_to_async
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
import logging

from bot.handlers.conversations_states import DAY_6
from bot.models import Video

logger = logging.getLogger(__name__)


async def block_0(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Привет! А вот и пролетели первые 5 рабочих дней!\n\n"
        "Мы все втроем - Таймпадрес, Таймика и Мастер Винтиков - очень рады были с тобой провести это время! \n\n"
    )
    button_1 = "ААА, какие вы классные!🎉"
    button_2 = "Спасибо, что помогали!"

    keyboard = ReplyKeyboardMarkup(
        [[button_1, button_2]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_photo(
        photo="https://disk.yandex.ru/i/OYKRdet92EJXLA",
        caption=text,
        reply_markup=keyboard,
    )
    return DAY_6[0]


async def block_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Пора тебе представить еще одного помощника, уже не виртуального 😉. \n\n"
        "Сегодня познакомим тебя с Бадди!"
    )
    button = "Кто это такой?🤔"

    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=text,
        reply_markup=keyboard,
    )
    return DAY_6[1]


async def block_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "**Бадди = друг, товарищ**🫱🏼‍🫲🏻 \n\n"
        "Который помогает новичкам адаптироваться в коллективе. \n\n"
        "*Название \"бадди\" происходит от английского слова \"buddy\", что переводится как \"друг\". *"
        "**С чем бадди помогает: **\n\n"
        "✌🏼Знакомство с коллективом и корпоративной культурой \n\n"
        "✌🏼Помощь в освоении рабочих процессов и инструментов \n\n"
        "✌🏼Ответы на вопросы и разъяснение неопределенностей \n\n"
        "✌🏼Создание комфортной и поддерживающей атмосферы \n\n"
        "**Что не должен делать бадди:** \n\n"
        "✋🏼Бадди не должен выполнять за новичка его обязанности или брать на себя его задачи \n\n"
        "✋🏼Не следует превращать поддержку в чрезмерное вмешательство или контроль \n\n"
        "✋🏼Бадди не должен навязывать свое мнение или методы работы, вместо этого он должен быть "
        "открытым для вопросов и проблем новичка"
    )
    button = ReplyKeyboardRemove()

    await update.message.reply_text(
        text=text,
        reply_markup=button,
    )

    text_2 = (
        "Ну что же, еще раз поздравляем тебя с первой рабочей неделей! \n\n"
        "Успехов тебе! И если нужна информация, заходи сюда и пользуйся Базой знаний \n\n"
        "Пока-пока!"
    )

    await update.message.reply_photo(
        photo="https://disk.yandex.ru/i/DbOiVozWm1rGMQ",
        caption=text_2,
        reply_markup=button
    )
    return DAY_6[2]

