from django.urls import path
from . import views
from . import admin_views
from . import health

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('test/', views.test, name='test'),
    path('booking/', views.quick_booking, name='quick_booking'),
    path('booking-choice/', views.booking_choice, name='booking_choice'),
    path('booking-preferences/', views.booking_preferences, name='booking_preferences'),
    path('table-selection/<int:guest_count>/', views.table_selection, name='table_selection'),
    path('api/table/<int:table_id>/seats/', views.get_table_seats, name='get_table_seats'),
    path('api/create-reservation/', views.create_reservation, name='create_reservation'),
    path('reservation-confirmation/<int:reservation_id>/', views.reservation_confirmation, name='reservation_confirmation'),
    path('reservation-success/<int:reservation_id>/', views.reservation_success, name='reservation_success'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('edit-reservation/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('cancel-reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('karaoke/', views.karaoke, name='karaoke'),
    path('api/karaoke/add/', views.add_to_karaoke_queue, name='add_to_karaoke_queue'),
    path('api/karaoke/remove/', views.remove_from_karaoke_queue, name='remove_from_karaoke_queue'),
    path('direct-reservation/', admin_views.direct_reservation, name='direct_reservation'),
    path('admin/', admin_views.admin_panel, name='admin_panel'),
    path('admin/table-selection/', admin_views.admin_table_selection, name='admin_table_selection'),
    path('api/admin/create-reservation/', admin_views.admin_create_reservation, name='admin_create_reservation'),
    path('create-event/', views.create_event, name='create_event'),
    path('my-events/', views.my_events, name='my_events'),
    path('health/', health.health_check, name='health_check'),
]
