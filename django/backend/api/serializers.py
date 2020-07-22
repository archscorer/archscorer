from .models import (User,
                     Club,
                     Archer,
                     LevelClass,
                     Course,
                     End,
                     Series,
                     Event,
                     Round,
                     Record,
                     Participant,
                     ScoreCard,
                     Arrow)
from rest_framework import serializers

class EndSerializer(serializers.ModelSerializer):
    class Meta:
        model = End
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
    ends = EndSerializer(many=True)
    class Meta:
        model = Course
        fields = '__all__'

class RoundSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()
    course_type = serializers.SerializerMethodField()
    scorecards = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Round
        fields = '__all__'

    def get_course_name(self, obj):
        return obj.course.name

    def get_course_type(self, obj):
        return obj.course.type

class ArrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arrow
        fields = ['id', 'end', 'ord', 'score', 'x']

# NOTE this is actually slower.. but bandwidth might come into account??
# this becomes useful for series and archived events
# class ParticipantScoreCardSerializer(serializers.ModelSerializer):
#     sum = serializers.SerializerMethodField()
#     x = serializers.SerializerMethodField()
#     class Meta:
#         model = ScoreCard
#         fields = ['round', 'sum', 'x']
#
#     def get_sum(self, obj):
#         return sum(a['score'] for a in obj.arrows.order_by().values('score') if a['score'])
#
#     def get_x(self, obj):
#         return sum(1 for a in obj.arrows.order_by().values('x') if a['x'])

class ParticipantScoreCardSerializer(serializers.ModelSerializer):
    arrows = ArrowSerializer(many=True, read_only=True)
    class Meta:
        model = ScoreCard
        fields = ['id', 'participant', 'round', 'arrows']

class ParticipantArcherSerializer(serializers.ModelSerializer):
    club = serializers.ReadOnlyField(source='club.name_short')
    user = serializers.ReadOnlyField(source='user.is_active')
    contact = serializers.SerializerMethodField()
    events = serializers.SerializerMethodField()
    class Meta:
        model = Archer
        fields = ['id', 'full_name', 'gender', 'club', 'user', 'contact', 'events']

    def get_contact(self, obj):
        if (isinstance(self.root.instance, Event) and
            isinstance(self.context['request'].user, User) and
            self.context['request'].user.email == self.root.instance.creator.email):
            return obj.email + '; ' + obj.phone
        else:
            return None

    def get_events(self, obj):
        return obj.events.all().count()

class ParticipantSerializer(serializers.ModelSerializer):
    archer = ParticipantArcherSerializer(read_only=True)
    scorecards = ParticipantScoreCardSerializer(many=True, read_only=True)
    class Meta:
        model = Participant
        fields = '__all__'

class LevelClassSerializer(serializers.ModelSerializer):
    # this will serialize archer classification classes to be part of archer serializer
    class Meta:
        model = LevelClass
        fields = '__all__'

class ArcherSerializer(serializers.ModelSerializer):
    events = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.is_active')
    level_classes = LevelClassSerializer(many=True, read_only=True)
    class Meta:
        model = Archer
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    archer = ArcherSerializer()
    csrftoken = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'email', 'archer', 'csrftoken']

    def get_csrftoken(self, obj):
        if hasattr(obj, 'csrftoken'):
            return obj.csrftoken
        return None

class ClubsSerializerList(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = '__all__'

    def get_members(self, obj):
        return obj.members.all().count()

class ObjAdminSerializer(serializers.RelatedField):
    class Meta:
        model = User

    def to_representation(self, obj):
        return obj.email

class ClubSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
    members = ArcherSerializer(many=True, read_only=True)
    admins = ObjAdminSerializer(many=True, read_only=True)

    class Meta:
        model = Club
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
    admins = ObjAdminSerializer(many=True, read_only=True)
    participants = ParticipantSerializer(many=True, read_only=True)
    rounds = RoundSerializer(many=True, read_only=True)
    class Meta:
        model = Event
        fields = '__all__'

class EventSerializerList(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
    rounds = RoundSerializer(many=True, read_only=True)
    participants = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = '__all__'

    def get_participants(self, obj):
        return obj.participants.all().count()

class StageSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
    rounds = RoundSerializer(many=True, read_only=True)
    participants = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = '__all__'

    def get_participants(self, obj):
        participants = obj.participants.order_by()
        # root.instance contains series object
        if self.root.instance.participant_restriction:
            try:
                for rule in self.root.instance.participant_restriction.split(','):
                    p, v = rule.split(':')
                    if p[0] == "!":
                        participants = participants.exclude(**{p[1:]: v})
                    else:
                        participants = participants.filter(**{p: v})
            except:
                print('parsing "' + self.root.instance.participant_restriction + '" failed')

        return ParticipantSerializer(instance=participants, many=True).data


class SeriesSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
    stages = StageSerializer(many=True, read_only=True)
    class Meta:
        model = Series
        fields = '__all__'

class SeriesSerializerList(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
    stages = EventSerializerList(many=True, read_only=True)
    class Meta:
        model = Series
        fields = '__all__'

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'
