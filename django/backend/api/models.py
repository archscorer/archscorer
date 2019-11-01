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
    username = username = models.CharField('username', max_length=30, blank=True)
    email = models.EmailField('email address', unique=True)

    objects = LocalUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ['-date_joined']

class Competition(models.Model):
    owner = models.ForeignKey('User', related_name='competitions', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(default=timezone.localdate)

    name = models.CharField(max_length=150, blank=False)
    description = models.TextField()

    class Meta:
        ordering = ['-start_date']
