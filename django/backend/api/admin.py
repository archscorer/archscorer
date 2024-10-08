from django.contrib import admin
from django.db.models import Count
from django.contrib.auth.admin import UserAdmin

from .models import (User, Club, Archer, Course, End,
                     Participant, Series, Event, Round,
                     Record, Arrow, ScoreCard, Association)

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

# take it out, as it is more trouble than it is worth
# class myParticipantInline(admin.TabularInline):
#     raw_id_fields = ('archer', 'event',)
#     readonly_fields = ('style',)
#     model = Participant

@admin.register(Archer)
class myArcherAdmin(admin.ModelAdmin):
    raw_id_fields = ('club', 'user',)
    list_display = ('full_name', 'id', 'events_count', 'gender', 'email', 'club_name', 'user')
    search_fields = ('full_name', 'club__name', 'club__name_short', 'user__email',)
    # inlines = (myParticipantInline,)

    def club_name(self, obj):
        if isinstance(obj.club, Club):
            return obj.club.name
        else:
            return ''
    club_name.short_description = 'Club'
    club_name.admin_order_field = 'club'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(events_count=Count('events'))  # Assume 'event' is the related name

    def events_count(self, obj):
        return obj.events_count
    events_count.short_description = 'Number of Events'
    events_count.admin_order_field = 'events_count'  # Allow sorting by count

class myArcherInline(admin.TabularInline):
    raw_id_fields = ('club',)
    model = Archer

@admin.register(Club)
class myClubAdmin(admin.ModelAdmin):
    raw_id_fields = ('association',)
    readonly_fields = ('get_association',)
    list_display = ('name','name_short','get_association')

    def get_association(self, obj):
        return [a.id for a in obj.association.all()]


@admin.register(Association)
class myAssociationAdmin(admin.ModelAdmin):
    list_display = ('name',)

class myEndInline(admin.TabularInline):
    model = End

@admin.register(Course)
class myCourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator')
    inlines = (myEndInline,)

@admin.register(Participant)
class myParticipantAdmin(admin.ModelAdmin):
    raw_id_fields = ('archer', 'event')
    list_display = ('archer_name', 'event_name', 'archer_rep', 'style', 'age_group')
    search_fields = ('archer__full_name', 'full_name', 'event__name')

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
    raw_id_fields = ('association', 'series')
    list_display = ('name', 'creator', 'archive',)
    search_fields = ('name', 'tags', 'creator__email')

@admin.register(Series)
class mySeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator')

@admin.register(Record)
class myRecordAdmin(admin.ModelAdmin):
    list_display = ('scope', 'format', 'style', 'gender', 'age_group', 'score', 'archer', 'updated_by', 'updated_at')
    search_fields = ('scope', 'format', 'style', 'age_group', 'archer')

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
