from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (BaseUserManager, AbstractUser)

# Create your models here.
class LocalUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

TYPE_CHOICES = [('private', 'Private'),
                ('club', 'Club'),
                ('open', 'Open')]

AGEGROUP_CHOICES = [('C', 'Cub'),
                    ('J', 'Junior'),
                    ('YA', 'Young Adult'),
                    ('A', 'Adult'),
                    ('V', 'Veteran'),
                    ('S', 'Senior'),
                    ('O', 'Open'),
                    ('U13', 'Under 13'),
                    ('U15', 'Under 15'),
                    ('U18', 'Under 18'),
                    ('U21', 'Under 21'),
                    ('50+', '50+')]

STYLE_CHOICES = [
    ('BB-C', 'Barebow Compound'),
    ('BB-R', 'Barebow Recurve'),
    ('BH-C', 'Bowhunter Compound'),
    ('BH-R', 'Bowhunter Recurve'),
    ('BL', 'Bowhunter Limited'),
    ('BU', 'Bowhunter Unlimited'),
    ('FS-C', 'Freestyle Limited Compound'),
    ('FS-R', 'Freestyle Limited Recurve'),
    ('FU', 'Freestyle Unlimited'),
    ('HB', 'Historic Longbow'),
    ('LB', 'Longbow'),
    ('TR', 'Traditional Recurve'),
    ('**', 'Variable'),
    ('R', 'Recurve'),
    ('C', 'Compound'),
    ('B', 'Barebow'),
    ('T', 'Traditional'),
    ('L', 'Longbow')]

LEVEL_CHOICES = [('A', 'A'),
                 ('B', 'B'),
                 ('C', 'C'),
                 ('*', '*')]

# NOTE also update src/statistics/Records.vue if changing these
RECORD_CHOICES = [
    ('flint', 'IFAA Flint'),
    ('indoor', 'IFAA Indoor'),
    ('animal', 'IFAA Animal (Marked Distances)'),
    ('field', 'IFAA Field'),
    ('hunter', 'IFAA Hunter')]

class User(AbstractUser):
    username = models.CharField('username', max_length=30, blank=True)
    email = models.EmailField('email address', unique=True)

    objects = LocalUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ['-date_joined']

class Association(models.Model):
    creator = models.ForeignKey(User, related_name='associations_created', null=True, on_delete=models.SET_NULL)
    name = models.CharField('Organisation name', max_length=150, blank=False, default='Unnamed archery association')
    name_short = models.CharField('Organisation name short', max_length=10, blank=True, default='***')
    contact = models.TextField('Contact Information')
    description = models.TextField()
    admins = models.ManyToManyField(User, related_name='admin_association', blank=True)

    class Meta:
        ordering = ['name']

class Club(models.Model):
    creator = models.ForeignKey(User, related_name='clubs_created', null=True, on_delete=models.SET_NULL)
    name = models.CharField('Club name', max_length=150, blank=False, default='Unnamed archery club')
    name_short = models.CharField('Club name short', max_length=10, blank=True, default='***')
    association = models.ManyToManyField(Association, related_name='clubs', blank=True)
    contact = models.TextField('Contact Information')
    description = models.TextField()
    admins = models.ManyToManyField(User, related_name='admin_clubs', blank=True)

    class Meta:
        ordering = ['name']

