import os

from django.conf import settings
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async
import logging

from bot.handlers import day_2
from bot.handlers.conversations_states import DAY_1, DAY_2, DAY_3
from bot.models import TelegramUser, Code

logger = logging.getLogger(__name__)


async def block_0(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user = await sync_to_async(TelegramUser.objects.get)(chat_id=chat_id)
    photo_url = os.path.join(settings.MEDIA_ROOT, "heysticker.webp")
    video = os.path.join(settings.MEDIA_ROOT, "Ценности и Миссия  (1).mp4")

    if user.work_type == 'Офис':
        text = (
            f"Привет, {user.name}!\n\n"
            "На связи Таймика 📻 \n\n"
            "Я помогу тебе с пользой провести время до встречи с HR: давай погрузимся "
            "в мир наших ценностей и миссии! 😉\n\n"
        )
        button = "Давай!"
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
        return DAY_2[0]
    else:
        text = (
            f"Привет, {user.name}!\n\n"
            "На связи Таймика 📻 ВАЖНАЯ ИНФОРМАЦИЯ!\n\n"
            "Твоя *встреча с HR* уже совсем скоро - мы ждём тебя в *11:00!*\n\n"
            "**Вот ссылка на [встречу в ZOOM](https://your-zoom-link.com)**\n\n"
            "*Заходи ровно в 11:00!*"
        )
        button = "Буду!"
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

    # Переход к следующему блоку после выполнения основной логики
        return DAY_2[0]


async def block_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user = await sync_to_async(TelegramUser.objects.get)(chat_id=chat_id)
    button = "Вдохновляет!"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    if user.work_type == 'Офис':
        await context.bot.send_video(
            chat_id=chat_id,
            video="BAACAgIAAxkBAAIVMGc6bQdEZLDVp_0wEaPrIqQRJjRlAAK7aAACoAjRSTdax4VaYUryNgQ",
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    else:
        text = (
            "Я помогу тебе с пользой провести время до нашей встречи: "
            "давай погрузимся в мир наших ценностей и миссии! 😉"
        )
        await update.message.reply_text(
            reply_markup=keyboard,
            text=text,
        )
        await context.bot.send_video(
            chat_id=chat_id,
            video="BAACAgIAAxkBAAIVMGc6bQdEZLDVp_0wEaPrIqQRJjRlAAK7aAACoAjRSTdax4VaYUryNgQ",
            parse_mode="Markdown",
            reply_markup=keyboard
        )

    return DAY_2[1]


async def block_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "А теперь небольшое задание: *подумай и выбери какая ценность для тебя самая близкая.*🤫 \n\n"
        "Небольшой секретик, это понадобится на встрече с HR!"
    )
    button = "Спасибо за совет! 😘"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
    return DAY_2[2]


async def block_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user = await sync_to_async(TelegramUser.objects.get)(chat_id=chat_id)
    if user.work_type == 'Офис':
        text = (
            "Удачи тебе! 🍀\n\n"
            "*Напиши мне после встречи!* У меня есть, что тебе рассказать 🤭"
        )
    else:
        text = (
            "И еще раз ссылочка на встречу с HR: https://your-zoom-link.com. Ждём тебя в *11:00!* \n\n"
            "Удачи! 🍀"
        )
    button = "Встреча прошла прекрасно!"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
    return DAY_2[3]


async def block_4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_url = os.path.join(settings.MEDIA_ROOT, "docsticker.webp")
    text = (
        "Привет-привет, это Таймпадрес-бот! 📻 \n\n"
        "Дальше мы пройдемся с тобой по организационным моментикам 📋."
    )
    await update.message.reply_sticker(
        sticker=open(photo_url, 'rb'),
    )
    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
    )

    text_2 = (
        "Расскажу тебе подробнее как и где мы общаемся, и как ставим задачки."
    )
    button = "Жду подробностей 🖋️"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=text_2,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
    return DAY_2[4]


async def block_5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "У нас есть каналы коммуникации и база знаний:\n\n"
        "💡 *Основной канал коммуникации* - Телеграм.\n\n"
        "Там чаты, куда тебя добавит HR и представит команде.\n\n"
        "🗓️ *Канал события* - там мы публикуем новости, анонсы на "
        "корпоративные активности и мероприятия.\n\n"
        "📸 *Offtop Timepad* - неформальный чат, где делимся своими фото и "
        "настроением, а также обсуждаем всё подряд.\n\n"
        "P.S. Ещё у тебя будут свои чаты с сотрудниками по отделам."
    )
    button = "Больше чатов, Богу чатов"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
    return DAY_2[5]


