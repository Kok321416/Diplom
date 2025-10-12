#!/bin/bash

# Скрипт резервного копирования базы данных
# Использование: ./scripts/backup.sh

BACKUP_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/skybar_backup_${DATE}.sql"

echo "💾 Создание резервной копии базы данных..."

# Создаем директорию для бэкапов
mkdir -p $BACKUP_DIR

# Создаем бэкап
docker-compose exec -T db pg_dump -U skybar_user skybar_db > $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo "✅ Резервная копия создана: $BACKUP_FILE"
    
    # Сжимаем бэкап
    gzip $BACKUP_FILE
    echo "🗜️ Файл сжат: ${BACKUP_FILE}.gz"
    
    # Удаляем старые бэкапы (старше 30 дней)
    find $BACKUP_DIR -name "*.gz" -mtime +30 -delete
    echo "🧹 Старые бэкапы удалены"
else
    echo "❌ Ошибка при создании резервной копии"
    exit 1
fi

