from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db import transaction
from .models import User, Table, Seat, Reservation
from .forms import DirectReservationForm


@login_required
def direct_reservation(request):
    """Прямое бронирование для пользователей"""
    if request.method == 'POST':
        form = DirectReservationForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Создаем бронирование
                    reservation = form.save(commit=False)
                    reservation.user = request.user
                    reservation.status = 'confirmed'  # Прямое подтверждение
                    reservation.save()
                    
                    # Помечаем места как занятые (автоматически для выбранного стола)
                    table = reservation.table
                    available_seats = table.seats.filter(is_available=True)[:reservation.guest_count]
                    
                    for seat in available_seats:
                        reservation.seats.add(seat)
                        seat.is_available = False
                        seat.save()
                
                messages.success(request, f'Бронирование создано успешно! Номер бронирования: #{reservation.id}')
                return redirect('home')
                
            except Exception as e:
                messages.error(request, f'Ошибка при создании бронирования: {str(e)}')
    else:
        form = DirectReservationForm(user=request.user)
    
    return render(request, 'restaurant/direct_reservation.html', {'form': form})


@login_required
def admin_panel(request):
    """Админ-панель для управления бронированиями"""
    if not request.user.is_admin():
        messages.error(request, 'У вас нет прав доступа к админ-панели')
        return redirect('home')
    
    # Получаем все бронирования
    reservations = Reservation.objects.all().order_by('-created_at')
    
    # Статистика
    total_reservations = reservations.count()
    confirmed_reservations = reservations.filter(status='confirmed').count()
    pending_reservations = reservations.filter(status='pending').count()
    today_reservations = reservations.filter(date=timezone.now().date()).count()
    
    context = {
        'reservations': reservations,
        'total_reservations': total_reservations,
        'confirmed_reservations': confirmed_reservations,
        'pending_reservations': pending_reservations,
        'today_reservations': today_reservations,
    }
    
    return render(request, 'restaurant/admin_panel.html', context)


@login_required
def admin_table_selection(request):
    """Админ-панель для выбора столов"""
    if not request.user.is_admin():
        messages.error(request, 'У вас нет прав доступа к админ-панели')
        return redirect('home')
    
    # Получаем все столы
    tables = Table.objects.filter(is_active=True).prefetch_related('seats')
    
    # Добавляем информацию о доступных местах
    for table in tables:
        available_seats = table.seats.filter(is_available=True).count()
        table.available_seats = available_seats
    
    return render(request, 'restaurant/admin_table_selection.html', {'tables': tables})


@login_required
def admin_create_reservation(request):
    """Создание бронирования администратором"""
    if not request.user.is_admin():
        return JsonResponse({'error': 'Нет прав доступа'}, status=403)
    
    if request.method == 'POST':
        try:
            data = request.POST
            table_id = data.get('table_id')
            seat_ids = data.getlist('seat_ids')
            guest_count = int(data.get('guest_count'))
            date = data.get('date')
            time = data.get('time')
            is_birthday = data.get('is_birthday') == 'on'
            birthday_person_name = data.get('birthday_person_name', '')
            special_requests = data.get('special_requests', '')
            user_phone = data.get('user_phone', '').strip()
            
            if not table_id or not seat_ids or not date or not time:
                return JsonResponse({'error': 'Не все поля заполнены'}, status=400)
            
            # Находим пользователя по телефону или создаем временного
            if user_phone:
                try:
                    user = User.objects.get(phone=user_phone)
                except User.DoesNotExist:
                    # Создаем временного пользователя
                    user = User.objects.create(
                        phone=user_phone,
                        email=f'temp_{user_phone}@skybar.ru',
                        username=f'temp_{user_phone}',
                        first_name='Гость',
                        last_name='Ресторана'
                    )
            else:
                user = request.user  # Админ создает бронирование от своего имени
            
            table = get_object_or_404(Table, id=table_id)
            seats = Seat.objects.filter(id__in=seat_ids, table=table, is_available=True)
            
            if len(seats) != len(seat_ids):
                return JsonResponse({'error': 'Некоторые места уже заняты'}, status=400)
            
            if len(seats) != guest_count:
                return JsonResponse({'error': 'Количество мест не соответствует количеству гостей'}, status=400)
            
            with transaction.atomic():
                # Создаем бронирование
                reservation = Reservation.objects.create(
                    user=user,
                    table=table,
                    date=date,
                    time=time,
                    guest_count=guest_count,
                    is_birthday=is_birthday,
                    birthday_person_name=birthday_person_name,
                    special_requests=special_requests,
                    status='confirmed'  # Админ сразу подтверждает
                )
                
                # Привязываем места и помечаем их как занятые
                for seat in seats:
                    reservation.seats.add(seat)
                    seat.is_available = False
                    seat.save()
            
            return JsonResponse({
                'success': True,
                'reservation_id': reservation.id,
                'message': f'Бронирование создано для {user.phone}!'
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Метод не разрешен'}, status=405)
