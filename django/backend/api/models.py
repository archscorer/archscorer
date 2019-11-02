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


class Archer(models.Model):
    full_name = models.CharField('full name', max_length=150, blank=False, default='Unnamed archer')  # full name <first_name last_name>
    gender = models.CharField('gender', max_length=1, choices=[('M', 'Male'),
                                                               ('F', 'Female')])
    club = models.CharField('club', max_length=150, blank=True)
    email = models.EmailField('email address', blank=True)
    phone = models.SlugField('phone number', max_length=20, blank=True)
    efaa_id = models.IntegerField('EFAA Archer ID')

class User(AbstractUser):
    archer = models.OneToOneField('Archer', on_delete=models.PROTECT)
    username = models.CharField('username', max_length=30, blank=True)
    email = models.EmailField('email address', unique=True)

    objects = LocalUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ['-date_joined']

class AgeGroup(models.Model):
    AGEGROUP_CHOICES = [('C', 'Cub'),
                        ('J', 'Junior'),
                        ('A', 'Adult'),
                        ('V', 'Veteran'),
                        ('S', 'Senior')]
    name = models.CharField('age group', max_length=1, blank=False, choices=AGEGROUP_CHOICES)

class Style(models.Model):
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
    name = models.CharField('Shooting style', max_length=5, blank=False, choices=STYLE_CHOICES)

class Course(models.Model):
    owner = models.ForeignKey('User', related_name='course', null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField('Course name', max_length=150, default='Unnamed course', blank=False)
    location = models.CharField(max_length=150, blank=True)

class End(models.Model):
    course = models.ForeignKey('Course', related_name='ends', on_delete=models.CASCADE)
    nr = models.CharField(max_length=10, blank=False)
    label = models.CharField(max_length=30, blank=True)
    arrows = models.PositiveSmallIntegerField(blank=False)  # number of max arrows that can be shot
    scoring = models.CharField(max_length=150, blank=False)

class Competition(models.Model):
    owner = models.ForeignKey('User', related_name='competitions', null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(default=timezone.localdate)
    registration_open = models.BooleanField(default=True)
    registration_due_date = models.DateField(default=timezone.localdate)

    name = models.CharField(max_length=150, default='Unnamed competition', blank=False)
    format = models.CharField(max_length=30, blank=True)
    description = models.TextField()

    courses = models.ManyToManyField('Course', related_name='competitions')

    class Meta:
        ordering = ['-start_date']

class Participant(models.Model):
    archer = models.ForeignKey(Archer, on_delete=models.PROTECT)
    competition = models.ForeignKey(Competition, on_delete=models.PROTECT)
    style = models.ForeignKey(Style, on_delete=models.PROTECT)
    age_group = models.ForeignKey(AgeGroup, on_delete=models.PROTECT)

class ScoreSheet(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
