.PHONY: help build up down restart logs shell migrate test clean

help:
	@echo "SkyBAR - Команды для управления проектом"
	@echo ""
	@echo "make build      - Собрать Docker образы"
	@echo "make up         - Запустить все сервисы"
	@echo "make down       - Остановить все сервисы"
	@echo "make restart    - Перезапустить web сервис"
	@echo "make logs       - Показать логи"
	@echo "make shell      - Открыть Django shell"
	@echo "make migrate    - Применить миграции"
	@echo "make test       - Запустить тесты"
	@echo "make clean      - Очистить временные файлы"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Сервисы запущены! Откройте http://localhost"

down:
	docker-compose down

restart:
	docker-compose restart web

logs:
	docker-compose logs -f web

shell:
	docker-compose exec web python manage.py shell

migrate:
	docker-compose exec web python manage.py migrate

test:
	docker-compose exec web pytest

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache htmlcov .coverage

