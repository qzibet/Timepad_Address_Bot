import asyncio
from functools import partial

import pytz
from datetime import datetime, timedelta, date

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, JobQueue
from telegram.ext import ContextTypes, CallbackContext

from bot.handlers import day_of_work, day_2, day_3, day_4, day_5, month_1, month_2, month_3
from asgiref.sync import sync_to_async

from bot.handlers.conversations_states import DAY_2, DAY_3, DAY_4, DAY_5, DAY_6, MONTH_1, MONTH_2, MONTH_3
from bot.models import TelegramUser, UserConversationState

AWAITING_NEXT = range(9999)

DAY_FUNCTIONS = {
    1: day_of_work.block_0,
    2: day_2.block_0,
    3: day_3.block_0,
    4: day_4.block_0,
    5: day_5.block_0,
    30: month_1.block_0,
    60: month_2.block_0,
    90: month_3.block_0,
}

STATE = {
    1: DAY_2[0],
    2: DAY_3[0],
    3: DAY_4[0],
    4: DAY_5[0],
    5: DAY_6[0],
    30: MONTH_1[0],
    60: MONTH_2[0],
    90: MONTH_3[0]
}

DAY_BLOCKS = {
    1: [
        day_of_work.block_0,
        day_of_work.block_1,
        day_of_work.block_2,
        day_of_work.block_3,
        day_of_work.block_4,
        day_of_work.block_5,
        day_of_work.block_6,
        day_of_work.block_7,
        day_of_work.block_8,
        day_of_work.block_9,
        day_of_work.block_10,
        day_of_work.block_11,
        day_of_work.block_12,
        day_of_work.block_13,
        day_of_work.block_14,
        day_of_work.block_15,
        day_of_work.block_16,
        day_of_work.block_17,
        day_of_work.block_18,
        day_of_work.block_19,
        day_of_work.block_20,
    ],
    2: [
        day_2.block_0,
        day_2.block_1,
        day_2.block_3,
        day_2.block_4,
        day_2.block_5,
        day_2.block_6,
        day_2.block_7,
        day_2.block_8,
        day_2.block_9,
        day_2.block_10,
        day_2.block_11,
        day_2.block_12,
        day_2.block_13,
        day_2.block_14,
        day_2.block_15,
        day_2.block_16,
        day_2.block_17,
        day_2.block_18,
        day_2.block_19,
        day_2.block_20,
        day_2.block_21,
        day_2.block_22,
        day_2.block_23
    ],
    3: [
        day_3.block_0,
        day_3.block_1,
        day_3.block_3,
        day_3.block_4,
    ],
    4: [
        day_4.block_0,
        day_4.block_1,
        day_4.block_3,
        day_4.block_4,
        day_4.block_5,
        day_4.block_6,
        day_4.block_7,
        day_4.block_8,
        day_4.block_9,
        day_4.block_10,
        day_4.block_11,
        day_4.block_12,
        day_4.block_13,
        day_4.block_14,
    ],
    5: [
        day_5.block_0,
        day_5.block_1,
        day_5.block_3,
        day_5.block_4,
    ],
    45: [
        month_1.block_0,
        month_1.block_1,
        month_1.block_2,
        month_1.block_3,
    ],
    60: [
        month_2.block_0,
        month_2.block_1,
        month_2.block_2,
        month_2.block_3,
        month_2.block_4
    ],
    90: [
        month_3.block_0,
        month_3.block_1,
        month_3.block_2,
        month_3.block_3,
        month_3.block_4,
    ],

}


def count_business_days(start_date, end_date):
    if start_date > end_date:
        return 0
    day_count = 0
    current_day = start_date
    while current_day <= end_date:
        if current_day.weekday() < 5:  # Пн–Пт
            day_count += 1
        current_day += timedelta(days=1)
    return day_count


async def daily_alarm(context: CallbackContext):
    print("daily_alarm запущен")

    moscow_tz = pytz.timezone("Europe/Moscow")
    today = datetime.now(moscow_tz).date()

    # Если сегодня суббота (5) или воскресенье (6), ничего не отправляем
    if today.weekday() >= 5:
        print("Сегодня выходной, рассылка не выполняется.")
        return

    users = await sync_to_async(
        lambda: list(
            TelegramUser.objects.select_related("code").filter(
                code__isnull=False
            ).exclude(code__start_date__isnull=True)
        )
    )()

    print("Пользователи извлечены")

    if not users:
        return

    for user in users:
        start_date = user.code.start_date
        if not start_date:
            continue

        # Считаем, сколько рабочих дней прошло
        business_days_elapsed = count_business_days(start_date, today)

        # Если за все время прошедших рабочих дней меньше 1, то день ещё не настал
        if business_days_elapsed < 1:
            continue

        # Список нужных "контрольных" дней (по бизнес-логике)
        periods = [1, 2, 3, 4, 5, 45, 60, 90]

        # Если этот "рабочий день" входит в нужные периоды — отправляем первый блок
        if business_days_elapsed in periods:
            day_blocks = DAY_BLOCKS.get(business_days_elapsed)
            chat_id = user.chat_id
            print(
                f"Отправляем контент пользователю {user.username} в чат {chat_id}, business_days_elapsed={business_days_elapsed}")

            if day_blocks:
                try:
                    block_func = day_blocks[0]
                    print(f"Выполняем block_0 для пользователя {user.username}")
                    await block_func(chat_id, context)

                    # Сохраняем состояние
                    await sync_to_async(
                        UserConversationState.objects.update_or_create,
                        thread_sensitive=True
                    )(
                        user=user,
                        defaults={
                            "chat_id": chat_id,
                            "state": f"DAY_{business_days_elapsed}[BLOCK_0]"
                        }
                    )
                    print(f"Состояние обновлено для пользователя {user.username}: DAY_{business_days_elapsed}[BLOCK_0]")

                except Exception as e:
                    print(f"Ошибка для пользователя {user.username}: {e}")


