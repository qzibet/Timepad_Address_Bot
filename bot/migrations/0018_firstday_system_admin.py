# Generated by Django 5.1.2 on 2024-12-11 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0017_faq_file_alter_faq_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='firstday',
            name='system_admin',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='контакт сис.админа'),
        ),
    ]
