# Generated by Django 5.1.2 on 2024-12-11 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0018_firstday_system_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firstday',
            name='system_admin',
            field=models.CharField(blank=True, default='@woolycrypticboy', max_length=25, null=True, verbose_name='контакт сис.админа'),
        ),
    ]
