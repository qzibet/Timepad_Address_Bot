import asyncio
import logging
import os

from asgiref.sync import sync_to_async

from bot.handlers.conversations_states import DAY_1, DAY_2, DAY_3, DAY_4, DAY_5, DAY_6, MONTH_1, MONTH_2, MONTH_3
from bot.handlers import preonbording, day_of_work, day_2, day_3, day_4, day_5, month_1, month_2, month_3
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, JobQueue, \
    CallbackQueryHandler
from bot.handlers.faq import faq, handle_callback_query, support, wallet
from bot.models import Code

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self):
        asyncio.run(self.initialize_bot())

    async def initialize_bot(self):
        self.token = os.getenv("TOKEN")
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
                DAY_1[9]: [MessageHandler(filters.TEXT & ~filters.COMMAND, preonbording.block_10)],
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
                DAY_2[17]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_18)],
                DAY_2[18]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_19)],
                DAY_2[19]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_of_work.block_20)],
                DAY_3[0]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_1)],
                DAY_3[1]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_2)],
                DAY_3[2]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_3)],
                DAY_3[3]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_4)],
                DAY_3[4]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_5)],
                DAY_3[5]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_6)],
                DAY_3[6]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_7)],
                DAY_3[7]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_8)],
                DAY_3[8]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_9)],
                DAY_3[9]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_10)],
                DAY_3[10]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_11)],
                DAY_3[11]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_12)],
                DAY_3[12]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_13)],
                DAY_3[13]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_14)],
                DAY_3[14]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_15)],
                DAY_3[15]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_16)],
                DAY_3[16]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_17)],
                DAY_3[17]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_18)],
                DAY_3[18]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_19)],
                DAY_3[19]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_20)],
                DAY_3[20]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_21)],
                DAY_3[21]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_22)],
                DAY_3[22]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_2.block_23)],
                DAY_4[0]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_3.block_1)],
                DAY_4[1]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_3.block_2)],
                DAY_4[2]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_3.block_3)],
                DAY_4[3]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_3.block_4)],
                DAY_5[0]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_4.block_1)],
                DAY_5[1]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_4.block_2)],
                DAY_5[2]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_4.block_3)],
                DAY_5[3]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_4.block_4)],
                DAY_5[4]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_4.block_5)],
                DAY_5[5]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_4.block_6)],
                DAY_5[6]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_4.block_7)],
                DAY_5[7]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_4.block_8)],
                DAY_5[8]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_4.block_9)],
                DAY_5[9]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_4.block_10)],
                DAY_5[10]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_4.block_11)],
                DAY_5[11]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_4.block_12)],
                DAY_5[12]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_4.block_13)],
                DAY_5[13]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_4.block_14)],
                DAY_6[0]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_5.block_1)],
                DAY_6[1]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_5.block_2)],
                DAY_6[2]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_5.block_3)],
                DAY_6[3]: [MessageHandler(filters.TEXT & ~filters.COMMAND, day_5.block_4)],
                MONTH_1[0]: [MessageHandler(filters.TEXT & ~filters.COMMAND, month_1.block_1)],
                MONTH_1[1]: [MessageHandler(filters.TEXT & ~filters.COMMAND, month_1.block_2)],
                MONTH_1[2]: [MessageHandler(filters.TEXT & ~filters.COMMAND, month_1.block_3)],
                MONTH_1[3]: [MessageHandler(filters.TEXT & ~filters.COMMAND, month_2.block_0)],
                MONTH_2[0]: [MessageHandler(filters.TEXT & ~filters.COMMAND, month_2.block_1)],
                MONTH_2[1]: [MessageHandler(filters.TEXT & ~filters.COMMAND, month_2.block_2)],
                MONTH_2[2]: [MessageHandler(filters.TEXT & ~filters.COMMAND, month_2.block_3)],
                MONTH_2[3]: [MessageHandler(filters.TEXT & ~filters.COMMAND, month_2.block_4)],
                MONTH_2[4]: [MessageHandler(filters.TEXT & ~filters.COMMAND, month_3.block_0)],
                MONTH_3[0]: [MessageHandler(filters.TEXT & ~filters.COMMAND, month_3.block_1)],
                MONTH_3[1]: [MessageHandler(filters.TEXT & ~filters.COMMAND, month_3.block_2)],
                MONTH_3[2]: [MessageHandler(filters.TEXT & ~filters.COMMAND, month_3.block_3)],
                MONTH_3[3]: [MessageHandler(filters.TEXT & ~filters.COMMAND, month_3.block_4)],

            },
            fallbacks=[CommandHandler("start", preonbording.start)],  # Обработчик для повторного вызова команды /start
        )

        self.application.add_handler(conversation_handler)
        self.application.add_handler(CommandHandler("faq", faq))
        self.application.add_handler(CommandHandler("help", support))
        self.application.add_handler(CommandHandler("wallet", wallet))

        self.application.add_handler(CallbackQueryHandler(handle_callback_query))  # Обработчик для кнопок
        #
        # await self.schedule_daily_tasks()

    @sync_to_async
    def get_user_code(self, user_id):
        return Code.objects.filter(user__chat_id=user_id).first()

    # async def schedule_daily_tasks(self):
    #     codes = await sync_to_async(list)(
    #         Code.objects.filter(start_date__isnull=False)
    #     )
    #
    #     for code in codes:
    #         start_time = make_aware(
    #             datetime.combine(
    #                 code.start_date, time(10, 0)
    #             )
    #         )
    #         current_time = make_aware(datetime.now())
    #
    #         if start_time > current_time:
    #             self.job_queue.run_once(
    #                 self.start_day_2,
    #                 when=(start_time - current_time).total_seconds(),
    #                 data=code.user
    #             )


    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.initialize_bot())
        self.application.run_polling(timeout=60)

