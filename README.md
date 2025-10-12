# 🍽️ SkyBAR - Система бронирования ресторана

Современная веб-система для управления бронированиями ресторана SkyBAR с поддержкой караоке и организации мероприятий.

## ✨ Основные возможности

### 👤 Для посетителей:
- 🎯 **Бронирование столов** - интерактивная карта с выбором конкретных мест
- 👥 **Гибкое бронирование** - до 12 гостей, можно выбирать места с разных столов
- 📊 **Ограничения** - максимум 2 активных бронирования на пользователя
- ✏️ **Редактирование** - изменение даты, времени и пожеланий
- 🎤 **Караоке** - очередь на исполнение, до 3 песен на пользователя
- 🎉 **Мероприятия** - организация событий до 50 участников с дополнительными услугами
- 🎂 **День рождения** - специальные опции для празднования

### 👨‍💼 Для администраторов:
- 📋 **Админ-панель** - управление бронированиями, столами, пользователями
- 📊 **Статистика** - отчеты по бронированиям и мероприятиям
- 🎵 **Управление караоке** - контроль очереди и песен

## 🚀 Технологии

- **Backend**: Django 4.2.7, Python 3.11
- **Database**: PostgreSQL 15 / SQLite (для разработки)
- **Cache**: Redis 7
- **Frontend**: Bootstrap 5.3, JavaScript (ES6+)
- **Deployment**: Docker, Docker Compose, Nginx, Gunicorn
- **CI/CD**: GitHub Actions
- **Testing**: pytest, pytest-django, coverage

## 📦 Установка и запуск

### Вариант 1: С помощью Docker (рекомендуется)

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/yourusername/skybar.git
cd skybar
```

2. **Создайте файл `.env` на основе `env.example`:**
```bash
copy env.example .env  # Windows
cp env.example .env    # Linux/Mac
```

3. **Отредактируйте `.env` файл** и укажите свои значения

4. **Запустите проект:**
```bash
docker-compose up -d
```

5. **Примените миграции:**
```bash
docker-compose exec web python manage.py migrate
```

6. **Создайте суперпользователя:**
```bash
docker-compose exec web python manage.py createsuperuser
```

7. **Заполните тестовые данные (опционально):**
```bash
docker-compose exec web python manage.py create_tables
docker-compose exec web python manage.py populate_songs
```

8. **Откройте браузер:**
- Приложение: http://localhost
- Админ-панель: http://localhost/admin

### Вариант 2: Локальная разработка

1. **Создайте виртуальное окружение:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. **Установите зависимости:**
```bash
python -m pip install -r requirements.txt
```

3. **Примените миграции:**
```bash
python manage.py migrate
```

4. **Создайте таблицу для кэша (опционально для работы без Redis):**
```bash
python manage.py createcachetable
```

**Примечание:** По умолчанию проект работает без Redis в режиме разработки. 
Для включения Redis установите `USE_REDIS=True` в переменных окружения.

4. **Создайте суперпользователя:**
```bash
python manage.py createsuperuser
```

5. **Заполните тестовые данные:**
```bash
python manage.py create_tables
python manage.py populate_songs
```

6. **Запустите сервер разработки:**
```bash
python manage.py runserver
```

7. **Откройте браузер:**
http://127.0.0.1:8000

## 🧪 Тестирование

### Запуск всех тестов:
```bash
pytest
```

### Запуск с покрытием кода:
```bash
pytest --cov=restaurant --cov-report=html
```

### Запуск конкретного теста:
```bash
pytest restaurant/tests/test_models.py::TestUserModel::test_create_user
```

### Проверка качества кода:
```bash
# Форматирование
black restaurant skybar

# Сортировка импортов
isort restaurant skybar

# Линтер
flake8 restaurant --max-line-length=120
```

## 📁 Структура проекта

```
Diplom/
├── restaurant/               # Основное приложение
│   ├── management/          # Команды управления
│   │   └── commands/
│   │       ├── create_tables.py
│   │       ├── populate_songs.py
│   │       └── create_admin.py
│   ├── migrations/          # Миграции БД
│   ├── tests/              # Тесты
│   │   ├── test_models.py
│   │   └── test_views.py
│   ├── models.py           # Модели данных
│   ├── views.py            # Представления
│   ├── forms.py            # Формы
│   ├── urls.py             # URL маршруты
│   └── admin.py            # Админ-панель
├── skybar/                  # Настройки проекта
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/               # HTML шаблоны
│   ├── base.html
│   └── restaurant/
├── static/                  # Статические файлы
│   ├── css/
│   └── js/
├── .github/                 # GitHub Actions
│   └── workflows/
│       └── ci.yml
├── Dockerfile              # Docker образ
├── docker-compose.yml      # Docker Compose конфигурация
├── nginx.conf              # Nginx конфигурация
├── requirements.txt        # Python зависимости
├── pytest.ini             # Настройки pytest
└── README.md              # Этот файл
```

## 🔧 Основные команды Django

### Миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Создание админа:
```bash
python manage.py createsuperuser
```

### Сбор статики:
```bash
python manage.py collectstatic
```

### Кастомные команды:
```bash
python manage.py create_tables      # Создать столы и места
python manage.py populate_songs     # Загрузить песни для караоке
python manage.py recreate_tables    # Пересоздать структуру столов
```

## 🐳 Docker команды

### Запуск:
```bash
docker-compose up -d         # Запустить в фоне
docker-compose up            # Запустить с логами
```

### Остановка:
```bash
docker-compose down          # Остановить
docker-compose down -v       # Остановить и удалить volumes
```

### Логи:
```bash
docker-compose logs -f web   # Логи Django
docker-compose logs -f db    # Логи PostgreSQL
docker-compose logs -f redis # Логи Redis
```

### Выполнение команд:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic
```

