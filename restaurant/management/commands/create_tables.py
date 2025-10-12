from django.core.management.base import BaseCommand
from restaurant.models import Table, Seat


class Command(BaseCommand):
    help = 'Создает тестовые столы и места для демонстрации'

    def handle(self, *args, **options):
        # Создаем столы
        tables_data = [
            {'number': '1', 'zone': 'regular', 'smoking_allowed': False, 'max_seats': 4, 'floor': 2, 'x_position': 100, 'y_position': 100},
            {'number': '2', 'zone': 'regular', 'smoking_allowed': False, 'max_seats': 6, 'floor': 2, 'x_position': 200, 'y_position': 100},
            {'number': '3', 'zone': 'regular', 'smoking_allowed': False, 'max_seats': 2, 'floor': 2, 'x_position': 300, 'y_position': 100},
            {'number': '4', 'zone': 'vip', 'smoking_allowed': False, 'max_seats': 8, 'floor': 2, 'x_position': 100, 'y_position': 200},
            {'number': '5', 'zone': 'vip', 'smoking_allowed': False, 'max_seats': 6, 'floor': 2, 'x_position': 200, 'y_position': 200},
            {'number': '6', 'zone': 'regular', 'smoking_allowed': True, 'max_seats': 4, 'floor': 2, 'x_position': 300, 'y_position': 200},
            {'number': '7', 'zone': 'regular', 'smoking_allowed': True, 'max_seats': 6, 'floor': 2, 'x_position': 100, 'y_position': 300},
            {'number': '8', 'zone': 'vip', 'smoking_allowed': False, 'max_seats': 10, 'floor': 2, 'x_position': 200, 'y_position': 300},
        ]
        
        created_tables = 0
        created_seats = 0
        
        for table_data in tables_data:
            table, created = Table.objects.get_or_create(
                number=table_data['number'],
                defaults=table_data
            )
            
            if created:
                created_tables += 1
                self.stdout.write(f'Создан стол: {table.number} ({table.get_zone_display()})')
                
                # Создаем места для стола
                for seat_num in range(1, table.max_seats + 1):
                    seat, seat_created = Seat.objects.get_or_create(
                        table=table,
                        seat_number=seat_num,
                        defaults={'is_available': True}
                    )
                    if seat_created:
                        created_seats += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Создано {created_tables} новых столов и {created_seats} мест')
        )

