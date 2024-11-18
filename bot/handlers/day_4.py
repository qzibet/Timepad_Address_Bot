import os

from asgiref.sync import sync_to_async
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
import logging

from bot.handlers import day_5
from bot.handlers.conversations_states import DAY_5, DAY_6
from bot.models import TelegramUser

logger = logging.getLogger(__name__)
IVAN_SECRET_PASSWORD = os.getenv("IVAN_SECRET_PASSWORD")


async def block_0(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Доброе утро! \n\n"
        "Начинаем день с зарядки и... разговора о корпоравтиных плюшках и всяких приколюхах! \n\n"
        "Расскажем тебе о наших корпоративах и мероприятиях, а \"на десерт\" - ДМС!"
    )
    photo_url = "https://disk.yandex.ru/i/G1uMLDaQXvCznA"
    button = "🚀🚀🚀"

    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_photo(
        photo=photo_url,
        caption=text,
        reply_markup=keyboard,
    )
    return DAY_5[0]


async def block_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Начнем с корпоративных скидок (от нас и наших компаний-друзей)! \n\n"
        "[Жми сюда](https://telegra.ph/Bonusy-i-partnerskie-skidki-11-14)"
    )
    button = "Скидочки-скидочки 💳"

    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    return DAY_5[1]


async def block_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_1 = (
        "А еще мы любим поздравлять сотрудников с ДНЕМ РОЖДЕНИЯ! 🎂 \n\n"
        "🥳 И делаем мы это так:"
    )
    await update.message.reply_text(
        text=text_1
    )
    await update.message.reply_text(
        "ссылка на форму про ДР",
    )
    text_2 = (
        "Заполни форму, чтобы мы знали, когда кричать тебе HAPPY BIRTHDAY!!! 🎉 \n\n"
        "А ещё, незабудь **выбрать себе подарок **🤩"
    )
    photo_url = "https://disk.yandex.ru/i/o3-uIABa4BX0cA"
    button = "О, подарочки! Это я люблю 🎁"

    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_photo(
        photo=photo_url,
        caption=text_2,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

    return DAY_5[2]


async def get_user_by_chat_id(chat_id):
    return await sync_to_async(TelegramUser.objects.get)(chat_id=chat_id)


async def save_user(user):
    await sync_to_async(user.save)()


async def block_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "А теперь о наших корпоративах!"
    button = "Хочу посмотреть!"

    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=text,
        reply_markup=keyboard,
    )
    return DAY_5[3]


async def block_4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = "Круто! Хочу также!"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    message = await update.message.reply_video(
        video="BAACAgIAAxkDAAINjGcw887CTsweNDQkKH5jP2u259CXAAIeZwACiaCISb6oAAFYx0ZLwTYE",
        reply_markup=keyboard,
        read_timeout=120,
        write_timeout=120,
        connect_timeout=120,
        pool_timeout=120
    )

    video_file_id = message.video.file_id
    logger.info(f"video id {video_file_id}")
    return DAY_5[4]


async def block_5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Но это не всё! У нас есть ещё и другие мероприятия ✨\n\n"
        "ссылка из ноушена про таймпад ап"
    )
    button = "Интересно 🤩"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        text=text,
        reply_markup=keyboard
    )
    return DAY_5[5]


async def block_6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Тут перечисление активностей добавить текст"
    )
    button = "Ух ты, как здорово!"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        text=text,
        reply_markup=keyboard
    )
    return DAY_5[6]


async def block_7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "А теперь небольшая анкета, чтобы мы лучше узнали тебя и твои увлечения 🎫 \n\n"
        "P.S. После заполнения возвращайся сюда, мне есть о чём тебе ещё рассказать!"
    )
    button = "Готовоооо"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        text=text,
        reply_markup=keyboard
    )
    return DAY_5[7]


async def block_8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = await get_user_by_chat_id(chat_id)
    user.timepad += 10
    await save_user(user)

    text = (
        "Лови **10 таймпадиков **и беги к Ване за паролем 🏃🏼‍♂️\n\n"
    )

    button = ReplyKeyboardRemove()

    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=button
    )

    context.user_data['awaiting_password'] = True
    return DAY_5[8]


