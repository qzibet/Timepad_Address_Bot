# Generated by Django 5.1.2 on 2024-12-15 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0021_telegramuser_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramuser',
            name='state',
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='current_block',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='current_day',
            field=models.IntegerField(default=1),
        ),
    ]