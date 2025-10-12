"""Pytest fixtures для тестов"""
import pytest
from restaurant.models import User, Table, Seat


@pytest.fixture
def user_factory():
    """Фабрика для создания пользователей"""
    def create_user(username='testuser', email='test@example.com', password='test123', **kwargs):
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **kwargs
        )
    return create_user


@pytest.fixture
def table_factory():
    """Фабрика для создания столов"""
    def create_table(number='1', zone='regular', max_seats=6, **kwargs):
        table = Table.objects.create(
            number=number,
            zone=zone,
            max_seats=max_seats,
            **kwargs
        )
        # Автоматически создаем места
        for i in range(1, max_seats + 1):
            Seat.objects.create(
                table=table,
                seat_number=i,
                is_available=True
            )
        return table
    return create_table


@pytest.fixture
def authenticated_client(client, user_factory):
    """Клиент с авторизованным пользователем"""
    user = user_factory()
    client.force_login(user)
    return client, user

