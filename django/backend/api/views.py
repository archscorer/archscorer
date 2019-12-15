from rest_framework import (status, viewsets, mixins, permissions)
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import AnonymousUser
from django.middleware.csrf import get_token
from django.db.models import Q
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from .models import (User, Club, Course, Archer, Event, Round, Participant, ScoreCard, Arrow)
from .serializers import (UserSerializer, ClubSerializer, CourseSerializer,
                          ArcherSerializer, EventSerializer, EventSerializerList,
                          RoundSerializer, ParticipantArcherSerializer,ParticipantSerializer,
                          ParticipantScoreCardSerializer, ArrowSerializer)

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows user information to be retrieved.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            # for AnonymousUser swap to User model and add archer
            user = User()
            _ = Archer(user=user)
            return [user]

        if not hasattr(user, 'archer'):
            # in case logged in user does not yet have archer model or it has
            # been deleted ?
            archer = Archer.objects.create(full_name=user.get_full_name(),
                                           email=user.email,
                                           user=user,
                                           club=Club.objects.get(pk=1))
        setattr(user, 'csrftoken', get_token(self.request))
        return [user]


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

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            # not logged in users can see and discover only 'open' type of events
            return Event.objects.filter(Q(type = 'open'))
        if self.action == 'list':
            # to list events show only those that should be listed
            return Event.objects.filter(Q(creator__pk = user.id) |
                                       (Q(creator__archer__club__pk = user.archer.club.id) & Q(type = 'club')) |
                                        Q(participants__in = user.archer.events.all()) |
                                        Q(type = 'open')).distinct()
        else:
            # In addition to 'my' events allow to discover events that are open
            # for registration
            return Event.objects.filter(Q(creator__pk = user.id) |
                                       (Q(creator__archer__club__pk = user.archer.club.id) & Q(type = 'club')) |
                                        Q(participants__in = user.archer.events.all()) |
                                        Q(type = 'open') |
                                        Q(is_open = True)).distinct()

    def get_serializer_class(self):
        if self.action == 'list':
            return EventSerializerList
        return EventSerializer

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

    @action(detail=False, methods=['POST'])
    def add(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ArcherViewSet(mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """
    API endpoint that allows archer to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ArcherSerializer
    queryset = Archer.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny])
    def search(self, request):
        """
        Search archer profiles by name
        """
        archers = Archer.objects.filter(full_name__contains=request.data['query'])
        if len(archers) == 0:
            return Response([{ 'header': 'no matching archer profiles' }],
                            status=status.HTTP_200_OK)
        return Response(ParticipantArcherSerializer(archers, many=True).data)

class ParticipantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows participants to be added or viewed.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ParticipantSerializer
    queryset = Participant.objects.all()

    @action(detail=False, methods=['POST'])
    def scorecards(self, request):
        """
        Retrieve user group scorecards for specified round
        """
        # get user start_group first
        event = Event.objects.get(pk=request.data['eId'])
        round = Round.objects.get(pk=request.data['rId'])

        user_participant = event.participants.get(archer__id=request.user.archer.id)

        # get or create scorecards for given round in start group
        for participant in event.participants.all():
            if participant.start_group == user_participant.start_group:
                sc, created = ScoreCard.objects.get_or_create(participant=participant, round=round)
                if created:
                    # fill in arrows, so we would have valid model always
                    for e in round.course.ends.all():
                        for a in range(e.nr_of_arrows):
                            Arrow.objects.create(scorecard=sc, end=e, ord=a)

        scorecards = ScoreCard.objects.filter(
                                            participant__event__pk=event.id).filter(
                                            participant__start_group=user_participant.start_group).filter(
                                            round=round)

        # return scorecards
        return Response(ParticipantScoreCardSerializer(scorecards, many=True).data)

    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """
        API endpoint that allows participants to be registered to an event. Does not need to be
        logged in to the API to do that. If archer object contains ID, tries to use existing object.
        Otherwise creates new Archer instance.
        """
        if 'archer' not in request.data:
            return Response({'details': 'invalid request'},
                            status=status.HTTP_400_BAD_REQUEST)

        req_archer = request.data['archer']
        if 'id' in req_archer:
            archer_serialized = ParticipantArcherSerializer(data=req_archer)
            if archer_serialized.is_valid():
                try:
                    archer = Archer.objects.get(pk=req_archer['id'])
                except ObjectDoesNotExist:
                    return Response({'details': 'Referenced archer does not exist.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(archer_serialized.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            archer_serialized = ArcherSerializer(data=req_archer)
            if ArcherSerializer(data=req_archer).is_valid():
                if 'club' in req_archer:
                    try:
                        req_archer['club'] = Club.objects.get(pk=req_archer['club'])
                    except ObjectDoesNotExist:
                        # if club does not exist just remove it silently
                        del req_archer['club']
                archer = Archer.objects.create(**req_archer)
            else:
                return Response(archer_serialized.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        req_participant = request.data
        req_participant['archer'] = archer
        participant_serialized = ParticipantSerializer(data=req_participant)
        if participant_serialized.is_valid():
            try:
                req_participant['event'] = Event.objects.get(pk=req_participant['event'])
            except ObjectDoesNotExist:
                return Response({'details': 'Referenced event does not exist.'},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                participant = Participant.objects.create(**req_participant)
            except IntegrityError:
                return Response({'details': 'Archer has already been registered to the event in given style.'},
                                status=status.HTTP_409_CONFLICT)
            return Response(ParticipantSerializer(participant).data)
        else:
            return Response(participant_serialized.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class ArrowViewSet(mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """
    Update arrow score
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ArrowSerializer
    queryset = Arrow.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.email)
