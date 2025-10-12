# 🚀 Руководство по деплою SkyBAR

## Содержание
- [Docker деплой](#docker-деплой)
- [Heroku деплой](#heroku-деплой)
- [VPS деплой](#vps-деплой)
- [Переменные окружения](#переменные-окружения)

## Docker деплой

### Локальный деплой

1. **Подготовка:**
```bash
# Клонируйте репозиторий
git clone https://github.com/yourusername/skybar.git
cd skybar

# Создайте .env файл
copy env.example .env  # Windows
cp env.example .env    # Linux/Mac

# Отредактируйте .env файл
```

2. **Запуск:**
```bash
# Сборка и запуск
docker-compose up -d

# Миграции
docker-compose exec web python manage.py migrate

# Создание админа
docker-compose exec web python manage.py createsuperuser

# Загрузка тестовых данных
docker-compose exec web python manage.py create_tables
docker-compose exec web python manage.py populate_songs
```

3. **Проверка:**
```bash
# Проверка здоровья сервисов
curl http://localhost/health/

# Просмотр логов
docker-compose logs -f web
```

### Production деплой с Docker

1. **Настройте переменные окружения для production:**
```env
DEBUG=False
SECRET_KEY=<generate-strong-secret-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.postgresql
SECURE_SSL_REDIRECT=True
```

2. **Запустите с production конфигурацией:**
```bash
docker-compose -f docker-compose.yml up -d
```

## Heroku деплой

1. **Установите Heroku CLI**

2. **Создайте приложение:**
```bash
heroku create skybar-app
```

3. **Добавьте аддоны:**
```bash
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev
```

4. **Установите переменные окружения:**
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=skybar-app.herokuapp.com
```

5. **Деплой:**
```bash
git push heroku main
```

6. **Миграции:**
```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku run python manage.py create_tables
```

## VPS деплой (Ubuntu/Debian)

### 1. Подготовка сервера

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo apt install docker-compose -y

# Создание пользователя для приложения
sudo useradd -m -s /bin/bash skybar
sudo usermod -aG docker skybar
```

### 2. Клонирование и настройка

```bash
# Переход к пользователю
sudo su - skybar

# Клонирование репозитория
git clone https://github.com/yourusername/skybar.git
cd skybar

# Создание .env файла
cp env.example .env
nano .env  # Редактирование
```

### 3. Запуск

```bash
# Сборка и запуск
docker-compose up -d

# Миграции
docker-compose exec web python manage.py migrate

# Создание админа
docker-compose exec web python manage.py createsuperuser

# Загрузка данных
docker-compose exec web python manage.py create_tables
docker-compose exec web python manage.py populate_songs
```

### 4. Настройка Nginx (если используете отдельный Nginx)

```bash
sudo nano /etc/nginx/sites-available/skybar
```

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /home/skybar/skybar/staticfiles/;
    }

    location /media/ {
        alias /home/skybar/skybar/media/;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/skybar /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. SSL сертификат (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## Переменные окружения

### Обязательные:
- `SECRET_KEY` - секретный ключ Django (генерируйте уникальный!)
- `DEBUG` - режим отладки (False для production)
- `ALLOWED_HOSTS` - разрешенные хосты

### База данных:
- `DB_ENGINE` - движок БД (postgresql для production)
- `DB_NAME` - имя базы данных
- `DB_USER` - пользователь БД
- `DB_PASSWORD` - пароль БД
- `DB_HOST` - хост БД
- `DB_PORT` - порт БД

### Redis:
- `REDIS_URL` - URL подключения к Redis

### Безопасность (Production):
- `SECURE_SSL_REDIRECT=True`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`

## 🔍 Мониторинг

### Health Check:
```bash
curl http://localhost/health/
```

### Логи:
```bash
# Docker
docker-compose logs -f web

# Файл
tail -f logs/django.log
```

### Метрики Redis:
```bash
docker-compose exec redis redis-cli INFO
```

### Метрики PostgreSQL:
```bash
docker-compose exec db psql -U skybar_user -d skybar_db -c "SELECT * FROM pg_stat_activity;"
```

## 🔄 Обновление

```bash
# Получить последние изменения
git pull origin main

# Пересобрать и перезапустить
docker-compose up -d --build

# Миграции
docker-compose exec web python manage.py migrate

# Сбор статики
docker-compose exec web python manage.py collectstatic --noinput
```

## 💾 Резервное копирование

### Создание бэкапа:
```bash
./scripts/backup.sh
```

### Восстановление:
```bash
./scripts/restore.sh backups/skybar_backup_20241012_120000.sql.gz
```

## 🆘 Troubleshooting

### Проблема: Контейнеры не запускаются
```bash
docker-compose down
docker-compose up --build
```

### Проблема: Ошибка подключения к БД
```bash
# Проверьте логи
docker-compose logs db

# Проверьте что БД запущена
docker-compose ps
```

### Проблема: Статика не загружается
```bash
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart nginx
```

### Проблема: Redis недоступен
```bash
docker-compose logs redis
docker-compose restart redis
```

## 📧 Поддержка

При возникновении проблем:
1. Проверьте логи: `docker-compose logs`
2. Проверьте health check: `curl http://localhost/health/`
3. Создайте issue в GitHub
4. Напишите на info@skybar.ru

