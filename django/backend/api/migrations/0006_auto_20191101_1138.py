# Generated by Django 2.2.6 on 2019-11-01 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20191101_1110'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competition',
            options={'ordering': ['-start_date']},
        ),
    ]
