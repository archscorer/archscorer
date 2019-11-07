from .models import (Club,
                     Archer,
                     Course,
                     End,
                     Competition,
                     Round,
                     Participant)
from rest_framework import serializers

class EndSerializer(serializers.ModelSerializer):
    # round = serializers.HyperlinkedRelatedField(view_name='round-detail', read_only=True)
    class Meta:
        model = End
        fields = ['id', 'course', 'ord', 'label', 'nr_of_arrows', 'scoring']

class CourseSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
    ends = EndSerializer(many=True)
    class Meta:
        model = Course
        fields = ['id', 'creator', 'name', 'description', 'location', 'ends']

class RoundSerializer(serializers.ModelSerializer):
    # competition = serializers.HyperlinkedRelatedField(view_name='competition-detail', read_only=True)
    # course = serializers.HyperlinkedRelatedField(view_name='course-detail', read_only=True)
    class Meta:
        model = Round
        fields = ['id', 'ord', 'course', 'label', 'is_open', 'competition']

class ParticipantSerializer(serializers.ModelSerializer):
    # archer = serializers.HyperlinkedRelatedField(view_name='archer-detail', read_only=True)
    # competition = serializers.HyperlinkedRelatedField(view_name='competition-detail', read_only=True)
    class Meta:
        model = Participant
        fields = ['id', 'archer', 'age_group', 'style', 'competition']

class ArcherSerializer(serializers.ModelSerializer):
    competitions = ParticipantSerializer(many=True, read_only=True)
    # club = serializers.HyperlinkedRelatedField(view_name='club-detail', read_only=True)
    user = serializers.ReadOnlyField(source='user.is_active')
    class Meta:
        model = Archer
        fields = ['id', 'full_name', 'gender', 'club', 'email', 'phone', 'efaa_id', 'competitions', 'user']

class ClubSerializer(serializers.ModelSerializer):
    members = ArcherSerializer(many=True, read_only=True)
    class Meta:
        model = Club
        fields = ['id', 'name', 'contact', 'members']

class CompetitionSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
    participants = ParticipantSerializer(many=True, read_only=True)
    rounds = RoundSerializer(many=True, read_only=True)
    class Meta:
        model = Competition
        fields = ['id', 'creator', 'name', 'description', 'date_start', 'date_end', 'rounds', 'participants']
