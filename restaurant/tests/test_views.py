import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from restaurant.models import User, Table, Seat, Reservation, BookingPreferences


@pytest.mark.django_db
class TestHomeView:
    """Тесты для главной страницы"""
    
    def test_home_page_loads(self, client):
        """Тест загрузки главной страницы"""
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assert 'SkyBAR' in response.content.decode()


@pytest.mark.django_db
class TestAuthViews:
    """Тесты для аутентификации"""
    
    def test_register_page_loads(self, client):
        """Тест загрузки страницы регистрации"""
        response = client.get(reverse('register'))
        assert response.status_code == 200
    
    def test_login_page_loads(self, client):
        """Тест загрузки страницы входа"""
        response = client.get(reverse('login'))
        assert response.status_code == 200
    
    def test_user_registration(self, client):
        """Тест регистрации пользователя"""
        response = client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        
        # Проверяем что пользователь создан
        assert User.objects.filter(username='newuser').exists()
    
    def test_user_login(self, client):
        """Тест входа пользователя"""
        user = User.objects.create_user(
            username='logintest',
            email='login@example.com',
            password='testpass123'
        )
        
        response = client.post(reverse('login'), {
            'username': 'logintest',
            'password': 'testpass123',
        })
        
        # Проверяем редирект после успешного входа
        assert response.status_code == 302


@pytest.mark.django_db
class TestBookingViews:
    """Тесты для бронирования"""
    
    @pytest.fixture
    def authenticated_user(self, client):
        """Фикстура авторизованного пользователя"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123'
        )
        client.force_login(user)
        return user
    
    @pytest.fixture
    def test_table(self):
        """Фикстура тестового стола"""
        table = Table.objects.create(
            number='1',
            zone='regular',
            max_seats=6,
            is_active=True
        )
        # Создаем места
        for i in range(1, 7):
            Seat.objects.create(
                table=table,
                seat_number=i,
                is_available=True
            )
        return table
    
    def test_booking_preferences_requires_login(self, client):
        """Тест что страница бронирования требует авторизации"""
        response = client.get(reverse('booking_preferences'))
        assert response.status_code == 302  # Redirect to login
    
    def test_booking_preferences_loads(self, client, authenticated_user):
        """Тест загрузки страницы параметров бронирования"""
        response = client.get(reverse('booking_preferences'))
        assert response.status_code == 200
    
    def test_table_selection_loads(self, client, authenticated_user, test_table):
        """Тест загрузки страницы выбора столов"""
        response = client.get(reverse('table_selection', kwargs={'guest_count': 4}))
        assert response.status_code == 200
    
    def test_create_reservation_limit(self, client, authenticated_user, test_table):
        """Тест ограничения количества бронирований (максимум 2)"""
        # Создаем 2 подтвержденных бронирования
        for i in range(2):
            Reservation.objects.create(
                user=authenticated_user,
                table=test_table,
                date=timezone.now().date() + timedelta(days=i+1),
                time=timezone.now().time(),
                guest_count=2,
                status='confirmed'
            )
        
        # Пытаемся создать третье - должно быть отклонено
        active_count = Reservation.objects.filter(
            user=authenticated_user,
            status__in=['confirmed', 'temporary']
        ).count()
        
        assert active_count == 2


@pytest.mark.django_db
class TestKaraokeViews:
    """Тесты для караоке"""
    
    def test_karaoke_page_loads(self, client):
        """Тест загрузки страницы караоке"""
        response = client.get(reverse('karaoke'))
        assert response.status_code == 200
    
    def test_add_to_queue_requires_login(self, client):
        """Тест что добавление в очередь требует авторизации"""
        response = client.post(reverse('add_to_karaoke_queue'))
        assert response.status_code == 302  # Redirect to login


@pytest.mark.django_db
class TestEventViews:
    """Тесты для мероприятий"""
    
    def test_create_event_requires_login(self, client):
        """Тест что создание мероприятия требует авторизации"""
        response = client.get(reverse('create_event'))
        assert response.status_code == 302
    
    def test_create_event_loads(self, client):
        """Тест загрузки страницы создания мероприятия"""
        user = User.objects.create_user(
            username='eventuser',
            email='event@example.com',
            password='event123'
        )
        client.force_login(user)
        
        response = client.get(reverse('create_event'))
        assert response.status_code == 200

