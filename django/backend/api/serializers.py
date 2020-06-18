from .models import (User,
                     Club,
                     Archer,
                     Course,
                     End,
                     Series,
                     Event,
                     Round,
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
        fields = ['id', 'creator', 'name', 'description', 'location', 'ends', 'halves']

class RoundSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()
    scorecards = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Round
        fields = '__all__'

    def get_course_name(self, obj):
        return obj.course.name

class ArrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arrow
        fields = ['id', 'end', 'ord', 'score', 'x']

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
        return len(obj.events.all())

class ParticipantSerializer(serializers.ModelSerializer):
    archer = ParticipantArcherSerializer(read_only=True)
    scorecards = ParticipantScoreCardSerializer(many=True, read_only=True)
    class Meta:
        model = Participant
        fields = '__all__'

class ArcherSerializer(serializers.ModelSerializer):
    events = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.is_active')
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
        return len(obj.members.all())

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
        return len(obj.participants.all())

class StageSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
    rounds = RoundSerializer(many=True, read_only=True)
    participants = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = '__all__'

    def get_participants(self, obj):
        participants = obj.participants.all()
        # root.instance contains series object
        if self.root.instance.participant_restriction:
            try:
                p, v = self.root.instance.participant_restriction.split(':')
                kwargs = {p: v}
                participants = obj.participants.filter(**kwargs)
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
