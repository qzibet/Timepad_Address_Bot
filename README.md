# Развертывание бота

## Настройка окружения

1. **Установите Python и виртуальное окружение**:
   ```bash
   python3 -m venv .venv
   source venv/bin/activate
   ```
---

2. **Настройте переменные окружения**:
   Создайте файл `.env` в корневой директории проекта:
   ```env
      ##Токен бота
      #Оставьте этот же токен
      TOKEN=7834125494:AAFJFjBjlQzZjsDjSTwe3fixYvxdqxCaPow
      
      #Настройки бд
      DB_NAME=hr_bot
      DB_USER=postgres
      DB_PASSWORD=postgres
      DB_HOST=host.docker.internal
      DB_PORT=5432
      
      ## Пароли от админов для продолжения контента
      #Оставьте эти же
      SECRET_PASSWORD="afisha"
      IVAN_SECRET_PASSWORD="time"
      MONTH_SECRET_PASSWORD="hobby"
   ```
3. **Настройка nginx, настройка(доменки)**:
   Перейдите в файл ./nginx/nginx.conf и отредактируйте его следующим образом: Включите строку server_name и замените server_domain_or_IP на ваш домен.
   ```bash
       server {
           listen 8000;
           server_name timepad-bot.ru;
   ```

4. **Запустите контейнеры**:
   Выполните следующую команду для запуска всех сервисов:
   ```bash
   docker-compose up
   ```
---

## Дополнительно

1. **Запуск миграций вручную**:
   Если нужно применить миграции отдельно, выполните:
   ```bash
   docker exec -it bot_web python manage.py migrate
   ```