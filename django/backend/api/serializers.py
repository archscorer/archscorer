from .models import (Club,
                     Archer,
                     Course,
                     End,
                     Competition,
                     Round,
                     Participant)
from rest_framework import serializers

class EndSerializer(serializers.HyperlinkedModelSerializer):
    round = serializers.HyperlinkedRelatedField(view_name='round-detail', read_only=True)
    class Meta:
        model = End
        fields = ['id', 'round', 'order', 'label', 'nr_of_arrows', 'scoring']

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
    ends = EndSerializer(many=True)
    class Meta:
        model = Course
        fields = ['id', 'creator', 'name', 'description', 'location', 'ends']

class RoundSerializer(serializers.ModelSerializer):
    competition = serializers.HyperlinkedRelatedField(view_name='competition-detail', read_only=True)
    course = serializers.HyperlinkedRelatedField(view_name='course-detail', read_only=True)
    class Meta:
        model = Round
        fields = ['id', 'competition', 'order', 'course', 'label', 'is_open']

class ParticipantSerializer(serializers.ModelSerializer):
    archer = serializers.HyperlinkedRelatedField(view_name='archer-detail', read_only=True)
    competition = serializers.HyperlinkedRelatedField(view_name='competition-detail', read_only=True)
    class Meta:
        model = Participant
        fields = ['id', 'archer', 'competition', 'age_group', 'style']

class ArcherSerializer(serializers.HyperlinkedModelSerializer):
    competitions = ParticipantSerializer(many=True)
    club = serializers.HyperlinkedRelatedField(view_name='club-detail', read_only=True)
    class Meta:
        model = Archer
        fields = ['url', 'full_name', 'gender', 'club', 'email', 'phone', 'efaa_id', 'competitions']

class ClubSerializer(serializers.HyperlinkedModelSerializer):
    members = ArcherSerializer(many=True)
    class Meta:
        model = Club
        fields = ['url', 'name', 'contact', 'members']

class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    participants = ParticipantSerializer(many=True)
    rounds = RoundSerializer(many=True)
    class Meta:
        model = Competition
        fields = ['url', 'owner', 'name', 'description', 'start_date', 'end_date', 'rounds', 'participants']
