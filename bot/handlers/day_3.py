import logging
import os

from django.conf import settings
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from bot.handlers import day_4
from bot.handlers.conversations_states import DAY_4, DAY_5

logger = logging.getLogger(__name__)


async def block_0(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ("Прием-прием! С тобой Таймика. Как твое настроение?")
    button_1 = "Супер!"
    button_2 = "Хорошее"
    button_3 = "Так себе"
    button_4 = "Плохое"
    keyboard = ReplyKeyboardMarkup(
        [[button_1, button_2, button_3, button_4]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        text=text,
        reply_markup=keyboard,
    )
    return DAY_4[0]


async def block_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Спасибо за искренность! \n\n"
        "Еще у нас принято хвалить коллег и давать обратную связь! 🤩 \n\n"
        "*Для обратной связи мы встречаемся на фейс-ту-фейс (или 1 to 1) с руководителем и HR.* \n\n"
        "А также проводим два больших опроса в год (в апреле и октябре), где изучаем \"Счастье сотрудников\" 💜"
    )
    photo_url = os.path.join(settings.MEDIA_ROOT, "likesticker.webp")
    await update.message.reply_sticker(
        sticker=open(photo_url, 'rb'),
    )
    button = "Как интересно!"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    return DAY_4[1]


# async def block_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = (
#         "здесь ИНФА про  сервис и регистрация!"
#     )
#     button = "Теперь буду использовать 👍"
#     keyboard = ReplyKeyboardMarkup(
#         [[button]],
#         resize_keyboard=True,
#         one_time_keyboard=True
#     )
#     await update.message.reply_text(
#         text=text,
#         reply_markup=keyboard,
#     )
#     return DAY_4[2]


async def block_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "А вот результат последнего исследования, где наш *eNPS* равен *78%*. \n\n"
        "*📝 eNPS - Employee Net Promoter Score или Индекс лояльности сотрудников.* \n\n"
        "Это самая популярная HR метрика. Она помогает оценить, насколько сотрудники "
        "довольны компанией и готовы рекомендовать ее другим. \n\n"
        "*eNPS выше 50 - считается отличным результатом и говорит о высоком уровне "
        "лояльности и удовлетворенности сотрудников *🤓"
    )
    button = "Ого! Вот это уcпех!🤩"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )
    return DAY_4[2]


async def block_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Конечно, мы будем очень рады, если и ты примешь участие и поможешь нам становиться лучше и лучше 🤗 "
    )
    button_1 = "Я только за!"
    button_2 = "Попробую :)"
    keyboard = ReplyKeyboardMarkup(
        [[button_1, button_2]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=text,
        reply_markup=keyboard,
    )
    return DAY_4[3]


async def block_4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Супер! На сегодня это все! 🤓\n\n"
        "С тобой было очень приятно и тепло! Увидимся завтра! 🧡"
    )

    button = ReplyKeyboardRemove()

    await update.message.reply_text(
        text=text,
        reply_markup=button
    )
    await day_4.block_0(update, context)
    return DAY_5[0]
