# Generated by Django 5.1.2 on 2024-12-10 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0014_firstday_hr_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firstday',
            name='hr_contact',
            field=models.CharField(blank=True, default='@malikovaj', max_length=255, null=True, verbose_name='Контакт hr'),
        ),
    ]
