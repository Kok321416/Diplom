# 🍽️ SkyBAR - Система бронирования ресторана

Современная веб-система для управления бронированиями ресторана SkyBAR с поддержкой караоке и организации мероприятий.

## ✨ Основные возможности

### 👤 Для посетителей:
- 🎯 **Интерактивная карта столов** - визуализация всех зон (обычная + VIP)
- 💺 **Выбор конкретных мест** - кликайте на стулья, выбирайте с разных столов
- 👥 **До 12 гостей** - гибкое бронирование с красивым интерфейсом
- 📊 **Лимит 2 бронирования** - не более 2 активных бронирований одновременно
- ✏️ **Редактирование** - изменение даты, времени и пожеланий
- ❌ **Отмена бронирования** - в один клик с освобождением мест
- 🎤 **Караоке** - до 3 песен на пользователя, удаление своих песен
- 🎉 **Мероприятия** - до 50 участников, 7 опций услуг (алкоголь, ведущий, декорации и др.)
- 🎂 **День рождения** - специальное оформление
- 🎨 **Красивый UI** - пастельные цвета, анимации, градиенты

### 👨‍💼 Для администраторов:
- 📋 **Django Admin** - полное управление всеми моделями
- 🎫 **Прямое бронирование** - создание бронирований от имени клиентов
- 📊 **Управление столами** - 25 столов (18 обычных, 7 VIP)
- 👥 **Управление пользователями** - роли (user/admin/staff)
- 🎵 **Управление караоке** - контроль очереди, статусы исполнения
- 🎉 **Заявки на мероприятия** - подтверждение/отмена событий

## 🚀 Технологии

### Backend:
- **Django 4.2.7** - web framework
- **Python 3.11+** - язык программирования
- **Gunicorn** - WSGI сервер для production
- **WhiteNoise** - обслуживание статических файлов

### Database & Cache:
- **PostgreSQL 15** - основная БД (production)
- **SQLite** - БД для разработки
- **Redis 7** - кэширование и сессии (опционально)
- **Database Cache** - fallback без Redis

### Frontend:
- **Bootstrap 5.3** - UI framework
- **JavaScript ES6+** - интерактивность
- **Font Awesome 6** - иконки
- **CSS3 Animations** - градиенты, переходы, эффекты

### DevOps:
- **Docker & Docker Compose** - контейнеризация
- **Nginx** - reverse proxy
- **GitHub Actions** - CI/CD автоматизация
- **pytest** - тестирование с покрытием кода

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

5. **Создайте суперпользователя:**
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

8. **Откройте браузер:**
- Сайт: http://127.0.0.1:8000
- Админ: http://127.0.0.1:8000/admin

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

### User (Пользователь)
- **Кастомная модель** на основе AbstractUser
- **Авторизация**: по username (не по телефону)
- **Поля**: username, email, phone (опционально), role
- **Роли**: user, admin, staff
- **Связи**: reservations, events, karaoke_queue

### Table (Стол)
- **Зоны**: regular (18 столов), vip (7 столов)
- **Поля**: number, zone, max_seats, floor, x/y_position
- **Визуализация**: позиции на интерактивной карте
- **Статус**: is_active

### Seat (Место)
- **Принадлежность**: к конкретному столу
- **Поля**: seat_number, is_available
- **Функционал**: бронирование/освобождение мест
- **Визуализация**: красные (занято) / зеленые (свободно)

### Reservation (Бронирование)
- **Статусы**: 
  - `temporary` - временное (10 минут)
  - `confirmed` - подтвержденное
  - `cancelled` - отмененное
  - `completed` - завершенное
- **Связи**: user, table, seats (ManyToMany)
- **Ограничения**: максимум 2 активных на пользователя
- **Редактирование**: дата, время, пожелания

### Event (Мероприятие)
- **Участники**: до 50 человек
- **Услуги** (Boolean поля):
  - alcohol, host, decoration, music
  - photographer, catering, sound_equipment
- **Статусы**: pending, confirmed, cancelled, completed
- **Поля**: date, time, special_requests

