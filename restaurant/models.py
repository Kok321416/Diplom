from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Кастомная модель пользователя"""
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
        ('staff', 'Персонал'),
    ]
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр."
    )
    
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Телефон"
    )
    email = models.EmailField(unique=True, verbose_name="Email")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name="Роль")
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    
    def is_admin(self):
        """Проверяет, является ли пользователь администратором"""
        return self.role == 'admin' or self.is_superuser
    
    def is_staff_member(self):
        """Проверяет, является ли пользователь персоналом"""
        return self.role in ['admin', 'staff'] or self.is_staff


class Table(models.Model):
    """Модель стола"""
    ZONE_CHOICES = [
        ('regular', 'Обычная зона'),
        ('vip', 'VIP зона'),
    ]
    
    number = models.CharField(max_length=10, unique=True, verbose_name="Номер стола")
    zone = models.CharField(max_length=10, choices=ZONE_CHOICES, verbose_name="Зона")
    smoking_allowed = models.BooleanField(default=False, verbose_name="Курение разрешено")
    max_seats = models.PositiveIntegerField(verbose_name="Максимальное количество мест")
    floor = models.PositiveIntegerField(default=2, verbose_name="Этаж")
    x_position = models.FloatField(verbose_name="Позиция X на карте")
    y_position = models.FloatField(verbose_name="Позиция Y на карте")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    
    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"
        ordering = ['number']
    
    def __str__(self):
        return f"Стол {self.number} ({self.get_zone_display()})"


class Seat(models.Model):
    """Модель места за столом"""
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='seats', verbose_name="Стол")
    seat_number = models.PositiveIntegerField(verbose_name="Номер места")
    is_available = models.BooleanField(default=True, verbose_name="Доступно")
    
    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"
        unique_together = ['table', 'seat_number']
        ordering = ['table', 'seat_number']
    
    def __str__(self):
        return f"Место {self.seat_number} за столом {self.table.number}"


class Reservation(models.Model):
    """Модель бронирования"""
    STATUS_CHOICES = [
        ('temporary', 'Временное бронирование'),
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
        ('completed', 'Завершено'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations', verbose_name="Пользователь")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations', verbose_name="Стол")
    seats = models.ManyToManyField(Seat, related_name='reservations', verbose_name="Места")
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    duration = models.PositiveIntegerField(default=120, verbose_name="Длительность (минуты)")
    guest_count = models.PositiveIntegerField(verbose_name="Количество гостей")
    is_birthday = models.BooleanField(default=False, verbose_name="День рождения")
    birthday_person_name = models.CharField(max_length=100, blank=True, verbose_name="Имя именинника")
    special_requests = models.TextField(blank=True, verbose_name="Особые пожелания")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='temporary', verbose_name="Статус")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Истекает в")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Бронирование {self.id} - {self.user.phone} на {self.date} в {self.time}"


class BookingPreferences(models.Model):
    """Модель предпочтений бронирования"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='booking_preferences', verbose_name="Пользователь")
    preferred_zone = models.CharField(max_length=10, choices=Table.ZONE_CHOICES, default='regular', verbose_name="Предпочитаемая зона")
    smoking_preference = models.BooleanField(default=False, verbose_name="Предпочитает курящую зону")
    
    class Meta:
        verbose_name = "Предпочтения бронирования"
        verbose_name_plural = "Предпочтения бронирования"
    
    def __str__(self):
        return f"Предпочтения {self.user.phone}"


class Song(models.Model):
    """Модель песни для караоке"""
    title = models.CharField(max_length=200, verbose_name="Название песни")
    artist = models.CharField(max_length=200, verbose_name="Исполнитель")
    duration = models.PositiveIntegerField(verbose_name="Длительность (секунды)")
    is_popular = models.BooleanField(default=False, verbose_name="Популярная песня")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    
    class Meta:
        verbose_name = "Песня"
        verbose_name_plural = "Песни"
        ordering = ['artist', 'title']
    
    def __str__(self):
        return f"{self.artist} - {self.title}"


