from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (User, Club, Archer, Participant, Event)

# Register your models here.
@admin.register(User)
class myUserAdmin(UserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(Archer)
class myUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'email', 'club_name')

    def club_name(self, obj):
        if isinstance(obj.club, Club):
            return obj.club.name
        else:
            return ''
    club_name.short_description = 'Club'

@admin.register(Participant)
class myUserAdmin(admin.ModelAdmin):
    list_display = ('archer_name', 'event_name', 'style', 'age_group')

    def archer_name(self, obj):
        return obj.archer.full_name
    archer_name.short_description = 'Archer'

    def event_name(self, obj):
        return obj.event.name
    event_name.short_description = 'Event'

@admin.register(Event)
class myUserAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Club)
class myUserAdmin(admin.ModelAdmin):
    list_display = ('name',)
