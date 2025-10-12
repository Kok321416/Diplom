"""Health check endpoints для мониторинга"""
from django.http import JsonResponse
from django.db import connections
from django.core.cache import cache
import redis


def health_check(request):
    """Общий health check"""
    health = {
        'status': 'healthy',
        'database': check_database(),
        'cache': check_cache(),
    }
    
    if not all([health['database'], health['cache']]):
        health['status'] = 'unhealthy'
        return JsonResponse(health, status=503)
    
    return JsonResponse(health)


def check_database():
    """Проверка подключения к базе данных"""
    try:
        connections['default'].cursor()
        return True
    except Exception:
        return False


def check_cache():
    """Проверка подключения к Redis"""
    try:
        cache.set('health_check', 'ok', 10)
        return cache.get('health_check') == 'ok'
    except Exception:
        return False

