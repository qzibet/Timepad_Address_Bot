# Generated by Django 5.1.2 on 2024-11-08 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_code_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='timepad',
            field=models.IntegerField(default=0, verbose_name='количество таймпадов'),
        ),
    ]
