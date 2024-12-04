from django.contrib import admin

from bot.models import TelegramUser, Code, FAQ, Category
from django.contrib.auth.models import Group, User
from django.contrib.admin.models import LogEntry


class HiddenModelAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


admin.site.register(LogEntry, HiddenModelAdmin)
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(TelegramUser)
admin.site.register(Code)
admin.site.register(FAQ)
admin.site.register(Category)
