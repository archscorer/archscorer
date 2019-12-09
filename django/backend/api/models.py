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


class User(AbstractUser):
    username = models.CharField('username', max_length=30, blank=True)
    email = models.EmailField('email address', unique=True)

    objects = LocalUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ['-date_joined']

class Club(models.Model):
    creator = models.ForeignKey('User', related_name='clubs_created', null=True, on_delete=models.SET_NULL)
    name = models.CharField('Club name', max_length=150, blank=False, default='Unnamed archery club')
    contact = models.TextField('Contact Information')
    description = models.TextField()

    class Meta:
        ordering = ['name']

class Archer(models.Model):
    full_name = models.CharField('Full Name', max_length=150, blank=False, default='Unnamed archer')  # full name <first_name last_name>
    gender = models.CharField('gender', max_length=1, default='U', choices=[('M', 'Male'),
                                                                            ('F', 'Female'),
                                                                            ('U', 'Unisex')])
    club = models.ForeignKey('Club', related_name='members', null=True, on_delete=models.CASCADE)
    email = models.EmailField('email address', blank=True)
    phone = models.CharField('phone number', max_length=20, blank=True)
    nat_id = models.CharField('National Archer ID', max_length=30, blank=True)

    user = models.OneToOneField('User', related_name='archer', null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['full_name']

class Course(models.Model):
    creator = models.ForeignKey('User', related_name='courses_created', null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField('Round name', max_length=150, default='Unnamed round', blank=False)
    description = models.TextField(blank=False)  # If creating custom non-standard course, describe its purpose
    location = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ['-created']

class End(models.Model):
    course = models.ForeignKey('Course', related_name='ends', on_delete=models.CASCADE)
    ord = models.IntegerField('End order', blank=False)
    label = models.CharField(max_length=30, blank=True)  # i.e 70 yards walk-up
    nr_of_arrows = models.PositiveSmallIntegerField(blank=False)  # number of max arrows that can be shot
    scoring = models.CharField(max_length=150, blank=False)

    class Meta:
        ordering = ['ord']

class Event(models.Model):
    TYPE_CHOICES = [('private', 'Private'),
                    ('club', 'Club'),
                    ('open', 'Open')]
    creator = models.ForeignKey('User', related_name='events_created', null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    date_start = models.DateField(default=timezone.localdate)
    date_end = models.DateField(default=timezone.localdate)
    is_open = models.BooleanField(default=True)

    name = models.CharField(max_length=150, default='Unnamed event', blank=False)
    description = models.TextField(blank=True)
    catering = models.BooleanField(default=False)
    type = models.CharField('event type', max_length=10, default='private', choices=TYPE_CHOICES)
    tags = models.CharField('event tags', max_length=255, blank=True)

    class Meta:
        ordering = ['-date_start']

class Round(models.Model):
    ord = models.IntegerField('Round order', blank=False)
    label = models.CharField('Label for round', max_length=150, blank=True)
    course = models.ForeignKey('Course', related_name='events', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', related_name='rounds', on_delete=models.CASCADE)
    is_open = models.BooleanField('is round open', default=False)
    start = models.DateTimeField('Round start time', blank=True, null=True)

    class Meta:
        ordering = ['ord']
        unique_together = ['ord', 'course', 'event']

class Participant(models.Model):
    AGEGROUP_CHOICES = [('C', 'Cub'),
                        ('J', 'Junior'),
                        ('A', 'Adult'),
                        ('V', 'Veteran'),
                        ('S', 'Senior')]
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
        ('TR', 'Traditional Recurve')
    ]
    created = models.DateTimeField(auto_now_add=True)
    archer = models.ForeignKey(Archer, related_name='events', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='participants', on_delete=models.CASCADE)
    age_group = models.CharField('age group', max_length=1, blank=False, choices=AGEGROUP_CHOICES)
    style = models.CharField('Shooting style', max_length=5, blank=False, choices=STYLE_CHOICES)
    eats = models.BooleanField(default=False)
    comments = models.CharField(max_length=255, blank=True)
    start_group = models.IntegerField(default=1)

    class Meta:
        ordering = ['created']
        unique_together = ['archer', 'event', 'style']

class ScoreCard(models.Model):
    participant = models.ForeignKey(Participant, related_name='scorecards', on_delete=models.CASCADE)
    round = models.ForeignKey(Round, related_name='rounds', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['participant', 'round']

class Arrow(models.Model):
    scorecard = models.ForeignKey(ScoreCard, related_name='arrows', on_delete=models.CASCADE)
    end = models.ForeignKey(End, related_name='arrows', on_delete=models.CASCADE)
    ord = models.IntegerField('arrow nr', blank=False)
    score = models.IntegerField('arrow score', blank=True, null=True)

    class Meta:
        ordering = ['end', 'ord']
