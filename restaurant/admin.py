from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import User, Table, Seat, Reservation, BookingPreferences, Song, KaraokeQueue, Event, PageContent, ContactMessage


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('phone', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('phone', 'email', 'first_name', 'last_name')
    ordering = ('phone',)
    
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'password1', 'password2'),
        }),
    )


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'zone_display', 'smoking_display', 'max_seats', 'floor', 'is_active_display')
    list_filter = ('zone', 'smoking_allowed', 'floor', 'is_active')
    search_fields = ('number',)
    ordering = ('number',)
    list_per_page = 25
    
    fieldsets = (
        ('🪑 Основная информация', {
            'fields': ('number', 'zone', 'max_seats', 'floor', 'is_active'),
            'classes': ('wide',)
        }),
        ('🚭 Настройки', {
            'fields': ('smoking_allowed',),
            'classes': ('wide',)
        }),
        ('📍 Позиция на карте', {
            'fields': ('x_position', 'y_position'),
            'classes': ('collapse',)
        }),
    )
    
    def zone_display(self, obj):
        colors = {
            'regular': '#28a745',
            'vip': '#ffc107'
        }
        icons = {
            'regular': '🪑',
            'vip': '👑'
        }
        color = colors.get(obj.zone, '#6c757d')
        icon = icons.get(obj.zone, '🪑')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color,
            icon,
            obj.get_zone_display()
        )
    zone_display.short_description = 'Зона'
    zone_display.admin_order_field = 'zone'
    
    def smoking_display(self, obj):
        if obj.smoking_allowed:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">🚭 Курение</span>'
            )
        else:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">🚫 Нет курения</span>'
            )
    smoking_display.short_description = 'Курение'
    smoking_display.admin_order_field = 'smoking_allowed'
    
    def is_active_display(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">✅ Активен</span>'
            )
        else:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">❌ Неактивен</span>'
            )
    is_active_display.short_description = 'Статус'
    is_active_display.admin_order_field = 'is_active'


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('table', 'seat_number', 'is_available')
    list_filter = ('is_available', 'table__zone')
    search_fields = ('table__number',)
    ordering = ('table', 'seat_number')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_info', 'table_info', 'date', 'time', 'guest_count', 'status_display', 'created_at')
    list_filter = ('status', 'date', 'table__zone', 'is_birthday')
    search_fields = ('user__phone', 'user__email', 'table__number')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25
    
    def user_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><small>{}</small>',
            f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.phone,
            obj.user.email or obj.user.phone
        )
    user_info.short_description = 'Клиент'
    user_info.admin_order_field = 'user__first_name'
    
    def table_info(self, obj):
        colors = {
            'regular': '#28a745',
            'vip': '#ffc107', 
            'bar': '#17a2b8'
        }
        color = colors.get(obj.table.zone, '#6c757d')
        return format_html(
            '<strong>Стол {}</strong><br><span style="color: {}; font-size: 12px;">{}</span>',
            obj.table.number,
            color,
            obj.table.get_zone_display()
        )
    table_info.short_description = 'Стол'
    table_info.admin_order_field = 'table__number'
    
    def status_display(self, obj):
        colors = {
            'pending': '#ffc107',
            'confirmed': '#28a745',
            'cancelled': '#dc3545',
            'completed': '#6c757d'
        }
        color = colors.get(obj.status, '#6c757d')
        icons = {
            'pending': '⏳',
            'confirmed': '✅',
            'cancelled': '❌',
            'completed': '✔️'
        }
        icon = icons.get(obj.status, '❓')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color,
            icon,
            obj.get_status_display()
        )
    status_display.short_description = 'Статус'
    status_display.admin_order_field = 'status'


@admin.register(BookingPreferences)
class BookingPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_zone', 'smoking_preference')
    list_filter = ('preferred_zone', 'smoking_preference')
    search_fields = ('user__phone', 'user__email')


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('artist', 'title', 'duration', 'is_popular', 'is_active')
    list_filter = ('is_popular', 'is_active')
    search_fields = ('artist', 'title')
    ordering = ('artist', 'title')


@admin.register(KaraokeQueue)
class KaraokeQueueAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_song', 'position', 'status', 'added_at')
    list_filter = ('status', 'added_at')
    search_fields = ('user__phone', 'user__first_name', 'user__last_name', 'song__title')
    ordering = ('position',)
    readonly_fields = ('added_at', 'started_at', 'completed_at')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'time', 'participants_count', 'status', 'created_at')
    list_filter = ('status', 'date', 'alcohol', 'host', 'decoration', 'music')
    search_fields = ('user__username', 'user__email', 'special_requests')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'participants_count', 'date', 'time', 'status')
        }),
        ('Дополнительные услуги', {
            'fields': ('alcohol', 'host', 'decoration', 'music', 'photographer', 'catering', 'sound_equipment')
        }),
        ('Пожелания', {
            'fields': ('special_requests',)
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )




@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ('page_display', 'title', 'is_active', 'updated_at')
    list_filter = ('page', 'is_active')
    search_fields = ('title', 'description')
    ordering = ('page',)
    list_per_page = 25
    
    fieldsets = (
        ('📄 Основная информация', {
            'fields': ('page', 'title', 'subtitle', 'description', 'is_active'),
            'classes': ('wide',)
        }),
        ('🏠 Контент главной страницы', {
            'fields': ('services', 'contacts'),
            'classes': ('collapse',)
        }),
        ('ℹ️ Контент страницы "О ресторане"', {
            'fields': ('history', 'mission', 'team'),
            'classes': ('collapse',)
        }),
        ('📊 Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def page_display(self, obj):
        icons = {
            'home': '🏠',
            'about': 'ℹ️'
        }
        icon = icons.get(obj.page, '📄')
        return f"{icon} {obj.get_page_display()}"
    page_display.short_description = 'Страница'
    page_display.admin_order_field = 'page'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status_display', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('👤 Информация о сообщении', {
            'fields': ('name', 'email', 'phone', 'subject', 'status'),
            'classes': ('wide',)
        }),
        ('💬 Содержание сообщения', {
            'fields': ('message',),
            'classes': ('wide',)
        }),
        ('📊 Метаданные', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at',)
    
    actions = ['mark_as_read', 'mark_as_replied']
    
    def status_display(self, obj):
        colors = {
            'new': '#dc3545',
            'read': '#ffc107', 
            'replied': '#28a745'
        }
        icons = {
            'new': '🆕',
            'read': '👁️',
            'replied': '✅'
        }
        color = colors.get(obj.status, '#6c757d')
        icon = icons.get(obj.status, '❓')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color,
            icon,
            obj.get_status_display()
        )
    status_display.short_description = 'Статус'
    status_display.admin_order_field = 'status'
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(status='read')
        self.message_user(request, f'Отмечено как прочитанное: {updated} сообщений')
    mark_as_read.short_description = "📖 Отметить как прочитанное"
    
    def mark_as_replied(self, request, queryset):
        updated = queryset.update(status='replied')
        self.message_user(request, f'Отмечено как отвеченное: {updated} сообщений')
    mark_as_replied.short_description = "✅ Отметить как отвеченное"
