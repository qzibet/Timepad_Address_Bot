from django.db import models
from solo.models import SingletonModel


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
        verbose_name="Количество таймпадов",
        default=0, null=True, blank=True
    )
    mood_third_day = models.CharField(
        max_length=50,
        verbose_name="Настроение на 3 день",
        null=True, blank=True
    )
    mood_second_month = models.CharField(
        max_length=50,
        verbose_name="Настроение через 2 месяца",
        null=True, blank=True
    )
    employment_type = models.CharField(
        max_length=50,
        verbose_name="Форма взаимодействия",
        null=True, blank=True
    )
    buddy = models.CharField(
        max_length=50,
        verbose_name="Бадди",
        null=True, blank=True
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Управление пользователями"
        verbose_name_plural = "Управление пользователями"


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
    start_date = models.DateField(verbose_name="Дата первого рабочего дня")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Код доступа"
        verbose_name_plural = "Коды доступа"


class FAQ(models.Model):
    name = models.TextField(verbose_name="Название")
    post = models.URLField(verbose_name="ссылка", null=True, blank=True)
    file = models.FileField(verbose_name="файл", null=True, blank=True, upload_to='uploads/',)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "База знаний"
        verbose_name_plural = "База знаний"


class PreonbordingLinks(SingletonModel):
    acquaintance = models.URLField(
        verbose_name="форма для знакомства",
        null=True, blank=True,
    )
    emails = models.CharField(
        verbose_name="почтовые адреса для оформления документов",
        null=True, blank=True,
    )
    address = models.URLField(
        verbose_name="адрес офиса (ссылка на yandex map)",
        null=True, blank=True,
    )

    def __str__(self):
        return "Преонбординг"

    class Meta:
        verbose_name = "Преонбординг"
        abstract = False


class FirstDay(SingletonModel):
    link_zoom = models.URLField(
        verbose_name="ссылка на встречу в ZOOM!",
        null=True, blank=True,
    )
    link_event_group = models.URLField(
        verbose_name="ссылка на Канал события",
        null=True, blank=True,
    )
    link_offtop_timepad = models.URLField(
        verbose_name="ссылка на Offtop Timepad",
        null=True, blank=True,
    )
    link_admin = models.CharField(
        verbose_name="контакт админа Барахолка и свопы",
        null=True, blank=True, max_length=25
    )
    link_eva = models.URLField(
        verbose_name="ссылка на чат Ева",
        null=True, blank=True,
    )
    logo_link = models.URLField(
        verbose_name="Ссылка на логотип",
        null=True, blank=True,
    )
    system_admin = models.CharField(
        verbose_name="контакт сис.админа",
        null=True, blank=True, max_length=25,
        default="@woolycrypticboy"
    )
    link_byod = models.URLField(
        verbose_name="Ссылка на BYOD",
        null=True, blank=True,
    )
    hr_documentation_contact = models.CharField(
        verbose_name="Контакт ответственного за кадровый документооборот",
        max_length=55,
        null=True, blank=True,
    )
    payroll_contact = models.CharField(
        verbose_name="Контакт ответственного за зарплату",
        max_length=255,
        null=True, blank=True,
    )
    hr_contact = models.CharField(
        verbose_name="Контакт hr",
        max_length=255,
        null=True, blank=True,
        default="@malikovaj"
    )
    interface_link = models.URLField(
        verbose_name="Ссылка на интерфейс для сотрудников",
        null=True, blank=True,
    )
    vacation_info = models.URLField(
        verbose_name="Ссылка на информацию про отпуск",
        null=True, blank=True,
    )
    freelance_vacation = models.URLField(
        verbose_name="Ссылка на информацию про отпуск(для внештатных)",
        null=True, blank=True,
    )
    avatar_images_link = models.URLField(
        verbose_name="Ссылка на скачивание картинок аватарок",
        null=True, blank=True,
    )
    work_reference_link = models.URLField(
        verbose_name="Ссылка на справку с работы",
        null=True, blank=True,
    )

    def __str__(self):
        return "1 рабочий день"

    class Meta:
        verbose_name = "1 рабочий день"
        abstract = False


class SecondDay(SingletonModel):
    link_afisha_group = models.URLField(
        verbose_name="Ссылка на афишу",
        null=True, blank=True,
    )
    art_branches_link = models.URLField(
        verbose_name="Ссылка на статью о арт-бранчах",
        null=True, blank=True,
    )
    forest_escapes_link = models.URLField(
        verbose_name="Ссылка на статью о лесных экотопах",
        null=True, blank=True,
    )
    travel_link = models.URLField(
        verbose_name="Ссылка на статью о путешествиях",
        null=True, blank=True,
    )
    tg_channel_weekends = models.CharField(
        verbose_name="Ссылка на TG-канал 'Спасите мои выходные'",
        max_length=255,
        default="@TimepadRU",
        null=True, blank=True,
    )
    tg_channel_paradnaya = models.CharField(
        verbose_name="Ссылка на TG-канал 'Спасите мои парадные'",
        max_length=255,
        default="@Timepadru_spb",
        null=True, blank=True,
    )
    vk_link = models.URLField(
        verbose_name="Ссылка на ВКонтакте",
        default="https://vk.com/timepadru",
        null=True, blank=True,
    )
    instagram_link = models.URLField(
        verbose_name="Ссылка на Инстаграм",
        default="https://www.instagram.com/timepad.ru",
        null=True, blank=True,
    )
    podcast_save_my_weekend = models.URLField(
        verbose_name='Ссылка на подкаст "Спасите мои выходные" с Варей Семенихиной',
        default="https://savemyweekend.mave.digital",
        null=True, blank=True,
    )
    podcast_tochno_idem = models.URLField(
        verbose_name='Ссылка на подкаст "Точно идем"',
        default="https://tochnoidem.mave.digital",
        null=True, blank=True,
    )
    development_director_contact = models.CharField(
        verbose_name="Контакт директора по развитию билетного бизнеса",
        max_length=25,
        default="@darialvistner",
        null=True, blank=True,
    )
    marketing_director_contact = models.CharField(
        verbose_name="Контакт руководителя отдела маркетинга",
        max_length=55,
        default="@dasha_gaydukova",
        null=True, blank=True,
    )
    smm_specialist_contact = models.CharField(
        verbose_name="Контакт СММщицы",
        max_length=255,
        default="@marypopossa",
    )
    advertising_director_contact = models.CharField(
        verbose_name="Контакт руководителя отдела рекламы",
        max_length=255,
        default="@azamorkvasov",
    )

    def __str__(self):
        return "2 рабочий день"

    class Meta:
        verbose_name = "2 рабочий день"
        abstract = False


class FourthDay(SingletonModel):
    corporate_discounts_link = models.URLField(
        verbose_name="Ссылка на страницу с корпоративными скидками",
        default="https://telegra.ph/Bonusy-i-partnerskie-skidki-11-14",
    )
    birthday_form_link = models.URLField(
        verbose_name="Ссылка на форму ДР",
        default="https://telegra.ph/Bonusy-i-partnerskie-skidki-11-14",
    )
    account_manager_contact = models.CharField(
        verbose_name="Контакт аккаунт-менеджера отдела развития",
        max_length=25,
        default="@vi_litvinova",
    )
    photo_link = models.URLField(
        verbose_name="Ссылка фотографии",
        default="https://drive.google.com/drive/u/1/folders/1kg8bYqISsnXgyKltrnZGRZBqrZ6T8gNn",
    )
    survey_link = models.URLField(
        verbose_name="Ссылка на анкету",
        default="https://docs.google.com/forms/d/e/1FAIpQLSfw1RFDwUod-F868-9MzN9VuJ-8CVD9T---I-RW_-ue5C6WuA/viewform",
    )
    event_recordings_and_presentations_link = models.URLField(
        verbose_name="Ссылка на записи и презентации мероприятий",
        default="https://www.notion.so/42d7ebd5335844e2afacbb1c6f0c061a?pvs=21",
    )
    corporate_events_link = models.URLField(
        verbose_name="Ссылка на корпоративные мероприятия",
        default="https://www.notion.so/4c1bcbf52bef458c8b5af800e94c8871?pvs=2",
    )
    ice_rink_link = models.URLField(
        verbose_name="Ссылка на канал про каток",
        default="https://t.me/+x2m0Ry7AU3cwODEy",
    )
    sup_link = models.URLField(
        verbose_name="Ссылка на канал про сапы",
        default="https://t.me/+XJlZ1_sJTKllZjQ6",
    )
    karaoke_link = models.URLField(
        verbose_name="Ссылка на канал про караоке",
        default="https://t.me/+WTlTv0-Tym0zNjUy",
    )
    humor_and_mishaps_link = models.URLField(
        verbose_name="Ссылка на канал Смех и грех",
        default="https://t.me/+aVrcvXCmZWcxYTMy",
    )
    dms_link = models.URLField(
        verbose_name="Ссылка на ДМС",
        default="https://timepaddev.notion.site",
    )

    def __str__(self):
        return "4 рабочий день"

    class Meta:
        verbose_name = "4 рабочий день"
        abstract = False


class MonthHalf(SingletonModel):
    survey_link = models.URLField(
        verbose_name="Ссылка на анкету",
        default="https://docs.google.com/forms/d/e/1FAIpQLScEQfKbumuqSd_3DeR1WDtQJUt5fYvUQEnGFJWgqXLmm9MLyQ/viewform",
    )

    def __str__(self):
        return "1,5 месяц"

    class Meta:
        verbose_name = "1,5 месяц"
        abstract = False


class SecondMonth(SingletonModel):
    hr_link = models.URLField(
        verbose_name="Ссылка на встречу",
        default="https://us02web.zoom.us/j/86826507585?pwd=qmo2josZPIVmEJzV8cnrd3FRKlIjl7.1",
    )

    def __str__(self):
        return "2 месяц"

    class Meta:
        verbose_name = "2 месяц"
        abstract = False


class ThirdMonth(SingletonModel):
    meet_link = models.URLField(
        verbose_name="Ссылка на встречу",
        default="https://docs.google.com/forms/d/e/1FAIpQLSf1X3GgiJ2x8-x-XXVearUhGp5tTYkX-_bI7hQX7OBCOzh4Qg/viewform",
    )

    def __str__(self):
        return "3 месяц"

    class Meta:
        verbose_name = "3 месяц"
        abstract = False





