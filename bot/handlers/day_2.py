import os
import re

from django.conf import settings
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async
import logging

from bot.handlers import day_3
from bot.handlers.conversations_states import DAY_3, DAY_4
from bot.models import TelegramUser, Code, SecondDay

logger = logging.getLogger(__name__)
SECRET_PASSWORD = os.getenv("SECRET_PASSWORD")


async def block_0(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"Привет! С тобой снова  Таймпадрес-бот и Таймика, мы уже соскучились! 😍\n\n"
        "А ты? 🤔"
    )
    button_1 = "Дааа! Я тоже!"
    button_2 = "Ну, почти😅 "
    keyboard = ReplyKeyboardMarkup(
        [[button_1, button_2]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    return DAY_3[0]


async def block_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_url = os.path.join(settings.MEDIA_ROOT, "tsticker.webp")
    text = (
        "Сегодня мы познакомим тебя с Timepad и расскажем про наши продукты!\n\n"
        "📌 Не забывай сохранять контакты коллег, они 100% тебе пригодятся!"
    )

    button = "Спасибо за совет!"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_sticker(
        sticker=open(photo_url, 'rb'),
    )
    await update.message.reply_text(
        text=text,
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

    photo_url = os.path.join(settings.MEDIA_ROOT, "5sticker.webp")
    text = (
        "А еще, у нас есть своя внутренняя валюта - **таймпадики**!\n\n"
        "Их можно потратить на билеты, на разные плюшки от нас и на мерч! Об этом ещё расскажем позже. "
        "А пока лови **5 приветственных таймпадиков!**\n\n"
        "*PS* посмотреть свой баланс таймпадиков ты можешь здесь по синей кнопке "
        "«Меню» (слева от строки ввода) и дальше «Кошелек»"
    )

    button = "🤑"
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
    await update.message.reply_sticker(
        sticker=open(photo_url, 'rb'),
    )
    return DAY_3[2]


async def block_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = await sync_to_async(
        lambda: SecondDay.objects.first().link_afisha_group
    )()
    text = (
        f"Это наша [Афиша]({link})) (делай ТЫК на слово \"афиша\")  - наша гордость и наша любовь!"
        "Ведь там располагаются все-все события от любимых организаторов! Здесь ты сможешь найти мероприятие, "
        "которое возможно станет твоим увлечением 🤩 \n\n"
        "Лови наше вдохновляющее видео!"
    )
    button = "Как интересно 😊"
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
    await update.message.reply_video(
        video="BAACAgIAAxkBAAIobWdPf7nyTnbAEuFBH9eaXCbtn_ZzAAKwcQACD5l4SmPU-vMLf0ycNgQ"
    )
    return DAY_3[3]


async def block_4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = await sync_to_async(
        lambda: SecondDay.objects.first().link_afisha_group
    )()
    text = (
        f"А теперь задание: *найди интересное для тебя мероприятие на нашей* [Афише]({link}) "
        "и *скинь его Юлии HR.*\n\n"
        "P.S. После выполнения задания ты получишь *пароль от Юлии и 5 таймпадиков от Таймики.*"
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
    """
    Prompt user to enter a password.
    """
    chat_id = update.effective_chat.id
    user = await get_user_by_chat_id(chat_id)
    user.timepad += 5
    await save_user(user)
    button = ReplyKeyboardRemove()
    photo_url = os.path.join(settings.MEDIA_ROOT, "5sticker.webp")
    await update.message.reply_sticker(
        sticker=open(photo_url, 'rb'),
    )
    text = "Отлично! Вводи полученный пароль и пойдём дальше!"
    await update.message.reply_text(text, reply_markup=button)

    context.user_data['awaiting_password'] = True
    return DAY_3[5]


async def verify_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Verify the entered password.
    """
    password = update.message.text
    return password == SECRET_PASSWORD


async def block_6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Process the password input and navigate further if correct.
    """
    if not context.user_data.get('awaiting_password', False):
        # If we are not awaiting a password, redirect to the starting block or raise an error
        await update.message.reply_text("Что-то пошло не так. Попробуй начать сначала.")
        return DAY_3[0]  # Возвращаем в начало, если состояние не найдено

    if await verify_password(update, context):
        # Password is correct
        context.user_data['awaiting_password'] = False
        text = (
            "Продолжим наше знакомство\\!\n\n"
            "Не так давно у нашей компании появился свой бренд\\-медиа \"Спасите мои выходные\"\\."
            "📙 Это наш журнал, который рассказывает о разных мероприятиях и хобби, "
            "которыми увлекаются герои журнала\\.\n\n"
            "*Здесь каждый может найти то, что будет по душе*: где самый классный каток, "
            "как и зачем играть в сквош и многое другое\\!"
        )

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
        return DAY_3[6]  # Указываем переход на следующий блок
    else:
        # Password is incorrect
        await update.message.reply_text("Пароль неверный 😓 попробуй ещё раз!")
        return DAY_3[5]  # Оставляем состояние прежним, чтобы повторить ввод


async def block_7(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    return DAY_3[7]


async def block_8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.message.text
    print(response)
    button = "О, да! Вдохновляет!"
    keyboard = ReplyKeyboardMarkup(
            [[button]],
            resize_keyboard=True,
            one_time_keyboard=True
    )
    links = await sync_to_async(
        lambda: SecondDay.objects.first()
    )()
    if response == "🖼":
        text = (
            f"🖼 Арт-бранчи каждые выходные — это твой язык любви: {links.art_branches_link}"
        )
    elif response == "🌳":
        text = (
            f"🌳 Уйти в лес и эстетично грустить...идеально: {links.forest_escapes_link}"
        )
    elif response == "✈️":
        text = (
            f"✈️ Путешествия вам к лицу: {links.travel_link}"
        )
    else:
        text = "what?:"

    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )
    return DAY_3[8]


async def block_9(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = await get_user_by_chat_id(chat_id)
    user.timepad += 5
    await save_user(user)

    photo_url = os.path.join(settings.MEDIA_ROOT, "5sticker.webp")
    text = "Лови **еще 5 таймпадиков!** Погнали дальше!"

    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
    )
    await update.message.reply_sticker(
        sticker=open(photo_url, 'rb'),
    )

    text_2 = (
        "*СММ* - это наша любовь! \n\n"
        "Ведь отдел так вкладывается в наши социальные сети.\n\n"
        "📣 Через соцсети мы не просто рассказываем о мероприятиях, а мы хотим как можно "
        "больше привлекать людей на события:\n\n"
        "🔹которые меняют жизнь! \n\n"
        "🔹где любой получит классные эмоции!\n\n"
        "🔹где каждый найдет себе то, что будет по душе!"
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
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

    return DAY_3[9]


async def block_10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    links = await sync_to_async(
        lambda: SecondDay.objects.first()
    )()
    text = (
        "А теперь небольшое задание для тебя: *подпишись на наши соц\\. сети* 😉\n\n"
        f"\\- tg\\-канал \"Спасите мои выходные\" {links.tg_channel_weekends} \n\n"
        f"\\- tg\\-канал для истинных петербуржцев \"Спасите мои парадные\" {links.tg_channel_paradnaya} \\_spb\n\n"
        f"\\- [ВК]({links.vk_link})\n\n"
        f"\\- [Инстаграм]({links.instagram_link}) \\(деятельность организации запрещена на территории РФ\\)\n\n"
        "После того, как подпишешься, *возвращайся и жми кнопку \"Готово\"*\\."
    )
    photo_url = os.path.join(settings.MEDIA_ROOT, "meditationsticker.webp")
    await update.message.reply_sticker(
        sticker=open(photo_url, 'rb'),
    )
    button = "Готово ✅"
    keyboard = ReplyKeyboardMarkup(
            [[button]],
            resize_keyboard=True,
            one_time_keyboard=True
    )

    await update.message.reply_text(
        text=text,
        parse_mode="MarkdownV2",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

    return DAY_3[10]


async def block_11(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = await get_user_by_chat_id(chat_id)
    user.timepad += 5
    await save_user(user)

    text = ("Лови *5 таймпадиков* и 100 плюсов к карме за поддержку отдела!")

    button = "Ура!"
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

    photo_url = os.path.join(settings.MEDIA_ROOT, "5sticker.webp")
    await update.message.reply_sticker(
        sticker=open(photo_url, 'rb'),
    )
    return DAY_3[11]


async def block_12(update: Update, context: ContextTypes.DEFAULT_TYPE):
    links = await sync_to_async(
        lambda: SecondDay.objects.first()
    )()
    text = (
        f"Еще у нас есть два подкаста, которые ты можешь послушать на досуге:\n\n"
        f"🎧\"[Спасите мои выходные]({links.podcast_save_my_weekend})\" с генеральным директором Варей Семенихиной "
        f"Подкаст о том, как найти любимое дело и превратить его в успешный бизнес! \n\n"
        f"🎧\"[Точно идем]({links.podcast_tochno_idem})\". Это подкаст от команды Timepad. В нем пробуем "
        f"разобраться в хобби занятых горожан, открыть для себя новые увлечения для новой реальности и понять, "
        f"как встроить их в полную работы жизнь! "
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
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

    return DAY_3[12]


async def block_13(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "*📊 А еще у нас есть Отдел рекламы!* \n\n"
        "Где создаются крутые инструменты, которые помогают растить нам выручку: \n\n"
        "*Мы продаем баннеры, места в соцсетях, а также верстаем классные дайджесты и рассылки!*"
    )
    button = "Ух! Вот это да!"
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
    links = await sync_to_async(
        lambda: SecondDay.objects.first()
    )()
    text = (
        f"А теперь сохраняй контакты коллег, которые помогут тебе лучше разобраться в наших продуктах и процессах:\n\n"
        f"📌 *Про Афишу* \\- Директор по развитию билетного бизнеса Даша Егорова {links.development_director_contact} \n\n"
        f"📌 *Про журнал \"Спасите мои выходные\"* \\- Руководитель отдела маркетинга Даша Гайдукова {links.marketing_director_contact}\n\n"
        f"📌 *Про СММ* \\- СММщица Маша Попова {links.smm_specialist_contact}\n\n"
        f"📌 *Про рекламу* \\- Руководитель отдела рекламы Азамат Орквасов {links.advertising_director_contact}"
    )
    keyboard = ReplyKeyboardMarkup(
            [["Уже в контактах 🫡 "]],
            resize_keyboard=True,
            one_time_keyboard=True
    )

    await update.message.reply_text(
        text=text,
        parse_mode="MarkdownV2",
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
        "Давай сделаем чек-ап того, что ты запомнил! \n\n"
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
        "И первый вопрос, *в какой системе мы ставим задачи?*"
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
        await update.message.reply_text(
            "Второй вопрос, *сколько у нас есть волшебных дней в году? 🪄*",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text("Эх, как же ты забыл нашу ЕВУ😓")
        await update.message.reply_text(
            "Второй вопрос, *сколько у нас есть волшебных дней в году? 🪄*",
            parse_mode="Markdown",
        )

    return DAY_3[17]


async def block_18(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.message.text

    if re.search(r"\b3\b", response, re.IGNORECASE):
        context.user_data['test_score'] += 1
        chat_id = update.effective_chat.id
        user = await get_user_by_chat_id(chat_id)
        user.timepad += 1
        await save_user(user)
        await update.message.reply_text("Верно! + 1 таймпадик")
        await update.message.reply_text(
            "Третий вопрос, *как назывется наш tg-канал с афишой?*",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text("Волшебные 3 дня! 🪄")
        await update.message.reply_text(
            "Третий вопрос, *как назывется наш tg-канал с афишой?*",
            parse_mode="Markdown",
        )

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
            "Четвертый вопрос, *где можно поделиться своими фотками с коллегами и неформально пообщаться?* "
            "(это какой-то из наших внутренних каналов, не нельзяграмм 😂)",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text("Эх, Спасите мои выходные! @TimepadRU")
        await update.message.reply_text(
            "Четвертый вопрос, **где можно поделиться своими фотками с коллегами и неформально пообщаться? "
            "**(это какой-то из наших внутренних каналов, не нельзяграмм 😂)",
            parse_mode="Markdown",
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
        cats_txt = (
            "Кстати, *каждую пятницу мы делимcя фотографиями своих четвероногих друзей!* Если у тебя есть питомец, "
            "то присоединяйся по пятницам к нашей милой традиции 🐾"
        )
        await update.message.reply_photo(
            photo="https://disk.yandex.ru/i/E5teV7j_hL-45Q",
            caption=cats_txt,
            parse_mode="Markdown",
        )
        await update.message.reply_text(
            "И финалный - пятый вопрос, вставь пропущенное слово: \n\n"
            "*Мы __ ________ увлечения, чтобы раскрывался потенциал и новые возможности*",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text("Правильный ответ - Offtop Timepad")
        cats_txt = (
            "Кстати, *каждую пятницу мы делимcя фотографиями своих четвероногих друзей!* Если у тебя есть питомец, "
            "то присоединяйся по пятницам к нашей милой традиции 🐾"
        )
        await update.message.reply_photo(
            photo="https://disk.yandex.ru/i/E5teV7j_hL-45Q",
            caption=cats_txt,
            parse_mode="Markdown",
        )
        await update.message.reply_text(
            "И финалный - пятый вопрос, вставь пропущенное слово: \n\n"
            "*Мы __ ________ увлечения, чтобы раскрывался потенциал и новые возможности*",
            parse_mode="Markdown",
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

    if re.search(r"\bподдерживаем\b", response, re.IGNORECASE):
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
            "Как же ты забыл нашу миссию 🥺 Мы поддерживаем!",
            reply_markup=keyboard
        )

    return DAY_3[21]


async def block_22(update: Update, context: ContextTypes.DEFAULT_TYPE):
    test_score = context.user_data.get('test_score', 0)
    text = (
        "Ты молодец! Лови еще заслуженную награду!"
    )
    button = "Ура! Как приятно!"
    keyboard = ReplyKeyboardMarkup(
            [[button]],
            resize_keyboard=True,
            one_time_keyboard=True
    )
    remove_button = ReplyKeyboardRemove()

    if test_score == 1:
        image_url = os.path.join(settings.MEDIA_ROOT, "1sticker.webp")
    elif test_score == 2:
        image_url = os.path.join(settings.MEDIA_ROOT, "2sticker.webp")
    elif test_score == 3:
        image_url = os.path.join(settings.MEDIA_ROOT, "3sticker.webp")
    elif test_score == 4:
        image_url = os.path.join(settings.MEDIA_ROOT, "4sticker.webp")
    elif test_score == 5:
        image_url = os.path.join(settings.MEDIA_ROOT, "5sticker.webp")
    else:
        button_2 = "Хорошо, сделаю💪"
        keyboard_2 = ReplyKeyboardMarkup(
            [[button_2]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await update.message.reply_text(
            "Это была хорошая попытка! Возможно, тебе стоит еще раз перечитать информацию, "
            "она тебе точно пригодится в работе!",
            reply_markup=keyboard_2
        )
        return DAY_3[22]

    await update.message.reply_text(
        text=text,
        reply_markup=keyboard
    )
    await update.message.reply_sticker(
        sticker=open(image_url, 'rb'),
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





