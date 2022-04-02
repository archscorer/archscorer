from .models import (User,
                     Association,
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

class AssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Association
        fields = ['name', 'name_short']

class EndSerializer(serializers.ModelSerializer):
    class Meta:
        model = End
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
    ends = EndSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = '__all__'

class CourseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'type', 'description', 'location', 'halves', 'format']


class RoundSerializer(serializers.ModelSerializer):
    course_details = serializers.SerializerMethodField()
    scorecards = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Round
        fields = '__all__'

    def get_course_details(self, obj):
        return CourseDetailsSerializer(instance=obj.course).data

class ArrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arrow
        fields = ['id', 'end', 'ord', 'score', 'x']

class LevelClassSerializer(serializers.ModelSerializer):
    # this will serialize archer classification classes to be part of archer serializer
    class Meta:
        model = LevelClass
        fields = '__all__'

class ParticipantScoreCardSerializer(serializers.ModelSerializer):
    last_arrow = serializers.SerializerMethodField()
    class Meta:
        model = ScoreCard
        fields = '__all__'

    def get_last_arrow(self, obj):
        if obj.round.course.type == 's':
            return obj.arrows.all().last().score
        return None

class ScoreCardSerializer(serializers.ModelSerializer):
    arrows = ArrowSerializer(many=True, read_only=True)
    class Meta:
        model = ScoreCard
        fields = '__all__'

class ClubDetailsSerializer(serializers.ModelSerializer):
    association = AssociationSerializer(many=True, read_only=True)
    class Meta:
        model = Club
        fields = ['id', 'name', 'name_short', 'association']

class ArcherSerializer(serializers.ModelSerializer):
    events = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.is_active')
    level_classes = LevelClassSerializer(many=True, read_only=True)
    class Meta:
        model = Archer
        fields = '__all__'

class ParticipantArcherSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.is_active')
    club_details = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()
    class Meta:
        model = Archer
        fields = ['id', 'full_name', 'gender', 'club_details', 'user', 'contact']

    def get_contact(self, obj):
        try:
            # NOTE this assumes that root.instance is Event object
            if self.context['request'].user.email == self.root.instance.creator.email:
                return obj.email + '; ' + obj.phone
        except (AttributeError, KeyError):
            return None

    def get_club_details(self, obj):
        return ClubDetailsSerializer(instance=obj.club).data

class ParticipantSerializer(serializers.ModelSerializer):
    archer = ParticipantArcherSerializer(read_only=True)
    scorecards = ScoreCardSerializer(many=True, read_only=True)
    class Meta:
        model = Participant
        fields = '__all__'

class StageParticipantSerializer(serializers.ModelSerializer):
    archer = ParticipantArcherSerializer(read_only=True)
    scorecards = ParticipantScoreCardSerializer(many=True, read_only=True)
    class Meta:
        model = Participant
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    archer = ArcherSerializer()
    csrftoken = serializers.SerializerMethodField()
    perms = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'email', 'archer', 'csrftoken', 'perms']

    def get_csrftoken(self, obj):
        if hasattr(obj, 'csrftoken'):
            return obj.csrftoken
        return None

    def get_perms(self, obj):
        if obj.id and obj.has_perm('api.add_record'):
            return ['record']
        return None

class ObjAdminSerializer(serializers.RelatedField):
    class Meta:
        model = User

    def to_representation(self, obj):
        return obj.email

    def to_internal_value(self, data):
        try:
            return User.objects.get(email=data)
        except User.DoesNotExist:
            return None
            # raise serializers.ValidationError('Invalid Email or no user with given Email.')

class ClubsSerializerList(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    association = AssociationSerializer(many=True, read_only=True)

    class Meta:
        model = Club
        fields = '__all__'

    def get_members(self, obj):
        return obj.members.all().count()

class ClubSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
    members = ArcherSerializer(many=True, read_only=True)
    admins = ObjAdminSerializer(many=True, read_only=True)

    class Meta:
        model = Club
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

class EventSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
    admins = ObjAdminSerializer(many=True, queryset=User.objects.all())
    series = serializers.SlugRelatedField(read_only=True, slug_field='name')
    participants = ParticipantSerializer(many=True, read_only=True)
    rounds = RoundSerializer(many=True, read_only=True)
    class Meta:
        model = Event
        fields = '__all__'

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

        return StageParticipantSerializer(instance=participants, many=True).data


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
