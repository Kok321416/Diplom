#!/bin/bash

# Скрипт деплоя SkyBAR
# Использование: ./scripts/deploy.sh

echo "🚀 Начинаем деплой SkyBAR..."

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден! Создайте его на основе env.example"
    exit 1
fi

echo "📦 Остановка старых контейнеров..."
docker-compose down

echo "🔨 Сборка Docker образов..."
docker-compose build

echo "🚀 Запуск сервисов..."
docker-compose up -d

echo "⏳ Ожидание запуска базы данных..."
sleep 10

echo "📊 Применение миграций..."
docker-compose exec -T web python manage.py migrate

echo "📁 Сбор статических файлов..."
docker-compose exec -T web python manage.py collectstatic --noinput

echo "🧪 Запуск тестов..."
docker-compose exec -T web pytest

echo "✅ Деплой завершен!"
echo "🌐 Приложение доступно на http://localhost"
echo "📊 Логи: docker-compose logs -f web"

