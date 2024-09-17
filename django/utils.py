from collections import namedtuple
from backend.api import models

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
c = models.Course.objects.create(name='GSL 3D Hunting Unit (3 arrows, 14 Ends)',
                                 description='28 ends / 3 arrows / 10,8,5', type='u', halves=False)
for i in range(14):
    models.End.objects.create(course=c, ord=i+1, nr_of_arrows=3, scoring='[10,8,5]', x=False)


# handled lithuanian archers club assignments (also cleared some duplicate profiles)
from backend.api import models
from collections import namedtuple
from django.db.models import Q
notHandled = []
with open('lit_archers.tsv') as fh:
    header = fh.readline().rstrip().split('\t')
    A = namedtuple('Archer', header, defaults=[None, None])
    for line in fh.readlines():
        a = A(*line.rstrip().split('\t'))
        try:
            archer = models.Archer.objects.get(full_name=a.full_name, email=a.email)
            club = models.Club.objects.get(name_short=a.club_short)
            archer.club = club
            for p in archer.events.all():
                if p.archer_rep == '|':
                    p.archer_rep = club.name_short + '|' + club.association.first().name_short
                p.save()
                print(a.full_name, p.full_name, p.archer_rep)
            archer.save()
        except:
            notHandled.append(a)

stillNotHandled = []
notDeleted = []
for a in notHandled:
    archers = models.Archer.objects.filter(Q(full_name=a.full_name))
    if not archers:
        stillNotHandled.append(a)
        continue
    user = []
    events = []
    for archer in archers.order_by('-id'):
        if archer.user:
            user.append(archer.user)
        events.extend(archer.events.all())
    if len(user) > 1:
        stillNotHandled.append(a)
        continue
    archer = archers.last()
    club = models.Club.objects.get(name_short=a.club_short)
    archer.club = club
    archer.full_name = a.full_name
    archer.email = a.email
    archer.phone = a.phone
    for p in events:
        p.archer = archer
        if p.archer_rep == '|':
            p.archer_rep = club.name_short + '|' + club.association.first().name_short
        p.save()
        print(archer.full_name, p.full_name, p.archer_rep)
    for obj in archers.exclude(pk=archer.id):
        obj.delete()
    if user:
        archer.user = user[0]
    archer.save()

for a in stillNotHandled:
    print(a)

# removes duplicate archer profiles (same name, email and club)
# this should be safe to run also on live database (backup first, for sure!)
from backend.api import models
from django.db.models import Count
duplicates = models.Archer.objects.values('full_name', 'email', 'club').annotate(dup_count=Count('id')).filter(dup_count__gt=1)

for d in duplicates.order_by('-dup_count'):
    print(d)

for d in duplicates:
    archers = models.Archer.objects.filter(full_name=d['full_name'], email=d['email'], club=d['club'])
    user = []
    events = []
    for archer in archers.order_by('-id'):
        if archer.user:
            user.append(archer.user)
        events.extend(archer.events.all())
    if len(user) > 1:
        print(d)
        continue
    archer = archers.last()
    for p in events:
        try:
            if p.archer != archer:
                p.archer = archer
                p.save()
                print(archer.full_name, p.full_name)
        except:
            print(archer.full_name, p.full_name, 'reassign failed', [p.id, p.archer.id, archer.id])
    for obj in archers.exclude(pk=archer.id):
        try:
            obj.delete()
        except:
            print('delete failed:', obj.id, obj.full_name)
    if user:
        archer.user = user[0]
        archer.save()


# here for future reference, chatGPT suggestion how to find duplicate archers with fuzzy matching.
# pip install fuzzywuzzy python-Levenshtein
from backend.api import models
from fuzzywuzzy import fuzz

def find_duplicates(model, field_name, threshold=85):
    records = model.objects.all()
    duplicates = []

    for i in range(len(records)):
        for j in range(i+1, len(records)):
            # Use fuzz.ratio() to get a similarity score
            if fuzz.ratio(getattr(records[i], field_name), getattr(records[j], field_name)) > threshold:
                duplicates.append((records[i], records[j]))

    return duplicates

duplicates = find_duplicates(models.Archer, 'name')
