FROM python:3.12-slim

# Установить системные зависимости, необходимые для Pillow и других пакетов
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    liblcms2-dev \
    libtiff5-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt /app/

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY ./entrypoint.sh /app/entrypoint.sh

# Создаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN ls -la /app
RUN cat /app/entrypoint.sh


# Открываем порты для Gunicorn и сервера Django
EXPOSE 8000

# Указываем команду по умолчанию
CMD ["/app/entrypoint.sh"]
