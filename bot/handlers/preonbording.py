from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async
import logging

from bot.handlers import day_of_work
from bot.handlers.conversations_states import DAY_1, DAY_2
from bot.handlers.day_of_work import block_0
from bot.models import TelegramUser, Code

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.username or "Неизвестно"
    chat_id = update.effective_chat.id
    user = await sync_to_async(TelegramUser.objects.filter(chat_id=chat_id).first)()

    welcome_text = (
        "Привет! Я твой друг **Таймпадрес-бот**! Рады, что ты совсем скоро "
        "станешь частью нашей команды Таймпад! Я вместе со своей помощницей "
        "**Таймикой** помогу тебе адаптироваться и пройти этот путь легко.\n\n"
        "Если я сломаюсь или у меня отвалятся какие-то винтики, то обратись "
        "к нашему **Мастеру Винтиков** (кнопка в меню - Тех. поддержка) 🙌\n\n"
        "**Мини-инструкция**: если не приходит следующее сообщение и ты не видишь "
        "кнопку на экране, ищи кнопки в строке ввода сообщений. Справа будет знак, "
        "похожий на пуговицу🔢 - кнопки прячутся там!"
    )

    welcome_back_text = "Привет! Давно тебя не было"
    if not user:
        await save_user(user_name, chat_id)
        text = welcome_text
        next_state = DAY_1[0]
    else:
        code = await sync_to_async(Code.objects.filter(user=user).first)()

        if not code:
            text = welcome_text
            next_state = DAY_1[0]
        else:
            text = welcome_back_text
            next_state = DAY_1[2]

    photo_url = "https://disk.yandex.ru/i/ufYMni4x127dhQ"
    button = KeyboardButton("Юхуу, погнали")
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

    return next_state


@sync_to_async
def save_user(user_name, chat_id):
    try:
        user, created = TelegramUser.objects.get_or_create(
            username=user_name, chat_id=chat_id
        )
        if not created:
            user.chat_id = chat_id
            user.save()
    except Exception as e:
        logger.error(f"Ошибка при сохранении пользователя: {e}")


@sync_to_async
def get_code_entry(code):
    return Code.objects.get(code=code)


@sync_to_async
def get_or_create_telegram_user(user_id):
    return TelegramUser.objects.get_or_create(chat_id=user_id)


@sync_to_async
def save_code_entry(code_entry):
    code_entry.save()


@sync_to_async
def get_user_chat_id(user):
    return user.chat_id if user else None


async def ask_for_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Пожалуйста, введите код доступа, который вам прислал администратор:"
    )
    return DAY_1[1]


async def request_access_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text.strip()

    try:
        code_entry = await get_code_entry(user_message)
        if code_entry.user:
            telegram_user, created = await get_or_create_telegram_user(user_id)
            code_entry.user = telegram_user
            await save_code_entry(code_entry)
            return DAY_1[2]
            await update.message.reply_text(
                "Код подтвержден, доступ предоставлен. Добро пожаловать!"
            )
            return DAY_1[2]
        else:
            telegram_user, created = await get_or_create_telegram_user(user_id)
            code_entry.user = telegram_user
            await save_code_entry(code_entry)
            return DAY_1[2]

    except ObjectDoesNotExist:
        await update.message.reply_text("Неверный код доступа!")
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
        await update.message.reply_text(f"Произошла ошибка: {str(e)}")
        return DAY_1[2]


async def request_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = await sync_to_async(
        TelegramUser.objects.filter(
            chat_id=user_id
        ).first)()
    code = await sync_to_async(
        Code.objects.filter(
            user=user
        ).first)()
    text = "Как я могу к тебе обращаться?"
    if code.start_date <= date.today():
        late_message = (
            "Я ждал тебя пару дней назад и подготовил контент еще до твоего первого рабочего дня. "
            "Прочитай его, пожалуйста, сейчас, так как он важный!"
        )
        text = f"{late_message}\n\n{text}"
    else:
        await update.message.reply_text(text=text)
        next_state = DAY_1[0]

    await update.message.reply_text(text=text)
    return DAY_1[3]


async def save_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    chat_id = update.message.chat_id
    await update_user_name(chat_id, name)

    text = (
        "Здорово! А теперь давай познакомимся с тобой поближе 😉\n\n"
        "Заполни, пожалуйста, анкету (делай ТЫК на слово \"[анкета](https://client.app-raise.org/ru/surveys/2647/3d9673f5-6b04-4650-9890-aa7b59162ce4/)\").\n\n"
        "P.S. Как только пройдешь анкету, снова возвращайся ко мне в бот и нажимай \"Всё готово\".\n\n"
        "P.P.S. Не пугайся, если не увидишь по возвращению кнопку - она спряталась в меню рядом с полем для сообщений."
    )

    button = KeyboardButton("Всё готово!")
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=keyboard
    )
    return DAY_1[4]


