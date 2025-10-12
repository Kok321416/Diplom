from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import User, Reservation, BookingPreferences, Table, Event


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        }),
        label='Имя пользователя'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@email.com'
        }),
        label='Email'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        }),
        label='Пароль'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        }),
        label='Подтверждение пароля'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email
    


class BookingPreferencesForm(forms.ModelForm):
    """Форма предпочтений бронирования"""
    guest_count = forms.IntegerField(
        min_value=1,
        max_value=12,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Количество гостей'
        }),
        label='Количество гостей'
    )
    zone = forms.ChoiceField(
        choices=BookingPreferences._meta.get_field('preferred_zone').choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Зона'
    )
    smoking_preference = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Курящая зона'
    )

    class Meta:
        model = BookingPreferences
        fields = ('preferred_zone', 'smoking_preference')


class ReservationForm(forms.ModelForm):
    """Форма бронирования"""
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Дата'
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time'
        }),
        label='Время'
    )
    is_birthday = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='День рождения'
    )
    birthday_person_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя именинника'
        }),
        label='Имя именинника'
    )
    special_requests = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Особые пожелания'
        }),
        label='Особые пожелания'
    )

    class Meta:
        model = Reservation
        fields = ('date', 'time', 'is_birthday', 'birthday_person_name', 'special_requests')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.guest_count = kwargs.pop('guest_count', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        is_birthday = cleaned_data.get('is_birthday')
        birthday_person_name = cleaned_data.get('birthday_person_name')

        if is_birthday and not birthday_person_name:
            raise ValidationError('Укажите имя именинника, если это день рождения.')

        return cleaned_data


class DirectReservationForm(forms.ModelForm):
    """Форма прямого бронирования для пользователей"""
    guest_count = forms.IntegerField(
        min_value=1,
        max_value=12,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Количество гостей'
        }),
        label='Количество гостей'
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Дата'
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time'
        }),
        label='Время'
    )
    table = forms.ModelChoiceField(
        queryset=Table.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Стол',
        empty_label="Выберите стол"
    )
    is_birthday = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='День рождения'
    )
    birthday_person_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя именинника'
        }),
        label='Имя именинника'
    )
    special_requests = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Особые пожелания'
        }),
        label='Особые пожелания'
    )

    class Meta:
        model = Reservation
        fields = ('guest_count', 'date', 'time', 'table', 'is_birthday', 'birthday_person_name', 'special_requests')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Фильтруем доступные столы
        self.fields['table'].queryset = Table.objects.filter(is_active=True)
        
        # Устанавливаем минимальную дату на сегодня
        today = timezone.now().date()
        self.fields['date'].widget.attrs['min'] = today.strftime('%Y-%m-%d')

    def clean(self):
        cleaned_data = super().clean()
        is_birthday = cleaned_data.get('is_birthday')
        birthday_person_name = cleaned_data.get('birthday_person_name')
        table = cleaned_data.get('table')
        guest_count = cleaned_data.get('guest_count')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if is_birthday and not birthday_person_name:
            raise ValidationError('Укажите имя именинника, если это день рождения.')

        if table and guest_count:
            if guest_count > table.max_seats:
                raise ValidationError(f'Максимальное количество мест за столом {table.number}: {table.max_seats}')

        if date and date < timezone.now().date():
            raise ValidationError('Дата не может быть в прошлом.')

        return cleaned_data


class EventForm(forms.ModelForm):
    """Форма организации мероприятия"""
    participants_count = forms.IntegerField(
        min_value=1,
        max_value=50,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Количество участников (до 50)'
        }),
        label='Количество участников'
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Дата мероприятия'
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time'
        }),
        label='Время начала'
    )
    alcohol = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Алкоголь'
    )
    host = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Ведущий'
    )
    decoration = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Декорации'
    )
    music = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Музыкальное сопровождение'
    )
    photographer = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Фотограф'
    )
    catering = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Кейтеринг'
    )
    sound_equipment = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Звуковое оборудование'
    )
    special_requests = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Опишите ваши особые пожелания...'
        }),
        label='Особые пожелания'
    )
    
    class Meta:
        model = Event
        fields = [
            'participants_count', 'date', 'time', 'alcohol', 'host', 
            'decoration', 'music', 'photographer', 'catering', 
            'sound_equipment', 'special_requests'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем минимальную дату на сегодня
        today = timezone.now().date()
        self.fields['date'].widget.attrs['min'] = today.strftime('%Y-%m-%d')
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < timezone.now().date():
            raise ValidationError('Дата не может быть в прошлом.')
        return date
