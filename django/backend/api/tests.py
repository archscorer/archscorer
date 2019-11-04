from django.test import TestCase

# Create your tests here.

# I use it maybe a bit in adverse way, but place I can put code to autogenerate some test data

from .models import (User,
                     Club,
                     Archer,
                     Course,
                     End,
                     Competition,
                     Participant,
                     Round,
                     ScoreCard,
                     Arrow)

def build_base_data():
    users = [User.objects.create_superuser('adler@ut.ee', 'testuser', first_name='Priit', last_name='Adler'),
             User.objects.create_user('ex@ample.com', 'testuser', first_name='Ex', last_name='Ample'),
             User.objects.create_user('ann@mail.ee', 'testuser', first_name='Ann', last_name='Mets')]

    clubs = [Club.objects.create(creator=users[0], name='Not assigned to any club'),
             Club.objects.create(creator=users[0], name='Tartu vibuklubi'),
             Club.objects.create(creator=users[2], name='Local mad archers')]

    archers = [Archer.objects.create(full_name='Priit Adler', gender='M', club=clubs[1]),
               Archer.objects.create(full_name='Ann Mets', gender='F', club=clubs[2]),
               Archer.objects.create(full_name='Volli Mets', gender='M', club=clubs[2])]

    course_1 = Course.objects.create(creator=users[0], name='Generic: 28 ends / animal')
    for i in range(28):
        End.objects.create(course=course_1, order=i+1, nr_of_arrows=1, scoring=[20,18,16,14,12,10])

    course_4 = Course.objects.create(creator=users[0], name='Generic: 28 ends / 4 arrows')
    for i in range(28):
        End.objects.create(course=course_4, order=i+1, nr_of_arrows=4, scoring=[5,4,3])

    course_5 = Course.objects.create(creator=users[2], name='Generic: 6 ends / 5 arrows')
    for i in range(6):
        End.objects.create(course=course_5, order=i+1, nr_of_arrows=5, scoring=[5,4,3,2,1])

    indoor_training = Competition.objects.create(creator=users[2], name='Indoor training')
    for r in range(2):
        Round.objects.create(order=r+1, course=course_5, competition=indoor_training, label='20y ' + str(r+1) + '. round')

    big_competition = Competition.objects.create(creator=users[0], name='Open type of comp')
    Round.objects.create(order=1, course=course_1, competition=big_competition, label='Animal round')
    Round.objects.create(order=2, course=course_4, competition=big_competition, label='Field round')
    Round.objects.create(order=3, course=course_4, competition=big_competition, label='Hunter round')


def test_registration():
    # register all archers
    # to the first competition in the database
    comp = Competition.objects.get(pk=1)

    Participant.objects.create(archer=Archer.objects.get(pk=1), competition=comp, age_group='A', style='LB')

    comp = Competition.objects.get(pk=2)

    for a in Archer.objects.all():
        Participant.objects.create(archer=a, competition=comp, age_group='A', style='LB')
        if a.full_name == 'Ann Mets':
            # test if archer can participate in multiple styles
            Participant.objects.create(archer=a, competition=comp, age_group='A', style='BU')


def test_scoring():
    from random import choice
    for comp in Competition.objects.all():

        for a in comp.participants.all():
            for r in comp.rounds.all():
                ScoreCard.objects.get_or_create(participant=a, round=r)

        cards = ScoreCard.objects.filter(participant__competition__pk=comp.pk)

        for c in cards:
            for e in c.round.course.ends.all():
                for a in range(e.nr_of_arrows):
                    scoring = eval(e.scoring) + [0]
                    score = choice(scoring)
                    arrow, created = Arrow.objects.get_or_create(scorecard=c, end=e, nr=a)
                    arrow.score=score
                    arrow.save()

        for c in cards:
            style = c.participant.age_group + c.participant.archer.gender + c.participant.style
            a_name = c.participant.archer.full_name
            r_name = c.round.label
            cum_score = sum([a.score for a in c.arrows.all()])
            print(style, a_name, r_name, cum_score)

# build_base_data()
# test_registration()
test_scoring()
