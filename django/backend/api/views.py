from rest_framework import viewsets
from rest_framework import permissions
from .models import (Club, Course, Archer, Event, Round, Participant)
from .serializers import (ClubSerializer, CourseSerializer,
                          ArcherSerializer, EventSerializer,
                          RoundSerializer, ParticipantSerializer)

class ClubViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows clubs to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ClubSerializer
    queryset = Club.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Courses to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ArcherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows archer to be viewed or edited.
    """
    serializer_class = ArcherSerializer
    queryset = Archer.objects.all()

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    Edit / create is privileged to registered users only.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class RoundViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    Edit / create is privileged to registered users only.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = RoundSerializer
    queryset = Round.objects.all()

    # def perform_create(self, serializer):
    #     serializer.save(creator=self.request.user)

class ParticipantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    Edit / create is privileged to registered users only.
    """
    serializer_class = ParticipantSerializer
    queryset = Participant.objects.all()

# Create your views here.
