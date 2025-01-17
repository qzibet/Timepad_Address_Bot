import os

from asgiref.sync import sync_to_async
from django.conf import settings
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging
from bot.handlers.conversations_states import DAY_6, MONTH_1
from bot.models import TelegramUser

logger = logging.getLogger(__name__)


async def block_0(chat_id, context):
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
    photo_url = os.path.join(settings.MEDIA_ROOT, "5daysticker.webp")
    await context.bot.send_sticker(
        chat_id=chat_id,
        sticker=open(photo_url, 'rb'),
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard,
    )
    return DAY_6[0]


async def block_1(chat_id, context):
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
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard,
    )
    return DAY_6[1]


async def block_2(chat_id, context):
    text = (
        "*Бадди = друг, товарищ*🫱🏼‍🫲🏻 \n\n"
        "Который помогает новичкам адаптироваться в коллективе. \n\n"
        "_Название \"бадди\" происходит от английского слова \"buddy\", что переводится как \"друг\". _ \n\n"
        "*С чем бадди помогает: *\n\n"
        "✌🏼Знакомство с коллективом и корпоративной культурой \n\n"
        "✌🏼Помощь в освоении рабочих процессов и инструментов \n\n"
        "✌🏼Ответы на вопросы и разъяснение неопределенностей \n\n"
        "✌🏼Создание комфортной и поддерживающей атмосферы \n\n"
        "*Что не должен делать бадди:* \n\n"
        "✋🏼Бадди не должен выполнять за новичка его обязанности или брать на себя его задачи \n\n"
        "✋🏼Не следует превращать поддержку в чрезмерное вмешательство или контроль \n\n"
        "✋🏼Бадди не должен навязывать свое мнение или методы работы, вместо этого он должен быть "
        "открытым для вопросов и проблем новичка"
    )
    button = "Ого! Как классно!"

    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

    return DAY_6[2]


async def block_3(chat_id, context):
    link = await sync_to_async(
        lambda: TelegramUser.objects.first().buddy
    )()
    text = (
        f"А вот и контакт твоего Бадди. Можешь написать ему или подождать, пока он с тобой свяжется 🤗 \n\n"
        f"{link}"
    )
    button = "Спасибо за контакт!"

    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )
    return DAY_6[3]


async def block_4(chat_id, context):
    text_2 = (
        "Ну что же, еще раз поздравляем тебя с первой рабочей неделей! \n\n"
        "Успехов тебе! И если нужна информация, заходи сюда и пользуйся Базой знаний "
        "(найдешь ее в Меню - синяя кнопка слева от строки сообщений). \n\n"
        "Пока-пока!"
    )
    button = ReplyKeyboardRemove()
    photo_url = os.path.join(settings.MEDIA_ROOT, "heartsticker.webp")
    await context.bot.send_sticker(
        chat_id=chat_id,
        sticker=open(photo_url, 'rb'),
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=text_2,
        reply_markup=button,
        parse_mode="Markdown",
    )

