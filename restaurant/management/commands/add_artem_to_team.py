from django.core.management.base import BaseCommand
from restaurant.models import TeamMember


class Command(BaseCommand):
    help = 'Add Artem Andrievsky to the team'

    def handle(self, *args, **options):
        # Добавляем Артема в команду
        member, created = TeamMember.objects.get_or_create(
            name='Андриевский Артем Александрович',
            defaults={
                'position': 'Основатель и CEO',
                'bio': 'Основатель SkyBAR - ресторана для программистов. Создал уникальное пространство, где IT-сообщество может работать, отдыхать и общаться. Связь: @andrievskypsy',
                'order': 0  # Первый в списке
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('[SUCCESS] Artem Andrievsky added to team as CEO'))
        else:
            self.stdout.write(self.style.SUCCESS('[INFO] Artem already exists in team'))
            
        self.stdout.write(self.style.SUCCESS('\nTeam member details:'))
        self.stdout.write(f'Name: {member.name}')
        self.stdout.write(f'Position: {member.position}')
        self.stdout.write(f'Order: {member.order}')
        self.stdout.write(f'Active: {member.is_active}')
        self.stdout.write(f'Telegram: @andrievskypsy')
        
        self.stdout.write(self.style.WARNING('\n[NOTE] To add photo:'))
        self.stdout.write('1. Go to admin panel: http://127.0.0.1:8000/admin')
        self.stdout.write('2. Navigate to Team -> Team Members')
        self.stdout.write('3. Find "Андриевский Артем Александрович"')
        self.stdout.write('4. Click on it and upload photo')
        self.stdout.write('5. Save changes')
