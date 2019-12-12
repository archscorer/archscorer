from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (User, Club, Archer, Course, End, Participant, Event, Round)

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

@admin.register(Club)
class myClubAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Archer)
class myArcherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'email', 'club_name', 'user')

    def club_name(self, obj):
        if isinstance(obj.club, Club):
            return obj.club.name
        else:
            return ''
    club_name.short_description = 'Club'

@admin.register(Course)
class myCourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator')

@admin.register(End)
class myEndAdmin(admin.ModelAdmin):
    list_display = ('has_label', 'course_name')

    def has_label(self, obj):
        if obj.label:
            return obj.label
        else:
            return '..no label..'
    has_label.short_description = 'Label for End'

    def course_name(self, obj):
        if isinstance(obj.course, Course):
            return obj.course.name
        else:
            return ''
    course_name.short_description = 'Course'

@admin.register(Participant)
class myParticipantAdmin(admin.ModelAdmin):
    list_display = ('archer_name', 'event_name', 'style', 'age_group')

    def archer_name(self, obj):
        return obj.archer.full_name
    archer_name.short_description = 'Archer'

    def event_name(self, obj):
        return obj.event.name
    event_name.short_description = 'Event'

@admin.register(Event)
class myEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator')

@admin.register(Round)
class myRoundAdmin(admin.ModelAdmin):
    list_display = ('has_label', 'event_name', 'course_name')

    def has_label(self, obj):
        if obj.label:
            return obj.label
        else:
            return '..no label..'
    has_label.short_description = 'Label for Round'

    def event_name(self, obj):
        if isinstance(obj.event, Event):
            return str(obj.id) + ': ' + obj.event.name
        else:
            return ''
    event_name.short_description = 'Event'

    def course_name(self, obj):
        if isinstance(obj.course, Course):
            return obj.course.name
        else:
            return ''
    course_name.short_description = 'Course'
