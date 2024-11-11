from django.contrib import admin

from bot.models import TelegramUser, Code, Video

admin.site.register(TelegramUser)
admin.site.register(Code)
admin.site.register(Video)