def sync_wrapper(func, *args, **kwargs):
    """Обёртка для запуска асинхронных функций."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(func(*args, **kwargs))


async def handle_user_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_response = update.message.text

    # Получаем пользователя
    user = await sync_to_async(lambda: TelegramUser.objects.get(chat_id=chat_id))()

    # Получаем текущее состояние пользователя
    try:
        user_state = await sync_to_async(lambda: UserConversationState.objects.get(user=user))()
    except UserConversationState.DoesNotExist:
        # await context.bot.send_message(chat_id=chat_id, text="Неизвестное состояние. Пожалуйста, начните сначала.")
        print()
        return

    # Разбор состояния
    try:
        state_parts = user_state.state.strip("]").split("[")  # Разделяем строку по "["
        current_day = state_parts[0].replace("DAY_", "")  # Получаем текущий день
        current_block = state_parts[1].replace("BLOCK_", "")  # Получаем текущий блок
    except (IndexError, ValueError) as e:
        await context.bot.send_message(chat_id=chat_id, text="Некорректное состояние. Пожалуйста, начните сначала.")
        print(f"Ошибка разбора состояния пользователя {user.username}: {e}")
        return

    try:
        current_day = int(current_day)
        current_block_index = int(current_block)
    except ValueError as e:
        await context.bot.send_message(chat_id=chat_id, text="Некорректное состояние. Пожалуйста, начните сначала.")
        print(f"Ошибка преобразования состояния пользователя {user.username}: {e}")
        return

    # Получаем блоки дня
    day_blocks = DAY_BLOCKS.get(current_day)
    if not day_blocks:
        await context.bot.send_message(chat_id=chat_id, text="Блоки дня не найдены. Пожалуйста, начните сначала.")
        return

    # Обработка блока 11 для сохранения выбора пользователя
    if current_day == 1 and current_block_index == 11:
        user_choice = user_response.strip()  # Получаем выбор пользователя
        if user_choice in ["Трудовой договор", "Иная форма"]:
            user.employment_type = user_choice
            await sync_to_async(user.save)()  # Сохраняем выбор в TelegramUser
            print(f"Выбор сохранён для пользователя {user.username}: {user_choice}")
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Пожалуйста, выбери один из предложенных вариантов: 'Трудовой договор' или 'Иная форма'.",
            )
            return

    if current_day == 2 and current_block_index == 6:
        user_choice = user_response.strip()  # Получаем выбор пользователя
        if user_choice in ["🖼", "🌳", "✈️"]:
            user.emodji = user_choice
            await sync_to_async(user.save)()  # Сохраняем выбор в TelegramUser
            print(f"Выбор сохранён для пользователя {user.username}: {user_choice}")
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Пожалуйста, выбери один из предложенных вариантов: '🖼', '🌳', '✈️' ",
            )
            return

    if current_day == 3 and current_block_index == 0:
        user_choice = user_response.strip()  # Получаем выбор пользователя
        if user_choice in ["Супер!", "Хорошее", "Так себе", "Плохое"]:
            user.mood_third_day = user_choice
            await sync_to_async(user.save)()  # Сохраняем выбор в TelegramUser
            print(f"Выбор сохранён для пользователя {user.username}: {user_choice}")
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Пожалуйста, выбери один из предложенных вариантов: 'Трудовой договор' или 'Иная форма'.",
            )
            return

    if current_day == 60 and current_block_index == 1:
        user_choice = user_response.strip()  # Получаем выбор пользователя
        if user_choice in ["Все прекрасно!", "Норм", "Ну, такое", "Совсем не очень"]:
            user.mood_second_month = user_choice
            await sync_to_async(user.save)()  # Сохраняем выбор в TelegramUser
            print(f"Выбор сохранён для пользователя {user.username}: {user_choice}")
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Пожалуйста, выбери один из предложенных вариантов: 'Трудовой договор' или 'Иная форма'.",
            )
            return

    # Проверяем, есть ли следующий блок
    if current_block_index + 1 < len(day_blocks):
        context.user_data['last_response'] = user_response.strip()

        next_block_func = day_blocks[current_block_index + 1]

        # Выполняем следующий блок
        print(f"Выполняем block_{current_block_index + 1} для пользователя {user.username}")
        next_block = await next_block_func(chat_id, context)

        # Обновляем состояние пользователя
        await sync_to_async(
            UserConversationState.objects.update_or_create,
            thread_sensitive=True
        )(
            user=user,
            defaults={
                "chat_id": chat_id,
                "state": f"DAY_{current_day}[BLOCK_{current_block_index + 1}]"  # Следующий блок
            }
        )
        print(f"Состояние обновлено для пользователя {user.username}: DAY_{current_day}[BLOCK_{current_block_index + 1}]")
    else:
        print(f"Все блоки для пользователя {user.username} завершены")
        await sync_to_async(UserConversationState.objects.filter(user=user).delete)()
