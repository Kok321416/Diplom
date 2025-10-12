from django.core.management.base import BaseCommand
from restaurant.models import Table, Seat


class Command(BaseCommand):
    help = 'Пересоздает столы и места согласно новой схеме'

    def handle(self, *args, **options):
        # Удаляем старые столы
        Table.objects.all().delete()
        self.stdout.write('Старые столы удалены')
        
        tables_created = 0
        seats_created = 0
        
        # Обычная зона - верхняя половина (столы 1-10)
        # 10 столов на 6 мест каждый, подняли выше
        for i in range(1, 11):
            row = (i - 1) // 5  # 5 столов в ряду
            col = (i - 1) % 5   # 5 столбцов
            
            table = Table.objects.create(
                number=f'{i}',
                zone='regular',
                smoking_allowed=True,  # Все зоны для курящих
                max_seats=6,
                floor=1,
                x_position=200 + col * 200,
                y_position=150 + row * 150,  # Подняли выше
                is_active=True
            )
            tables_created += 1
            
            for seat_num in range(1, 7):
                Seat.objects.create(
                    table=table,
                    seat_number=seat_num,
                    is_available=True
                )
                seats_created += 1
        
        # VIP зона - нижняя половина (столы 11-17)
        # 4 стола по 2 места + 3 стола по 4 места
        for i in range(11, 18):
            row = (i - 11) // 4  # 4 стола в ряду
            col = (i - 11) % 4   # 4 столбца
            
            # Первые 4 стола по 2 места, остальные по 4 места
            max_seats = 2 if i <= 14 else 4
            
            table = Table.objects.create(
                number=f'{i}',
                zone='vip',
                smoking_allowed=True,  # Все зоны для курящих
                max_seats=max_seats,
                floor=1,
                x_position=300 + col * 200,  # Сдвинули правее
                y_position=500 + row * 150,  # Нижняя половина
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
        
        # Барная зона - возле сцены (столы 18-25)
        # 8 барных мест возле сцены
        for i in range(18, 26):
            table = Table.objects.create(
                number=f'{i}',
                zone='bar',
                smoking_allowed=True,  # Все зоны для курящих
                max_seats=1,
                floor=1,
                x_position=50,  # Возле сцены (левая сторона)
                y_position=150 + (i-18) * 60,  # Вертикально
                is_active=True
            )
            tables_created += 1
            
            Seat.objects.create(
                table=table,
                seat_number=1,
                is_available=True
            )
            seats_created += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Создано {tables_created} столов и {seats_created} мест\n'
                f'- 10 столов по 6 мест (обычная зона, верх)\n'
                f'- 4 стола по 2 места + 3 стола по 4 места (VIP зона, низ)\n'
                f'- 8 барных мест (возле сцены, слева)'
            )
        )