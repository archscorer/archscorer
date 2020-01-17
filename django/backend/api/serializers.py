from .models import (User,
                     Club,
                     Archer,
                     Course,
                     End,
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
        fields = '__all__'

class ParticipantScoreCardSerializer(serializers.ModelSerializer):
    arrows = ArrowSerializer(many=True, read_only=True)
    class Meta:
        model = ScoreCard
        fields = ['id', 'participant', 'round', 'arrows']

class ParticipantArcherSerializer(serializers.ModelSerializer):
    club = serializers.ReadOnlyField(source='club.name')
    user = serializers.ReadOnlyField(source='user.is_active')
    class Meta:
        model = Archer
        fields = ['id', 'full_name', 'gender', 'club', 'user']

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

class ClubSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Club
        fields = ['id', 'name', 'contact', 'members']
        depth = 1

class EventSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
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
