import os
import re

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async
import logging

from bot.handlers import day_3
from bot.handlers.conversations_states import DAY_3, DAY_4
from bot.models import TelegramUser, Code

logger = logging.getLogger(__name__)
SECRET_PASSWORD = os.getenv("SECRET_PASSWORD")


async def block_0(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"Привет! С тобой снова  Таймпадрес-бот и Таймика, мы уже соскучились! 😍\n\n"
        "А ты? 🤔"
    )
    photo_url = "https://disk.yandex.ru/i/_ghhRcXzCavlEw"
    button_1 = "Дааа! Я тоже!"
    button_2 = "Ну, почти😅 "
    keyboard = ReplyKeyboardMarkup(
        [[button_1, button_2]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_photo(
        photo=photo_url,
        caption=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    return DAY_3[0]


async def block_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_url = "https://disk.yandex.ru/i/g1x7ZAxQoITwSA"
    text = (
        "Сегодня мы познакомим тебя с Timepad и расскажем про наши продукты!\n\n"
        "💡Kind reminder:  Всех, кто встречается на твоем пути в этом боте сохраняй в контакты: "
        "**Фамилия Имя должность/отдел и название компании**\n\n"
        "Например, Юлия Маликова HR Timepad @malikovaj (делай ТЫК, чтобы ещё раз сохранить котакт Юли). "
        "Это поможет тебе быстро находить коллег в чатах."
    )

    button = "Спасибо за совет!"
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
    return DAY_3[1]


async def get_user_by_chat_id(chat_id):
    return await sync_to_async(TelegramUser.objects.get)(chat_id=chat_id)


async def save_user(user):
    await sync_to_async(user.save)()


async def block_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = await get_user_by_chat_id(chat_id)
    user.timepad = 5
    await save_user(user)

    photo_url = "https://disk.yandex.ru/i/g1x7ZAxQoITwSA"
    text = (
        "А еще, у нас есть своя внутренняя валюта - **таймпадики**!\n\n"
        "Их можно потратить на билеты, на разные плюшки от нас и на мерч! Об этом ещё расскажем позже. "
        "А пока лови **5 приветственных таймпадиков!**\n\n"
    )

    button = "🤑"
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
    return DAY_3[2]


async def block_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Это наша Афиша (делай ТЫК на слово [афиша](https://afisha.timepad.ru))"
        "Про нее расскажет Директор по развитию билетного бизнеса Даша Егорова @darialvistner"
    )
    button = "Приятно познакомиться 😊"
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
    return DAY_3[3]


async def block_4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "А теперь задание: **найди интересное для тебя мероприятие на нашей [Афише] (https://afisha.timepad.ru)** "
        "**и скинь его Юлии HR.**\n\n"
        "P.S. После выполнения задания ты получишь **пароль от Юлии и 5 таймпадиков от Таймики.**"
    )
    button = "Пароль у меня, где мои таймпадики?"
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
    return DAY_3[4]


async def block_5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Отлично! Вводи полученный пароль и пойдём дальше!"
    await update.message.reply_text(text)

    context.user_data['awaiting_password'] = True
    return DAY_3[5]


async def block_6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_password', False):
        password = update.message.text

        if password == SECRET_PASSWORD:
            context.user_data['awaiting_password'] = False
            return DAY_3[6]
        else:
            await update.message.reply_text("Пароль неверный 😓 попробуй ещё раз!")
            await block_5(update, context)


async def block_7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ("Продолжим наше знакомство\\!\n\n"
            "У нас есть журнал \"Спасите мои выходные\"\\. Про него расскажет "
            "\\(руководитель отдела маркетинга Даша Гайдукова @dasha\\_gaydukova\\)\n\n"
            "P\\.S\\. Ты записываешь новые контакты\\?\\)")

    button = "Здорово! Что дальше?"
    keyboard = ReplyKeyboardMarkup(
            [[button]],
            resize_keyboard=True,
            one_time_keyboard=True
    )

    await update.message.reply_text(
        text=text,
        parse_mode="MarkdownV2",
        reply_markup=keyboard
    )
    return DAY_3[7]


async def block_8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ("Выбери эмоджи, которое лучше всего описывает твои идеальные выходные:")
    button_1 = "🖼"
    button_2 = "🌳"
    button_3 = "✈️"

    keyboard = ReplyKeyboardMarkup(
            [[button_1, button_2, button_3]],
            resize_keyboard=True,
            one_time_keyboard=True
    )

    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    return DAY_3[8]


async def block_9(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.message.text
    print(response)
    button = "О, да! Вдохновляет!"
    keyboard = ReplyKeyboardMarkup(
            [[button]],
            resize_keyboard=True,
            one_time_keyboard=True
    )

    if response == "🖼":
        text = (
            "🖼 Арт-бранчи каждые выходные — это твой язык любви: https://journal.timepad.ru/selections/branchi-moskvy"
        )
    elif response == "🌳":
        text = (
            "🌳 Уйти в лес и эстетично грустить...идеально: https://journal.timepad.ru/selections/ekotropy-podmoskovya"
        )
    elif response == "✈️":
        text = (
            "✈️ Путешествия вам к лицу: https://journal.timepad.ru/tag/ekskursii-i-puteshestviya"
        )
    else:
        text = "what?:"

    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    return DAY_3[9]


async def block_10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = await get_user_by_chat_id(chat_id)
    user.timepad += 5
    await save_user(user)

    photo_url = "https://disk.yandex.ru/i/g1x7ZAxQoITwSA"
    text = "Лови **еще 5 таймпадиков!** Погнали дальше!"

    await update.message.reply_photo(
        photo=photo_url,
        caption=text,
        parse_mode="Markdown",
    )

    text_2 = (
        "У нас ещё есть tg-канал \"Спасите мои выходные\" @TimepadRU "
        "(делай ТЫК на [Спасите мои выходные](https://t.me/TimepadRU), чтобы перейти в канал ). "
        "Про него подробнее расскажет наша СММщица Маша Попова @marypopossa"
    )
    button = "Круто!"
    keyboard = ReplyKeyboardMarkup(
            [[button]],
            resize_keyboard=True,
            one_time_keyboard=True
    )

    await update.message.reply_text(
        text=text_2,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

    return DAY_3[10]


async def block_11(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "А теперь небошьшое задание для тебя 😉: подпишись на tg-канал "
        "\"Спасите мои выходные\". @TimepadRU"
    )
    button = "Готово ✅"
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

    return DAY_3[11]


async def block_12(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = await get_user_by_chat_id(chat_id)
    user.timepad += 5
    await save_user(user)

    photo_url = "https://disk.yandex.ru/i/e9OYMWi8p8hIXg"
    text = ("Лови **5 таймпадиков** и 100 плюсов к карме за поддержку отдела!")

    button = "Ура!"
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

    return DAY_3[12]


async def block_13(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Еще у нас есть два подкаста, которые ты можешь послушать на досуге:\n\n"
        "🎧\"Спасите мои выходные\" с генеральным директором [Варей Семенихиной](https://savemyweekend.mave.digital)\n\n"
        "🎧\"[Точно идем](https://tochnoidem.mave.digital)\""
    )
    button = "О, как классно! 🎧"
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

    return DAY_3[13]


async def block_14(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Теперь бежим знакомиться с коллегами из отдела рекламы! \n\n"
        "У нас есть множество рекламных инструментов, про которые нам расскажет руководитель "
        "отдела рекламы - Азамат Орквасов @azamorkvasov ✌🏼"
    )
    button = "Ну ничего себе!"
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

    return DAY_3[14]


async def block_15(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Согласись, у нас много всего интересного? 🎪"
    )
    button = "Дааааа!"
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

    return DAY_3[15]


async def block_16(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['test_score'] = 0
    text = (
        "Давай сделаем чек-ап того, что запомнил! \n\n"
        "Пройди небольшой тест 🤓 \n\n"
        "P.S. За каждый верный ответ тебе начислят таймпадики!"
    )
    button = ReplyKeyboardRemove()

    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=button
    )

    text_2 = (
        "Тогда погнали! \n\n"
        "И первый вопрос, **в какой системе мы ставим задачи?**"
    )
    await update.message.reply_text(
        text=text_2,
        parse_mode="Markdown",
        reply_markup=button
    )

    return DAY_3[16]


async def block_17(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.message.text

    if re.search(r"\bева\b", response, re.IGNORECASE):
        context.user_data['test_score'] += 1
        chat_id = update.effective_chat.id
        user = await get_user_by_chat_id(chat_id)
        user.timepad += 1
        await save_user(user)
        await update.message.reply_text("Верно! + 1 таймпадик")
        await update.message.reply_text("Второй вопрос, **в какие дни у нас приходит зарплата?**")
    else:
        await update.message.reply_text("Эх, как же ты забыл нашу ЕВУ😓")
        await update.message.reply_text("Второй вопрос, **в какие дни у нас приходит зарплата?**")

    return DAY_3[17]


async def block_18(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.message.text

    if re.search(r"\b5\b" and r"\b5\b", response, re.IGNORECASE):
        context.user_data['test_score'] += 1
        chat_id = update.effective_chat.id
        user = await get_user_by_chat_id(chat_id)
        user.timepad += 1
        await save_user(user)
        await update.message.reply_text("Верно! + 1 таймпадик")
        await update.message.reply_text("Третий вопрос, **как назывется наш tg-канал с афишой?**")
    else:
        await update.message.reply_text("Записывай в календарь - 5 и 20 🗓️")
        await update.message.reply_text("Третий вопрос, **как назывется наш tg-канал с афишой?**")

    return DAY_3[18]


async def block_19(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.message.text

    if re.search(r"\bСпасите мои выходные\b", response, re.IGNORECASE):
        context.user_data['test_score'] += 1
        chat_id = update.effective_chat.id
        user = await get_user_by_chat_id(chat_id)
        user.timepad += 1
        await save_user(user)
        await update.message.reply_text("Верно! + 1 таймпадик")
        await update.message.reply_text(
            "Четвертый вопрос, **где можно педелиться своими фотками с коллегами и неформально пообщаться? "
            "**(это какой-то из наших внутренних каналов, не нельзяграмм 😂)"
        )
    else:
        await update.message.reply_text("Эх, Спасите мои выходные! @TimepadRU")
        await update.message.reply_text(
            "Четвертый вопрос, **где можно педелиться своими фотками с коллегами и неформально пообщаться? "
            "**(это какой-то из наших внутренних каналов, не нельзяграмм 😂)"
        )
    return DAY_3[19]


async def block_20(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.message.text

    if re.search(r"\bOfftop Timepad\b", response, re.IGNORECASE):
        context.user_data['test_score'] += 1
        chat_id = update.effective_chat.id
        user = await get_user_by_chat_id(chat_id)
        user.timepad += 1
        await save_user(user)
        await update.message.reply_text("Верно! + 1 таймпадик")
        await update.message.reply_text(
            "И финалный - пятый вопрос, **как зовут помощницу Таймпадрес бота?**"
        )
    else:
        await update.message.reply_text("Правильно - Offtop Timepad, скорее кидай туда свою фотку 📸")
        await update.message.reply_text(
            "И финалный - пятый вопрос, **как зовут помощницу Таймпадрес бота?**"
        )
    return DAY_3[20]


async def block_21(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.message.text
    button = "Тест пройден 📋"
    keyboard = ReplyKeyboardMarkup(
            [[button]],
            resize_keyboard=True,
            one_time_keyboard=True
    )

    if re.search(r"\bТаймика\b", response, re.IGNORECASE):
        context.user_data['test_score'] += 1
        chat_id = update.effective_chat.id
        user = await get_user_by_chat_id(chat_id)
        user.timepad += 1
        await save_user(user)
        await update.message.reply_text(
            "Верно! + 1 таймпадик",
            reply_markup=keyboard
        )
    else:
        await update.message.reply_text(
            "Как же ты забыл имя нашей дорогой Таймики 🥺",
            reply_markup=keyboard
        )

    return DAY_3[21]


async def block_22(update: Update, context: ContextTypes.DEFAULT_TYPE):
    test_score = context.user_data.get('test_score', 0)
    text = (
        "Ты молодец! Лови еще заслуженную награду!"
    )
    button = "Хорошо, сделаю💪"
    keyboard = ReplyKeyboardMarkup(
            [[button]],
            resize_keyboard=True,
            one_time_keyboard=True
    )
    remove_button = ReplyKeyboardRemove()

    if test_score == 1:
        image_url = "https://disk.yandex.ru/i/sLgJsP-BUHEBBA"
    elif test_score == 2:
        image_url = "https://disk.yandex.ru/i/iYuvVWAoxkaYCQ"
    elif test_score == 3:
        image_url = "https://disk.yandex.ru/i/QZ_B6-N5P-aWiw"
    elif test_score == 4:
        image_url = "https://disk.yandex.ru/i/QonQ3L8CPexhWA"
    elif test_score >= 5:
        image_url = "https://disk.yandex.ru/i/nocYHnbfjMJY3Q"
    else:
        await update.message.reply_text(
            "Это была хорошая попытка! Возможно, тебе стоит еще раз перечитать информацию, "
            "она тебе точно пригодится в работе!",
            reply_markup=keyboard
        )
        return DAY_3[22]

    await update.message.reply_photo(
        photo=image_url,
        caption=text,
        reply_markup=keyboard
    )
    return DAY_3[22]


async def block_23(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "На сегодня это все! Встретимся завтра и продолжим! Чао 🖐"
    )
    button = ReplyKeyboardRemove()

    await update.message.reply_text(
        text=text,
        reply_markup=button
    )
    await day_3.block_0(update, context)
    return DAY_4[0]





