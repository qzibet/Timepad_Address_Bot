import logging

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
        "Для обратной связи мы встречаемся пару раз в год, попозже узнаешь об этом подробнее ☺"
    )
    photo_url = "https://disk.yandex.ru/i/On_TE_d_hpjfYA"
    button = "Как интересно!"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_photo(
        photo=photo_url,
        caption=text,
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
        "Это еще не все хорошие новости! \n\n"
        "Два раза в год мы проводим исследование и **измеряем счастье сотрдуников**! \n\n"
        "Вот результаты актуального исследования: **79% eNPS**. \n\n"
    )
    button = "Ого! Вот это упех!🤩"
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
        "Конечно, мы будем очень рады, если и ты будешь принимать участие и "
        "помогать становится нам лучше 🤗"
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
        "Супер! На сегодня это все! Пойду делать еще дела 🤓 \n\n"
        "С тобой было очень приятно и тепло! Увидимся завтра! 🧡"
    )

    button = ReplyKeyboardRemove()

    await update.message.reply_text(
        text=text,
        reply_markup=button
    )
    await day_4.block_0(update, context)
    return DAY_5[0]
