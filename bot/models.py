from django.db import models


class TelegramUser(models.Model):
    name = models.CharField(
        max_length=120,
        verbose_name="имя",
        null=True, blank=True
    )
    username = models.CharField(
        max_length=120,
        verbose_name="никнейм",
        unique=True
    )
    chat_id = models.CharField(
        max_length=120,
        verbose_name="chat_id чтобы запомнить при выходе",
        unique=True
    )
    work_type = models.CharField(
        max_length=50,
        verbose_name="Тип работы",
        null=True, blank=True
    )
    timepad = models.IntegerField(
        verbose_name="количество таймпадов",
        default=0,
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Code(models.Model):
    code = models.CharField(
        max_length=12,
        unique=True,
        verbose_name="код доступа"
    )
    user = models.OneToOneField(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name="code",
        null=True, blank=True,
        max_length="пользователь"
    )
    start_date = models.DateField(verbose_name="дата начала")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Код доступа"
        verbose_name_plural = "Коды доступа"


class Video(models.Model):
    video = models.FileField(upload_to='videos/')
    number = models.IntegerField()

    def __str__(self):
        return f"Video {self.number}"
