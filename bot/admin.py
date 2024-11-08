from django.contrib import admin

from bot.models import TelegramUser, Code

admin.site.register(TelegramUser)
admin.site.register(Code)