async def block_6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Для постановки задач мы используем *систему Ева.*\n\n"
        "Знакомство с ней было на велком-встрече. Прочитать подробнее про неё можно [здесь](https://your-link.com). "
        "ТЫК на слово здесь"
    )
    button = "А где Адам? 😂"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
    return DAY_2[6]


async def block_7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Ха-ха, Адам пока в разработке.\n\n"
        "А ещё у нас есть почта. Кстати, не забудь добавить там красивую подпись!"
    )
    button = "📝, а где созвоны?"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
    return DAY_2[7]


async def block_8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Созваниваемся чаще всего в ZOOM, но некотрые команды общаются в Google Meet."
    )
    button = "Здорово! А что там с доками?"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
    return DAY_2[8]


async def block_9(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Порешаем кадровые вопросики?"
    )
    button = "Да, да 🤓"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
    return DAY_2[9]


async def block_10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📑 За кадровый документооборот у нас отвечает *Аня Саухина.* @Chodarova \n\n"
        "💳 За зарплату *Настя Шувалова.*  Не забывай записывать номера коллег, они 100% тебе пригодятся")
    button = (
        "Уже в контактах 🫡"
    )
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
    return DAY_2[10]


async def block_11(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Что ещё важно знать:\n\n"
        "💳 Зарплата приходит *5 и 20 числа каждого месяца*, если твоё оформление по ТК РФ.\n\n"
        "*Аванс:* (20го числа)\n"
        "Это сумма, которая рассчитывается за отработанные дни с 1 по 15 число. "
        "(Поэтому в январе всегда маленький аванс, так как мы там совсем немножко работаем).\n\n"
        "*Зарплата:*\n"
        "5го числа приходит остальная сумма по твоему договору.\n\n"
        "*Формула такая:* зарплата / на количество рабочих дней \\* на отработанные дни.\n\n"
        "*Например:* зарплата на руки 120 000. В июле 23 рабочих дня. Отработано 11 дней (с 1 по 15 июля).\n"
        "120 000 / 23 \\* 11 = 57 391. Значит, в зарплату придёт оставшаяся часть = 62 609.\n\n"
        "📝Если у тебя иная форма взаимодействия с нами, то даты выплат нужно уточнить *у Ани Саухиной* @Chodarova"
    )
    button = "Оки-доки"
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
    return DAY_2[11]


async def block_12(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "У нас есть система кадрового электронного документооборота (сокращенно - *КЭДО*). \n\n"
        "Система, которую мы используем - ТинькоффКЭДО. сотрудников "
        "используется интерфейс - https://work.jump.finance/ \n\n"
        "По всем вопросам о КЭДО можно обратиться к *Анне Саухиной*.\n\n"
        "А тебе в помощь - короткое видео про КЭДО, наслаждайся!"
    )
    button = (
        "Ух какая автоматизация!"
    )
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
    return DAY_2[12]


async def block_13(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = (
         "Понял, принял"
    )
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_video(
        video="BAACAgIAAxkBAAIYj2c6fOSdrqhTWMmRRzNDDi-TZ1CfAAL2aAACoAjRSRIpjvM5t642NgQ",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

    return DAY_2[13]


async def block_14(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "А теперь - приятное, про отпуск и волшебный день! 🏝️ \n\n"
        "Заходи по [ссылке](https://telegra.ph/Otpusk-bolnichnyj-ili-volshebnyj-den-10-29) и "
        "читай важную информацию! \n\n"
        ""
    )
    button_1 = (
        "Классно!"
    )
    button_2 = (
        "В отпуске клево!"
    )
    keyboard = ReplyKeyboardMarkup(
        [[button_1, button_2]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )
    return DAY_2[14]


async def block_15(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Ещё немного нюансиков: \n\n"
        "Если у тебя *меняется фамилия/место жительство/ реквизиты в банке* - мы всегда просим "
        "об этом нам сообщать для верной документации."
    )
    button = (
        "Хорошо"
    )
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
    return DAY_2[15]


async def block_16(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Если тебе нужна справка  с работы - переходи по [ссылке](https://telegra.ph/Spravka-s-raboty-10-29) "
        "и ты узнаешь как ее получить 🙌"
    )
    button = (
        "Возьму на заметку📝"
    )
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
    return DAY_2[16]


async def block_17(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_url = os.path.join(settings.MEDIA_ROOT, "laptopsticker.webp")

    await update.message.reply_sticker(
        sticker=open(photo_url, 'rb'),
    )
    text = (
        "Ух! Много информации сразу, понимаю. \n\n"
        "Поэтому продолжим завтра. А пока погружайся в  рабочий процесс, знакомься с коллегами и руководителем! 🗂️"
    )
    button = ReplyKeyboardRemove()
    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=button,
    )
    await day_2.block_0(update, context)
    return DAY_3[0]