# sql to find duplicate archers from db
# SELECT full_name, count(full_name) FROM `api_archer` group by full_name having count(full_name) > 1
class Archer(models.Model):
    full_name = models.CharField('Full Name', max_length=150, blank=False, default='Unnamed archer')  # full name <first_name last_name>
    gender = models.CharField('gender', max_length=1, default='U', choices=[('M', 'Male'),
                                                                            ('F', 'Female'),
                                                                            ('U', 'Unisex')])
    club = models.ForeignKey(Club, related_name='members', null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField('email address', blank=True)
    phone = models.CharField('phone number', max_length=20, blank=True)
    nat_id = models.CharField('National Archer ID', max_length=30, blank=True)

    user = models.OneToOneField('User', related_name='archer', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['full_name']

class LevelClass(models.Model):
    # this is intended for level classes for archers (A, B, C, *)
    archer = models.ForeignKey(Archer, related_name='level_classes', on_delete=models.CASCADE)
    level = models.CharField('Level', max_length=1, blank=False, choices=LEVEL_CHOICES)
    age_group = models.CharField('age group', max_length=3, blank=False, choices=AGEGROUP_CHOICES)
    style = models.CharField('Shooting style', max_length=5, blank=False, choices=STYLE_CHOICES)
    date = models.DateField('Date of achievement', blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.EmailField(blank=True, null=True)

    class Meta:
        ordering = ['style', 'age_group']
        unique_together = ['style', 'age_group', 'archer']

class Course(models.Model):
    creator = models.ForeignKey(User, related_name='courses_created', null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField('Course name', max_length=150, default='Unnamed course', blank=False)
    description = models.TextField(blank=True)  # If creating custom non-standard course, describe its purpose
    location = models.CharField(max_length=150, blank=True)
    halves = models.BooleanField(default=False)
    # type 'Unit' has to be twice in the competition to account for records, 'Round' once
    type = models.CharField('Round/Unit', max_length=1, default='r', choices=[('u', 'Unit'),
                                                                              ('r', 'Round'),
                                                                              ('s', 'Shootoff')])
    format = models.CharField('Format', max_length=255, blank=True, choices=RECORD_CHOICES)

    class Meta:
        ordering = ['name']

class End(models.Model):
    course = models.ForeignKey(Course, related_name='ends', on_delete=models.CASCADE)
    ord = models.IntegerField('End order', blank=False)
    label = models.CharField(max_length=30, blank=True)  # i.e 70 yards walk-up
    nr_of_arrows = models.PositiveSmallIntegerField(blank=False)  # number of max arrows that can be shot
    scoring = models.CharField(max_length=150, blank=False)
    x = models.BooleanField('Target has x', default=True)

    class Meta:
        ordering = ['ord']

class Record(models.Model):
    archer = models.CharField('Archer name', max_length=255, blank=False)
    date = models.DateField('Date of achievement', blank=True, null=True)
    age_group = models.CharField('age group', max_length=3, blank=False, choices=AGEGROUP_CHOICES)
    gender = models.CharField('gender', max_length=1, blank=False, choices=[('M', 'Male'), ('F', 'Female')])
    style = models.CharField('Shooting style', max_length=5, blank=False, choices=STYLE_CHOICES)
    format = models.CharField('Format', max_length=255, blank=False, choices=RECORD_CHOICES)
    event = models.CharField('Event', max_length=255, blank=True)
    score = models.IntegerField('Record score', blank=False)
    # scope should be explained - country code (EE, LAT, etc) for national ones, EU, USA for unions, W for world
    scope = models.CharField('record scope (EE/EU/W)', max_length=50, blank=False, default='EE')

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.EmailField(blank=True, null=True)

    class Meta:
        ordering = ['age_group', 'style', '-date']
        unique_together = ['format', 'age_group', 'gender', 'style', 'scope', 'date']

class Series(models.Model):
    creator = models.ForeignKey(User, related_name='series_created', null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    date_start = models.DateField(default=timezone.localdate)
    date_end = models.DateField(default=timezone.localdate)

    name = models.CharField(max_length=150, default='Unnamed Series', blank=False)
    description = models.TextField(blank=True)
    type = models.CharField('event type', max_length=10, default='private', choices=TYPE_CHOICES)

    points_max = models.IntegerField('Maximum point score for the first place', default=10)

    # use None for no restriction. Otherwise archer__club__association should be used as limitation (i.e FAAE)
    participant_restriction = models.CharField('i.e. "archer__club__association:FAAE"', max_length=255, blank=True, null=True, default=None)
    participant_min = models.IntegerField('Minimum nr of events for final ranking', default=1)
    participant_max = models.IntegerField('Maximum nr of envets used for final ranking', default=None, null=True)
    # Aimed to accommodate club cup and comparing clubs
    club_ranking = models.BooleanField(default=False)
    club_ranking_max = models.IntegerField('Max nr of club members to contribute points to club per class', default=3)
    ignore_gender = models.CharField('age_style to merge gender (A_TR, V_TR)', max_length=50, blank=True, default='')

    class Meta:
        ordering = ['-date_end']

class Event(models.Model):
    creator = models.ForeignKey(User, related_name='events_created', null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    date_start = models.DateField(default=timezone.localdate)
    date_end = models.DateField(default=timezone.localdate)
    is_open = models.BooleanField(default=True)
    # TODO: archive is implemented on client level, api currenlty is unaware of it
    archive = models.BooleanField(default=False)

    name = models.CharField(max_length=150, default='Unnamed event', blank=False)
    location = models.CharField(max_length=150, default='', blank=True)
    organizer = models.CharField(max_length=150, default='', blank=True)
    judges = models.CharField(max_length=255, default='', blank=True)
    description = models.TextField(blank=True)
    catering = models.BooleanField('Provide catering', default=False)
    catering_choices = models.CharField(max_length=255, blank=True)
    type = models.CharField('event type', max_length=10, default='private', choices=TYPE_CHOICES)
    association = models.ForeignKey(Association, related_name='events', null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.CharField('event tags', max_length=255, blank=True)
    admins = models.ManyToManyField(User, related_name='admin_events', blank=True)
    # TODO: recrords could also be joice, default beeing 'Training' -- no records
    records = models.CharField('record category (nat/EM/MM)', max_length=50, blank=True, default='')
    use_level_class = models.BooleanField('Use Level Classes', default=False)
    ignore_gender = models.CharField('age_style to merge gender (A_TR, V_TR)', max_length=50, blank=True, default='')
    age_style_used = models.TextField('age_style classes used in the event', blank=True)

    series = models.ForeignKey(Series, related_name='stages', null=True, blank=True, on_delete=models.SET_NULL)


    class Meta:
        ordering = ['-date_start']

class Round(models.Model):
    ord = models.IntegerField('Round order', blank=False)
    label = models.CharField('Label for round', max_length=150, blank=True)
    course = models.ForeignKey(Course, related_name='events', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='rounds', on_delete=models.CASCADE)
    is_open = models.BooleanField('is round open', default=False)
    start = models.DateTimeField('Round start time', blank=True, null=True)

    class Meta:
        ordering = ['ord']
        unique_together = ['ord', 'course', 'event']

class Participant(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, related_name='participants', on_delete=models.CASCADE)
    # archer here now is only for scoring in the event, after the envent it can be safely removed from the database without
    # affecting past events, although currently it is still protected.
    archer = models.ForeignKey(Archer, related_name='events', on_delete=models.PROTECT)
    archer_rep = models.CharField('archer representation in a form "club_short|association_short"', max_length=20, default='|')
    gender = models.CharField('gender', max_length=1, default='U', choices=[('M', 'Male'),
                                                                            ('F', 'Female'),
                                                                            ('U', 'Unisex')]) # from archer
    full_name = models.CharField('Full Name', max_length=150, blank=False, default='Unnamed archer') # from archer
    age_group = models.CharField('age group', max_length=3, blank=False, choices=AGEGROUP_CHOICES)
    style = models.CharField('Shooting style', max_length=5, blank=False, choices=STYLE_CHOICES)
    food = models.BooleanField(default=False)
    food_choices = models.CharField(max_length=255, blank=True)
    comments = models.CharField('Comments to organiser', max_length=255, blank=True)
    session = models.CharField('Session', max_length=10, blank=True, default='')
    group = models.IntegerField('Group nr', default=1)
    group_pos = models.CharField('Archer position', max_length=1, blank=True, default='')
    level_class = models.CharField('Level class', max_length=1, blank=True, default='')

    class Meta:
        ordering = ['created']
        unique_together = ['archer', 'event', 'style', 'age_group']

class ScoreCard(models.Model):
    participant = models.ForeignKey(Participant, related_name='scorecards', on_delete=models.CASCADE)
    round = models.ForeignKey(Round, related_name='scorecards', on_delete=models.CASCADE)
    score = models.IntegerField('Final score', default=None, null=True)
    spots = models.IntegerField('nr of "x" or equivalent', default=None, null=True)

    class Meta:
        ordering = ['participant__group_pos']
        unique_together = ['participant', 'round']

class Arrow(models.Model):
    scorecard = models.ForeignKey(ScoreCard, related_name='arrows', on_delete=models.CASCADE)
    end = models.ForeignKey(End, related_name='arrows', on_delete=models.CASCADE)
    ord = models.IntegerField('arrow nr', blank=False)
    score = models.IntegerField('arrow score', blank=True, null=True)
    x = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.EmailField(blank=True, null=True)

    class Meta:
        ordering = ['end', 'ord']
