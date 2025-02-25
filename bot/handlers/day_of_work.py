import os

from django.conf import settings
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from asgiref.sync import sync_to_async
import logging

from bot.handlers import day_2
from bot.handlers.conversations_states import DAY_1, DAY_2, DAY_3
from bot.models import TelegramUser, Code, FirstDay

logger = logging.getLogger(__name__)


async def get_user_by_chat_id(chat_id):
    return await sync_to_async(TelegramUser.objects.get)(chat_id=chat_id)


async def save_user(user):
    await sync_to_async(user.save)()


async def block_0(chat_id, context):
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
        return DAY_2[0]
    else:
        meet_link = await sync_to_async(
            lambda: FirstDay.objects.first().link_zoom
        )()
        text = (
            f"Привет, {user.name}!\n\n"
            "На связи Таймика 📻 ВАЖНАЯ ИНФОРМАЦИЯ!\n\n"
            "Твоя *встреча с HR* уже совсем скоро - мы ждём тебя в *11:00!*\n\n"
            f"*Вот ссылка на* [встречу в ZOOM]({meet_link})\n\n"
            "*Заходи ровно в 11:00!*"
        )
        button = "Буду!"
        keyboard = ReplyKeyboardMarkup(
            [[button]],
            resize_keyboard=True,
            one_time_keyboard=True,

        )

        await context.bot.send_sticker(
            sticker=open(photo_url, 'rb'),
        )

        await context.bot.send_message(
            text=text,
            parse_mode="Markdown",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )

    # Переход к следующему блоку после выполнения основной логики
        return DAY_2[0]


async def block_1(chat_id, context):
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
            video="BAACAgIAAxkBAAMkZ6IORBkDn1DG2SOgh6Ez3SaiUZEAArtoAAKgCNFJcq0h00fMi3U2BA",
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    else:
        text = (
            "Я помогу тебе с пользой провести время до нашей встречи: "
            "давай погрузимся в мир наших ценностей и миссии! 😉"
        )
        await context.bot.send_message(
            chat_id=chat_id,
            reply_markup=keyboard,
            text=text,
        )
        await context.bot.send_video(
            chat_id=chat_id,
            video="BAACAgIAAxkBAAMkZ6IORBkDn1DG2SOgh6Ez3SaiUZEAArtoAAKgCNFJcq0h00fMi3U2BA",
            parse_mode="Markdown",
            reply_markup=keyboard
        )

    return DAY_2[1]


async def block_2(chat_id, context):
    text = (
        "Итак: **Наша миссия** \n\n"
        "Мы поддерживаем увлечения, чтобы раскрывался потенциал и новые возможности \n\n"
        "**Наши ценности** \n\n"
        "💜 Заботимся друг о друге \n\n"
        "👍 Адаптируем опыт \n\n"
        "🔝 Содействуем развитию \n\n"
        "🎉 Создаем атмосферу \n\n"
        "А теперь небольшое задание: **подумай и выбери какая ценность для тебя самая близкая.** \n\n"
        "🤫 Небольшой секретик, это понадобится на встрече с HR!"
    )
    button = "Спасибо за совет! 😘"
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
    )
    return DAY_2[2]


async def block_3(chat_id, context):
    user = await sync_to_async(TelegramUser.objects.get)(chat_id=chat_id)
    if user.work_type == 'Офис':
        text = (
            "Удачи тебе! 🍀\n\n"
            "*Напиши мне после встречи!* У меня есть, что тебе рассказать 🤭"
        )
    else:
        meet_link = await sync_to_async(
            lambda: FirstDay.objects.first().link_zoom
        )()
        text = (
            f"И еще раз [сылочка]({meet_link})"
            " на встречу с HR. Ждём тебя в *11:00!* \n\n"
            "**После встречи нажми кнопку \"Встреча прошла!\"** \n\n"
            "Удачи! 🍀"
        )
    button = "Встреча прошла!"
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
    return DAY_2[3]


