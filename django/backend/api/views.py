from rest_framework import viewsets
from .models import (User, Competition)
from .serializers import (UserSerializer, CompetitionSerializer)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

class CompetitionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows competitions to be viewed or edited.
    Edit / create is privileged to registered users only.
    """
    serializer_class = CompetitionSerializer
    queryset = Competition.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Create your views here.
