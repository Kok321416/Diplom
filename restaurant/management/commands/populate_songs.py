from django.core.management.base import BaseCommand
from restaurant.models import Song


class Command(BaseCommand):
    help = 'Заполняет базу данных популярными песнями для караоке'

    def handle(self, *args, **options):
        popular_songs = [
            {'artist': 'Queen', 'title': 'Bohemian Rhapsody', 'duration': 355},
            {'artist': 'ABBA', 'title': 'Dancing Queen', 'duration': 230},
            {'artist': 'Elton John', 'title': 'Your Song', 'duration': 241},
            {'artist': 'The Beatles', 'title': 'Let It Be', 'duration': 243},
            {'artist': 'Whitney Houston', 'title': 'I Will Always Love You', 'duration': 273},
            {'artist': 'Celine Dion', 'title': 'My Heart Will Go On', 'duration': 280},
            {'artist': 'Adele', 'title': 'Someone Like You', 'duration': 285},
            {'artist': 'Ed Sheeran', 'title': 'Shape of You', 'duration': 233},
            {'artist': 'Billie Eilish', 'title': 'Bad Guy', 'duration': 194},
            {'artist': 'Dua Lipa', 'title': 'Levitating', 'duration': 203},
        ]

        created_count = 0
        for song_data in popular_songs:
            song, created = Song.objects.get_or_create(
                artist=song_data['artist'],
                title=song_data['title'],
                defaults={
                    'duration': song_data['duration'],
                    'is_popular': True,
                    'is_active': True
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Создана песня: {song.artist} - {song.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Создано {created_count} новых песен из {len(popular_songs)}')
        )