### Song & KaraokeQueue (Караоке)
- **Song**: artist, title, duration, is_popular
- **KaraokeQueue**: 
  - До 3 песен на пользователя
  - Позиции в очереди
  - Статусы: waiting, singing, completed
  - Удаление только своих песен

### BookingPreferences (Предпочтения)
- Сохраненные настройки пользователя
- Preferred_zone, smoking_preference

## 🎨 Особенности UI/UX

### Дизайн:
- 🌿 **Пастельная палитра** - мягкие зеленые, бежевые и персиковые тона
- 🌈 **Градиенты** - плавные цветовые переходы
- ✨ **Плавные анимации** - появление, масштабирование, вращение
- 💫 **Эффекты свечения** - мягкие тени и подсветки
- 🎭 **Glassmorphism** - полупрозрачные элементы с размытием

### Интерактивность:
- 🎯 **Интерактивная карта** - выбор мест в реальном времени
- 🔴 **Визуализация занятости** - красные места = заняты, зеленые = свободны
- 🎪 **Hover эффекты** - увеличение, поворот, свечение
- 📱 **Адаптивность** - работает на всех устройствах
- ⚡ **Мгновенная обратная связь** - изменения видны сразу
- 🎨 **Кастомные элементы** - красивые карточки выбора времени и зон

## 🔄 CI/CD Pipeline

GitHub Actions автоматически:
- ✅ Запускает тесты при push/PR
- ✅ Проверяет покрытие кода
- ✅ Проверяет качество кода (flake8, black, isort)
- ✅ Собирает Docker образ для main ветки

## 📝 API Endpoints

### Публичные:
- `GET /` - Главная страница
- `GET /karaoke/` - Караоке с очередью
- `POST /auth/register/` - Регистрация (по username)
- `POST /auth/login/` - Вход (по username)
- `GET /health/` - Health check endpoint

### Бронирование (требует авторизации):
- `GET /booking-preferences/` - Выбор параметров (гости, зона)
- `GET /table-selection/<guest_count>/` - Интерактивная карта
- `POST /api/create-reservation/` - Создание бронирования
- `GET /reservation-confirmation/<id>/` - Подтверждение и оплата
- `GET /reservation-success/<id>/` - Успешное бронирование
- `GET /my-reservations/` - Список бронирований
- `GET /edit-reservation/<id>/` - Редактирование
- `POST /cancel-reservation/<id>/` - Отмена с освобождением мест
- `GET /direct-reservation/` - Прямое бронирование (быстрая форма)

### Мероприятия (требует авторизации):
- `GET /create-event/` - Создание мероприятия
- `GET /my-events/` - Список мероприятий

### Караоке (требует авторизации):
- `POST /api/karaoke/add/` - Добавить песню (макс 3)
- `POST /api/karaoke/remove/` - Удалить свою песню

### Административные:
- `GET /admin/` - Django Admin панель
- `GET /admin/panel/` - Кастомная панель управления
- `GET /admin/table-selection/` - Выбор столов для админа

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

## ✅ Реализовано

- ✅ Система бронирования с интерактивной картой
- ✅ Выбор конкретных мест (можно с разных столов)
- ✅ Визуализация занятых мест (красные стулья)
- ✅ Редактирование и отмена бронирований
- ✅ Лимит 2 активных бронирования на пользователя
- ✅ Караоке с очередью (до 3 песен)
- ✅ Система мероприятий (до 50 человек)
- ✅ Авторизация по username
- ✅ Две зоны: обычная (18 столов) и VIP (7 столов)
- ✅ Красивый UI с пастельными цветами
- ✅ Docker готов к деплою
- ✅ Redis для кэширования (опционально)
- ✅ Тесты и CI/CD

## 🎯 Планы развития

- [ ] Email уведомления о бронированиях
- [ ] Интеграция с платежными системами
- [ ] WebSocket для real-time обновлений караоке
- [ ] Telegram бот для бронирований
- [ ] Система лояльности и бонусов
- [ ] Отзывы и рейтинги
- [ ] Mobile приложение (React Native)
- [ ] QR-коды для бронирований
- [ ] Автоматическое освобождение просроченных бронирований (Celery)

---

Сделано с ❤️ для любителей хорошей кухни и караоке
