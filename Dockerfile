# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    musl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt
COPY requirements.txt /app/

# Устанавливаем Python зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем проект
COPY . /app/

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Создаем директорию для медиа файлов
RUN mkdir -p /app/media

# Открываем порт
EXPOSE 8000

# Запускаем gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "skybar.wsgi:application"]