### Перезапуск сервиса:
```bash
docker-compose restart web
```

## 🔐 Переменные окружения

Создайте файл `.env` в корне проекта:

```env
# Django
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=skybar_db
DB_USER=skybar_user
DB_PASSWORD=secure_password
DB_HOST=db
DB_PORT=5432

# Redis (для production с Docker)
USE_REDIS=True
REDIS_URL=redis://redis:6379/1

# Для локальной разработки без Redis:
# USE_REDIS=False
```

## 📊 Модели данных

### User
- Кастомная модель пользователя с ролями (user/admin/staff)
- Авторизация по username
- Email, телефон (опционально)

### Table
- Номер стола, зона (regular/vip), количество мест
- Координаты для визуализации на карте

### Seat
- Места за столом с возможностью бронирования

### Reservation
- Бронирования с временными слотами
- Статусы: temporary (10 мин), confirmed, cancelled, completed
- Привязка к пользователю, столу и местам

### Event
- Мероприятия до 50 участников
- Опции: алкоголь, ведущий, декорации, музыка, фотограф, кейтеринг
- Статусы: pending, confirmed, cancelled, completed

### Song & KaraokeQueue
- База песен для караоке
- Очередь с позициями и статусами

## 🎨 Особенности UI/UX

- 🌈 **Градиентный дизайн** - современные цветовые переходы
- ✨ **Анимации** - плавные переходы и эффекты
- 📱 **Адаптивность** - работает на всех устройствах
- 🎪 **Интерактивность** - реагирование на действия пользователя
- 💫 **Эффекты свечения** - для важных элементов
- 🎯 **Визуальная карта** - выбор столов и мест в реальном времени

## 🔄 CI/CD Pipeline

GitHub Actions автоматически:
- ✅ Запускает тесты при push/PR
- ✅ Проверяет покрытие кода
- ✅ Проверяет качество кода (flake8, black, isort)
- ✅ Собирает Docker образ для main ветки

## 📝 API Endpoints

### Публичные:
- `GET /` - Главная страница
- `GET /karaoke/` - Страница караоке
- `POST /auth/register/` - Регистрация
- `POST /auth/login/` - Вход

### Требующие авторизации:
- `GET /booking-preferences/` - Параметры бронирования
- `GET /table-selection/<guest_count>/` - Выбор столов
- `POST /api/create-reservation/` - Создание бронирования
- `GET /my-reservations/` - Мои бронирования
- `GET /edit-reservation/<id>/` - Редактирование
- `POST /cancel-reservation/<id>/` - Отмена
- `GET /create-event/` - Создание мероприятия
- `POST /api/karaoke/add/` - Добавить песню в караоке
- `POST /api/karaoke/remove/` - Удалить песню

### Административные:
- `GET /admin/` - Админ-панель Django
- `GET /admin/` (custom) - Кастомная админ-панель

## 🛡️ Безопасность

- 🔒 CSRF защита
- 🔐 Хеширование паролей (Django встроенное)
- 🚫 SQL Injection защита (Django ORM)
- 📝 Валидация форм
- ⏱️ Временные бронирования (10 минут)
- 👮 Проверка прав доступа

## 📈 Производительность

- ⚡ Redis кэширование
- 💾 Redis для сессий
- 🗜️ WhiteNoise для статики
- 🚀 Gunicorn с 3 workers
- 📦 Docker для изоляции

## 🤝 Контрибьюция

1. Fork проекта
2. Создайте feature ветку (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📞 Контакты

- Email: info@skybar.ru
- Телефон: +7 (950) 068-95-64

## 📄 Лицензия

Этот проект создан для образовательных целей.

## 🎯 TODO

- [ ] Добавить email уведомления
- [ ] Интеграция с платежными системами
- [ ] Mobile приложение
- [ ] WebSocket для real-time обновлений очереди караоке
- [ ] Telegram бот для бронирований
- [ ] Система лояльности
- [ ] Отзывы и рейтинги

---

Сделано с ❤️ для любителей хорошей кухни и караоке
