from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async

from bot.models import Category, FAQ


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
            text = "\n\n".join([f"- {faq.post}" for faq in faqs])
            await query.edit_message_text(text=f"Посты в категории:\n\n{text}", disable_web_page_preview=True)
        else:
            await query.edit_message_text(text="Нет постов в этой категории.")

