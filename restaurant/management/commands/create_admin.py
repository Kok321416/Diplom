from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает администратора с логином admin и паролем admin'

    def handle(self, *args, **options):
        # Создаем или обновляем администратора
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'phone': '+79999999999',
                'email': 'admin@skybar.ru',
                'first_name': 'Администратор',
                'last_name': 'SkyBAR',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        
        if created:
            admin_user.set_password('admin')
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS('Администратор создан успешно!')
            )
            self.stdout.write('Логин: admin')
            self.stdout.write('Пароль: admin')
            self.stdout.write('Телефон: +79999999999')
        else:
            # Обновляем пароль если пользователь уже существует
            admin_user.set_password('admin')
            admin_user.role = 'admin'
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS('Администратор обновлен!')
            )
            self.stdout.write('Логин: admin')
            self.stdout.write('Пароль: admin')

