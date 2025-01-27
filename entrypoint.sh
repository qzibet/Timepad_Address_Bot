#!/bin/sh
# Выполнение миграций
echo "Применение миграций"
python manage.py migrate

echo "экспорт переменных"
export $(grep -v '^#' .env | xargs)

# Собираем статику (если нужно)
echo "Сбор статических файлов"
python manage.py collectstatic --noinput

# Создание суперпользователя, если он не существует
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Создание суперпользователя"
    python manage.py shell << END
from django.contrib.auth.models import User

username = "$DJANGO_SUPERUSER_USERNAME"
email = "$DJANGO_SUPERUSER_EMAIL"
password = "$DJANGO_SUPERUSER_PASSWORD"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Суперпользователь '{username}' создан")
else:
    print(f"Суперпользователь '{username}' уже существует")
END
else
    echo "Переменные для создания суперпользователя не заданы"
fi

# Запуск сервера
exec "$@"
