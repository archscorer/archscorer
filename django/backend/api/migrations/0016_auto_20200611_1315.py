# Generated by Django 3.0.2 on 2020-06-11 13:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20200605_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='admins',
            field=models.ManyToManyField(blank=True, related_name='admin_clubs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='catering_choices',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='participant',
            name='food_choices',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='event',
            name='admins',
            field=models.ManyToManyField(blank=True, related_name='admin_events', to=settings.AUTH_USER_MODEL),
        ),
    ]
