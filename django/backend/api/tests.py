from django.test import TestCase

from random import choice

# Create your tests here.

# I use it maybe a bit in adverse way, but place I can put code to autogenerate some test data

from .models import (User,
                     Club,
                     Archer,
                     Course,
                     End,
                     Event,
                     Participant,
                     Round,
                     ScoreCard,
                     Arrow)

first_names = ['Liam', 'Noah', 'William', 'James', 'Oliver', 'Benjamin', 'Elijah', 'Lucas',
               'Mason', 'Logan', 'Alexander', 'Ethan', 'Jacob', 'Michael', 'Daniel', 'Henry',
               'Jackson', 'Sebastian', 'Aiden', 'Matthew', 'Samuel', 'David', 'Joseph', 'Carter',
               'Owen', 'Wyatt', 'John', 'Jack', 'Luke', 'Jayden', 'Dylan', 'Grayson', 'Levi', 'Isaac',
               'Gabriel', 'Julian', 'Mateo', 'Anthony', 'Jaxon', 'Lincoln', 'Joshua', 'Christopher',
               'Andrew', 'Theodore', 'Caleb', 'Ryan', 'Asher', 'Nathan', 'Thomas', 'Leo', 'Isaiah',
               'Charles', 'Josiah', 'Hudson', 'Christian', 'Hunter', 'Connor', 'Eli', 'Ezra', 'Aaron',
               'Landon', 'Adrian', 'Jonathan', 'Nolan', 'Jeremiah', 'Easton', 'Elias', 'Colton',
               'Cameron', 'Carson', 'Robert', 'Angel', 'Maverick', 'Nicholas', 'Dominic', 'Jaxson',
               'Greyson', 'Adam', 'Ian', 'Austin', 'Santiago', 'Jordan', 'Cooper', 'Brayden',
               'Roman', 'Evan', 'Ezekiel', 'Xavier', 'Jose', 'Jace', 'Jameson', 'Leonardo', 'Bryson',
               'Axel', 'Everett', 'Parker', 'Kayden', 'Miles', 'Sawyer', 'Jason']

last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia',
              'Rodriguez', 'Wilson', 'Martinez', 'Anderson', 'Taylor', 'Thomas', 'Hernandez',
              'Moore', 'Martin', 'Jackson', 'Thompson', 'White', 'Lopez', 'Lee', 'Gonzalez',
              'Harris', 'Clark', 'Lewi']


def build_base_data():

    clubs = [Club.objects.create(creator=None, name='..no club..')]

    course_1 = Course.objects.create(creator=None, halves=True, name='28 ends / 1 arrow / 20,18,16,14,12,10')
    for i in range(28):
        End.objects.create(course=course_1, ord=i+1, nr_of_arrows=1, x=False, scoring=[20,18,16,14,12,10])

    course_1 = Course.objects.create(creator=None, name='14 ends / 1 arrow / 20,18,16,14,12,10')
    for i in range(14):
        End.objects.create(course=course_1, ord=i+1, nr_of_arrows=1, x=False, scoring=[20,18,16,14,12,10])

    course_1 = Course.objects.create(creator=None, halves=True, name='28 ends / 1 arrow / 20,16,10')
    for i in range(28):
        End.objects.create(course=course_1, ord=i+1, nr_of_arrows=1, scoring=[20,16,10])

    course_1 = Course.objects.create(creator=None, name='14 ends / 1 arrow / 20,16,10')
    for i in range(14):
        End.objects.create(course=course_1, ord=i+1, nr_of_arrows=1, scoring=[20,16,10])

    course_2 = Course.objects.create(creator=None, halves=True, name='28 ends / 2 arrows / 10,8,5')
    for i in range(28):
        End.objects.create(course=course_2, ord=i+1, nr_of_arrows=2, scoring=[10,8,5])

    course_2 = Course.objects.create(creator=None, name='14 ends / 2 arrows / 10,8,5')
    for i in range(14):
        End.objects.create(course=course_2, ord=i+1, nr_of_arrows=2, scoring=[10,8,5])

    course_2 = Course.objects.create(creator=None, halves=True, name='24 ends / 2 arrows / 11,10,8,5')
    for i in range(24):
        End.objects.create(course=course_2, ord=i+1, nr_of_arrows=2, x=False, scoring=[11,10,8,5])

    course_2 = Course.objects.create(creator=None, name='12 ends / 2 arrows / 11,10,8,5')
    for i in range(12):
        End.objects.create(course=course_2, ord=i+1, nr_of_arrows=2, x=False, scoring=[11,10,8,5])

    course_3 = Course.objects.create(creator=None, name='10 ends / 3 arrows / 10,9,8,7,6,5,4,3,2,1')
    for i in range(10):
        End.objects.create(course=course_3, ord=i+1, nr_of_arrows=3, scoring=[10,9,8,7,6,5,4,3,2,1])

    course_4 = Course.objects.create(creator=None, halves=True, name='28 ends / 4 arrows / 5,4,3')
    for i in range(28):
        End.objects.create(course=course_4, ord=i+1, nr_of_arrows=4, scoring=[5,4,3])

    course_4 = Course.objects.create(creator=None, name='14 ends / 4 arrows / 5,4,3')
    for i in range(14):
        End.objects.create(course=course_4, ord=i+1, nr_of_arrows=4, scoring=[5,4,3])

    course_4 = Course.objects.create(creator=None, name='7 ends / 4 arrows / 5,4,3')
    for i in range(7):
        End.objects.create(course=course_4, ord=i+1, nr_of_arrows=4, scoring=[5,4,3])

    course_5 = Course.objects.create(creator=None, name='6 ends / 5 arrows / 5,4,3,2,1')
    for i in range(6):
        End.objects.create(course=course_5, ord=i+1, nr_of_arrows=5, scoring=[5,4,3,2,1])


