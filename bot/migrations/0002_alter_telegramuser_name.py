# Generated by Django 5.1.2 on 2024-11-05 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='name',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='имя'),
        ),
    ]