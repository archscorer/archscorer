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
from .models import (User, Club, Course, Archer, Series, Event, Round, Participant, ScoreCard, Arrow, Record)
from .serializers import (UserSerializer, ClubSerializer, ClubsSerializerList, CourseSerializer,
                          ArcherSerializer, SeriesSerializer, EventSerializer, EventSerializerList,
                          RoundSerializer, ParticipantSerializer,
                          ScoreCardSerializer, ArrowSerializer, SeriesSerializerList,
                          RecordSerializer)

class ActiveEvent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.event.archive:
            return request.method in permissions.SAFE_METHODS
        return True

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
            _ = Archer(user = user)
            return [user]

        if not hasattr(user, 'archer'):
            # in case logged in user does not yet have archer model or it has
            # been deleted ?

            # this if there should return at least one response, here user.email
            # can not be empty
            archer = Archer.objects.filter(email = user.email, user = None).first()
            if archer:
                Archer.objects.filter(pk = archer.id).update(user = user)
                user.refresh_from_db()
            else:
                Archer.objects.create(full_name = user.get_full_name(),
                                      email = user.email,
                                      user = user,
                                      club = Club.objects.get(pk=1))
        setattr(user, 'csrftoken', get_token(self.request))
        return [user]

class ClubViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows clubs to be viewed or edited.
    Edit / create is privileged to registered users only.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Club.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or isinstance(self.request.user, AnonymousUser):
            return ClubsSerializerList
        return ClubSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    Edit / create is privileged to registered users only.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class SeriesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    Edit / create is privileged to registered users only.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = SeriesSerializer
    queryset = Series.objects.all()

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            # not logged in users can see only 'open' type of events
            return Series.objects.filter(Q(type = 'open'))
        else:
            # to list events that are associated with the user / archer
            return Series.objects.filter(Q(creator__pk = user.id) |
                                       (Q(creator__archer__club__pk = user.archer.club.id) & Q(type = 'club')) |
                                        Q(stages__participants__in = user.archer.events.all()) |
                                        Q(type = 'open')).distinct()

    def get_serializer_class(self):
        if self.action == 'list':
            return SeriesSerializerList
        return SeriesSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    Edit / create is privileged to registered users only.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if self.action == 'list':
            if isinstance(user, AnonymousUser):
                # not logged in users can see only 'open' type of events
                return Event.objects.filter(Q(type = 'open'))
            else:
                # to list events that are associated with the user / archer
                return Event.objects.filter(Q(creator__pk = user.id) |
                                           (Q(creator__archer__club__pk = user.archer.club.id) & Q(type = 'club')) |
                                            Q(participants__in = user.archer.events.all()) |
                                            Q(admins__pk = user.id) |
                                            Q(type = 'open')).distinct()
        else:
            if isinstance(user, AnonymousUser):
                # not logged in users can discover 'open' and open for registration type of events
                return Event.objects.filter(Q(type = 'open') | Q(is_open = True)).distinct()
            else:
                # In addition to 'my' events allow to discover events that are open
                # for registration
                return Event.objects.filter(Q(creator__pk = user.id) |
                                           (Q(creator__archer__club__pk = user.archer.club.id) & Q(type = 'club')) |
                                            Q(participants__in = user.archer.events.all()) |
                                            Q(type = 'open') |
                                            Q(admins__pk = user.id) |
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
    permission_classes = [permissions.IsAuthenticated&ActiveEvent]
    serializer_class = RoundSerializer
    queryset = Round.objects.all()

    @action(detail=False, methods=['POST'])
    def add(self, request, *args, **kwargs):
        if Event.objects.get(pk=request.data.get('event')).archive:
            return Response({'details': 'No new rounds on archived event.'},
                            status=status.HTTP_403_FORBIDDEN)
        return self.create(request, *args, **kwargs)


class ArcherViewSet(mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """
    API endpoint that allows archer to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ArcherSerializer
    queryset = Archer.objects.all()

    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny])
    def search(self, request):
        """
        Search archer profiles by name
        """
        archers = Archer.objects.filter(full_name__icontains=request.data['query'])
        if len(archers) == 0:
            return Response([{ 'header': 'no matching archer profiles' }],
                            status=status.HTTP_200_OK)
        return Response(ArcherSerializer(archers, many=True).data)

class ParticipantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows participants to be added or viewed.
    """
    permission_classes = [permissions.IsAuthenticated&ActiveEvent]
    serializer_class = ParticipantSerializer
    queryset = Participant.objects.all()

    @action(detail=False, methods=['POST'])
    def scorecards(self, request):
        """
        Retrieve user group scorecards for specified round
        """
        # get user group first
        event = Event.objects.get(pk=request.data['eId'])
        round = Round.objects.get(pk=request.data['rId'])

        if (request.user in [event.creator, *event.admins.all()] and
            'session' in request.data and
            'group' in request.data):
            session = request.data['session']
            group = request.data['group']
        else:
            user_participant = event.participants.filter(
               archer__id=request.user.archer.id).get(
               pk=request.data['pId'])
            session = user_participant.session
            group = user_participant.group

        # get or create scorecards for given round in start session
        for participant in event.participants.order_by():
            if (participant.session == session and
                participant.group == group):
                sc, created = ScoreCard.objects.get_or_create(participant=participant, round=round)
                if created:
                    # fill in arrows, so we would have valid model always
                    for e in round.course.ends.all():
                        for a in range(e.nr_of_arrows):
                            Arrow.objects.create(scorecard=sc, end=e, ord=a)

        scorecards = ScoreCard.objects.filter(
                                            participant__event__pk=event.id).filter(
                                            participant__session=session).filter(
                                            participant__group=group).filter(
                                            round=round)

        # return scorecards
        return Response(ScoreCardSerializer(scorecards, many=True).data)

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
        archer_serialized = ArcherSerializer(data=req_archer)
        if archer_serialized.is_valid():
            if 'id' in req_archer:
                try:
                    archer = Archer.objects.get(pk=req_archer['id'])
                except ObjectDoesNotExist:
                    return Response({'details': 'Referenced archer does not exist.'},
                                    status=status.HTTP_404_NOT_FOUND)
            else:
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
        req_participant['gender'] = archer.gender
        req_participant['full_name'] = archer.full_name
        participant_serialized = ParticipantSerializer(data=req_participant)
        if participant_serialized.is_valid():
            try:
                event = Event.objects.get(pk=req_participant['event'])
                if event.archive:
                    return Response({'details': 'No new participants on archived event.'},
                                    status=status.HTTP_403_FORBIDDEN)
                req_participant['event'] = event
            except ObjectDoesNotExist:
                return Response({'details': 'Referenced event does not exist.'},
                                status=status.HTTP_404_NOT_FOUND)
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
        sc = self.get_object().scorecard
        if not sc.participant.event.archive:
            # import random
            # import time
            # time.sleep(1) # use if needed to simulate slow net or smth
            # if random.random() > 0.4:
            #     from rest_framework.exceptions import APIException
            #     raise APIException("too late")

            # arrow is saved only if event is active. otherwise returns silently
            # existing model from the database
            serializer.save(updated_by=self.request.user.email)
            # update scorecard on arrow update
            args = {'score': sum(a['score'] for a in sc.arrows.order_by().values('score') if a['score'])}
            spots = sum(1 for a in sc.arrows.order_by().values('x') if a['x'])
            if spots:
                args['spots'] = spots
            ScoreCard.objects.filter(pk = sc.id).update(**args)

class RecordViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List all records. Only list them, no update nor create currently implemented
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = RecordSerializer
    queryset = Record.objects.all()