class KaraokeQueue(models.Model):
    """Модель очереди караоке"""
    STATUS_CHOICES = [
        ('waiting', 'В очереди'),
        ('singing', 'Поет'),
        ('completed', 'Завершено'),
        ('cancelled', 'Отменено'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='karaoke_entries', verbose_name="Пользователь")
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='queue_entries', verbose_name="Песня")
    custom_song_title = models.CharField(max_length=200, blank=True, verbose_name="Название кастомной песни")
    custom_artist = models.CharField(max_length=200, blank=True, verbose_name="Исполнитель кастомной песни")
    position = models.PositiveIntegerField(verbose_name="Позиция в очереди")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting', verbose_name="Статус")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено в очередь")
    started_at = models.DateTimeField(null=True, blank=True, verbose_name="Начато пение")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Завершено")
    
    class Meta:
        verbose_name = "Запись в очереди караоке"
        verbose_name_plural = "Очередь караоке"
        ordering = ['position']
    
    def __str__(self):
        song_title = self.custom_song_title if self.custom_song_title else self.song.title
        artist = self.custom_artist if self.custom_artist else self.song.artist
        return f"{self.user.first_name} {self.user.last_name} - {artist} - {song_title}"
    
    @property
    def display_song(self):
        """Отображаемое название песни"""
        if self.custom_song_title:
            return f"{self.custom_artist} - {self.custom_song_title}"
        return f"{self.song.artist} - {self.song.title}"


class PageContent(models.Model):
    """Модель для управления контентом страниц"""
    PAGE_CHOICES = [
        ('home', 'Главная страница'),
        ('about', 'О ресторане'),
    ]
    
    page = models.CharField(max_length=20, choices=PAGE_CHOICES, unique=True, verbose_name="Страница")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    subtitle = models.TextField(blank=True, verbose_name="Подзаголовок")
    description = models.TextField(verbose_name="Описание")
    services = models.TextField(blank=True, verbose_name="Услуги")
    contacts = models.TextField(blank=True, verbose_name="Контакты")
    history = models.TextField(blank=True, verbose_name="История")
    mission = models.TextField(blank=True, verbose_name="Миссия и ценности")
    team = models.TextField(blank=True, verbose_name="Команда")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    class Meta:
        verbose_name = "Контент страницы"
        verbose_name_plural = "Контент страниц"
        ordering = ['page']
    
    def __str__(self):
        return f"{self.get_page_display()} - {self.title}"


class ContactMessage(models.Model):
    """Модель для сообщений обратной связи"""
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('read', 'Прочитано'),
        ('replied', 'Отвечено'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    subject = models.CharField(max_length=200, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    
    class Meta:
        verbose_name = "Сообщение обратной связи"
        verbose_name_plural = "Сообщения обратной связи"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.get_status_display()})"


class Event(models.Model):
    """Модель мероприятия"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
        ('completed', 'Завершено'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events', verbose_name="Пользователь")
    participants_count = models.IntegerField(verbose_name="Количество участников")
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    
    # Опции для мероприятия
    alcohol = models.BooleanField(default=False, verbose_name="Алкоголь")
    host = models.BooleanField(default=False, verbose_name="Ведущий")
    decoration = models.BooleanField(default=False, verbose_name="Декорации")
    music = models.BooleanField(default=False, verbose_name="Музыкальное сопровождение")
    photographer = models.BooleanField(default=False, verbose_name="Фотограф")
    catering = models.BooleanField(default=False, verbose_name="Кейтеринг")
    sound_equipment = models.BooleanField(default=False, verbose_name="Звуковое оборудование")
    
    # Дополнительная информация
    special_requests = models.TextField(blank=True, verbose_name="Особые пожелания")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Мероприятие от {self.user.username} на {self.date} ({self.participants_count} чел.)"


class SiteContent(models.Model):
    """Модель для управления контентом сайта через админку"""
    CONTENT_TYPE_CHOICES = [
        ('hero', 'Главный баннер'),
        ('about', 'О ресторане'),
        ('services', 'Услуги'),
        ('contact', 'Контакты'),
    ]
    
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, unique=True, verbose_name="Тип контента")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Подзаголовок")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='content/', blank=True, null=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    class Meta:
        verbose_name = "Контент сайта"
        verbose_name_plural = "Контент сайта"
    
    def __str__(self):
        return f"{self.get_content_type_display()}: {self.title}"


class TeamMember(models.Model):
    """Модель для членов команды ресторана"""
    name = models.CharField(max_length=100, verbose_name="Имя")
    position = models.CharField(max_length=100, verbose_name="Должность")
    bio = models.TextField(verbose_name="Биография")
    photo = models.ImageField(upload_to='team/', blank=True, null=True, verbose_name="Фото")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    
    class Meta:
        verbose_name = "Член команды"
        verbose_name_plural = "Команда"
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.position}"


