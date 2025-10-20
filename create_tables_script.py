#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skybar.settings')
django.setup()

from restaurant.models import Table, Seat

def create_tables():
    """Создает столы для ресторана"""
    
    # Удаляем существующие столы
    Table.objects.all().delete()
    print("Старые столы удалены")
    
    tables_created = 0
    seats_created = 0
    
    # Обычная зона - столы 1-10 (по 6 мест)
    for i in range(1, 11):
        row = (i - 1) // 5
        col = (i - 1) % 5
        
        table = Table.objects.create(
            number=f'{i}',
            zone='regular',
            smoking_allowed=True,
            max_seats=6,
            floor=1,
            x_position=200 + col * 200,
            y_position=150 + row * 150,
            is_active=True
        )
        tables_created += 1
        
        # Создаем места для стола
        for seat_num in range(1, 7):
            Seat.objects.create(
                table=table,
                seat_number=seat_num,
                is_available=True
            )
            seats_created += 1
    
    # VIP зона - столы 11-17
    for i in range(11, 18):
        row = (i - 11) // 4
        col = (i - 11) % 4
        
        max_seats = 2 if i <= 14 else 4
        
        table = Table.objects.create(
            number=f'{i}',
            zone='vip',
            smoking_allowed=True,
            max_seats=max_seats,
            floor=1,
            x_position=300 + col * 200,
            y_position=500 + row * 150,
            is_active=True
        )
        tables_created += 1
        
        for seat_num in range(1, max_seats + 1):
            Seat.objects.create(
                table=table,
                seat_number=seat_num,
                is_available=True
            )
            seats_created += 1
    
    # Барная зона - столы 18-25
    for i in range(18, 26):
        table = Table.objects.create(
            number=f'{i}',
            zone='bar',
            smoking_allowed=True,
            max_seats=1,
            floor=1,
            x_position=50,
            y_position=150 + (i-18) * 60,
            is_active=True
        )
        tables_created += 1
        
        Seat.objects.create(
            table=table,
            seat_number=1,
            is_available=True
        )
        seats_created += 1
    
    print(f"Создано {tables_created} столов и {seats_created} мест")
    print("Столы успешно созданы!")

if __name__ == "__main__":
    create_tables()
