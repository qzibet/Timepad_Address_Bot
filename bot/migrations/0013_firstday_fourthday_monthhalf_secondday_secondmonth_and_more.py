# Generated by Django 5.1.2 on 2024-12-09 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0012_preonbordinglinks'),
    ]

    operations = [
        migrations.CreateModel(
            name='FirstDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_zoom', models.URLField(blank=True, null=True, verbose_name='ссылка на встречу в ZOOM!')),
                ('link_event_group', models.URLField(blank=True, null=True, verbose_name='ссылка на Канал события')),
                ('link_offtop_timepad', models.URLField(blank=True, null=True, verbose_name='ссылка на Offtop Timepad')),
                ('link_admin', models.URLField(blank=True, null=True, verbose_name='контакт админа Барахолка и свопы')),
                ('link_eva', models.URLField(blank=True, null=True, verbose_name='ссылка на чат Ева')),
                ('logo_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на логотип')),
                ('link_byod', models.URLField(blank=True, null=True, verbose_name='Ссылка на BYOD')),
                ('hr_documentation_contact', models.CharField(blank=True, max_length=55, null=True, verbose_name='Контакт ответственного за кадровый документооборот')),
                ('payroll_contact', models.CharField(blank=True, max_length=255, null=True, verbose_name='Контакт ответственного за зарплату')),
                ('interface_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на интерфейс для сотрудников')),
                ('vacation_info', models.URLField(blank=True, null=True, verbose_name='Ссылка на информацию про отпуск')),
                ('freelance_vacation', models.URLField(blank=True, null=True, verbose_name='Ссылка на информацию про отпуск(для внештатных)')),
                ('avatar_images_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на скачивание картинок аватарок')),
                ('work_reference_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на справку с работы')),
            ],
            options={
                'verbose_name': '1 рабочий день',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FourthDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corporate_discounts_link', models.URLField(default='https://telegra.ph/Bonusy-i-partnerskie-skidki-11-14', verbose_name='Ссылка на страницу с корпоративными скидками')),
                ('birthday_form_link', models.URLField(default='https://telegra.ph/Bonusy-i-partnerskie-skidki-11-14', verbose_name='Ссылка на форму ДР')),
                ('account_manager_contact', models.CharField(default='@vi_litvinova', max_length=25, verbose_name='Контакт аккаунт-менеджера отдела развития')),
                ('photo_link', models.URLField(default='https://drive.google.com/drive/u/1/folders/1kg8bYqISsnXgyKltrnZGRZBqrZ6T8gNn', verbose_name='Ссылка фотографии')),
                ('survey_link', models.URLField(default='https://docs.google.com/forms/d/e/1FAIpQLSfw1RFDwUod-F868-9MzN9VuJ-8CVD9T---I-RW_-ue5C6WuA/viewform', verbose_name='Ссылка на анкету')),
                ('event_recordings_and_presentations_link', models.URLField(default='https://www.notion.so/42d7ebd5335844e2afacbb1c6f0c061a?pvs=21', verbose_name='Ссылка на записи и презентации мероприятий')),
                ('corporate_events_link', models.URLField(default='https://www.notion.so/4c1bcbf52bef458c8b5af800e94c8871?pvs=2', verbose_name='Ссылка на корпоративные мероприятия')),
                ('ice_rink_link', models.URLField(default='https://t.me/+x2m0Ry7AU3cwODEy', verbose_name='Ссылка на канал про каток')),
                ('sup_link', models.URLField(default='https://t.me/+XJlZ1_sJTKllZjQ6', verbose_name='Ссылка на канал про сапы')),
                ('karaoke_link', models.URLField(default='https://t.me/+WTlTv0-Tym0zNjUy', verbose_name='Ссылка на канал про караоке')),
                ('humor_and_mishaps_link', models.URLField(default='https://t.me/+aVrcvXCmZWcxYTMy', verbose_name='Ссылка на канал Смех и грех')),
                ('dms_link', models.URLField(default='https://timepaddev.notion.site', verbose_name='Ссылка на ДМС')),
            ],
            options={
                'verbose_name': '4 рабочий день',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MonthHalf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_link', models.URLField(default='https://docs.google.com/forms/d/e/1FAIpQLScEQfKbumuqSd_3DeR1WDtQJUt5fYvUQEnGFJWgqXLmm9MLyQ/viewform', verbose_name='Ссылка на ДМС')),
            ],
            options={
                'verbose_name': '1,5 месяц',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SecondDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_afisha_group', models.URLField(blank=True, null=True, verbose_name='Ссылка на афишу')),
                ('art_branches_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на статью о арт-бранчах')),
                ('forest_escapes_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на статью о лесных экотопах')),
                ('travel_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на статью о путешествиях')),
                ('tg_channel_weekends', models.CharField(blank=True, default='@TimepadRU', max_length=255, null=True, verbose_name="Ссылка на TG-канал 'Спасите мои выходные'")),
                ('tg_channel_paradnaya', models.CharField(blank=True, default='@Timepadru_spb', max_length=255, null=True, verbose_name="Ссылка на TG-канал 'Спасите мои парадные'")),
                ('vk_link', models.URLField(blank=True, default='https://vk.com/timepadru', null=True, verbose_name='Ссылка на ВКонтакте')),
                ('instagram_link', models.URLField(blank=True, default='https://www.instagram.com/timepad.ru', null=True, verbose_name='Ссылка на Инстаграм')),
                ('podcast_save_my_weekend', models.URLField(blank=True, default='https://savemyweekend.mave.digital', null=True, verbose_name='Ссылка на подкаст "Спасите мои выходные" с Варей Семенихиной')),
                ('podcast_tochno_idem', models.URLField(blank=True, default='https://tochnoidem.mave.digital', null=True, verbose_name='Ссылка на подкаст "Точно идем"')),
                ('development_director_contact', models.CharField(blank=True, default='@darialvistner', max_length=25, null=True, verbose_name='Контакт директора по развитию билетного бизнеса')),
                ('marketing_director_contact', models.CharField(blank=True, default='@dasha_gaydukova', max_length=55, null=True, verbose_name='Контакт руководителя отдела маркетинга')),
                ('smm_specialist_contact', models.CharField(default='@marypopossa', max_length=255, verbose_name='Контакт СММщицы')),
                ('advertising_director_contact', models.CharField(default='@azamorkvasov', max_length=255, verbose_name='Контакт руководителя отдела рекламы')),
            ],
            options={
                'verbose_name': '2 рабочий день',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SecondMonth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hr_link', models.URLField(default='https://us02web.zoom.us/j/86826507585?pwd=qmo2josZPIVmEJzV8cnrd3FRKlIjl7.1', verbose_name='Ссылка на ДМС')),
            ],
            options={
                'verbose_name': '2 месяц',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ThirdMonth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meet_link', models.URLField(default='https://docs.google.com/forms/d/e/1FAIpQLSf1X3GgiJ2x8-x-XXVearUhGp5tTYkX-_bI7hQX7OBCOzh4Qg/viewform', verbose_name='Ссылка на ДМС')),
            ],
            options={
                'verbose_name': '3 месяц',
                'abstract': False,
            },
        ),
    ]
