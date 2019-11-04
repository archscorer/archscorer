from rest_framework import viewsets
from rest_framework import permissions
from .models import (Club, Course, Archer, Competition)
from .serializers import (ClubSerializer, CourseSerializer,
                          ArcherSerializer, CompetitionSerializer)

class ClubViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows archer to be viewed or edited.
    """
    serializer_class = ClubSerializer
    queryset = Club.objects.all()

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows archer to be viewed or edited.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

class ArcherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows archer to be viewed or edited.
    """
    serializer_class = ArcherSerializer
    queryset = Archer.objects.all()

class CompetitionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows competitions to be viewed or edited.
    Edit / create is privileged to registered users only.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CompetitionSerializer
    queryset = Competition.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Create your views here.
