# Generated by Django 5.1.2 on 2024-11-10 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_telegramuser_timepad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='videos/')),
                ('number', models.IntegerField()),
            ],
        ),
    ]