async def block_4(chat_id, context):
    photo_url = os.path.join(settings.MEDIA_ROOT, "docsticker.webp")
    text = (
        "Привет-привет, это Таймпадрес-бот! 📻 \n\n"
        "Дальше мы пройдемся с тобой по организационным моментикам 📋."
    )
    await context.bot.send_sticker(
        chat_id=chat_id,
        sticker=open(photo_url, 'rb'),
    )
    await context.bot.send_message(
        chat_id=chat_id,
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
    await context.bot.send_message(
        chat_id=chat_id,
        text=text_2,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
    return DAY_2[4]


async def block_5(chat_id, context):
    links = await sync_to_async(
        lambda: FirstDay.objects.first()
    )()
    text = (
        "У нас есть каналы коммуникации и база знаний:\n\n"
        "💡 *Основной канал коммуникации* - Телеграм.\n\n"
        "В чаты ниже добавляйся по ссылке (если она есть), в остальные тебя добавит HR и представит команде. \n\n"
        "🔊 *Timepad* - чат, где мы публикуем важные сообщения для команды, поздравляем с ДР, "
        "а также приветствуем новых сотрудников компании! \n\n"
        f"🗓️ [Канал события]({links.link_event_group}) - там мы публикуем новости, "
        "анонсы накорпоративные активности и мероприятия. \n\n"
        f"📸 [Offtop Timepad]({links.link_offtop_timepad})  - неформальный чат, где делимся своими фото и "
        "настроением, а также обсуждаем всё подряд.\n\n"
        "🛒*Барахолка и свопы* — чат для обмена, покупки и продажи ненужных, но хороших вещей. "
        f"Там же устраиваем распродажи офисной техники и т.п. Для входа напиши Паше {links.link_admin} \n\n"
        "P.S. Ещё у тебя будут свои чаты с сотрудниками по отделам. \n\n"
        "P.P.S. Если не получилось войти, напиши Юле в HR и тебя добавят💜"

    )
    button = "Больше чатов, Богу чатов"
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
    return DAY_2[5]


async def block_6(chat_id, context):
    link_eva = await sync_to_async(
        lambda: FirstDay.objects.first().link_eva
    )()
    text = (
        "Для постановки задач мы используем *систему ЕВА. \n\n"
        "* Знакомство с ней пройдёт на велком-встрече и дальше уже в работе. \n\n"
        f"Добавляйся в [чат]({link_eva}), где ты сможешь задать все "
        "возникающие в работе вопросы по системе ЕВА ⚙️ \n\n"

    )
    button = "А где Адам? 😂"
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
    return DAY_2[6]


async def block_7(chat_id, context):
    logo_link = await sync_to_async(
        lambda: FirstDay.objects.first().logo_link
    )()
    text = (
        "Ха-ха, Адам пока в разработке.\n\n"
        "А ещё у нас есть почта. Кстати, не забудь добавить там красивую подпись! \n\n"
        f"Вот здесь можно скачать [лого]({logo_link} )"
    )
    button = "📝, а где созвоны?"
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
    return DAY_2[7]


async def block_8(chat_id, context):
    admin = await sync_to_async(
        lambda: FirstDay.objects.first().system_admin
    )()
    text = (
        "Созваниваемся чаще всего в ZOOM, но некоторые команды общаются в Google Meet. \n\n"
        "*P.S.* Если ты вдруг не сможешь зайти в ZOOM, почту или другие ресурсы, или техника будет "
        f"барахлить - тебе поможет наш друг *Паша Флайт {admin}. *Он системный администратор "
        "компании, который знает все ответы на технические вопросы ⚙️ 🔧"
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
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
    return DAY_2[8]


async def block_9(chat_id, context):
    byod_link = await sync_to_async(
        lambda: FirstDay.objects.first().link_byod
    )()
    text = (
        f"Обязательно изучи нашу программу [BYOD]({byod_link})! "
        "Это тебе поможет в работе 💻"
    )
    button = "Здорово, изучу! А что там с доками?"
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
    return DAY_2[9]


async def block_10(chat_id, context):
    links = await sync_to_async(
        lambda: FirstDay.objects.first()
    )()
    text = (
        f"📑 За кадровый документооборот у нас отвечает *Аня Саухина.* {links.hr_documentation_contact} \n\n"
        f"💳 За зарплату *Настя Шувалова* {links.payroll_contact} \n\n"
        f"💡Kind reminder:  Всех, кто встречается на твоем пути в этом боте сохраняй в контакты: "
        f"*Фамилия Имя должность/отдел и название компании* \n\n"
        f"Например, Юлия Маликова HR Timepad {links.hr_contact} (делай ТЫК, чтобы ещё раз сохранить котакт Юли). "
        f"Это поможет тебе быстро находить коллег в чатах."
    )
    button = (
        "Уже в контактах"
    )
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
    )
    return DAY_2[10]


async def block_11(chat_id, context):
    button_1 = "Трудовой договор"
    button_2 = "Иная форма"
    keyboard = ReplyKeyboardMarkup(
        [[button_1, button_2]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    text = (
        "Дальше выбери, пожалуйста, какая у тебя форма взаимодействия с нами: "
        "работа *по трудовому договору**  или **иная форма* (сюда входят - самозанятость, ИП и "
        "договор ГПХ)."
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
    return DAY_2[11]


async def block_12(chat_id, context):
    user = await sync_to_async(lambda: TelegramUser.objects.get(chat_id=chat_id))()
    user_choice = user.employment_type
    user = await get_user_by_chat_id(chat_id)
    hr_link = await sync_to_async(
        lambda: FirstDay.objects.first().hr_contact
    )()

    if user_choice == "Трудовой договор":
        user.employment_type = "Трудовой договор"
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
            f"📝Если у тебя иная форма взаимодействия с нами, то даты выплат нужно уточнить *у Ани Саухиной* {hr_link}"
        )
    else:
        user.employment_type = "Иная форма"
        text = (
            "📝 Поскольку у тебя иная форма взаимодействия с нами, даты выплат нужно уточнить "
            f"*у Ани Саухиной* {hr_link}."
        )

    await save_user(user)

    button = "Оки-доки"
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
    )
    return DAY_2[12]


async def block_13(chat_id, context):
    user = await get_user_by_chat_id(chat_id)
    link = await sync_to_async(
        lambda: FirstDay.objects.first().interface_link
    )()

    if user.employment_type == "Трудовой договор":
        text = (
            "У нас есть система кадрового электронного документооборота (сокращенно - *КЭДО*). \n\n"
            "Система, которую мы используем - ТинькоффКЭДО. Для сотрудников "
            f"используется интерфейс - {link} \n\n"
            "По всем вопросам о КЭДО можно обратиться к *Анне Саухиной*.\n\n"
            "А тебе в помощь - короткое видео про КЭДО, наслаждайся!"
        )
        button = "Ух какая автоматизация!"
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
    else:
        text = (
            "А теперь - приятное, про отпуск и волшебный день! 🏝️ \n\n"
            "Чтобы обезопасить себя от рабочих вопросов в отпуске или на выходном, "
            "ты *можешь поставить себе на аватарку в мессенджер одну из наших отпускных аватарок*😎"
            ""
        )
        button = (
            "О, хочу посмотреть!"
        )
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

    return DAY_2[13]


async def block_14(chat_id, context):
    user = await get_user_by_chat_id(chat_id)

    if user.employment_type == "Трудовой договор":
        button = (
            "Понял, принял"
        )
        keyboard = ReplyKeyboardMarkup(
            [[button]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await context.bot.send_video(
            chat_id=chat_id,
            video="BAACAgIAAxkBAAMmZ6IOVBBOmPKQnwesDdPBf8wc1YUAAvZoAAKgCNFJL_-tFpOWTiQ2BA",
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    else:
        photo_url = "https://disk.yandex.ru/i/INGSewyFoQWJog"
        link = await sync_to_async(
            lambda: FirstDay.objects.first().avatar_images_link
        )()
        text = (
            "😛 Фан-факт: почти все животные — это домашние питомцы наших сотрудников! \n\n"
            "Скачать картинки аватарок можно "
            f"[здесь]({link})"
        )
        keyboard = ReplyKeyboardMarkup(
            [["В отпуске клево!"]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=photo_url,
            caption=text,
            parse_mode="Markdown",
            reply_markup=keyboard,
        )
    return DAY_2[14]


async def block_15(chat_id, context):
    user = await get_user_by_chat_id(chat_id)

    if user.employment_type == "Трудовой договор":
        text = (
            "А теперь - приятное, про отпуск и волшебный день! 🏝️ \n\n"
            "Чтобы обезопасить себя от рабочих вопросов в отпуске или на выходном, "
            "ты *можешь поставить себе на аватарку в мессенджер одну из наших отпускных аватарок*😎"
            ""
        )
        button = (
            "О, хочу посмотреть!"
        )
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
    else:
        link = await sync_to_async(
            lambda: FirstDay.objects.first().freelance_vacation
        )()
        text = (
            f"🏝️ Заходи по [ссылке]({link}) и "
            f"читай важную информацию про отпуск!"
        )
        keyboard = ReplyKeyboardMarkup(
            [["Классно!"]],
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
    return DAY_2[15]


async def block_16(chat_id, context):
    user = await get_user_by_chat_id(chat_id)

    if user.employment_type == "Трудовой договор":
        photo_url = "https://disk.yandex.ru/i/INGSewyFoQWJog"
        link = await sync_to_async(
            lambda: FirstDay.objects.first().avatar_images_link
        )()
        text = (
            "😛 Фан-факт: почти все животные — это домашние питомцы наших сотрудников! \n\n"
            "Скачать картинки аватарок можно "
            f"[здесь]({link})"
        )
        keyboard = ReplyKeyboardMarkup(
            [["В отпуске клево!"]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=photo_url,
            caption=text,
            parse_mode="Markdown",
            reply_markup=keyboard,
        )
    else:
        text = (
            "Ещё немного нюансиков: Если у тебя *меняется фамилия/место жительство/ реквизиты в банке* - мы всегда "
            "просим об этом нам сообщать для верной документации. Обязательно скажи об изменениях своему руководителю "
            "и HR Юле Маликовой!"
        )
        keyboard = ReplyKeyboardMarkup(
            [["Хорошо"]],
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

    return DAY_2[16]


async def block_17(chat_id, context):
    user = await get_user_by_chat_id(chat_id)

    if user.employment_type == "Трудовой договор":
        link = await sync_to_async(
            lambda: FirstDay.objects.first().vacation_info
        )()
        text = (
            f"🏝️ Заходи по [ссылке]({link}) и "
            f"читай важную информацию про отпуск!"
        )
        keyboard = ReplyKeyboardMarkup(
            [["Классно!"]],
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
    else:
        work_reference = await sync_to_async(
            lambda: FirstDay.objects.first().work_reference_link
        )()
        text = (
            f"Если тебе нужна справка  с работы - переходи по [ссылке]({work_reference}) и "
            f"ты узнаешь как ее получить 🙌")
        keyboard = ReplyKeyboardMarkup(
            [["Удобно и понятно 😊"]],
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
    return DAY_2[17]


async def block_18(chat_id, context):
    user = await get_user_by_chat_id(chat_id)

    if user.employment_type == "Трудовой договор":
        text = (
            "Ещё немного нюансиков: Если у тебя *меняется фамилия/место жительство/ реквизиты в банке* - мы всегда "
            "просим об этом нам сообщать для верной документации. Обязательно скажи об изменениях своему руководителю "
            "и HR Юле Маликовой!"
        )
        keyboard = ReplyKeyboardMarkup(
            [["Хорошо"]],
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
    else:
        photo_url = os.path.join(settings.MEDIA_ROOT, "laptopsticker.webp")
        await context.bot.send_sticker(
            sticker=open(photo_url, 'rb'),
            chat_id=chat_id
        )
        text = (
            "Ух! Много информации сразу, понимаю. \n\n"
            "Поэтому продолжим завтра. А пока погружайся в  рабочий процесс, знакомься с коллегами и руководителем! 🗂️"
        )
        button = ReplyKeyboardRemove()
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode="Markdown",
            reply_markup=button,
        )
        return ConversationHandler.END
        # return DAY_3[0]

    return DAY_2[18]


async def block_19(chat_id, context):
    photo_url = os.path.join(settings.MEDIA_ROOT, "laptopsticker.webp")
    user = await get_user_by_chat_id(chat_id)

    if user.employment_type == "Трудовой договор":
        work_reference = await sync_to_async(
            lambda: FirstDay.objects.first().work_reference_link
        )()
        text = (
            f"Если тебе нужна справка  с работы - переходи по [ссылке]({work_reference}) и "
            f"ты узнаешь как ее получить 🙌")
        keyboard = ReplyKeyboardMarkup(
            [["Удобно и понятно 😊"]],
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
    else:
        pass
    return DAY_2[19]


async def block_20(chat_id, context):
    photo_url = os.path.join(settings.MEDIA_ROOT, "laptopsticker.webp")
    user = await get_user_by_chat_id(chat_id)

    if user.employment_type == "Трудовой договор":
        await context.bot.send_sticker(
            sticker=open(photo_url, 'rb'),
            chat_id=chat_id
        )
        text = (
            "Ух! Много информации сразу, понимаю. \n\n"
            "Поэтому продолжим завтра. А пока погружайся в  рабочий процесс, знакомься с коллегами и руководителем! 🗂️"
        )
        button = ReplyKeyboardRemove()
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode="Markdown",
            reply_markup=button,
        )
    else:
        pass
