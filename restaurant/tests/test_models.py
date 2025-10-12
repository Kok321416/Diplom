import pytest
from django.utils import timezone
from datetime import timedelta
from restaurant.models import User, Table, Seat, Reservation, Song, KaraokeQueue, Event


@pytest.mark.django_db
class TestUserModel:
    """Тесты для модели User"""
    
    def test_create_user(self):
        """Тест создания пользователя"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.check_password('testpass123')
    
    def test_user_is_admin(self):
        """Тест проверки роли администратора"""
        admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='admin'
        )
        assert admin.is_admin() is True
        
        regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='user123'
        )
        assert regular_user.is_admin() is False


@pytest.mark.django_db
class TestTableModel:
    """Тесты для модели Table"""
    
    def test_create_table(self):
        """Тест создания стола"""
        table = Table.objects.create(
            number='1',
            zone='regular',
            max_seats=6,
            smoking_allowed=True,
            floor=1
        )
        assert table.number == '1'
        assert table.zone == 'regular'
        assert table.max_seats == 6
        assert table.is_active is True
    
    def test_table_str(self):
        """Тест строкового представления стола"""
        table = Table.objects.create(
            number='5',
            zone='vip',
            max_seats=4
        )
        assert str(table) == 'Стол 5 (VIP зона, 4 мест)'


@pytest.mark.django_db
class TestReservationModel:
    """Тесты для модели Reservation"""
    
    def test_create_reservation(self):
        """Тест создания бронирования"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123'
        )
        table = Table.objects.create(
            number='1',
            zone='regular',
            max_seats=6
        )
        
        reservation = Reservation.objects.create(
            user=user,
            table=table,
            date=timezone.now().date(),
            time=timezone.now().time(),
            guest_count=4,
            status='confirmed'
        )
        
        assert reservation.user == user
        assert reservation.table == table
        assert reservation.guest_count == 4
        assert reservation.status == 'confirmed'


@pytest.mark.django_db
class TestEventModel:
    """Тесты для модели Event"""
    
    def test_create_event(self):
        """Тест создания мероприятия"""
        user = User.objects.create_user(
            username='eventuser',
            email='event@example.com',
            password='event123'
        )
        
        event = Event.objects.create(
            user=user,
            participants_count=30,
            date=timezone.now().date() + timedelta(days=7),
            time=timezone.now().time(),
            alcohol=True,
            host=True,
            music=True
        )
        
        assert event.participants_count == 30
        assert event.alcohol is True
        assert event.host is True
        assert event.status == 'pending'

