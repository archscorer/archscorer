from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (User, Club, Archer, Course, End,
                     Participant, Series, Event, EventDescription,
                     Round, Record, LevelClass, Arrow, ScoreCard)

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
    list_display = ('email', 'id', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

class myParticipantInline(admin.TabularInline):
    raw_id_fields = ('archer', 'event')
    model = Participant

@admin.register(Archer)
class myArcherAdmin(admin.ModelAdmin):
    raw_id_fields = ('club', 'user')
    list_display = ('full_name', 'id', 'gender', 'email', 'club_name', 'user')
    search_fields = ('full_name', 'club__name')
    inlines = (myParticipantInline,)

    def club_name(self, obj):
        if isinstance(obj.club, Club):
            return obj.club.name
        else:
            return ''
    club_name.short_description = 'Club'
    club_name.admin_order_field = 'club'

class myArcherInline(admin.TabularInline):
    raw_id_fields = ('club',)
    model = Archer

@admin.register(Club)
class myClubAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # inlines = (myArcherInline,)

class myEndInline(admin.TabularInline):
    model = End

@admin.register(Course)
class myCourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator')
    inlines = (myEndInline,)

@admin.register(Participant)
class myParticipantAdmin(admin.ModelAdmin):
    raw_id_fields = ('archer', 'event')
    list_display = ('archer_name', 'event_name', 'style', 'age_group')
    search_fields = ('archer__full_name', 'event__name')

    def archer_name(self, obj):
        return obj.archer.full_name + '[' + str(obj.archer.id) + ']'
    archer_name.short_description = 'Archer'
    archer_name.admin_order_field = 'archer__full_name'

    def event_name(self, obj):
        return obj.event.name
    event_name.short_description = 'Event'
    event_name.admin_order_field = 'event'

@admin.register(Event)
class myEventAdmin(admin.ModelAdmin):
    raw_id_fields = ('series',)
    list_display = ('name', 'creator', 'archive')
    search_fields = ('name', 'tags')

@admin.register(EventDescription)
class myEventDescriptionAdmin(admin.ModelAdmin):
    raw_id_fields = ('event',)

@admin.register(Series)
class mySeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator')

@admin.register(LevelClass)
class myLevelClassAdmin(admin.ModelAdmin):
    raw_id_fields = ('archer',)
    list_display = ('archer', 'level', 'age_group', 'style')

@admin.register(Record)
class myRecordAdmin(admin.ModelAdmin):
    list_display = ('scope', 'format', 'style', 'gender', 'age_group', 'score', 'archer', 'updated_by', 'updated_at')
    search_fields = ('scope', 'format', 'style', 'age_group')

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
            return str(obj.ord) + ': ' + obj.event.name
        else:
            return ''
    event_name.short_description = 'Event'
    event_name.admin_order_field = 'event'

    def course_name(self, obj):
        if isinstance(obj.course, Course):
            return obj.course.name
        else:
            return ''
    course_name.short_description = 'Course'
    course_name.admin_order_field = 'course'

class myArrowInline(admin.TabularInline):
    model = Arrow

@admin.register(ScoreCard)
class myScoreCardAdmin(admin.ModelAdmin):
    raw_id_fields = ('participant', 'round')
    list_display = ('participant_name', 'event_name', 'course_name', 'sum')
    search_fields = ('participant__archer__full_name', 'participant__event__name')
    inlines = (myArrowInline,)

    def participant_name(self, obj):
        if isinstance(obj.participant, Participant):
            return obj.participant.archer.full_name
        else:
            return ''
    participant_name.short_description = 'Archer'
    participant_name.admin_order_field = 'participant__archer'

    def event_name(self, obj):
        if isinstance(obj.round.event, Event):
            return obj.round.event.name + (' (Archived)' if obj.round.event.archive else '')
        else:
            return ''
    event_name.short_description = 'Event'
    event_name.admin_order_field = 'round__event'

    def course_name(self, obj):
        if isinstance(obj.round.course, Course):
            return obj.round.course.name
        else:
            return ''
    course_name.short_description = 'Course'
    course_name.admin_order_field = 'round__course'

    def sum(self, obj):
        scores = [a.score for a in obj.arrows.all() if a.score is not None]
        if scores:
            return sum(scores)
        return '-'
    sum.short_description = 'Score'
