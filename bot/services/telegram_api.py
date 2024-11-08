import asyncio
import logging

from asgiref.sync import sync_to_async

from bot.handlers.conversations_states import DAY_1, DAY_2
from bot.handlers import preonbording, day_of_work
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, JobQueue
from datetime import datetime, time, timedelta
from django.utils.timezone import make_aware

from bot.models import Code

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self):
        asyncio.run(self.initialize_bot())

    async def initialize_bot(self):
        self.token = "7437555334:AAHUo2Pwo5Hy9P3q0-2qIjT7sxCK5IWlcTs"
        self.application = Application.builder().token(self.token).build()
        self.job_queue = JobQueue()
        self.job_queue.set_application(self.application)
        await self.job_queue.start()
        await self.add_handlers()

    async def add_handlers(self):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler("start", preonbording.start)],  # Обработчик для команды /start
            states={
                DAY_1[0]: [MessageHandler(filters.Regex("^Юхуу, погнали$") & ~filters.COMMAND, preonbording.ask_for_code)],
                DAY_1[1]: [MessageHandler(filters.TEXT & ~filters.COMMAND, preonbording.request_access_code)],
                DAY_1[2]: [MessageHandler(filters.TEXT & ~filters.COMMAND, preonbording.request_name)],
                DAY_1[3]: [MessageHandler(filters.TEXT & ~filters.COMMAND, preonbording.save_name)],
                DAY_1[4]: [MessageHandler(filters.TEXT & ~filters.COMMAND, preonbording.block_5)],
                DAY_1[5]: [MessageHandler(filters.TEXT & ~filters.COMMAND, preonbording.block_6)],
                DAY_1[6]: [MessageHandler(filters.TEXT & ~filters.COMMAND, preonbording.block_7)],
                DAY_1[7]: [MessageHandler(filters.TEXT & ~filters.COMMAND, preonbording.block_8)],
                DAY_1[8]: [MessageHandler(filters.TEXT & ~filters.COMMAND, preonbording.block_9)],
                DAY_2[0]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_1)],
                DAY_2[1]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_2)],
                DAY_2[2]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_3)],
                DAY_2[3]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_4)],
                DAY_2[4]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_5)],
                DAY_2[5]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_6)],
                DAY_2[6]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_7)],
                DAY_2[7]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_8)],
                DAY_2[8]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_9)],
                DAY_2[9]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_10)],
                DAY_2[10]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_11)],
                DAY_2[11]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_12)],
                DAY_2[12]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_13)],
                DAY_2[13]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_14)],
                DAY_2[14]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_15)],
                DAY_2[15]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_16)],
                DAY_2[16]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_17)],
                DAY_2[17]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_17)],
            },
            fallbacks=[CommandHandler("start", preonbording.start)],  # Обработчик для повторного вызова команды /start
        )

        self.application.add_handler(conversation_handler)
        await self.schedule_daily_tasks()

    @sync_to_async
    def get_user_code(self, user_id):
        return Code.objects.filter(user__chat_id=user_id).first()

    async def schedule_daily_tasks(self):
        codes = await sync_to_async(list)(
            Code.objects.filter(start_date__isnull=False)
        )

        for code in codes:
            start_time = make_aware(
                datetime.combine(
                    code.start_date, time(10, 0)
                )
            )
            current_time = make_aware(datetime.now())

            if start_time > current_time:
                self.job_queue.run_once(
                    self.start_day_2,
                    when=(start_time - current_time).total_seconds(),
                    data=code.user
                )

    def start_day_2(self, context):
        user = context.job.data
        day_of_work.block_0(user, context)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.initialize_bot())
        self.application.run_polling(timeout=60)

