from django.contrib import admin

from bot.models import TelegramUser, Code, Video, FAQ, Category

admin.site.register(TelegramUser)
admin.site.register(Code)
admin.site.register(Video)
admin.site.register(FAQ)
admin.site.register(Category)