async def block_9(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_password', False):
        password = update.message.text
        print(password)

        if password == IVAN_SECRET_PASSWORD:
            context.user_data['awaiting_password'] = False
            return DAY_5[9]
        else:
            await update.message.reply_text("Пароль неверный 😓 попробуй ещё раз!")
            await block_8(update, context)


async def block_10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Круто!\n\n"
        "Мы работаем в гибридном формате и видимся не каждый день, к сожалению 😔 "
        "НО у тебя есть крутая возможность встречаться с коллегами чаще (онлайн и офлайн), "
        "**зарегистрировавшись в нашем внутреннем Random coffee** ☕️ \n\n"
        "**Как это работает?** После регистрации в [боте](https://t.me/Timepadres_bot),"
        "раз в неделю тебе будет приходить ссылка на твоего нового random coffee друга, с которым вы "
        "могли бы встретиться онлайн/офлайн и круто провести время!\n\n"
        "За регистрацию в Random coffee тебе также упадет **10 таймпадиков!*"
    )
    await update.message.reply_text(text=text, parse_mode="Markdown")
    await update.message.reply_text("Как пройдешь регистрацию - возвращайся ко мне!")
    button_1 = "РЕГИСТРАЦИЯ ПРОЙДЕНА, жду новые знакомства! ☕️"
    button_2 = "Пока подумаю!"
    keyboard = ReplyKeyboardMarkup(
        [[button_1, button_2]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        "Прошел регистрацию?",
        reply_markup=keyboard,
    )
    return DAY_5[10]


async def block_11(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.message.text
    print(response)
    button = "Посмотрю 😇"
    keyboard = ReplyKeyboardMarkup(
            [[button]],
            resize_keyboard=True,
            one_time_keyboard=True
    )

    if response == "Пока подумаю!":
        text = (
            "Будет здорово, если ты станешь частью этого сообщества 🥺 НО, если пока не хочешь, то погнали дальше!"
        )
    else:
        chat_id = update.effective_chat.id
        user = await get_user_by_chat_id(chat_id)
        user.timepad += 10
        await save_user(user)
        text = "Ну, тогда погнали дальше!"
        photo_url = "https://disk.yandex.ru/i/_AChZmNyyms1Jg"
        await update.message.reply_photo(
            photo=photo_url,
            caption="Лови 10 таймпадиков за подписку",
            reply_markup=keyboard,
        )

    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    big_text = (
        "У нас есть традиция! \n\n"
        "Раз в месяц **мы встречаемся все вместе онлайн** и подводим итоги - как у кого прошел месяц! \n\n"
        "🧐 **Задание: **посмотреть последнюю встречу, чтобы вникнуть в наш продукт и познакомиться с коллегами!"
    )
    await update.message.reply_text(
        text=big_text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    return DAY_5[11]


async def block_12(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Как прошёл месяц в Timepad? — общая встреча, где команды делятся своими "
        "успехами в прошлом месяце и планами на следующий. \n\n"
        "Как это было? \n\n"
        "[Записи и презентации мероприятий](https://www.notion.so/42d7ebd5335844e2afacbb1c6f0c061a?pvs=21) \n\n"
        "[Корпоративные мероприятия](https://www.notion.so/4c1bcbf52bef458c8b5af800e94c8871?pvs=21) \n\n"
        "P.S. Как только посмотришь видео - нажимай \"просмотрено\"."
    )
    button = "Просмотрено ✅"
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
    return DAY_5[12]


async def block_13(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = await get_user_by_chat_id(chat_id)
    user.timepad += 10
    await save_user(user)
    text = "Тогда лови еще **10 таймпадиков!**"
    button = "Ура ура!!!"
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
    return DAY_5[13]


async def block_14(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Ещё у нас есть **разные чаты по интересам!** \n\n"
        "Вступать во все не нужно 😅, а **только по желанию! **"
    )
    button = "Хочу хочу"
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
    return DAY_5[14]


async def block_15(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "**Выбирай:** \n\n"
        "- [Каток](https://t.me/+x2m0Ry7AU3cwODEy) \n\n"
        "- [Сапы](https://t.me/+XJlZ1_sJTKllZjQ6) \n\n"
        "- [Караоке](https://t.me/+WTlTv0-Tym0zNjUy) \n\n"
    )
    button = "Выбор сделан 🔦"
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
    return DAY_5[15]


async def block_16(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = ReplyKeyboardRemove()
    await update.message.reply_photo(
        photo="https://disk.yandex.ru/i/sQX7fAlOSiFTOQ",
        caption="Круто поболтали! Пока-пока, и до завтра!",
        reply_markup=button,
    )
    await day_5.block_0(update, context)
    return DAY_6[0]


