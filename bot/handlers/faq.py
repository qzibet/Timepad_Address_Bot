from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async

from bot.models import Category, FAQ

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
