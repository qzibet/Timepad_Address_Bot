import sys
import os
from datetime import datetime, timedelta
from django.utils import timezone
from telegram import Update
from telegram.ext import CallbackContext

from administration.models import TelegramUser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


def block_0(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    now = timezone.now()

    try:
        # Проверка, есть ли пользователь в базе и совпадает ли код доступа
        telegram_user = TelegramUser.objects.get(telegram_id=chat_id)

        # Проверка, не прошло ли время старта рассылки
        if now >= telegram_user.start_date:
            # Если пользователь вошел позже старта, добавляем сообщение
            if now > telegram_user.start_date + timedelta(days=1):
                context.bot.send_message(
                    chat_id=chat_id,
                    text="Я ждал тебя пару дней назад и подготовил контент еще до твоего первого рабочего дня. Прочитай его, пожалуйста, сейчас, так как он важный!"
                )
            # Начало рассылки с преонбординга
            send_preonboarding_messages(update, context, telegram_user)
        else:
            context.bot.send_message(chat_id=chat_id, text="Привет! Твой процесс преонбординга еще не начался.")

    except TelegramUser.DoesNotExist:
        # Если пользователя нет в базе, выводим сообщение о неверном коде
        context.bot.send_message(chat_id=chat_id, text="Неверный код доступа. Пожалуйста, введите правильный код.")


def send_preonboarding_messages(update: Update, context: CallbackContext, telegram_user: TelegramUser):
    # Логика отправки преонбординговых сообщений
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Добро пожаловать в преонбординг! Вот ваше первое сообщение."
    )
    # Помечаем, что преонбординг начался
    telegram_user.preonboarding_started = True
    telegram_user.save()

