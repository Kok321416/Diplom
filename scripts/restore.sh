#!/bin/bash

# Скрипт восстановления базы данных из бэкапа
# Использование: ./scripts/restore.sh <backup_file.sql.gz>

if [ -z "$1" ]; then
    echo "❌ Укажите файл бэкапа"
    echo "Использование: ./scripts/restore.sh backups/skybar_backup_YYYYMMDD_HHMMSS.sql.gz"
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Файл не найден: $BACKUP_FILE"
    exit 1
fi

echo "⚠️  ВНИМАНИЕ: Все текущие данные будут удалены!"
read -p "Продолжить? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Восстановление отменено"
    exit 0
fi

echo "📤 Распаковка бэкапа..."
gunzip -c $BACKUP_FILE > /tmp/restore.sql

echo "🗑️ Удаление текущей базы данных..."
docker-compose exec -T db dropdb -U skybar_user skybar_db --if-exists

echo "🔨 Создание новой базы данных..."
docker-compose exec -T db createdb -U skybar_user skybar_db

echo "📥 Восстановление данных..."
docker-compose exec -T db psql -U skybar_user -d skybar_db < /tmp/restore.sql

if [ $? -eq 0 ]; then
    echo "✅ База данных восстановлена успешно!"
    rm /tmp/restore.sql
else
    echo "❌ Ошибка при восстановлении"
    exit 1
fi

echo "🔄 Перезапуск web сервиса..."
docker-compose restart web

echo "✅ Готово!"