@sync_to_async
def update_user_name(chat_id, name):
    from bot.models import TelegramUser  # импорт модели
    try:
        user = TelegramUser.objects.get(chat_id=chat_id)
        user.name = name
        user.save()
    except TelegramUser.DoesNotExist:
        logger.error(f"Пользователь с chat_id {chat_id} не найден.")


async def block_5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Ура! Первый этап преодолен. Дальше тебя ждут классные встречи с командой, "
        "погружение в продукт и мемасы!"
    )
    button_1 = KeyboardButton("🥳")
    button_2 = KeyboardButton("🥰")
    button_3 = KeyboardButton("👍")

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

    return DAY_1[5]


async def block_6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        'Лови наш стикер-пак (делай ТЫК на слово "[стикер-пак](https://t.me/addstickers/timepadres)") '
        'И читай историю создания этих картинок 😉'
    )

    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
    )

    document_url = "https://s604vla.storage.yandex.net/rdisk/836e6d5a86ddb541ade405f938f5cc549f99ee03d3ea3a22afffe75135034779/672c38cf/MM8Im2FXnMYzmVy63dTdDHjYfQuQmLs1A96lQqEXlb0bs7C_aNanj0mF_gRhxM_8taQd9GC_w8tfazEX5li6QQ==?uid=0&filename=%D0%98%D1%81%D1%82%D0%BE%D1%80%D0%B8%D1%8F_%D0%A1%D1%82%D0%B8%D0%BA%D0%B5%D1%80%D0%BF%D0%B0%D0%BA%D0%B0.pdf&disposition=attachment&hash=MV%2F8f%2FpP4VsWGP6Wj8m8WTgaAVnuxMX0HzIhPb6YjATxI2915oCVC5b1QdqR4kPrG7pWpVQYsubyrcajHimPFw%3D%3D&limit=0&content_type=application%2Fpdf&owner_uid=1130000064556865&fsize=4866463&hid=9c2b58a1908ba469c48366b0225eddcd&media_type=document&tknv=v2&ts=6264a85d491c0&s=1df1e7318d6ec5dbdbf0fb583f71dd5f4c4f582aaa8f85246c707dd6ff14bf27&pb=U2FsdGVkX18_jJDXO_tK2_RICA_C-7vx2DBiVMgx4oxmxIvqoFO9d-Fye6V0eXCpN92UsUouH8J4RSIl7MnONO86z13GbKXiwMy999pyxcM"  # Убедитесь, что ссылка доступна и поддерживается
    button = KeyboardButton("Спасибо ❤️")
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_document(
        document=document_url,
        reply_markup=keyboard
    )

    return DAY_1[6]


async def block_7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Ждём тебя в первый рабочий день в нашем **офисе - если ты работаешь из Москвы,** "
        "а если **удаленно - пришлем тебе ссылку на зум!**"
    )
    office_button = "Я приду в офис!"
    freelance_button = "Я удаленный сотрудник!"
    keyboard = ReplyKeyboardMarkup(
        [[office_button, freelance_button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

    return DAY_1[7]


async def block_8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    response = update.message.text

    try:
        user = await sync_to_async(TelegramUser.objects.get)(chat_id=chat_id)
    except TelegramUser.DoesNotExist:
        return
    print(response)
    if response == 'Я приду в офис!':
        user.work_type = 'Офис'
    elif response == 'Я удаленный сотрудник!':
        user.work_type = 'Удаленка'

    if user.work_type:
        await sync_to_async(user.save)()
    # Получаем chat_id пользователя
    chat_id = update.message.chat_id
    user = await sync_to_async(TelegramUser.objects.get)(chat_id=chat_id)
    button = "Супер! Все понятно😎!"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    # В зависимости от типа работы отправляем соответствующее сообщение
    if user.work_type == 'Офис':
        text = (
            "Круто! Тогда лови наш адрес и видео-путеводитель, чтобы добраться до нас!\n\n"
            "Адрес: Холодильный пер. 3, офис 325"
        )
        # Отправка видео как файл
        video_url = "https://disk.yandex.ru/i/948L4A1ZazDpEg"
        await update.message.reply_text(
            text=text,
            parse_mode="Markdown",
            reply_markup=keyboard
        )
        return DAY_1[8]

    elif user.work_type == 'Удаленка':
        text = (
            "Прекрасно! В твой первый рабочий день пришлю сюда **ссылку в ZOOM на встречу с HR.**\n"
            "Встреча начнется в 11:00.\n\n"
            "Жди моих сообщений!"
        )
        await update.message.reply_text(
            text=text,
            parse_mode="Markdown",
            reply_markup=keyboard
        )

    return DAY_1[8]


async def block_9(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Пока-пока! До встречи в твой первый рабочий день!"
    )
    photo_url = "https://disk.yandex.ru/i/54JX9HTdn7pavg"

    empty_keyboard = ReplyKeyboardRemove()

    await update.message.reply_photo(
        photo=photo_url,
        caption=text,
        parse_mode="Markdown",
        reply_markup=empty_keyboard
    )
    await block_0(update, context)
    return DAY_2[0]
