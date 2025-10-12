# ⚡ Быстрый старт SkyBAR

## 🎯 Для локальной разработки (без Docker)

### 1. Установите зависимости:
```bash
python -m pip install -r requirements.txt
```

### 2. Примените миграции:
```bash
python manage.py migrate
```

### 3. Создайте таблицу для кэша (для работы без Redis):
```bash
python manage.py createcachetable
```

**Примечание:** По умолчанию локальная разработка использует SQLite для кэша и сессий. 
Для использования Redis установите переменную окружения `USE_REDIS=True` и запустите Redis.

### 4. Создайте тестовые данные:
```bash
python manage.py create_tables
python manage.py populate_songs
```

### 5. Создайте администратора:
```bash
python manage.py createsuperuser
```

### 6. Запустите сервер:
```bash
python manage.py runserver
```

### 7. Откройте браузер:
- Сайт: http://127.0.0.1:8000
- Админ: http://127.0.0.1:8000/admin

---

## 🐳 Для Docker деплоя

### 1. Создайте .env файл:
```bash
copy env.example .env  # Windows
cp env.example .env    # Linux/Mac
```

### 2. Запустите Docker:
```bash
docker-compose up -d
```

### 3. Миграции и данные:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py create_tables
docker-compose exec web python manage.py populate_songs
docker-compose exec web python manage.py createsuperuser
```

### 4. Откройте:
- http://localhost

---

## 🧪 Тестирование

```bash
# Все тесты
pytest

# С покрытием
pytest --cov=restaurant --cov-report=html

# Открыть отчет
# Откройте htmlcov/index.html
```

---

## 📋 Основные команды

```bash
# Создать миграции
python manage.py makemigrations

# Применить миграции
python manage.py migrate

# Собрать статику
python manage.py collectstatic

# Создать админа
python manage.py createsuperuser

# Запустить shell
python manage.py shell
```

---

## ✅ Готово!

Сервер запущен и работает на http://127.0.0.1:8000

