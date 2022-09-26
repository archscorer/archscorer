from backend.api import models
from collections import namedtuple

def import_archers(club=None, file=None):

    club, created = models.Club.objects.get_or_create(name = club)

    with open(file) as fh:
        header = fh.readline().rstrip().split('\t')
        A = namedtuple('Archer', header, defaults=[None, None])
        for line in fh.readlines():
            a = A(*line.rstrip().split('\t'))
            gender = 'M' if str(a.nat_id[0]) in ['3', '5'] else 'F'
            models.Archer.objects.get_or_create(full_name=a.full_name,
                                                club=club,
                                                nat_id=a.nat_id,
                                                gender=gender,
                                                email=a.email if a.email else '',
                                                phone=a.phone if a.phone else '')


def import_and_register(file=None, event_pk=None):
    event = models.Event.objects.get(pk = event_pk)
    with open(file) as fh:
        header = fh.readline().rstrip().split(',')
        A = namedtuple('Archer', header)
        for line in fh.readlines():
            a = A(*line.rstrip().split(','))
            archer, created = models.Archer.objects.get_or_create(full_name=a.full_name)
            if created:
                club, created = models.Club.objects.get_or_create(name = a.club)
                models.Archer.objects.filter(pk = archer.id).update(club=club,
                                                                    nat_id=a.nat_id,
                                                                    gender=a.gender,
                                                                    email=a.email,
                                                                    phone=a.phone)
            models.Participant.objects.get_or_create(archer=archer,
                                                     event=event,
                                                     style=a.style,
                                                     age_group=a.age_group)


def generate_participants(event_pk=None, n=10):
    import random
    # we have more than thousand archers in database just use some random subset of those
    event = models.Event.objects.get(pk = event_pk)
    archers = random.sample(list(models.Archer.objects.all()), n)
    for a in archers:
        try:
            archer_rep=a.club.name_short + '|' + a.club.association.first().name_short
        except:
            archer_rep=a.club.name_short + '|'
        models.Participant.objects.get_or_create(archer=a,
                                                 event=event,
                                                 style=random.choice(models.STYLE_CHOICES[:11])[0],
                                                 age_group=random.choice(models.AGEGROUP_CHOICES[:5])[0],
                                                 gender=a.gender,
                                                 full_name=a.full_name,
                                                 archer_rep=archer_rep)
        print(a.full_name)


def register(file=None, event_pk=None):
    # participant fields
    # archer, event, age_group, style, food, comments, group, group_target, group_pos
    event = models.Event.objects.get(pk = event_pk)
    with open(file) as fh:
        header = fh.readline().rstrip().split('\t')
        A = namedtuple('Archer', header)
        for line in fh.readlines():
            a = A(*line.rstrip().split('\t'))
            try:
                archer = models.Archer.objects.get(full_name=a.full_name)
                models.Participant.objects.get_or_create(archer=archer,
                                                         event=event,
                                                         style=a.style,
                                                         age_group=a.age_group,
                                                         food=True if a.food == 'TRUE' else False)
            except:
                print(a)


def read_clubs():
    # import_archers(club='Kagu Vibuklubi', file='kagu_vibuklubi.tsv')
    # import_archers(club='Tartu Vibuklubi', file='tartu_vibuklubi.tsv')
    pass


# from backend.api import models, serializers
# event = models.Event.objects.get(pk = 274)
# cProfile.runctx('serializers.EventSerializer(event).data', None, locals(), sort='cumtime')

# update all latvian archers to have correct club and association
from backend.api import models
for a in models.Archer.objects.all():
    ass = a.club.association.all()
    if len(ass) == 1 and ass[0].id == 2:
        for p in a.events.all():
            archer_rep = a.club.name_short + '|' + ass[0].name_short
            if archer_rep != p.archer_rep:
                p.archer_rep = archer_rep
                p.save()
                print(p.full_name, p.archer_rep)


# create new course
c = models.Course.objects.create(name='IFAA Expert Field Round (4 Arrows, 28 Ends)',
                                 description='28 ends / 4 arrows / 5,4,3,2,1', type='r', halves=True)
for i in range(28):
    models.End.objects.create(course=c, ord=i+1, nr_of_arrows=4, scoring='[5,4,3,2,1]', x=True)
