import os
import re

from django.conf import settings
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.constants import ChatAction
from asgiref.sync import sync_to_async
import logging

from telegram.helpers import escape_markdown

from bot.handlers import day_3
from bot.handlers.conversations_states import DAY_3, DAY_4
from bot.models import TelegramUser, Code, SecondDay

logger = logging.getLogger(__name__)
SECRET_PASSWORD = os.getenv("SECRET_PASSWORD")


async def block_0(chat_id, context):
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

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    return DAY_3[0]


async def block_1(chat_id, context):
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
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

    await context.bot.send_sticker(
        sticker=open(photo_url, 'rb'),
        chat_id=chat_id
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

    return DAY_3[1]


async def get_user_by_chat_id(chat_id):
    return await sync_to_async(TelegramUser.objects.get)(chat_id=chat_id)


async def save_user(user):
    await sync_to_async(user.save)()


async def block_2(chat_id, context):
    user = await get_user_by_chat_id(chat_id)
    user.timepad = 5
    await save_user(user)

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
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

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    await context.bot.send_sticker(
        sticker=open(photo_url, 'rb'),
    )
    return DAY_3[2]


async def block_3(chat_id, context):
    link = await sync_to_async(
        lambda: SecondDay.objects.first().link_afisha_group
    )()

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
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

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )
    await context.bot.send_video(
        video="BAACAgIAAxkBAAMoZ6IOX6caP-QsyuUDQET8E1hRtg0AArBxAAIPmXhK-W8F7S4PUN02BA",
        chat_id=chat_id,
    )
    return DAY_3[3]


async def block_4(chat_id, context):
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

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )
    return DAY_3[4]


async def block_5(chat_id, context):
    user = await get_user_by_chat_id(chat_id)
    user.timepad += 5
    await save_user(user)
    button = ReplyKeyboardRemove()
    photo_url = os.path.join(settings.MEDIA_ROOT, "5sticker.webp")
    await context.bot.send_sticker(
        chat_id=chat_id,
        sticker=open(photo_url, 'rb'),
    )
    text = "Отлично! Вводи полученный пароль и пойдём дальше!"
    await context.bot.send_message(
        chat_id=chat_id, text=text, reply_markup=button
    )

    context.user_data['awaiting_password'] = True
    return DAY_3[5]


async def verify_password(context):
    """
    Verify the entered password.
    """
    password = context.user_data.get('last_response')
    return password == SECRET_PASSWORD


async def block_6(chat_id, context):
    """
    Process the password input and navigate further if correct.
    """
    if not context.user_data.get('awaiting_password', False):
        # Если не ожидается пароль, перенаправляем в начало
        await context.bot.send_message(
            chat_id=chat_id, text="Что-то пошло не так. Попробуй начать сначала."
        )
        return DAY_3[0]  # Возвращаем в начало, если состояние не найдено

    # Предполагаем, что последнее сообщение пользователя сохранено в user_data

    if await verify_password(context):
        # Если пароль верный
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

        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode="MarkdownV2",
            reply_markup=keyboard
        )
        return DAY_3[6]  # Указываем переход на следующий блок
    else:
        # Если пароль неверный
        context.user_data['awaiting_password'] = True  # Сохраняем ожидание
        await context.bot.send_message(chat_id=chat_id, text="Пароль неверный 😓 попробуй ещё раз!")
        return DAY_3[5]


async def block_7(chat_id, context):
    text = ("Выбери эмоджи, которое лучше всего описывает твои идеальные выходные:")
    button_1 = "🖼"
    button_2 = "🌳"
    button_3 = "✈️"

    keyboard = ReplyKeyboardMarkup(
            [[button_1, button_2, button_3]],
            resize_keyboard=True,
            one_time_keyboard=True
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    return DAY_3[7]


async def block_8(chat_id, context):
    user = await sync_to_async(lambda: TelegramUser.objects.get(chat_id=chat_id))()
    response = user.emodji
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

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )
    return DAY_3[8]


