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


for p in models.Participant.objects.all():
    print(p.archer.club.association.get(id=1)

for p in models.Participant.objects.all():
    if p.archer_rep == '|':
        try:
            a = p.archer.club.association.get(id=1)
            p.archer_rep = p.archer.club.name_short + '|' + a.name_short
            print(p.archer.club.name_short + '|' + a.name_short)
            p.save()
        except:
            print(p.archer.club.name_short)
