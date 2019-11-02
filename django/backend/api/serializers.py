from .models import User
from .models import Competition
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    competitions = serializers.HyperlinkedRelatedField(many=True, view_name='competition-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'email', 'first_name', 'last_name', 'competitions']

class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Competition
        fields = ['url', 'name', 'description', 'start_date', 'end_date', 'owner']