def test_event_creation():
    users = [User.objects.create_superuser('adler@ut.ee', 'testuser', first_name='Priit', last_name='Adler'),
             User.objects.create_user('ex@ample.com', 'testuser', first_name='Ex', last_name='Ample'),
             User.objects.create_user('ann@mail.ee', 'testuser', first_name='Ann', last_name='Mets')]

    users = User.objects.all()
    courses = Course.objects.all()
    big_event = Event.objects.create(creator=users[0], name='Open type of comp')
    Round.objects.create(ord=1, course=courses[5], event=big_event, label='Animal round')
    Round.objects.create(ord=2, course=courses[1], event=big_event, label='Field round')
    Round.objects.create(ord=3, course=courses[1], event=big_event, label='Hunter round')

    indoor_training = Event.objects.create(creator=users[0], name='Indoor training')
    for r in range(2):
        Round.objects.create(ord=r+1, course=courses[0], event=indoor_training, label='20y ' + str(r+1) + '. round')


def test_registration():
    # register all archers
    # to the first event in the database
    comp = Event.objects.get(pk=2)
    archers = [Archer.objects.create(full_name='Priit Adler', user=users[0], gender='M', club=clubs[1]),
               Archer.objects.create(full_name='Ann Mets', user=users[2], gender='F', club=clubs[2]),
               Archer.objects.create(full_name='Volli Mets', gender='M', club=clubs[2])]


    Participant.objects.create(archer=Archer.objects.get(pk=1), event=comp, age_group='A', style='LB', group=choice(range(1,6)))

    comp = Event.objects.get(pk=1)

    for a in Archer.objects.all():
        Participant.objects.create(archer=a, event=comp, age_group='A', style='LB', group=choice(range(1,6)))
        if a.full_name == 'Ann Mets':
            # test if archer can participate in multiple styles
            Participant.objects.create(archer=a, event=comp, age_group='A', style='BU', group=choice(range(1,6)))

    for _ in range(20):
        Participant.objects.create(archer=Archer.objects.create(full_name=choice(first_names) + ' ' + choice(last_names), gender='M'),
                                   event=comp, age_group='A', style='LB', group=choice(range(1,6)))


def test_scoring():
    for comp in Event.objects.all():

        for p in comp.participants.all():
            for r in comp.rounds.all():
                sc, created = ScoreCard.objects.get_or_create(participant=p, round=r)
                if created:
                    # fill scorecard with arrows
                    for e in r.course.ends.all():
                        for a in range(e.nr_of_arrows):
                            Arrow.objects.create(scorecard=sc, end=e, ord=a)
                for e in r.course.ends.all():
                    for a in sc.arrows.filter(end__id=e.id):
                        scoring = eval(e.scoring) + [0]
                        score = choice(scoring)
                        a.score=score
                        a.save()

            for sc in p.scorecards.all():
                style = p.age_group + p.archer.gender + p.style
                a_name = p.archer.full_name
                r_name = sc.round.label
                cum_score = sum([a.score for a in sc.arrows.all()])
                print(style, a_name, r_name, cum_score)


def run_all_tests():
    build_base_data()
    test_event_creation()
    test_registration()
    test_scoring()