async def block_9(chat_id, context):
    user = await get_user_by_chat_id(chat_id)
    user.timepad += 5
    await save_user(user)

    photo_url = os.path.join(settings.MEDIA_ROOT, "5sticker.webp")
    text = "Лови **еще 5 таймпадиков!** Погнали дальше!"

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
    )
    await context.bot.send_sticker(
        chat_id=chat_id,
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

    await context.bot.send_message(
        chat_id=chat_id,
        text=text_2,
        parse_mode="Markdown",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

    return DAY_3[9]


async def block_10(chat_id, context):
    # Получаем данные из базы данных асинхронно
    links = await sync_to_async(lambda: SecondDay.objects.first())()

    # Экранируем динамические данные для MarkdownV2
    tg_channel_weekends = escape_markdown(links.tg_channel_weekends, version=2)
    tg_channel_paradnaya = escape_markdown(links.tg_channel_paradnaya, version=2)
    vk_link = escape_markdown(links.vk_link, version=2)
    instagram_link = escape_markdown(links.instagram_link, version=2)

    # Формируем текст сообщения с экранированием специальных символов
    text = (
        "А теперь небольшое задание для тебя: *подпишись на наши соц.сети* 😉\n\n"
        f"- tg-канал \"Спасите мои выходные\" {tg_channel_weekends}\n\n"
        f"- tg-канал для истинных петербуржцев \"Спасите мои парадные\" {tg_channel_paradnaya}\n\n"
        f"- [ВК]({vk_link}).\n\n"
        f"- [Инстаграм]({instagram_link}) (деятельность организации запрещена на территории РФ)\n\n"
        "После того, как подпишешься, *возвращайся и жми кнопку \"Готово\"*"
    )

    # Отправляем стикер
    photo_url = os.path.join(settings.MEDIA_ROOT, "meditationsticker.webp")
    with open(photo_url, 'rb') as sticker:
        await context.bot.send_sticker(
            chat_id=chat_id,
            sticker=sticker,
        )

    # Создаём клавиатуру с кнопкой
    button = "Готово ✅"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    # Логирование текста сообщения для отладки (необязательно)
    print("Сообщение для отправки:")
    print(text)

    # Отправляем сообщение
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

    return DAY_3[10]


async def block_11(chat_id, context):
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

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

    photo_url = os.path.join(settings.MEDIA_ROOT, "5sticker.webp")
    await context.bot.send_sticker(
        sticker=open(photo_url, 'rb'),
        chat_id=chat_id
    )
    return DAY_3[11]


async def block_12(chat_id, context):
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

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

    return DAY_3[12]


async def block_13(chat_id, context):
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

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

    return DAY_3[13]


async def block_14(chat_id, context):
    links = await sync_to_async(lambda: SecondDay.objects.first())()

    text = (
        "А теперь сохраняй контакты коллег, которые помогут тебе лучше разобраться в наших продуктах и процессах:\n\n"
        "📌 <b>Про Афишу</b> - Директор по развитию билетного бизнеса Даша Егорова "
        f"{links.development_director_contact}\n\n"
        "📌 <b>Про журнал \"Спасите мои выходные\"</b> - Руководитель отдела маркетинга Даша Гайдукова "
        f"{links.marketing_director_contact}\n\n"
        "📌 <b>Про СММ</b> - СММщица Маша Попова "
        f"{links.smm_specialist_contact}\n\n"
        "📌 <b>Про рекламу</b> - Руководитель отдела рекламы Азамат Орквасов "
        f"{links.advertising_director_contact}"
    )

    keyboard = ReplyKeyboardMarkup(
        [["Уже в контактах 🫡 "]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard
    )
    return DAY_3[14]


async def block_15(chat_id, context):
    text = (
        "Согласись, у нас много всего интересного? 🎪"
    )
    button = "Дааааа!"
    keyboard = ReplyKeyboardMarkup(
            [[button]],
            resize_keyboard=True,
            one_time_keyboard=True
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

    return DAY_3[15]


async def block_16(chat_id, context):
    context.user_data['test_score'] = 0
    text = (
        "Давай сделаем чек-ап того, что ты запомнил! \n\n"
        "Пройди небольшой тест 🤓 \n\n"
        "P.S. За каждый верный ответ тебе начислят таймпадики!"
    )
    button = ReplyKeyboardRemove()

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=button
    )

    text_2 = (
        "Тогда погнали! \n\n"
        "И первый вопрос, *в какой системе мы ставим задачи?*"
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=text_2,
        parse_mode="Markdown",
        reply_markup=button
    )

    return DAY_3[16]


async def block_17(chat_id, context):
    response = context.user_data.get('last_response')  # Получаем последний ответ пользователя

    if not response:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Кажется, вы ничего не ответили. Попробуйте снова!"
        )
        return DAY_3[16]

    if re.search(r"\bева\b", response, re.IGNORECASE):
        context.user_data['test_score'] += 1
        user = await get_user_by_chat_id(chat_id)
        user.timepad += 1
        await save_user(user)
        await context.bot.send_message(
        chat_id=chat_id, text="Верно! + 1 таймпадик")
        await context.bot.send_message(
            chat_id=chat_id,
            text="Второй вопрос, *сколько у нас есть волшебных дней в году? 🪄*",
            parse_mode="Markdown",
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id, text="Эх, как же ты забыл нашу ЕВУ😓")
        await context.bot.send_message(
            chat_id=chat_id,
            text="Второй вопрос, *сколько у нас есть волшебных дней в году? 🪄*",
            parse_mode="Markdown",
        )

    return DAY_3[17]


async def block_18(chat_id, context):
    response = context.user_data.get('last_response')

    if re.search(r"\b3\b", response, re.IGNORECASE):
        context.user_data['test_score'] += 1
        user = await get_user_by_chat_id(chat_id)
        user.timepad += 1
        await save_user(user)
        await context.bot.send_message(
            chat_id=chat_id, text="Верно! + 1 таймпадик")
        await context.bot.send_message(
            chat_id=chat_id,
            text="Третий вопрос, *как назывется наш tg-канал с афишой?*",
            parse_mode="Markdown",
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id, text="Волшебные 3 дня! 🪄")
        await context.bot.send_message(
            chat_id=chat_id,
            text="Третий вопрос, *как назывется наш tg-канал с афишой?*",
            parse_mode="Markdown",
        )

    return DAY_3[18]


async def block_19(chat_id, context):
    response = context.user_data.get('last_response')

    if re.search(r"\bСпасите мои выходные\b", response, re.IGNORECASE):
        context.user_data['test_score'] += 1
        user = await get_user_by_chat_id(chat_id)
        user.timepad += 1
        await save_user(user)
        await context.bot.send_message(
            chat_id=chat_id, text="Верно! + 1 таймпадик")
        await context.bot.send_message(
            chat_id=chat_id,
            text="Четвертый вопрос, *где можно поделиться своими фотками с коллегами и неформально пообщаться?* "
            "(это какой-то из наших внутренних каналов, не нельзяграмм 😂)",
            parse_mode="Markdown",
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id, text="Эх, Спасите мои выходные! @TimepadRU")
        await context.bot.send_message(
            chat_id=chat_id,
            text="Четвертый вопрос, **где можно поделиться своими фотками с коллегами и неформально пообщаться? "
            "**(это какой-то из наших внутренних каналов, не нельзяграмм 😂)",
            parse_mode="Markdown",
        )
    return DAY_3[19]


async def block_20(chat_id, context):
    response = context.user_data.get('last_response')

    if re.search(r"\bOfftop Timepad\b", response, re.IGNORECASE):
        context.user_data['test_score'] += 1
        user = await get_user_by_chat_id(chat_id)
        user.timepad += 1
        await save_user(user)
        await context.bot.send_message(
            chat_id=chat_id, text="Верно! + 1 таймпадик")
        cats_txt = (
            "Кстати, *каждую пятницу мы делимcя фотографиями своих четвероногих друзей!* Если у тебя есть питомец, "
            "то присоединяйся по пятницам к нашей милой традиции 🐾"
        )
        await context.bot.send_photo(
            chat_id=chat_id,
            photo="https://disk.yandex.ru/i/E5teV7j_hL-45Q",
            caption=cats_txt,
            parse_mode="Markdown",
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text="И финалный - пятый вопрос, вставь пропущенное слово: \n\n"
            "*Мы __ ________ увлечения, чтобы раскрывался потенциал и новые возможности*",
            parse_mode="Markdown",
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id, text="Правильный ответ - Offtop Timepad")
        cats_txt = (
            "Кстати, *каждую пятницу мы делимcя фотографиями своих четвероногих друзей!* Если у тебя есть питомец, "
            "то присоединяйся по пятницам к нашей милой традиции 🐾"
        )
        await context.bot.send_photo(
            chat_id=chat_id,
            photo="https://disk.yandex.ru/i/E5teV7j_hL-45Q",
            caption=cats_txt,
            parse_mode="Markdown",
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text="И финалный - пятый вопрос, вставь пропущенное слово: \n\n"
            "*Мы __ ________ увлечения, чтобы раскрывался потенциал и новые возможности*",
            parse_mode="Markdown",
        )
    return DAY_3[20]


async def block_21(chat_id, context):
    response = context.user_data.get('last_response')
    button = "Тест пройден 📋"
    keyboard = ReplyKeyboardMarkup(
            [[button]],
            resize_keyboard=True,
            one_time_keyboard=True
    )

    if re.search(r"\bподдерживаем\b", response, re.IGNORECASE):
        context.user_data['test_score'] += 1
        user = await get_user_by_chat_id(chat_id)
        user.timepad += 1
        await save_user(user)
        await context.bot.send_message(
            chat_id=chat_id,
            text="Верно! + 1 таймпадик",
            reply_markup=keyboard
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Как же ты забыл нашу миссию 🥺 Мы поддерживаем!",
            reply_markup=keyboard
        )

    return DAY_3[21]


async def block_22(chat_id, context):
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
        await context.bot.send_message(
            chat_id=chat_id,
            text="Это была хорошая попытка! Возможно, тебе стоит еще раз перечитать информацию, "
            "она тебе точно пригодится в работе!",
            reply_markup=keyboard_2
        )
        return DAY_3[22]

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard
    )
    await context.bot.send_sticker(
        chat_id=chat_id,
        sticker=open(image_url, 'rb'),
    )
    return DAY_3[22]


async def block_23(chat_id, context):
    text = (
        "На сегодня это все! Встретимся завтра и продолжим! Чао 🖐"
    )
    button = ReplyKeyboardRemove()

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=button
    )






