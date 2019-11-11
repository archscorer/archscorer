from rest_framework import (status, viewsets, permissions)
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import AnonymousUser
from django.db.utils import IntegrityError
from .models import (User, Club, Course, Archer, Event, Round, Participant)
from .serializers import (UserSerializer, ClubSerializer, CourseSerializer,
                          ArcherSerializer, EventSerializer, RoundSerializer,
                          ParticipantSerializer)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows user information to be retrieved.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserSerializer

    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return [User()]
        else:
            return [self.request.user]

class ClubViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows clubs to be viewed or edited.
    Edit / create is privileged to registered users only.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ClubSerializer
    queryset = Club.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    Edit / create is privileged to registered users only.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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
    API endpoint that allows rounds to be viewed or edited.
    Edit / create is privileged to registered users only.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = RoundSerializer
    queryset = Round.objects.all()

class ArcherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows archer to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ArcherSerializer
    queryset = Archer.objects.all()

class ParticipantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows participants to be added or viewed.
    """
    serializer_class = ParticipantSerializer
    queryset = Participant.objects.all()

    @action(detail=False, methods=['POST'])
    def register(self, request):
        """
        API endpoint that allows participants to be registered to an event. Does not need to be
        logged in to the API to do that. Will automatically create new archer if by 'full_name'
        and 'email' it does not exist. If it exists, existing one will be used (note: existing
        archer additional details will not be updated).
        """
        if 'archer' not in request.data:
            return Response({'details': 'invalid request'},
                            status=status.HTTP_400_BAD_REQUEST)

        req_archer = request.data['archer']
        archer_serialized = ArcherSerializer(data=req_archer)
        if archer_serialized.is_valid():
            archer, created = Archer.objects.get_or_create(full_name=req_archer['full_name'],
                                                           email=req_archer['email'])
            if created:
                # if new archer is created fill in additional submitted information
                for key in req_archer:
                    if req_archer[key]:
                        if key == 'club':
                            # expects to be club instance not its primary key
                            req_archer[key] = Club.objects.get(pk=req_archer[key])
                        setattr(archer, key, req_archer[key])
                archer.save()
        else:
            return Response(archer_serialized.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        req_participant = request.data
        req_participant['archer'] = archer
        # TODO like for archer we use arcer base serializer here we could have same for
        # participant.
        participant_serialized = ParticipantSerializer(data=req_participant)
        if participant_serialized.is_valid():
            req_participant['event'] = Event.objects.get(pk=req_participant['event'])
            try:
                participant = Participant.objects.create(**req_participant)
            except IntegrityError:
                return Response({'details': 'Archer has already been registered to the event in given style.'},
                                status=status.HTTP_409_CONFLICT)
            return Response(ParticipantSerializer(participant).data)
        else:
            return Response(participant_serialized.errors,
                            status=status.HTTP_400_BAD_REQUEST)
