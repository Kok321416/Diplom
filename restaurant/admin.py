from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Table, Seat, Reservation, BookingPreferences, Song, KaraokeQueue, Event, SiteContent, TeamMember, ContactMessage


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
    list_display = ('number', 'zone', 'smoking_allowed', 'max_seats', 'floor', 'is_active')
    list_filter = ('zone', 'smoking_allowed', 'floor', 'is_active')
    search_fields = ('number',)
    ordering = ('number',)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('table', 'seat_number', 'is_available')
    list_filter = ('is_available', 'table__zone')
    search_fields = ('table__number',)
    ordering = ('table', 'seat_number')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'table', 'date', 'time', 'guest_count', 'status', 'created_at')
    list_filter = ('status', 'date', 'table__zone', 'is_birthday')
    search_fields = ('user__phone', 'user__email', 'table__number')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


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


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'title', 'is_active', 'updated_at')
    list_filter = ('content_type', 'is_active')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('content_type', 'title', 'subtitle', 'description', 'image', 'is_active')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order', 'is_active')
    list_filter = ('is_active', 'position')
    search_fields = ('name', 'position', 'bio')
    ordering = ('order', 'name')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'position', 'bio', 'photo', 'order', 'is_active')
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Отметить как прочитанное"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Отметить как непрочитанное"
