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
from datetime import datetime
from .utilities import get_archer_class
from .models import (User, Club, Course, Archer, Series, Event, Round, Participant, ScoreCard, Arrow, Record)
from .serializers import (ArcherSearchSerializer,
                          ArcherSerializer,
                          ArrowSerializer,
                          ArrowFilterSerializer,
                          ClubSerializer,
                          ClubsSerializerList,
                          CourseSerializer,
                          EventSerializer,
                          EventSerializerList,
                          LevelClassSerializer,
                          ParticipantSerializer,
                          RecordSerializer,
                          RoundSerializer,
                          ScoreCardSerializer,
                          SeriesSerializer,
                          SeriesSerializerList,
                          UserSerializer)

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
    queryset = Course.objects.all().prefetch_related('ends')

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class SeriesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    Edit / create is privileged to registered users only.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Series.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = Series.objects.all()
        if isinstance(user, AnonymousUser):
            # not logged in users can see only 'open' type of events
            queryset = queryset.filter(Q(type = 'open'))
        else:
            # to list events that are associated with the user / archer
            queryset = queryset.filter(Q(creator__pk = user.id) |
                                      (Q(creator__archer__club__pk = user.archer.club.id) & Q(type = 'club')) |
                                       Q(stages__participants__in = user.archer.events.all()) |
                                       Q(type = 'open')).distinct()
        if self.action == 'list':
            return queryset
        else:
            return queryset.prefetch_related('stages__participants',
                                             'stages__participants__scorecards')

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
        queryset = Event.objects.all()
        if self.action == 'list':
            if isinstance(user, AnonymousUser):
                # not logged in users can see only 'open' type of events
                return queryset.filter(Q(type = 'open'))
            else:
                # to list events that are associated with the user / archer
                return queryset.filter(Q(creator__pk = user.id) |
                                      (Q(creator__archer__club__pk = user.archer.club.id) & Q(type = 'club')) |
                                       Q(participants__in = user.archer.events.all()) |
                                       Q(admins__pk = user.id) |
                                       Q(type = 'open')).distinct().prefetch_related('rounds')
        else:
            if isinstance(user, AnonymousUser):
                # not logged in users can discover 'open' and open for registration type of events
                queryset = queryset.filter(Q(type = 'open') | Q(is_open = True)).distinct()
            else:
                # In addition to 'my' events allow to discover events that are open
                # for registration
                queryset = queryset.filter(Q(creator__pk = user.id) |
                                    (Q(creator__archer__club__pk = user.archer.club.id) & Q(type = 'club')) |
                                     Q(participants__in = user.archer.events.all()) |
                                     Q(type = 'open') |
                                     Q(admins__pk = user.id) |
                                     Q(is_open = True)).distinct()
            return queryset.prefetch_related('participants',
                                             'participants__scorecards',
                                             'participants__archer',
                                             'participants__archer__user',
                                             'rounds')

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
        return Response(ArcherSearchSerializer(archers, many=True).data)

    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny])
    def archer_classification(self, request):
        """
        Search archer profiles by name
        """
        archer = Archer.objects.get(pk=request.data['aId'])
        date = datetime.strptime(request.data['date'], '%Y-%m-%d').date()
        level_class = get_archer_class(archer, date)
        return Response(LevelClassSerializer(level_class, many=True).data)

class ParticipantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows participants to be added or viewed.
    """
    permission_classes = [permissions.IsAuthenticated&ActiveEvent]
    serializer_class = ParticipantSerializer
    queryset = Participant.objects.all()

    @action(detail=False, methods=['POST'])
    def filter(self, request):
        """
        Filter participants by event and / or archer
        """
        queryset = Participant.objects.none()
        if 'eId' in request.data:
            queryset = Participant.objects.filter(event__pk=request.data['eId'])
        if 'aId' in request.data:
            queryset = Participant.objects.filter(archer__pk=request.data['aId'])
        return Response(ParticipantSerializer(queryset, many=True).data)

    @action(detail=False, methods=['POST'])
    def scorecard_check(self, request):
        """
        Event owner and admins can mark scorecards as checked after shooting
        """
        event = Event.objects.get(pk=request.data['eId'])

        if (request.user in [event.creator, *event.admins.all()] and
            'scId' in request.data):
            scorecard = ScoreCard.objects.get(pk=request.data['scId'])
            scorecard.checked = True
            scorecard.save()
            return Response([{ 'header': 'scorecard with pk:' + str(scorecard.id) + ' marked as checked!'}],
                            status=status.HTTP_200_OK)
        return Response({'details': 'You probably don\'t have the permission to do this'},
                        status=status.HTTP_403_FORBIDDEN)


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
            'target' in request.data):
            session = request.data['session']
            target = request.data['target']
        else:
            user_participant = event.participants.filter(
               archer__id=request.user.archer.id).get(
               pk=request.data['pId'])
            session = user_participant.session
            target = user_participant.target

        # get or create scorecards for given round in start session
        for participant in event.participants.order_by():
            if (participant.session == session and
                participant.target == target):
                sc, created = ScoreCard.objects.get_or_create(participant=participant, round=round)
                if created:
                    # fill in arrows, so we would have valid model always
                    for e in round.course.ends.all():
                        for a in range(e.nr_of_arrows):
                            Arrow.objects.create(scorecard=sc, end=e, ord=a)

        scorecards = ScoreCard.objects.filter(
                                            participant__event__pk=event.id).filter(
                                            participant__session=session).filter(
                                            participant__target=target).filter(
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

    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny])
    def filter(self, request):
        arrows = Arrow.objects.none()
        if 'pId' in request.data:
            arrows = Arrow.objects.filter(scorecard__participant__id=request.data['pId']).order_by('scorecard', 'end', 'ord')
        if 'rId' in request.data:
            if isinstance(request.data['rId'],list):
                arrows = Arrow.objects.filter(scorecard__round__id__in=request.data['rId']).order_by('scorecard', 'end', 'ord')
            else:
                arrows = Arrow.objects.filter(scorecard__round__id=request.data['rId']).order_by('scorecard', 'end', 'ord')
        return Response(ArrowFilterSerializer(arrows, many=True).data)


    def perform_update(self, serializer):
        sc = self.get_object().scorecard
        if (not sc.participant.event.archive and
            (self.request.user in [sc.participant.event.creator, *sc.participant.event.admins.all()] or
            sc.round.is_open)):
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
            arrows = sc.arrows.order_by()
            args = {
                'score': sum(a['score'] for a in arrows.values('score') if a['score']),
                'pr': round(sum(1 for a in arrows.values('score') if a['score'] != None) / arrows.count(), 2)
            }
            spots = sum(1 for a in arrows.values('x') if a['x'])
            if spots:
                args['spots'] = spots
            ScoreCard.objects.filter(pk = sc.id).update(**args)

class RecordViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """
    List all records. Users with model permissions can also create and update
    """
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = RecordSerializer
    queryset = Record.objects.all()

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
