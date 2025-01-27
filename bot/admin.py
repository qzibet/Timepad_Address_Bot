from django.contrib import admin

from bot.models import (
    TelegramUser,
    Code, FAQ,
    PreonbordingLinks,
    FirstDay, SecondDay,
    FourthDay, MonthHalf,
    ThirdMonth, SecondMonth, UserConversationState
)
from django.contrib.auth.models import Group, User
from django.contrib.admin.models import LogEntry
from solo.admin import SingletonModelAdmin


@admin.register(PreonbordingLinks)
class PreonbordingLinksAdmin(SingletonModelAdmin):
    pass


@admin.register(FirstDay)
class FirstDayAdmin(SingletonModelAdmin):
    pass


@admin.register(SecondDay)
class SecondDayAdmin(SingletonModelAdmin):
    pass


@admin.register(FourthDay)
class FourthDayAdmin(SingletonModelAdmin):
    pass


@admin.register(MonthHalf)
class MonthHalfAdmin(SingletonModelAdmin):
    pass


@admin.register(SecondMonth)
class SecondMonthAdmin(SingletonModelAdmin):
    pass


@admin.register(ThirdMonth)
class ThirdMonthAdmin(SingletonModelAdmin):
    pass


class HiddenModelAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


admin.site.register(LogEntry, HiddenModelAdmin)
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(TelegramUser)
admin.site.register(Code)
admin.site.register(FAQ)

