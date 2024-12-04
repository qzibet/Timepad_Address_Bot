import os

from django.conf import settings
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async
from PIL import Image, ImageDraw, ImageFont

from bot.models import Category, FAQ, TelegramUser

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
    """Обработчик команды /faq."""
    categories = await sync_to_async(list)(Category.objects.all())
    keyboard = [
        [InlineKeyboardButton(category.name, callback_data=f"category_{category.id}")]
        for category in categories
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите категорию:", reply_markup=reply_markup)


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора категории."""
    query = update.callback_query
    await query.answer()

    if query.data.startswith("category_"):
        category_id = int(query.data.split("_")[1])
        faqs = await sync_to_async(list)(FAQ.objects.filter(category_id=category_id))
        if faqs:
            processed_faqs = [
                f"- {process_text_with_clickable_links(faq.post)}" for faq in faqs
            ]
            text = "\n\n".join(processed_faqs)
            await query.edit_message_text(
                text=f"{text}",
                parse_mode="HTML",  # Используем HTML
                disable_web_page_preview=True
            )
        else:
            await query.edit_message_text(
                text="Нет постов в этой категории.",
                parse_mode="HTML"
            )


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Лови контакты тех.поддержки: @fruktstyle"
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

        # Определяем оптимальный размер шрифта, чтобы цифра вписалась в высоту изображения
        base_font_size = 150
        font = ImageFont.truetype(font_path, size=base_font_size)
        text = str(user_timepad)

        # Снижение размера шрифта для соответствия высоте изображения
        text_width, text_height = font.getsize(text)
        while text_height > img_height * 0.9:  # 90% высоты изображения
            base_font_size -= 5
            font = ImageFont.truetype(font_path, size=base_font_size)
            text_width, text_height = font.getsize(text)

        # Создание нового изображения с увеличенной шириной для текста
        new_width = img_width + text_width + 50  # Дополнительное место для текста
        new_height = max(img_height, text_height)  # Новая высота равна максимальной из двух
        new_img = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))

        # Копирование оригинального изображения в новое
        new_img.paste(img, (0, (new_height - img_height) // 2))

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
