from django.core.management.base import BaseCommand
from restaurant.models import SiteContent, TeamMember


class Command(BaseCommand):
    help = 'Populate initial site content and team members'

    def handle(self, *args, **options):
        # Создаем начальный контент для главной страницы
        hero, created = SiteContent.objects.get_or_create(
            content_type='hero',
            defaults={
                'title': 'SkyBAR - Ресторан для программистов',
                'subtitle': 'Место где код встречается с кухней',
                'description': 'Уникальное место, где собираются те, кто любит программирование. '
                              'Здесь вы можете не только насладиться отличной кухней, но и обсудить '
                              'последние технологии, поделиться опытом и найти единомышленников.',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('[OK] Hero content created'))

        services, created = SiteContent.objects.get_or_create(
            content_type='services',
            defaults={
                'title': 'О SkyBAR',
                'subtitle': '',
                'description': 'SkyBAR — это не просто ресторан, это место силы для IT-сообщества. '
                              'Мы понимаем специфику работы программистов и создали пространство, '
                              'где можно не только поесть, но и поработать, провести встречу или '
                              'просто отдохнуть в кругу единомышленников.',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('[OK] Services content created'))

        contact, created = SiteContent.objects.get_or_create(
            content_type='contact',
            defaults={
                'title': 'Режим работы',
                'subtitle': '',
                'description': 'Пн - Чт: 10:00 - 02:00\nПт - Вс: 10:00 - 04:00\n\nТелефон: +7 (950) 068-95-64',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('[OK] Contact content created'))

        # Создаем контент для страницы "О ресторане"
        about, created = SiteContent.objects.get_or_create(
            content_type='about',
            defaults={
                'title': 'О SkyBAR',
                'subtitle': 'Место встречи программистов',
                'description': '''Наша история

SkyBAR был создан в 2024 году группой программистов, которые мечтали о месте, где IT-сообщество могло бы собираться не только для работы, но и для отдыха. Мы понимаем уникальные потребности разработчиков, инженеров и всех, кто связан с технологиями.

Наше пространство оснащено всем необходимым: быстрым интернетом, удобными рабочими местами, розетками у каждого стола и зонами для проведения встреч. При этом мы не забываем о главном — отличной кухне и напитках, которые помогают создавать лучший код.

Наша миссия

Создать комфортное пространство, где технологии встречаются с гастрономией, а программисты могут работать, общаться и отдыхать в атмосфере взаимопонимания и поддержки.''',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('[OK] About content created'))

        # Создаем примеры членов команды
        team_members = [
            {
                'name': 'Артём Иванов',
                'position': 'Шеф-повар',
                'bio': 'Мастер кулинарии с 10-летним опытом. Специализируется на европейской кухне и экспериментирует с fusion-блюдами.',
                'order': 1
            },
            {
                'name': 'Мария Петрова',
                'position': 'Менеджер зала',
                'bio': 'Профессионал в сфере гостеприимства. Создает атмосферу уюта и заботится о каждом госте.',
                'order': 2
            },
            {
                'name': 'Дмитрий Сидоров',
                'position': 'IT-менеджер',
                'bio': 'Следит за инфраструктурой, Wi-Fi и всеми техническими аспектами ресторана.',
                'order': 3
            },
        ]

        for member_data in team_members:
            member, created = TeamMember.objects.get_or_create(
                name=member_data['name'],
                defaults=member_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] Team member {member.name} added'))

        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] All initial data created!'))

