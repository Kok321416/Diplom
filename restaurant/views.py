from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from .models import User, Table, Seat, Reservation, BookingPreferences, Song, KaraokeQueue, Event
from .forms import CustomUserCreationForm, BookingPreferencesForm, ReservationForm, DirectReservationForm, EventForm


def home(request):
    """Главная страница"""
    return render(request, 'restaurant/home.html')


def booking_choice(request):
    """Страница выбора способа бронирования"""
    return render(request, 'restaurant/booking_choice.html')


def quick_booking(request):
    """Быстрое бронирование за 4 шага"""
    return render(request, 'restaurant/quick_booking.html')


def test(request):
    """Тестовая страница"""
    from django.utils import timezone
    return render(request, 'test.html', {'now': timezone.now()})


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'restaurant/register.html', {'form': form})


def user_login(request):
    """Вход пользователя"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                messages.success(request, 'Добро пожаловать!')
                return redirect('home')
            else:
                messages.error(request, 'Неверный пароль.')
        except User.DoesNotExist:
            messages.error(request, 'Пользователь с таким именем не найден.')
    
    return render(request, 'restaurant/login.html')


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('home')


@login_required
def booking_preferences(request):
    """Страница выбора параметров бронирования"""
    if request.method == 'POST':
        # Сохраняем данные в сессии для передачи на следующий шаг
        guest_count = request.POST.get('guest_count')
        zone = request.POST.get('zone', 'regular')
        is_birthday = request.POST.get('is_birthday') == 'on'
        birthday_person_name = request.POST.get('birthday_person_name', '')
        
        # Сохраняем предпочтения в профиле
        preferences, created = BookingPreferences.objects.get_or_create(
            user=request.user,
            defaults={
                'preferred_zone': zone,
                'smoking_preference': True  # Все зоны для курящих
            }
        )
        if not created:
            preferences.preferred_zone = zone
            preferences.smoking_preference = True  # Все зоны для курящих
            preferences.save()
        
        # Сохраняем данные о дне рождения в сессии
        request.session['is_birthday'] = is_birthday
        request.session['birthday_person_name'] = birthday_person_name
        
        return redirect('table_selection', guest_count=guest_count)
    
    return render(request, 'restaurant/booking_preferences.html')


@login_required
def table_selection(request, guest_count):
    """Страница выбора столов"""
    # Получаем предпочтения пользователя
    try:
        preferences = request.user.booking_preferences
        selected_zone = preferences.preferred_zone
        smoking = preferences.smoking_preference
    except BookingPreferences.DoesNotExist:
        selected_zone = 'regular'
        smoking = False
    
    # Получаем данные о дне рождения из сессии
    is_birthday = request.session.get('is_birthday', False)
    birthday_person_name = request.session.get('birthday_person_name', '')
    
    # Получаем ВСЕ столы для визуализации, но пометим какие можно бронировать
    all_tables = Table.objects.filter(
        is_active=True
    ).prefetch_related('seats')
    
    # Преобразуем QuerySet в список словарей для JSON
    import json
    tables_data = []
    for table in all_tables:
        # Получаем информацию о занятости мест
        all_seats = table.seats.all()
        available_seats_count = table.seats.filter(is_available=True).count()
        has_enough_seats = available_seats_count >= guest_count
        is_in_selected_zone = table.zone == selected_zone
        
        # Список занятых мест (номера)
        occupied_seat_numbers = [
            seat.seat_number for seat in all_seats if not seat.is_available
        ]
        
        # Столик доступен для бронирования только если:
        # 1. Достаточно мест
        # 2. Находится в выбранной пользователем зоне
        can_book = has_enough_seats and is_in_selected_zone
        
        tables_data.append({
            'id': table.id,
            'number': table.number,
            'zone': table.zone,
            'smoking_allowed': table.smoking_allowed,
            'max_seats': table.max_seats,
            'is_available': can_book,
            'available_seats': available_seats_count,
            'occupied_seats': occupied_seat_numbers,  # Список занятых мест
            'has_enough_seats': has_enough_seats,
            'is_in_selected_zone': is_in_selected_zone,
            'floor': table.floor,
            'x_position': table.x_position,
            'y_position': table.y_position
        })
    
    return render(request, 'restaurant/table_selection.html', {
        'tables': json.dumps(tables_data),
        'guest_count': guest_count,
        'selected_zone': selected_zone,
        'is_birthday': is_birthday,
        'birthday_person_name': birthday_person_name
    })


@login_required
def get_table_seats(request, table_id):
    """AJAX запрос для получения мест за столом"""
    table = get_object_or_404(Table, id=table_id)
    seats = table.seats.all()
    
    seats_data = []
    for seat in seats:
        seats_data.append({
            'id': seat.id,
            'seat_number': seat.seat_number,
            'is_available': seat.is_available,
            'x_position': seat.seat_number * 20,  # Простая позиция для демонстрации
            'y_position': 20
        })
    
    return JsonResponse({
        'seats': seats_data,
        'table_number': table.number,
        'max_seats': table.max_seats
    })


@login_required
@require_http_methods(["POST"])
def create_reservation(request):
    """Создание бронирования"""
    try:
        # Проверяем количество активных бронирований пользователя
        active_reservations_count = Reservation.objects.filter(
            user=request.user,
            status__in=['confirmed', 'temporary']
        ).count()
        
        if active_reservations_count >= 2:
            return JsonResponse({'error': 'У вас уже есть 2 активных бронирования. Максимум - 2 бронирования на пользователя.'}, status=400)
        
        data = request.POST
        table_id = data.get('table_id')  # Основной стол (первый выбранный)
        seat_numbers = data.getlist('seat_ids')  # Номера мест
        seat_table_ids = data.getlist('seat_table_ids')  # ID столов для каждого места
        guest_count = int(data.get('guest_count'))
        date = data.get('date')
        time = data.get('time')
        is_birthday = data.get('is_birthday') == 'on'
        birthday_person_name = data.get('birthday_person_name', '')
        special_requests = data.get('special_requests', '')
        
        if not table_id or not seat_numbers or not date or not time:
            return JsonResponse({'error': 'Не все поля заполнены'}, status=400)
        
        # Получаем основной стол
        main_table = get_object_or_404(Table, id=table_id)
        
        # Собираем все места из всех столов
        all_seats = []
        for i, seat_num in enumerate(seat_numbers):
            seat_table_id = seat_table_ids[i] if i < len(seat_table_ids) else table_id
            seat_table = Table.objects.get(id=seat_table_id)
            
            # Ищем место по номеру и столу
            try:
                seat = Seat.objects.get(
                    table=seat_table,
                    seat_number=int(seat_num),
                    is_available=True
                )
                all_seats.append(seat)
            except Seat.DoesNotExist:
                return JsonResponse({'error': f'Место {seat_num} за столом {seat_table.number} уже занято или не существует'}, status=400)
        
        if len(all_seats) != guest_count:
            return JsonResponse({'error': f'Выбрано {len(all_seats)} мест, а нужно {guest_count}'}, status=400)
        
        with transaction.atomic():
            # Создаем временное бронирование
            reservation = Reservation.objects.create(
                user=request.user,
                table=main_table,  # Указываем основной стол
                date=date,
                time=time,
                guest_count=guest_count,
                is_birthday=is_birthday,
                birthday_person_name=birthday_person_name,
                special_requests=special_requests,
                status='temporary',
                expires_at=timezone.now() + timedelta(minutes=10)
            )
            
            # Привязываем все выбранные места (пока не помечаем как занятые)
            for seat in all_seats:
                reservation.seats.add(seat)
        
        return JsonResponse({
            'success': True,
            'reservation_id': reservation.id,
            'redirect_url': f'/reservation-confirmation/{reservation.id}/',
            'message': 'Временное бронирование создано!'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def reservation_confirmation(request, reservation_id):
    """Страница подтверждения бронирования"""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user, status='temporary')
    
    # Проверяем, не истекло ли время
    if reservation.expires_at and timezone.now() > reservation.expires_at:
        # Освобождаем места и удаляем временное бронирование
        for seat in reservation.seats.all():
            seat.is_available = True
            seat.save()
        reservation.delete()
        messages.error(request, 'Время бронирования истекло. Пожалуйста, начните заново.')
        return redirect('booking_preferences')
    
    if request.method == 'POST':
        confirmation_comment = request.POST.get('confirmation_comment', '')
        
        with transaction.atomic():
            # Подтверждаем бронирование
            reservation.status = 'confirmed'
            reservation.special_requests = confirmation_comment
            reservation.expires_at = None  # Убираем время истечения
            reservation.save()
            
            # Помечаем места как занятые
            for seat in reservation.seats.all():
                seat.is_available = False
                seat.save()
        
        messages.success(request, 'Бронирование подтверждено и оплачено!')
        return redirect('reservation_success', reservation_id=reservation.id)
    
    return render(request, 'restaurant/reservation_confirmation.html', {
        'reservation': reservation
    })


@login_required
def reservation_success(request, reservation_id):
    """Страница успешного бронирования"""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    return render(request, 'restaurant/reservation_success.html', {
        'reservation': reservation
    })


@login_required
def my_reservations(request):
    """Мои бронирования"""
    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    
    # Считаем количество активных бронирований
    active_count = Reservation.objects.filter(
        user=request.user,
        status__in=['confirmed', 'temporary']
    ).count()
    
    return render(request, 'restaurant/my_reservations.html', {
        'reservations': reservations,
        'active_count': active_count
    })


@login_required
def edit_reservation(request, reservation_id):
    """Редактирование бронирования"""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    # Можно редактировать только подтвержденные бронирования
    if reservation.status not in ['confirmed', 'temporary']:
        messages.error(request, 'Это бронирование нельзя редактировать.')
        return redirect('my_reservations')
    
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        is_birthday = request.POST.get('is_birthday') == 'on'
        birthday_person_name = request.POST.get('birthday_person_name', '')
        special_requests = request.POST.get('special_requests', '')
        
        # Обновляем бронирование
        reservation.date = date
        reservation.time = time
        reservation.is_birthday = is_birthday
        reservation.birthday_person_name = birthday_person_name
        reservation.special_requests = special_requests
        reservation.save()
        
        messages.success(request, 'Бронирование успешно обновлено!')
        return redirect('my_reservations')
    
    return render(request, 'restaurant/edit_reservation.html', {
        'reservation': reservation
    })


@login_required
def cancel_reservation(request, reservation_id):
    """Отмена бронирования"""
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
        
        # Можно отменить только подтвержденные или временные бронирования
        if reservation.status in ['confirmed', 'temporary']:
            with transaction.atomic():
                # Освобождаем места
                for seat in reservation.seats.all():
                    seat.is_available = True
                    seat.save()
                
                # Меняем статус на отменено
                reservation.status = 'cancelled'
                reservation.save()
            
            messages.success(request, 'Бронирование успешно отменено.')
        else:
            messages.error(request, 'Это бронирование нельзя отменить.')
        
        return redirect('my_reservations')
    
    return redirect('my_reservations')


def karaoke(request):
    """Страница караоке"""
    # Получаем текущую очередь
    queue = KaraokeQueue.objects.filter(status__in=['waiting', 'singing']).order_by('position')
    
    # Получаем популярные песни
    popular_songs = Song.objects.filter(is_popular=True, is_active=True).order_by('artist', 'title')
    
    # Получаем все активные песни
    all_songs = Song.objects.filter(is_active=True).order_by('artist', 'title')
    
    return render(request, 'restaurant/karaoke.html', {
        'queue': queue,
        'popular_songs': popular_songs,
        'all_songs': all_songs
    })


@login_required
def add_to_karaoke_queue(request):
    """Добавление в очередь караоке"""
    if request.method == 'POST':
        song_id = request.POST.get('song_id')
        custom_song_title = request.POST.get('custom_song_title', '').strip()
        custom_artist = request.POST.get('custom_artist', '').strip()
        
        try:
            if song_id:
                # Выбрана существующая песня
                song = get_object_or_404(Song, id=song_id, is_active=True)
                custom_song_title = ''
                custom_artist = ''
            else:
                # Кастомная песня
                if not custom_song_title or not custom_artist:
                    return JsonResponse({'error': 'Укажите название песни и исполнителя'}, status=400)
                
                # Создаем временную песню для кастомной
                song = Song.objects.create(
                    title=custom_song_title,
                    artist=custom_artist,
                    duration=180,  # 3 минуты по умолчанию
                    is_popular=False,
                    is_active=True
                )
            
            # Получаем следующую позицию в очереди
            last_position = KaraokeQueue.objects.filter(status='waiting').order_by('-position').first()
            next_position = (last_position.position + 1) if last_position else 1
            
            # Проверяем, сколько песен пользователь уже добавил в очередь
            user_songs_count = KaraokeQueue.objects.filter(
                user=request.user,
                status__in=['waiting', 'singing']
            ).count()
            
            if user_songs_count >= 3:
                return JsonResponse({'error': 'Вы можете добавить максимум 3 песни в очередь'}, status=400)
            
            # Создаем запись в очереди
            queue_entry = KaraokeQueue.objects.create(
                user=request.user,
                song=song,
                custom_song_title=custom_song_title,
                custom_artist=custom_artist,
                position=next_position
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Вы добавлены в очередь караоке!',
                'position': next_position
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Метод не разрешен'}, status=405)


@login_required
def remove_from_karaoke_queue(request):
    """Удаление конкретной песни из очереди караоке"""
    if request.method == 'POST':
        try:
            queue_id = request.POST.get('queue_id')
            
            if not queue_id:
                return JsonResponse({'error': 'Не указан ID записи'}, status=400)
            
            # Проверяем, что это песня текущего пользователя
            queue_entry = get_object_or_404(
                KaraokeQueue,
                id=queue_id,
                user=request.user,
                status='waiting'
            )
            
            removed_position = queue_entry.position
            
            # Удаляем запись
            queue_entry.delete()
            
            # Обновляем позиции остальных в очереди
            remaining_entries = KaraokeQueue.objects.filter(
                status='waiting',
                position__gt=removed_position
            ).order_by('position')
            
            for i, entry in enumerate(remaining_entries, start=removed_position):
                entry.position = i
                entry.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Песня удалена из очереди'
            })
            
        except KaraokeQueue.DoesNotExist:
            return JsonResponse({'error': 'Песня не найдена или уже исполняется'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Метод не разрешен'}, status=405)


@login_required
def create_event(request):
    """Страница создания мероприятия"""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, 'Ваша заявка на мероприятие принята! Мы свяжемся с вами в ближайшее время.')
            return redirect('my_events')
    else:
        form = EventForm()
    
    return render(request, 'restaurant/create_event.html', {'form': form})


@login_required
def my_events(request):
    """Мои мероприятия"""
    events = Event.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'restaurant/my_events.html', {'events': events})
