import os

from django.conf import settings
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async
from PIL import Image, ImageDraw, ImageFont

from bot.models import FAQ, TelegramUser

import re
from html import escape


def process_text_with_clickable_links(text: str) -> str:
    """
    Обрабатывает текст, удаляет Markdown-гиперссылки, оставляя кликабельные ссылки.
    """
    # Преобразовать Markdown-ссылки в HTML-ссылки
    def replace_link(match):
        link_text = match.group(1)
        link_url = match.group(2)
        return f'<a href="{escape(link_url)}">{escape(link_text)}</a>'

    text = re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)', replace_link, text)

    # Заменить типографические символы для лучшей читаемости
    text = text.replace("“", '"').replace("”", '"').replace("«", '"').replace("»", '"')
    text = text.replace("—", "-").replace("–", "-")
    return text


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    faqs = await sync_to_async(lambda: list(FAQ.objects.all()))()
    keyboard = []

    for faq in faqs:
        if faq.post:
            keyboard.append([InlineKeyboardButton(faq.name, url=faq.post)])
        elif faq.file:
            keyboard.append([InlineKeyboardButton(faq.name, callback_data=f"faq_file_{faq.id}")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text="Выберите нужный раздел:",
        reply_markup=reply_markup
    )


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("faq_file_"):
        faq_id = int(query.data.split("_")[-1])

        faq = await sync_to_async(lambda: FAQ.objects.filter(id=faq_id).first())()

        if faq and faq.file:
            await query.message.reply_photo(
                photo=faq.file,
            )
        else:
            await query.message.reply_text("Файл не найден.")


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Лови контакты тех.поддержки: @devurfut"
    )
    button = ReplyKeyboardRemove()
    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=button,
        disable_web_page_preview=True
    )


async def get_user_by_chat_id(chat_id):
    return await sync_to_async(TelegramUser.objects.get)(chat_id=chat_id)


async def save_user(user):
    await sync_to_async(user.save)()


async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = await get_user_by_chat_id(chat_id)
    user_timepad = user.timepad

    # Путь к исходному изображению
    original_image_path = os.path.join(settings.MEDIA_ROOT, "walletsticker.webp")

    # Открытие изображения
    with Image.open(original_image_path) as img:
        # Определение размеров оригинального изображения
        img_width, img_height = img.size

        # Установка шрифта
        font_path = os.path.join(settings.MEDIA_ROOT, "Gamilia-Regular.otf")  # Замените на реальный путь

        # Начинаем с базового размера шрифта
        base_font_size = 150
        font = ImageFont.truetype(font_path, size=base_font_size)
        text = str(user_timepad)

        # Автоматическая подгонка размера шрифта под высоту изображения
        while True:
            text_width, text_height = font.getsize(text)
            if text_height >= img_height:  # Если текст слишком большой
                base_font_size -= 1
                font = ImageFont.truetype(font_path, size=base_font_size)
            else:
                break

        # Создание нового изображения с увеличенной шириной для текста
        new_width = img_width + text_width + 50  # Дополнительное место для текста
        new_height = img_height  # Высота остаётся как у оригинального изображения
        new_img = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))

        # Копирование оригинального изображения в новое
        new_img.paste(img, (0, 0))

        # Позиция текста (справа от изображения)
        position = (img_width + 20, (new_height - text_height) // 2)

        # Добавление текста
        draw = ImageDraw.Draw(new_img)
        draw.text(position, text, fill="white", font=font)

        # Сохранение обработанного изображения во временный файл
        modified_image_path = os.path.join(settings.MEDIA_ROOT, "modified_walletsticker.webp")
        new_img.save(modified_image_path, "WEBP")

    # Отправка изображения как стикера
    with open(modified_image_path, 'rb') as sticker_file:
        await update.message.reply_sticker(
            sticker=sticker_file,
            write_timeout=120,
            pool_timeout=120,
            read_timeout=120,
            connect_timeout=120
        )

    # Очистка клавиатуры (если нужно)
    button = ReplyKeyboardRemove()

